"""T5.2 Phase C — evidence normalization.

Turns a raw retrieved excerpt (and its title/section heading) into a typed structure so the answer
generator can build a sentence frame without ever guessing at structure it cannot see. Read-only over
the string already returned by the database; never touches the corpus, never calls an external service.

Four shapes are distinguished, because each needs different handling to avoid losing meaning:
  - "table"     — a markdown pipe table (common in this corpus for dosage/recommendation tables).
                  Rows are kept as column-name -> cell-value dicts, so a value is never separated from
                  the column header that gives it meaning, and the cell text (which may carry a unit,
                  e.g. "1-3mg") is kept verbatim, never re-parsed into a bare number.
  - "list"      — a bulleted or asterisk-delimited list (common for "signs include: * ... * ...").
                  Each item is kept as one string; an age/number mentioned in the item (e.g. "by 18
                  months of age") is extracted alongside it, not stripped out, so a caller can match a
                  query's named age against the item that actually names that age.
  - "heading"   — not used standalone here; title/section are passed to callers separately already by
                  `RetrievedChunk`. Kept as a named kind for completeness/testability, not emitted by
                  `classify`.
  - "paragraph" — anything else; the excerpt's cleaned prose.

Stated limitation: this is pattern-based (regex/string parsing), not a real table/document parser — it
handles the two table layouts actually observed in this corpus (see tests) and may not generalize to
every possible markdown table variant. When parsing fails to find a clean row/column structure, it falls
back to `paragraph`, never to a malformed `table` guess.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_AGE_RE = re.compile(r"\b(\d{1,3})\s*(months?|years?|tháng|thang|tuổi|tuoi)\b", re.IGNORECASE)
_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
# Trailing corpus boilerplate (CDC "Keep Reading:"/"See Also" footers) observed in this corpus's
# converted pages. Stripped line-by-line from the END only (never from the middle, where "Image:" or
# similar markers can legitimately precede real content — e.g. CDC milestone pages) so real content is
# never discarded.
_TRAILING_BOILERPLATE_LINE_RE = re.compile(r"^\s*(Keep Reading:|See Also\b).*$", re.IGNORECASE)


def strip_boilerplate(text: str) -> str:
    lines = text.split("\n")
    while lines and (not lines[-1].strip() or _TRAILING_BOILERPLATE_LINE_RE.match(lines[-1])):
        lines.pop()
    return "\n".join(lines).strip()
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
_BULLET_SPLIT_RE = re.compile(r"(?:^|\s)\*\s+")


@dataclass(frozen=True)
class TableEvidence:
    caption: str
    columns: list[str]
    rows: list[dict[str, str]]


@dataclass(frozen=True)
class ListEvidence:
    intro: str  # the sentence before the first bullet, e.g. "Examples ... can include"; "" if none
    items: list[str]
    item_ages: list[list[str]]  # ages mentioned in each item, same index as `items`; [] if none


@dataclass(frozen=True)
class ParagraphEvidence:
    text: str


@dataclass(frozen=True)
class NormalizedEvidence:
    kind: str  # "table" | "list" | "paragraph"
    table: TableEvidence | None = None
    list_: ListEvidence | None = None
    paragraph: ParagraphEvidence | None = None
    source_ages: list[str] = field(default_factory=list)  # every age mentioned anywhere in the excerpt


def extract_ages(text: str) -> list[str]:
    return [m.group(1) for m in _AGE_RE.finditer(text)]


def _try_parse_table(text: str) -> TableEvidence | None:
    lines = [ln for ln in text.split("\n") if ln.strip()]
    table_start = None
    for i, ln in enumerate(lines):
        if _TABLE_ROW_RE.match(ln) and i + 1 < len(lines) and _TABLE_SEP_RE.match(lines[i + 1]):
            table_start = i
            break
    if table_start is None:
        return None

    caption = " ".join(lines[:table_start]).strip()
    header_cells = [c.strip() for c in lines[table_start].strip().strip("|").split("|")]
    data_rows: list[dict[str, str]] = []
    for ln in lines[table_start + 2:]:
        m = _TABLE_ROW_RE.match(ln)
        if not m:
            break
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) != len(header_cells):
            # A row that doesn't line up with the header is not safely attributable to any column —
            # stop rather than guess which cell belongs to which header (the task's explicit rule:
            # never separate a row from its header, never misattribute column <-> value).
            break
        data_rows.append(dict(zip(header_cells, cells, strict=True)))
    if not data_rows:
        return None
    return TableEvidence(caption=caption, columns=header_cells, rows=data_rows)


def _try_parse_list(text: str) -> ListEvidence | None:
    starts_with_bullet = bool(re.match(r"^\s*\*\s+", text))
    parts = [p.strip() for p in _BULLET_SPLIT_RE.split(text) if p.strip()]
    intro, items = ("", parts) if starts_with_bullet else (parts[0], parts[1:]) if parts else ("", [])
    if len(items) < 2:  # need at least 2 real bullets to call this a "list", not noise
        return None
    return ListEvidence(intro=intro, items=items, item_ages=[extract_ages(p) for p in items])


def classify(excerpt: str) -> NormalizedEvidence:
    excerpt = strip_boilerplate(excerpt)
    table = _try_parse_table(excerpt)
    if table is not None:
        return NormalizedEvidence(kind="table", table=table, source_ages=extract_ages(excerpt))

    list_ev = _try_parse_list(excerpt)
    if list_ev is not None:
        return NormalizedEvidence(kind="list", list_=list_ev, source_ages=extract_ages(excerpt))

    return NormalizedEvidence(kind="paragraph", paragraph=ParagraphEvidence(text=excerpt.strip()),
                              source_ages=extract_ages(excerpt))


def table_cell(table: TableEvidence, column: str, row_match: dict[str, str]) -> str | None:
    """Looks up a cell by column name, from the row matching every key/value in `row_match` on other
    columns — a safe way to ask "what is the Recommendation for the row where Practice Area is X" without
    ever indexing rows/columns by position (which is how a row could get separated from its header)."""
    for row in table.rows:
        if all(row.get(k) == v for k, v in row_match.items()):
            return row.get(column)
    return None
