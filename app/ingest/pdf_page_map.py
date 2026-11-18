"""Recover page provenance for PDF-derived corpus files that were converted without page markers.

The three WHO PDFs were converted (Carobud_ASD_2026, scripts/source_library/build_library.py) as
    pages = [page.extract_text() or "" for page in PdfReader(pdf).pages]   # pypdf 6.11.0
    body  = clean("\\n\\n".join(pages))   where clean(v) = re.sub(r"\\n{3,}", "\\n\\n", v).strip() + "\\n"
Re-running exactly that produces the corpus body byte for byte, so every page boundary can be
computed by translating offsets through the same join + clean. Nothing in the corpus changes.

A page map is accepted only if (1) the reproduced body equals the corpus body exactly and (2) every
page's text, whitespace-normalised, equals the corpus slice assigned to it. Otherwise no map is
written and the document stays page_provenance_incomplete — page numbers are never guessed.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from app.ingest.markdown_blocks import BODY_MARKER

EXTRACTOR = "pypdf"
EXTRACTOR_VERSION = "6.11.0"
METHOD = "pypdf extract_text per page; pages joined with '\\n\\n'; clean() collapses \\n{3,} and strips"
MAP_VERSION = "v1"


@dataclass(frozen=True)
class PageSpan:
    page: int  # 1-based physical page index in the PDF
    label: str | None  # printed page label from the PDF page-label tree ("iv", "12"), if defined
    char_start: int  # offsets into the corpus file (same coordinates as chunks.char_start)
    char_end: int
    chars: int
    text_sha256: str


@dataclass
class PageMap:
    source_id: str
    corpus_sha256: str
    original_sha256: str
    pages: list[PageSpan] = field(default_factory=list)
    verified: bool = False
    failures: list[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {"source_id": self.source_id, "map_version": MAP_VERSION, "extractor": EXTRACTOR,
                "extractor_version": EXTRACTOR_VERSION, "method": METHOD, "corpus_sha256": self.corpus_sha256,
                "original_sha256": self.original_sha256, "verified": self.verified, "failures": self.failures,
                "page_count": len(self.pages), "pages": [asdict(p) for p in self.pages]}


def clean(value: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", value).strip() + "\n"


def _translator(raw: str):
    """Map an offset in `raw` to the offset in clean(raw), as the old converter's canonicalisation did."""
    removed = [(m.start() + 2, m.end()) for m in re.finditer(r"\n{3,}", raw)]
    normalized = re.sub(r"\n{3,}", "\n\n", raw)
    leading = len(normalized) - len(normalized.lstrip())

    def translate(position: int) -> int:
        deleted = sum(max(0, min(position, end) - start) for start, end in removed)
        return max(0, position - deleted - leading)

    return translate


def _reliable_labels(reader, count: int) -> list[str | None]:
    """Printed page labels; None where pypdf warns it could not determine the label (no guessed labels)."""
    import logging

    from pypdf._page_labels import index2label

    class Capture(logging.Handler):
        def __init__(self) -> None:
            super().__init__()
            self.hit = False

        def emit(self, record: logging.LogRecord) -> None:
            self.hit = True

    logger = logging.getLogger("pypdf")
    labels: list[str | None] = []
    for i in range(count):
        handler = Capture()
        logger.addHandler(handler)
        try:
            label = index2label(reader, i)
        finally:
            logger.removeHandler(handler)
        labels.append(None if handler.hit else label)
    return labels


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_page_map(source_id: str, pdf_path: Path, corpus_path: Path) -> PageMap:
    from pypdf import PdfReader, __version__

    document = corpus_path.read_text(encoding="utf-8")
    pm = PageMap(source_id, hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
                 hashlib.sha256(pdf_path.read_bytes()).hexdigest())
    if __version__ != EXTRACTOR_VERSION:
        pm.failures.append(f"pypdf {__version__} installed; the conversion used {EXTRACTOR_VERSION}")
        return pm
    body_start = document.index(BODY_MARKER) + len(BODY_MARKER) + 1  # marker line ends with "\n"
    reader = PdfReader(pdf_path)
    pages = [p.extract_text() or "" for p in reader.pages]
    labels = _reliable_labels(reader, len(pages))
    raw = "\n\n".join(pages)
    if clean(raw) != document[body_start:]:
        pm.failures.append("reproduced text differs from the corpus body; page boundaries not derivable")
        return pm
    translate = _translator(raw)
    cursor = 0
    for index, text in enumerate(pages):
        start, end = translate(cursor), translate(cursor + len(text))
        cursor += len(text) + 2  # the "\n\n" joiner
        span = document[body_start + start: body_start + end]
        if _squash(span) != _squash(text):
            pm.failures.append(f"page {index + 1}: corpus slice does not equal the page text")
        pm.pages.append(PageSpan(index + 1, labels[index], body_start + start, body_start + end, len(text),
                                 hashlib.sha256(text.encode("utf-8")).hexdigest()))
    pm.verified = not pm.failures
    return pm


def page_lookup(page_map: dict) -> list[tuple[int, int, int]]:
    """(char_start, char_end, page) for non-empty pages of a verified map, sorted by offset."""
    if not page_map.get("verified"):
        return []
    return sorted((p["char_start"], p["char_end"], p["page"]) for p in page_map["pages"] if p["chars"])


def page_at(lookup: list[tuple[int, int, int]], offset: int) -> int | None:
    """Page containing `offset`; offsets in the "\\n\\n" between pages belong to the next page."""
    for start, end, page in lookup:
        if offset < end or offset < start:
            return page
    return lookup[-1][2] if lookup else None
