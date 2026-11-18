"""section_v2_1: page maps, table review statuses, repeated headings, stricter heading/front-matter rules,
data-row and glyph-encoding detection. section_v2 behaviour must stay unchanged."""

from dataclasses import replace
from pathlib import Path

from app.ingest import chunking
from app.ingest.chunking import ChunkingProfile, DocumentInfo, chunk_document
from app.ingest.pdf_layout import Line, _flat_runs, _numbers_are_boilerplate, _page_runs, heading_signal
from app.ingest.pdf_page_map import _translator, clean, page_at, page_lookup


class WordCounter:
    def count(self, text: str) -> int:
        return len(text.split())


V2 = ChunkingProfile(
    name="t_v2", max_tokens=80, target_min_tokens=30, merge_tail_below_tokens=10, hard_max_tokens=90,
    overlap_tokens=10, front_matter_min_words=8, tokenizer_path=Path("unused"), tokenizer_sha256="",
    normalizer="v2", pdf_layout=True, content_detection=True,
)
V21 = replace(V2, name="t_v2_1", page_maps=True, table_review=True, rules="v2_1")
INFO = DocumentInfo("PDF-1", "PDF-1@v1", "Caregiver Guide", "gaps", "official_training_manual", "en", {"graphic": 1})


def doc(body: str) -> str:
    return "# Caregiver Guide\n\nTên tài liệu: x\n\n<!-- ORIGINAL_DOCUMENT_BODY -->\n" + body


def words(n: int) -> str:
    return "".join(chr(97 + int(d)) for d in str(n))


def paged(pages: dict[int, list[str]]) -> str:
    return doc("".join(f"<!-- SOURCE_PDF_PAGE {n} -->\n" + "\n".join(lines) + "\n"
                       for n, lines in sorted(pages.items())))


def prose(n: int) -> list[str]:
    return [f"The {words(n)} page explains part {words(i)} of the caregiver programme in plain words."
            for i in range(3)]


# ---------------------------------------------------------------- page maps


def test_page_offsets_survive_the_old_converters_join_and_clean():
    pages = ["Alpha text.\n\n\n\nmore alpha", "", "Beta text."]
    raw = "\n\n".join(pages)
    body, translate = clean(raw), _translator(raw)
    cursor, spans = 0, []
    for text in pages:
        spans.append((translate(cursor), translate(cursor + len(text))))
        cursor += len(text) + 2
    assert body[spans[0][0]:spans[0][1]].split() == pages[0].split()
    assert body[spans[2][0]:spans[2][1]] == "Beta text."


def test_page_lookup_ignores_unverified_maps_and_empty_pages():
    pm = {"verified": True, "pages": [{"page": 1, "char_start": 10, "char_end": 20, "chars": 10},
                                      {"page": 2, "char_start": 22, "char_end": 22, "chars": 0},
                                      {"page": 3, "char_start": 24, "char_end": 40, "chars": 16}]}
    lookup = page_lookup(pm)
    assert [p for *_, p in lookup] == [1, 3]
    assert page_at(lookup, 12) == 1 and page_at(lookup, 21) == 3 and page_at(lookup, 30) == 3
    assert page_lookup(pm | {"verified": False}) == []


def test_chunks_without_any_page_source_are_flagged_and_not_retrievable(monkeypatch):
    monkeypatch.setattr(chunking, "_page_lookup", lambda source_id, document: None)
    chunks = chunk_document(doc("\n".join(prose(1)) + "\n"), INFO, V21, WordCounter()).chunks
    assert chunks and all(c.completeness_status == "page_provenance_incomplete" and not c.retrieval_eligible
                          for c in chunks)


# ---------------------------------------------------------------- running titles and repeated headings


def test_running_title_uses_contiguous_runs_not_min_max():
    assert _page_runs({3, 40, 41, 43, 44, 270}) == [(40, 44)]  # contents page 3 and annex page 270 are isolated
    assert _page_runs({10, 12, 14}) == [(10, 14)]  # printed on alternate pages


def test_footer_numbers_must_be_constant_or_follow_the_page():
    assert _numbers_are_boilerplate([(p, [26, 29]) for p in range(1, 9)])  # "Vol. 26 No. 29"
    assert _numbers_are_boilerplate([(p, [p + 10]) for p in range(1, 9)])  # printed page number
    assert not _numbers_are_boilerplate([(p, [p, 3 * p, 5 * p]) for p in range(1, 9)])  # data row


def test_repeated_real_headings_are_kept_in_v2_1_but_deduplicated_in_v2():
    # As in the WHO workbook: a session heading repeated on few pages (8 of 80 = 10%) but spread over the book.
    pages = {}
    for n in range(1, 81):
        pages[n] = ["What we will learn today", *prose(n)] if n % 10 == 1 else prose(n)
    v2 = "\n".join(c.content for c in chunk_document(paged(pages), INFO, V2, WordCounter()).chunks)
    v21 = "\n".join(c.content for c in chunk_document(paged(pages), INFO, V21, WordCounter()).chunks)
    assert v2.count("What we will learn today") <= 1  # section_v2 behaviour is unchanged
    assert v21.count("What we will learn today") == 8


# ---------------------------------------------------------------- headings, front matter, data rows, glyphs


def test_bare_integer_line_is_a_heading_only_in_heading_case_under_v2_1():
    prev = Line("Items were scored by carers.", 0, 1, 5, False)
    nxt = Line("Scores ranged widely across the sample.", 0, 1, 5, False)
    footnote = Line("69 For all ABC subscales items were rated on four", 0, 1, 5, False)
    assert heading_signal(footnote, prev, nxt, "v2") is not None  # the v2 false positive, kept for reproducibility
    assert heading_signal(footnote, prev, nxt, "v2_1") is None
    assert heading_signal(Line("3 Methods", 0, 1, 5, False), prev, nxt, "v2_1") == (1, "numbered")
    assert heading_signal(Line("2.1 Participants", 0, 1, 5, False), prev, nxt, "v2_1") == (2, "numbered")


def test_runs_of_numeric_data_rows_are_flattened_tables_in_v2_1():
    rows = ["Community care 208.43 (476.77) 259.77 (754.44) –51.34 ( –371.73 to 269.05)",
            "Hospital care 226.12 (913.45) 98.93 (291.66) 127.19 ( –267.49 to 521.87)",
            "Carer training 5.89 (25.96) 0.00 ( –) 5.89 ( –4.97 to 16.77)"]
    kept = [Line(t, 0, 1, 1, False) for t in ["The costs were compared between arms of the trial.", *rows]]
    assert _flat_runs(kept, "v2") == set()
    assert _flat_runs(kept, "v2_1") == {1, 2, 3}


def test_author_marks_deep_in_a_report_are_not_front_matter():
    region_rows = ", ".join(f"Health Board {words(n).title()} {n}" for n in range(1, 8))
    pages = {n: prose(n) for n in range(1, 61)}
    pages[40] = [f"Carers were recruited from {region_rows} across the study area as planned."]
    chunks = chunk_document(paged(pages), INFO, V21, WordCounter()).chunks
    deep = [c for c in chunks if "Health Board" in c.content]
    assert deep and all(c.section_type != "front_matter_detected" for c in deep)


def test_glyph_id_text_is_flagged_and_excluded():
    body = "Normal sentence about the session plan.\n\n/gid00002/gid00039/gid00039 /gid00042/gid00033 text\n"
    chunks = chunk_document(doc(body), INFO, V21, WordCounter()).chunks
    bad = [c for c in chunks if "/gid" in c.content]
    assert bad and all(c.completeness_status == "text_encoding_lost" and not c.retrieval_eligible for c in bad)


def test_flattened_table_status_needs_a_recovered_table_on_every_page(monkeypatch):
    cells = ["Outcome", "No serious", "serious", "Not", "CRITICAL", "Low", "High", "None", "Moderate"]
    pages = {n: prose(n) for n in range(1, 21)}
    pages[18] = [*prose(18), *cells]
    monkeypatch.setattr(chunking, "recovered_table_pages", lambda sid: {18})
    flat = [c for c in chunk_document(paged(pages), INFO, V21, WordCounter()).chunks if "No serious" in c.content]
    assert flat and all(c.completeness_status == "table_recovered_pending_review" and not c.retrieval_eligible
                        for c in flat)
    monkeypatch.setattr(chunking, "recovered_table_pages", lambda sid: set())
    flat = [c for c in chunk_document(paged(pages), INFO, V21, WordCounter()).chunks if "No serious" in c.content]
    assert flat and all(c.completeness_status == "table_structure_unrecoverable" for c in flat)


def test_table_caption_starts_an_excluded_region_and_prose_before_it_stays():
    pages = {n: prose(n) for n in range(1, 21)}
    pages[9] = ["Carers described the services they had used before the trial started.",
                "TABLE 1 Respondents by region", "Region n (%) Board n (%)", "Wales 32 (20.1) Aneurin Bevan 12 (7.5)",
                "England 40 (25.2) Other 3 (1.9)"]
    chunks = chunk_document(paged(pages), INFO, V21, WordCounter()).chunks
    table = [c for c in chunks if "TABLE 1" in c.content]
    assert table and all(not c.retrieval_eligible and c.completeness_status.startswith("table_") for c in table)
    assert all("TABLE 1" not in c.content for c in chunks if "services they had used" in c.content)
    assert any(c.retrieval_eligible and "services they had used" in c.content for c in chunks)


def test_short_effect_size_fragment_is_not_retrievable():
    pages = {n: prose(n) for n in range(1, 21)}
    pages[15] = [*prose(15), "", "None 289 295 – SMD 0.3 SD higher", "", *prose(150)]
    chunks = chunk_document(paged(pages), INFO, V21, WordCounter()).chunks
    frag = [c for c in chunks if "SMD 0.3" in c.content]
    assert frag and all(not c.retrieval_eligible for c in frag)


def test_table_rows_inside_prose_are_held_back(monkeypatch):
    def run(row: str, recovered: set[int]):
        pages = {n: prose(n) for n in range(1, 21)}
        pages[12] = ["Results for the child outcomes were pooled across the trials as follows here.", row]
        monkeypatch.setattr(chunking, "recovered_table_pages", lambda sid: recovered)
        return [c for c in chunk_document(paged(pages), INFO, V21, WordCounter()).chunks if "0.15" in c.content]

    four = "Language development 0.00 -0.15, 0.15 4 was the pooled estimate for attachment outcomes."
    held = run(four, {12})  # 4 numbers in a row on a page with a recovered table: its rows, held for review
    assert held and all(c.completeness_status == "table_recovered_pending_review" and not c.retrieval_eligible
                        for c in held)
    assert all(c.retrieval_eligible for c in run(four, set()))  # 4 numbers without table evidence stay
    eight = "Language development 0.00 -0.15, 0.15 4 0.23 0.16, 0.30 1 Attachment was also measured."
    assert all(c.completeness_status == "table_structure_unrecoverable" and not c.retrieval_eligible
               for c in run(eight, set()))
