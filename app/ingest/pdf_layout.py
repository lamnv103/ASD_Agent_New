"""Recover structure from PDF-derived text that has no Markdown headings (profile section_v2).

The converted PDFs are plain lines: hard-wrapped paragraphs, page markers (sometimes), running
headers/footers repeated on most pages, chapter titles printed in the page margin, and tables that
were flattened into one cell per line. No font information survived conversion, so structure is
inferred from what the text still carries:

  * position   — first/last lines of a page (edge zone) vs body lines
  * repetition — how many pages (or how far apart) a normalised line recurs
  * spacing    — blank lines, line length relative to the document's typical line
  * context    — the previous line ends a sentence, the next line starts one
  * form       — numbering ("2.3 Outcomes"), "Chapter/Session N", ALL CAPS, standard section names

A line is only promoted to a heading when form AND context agree; otherwise the text stays
unclassified rather than being given an invented section name.
"""

from __future__ import annotations

import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from itertools import pairwise

from app.ingest.markdown_blocks import PAGE, Block, body_offset, normalize_inline
from app.ingest.pdf_page_map import page_at

EDGE_TOP, EDGE_BOTTOM = 3, 8
MIN_REPEAT_PAGES = 3
# Document-level boilerplate is spread over the whole document; a chapter title repeats only over its own
# run of pages, however long the chapter is. So "global" is judged by spread, not by page share alone.
GLOBAL_PAGE_SHARE, GLOBAL_SPAN_SHARE = 0.5, 0.8
SPREAD_MIN_PAGE_SHARE = 0.15  # used when repeated lines are kept (section_v2_1)
EDGE_SHARE = 0.6  # >= 60% of occurrences in the edge zone
UNPAGED_MIN_REPEAT, UNPAGED_MIN_GAP = 4, 15
FLAT_TABLE_RUN, FLAT_TABLE_MAX_WORDS = 8, 4
NUMERIC_ROW_RUN = 3
NUMBER_TOKEN = re.compile(r"[(\[]?[–−-]?[\d.,]+%?[)\]]?[;,]?")
TABLE_CAPTION_LINE = re.compile(r"^TABLE\s+\d+[A-Z]?\b")  # upper-case caption style of NIHR/HTA reports

PAGE_NUMBER = re.compile(r"^(page\s+)?\d{1,4}(\s+of\s+\d{1,4})?$", re.I)
NUMBERED = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+(\S.{1,95})$")
DIVISION = re.compile(r"^(chapter|session|module|part|section|appendix|annex)\s+([0-9IVXLA-Z]{1,4})\b[:.\-–]?\s*(.*)$",
                      re.I)
KNOWN_SECTIONS = re.compile(
    r"^(abstract|scientific summary|plain language summary|summary|introduction|background|aims?( and objectives)?|"
    r"objectives|methods?|methodology|materials and methods|results|findings|discussion|limitations|"
    r"strengths and limitations|conclusions?|recommendations?|implications|references|bibliography|"
    r"acknowledg(e)?ments?|contributors|contributions of authors|list of contributors|supplementary materials?|"
    r"appendix|appendices|annex(es)?|glossary|list of abbreviations|abbreviations|contents|table of contents|"
    r"foreword|preface|disclaimer)$", re.I)
CITATION_LIKE = re.compile(
    r"\b(19|20)\d{2}\b.*\b(et al|vol\.|doi|pp\.|journal)\b|^\d{1,3}\.\s+[A-Z][a-zA-Z'’-]+ [A-Z]{1,3}\b", re.I)
NOT_TITLE = re.compile(r"https?://|www\.|doi[:\s]|©|copyright|\bvol\.\s*\d|\bisbn\b|@", re.I)
BULLET = re.compile(r"^([•▪●○◦✓■□\-–]|\(?[a-z0-9]{1,2}[.)])\s+")
SENTENCE_END = re.compile(r"[.!?:]['\")\]]?$")
TRAILING_FUNCTION_WORD = re.compile(r"\b(of|and|or|the|a|an|in|on|to|for|with|by|from|at|as|that|which)$", re.I)
LEADING_PAGE_NUMBERS = re.compile(r"^\d{1,4}(?:\s+\d{1,4})*\s*(?=[A-Za-z])")


@dataclass(frozen=True)
class Line:
    text: str
    start: int
    end: int
    page: int | None
    blank_before: bool


@dataclass
class LayoutResult:
    blocks: list[Block]
    removed: Counter = field(default_factory=Counter)  # reason -> characters removed
    removed_examples: dict[str, list[str]] = field(default_factory=dict)
    running_titles: list[str] = field(default_factory=list)
    headings: list[tuple[int, str, str]] = field(default_factory=list)  # (level, text, signal)


def norm(text: str) -> str:
    """Key for repetition counting. Case is kept on purpose: a running title "METHODS" printed in the
    margin must not be merged with an in-text "Methods" heading that happens to sit at a page top."""
    text = re.sub(r"\d+", "#", text)
    return re.sub(r"\s+", " ", text).strip(" .:;,-–|")


def _lines(document: str, page_lookup: list[tuple[int, int, int]] | None = None) -> list[Line]:
    """Body lines with offsets. Pages come from in-text markers or, for documents converted without
    markers, from a verified page map (app.ingest.pdf_page_map); otherwise page is None."""
    out: list[Line] = []
    pos = body_offset(document)
    page: int | None = None
    blank = True
    for raw in document[pos:].splitlines(keepends=True):
        stripped = raw.strip()
        if marker := PAGE.match(stripped):
            page = int(marker.group(1))  # a page break alone does not end a paragraph
        elif not stripped:
            blank = True
        else:
            line_page = page_at(page_lookup, pos) if page_lookup else page
            out.append(Line(normalize_inline(stripped, "v2"), pos, pos + len(raw.rstrip("\r\n")), line_page, blank))
            blank = False
        pos += len(raw)
    return [ln for ln in out if ln.text]


def title_like(text: str) -> bool:
    words = text.split()
    return (1 <= len(words) <= 12 and len(text) <= 100 and text[0].isalnum() and not text[0].islower()
            and not NOT_TITLE.search(text) and not re.search(r"[,;]$", text))


def is_all_caps(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return len(letters) >= 4 and sum(c.isupper() for c in letters) / len(letters) >= 0.9


def heading_case(text: str) -> bool:
    """ALL CAPS, or every content word (>= 4 letters) capitalised — how printed running titles look."""
    if is_all_caps(text):
        return True
    words = [w for w in re.findall(r"[A-Za-z]+", text) if len(w) >= 4]
    return len(words) >= 2 and all(w[0].isupper() for w in words)


def running_title(text: str) -> str | None:
    """The section title carried by a repeated margin line, or None if it does not look like one."""
    text = LEADING_PAGE_NUMBERS.sub("", text).strip()
    if not text or not title_like(text) or text.endswith((".", ":")) or TRAILING_FUNCTION_WORD.search(text):
        return None
    if DIVISION.match(text) or (KNOWN_SECTIONS.match(text) and heading_case(text)):
        return text
    # Any other single capitalised word repeated in the margin ("HIGH", "CAREGIVER") is a table label.
    return text if heading_case(text) and len(text.split()) >= 2 else None


# ---------------------------------------------------------------- boilerplate


def _paged_boilerplate(lines: list[Line],
                       rules: str = "v2") -> tuple[set[int], dict[int, str], set[str]]:
    """rules="v2" reproduces section_v2; rules="v2_1" keeps repeated in-text headings, needs a page share for
    spread-out boilerplate, and gives a running title only its contiguous page runs."""
    v21 = rules == "v2_1"
    """Return (indices to remove, page -> running section title, global boilerplate keys)."""
    by_page: dict[int, list[int]] = defaultdict(list)
    for i, ln in enumerate(lines):
        by_page[ln.page or 0].append(i)
    edge: set[int] = set()
    for idx in by_page.values():
        edge.update(idx[:EDGE_TOP] + idx[-EDGE_BOTTOM:])
    pages_with: dict[str, set[int]] = defaultdict(set)
    numbers_by_key: dict[str, list[tuple[int, list[int]]]] = defaultdict(list)
    edge_count: Counter = Counter()
    all_count: Counter = Counter()
    for i, ln in enumerate(lines):
        key = norm(ln.text)
        all_count[key] += 1
        if i in edge:
            edge_count[key] += 1
            pages_with[key].add(ln.page or 0)
            numbers_by_key[key].append((ln.page or 0, [int(n) for n in re.findall(r"\d+", ln.text)]))
    n_pages = max(1, len(by_page))
    remove: set[int] = set()
    page_title: dict[int, str] = {}
    global_keys: set[str] = set()
    title_pages: dict[str, set[int]] = {}
    first_seen: set[str] = set()
    for i, ln in enumerate(lines):
        if i not in edge:
            continue
        key = norm(ln.text)
        if PAGE_NUMBER.match(ln.text):
            remove.add(i)
            continue
        repeated = len(pages_with[key]) >= MIN_REPEAT_PAGES and edge_count[key] >= EDGE_SHARE * all_count[key]
        if not repeated or len(ln.text) > 220:
            continue
        title = running_title(ln.text)
        pages = pages_with[key]
        span = max(pages) - min(pages) + 1
        is_global = len(pages) >= GLOBAL_PAGE_SHARE * n_pages or (
            span >= GLOBAL_SPAN_SHARE * n_pages
            # section_v2_1: a heading repeated once per session is spread out but rare (9 of 276 pages);
            # real running boilerplate also covers a sizeable share of pages (SENITA footer: 43%).
            and (not v21 or len(pages) >= SPREAD_MIN_PAGE_SHARE * n_pages))
        if is_global and _numbers_are_boilerplate(numbers_by_key[key]):
            global_keys.add(key)  # journal/report boilerplate on many pages: remove every occurrence
            remove.add(i)
        elif title:
            title_pages.setdefault(title, set()).update(pages_with[key])
            remove.add(i)
        elif not v21 and ln.text in first_seen:
            # section_v2 only: exact duplicate at a page edge (e.g. a table header on continuation pages) keeps
            # its first copy. section_v2_1 turns this off — WHO workbooks repeat real headings ("What we will
            # learn today", "WHO recommends:") in every session, and those must not be deleted.
            remove.add(i)
        else:
            first_seen.add(ln.text)
    # A title covers its contiguous run of pages (printed on alternate pages, so fill the gaps), and a page
    # outside every run has no running title. Overlaps: the most specific title (fewest pages) wins.
    for title, pages in sorted(title_pages.items(), key=lambda kv: -len(kv[1])):
        for start, end in (_page_runs(pages) if v21 else [(min(pages), max(pages))]):
            for p in range(start, end + 1):
                page_title[p] = title
    return remove, page_title, global_keys


def _page_runs(pages: set[int], max_gap: int = 2, min_pages: int = 2) -> list[tuple[int, int]]:
    """Contiguous runs of pages (gaps up to max_gap: titles alternate between facing pages); a title seen
    on a single isolated page (a contents list, a summary annex) does not open a run."""
    runs, ordered = [], sorted(pages)
    start = prev = ordered[0]
    for p in ordered[1:]:
        if p - prev > max_gap:
            runs.append((start, prev))
            start = p
        prev = p
    runs.append((start, prev))
    return [(a, b) for a, b in runs if len([p for p in ordered if a <= p <= b]) >= min_pages]


def _numbers_are_boilerplate(occurrences: list[tuple[int, list[int]]]) -> bool:
    """A footer's numbers are constant ("Vol. 26 No. 29") or follow the page ("… 138"); a data row's are not.
    Every number position must be constant or keep a constant offset from the page number."""
    lengths = {len(nums) for _, nums in occurrences}
    if len(lengths) != 1:
        return False
    for position in range(lengths.pop()):
        values = {nums[position] for _, nums in occurrences}
        offsets = {nums[position] - page for page, nums in occurrences}
        # Facing-page headers print "10 11": allow the offset to alternate between two values.
        if len(values) > 1 and len(offsets) > 2:
            return False
    return True


def _unpaged_boilerplate(lines: list[Line]) -> tuple[set[int], dict[int, str], set[str]]:
    """Without page markers there is no edge zone, so removal is stricter: a repeated line spaced like a
    page header (not dense like table cells) is removed only if it is a document-wide running header,
    or a section running title (Session/Chapter N, ALL CAPS). Repeated form labels ("Routine 1:") stay."""
    positions: dict[str, list[int]] = defaultdict(list)
    for i, ln in enumerate(lines):
        positions[norm(ln.text)].append(i)
    remove: set[int] = set()
    starts_title: dict[int, str] = {}
    global_keys: set[str] = set()
    total = max(1, len(lines))
    for key, idx in positions.items():
        if len(idx) < UNPAGED_MIN_REPEAT or len(lines[idx[0]].text) > 120:
            continue
        gaps = [b - a for a, b in pairwise(idx)]
        if statistics.median(gaps) < UNPAGED_MIN_GAP:
            continue  # dense repetition = table cells or list items, not a running header
        text = lines[idx[0]].text
        title = running_title(text)
        # A repeated caps line that is mostly followed by short table cells is a table label ("VERY LOW").
        followed_by_cells = sum(i + 1 < len(lines) and _is_flat_cell(lines[i + 1].text) for i in idx) > len(idx) / 2
        if title and (DIVISION.match(title) or (not followed_by_cells and is_all_caps(title)
                                                 and len(title.split()) >= 2)):
            remove.update(idx)
            for i in idx:
                starts_title[i] = title
        elif (len(idx) >= 10 and (idx[-1] - idx[0]) / total >= 0.5 and title_like(text)
              and not text.endswith(":")):
            remove.update(idx)
            global_keys.add(key)
    return remove, starts_title, global_keys


# ---------------------------------------------------------------- headings


def heading_signal(line: Line, prev: Line | None, nxt: Line | None, rules: str = "v2") -> tuple[int, str] | None:
    """(relative level, signal) when form AND context indicate a heading, else None."""
    text = line.text
    caps_continues = is_all_caps(text) and nxt is not None and is_all_caps(nxt.text)
    if not title_like(text) or CITATION_LIKE.search(text) or (TRAILING_FUNCTION_WORD.search(text)
                                                               and not caps_continues):
        return None
    if SENTENCE_END.search(text) and not (text.endswith(":") and DIVISION.match(text)):
        return None  # headings do not end like sentences; "Session 2:" is the only colon form accepted
    context = (prev is None or line.blank_before or bool(SENTENCE_END.search(prev.text)) or line.page != prev.page
               or bool(PAGE_NUMBER.match(prev.text)))  # a bare page number left in unpaged text is a boundary
    next_ok = nxt is not None and (nxt.text[0].isupper() or nxt.text[0].isdigit() or BULLET.match(nxt.text))
    if not (context and next_ok):
        return None
    if m := DIVISION.match(text):
        return 1, f"division:{m.group(1).lower()}"
    if m := NUMBERED.match(text):
        # v2_1: a bare integer ("69 For all ABC subscales, items were rated on four") is usually a footnote
        # or a wrapped list item; it counts as a heading only when the words look like a heading.
        bare = "." not in m.group(1)
        if rules == "v2_1" and bare and not (heading_case(m.group(2)) or KNOWN_SECTIONS.match(m.group(2))):
            return None
        if len(m.group(2).split()) <= 12 and m.group(2)[0].isupper():
            return m.group(1).count(".") + 1, "numbered"
        return None
    if KNOWN_SECTIONS.match(text.strip()):
        return 1, "known_section_name"
    if is_all_caps(text) and len(text.split()) <= 10:
        return 1, "all_caps"
    return None


# ---------------------------------------------------------------- paragraphs


def _is_flat_cell(text: str) -> bool:
    return len(text.split()) <= FLAT_TABLE_MAX_WORDS and not SENTENCE_END.search(text)


def layout_blocks(document: str, page_lookup: list[tuple[int, int, int]] | None = None,
                  rules: str = "v2") -> LayoutResult:
    lines = _lines(document, page_lookup)
    result = LayoutResult(blocks=[])
    if not lines:
        return result
    paged = any(ln.page is not None for ln in lines)
    if paged:
        remove, titles, _global_keys = _paged_boilerplate(lines, rules)
    else:
        remove, titles, _global_keys = _unpaged_boilerplate(lines)
    title_set = set(titles.values())
    for i in sorted(remove):
        if PAGE_NUMBER.match(lines[i].text):
            reason = "page_number"
        elif running_title(lines[i].text) in title_set:
            reason = "running_title"
        else:
            reason = "header_footer"
        result.removed[reason] += len(lines[i].text)
        examples = result.removed_examples.setdefault(reason, [])
        if lines[i].text not in examples and len(examples) < 6:
            examples.append(lines[i].text)
    result.running_titles = list(dict.fromkeys(titles.values()))

    kept = [ln for i, ln in enumerate(lines) if i not in remove]
    flat = _flat_runs(kept, rules)
    current_title: str | None = None
    para: list[Line] = []
    para_flat = False
    median_len = statistics.median(len(ln.text) for ln in kept) if kept else 0

    def flush() -> None:
        nonlocal para, para_flat
        if para:
            text = para[0].text
            for prev_ln, ln in pairwise(para):
                if re.search(r"[a-z]-$", prev_ln.text) and ln.text[:1].islower():
                    text = text[:-1] + ln.text  # de-hyphenate a word broken across lines
                else:
                    text += " " + ln.text
            pages = [ln.page for ln in para if ln.page is not None]
            # v2_1: a short paragraph made of numbers ("None 289 295 – SMD 0.3 SD higher") is a table cell group
            # cut loose from its labels; flag it so it is never packed into a retrievable prose chunk.
            fragment = rules == "v2_1" and _is_numeric_fragment(text)
            result.blocks.append(Block("paragraph", para[0].start, para[-1].end, "", text,
                                       page_start=min(pages) if pages else None,
                                       page_end=max(pages) if pages else None,
                                       flags=("flattened_table",) if para_flat or fragment else ()))
        para, para_flat = [], False

    def emit_heading(level: int, text: str, line: Line, signal: str) -> None:
        flush()
        result.blocks.append(Block("heading", line.start, line.end, "", text, level=level,
                                   page_start=line.page, page_end=line.page))
        result.headings.append((level, text, signal))

    original_index = {id(ln): i for i, ln in enumerate(lines)}
    skip_next = False
    for k, ln in enumerate(kept):
        if skip_next:
            skip_next = False
            continue
        title = titles.get(ln.page or 0) if paged else _latest_title(titles, original_index[id(ln)])
        if title != current_title and (title or paged):
            current_title = title
            # Leaving a running title's pages without entering another: close the section with an empty
            # level-1 heading (no invented name; empty headings are dropped from section paths).
            emit_heading(1, title or "", ln, "running_title" if title else "running_title_end")
        prev = kept[k - 1] if k else None
        nxt = kept[k + 1] if k + 1 < len(kept) else None
        signal = None if k in flat else heading_signal(ln, prev, nxt, rules)
        if signal:
            level, kind = signal
            text = ln.text
            # An ALL CAPS heading broken over two lines ("AVAILABLE EVIDENCE AND" / "RESEARCH GAPS").
            after = kept[k + 2] if k + 2 < len(kept) else None
            if kind == "all_caps" and nxt and is_all_caps(nxt.text) and len(nxt.text.split()) <= 8 \
                    and not SENTENCE_END.search(nxt.text) and (after is None or not is_all_caps(after.text)):
                text, skip_next = f"{text} {nxt.text}", True
            # Chapter/Session/Annex N in the text is top level and closes the previous running title;
            # other headings sit below the running title when the document has one.
            top_level = kind.startswith("division")
            emit_heading(1 if top_level else level + (1 if result.running_titles else 0), text, ln, kind)
            continue
        is_flat = k in flat
        prev_ends = bool(para and SENTENCE_END.search(para[-1].text))
        caption = rules == "v2_1" and bool(TABLE_CAPTION_LINE.match(ln.text))
        # v2_1: an upper-case "TABLE n" caption opens a table region that lasts to the end of its paragraph;
        # the rows that follow have lost their columns, so the region is flagged like any flattened table.
        if para_flat and not caption and rules == "v2_1" and para and TABLE_CAPTION_LINE.match(para[0].text):
            is_flat = True
        new_para = (not para or caption or ln.blank_before or bool(BULLET.match(ln.text)) or is_flat != para_flat
                    or (prev_ends and len(para[-1].text) < 0.75 * median_len)
                    or (prev_ends and ln.page != para[-1].page))  # page break after a finished sentence
        if new_para:
            flush()
        para.append(ln)
        para_flat = is_flat or caption
    flush()
    return result


def _latest_title(starts: dict[int, str], index: int) -> str | None:
    best = None
    for i in starts:
        if i <= index and (best is None or i > best):
            best = i
    return starts[best] if best is not None else None


def _flat_runs(kept: list[Line], rules: str = "v2") -> set[int]:
    """Indices of lines inside runs of >= FLAT_TABLE_RUN consecutive table-cell-like lines; with rules v2_1
    also runs of >= NUMERIC_ROW_RUN data rows (long lines made mostly of numbers, e.g. "5.89 (25.96) 0.00 ( –)")."""
    flat: set[int] = set()
    for is_cell, min_run in ((_is_flat_cell, FLAT_TABLE_RUN),
                             *(((_is_numeric_row, NUMERIC_ROW_RUN),) if rules == "v2_1" else ())):
        run: list[int] = []
        for k, ln in enumerate([*kept, None]):
            if ln is not None and is_cell(ln.text):
                run.append(k)
                continue
            if len(run) >= min_run:
                flat.update(run)
            run = []
    return flat


def _is_numeric_fragment(text: str) -> bool:
    tokens = text.split()
    numbers = sum(bool(NUMBER_TOKEN.fullmatch(t)) for t in tokens)
    return len(tokens) < 40 and numbers >= 3 and numbers >= 0.25 * len(tokens)


def _is_numeric_row(text: str) -> bool:
    tokens = text.split()
    numbers = [t for t in tokens if NUMBER_TOKEN.fullmatch(t)]
    return len(numbers) >= 3 and len(numbers) >= 0.4 * len(tokens)
