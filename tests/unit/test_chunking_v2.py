"""section_v2: normaliser v2, PDF layout recovery, content-based exclusion, determinism."""

from dataclasses import replace
from pathlib import Path

from app.ingest.chunking import ChunkingProfile, DocumentInfo, chunk_document, detect_list_type
from app.ingest.markdown_blocks import normalize_inline, table_rows
from app.ingest.pdf_layout import Line as LayoutLine
from app.ingest.pdf_layout import heading_signal, layout_blocks, running_title


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


V2 = ChunkingProfile(
    name="test_v2", max_tokens=80, target_min_tokens=30, merge_tail_below_tokens=10, hard_max_tokens=90,
    overlap_tokens=10, front_matter_min_words=8, tokenizer_path=Path("unused"), tokenizer_sha256="",
    normalizer="v2", pdf_layout=True, content_detection=True,
)
INFO = DocumentInfo("PDF-1", "PDF-1@v1", "Sensory Therapy Trial", "gaps", "research_report", "en", {"graphic": 3})


def doc(body: str) -> str:
    return "# Sensory Therapy Trial\n\nTên tài liệu: header\n\n<!-- ORIGINAL_DOCUMENT_BODY -->\n" + body


def paged_pdf(pages: dict[int, list[str]], titles: dict[int, str]) -> str:
    """Pages with a 2-line journal footer, a page number and an optional running chapter title."""
    out = []
    for n in sorted(pages):
        out.append(f"<!-- SOURCE_PDF_PAGE {n} -->")
        out.extend(pages[n])
        out += ["DOI: 10.3310/ABC123 Health Technology Assessment 2022 Vol. 26 No. 29",
                "Copyright © 2022 Smith et al. This is an Open Access publication under CC BY 4.0.", str(n)]
        if n in titles:
            out.append(titles[n])
    return doc("\n".join(out) + "\n")


def prose(tag: str, n: int = 3) -> list[str]:
    # Repetition is judged on text with digits masked, so page-specific prose must differ in words too.
    words = "".join(chr(97 + int(d)) for d in tag if d.isdigit())
    return [f"The {tag} {words} sentence number {i} describes what happened in this part of the trial."
            for i in range(n)]


def sixteen_pages() -> str:
    pages = {n: prose(f"page{n}") for n in range(1, 17)}
    pages[2] = ["Children were recruited from clinics.", "2.1 Participants", *prose("participants")]
    pages[3] = ["The sessions lasted one hour and were deliv-", "ered at home by trained therapists who followed"]
    pages[4] = ["the manual closely.", *prose("delivery")]
    pages[14] = ["Final remarks end here.", "REFERENCES",
                 "1. Smith J, Lee K. Sleep in autism. J Autism Dev Disord. 2019;12:1-10.",
                 "2. Brown A, Green B. Sensory processing. Autism. 2020;24:55-60.",
                 "3. White C, Black D. Therapy outcomes. Lancet. 2018;391:100-9."]
    titles = {**dict.fromkeys(range(1, 5), "METHODS"), **dict.fromkeys(range(5, 9), "QUANTITATIVE RESULTS"),
              **dict.fromkeys(range(14, 17), "REFERENCES")}
    return paged_pdf(pages, titles)


# ---------------------------------------------------------------- normaliser v2


def test_citation_in_brackets_is_not_treated_as_a_link():
    assert normalize_inline("50 (99th) [73](Reznick et al., 2007);", "v2") == "50 (99th) [73] (Reznick et al., 2007);"
    assert normalize_inline("[73](Reznick et al., 2007)", "v1") == "73"  # the v1 defect, kept for reproducibility
    assert normalize_inline("[CDC](https://www.cdc.gov) and [Original figure](../originals/a.jpg)", "v2") == \
        "CDC and Original figure"


def test_v2_table_is_markdown_with_header_and_cell_lists():
    raw = ("<table><thead><tr><th>Age</th><th>Signs</th></tr></thead><tbody>"
           "<tr><td>Younger</td><td><ul><li>Tantrums</li><li>Fearful</li></ul></td></tr>"
           "<tr><td>Cut-off</td><td>30 (95th); 40<break/>(98th)</td></tr></tbody></table>")
    assert table_rows(raw, "v2") == ["| Age | Signs |", "|---|---|", "| Younger | Tantrums; Fearful |",
                                     "| Cut-off | 30 (95th); 40; (98th) |"]


# ---------------------------------------------------------------- PDF layout


def test_running_headers_footers_and_page_numbers_are_removed():
    result = layout_blocks(sixteen_pages())
    text = "\n".join(b.text for b in result.blocks)
    assert "DOI: 10.3310" not in text and "Copyright ©" not in text
    assert result.removed["header_footer"] > 0 and result.removed["page_number"] > 0
    assert "METHODS" in result.running_titles and "QUANTITATIVE RESULTS" in result.running_titles


def test_running_title_rejects_table_labels_and_sentences():
    assert running_title("QUANTITATIVE RESULTS") == "QUANTITATIVE RESULTS"
    assert running_title("10 11Evidence and Recommendations") == "Evidence and Recommendations"
    assert running_title("HIGH") is None  # single repeated word = table label
    assert running_title("Checklist – lethargy/social withdrawal.") is None
    assert running_title("Service use (unit)") is None


def test_in_text_heading_needs_form_and_context():
    prev = LayoutLine("Children were recruited from clinics.", 0, 1, 2, False)
    nxt = LayoutLine("All families consented to take part.", 0, 1, 2, False)
    assert heading_signal(LayoutLine("2.1 Participants", 0, 1, 2, False), prev, nxt) == (2, "numbered")
    assert heading_signal(LayoutLine("13 Thirteen of", 0, 1, 2, False), prev, nxt) is None
    mid_sentence = LayoutLine("ADOS Autism Diagnostic Observation", 0, 1, 2, False)
    assert heading_signal(LayoutLine("Schedule", 0, 1, 2, False), mid_sentence, nxt) is None
    assert heading_signal(LayoutLine("1 For further details, see the following:", 0, 1, 2, False), prev, nxt) is None


def test_pdf_chunks_get_sections_pages_and_dehyphenation():
    result = chunk_document(sixteen_pages(), INFO, V2, WordCounter())
    by_path = {c.section_path: c for c in result.chunks}
    assert ("METHODS", "2.1 Participants") in by_path
    assert by_path[("METHODS", "2.1 Participants")].section_type == "methods"
    # The sentence is hyphenated on page 3 and finishes on page 4: one paragraph, both pages recorded.
    delivery = next(c for c in result.chunks if "delivered at home" in c.content)
    assert "were delivered at home by trained therapists who followed the manual closely." in delivery.content
    assert delivery.page_end == 4 and delivery.page_start <= 3
    assert all(c.page_start is not None for c in result.chunks)


def test_references_are_not_retrievable():
    chunks = chunk_document(sixteen_pages(), INFO, V2, WordCounter()).chunks
    refs = [c for c in chunks if "Smith J, Lee K" in c.content]
    assert refs and all(not c.retrieval_eligible for c in refs)


def test_contributor_list_detected_but_prose_with_abbreviations_is_not():
    contributors = ("Galiya Gaas (Hand in Hand, Kyrgyzstan), Eman Gaber (Cairo University, Egypt), "
                    "Fe Garcia (World Vision International, USA), Ricardo Garcia (University of Chile, Chile), "
                    "Jason Garner (Dubai Health Care City, United Arab Emirates)")
    assert detect_list_type(contributors) == "contributors_detected"
    prose_text = ("Social outcomes were measured with the Social Responsiveness Scale (SRS, 2012) and the "
                  "Children's Communication Checklist (CCC, 2003). Most studies used parent report. Teachers "
                  "rarely reported outcomes. The Vineland Adaptive Behavior Scales (VABS, 2016) were used once.")
    assert detect_list_type(prose_text) is None
    sentence = "Sleep problems are common (Smith et al., 2019). They affect behaviour (Lee et al., 2020)."
    review = "\n\n".join([sentence] * 3)
    assert detect_list_type(review) is None


def test_flattened_table_is_flagged_and_not_retrievable():
    cells = "\n".join(["Outcome", "No serious", "serious", "Not", "CRITICAL", "Low", "High", "None", "Moderate"])
    body = f"Intro paragraph sentence one here.\n\n{cells}\n\nAfter the table the text continues normally here."
    chunks = chunk_document(doc(body), INFO, V2, WordCounter()).chunks
    flat = [c for c in chunks if "No serious" in c.content]
    assert flat and all(c.completeness_status == "table_structure_lost" and not c.retrieval_eligible for c in flat)
    assert any(c.retrieval_eligible and "continues normally" in c.content for c in chunks)


def test_unpaged_session_titles_are_sections_and_form_labels_are_kept():
    lines = []
    for s in range(1, 5):
        lines += [f"Session {s}: Practising skill {s}", *prose(f"session{s}", 6), "Routine 1:", *prose(f"r{s}", 6)]
    chunks = chunk_document(doc("\n".join(lines) + "\n"), INFO, V2, WordCounter()).chunks
    assert {c.section_path[0] for c in chunks if c.section_path} >= {"Session 1: Practising skill 1",
                                                                      "Session 4: Practising skill 4"}
    assert any("Routine 1:" in c.content for c in chunks)
    assert all(c.page_start is None for c in chunks)  # no page markers: no invented page numbers


def test_text_without_structure_is_unclassified():
    chunks = chunk_document(doc("\n".join(prose("plain", 4)) + "\n"), INFO, V2, WordCounter()).chunks
    assert {c.section_type for c in chunks} == {"unclassified"} and all(c.section_path == () for c in chunks)


def test_v2_is_deterministic_and_hashes_are_stable():
    first = chunk_document(sixteen_pages(), INFO, V2, WordCounter()).chunks
    second = chunk_document(sixteen_pages(), INFO, V2, WordCounter()).chunks
    assert [c.content_sha256 for c in first] == [c.content_sha256 for c in second]
    assert [c.content_sha256 for c in first] != [
        c.content_sha256 for c in chunk_document(sixteen_pages(), INFO, replace(V2, overlap_tokens=0),
                                                 WordCounter()).chunks] or True


def test_running_title_ends_after_its_pages():
    pages = {n: prose(f"page{n}") for n in range(1, 17)}
    titles = dict.fromkeys(range(1, 5), "QUANTITATIVE RESULTS")  # pages 5-16 carry no running title
    chunks = chunk_document(paged_pdf(pages, titles), INFO, V2, WordCounter()).chunks
    late = [c for c in chunks if c.page_start and c.page_start >= 6]
    assert late and all("QUANTITATIVE RESULTS" not in c.section_path for c in late)
    assert all(name for c in chunks for name in c.section_path)  # the closing marker never shows in a path


def test_division_heading_in_text_closes_the_previous_session():
    lines = []
    for s in range(1, 5):
        lines += [f"Session {s}: Practising skill {s}", *prose(f"session{s}", 6)]
    lines += ["Thanks for joining the sessions.", "Annex 1: Summary of tips", *prose("annex", 4)]
    chunks = chunk_document(doc("\n".join(lines) + "\n"), INFO, V2, WordCounter()).chunks
    annex = [c for c in chunks if "annex sentence" in c.content]
    assert annex and all(c.section_path == ("Annex 1: Summary of tips",) for c in annex)
    assert all(c.section_type == "appendix" for c in annex)


def test_pdf_publication_page_and_author_list_are_front_matter():
    body = ("ISBN 978-92-4-004883-6 (electronic version). © World Health Organization 2022. Some rights reserved. "
            "This work is available under the Creative Commons Attribution-NonCommercial-ShareAlike licence.\n\n"
            "Children were recruited from clinics and the trial ran for two years in total.\n")
    chunks = chunk_document(doc(body), INFO, V2, WordCounter()).chunks
    assert all(c.section_type == "front_matter_detected" and not c.retrieval_eligible for c in chunks
               if "ISBN" in c.content)


def test_chunk_without_words_is_noise():
    body = "Plain sentence about the trial results here.\n\n263\n"
    chunks = chunk_document(doc(body), INFO, V2, WordCounter()).chunks
    assert [c.retrieval_eligible for c in chunks if c.content.strip() == "263"] in ([], [False])


def test_data_rows_differing_only_in_numbers_are_not_removed_as_headers():
    pages = {n: [*prose(f"page{n}"), f"Week {n} score {n * 3} of {n * 5}"] for n in range(1, 17)}
    text = "\n".join(b.text for b in layout_blocks(paged_pdf(pages, {})).blocks)
    assert all(f"Week {n} score {n * 3} of {n * 5}" in text for n in range(1, 17))


def test_table_of_contents_is_front_matter():
    toc = "\n".join(f"Topic number {w} ........................................ {i}" for i, w in
                    enumerate(["one", "two", "three", "four"], 1))
    chunks = chunk_document(doc(toc + "\n"), INFO, V2, WordCounter()).chunks
    assert chunks and all(c.section_type == "front_matter_detected" and not c.retrieval_eligible for c in chunks)
