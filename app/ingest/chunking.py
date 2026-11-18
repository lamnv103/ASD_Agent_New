"""Section-aware chunking of one corpus document.

Rules shared by all profiles (see config/chunking_profiles.json):
  * A chunk never crosses a heading: each leaf section is packed on its own.
  * Paragraphs are packed greedily up to max_tokens; an oversize paragraph is split by sentence.
  * Overlap (trailing sentences, <= overlap_tokens) is added only between chunks of the SAME section.
  * Tables become their own chunks with their caption and footnotes; large tables are split by rows
    and repeat the header.
  * Front matter (before the first sub-heading) keeps only prose paragraphs (the unlabeled abstract
    in PMC articles); author lists, affiliations, copyright lines are dropped and counted.
  * References and back matter are kept as chunks but marked retrieval_eligible = false; tables printed
    after the reference list are "floating_table" chunks and stay retrievable.
  * Missing components are never hidden (completeness_status + missing_context).

Additional rules switched on by profile features (section_v2):
  * normalizer "v2": citation-safe link handling, list items / line breaks kept inside table cells,
    tables rendered as Markdown tables with a header row.
  * pdf_layout: documents without Markdown sub-headings go through app.ingest.pdf_layout (running
    headers/footers removed, chapter titles and in-text headings recovered, paragraphs rebuilt).
    Text with no structural evidence is section_type "unclassified".
  * content_detection: text chunks that are mostly citations or contributor lists are excluded from
    retrieval even when no heading says so.
  * Flattened PDF tables (one cell per line) are marked table_structure_lost and not retrievable.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from app.config import ROOT
from app.ingest.markdown_blocks import Block, parse_blocks
from app.ingest.pdf_layout import LayoutResult, layout_blocks
from app.ingest.pdf_page_map import page_lookup

PROFILES_FILE = ROOT / "config" / "chunking_profiles.json"
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\"“'])")
# Captions may carry a publisher prefix, e.g. "brainsci-10-00441-t004_Table 4Table 4".
TABLE_CAPTION = re.compile(r"^.{0,60}?(?:^|[_\s])(table|tab\.)\s*[0-9IVX]+", re.I)
# Short notes printed right after a table: abbreviations, significance markers, arrows, "Note:".
TABLE_FOOTNOTE = re.compile(
    r"^([*†‡§#]+|note\b|[a-z]\s|[↑↓])|\bp\s*[<>=≤≥]\s*0?\.\d|\s=\s|^[A-Z][A-Za-z0-9/-]{1,12}, [A-Za-z]", re.I)
FOOTNOTE_MAX_TOKENS = 80
FRONT_NOISE = re.compile(
    r"copyright|©|creative commons|distributed under the terms|licen[cs]ed under|open[- ]access article|"
    r"correspondence|submitted to|edited by|reviewed by|this article is|@", re.I)
MISSING_COMPONENT_MENTION = re.compile(
    r"\b(fig(?:ure)?s?\.?\s*\d+|supplementary|additional file|online resource|appendix|video\s*\d*)\b", re.I)
TABLE_SEPARATOR = re.compile(r"^\|(?:-{3}\|)+$")

SECTION_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("references", re.compile(r"^(references?|bibliography|works cited|literature cited)\b", re.I)),
    ("back_matter", re.compile(
        r"^(acknowledg|funding|conflicts? of interest|competing interests?|declarations?|author'?s?'? contributions?|"
        r"ethics|data availability|availability of data|publisher'?s note|supplementary|abbreviations|footnotes|"
        r"consent|orcid|disclosure|end matter|keywords|(systematic review |trial )?registration)", re.I)),
    ("limitations", re.compile(r"limitation", re.I)),
    ("abstract", re.compile(r"^(abstract|summary|plain language summary|key points|highlights)\b", re.I)),
    ("introduction", re.compile(r"^(introduction|background)\b", re.I)),
    ("methods", re.compile(r"^(methods?|materials and methods|methodology|participants|procedures?|study design|"
                           r"search strategy|data extraction|statistical analys[ie]s|measures)\b", re.I)),
    ("results", re.compile(r"^(results?|findings)\b", re.I)),
    ("discussion", re.compile(r"^discussion\b", re.I)),
    ("conclusion", re.compile(r"^(conclusions?|implications|recommendations?|summary and conclusions?)\b", re.I)),
]
# section_v2 adds structural sections common in reports/manuals; checked before the v1 rules.
SECTION_RULES_V2: list[tuple[str, re.Pattern[str]]] = [
    ("front_matter", re.compile(r"^(contents|table of contents|list of (tables|figures|boxes)|foreword|preface|"
                                r"disclaimer|this report should be referenced|editorial|copyright)", re.I)),
    ("contributors", re.compile(r"^(contributors|list of contributors|contributions of authors|"
                                r"author contributions|editorial (team|board)|steering group)", re.I)),
    ("back_matter", re.compile(r"^(list of abbreviations|glossary of abbreviations)", re.I)),
    ("appendix", re.compile(r"^(appendix|appendices|annex(es)?)\b", re.I)),
    ("glossary", re.compile(r"^glossary\b", re.I)),
    ("recommendations", re.compile(r"^(recommendations?|who recommends)\b", re.I)),
    *SECTION_RULES,
]
NOT_RETRIEVABLE = {"references", "back_matter"}
NOT_RETRIEVABLE_V2 = NOT_RETRIEVABLE | {"front_matter", "contributors", "references_detected", "contributors_detected",
                                        "front_matter_detected", "noise"}
# PDF front pages (layout pass only): publication/licence boilerplate and author lists with affiliation marks.
PUBLICATION_INFO = re.compile(r"\bISBN\b|Some rights reserved|Cataloguing-in-Publication|Suggested citation|"
                              r"should be referenced as|Printed in [A-Z]|All rights reserved|"
                              r"Creative Commons Attribution|commissioning contract", re.I)
NUMERIC_TOKEN = re.compile(r"[(\[]?[–−-]?[\d.,]+%?[)\]]?[;,]?")
GLYPH_ID = re.compile(r"/gid\d{5}")  # unmapped PDF glyphs written as glyph ids
DOT_LEADER = re.compile(r"\.{6,}\s*[0-9ivxlc]{1,4}\b", re.I)
AUTHOR_WITH_AFFILIATION_MARK = re.compile(r"[A-Z][a-z]+(?:[ -][A-Z][a-z'’-]+)+ ?,?\d[*†,\d]*")

# Content-based detection (v2). A reference-list entry STARTS with authors ("12. Smith J, Lee K." /
# "Smith, J., & Lee, K. (2019)") and carries a year; running prose that merely cites "et al., 2019"
# does not start that way, so review paragraphs are not mistaken for reference lists.
AUTHOR_TOKEN = re.compile(r"\b[A-Z][a-zà-ÿ'’\-]+,?\s+(?:[A-Z]{1,3}\b|[A-Z]\.(?:\s?[A-Z]\.)*)")
REF_ENTRY_START = re.compile(r"^\s*(?:\[?\d{1,3}[\].)]?\s+)?[A-Z][a-zà-ÿ'’\-]+,?\s+(?:[A-Z]{1,3}\b|[A-Z]\.)")
YEAR = re.compile(r"\b(19|20)\d{2}\b")
CONTRIBUTOR_ENTRY = re.compile(
    r"[A-Z][a-zà-ÿ'’\-]+(?: [A-Z][a-zà-ÿ'’\-]+){1,3},? \([^()]*(?:,|University|Institute|Hospital|Centre|Center|"
    r"Ministry|Organi[sz]ation|Foundation|Department|School|Association|Society|Council|Agency|WHO|UNICEF)[^()]*\)")


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...


class HFTokenCounter:
    """Exact token counts with the embedding model's own tokenizer."""

    def __init__(self, path: Path, expected_sha256: str) -> None:
        from tokenizers import Tokenizer

        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected_sha256:
            raise ValueError(f"tokenizer {path.name} sha256 mismatch")
        self._tokenizer = Tokenizer.from_file(str(path))

    def count(self, text: str) -> int:
        return len(self._tokenizer.encode(text, add_special_tokens=False).ids)


@dataclass(frozen=True)
class ChunkingProfile:
    name: str
    max_tokens: int
    target_min_tokens: int
    merge_tail_below_tokens: int
    hard_max_tokens: int
    overlap_tokens: int
    front_matter_min_words: int
    tokenizer_path: Path
    tokenizer_sha256: str
    normalizer: str = "v1"
    pdf_layout: bool = False
    content_detection: bool = False
    page_maps: bool = False  # use verified page maps (data/extractions/) for PDFs converted without markers
    table_review: bool = False  # flattened PDF tables: recovered-pending-review vs unrecoverable (sidecar)
    rules: str = "v2"  # "v2_1": keep repeated headings, stricter front matter/numbered headings, data-row and
    #                    glyph-encoding detection (see config/chunking_profiles.json)

    @property
    def v2(self) -> bool:
        return self.normalizer == "v2"

    @classmethod
    def load(cls, name: str, path: Path = PROFILES_FILE) -> ChunkingProfile:
        cfg = json.loads(path.read_text(encoding="utf-8"))[name]
        features = cfg.get("features", {})
        return cls(name=name, max_tokens=cfg["max_tokens"], target_min_tokens=cfg["target_min_tokens"],
                   merge_tail_below_tokens=cfg["merge_tail_below_tokens"], hard_max_tokens=cfg["hard_max_tokens"],
                   overlap_tokens=cfg["overlap_tokens"], front_matter_min_words=cfg["front_matter_min_words"],
                   tokenizer_path=ROOT / cfg["tokenizer"]["path"], tokenizer_sha256=cfg["tokenizer"]["sha256"],
                   normalizer=features.get("normalizer", "v1"), pdf_layout=features.get("pdf_layout", False),
                   content_detection=features.get("content_detection", False),
                   page_maps=features.get("page_maps", False), table_review=features.get("table_review", False),
                   rules=features.get("rules", "v2"))

    def as_config(self) -> dict:
        return {k: (str(v.relative_to(ROOT).as_posix()) if isinstance(v, Path) else v)
                for k, v in self.__dict__.items()}


@dataclass(frozen=True)
class DocumentInfo:
    source_id: str
    document_id: str
    title: str
    corpus_role: str  # core | gaps
    source_type: str | None
    language: str
    missing_components: dict[str, int]


@dataclass
class Piece:
    """A paragraph or sentence group: the unit that is packed into chunks."""

    text: str
    tokens: int
    start: int
    end: int
    page_start: int | None
    page_end: int | None = None
    whole_paragraph: bool = True
    flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class Chunk:
    chunk_index: int
    section_path: tuple[str, ...]
    section_type: str
    content_kind: str
    page_start: int | None
    page_end: int | None
    char_start: int
    char_end: int
    content: str
    token_count: int
    completeness_status: str
    missing_context: str | None
    retrieval_eligible: bool
    has_overlap: bool

    @property
    def section_heading(self) -> str:
        return " > ".join(self.section_path)

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()


@dataclass
class ChunkingResult:
    chunks: list[Chunk]
    body_chars: int
    dropped: Counter = field(default_factory=Counter)  # reason -> normalised chars
    layout: LayoutResult | None = None  # set when the PDF layout pass was used

    @property
    def kept_chars(self) -> int:
        return self.body_chars - sum(self.dropped.values())


# ---------------------------------------------------------------- helpers


def classify_section(path: tuple[str, ...], fallback: str,
                     rules: list[tuple[str, re.Pattern[str]]] = SECTION_RULES) -> str:
    """Most specific matching heading wins (leaf first), so 'Discussion > Limitations' -> limitations."""
    for heading in reversed(path):
        for section_type, pattern in rules:
            if pattern.search(heading.strip()):
                return section_type
    return fallback


def detect_list_type(content: str) -> str | None:
    """'references_detected' / 'contributors_detected' when a text chunk is mostly such a list."""
    segments = [s for s in re.split(r"\n+|(?<=\.)\s+(?=\d{1,3}\.\s)", content) if len(s.strip()) > 3]

    def is_reference(s: str) -> bool:
        return (bool(REF_ENTRY_START.match(s)) and bool(YEAR.search(s)) and len(s.split()) <= 80
                and (len(AUTHOR_TOKEN.findall(s)) >= 2 or "et al" in s))

    if len(segments) >= 3 and sum(map(is_reference, segments)) / len(segments) >= 0.5:
        return "references_detected"
    # A contributor list is made OF entries; prose that mentions a few "Scale (ABC, 2010)" is not.
    entries = [m.group(0) for m in CONTRIBUTOR_ENTRY.finditer(content)]
    sentences = len(re.findall(r"[a-z]{3,}\. [A-Z]", content))
    coverage = sum(map(len, entries)) / max(1, len(content))
    if len(entries) >= 4 and len(entries) > 2 * sentences and coverage >= 0.35:
        return "contributors_detected"
    return None


EXTRACTIONS = ROOT / "data" / "extractions"


def _page_lookup(source_id: str, document: str) -> list[tuple[int, int, int]] | None:
    """Verified page map for exactly this corpus text (matched by SHA-256), else None."""
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()
    for path in sorted((EXTRACTIONS / source_id).glob("page_map.*.json")):
        page_map = json.loads(path.read_text(encoding="utf-8"))
        if page_map.get("verified") and page_map.get("corpus_sha256") == digest:
            return page_lookup(page_map)
    return None


def recovered_table_pages(source_id: str) -> set[int]:
    """Pages holding a PDF table candidate that passed automated structure checks (data/extractions)."""
    pages: set[int] = set()
    for path in sorted((EXTRACTIONS / source_id).glob("tables.*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line) if line.strip() else {}
            if row.get("auto_checks_passed"):
                pages.add(row["page"])
    return pages


def longest_numeric_run(text: str) -> int:
    best = current = 0
    for token in text.split():
        current = current + 1 if NUMERIC_TOKEN.fullmatch(token) else 0
        best = max(best, current)
    return best


def _same_title(heading: str, title: str) -> bool:
    a, b = heading.casefold().strip(" .:"), title.casefold().strip(" .:")
    return bool(a) and (a.startswith(b[:60]) or b.startswith(a[:60]))


def split_sentences(text: str) -> list[str]:
    return [s for s in SENTENCE_END.split(text) if s.strip()]


def _missing_context(info: DocumentInfo) -> str | None:
    if not info.missing_components:
        return None
    parts = ", ".join(f"{kind}×{n}" for kind, n in sorted(info.missing_components.items()))  # e.g. graphic x 4
    return f"Tài liệu gốc có phần chưa chuyển thành văn bản: {parts}."


# ---------------------------------------------------------------- packing


class _SectionPacker:
    def __init__(self, profile: ChunkingProfile, counter: TokenCounter) -> None:
        self.p, self.counter = profile, counter
        # A piece must still fit after an overlap prefix is added in front of it.
        self.piece_limit = profile.max_tokens - profile.overlap_tokens

    def pieces(self, block: Block, page: int | None) -> list[Piece]:
        p_start = block.page_start if block.page_start is not None else page
        p_end = block.page_end if block.page_end is not None else p_start

        def piece(text: str, tokens: int, whole: bool) -> Piece:
            return Piece(text, tokens, block.start, block.end, p_start, p_end, whole, block.flags)

        tokens = self.counter.count(block.text)
        if tokens <= self.piece_limit:
            return [piece(block.text, tokens, True)]
        out: list[Piece] = []
        current: list[str] = []
        for sentence in split_sentences(block.text):
            for part in self._hard_split(sentence):
                candidate = " ".join([*current, part])
                if current and self.counter.count(candidate) > self.piece_limit:
                    text = " ".join(current)
                    out.append(piece(text, self.counter.count(text), False))
                    current = [part]
                else:
                    current.append(part)
        if current:
            text = " ".join(current)
            out.append(piece(text, self.counter.count(text), False))
        return out

    def _hard_split(self, sentence: str) -> list[str]:
        if self.counter.count(sentence) <= self.piece_limit:
            return [sentence]
        words, parts, current = sentence.split(), [], []
        for word in words:
            if current and self.counter.count(" ".join([*current, word])) > self.piece_limit:
                parts.append(" ".join(current))
                current = []
            current.append(word)
        return [*parts, " ".join(current)] if current else parts

    def overlap(self, text: str) -> str:
        tail: list[str] = []
        for sentence in reversed(split_sentences(text)):
            if self.counter.count(" ".join([sentence, *tail])) > self.p.overlap_tokens:
                break
            tail.insert(0, sentence)
        return " ".join(tail)

    def pack(self, pieces: list[Piece]) -> list[tuple[list[Piece], str]]:
        """Group pieces into chunks. Returns (pieces, overlap_prefix) per chunk."""
        groups: list[list[Piece]] = []
        current: list[Piece] = []
        for piece in pieces:
            # Every group after the first will get an overlap prefix: reserve room for it.
            budget = self.p.max_tokens - (self.p.overlap_tokens if groups else 0)
            # v2: never mix flattened-table text with prose in one chunk.
            flag_change = self.p.v2 and current and current[-1].flags != piece.flags
            if current and (sum(x.tokens for x in current) + piece.tokens > budget or flag_change):
                groups.append(current)
                current = []
            current.append(piece)
        if current:
            groups.append(current)
        # Merge a small tail into its predecessor when the result stays under the hard limit.
        if len(groups) >= 2 and (not self.p.v2 or groups[-1][0].flags == groups[-2][-1].flags):
            tail_tokens = sum(x.tokens for x in groups[-1])
            prefix_room = self.p.overlap_tokens if len(groups) > 2 else 0
            if tail_tokens < self.p.merge_tail_below_tokens and \
                    sum(x.tokens for x in groups[-2]) + tail_tokens + prefix_room <= self.p.hard_max_tokens:
                groups[-2:] = [groups[-2] + groups[-1]]
        result = []
        for i, group in enumerate(groups):
            same_kind = not self.p.v2 or (i and groups[i - 1][-1].flags == group[0].flags)
            prefix = self.overlap(" ".join(x.text for x in groups[i - 1])) if i and same_kind else ""
            result.append((group, prefix))
        return result


# ---------------------------------------------------------------- document


def chunk_document(document: str, info: DocumentInfo, profile: ChunkingProfile,
                   counter: TokenCounter) -> ChunkingResult:
    blocks = parse_blocks(document, profile.normalizer)
    headings = [b for b in blocks if b.kind == "heading"]
    root = headings[0] if headings and _same_title(headings[0].text, info.title) else None
    has_subheadings = any(h is not root for h in headings)

    layout = None
    if profile.pdf_layout and not has_subheadings:
        lookup = _page_lookup(info.source_id, document) if profile.page_maps and "SOURCE_PDF_PAGE" not in document \
            else None
        layout = layout_blocks(document, lookup, rules=profile.rules)
        blocks, root = layout.blocks, None
        has_subheadings = False  # no front-matter filtering: layout text has no reliable front matter boundary
    content_blocks = [b for b in blocks if b.kind in ("paragraph", "table")]
    removed_chars = sum(layout.removed.values()) if layout else 0
    result = ChunkingResult(chunks=[], body_chars=sum(len(b.text) for b in content_blocks) + removed_chars,
                            layout=layout)
    if layout:
        for reason, chars in layout.removed.items():
            result.dropped[reason] += chars

    rules = SECTION_RULES_V2 if profile.v2 else SECTION_RULES
    not_retrievable = NOT_RETRIEVABLE_V2 if profile.v2 else NOT_RETRIEVABLE
    front_type = "abstract_inferred" if info.source_type and "research" in info.source_type else "overview_inferred"

    # 1) Assign every content block to a section path (or drop it, with a reason).
    sections: list[tuple[tuple[str, ...], str | None, list[tuple[Block, int | None]]]] = []
    stack: list[tuple[int, str]] = []
    page: int | None = None
    in_front = has_subheadings
    for block in blocks:
        if block.kind == "page":
            page = block.page
            continue
        if block.kind == "heading":
            if block is not root:
                in_front = False
                while stack and stack[-1][0] >= block.level:
                    stack.pop()
                stack.append((block.level, block.text))
            continue
        # Empty level-1 headings from the layout pass close a running title; they never appear in a path.
        path = tuple(text for _, text in stack if text or layout is None)
        forced_type = None
        if in_front:
            words = len(block.text.split())
            if block.kind == "paragraph" and words >= profile.front_matter_min_words \
                    and re.search(r"[.!?]", block.text) and not FRONT_NOISE.search(block.text):
                forced_type = front_type
            else:
                result.dropped["front_matter_metadata"] += len(block.text)
                continue
        if not block.text.strip():
            result.dropped["empty_table"] += len(block.text)
            continue
        if sections and sections[-1][0] == path and sections[-1][1] == forced_type:
            sections[-1][2].append((block, page))
        else:
            sections.append((path, forced_type, [(block, page)]))

    # 2) Pack each section independently.
    packer = _SectionPacker(profile, counter)
    gaps_context = _missing_context(info) if info.corpus_role == "gaps" else None
    table_pages = recovered_table_pages(info.source_id) if profile.table_review and layout else set()
    layout_pages = [b.page_end for b in blocks if b.page_end is not None]
    front_page_limit = max(5, -(-max(layout_pages) // 10)) if layout and layout_pages else None  # first 10%
    fallback_type = "unclassified" if layout else "body"
    for path, forced_type, items in sections:
        section_type = forced_type or classify_section(path, fallback_type if not path else "body", rules)
        # Publishers (e.g. MDPI) print tables after the reference list; they are content, not references.
        table_path, table_type = (("Tables",), "floating_table") if section_type in not_retrievable \
            else (path, section_type)
        drafts: list[_Draft] = []
        buffer: list[Piece] = []
        open_table: tuple[Block, int | None, list[Piece], list[Piece]] | None = None  # block, page, caption, notes

        def flush(buf: list[Piece], out: list[_Draft] = drafts, p: tuple[str, ...] = path,
                  t: str = section_type) -> None:
            for group, prefix in packer.pack(buf):
                body = "\n\n".join(x.text for x in group)
                out.append(_Draft("text", f"{prefix}\n\n{body}" if prefix else body, group, bool(prefix), p, t))

        def close_table(out: list[_Draft] = drafts, p: tuple[str, ...] = table_path, t: str = table_type) -> None:
            nonlocal open_table
            if open_table:
                block, block_page, caption, notes = open_table
                out.extend(_table_drafts(block, block_page, caption, notes, packer, p, t))
                open_table = None

        for block, block_page in items:
            if block.kind == "table":
                close_table()
                caption: list[Piece] = []
                for i in range(len(buffer) - 1, max(len(buffer) - 3, -1), -1):
                    if buffer[i].whole_paragraph and TABLE_CAPTION.match(buffer[i].text):
                        caption, buffer = buffer[i:], buffer[:i]
                        break
                flush(buffer)
                buffer = []
                open_table = (block, block_page, caption, [])
                continue
            pieces = packer.pieces(block, block_page)
            if open_table and len(pieces) == 1 and pieces[0].tokens <= FOOTNOTE_MAX_TOKENS \
                    and TABLE_FOOTNOTE.search(pieces[0].text):
                open_table[3].append(pieces[0])
                continue
            close_table()
            buffer.extend(pieces)
        close_table()
        flush(buffer)

        for draft in drafts:
            result.chunks.append(_finish(draft, len(result.chunks), gaps_context, not_retrievable, profile, counter,
                                         from_layout=layout is not None, table_pages=table_pages,
                                         front_page_limit=front_page_limit))
    return result


def _finish(draft: _Draft, index: int, gaps_context: str | None, not_retrievable: set[str],
            profile: ChunkingProfile, counter: TokenCounter, from_layout: bool = False,
            table_pages: set[int] | None = None, front_page_limit: int | None = None) -> Chunk:
    group, content = draft.pieces, draft.content
    section_type = draft.section_type
    first_page = min((x.page_start for x in group if x.page_start is not None), default=None)
    # v2_1: author lists with affiliation marks are front matter only on the front pages; deeper in a report the
    # same pattern is a table of regions or services ("University Health Board 12").
    on_front_pages = profile.rules != "v2_1" or first_page is None or front_page_limit is None \
        or first_page <= front_page_limit
    if profile.content_detection and draft.kind == "text" and section_type not in not_retrievable:
        section_type = detect_list_type(content) or section_type
        if from_layout and (len(set(m.group(0).lower() for m in PUBLICATION_INFO.finditer(content))) >= 2
                            or (on_front_pages and len(AUTHOR_WITH_AFFILIATION_MARK.findall(content)) >= 5)):
            section_type = "front_matter_detected"
        if len(DOT_LEADER.findall(content)) >= 3:  # table of contents: "Background ........ 1"
            section_type = "front_matter_detected"
    if profile.v2 and draft.kind == "text" and len(re.findall(r"[A-Za-z]{3,}", content)) < 3:
        section_type = "noise"  # e.g. a stray page number left in unpaged PDF text
    flattened = any("flattened_table" in x.flags for x in group)
    if profile.rules == "v2_1" and from_layout and draft.kind == "text" and not flattened:
        # PDF table rows wrapped irregularly escape the line-based detector; a chunk made mostly of numbers is
        # still table data whose column headers are lost ("training 180.79 (548.03) 145.67 (428.49) ...").
        tokens = content.split()
        numbers = sum(bool(NUMERIC_TOKEN.fullmatch(t)) for t in tokens)
        share = numbers / max(1, len(tokens))
        # ... and a short fragment of effect sizes ("None 289 295 – SMD 0.3 SD higher") is a table cut loose
        # from its outcome label — the most dangerous kind of number to retrieve.
        flattened = ((numbers >= 20 and share >= 0.25) or (numbers >= 10 and share >= 0.3)
                     or (numbers >= 3 and share >= 0.25 and len(tokens) < 40))
    starts = [x.page_start for x in group if x.page_start is not None]
    ends = [x.page_end if x.page_end is not None else x.page_start for x in group if x.page_start is not None]
    pages = set(range(min(starts), max(ends) + 1)) if starts else set()
    no_pages = profile.page_maps and from_layout and not starts
    # v2_1: table rows can sit inside an otherwise prose chunk ("Language development 0.00 -0.15, 0.15 4 0.23").
    # A run of numbers is treated as embedded table data: >= 5 always; >= 4 when a structured table was
    # recovered from the original PDF on one of the chunk's pages (then it awaits review with that table).
    embedded_table = False
    if profile.rules == "v2_1" and from_layout and draft.kind == "text" and not flattened:
        run = longest_numeric_run(content)
        embedded_table = run >= 5 or (run >= 4 and bool(pages & (table_pages or set())))
        flattened = embedded_table
    encoding_lost = profile.rules == "v2_1" and bool(GLYPH_ID.search(content))
    # Every page the flattened chunk spans must hold a recovered table, not just one of them.
    if encoding_lost:
        status = "text_encoding_lost"
        note = ("Văn bản trích xuất chứa mã glyph (/gidNNNNN) thay vì chữ — font PDF thiếu bảng ánh xạ ký tự; "
                "có bản trích xuất lại đề xuất trong data/extractions, chờ người duyệt.")
        missing = f"{note} {gaps_context}" if gaps_context else note
    elif flattened and profile.table_review and pages and (
            pages <= (table_pages or set()) or (embedded_table and pages & (table_pages or set()))):
        status = "table_recovered_pending_review"
        note = ("Bảng trong PDF mất cấu trúc trong văn bản trích xuất; đã dựng lại từ PDF gốc (data/extractions) và "
                "qua kiểm tra tự động, nhưng chưa được người duyệt — không dùng cho truy xuất.")
        missing = f"{note} {gaps_context}" if gaps_context else note
    elif flattened and profile.table_review:
        status = "table_structure_unrecoverable"
        note = ("Bảng trong PDF mất cấu trúc hàng/cột và không dựng lại được một cách tin cậy; "
                "không dùng số liệu từ đoạn này.")
        missing = f"{note} {gaps_context}" if gaps_context else note
    elif flattened:
        status = "table_structure_lost"
        note = "Bảng trong PDF đã mất cấu trúc hàng/cột khi trích xuất; không dùng số liệu từ đoạn này."
        missing = f"{note} {gaps_context}" if gaps_context else note
    elif no_pages:
        status = "page_provenance_incomplete"
        missing = "Không xác định được trang gốc của đoạn này (không có bản đồ trang đã kiểm chứng)."
    elif MISSING_COMPONENT_MENTION.search(content):
        status = "references_missing_component"
        note = "Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản."
        missing = f"{note} {gaps_context}" if gaps_context else note
    elif gaps_context:
        status, missing = "document_has_gaps", gaps_context
    else:
        status, missing = "complete", None
    return Chunk(
        chunk_index=index, section_path=draft.path, section_type=section_type, content_kind=draft.kind,
        page_start=min(starts) if starts else None, page_end=max(ends) if ends else None,
        char_start=min(x.start for x in group), char_end=max(x.end for x in group),
        content=content, token_count=counter.count(content), completeness_status=status, missing_context=missing,
        retrieval_eligible=section_type not in not_retrievable and not flattened and not no_pages and not encoding_lost,
        has_overlap=draft.has_overlap,
    )


@dataclass(frozen=True)
class _Draft:
    kind: str
    content: str
    pieces: list[Piece]
    has_overlap: bool
    path: tuple[str, ...]
    section_type: str


def _table_drafts(block: Block, page: int | None, caption: list[Piece], notes: list[Piece],
                  packer: _SectionPacker, path: tuple[str, ...], section_type: str) -> list[_Draft]:
    """Caption + rows + footnotes; split by rows (repeating caption, header and notes) when too long."""
    rows = block.text.split("\n")
    head = "\n".join(x.text for x in caption)
    tail = "\n".join(x.text for x in notes)
    span = [block, *caption, *notes]
    p_start = block.page_start if block.page_start is not None else page
    anchor = Piece("", 0, min(x.start for x in span), max(x.end for x in span), p_start,
                   block.page_end if block.page_end is not None else p_start)

    def draft(body_rows: list[str]) -> _Draft:
        return _Draft("table", "\n".join(filter(None, [head, *body_rows, tail])), [anchor], False, path, section_type)

    whole = draft(rows)
    if packer.counter.count(whole.content) <= packer.p.max_tokens or len(rows) < 3:
        return [whole]
    # v2 Markdown tables: the header is every row up to and including the |---| separator.
    sep = next((i for i, r in enumerate(rows[:6]) if TABLE_SEPARATOR.match(r)), None) if packer.p.v2 else None
    header_rows = rows[: sep + 1] if sep is not None else rows[:1]
    out, current = [], []
    for row in rows[len(header_rows):]:
        if current and packer.counter.count(draft([*header_rows, *current, row]).content) > packer.p.max_tokens:
            out.append(draft([*header_rows, *current]))
            current = []
        current.append(row)
    if current:
        out.append(draft([*header_rows, *current]))
    return out
