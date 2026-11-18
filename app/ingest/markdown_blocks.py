"""Split a corpus Markdown file into typed blocks with character offsets, and normalise their text.

Corpus files (data/corpus/<tier>/<source_id>.md) start with a Vietnamese metadata header, then
`<!-- ORIGINAL_DOCUMENT_BODY -->`, then the converted body: Markdown headings, paragraphs,
single-line HTML tables, inline JATS/HTML tags, MathML, and `<!-- SOURCE_PDF_PAGE n -->` markers
for PDF-derived documents. Only the body is returned.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Literal

BODY_MARKER = "<!-- ORIGINAL_DOCUMENT_BODY -->"
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
PAGE = re.compile(r"^<!-- SOURCE_PDF_PAGE (\d+) -->\s*$")
MATH = re.compile(r"<math\b[^>]*>.*?</math>", re.S | re.I)
ALTTEXT = re.compile(r'alttext="([^"]*)"', re.I)
CITATION_SUP = re.compile(r"<sup>\s*[\d,\s\u2013-]*\s*</sup>", re.I)  # digits, commas, en dash, hyphen
TAG = re.compile(r"<[^>]+>")
EMPTY_LINK = re.compile(r"\[\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]+)\]\((?:[^)]*)\)")
ROW = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S | re.I)
CELL = re.compile(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", re.S | re.I)
SPACES = re.compile(r"[ \t\u00a0]+")

# v2 only: a "[text](target)" is a link only when the target looks like a URL or a path. In v1 the
# citation "[73](Reznick et al., 2007)" was mistaken for a link and the parenthesis was lost.
LINK_V2 = re.compile(r"\[([^\]]+)\]\(((?:https?://|www\.|/|#|mailto:|\.\.?/)[^)\s]*|[^)\s]+\.[a-z0-9]{2,4})\)", re.I)
CELL_ITEM_BREAK = re.compile(r"</li>\s*<li\b[^>]*>|<br\s*/?>|<break\s*/>", re.I)
THEAD = re.compile(r"<thead\b.*?</thead>", re.S | re.I)
NORMALIZERS = ("v1", "v2")

BlockKind = Literal["heading", "page", "table", "paragraph"]


class FormatError(ValueError):
    pass


@dataclass(frozen=True)
class Block:
    kind: BlockKind
    start: int  # char offset in the file
    end: int
    raw: str
    text: str  # normalised text ("" for page markers)
    level: int = 0  # heading level
    page: int | None = None  # page number for page markers
    page_start: int | None = None  # set by the PDF layout pass, where a paragraph can span pages
    page_end: int | None = None
    flags: tuple[str, ...] = ()  # e.g. ("flattened_table",)


def _math_text(match: re.Match[str]) -> str:
    alt = ALTTEXT.search(match.group(0))
    inner = alt.group(1) if alt else TAG.sub("", match.group(0))
    return " " + html.unescape(inner).strip() + " "


def normalize_inline(text: str, version: str = "v1") -> str:
    """Strip markup, keep the words. Citation superscripts are dropped; other tags keep inner text."""
    text = MATH.sub(_math_text, text)
    text = CITATION_SUP.sub("", text)
    text = EMPTY_LINK.sub("", text)
    if version == "v2":
        text = LINK_V2.sub(r"\1", text)
        text = re.sub(r"\]\(", "] (", text)  # keep "[73] (Reznick et al., 2007)" readable
    else:
        text = LINK.sub(r"\1", text)
    text = TAG.sub("", text)
    text = html.unescape(text)
    lines = [SPACES.sub(" ", line).strip() for line in text.splitlines()]
    return " ".join(line for line in lines if line)


def _cell_text(cell: str, version: str) -> str:
    if version == "v2":  # list items and line breaks inside a cell are separate values
        cell = CELL_ITEM_BREAK.sub("; ", cell)
    return normalize_inline(cell, version).strip("; ").replace(";  ", "; ")


def table_rows(raw: str, version: str = "v1") -> list[str]:
    """v1: one string per row, cells joined with ' | '.
    v2: a Markdown table — header row(s) from <thead> (or <th> cells), a separator, then body rows."""
    if version != "v2":
        rows = []
        for row in ROW.findall(raw):
            cells = [normalize_inline(c) for c in CELL.findall(row)]
            if any(cells):
                rows.append(" | ".join(cells))
        return rows
    thead = THEAD.search(raw)
    header_rows = ROW.findall(thead.group(0)) if thead else []
    body_html = raw.replace(thead.group(0), "") if thead else raw
    body_rows = ROW.findall(body_html)
    if not header_rows and body_rows and re.search(r"<th\b", body_rows[0], re.I) and not re.search(
            r"<td\b", body_rows[0], re.I):
        header_rows, body_rows = body_rows[:1], body_rows[1:]

    def render(row: str) -> str | None:
        cells = [_cell_text(c, version) for c in CELL.findall(row)]
        return "| " + " | ".join(cells) + " |" if any(cells) else None

    header = [r for r in map(render, header_rows) if r]
    body = [r for r in map(render, body_rows) if r]
    if header:
        width = max(r.count("|") - 1 for r in header)
        header.append("|" + "---|" * width)
    return header + body


def body_offset(document: str) -> int:
    index = document.find(BODY_MARKER)
    if index < 0:
        raise FormatError(f"missing {BODY_MARKER}")
    return index + len(BODY_MARKER)


def parse_blocks(document: str, version: str = "v1") -> list[Block]:
    """Blocks of the body, in order. Offsets refer to the full document string. `version` selects the normaliser."""
    if version not in NORMALIZERS:
        raise ValueError(f"unknown normaliser {version}")
    blocks: list[Block] = []
    lines = document[body_offset(document):].splitlines(keepends=True)
    pos = body_offset(document)
    para_start: int | None = None
    para_lines: list[str] = []
    table_start: int | None = None
    table_lines: list[str] = []

    def flush_paragraph(end: int) -> None:
        nonlocal para_start, para_lines
        if para_start is not None:
            raw = "".join(para_lines)
            text = normalize_inline(raw, version)
            if text:
                blocks.append(Block("paragraph", para_start, end, raw, text))
        para_start, para_lines = None, []

    for line in lines:
        line_end = pos + len(line)
        stripped = line.strip()
        if table_start is not None:  # inside a multi-line table
            table_lines.append(line)
            if "</table>" in stripped.lower():
                raw = "".join(table_lines)
                blocks.append(Block("table", table_start, line_end, raw, "\n".join(table_rows(raw, version))))
                table_start, table_lines = None, []
        elif not stripped:
            flush_paragraph(pos)
        elif heading := HEADING.match(stripped):
            flush_paragraph(pos)
            blocks.append(Block("heading", pos, line_end, line, normalize_inline(heading.group(2), version),
                                level=len(heading.group(1))))
        elif page := PAGE.match(stripped):
            flush_paragraph(pos)
            blocks.append(Block("page", pos, line_end, line, "", page=int(page.group(1))))
        elif stripped.lower().startswith("<table"):
            flush_paragraph(pos)
            if "</table>" in stripped.lower():
                blocks.append(Block("table", pos, line_end, line, "\n".join(table_rows(line, version))))
            else:
                table_start, table_lines = pos, [line]
        else:
            if para_start is None:
                para_start = pos
            para_lines.append(line)
        pos = line_end
    flush_paragraph(pos)
    if table_start is not None:
        raise FormatError(f"unterminated <table> starting at offset {table_start}")
    return blocks
