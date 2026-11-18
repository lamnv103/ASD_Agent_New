from pathlib import Path

import pytest

from app.ingest.chunking import ChunkingProfile, DocumentInfo, chunk_document, classify_section
from app.ingest.markdown_blocks import FormatError, normalize_inline, parse_blocks, table_rows


class WordCounter:
    """Deterministic stand-in for the real tokenizer: one token per whitespace-separated word."""

    def count(self, text: str) -> int:
        return len(text.split())


PROFILE = ChunkingProfile(
    name="test", max_tokens=60, target_min_tokens=30, merge_tail_below_tokens=10, hard_max_tokens=70,
    overlap_tokens=10, front_matter_min_words=8, tokenizer_path=Path("unused"), tokenizer_sha256="",
)


def info(role: str = "core", gaps: dict | None = None) -> DocumentInfo:
    return DocumentInfo("SRC-1", "SRC-1@v1", "A Study of Sleep", role, "research", "en", gaps or {})


def doc(body: str) -> str:
    return "# A Study of Sleep\n\nTên tài liệu: header that must be ignored\n\n<!-- ORIGINAL_DOCUMENT_BODY -->\n" + body


def sentences(n: int, word: str = "word") -> str:
    return " ".join(f"{word.capitalize()} number {i} is here in this sentence." for i in range(n))


# ---------------------------------------------------------------- markdown_blocks


def test_normalize_strips_markup_and_citation_superscripts():
    text = 'Autism<sup>1,2</sup> is <italic>common</italic> &lt; [](http://x) [CDC](https://cdc.gov) <sup>a</sup>'
    assert normalize_inline(text) == "Autism is common < CDC a"


def test_table_rows_are_pipe_joined():
    raw = "<table><tr><th>Drug</th><th>Dose</th></tr><tr><td>A</td><td><bold>1 mg</bold></td></tr></table>"
    assert table_rows(raw) == ["Drug | Dose", "A | 1 mg"]


def test_header_before_body_marker_is_ignored_and_pages_are_tracked():
    blocks = parse_blocks(doc("<!-- SOURCE_PDF_PAGE 3 -->\nSome text.\n"))
    assert [b.kind for b in blocks] == ["page", "paragraph"]
    assert blocks[0].page == 3 and "header" not in blocks[1].text


def test_missing_body_marker_is_an_error():
    with pytest.raises(FormatError):
        parse_blocks("# Title\n\nno marker")


# ---------------------------------------------------------------- chunking


def test_chunks_never_cross_headings_and_overlap_stays_inside_section():
    body = f"## A Study of Sleep\n\n### Introduction\n\n{sentences(12)}\n\n### Results\n\n{sentences(3, 'result')}\n"
    chunks = chunk_document(doc(body), info(), PROFILE, WordCounter()).chunks
    assert {c.section_path for c in chunks} == {("Introduction",), ("Results",)}
    results = [c for c in chunks if c.section_path == ("Results",)]
    assert len(results) == 1 and not results[0].has_overlap and "Result" in results[0].content
    intro = [c for c in chunks if c.section_path == ("Introduction",)]
    assert len(intro) >= 2 and intro[1].has_overlap
    assert all(c.token_count <= PROFILE.hard_max_tokens for c in chunks)


def test_front_matter_keeps_prose_and_drops_metadata():
    body = ("## A Study of Sleep\n\nJane Doe 1\n\n"
            "Copyright © 2024 the authors, distributed under the terms of CC BY.\n\n"
            "Sleep problems are common in autistic children and affect daytime behaviour and family life.\n\n"
            "### Introduction\n\nText.\n")
    result = chunk_document(doc(body), info(), PROFILE, WordCounter())
    front = [c for c in result.chunks if c.section_type == "abstract_inferred"]
    assert len(front) == 1 and "Sleep problems" in front[0].content
    assert result.dropped["front_matter_metadata"] > 0


def test_table_keeps_caption_and_footnotes_together():
    body = ("## A Study of Sleep\n\n### Results\n\nTable 1\n\nMelatonin dosing by age.\n\n"
            "<table><tr><th>Age</th><th>Dose</th></tr><tr><td>3-5</td><td>1 mg</td></tr></table>\n\n"
            "mg, milligram.\n\nNext paragraph of normal results text continues here.\n")
    chunks = chunk_document(doc(body), info(), PROFILE, WordCounter()).chunks
    table = [c for c in chunks if c.content_kind == "table"]
    assert len(table) == 1
    assert table[0].content.startswith("Table 1") and "Age | Dose" in table[0].content
    assert table[0].content.endswith("mg, milligram.")
    assert any("Next paragraph" in c.content for c in chunks if c.content_kind == "text")


def test_tables_after_references_are_retrievable_floating_tables():
    body = ("## A Study of Sleep\n\n### References\n\n1. Smith J. Sleep. 2020.\n\n"
            "<table><tr><td>Level 1</td><td>Sleep hygiene</td></tr></table>\n")
    chunks = chunk_document(doc(body), info(), PROFILE, WordCounter()).chunks
    refs = [c for c in chunks if c.section_type == "references"]
    floating = [c for c in chunks if c.section_type == "floating_table"]
    assert refs and not refs[0].retrieval_eligible
    assert floating and floating[0].retrieval_eligible and floating[0].section_path == ("Tables",)


def test_missing_components_are_never_hidden():
    body = "## A Study of Sleep\n\n### Results\n\nAs shown in Figure 2, sleep improved.\n\nOther text without refs.\n"
    plain = chunk_document(doc(body), info(), PROFILE, WordCounter()).chunks
    assert plain[0].completeness_status == "references_missing_component"
    gaps = chunk_document(doc("## A Study of Sleep\n\n### Results\n\nPlain text.\n"),
                          info("gaps", {"graphic": 2}), PROFILE, WordCounter()).chunks
    assert gaps[0].completeness_status == "document_has_gaps" and "graphic" in gaps[0].missing_context


def test_document_without_subheadings_is_chunked_as_body():
    body = f"<!-- SOURCE_PDF_PAGE 1 -->\n{sentences(6)}\n\n<!-- SOURCE_PDF_PAGE 2 -->\n{sentences(6)}\n"
    chunks = chunk_document(doc(body), info("gaps"), PROFILE, WordCounter()).chunks
    assert chunks and all(c.section_type == "body" for c in chunks)
    assert chunks[0].page_start == 1 and chunks[-1].page_end == 2


@pytest.mark.parametrize(("path", "expected"), [
    (("Discussion", "Limitations"), "limitations"),
    (("Materials and Methods", "Statistical Analysis"), "methods"),
    (("Conflict of Interest",), "back_matter"),
    (("References",), "references"),
    (("What to know",), "body"),
])
def test_section_classification_prefers_the_most_specific_heading(path, expected):
    assert classify_section(path, "body") == expected
