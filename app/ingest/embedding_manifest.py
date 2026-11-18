"""Decide, chunk by chunk, what the research embedding run may send to the provider.

Pure functions (no database, no network) so the rules are unit-tested. A chunk is eligible only if
its document is current and not quarantined, the chunk passed chunking's own retrieval checks, its
structure status is verified, it carries provenance, it is not an undetermined fragment, and it is the
first chunk (by chunk_id) with its exact content. Every other chunk gets one explicit exclusion reason.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from urllib.parse import urlparse

VERIFIED_STATUSES = frozenset({"complete", "document_has_gaps", "references_missing_component"})
UNDETERMINED_SECTION_TYPES = frozenset({"unclassified"})
MIN_WORDS = 6
WORD = re.compile(r"\w+")
GLYPH_GARBAGE = re.compile(r"/gid\d")

# group membership: A = full-text corpus, B = non-commercial licence, C = agency-policy evidence only
GROUP_A_ROLES = frozenset({"core", "gaps"})
GROUP_B_RIGHTS = "verified_noncommercial_research"
GROUP_C_EVIDENCE = "agency_policy_only"


@dataclass(frozen=True)
class ChunkRow:
    chunk_id: str
    document_id: str
    source_id: str
    section_type: str
    completeness_status: str
    retrieval_eligible: bool
    content: str
    content_sha256: str
    file_format: str
    page_start: int | None
    page_end: int | None
    char_start: int | None
    char_end: int | None


def group_membership(corpus_role: str, rights_status: str, verification_status: str) -> tuple[str, ...]:
    groups = []
    if corpus_role in GROUP_A_ROLES:
        groups.append("A")
    if rights_status == GROUP_B_RIGHTS:
        groups.append("B")
    if verification_status == GROUP_C_EVIDENCE:
        groups.append("C")
    return tuple(groups)


def valid_url(url: str | None) -> bool:
    if not url or url != url.strip() or any(c.isspace() for c in url):
        return False
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and "." in parsed.netloc


def has_provenance(row: ChunkRow) -> bool:
    if row.file_format == "pdf":
        return row.page_start is not None and row.page_end is not None and row.page_start <= row.page_end
    return row.char_start is not None and row.char_end is not None and row.char_start < row.char_end


def word_count(text: str) -> int:
    return len(WORD.findall(text))


def chunk_exclusion(row: ChunkRow) -> str | None:
    """The first rule a chunk fails, or None. Order matters: structural reasons before content rules."""
    if row.completeness_status not in VERIFIED_STATUSES:
        return row.completeness_status  # table_structure_unrecoverable, text_encoding_lost, pending review, …
    if not row.retrieval_eligible:
        return f"non_content_section:{row.section_type}"
    if not row.content.strip():
        return "empty_chunk"
    if GLYPH_GARBAGE.search(row.content):
        return "text_encoding_lost"
    if not has_provenance(row):
        return "missing_provenance"
    if row.section_type in UNDETERMINED_SECTION_TYPES:
        return "undetermined_content_section"
    if word_count(row.content) < MIN_WORDS:
        return "fragment_too_short"
    return None


def classify(rows: Iterable[ChunkRow]) -> dict[str, str | None]:
    """chunk_id -> exclusion reason (None = eligible). Exact duplicates keep the first chunk_id."""
    out: dict[str, str | None] = {}
    first_by_hash: dict[str, str] = {}
    for row in sorted(rows, key=lambda r: r.chunk_id):
        reason = chunk_exclusion(row)
        if reason is None:
            keeper = first_by_hash.setdefault(row.content_sha256, row.chunk_id)
            if keeper != row.chunk_id:
                reason = f"duplicate_content_of:{keeper}"
        out[row.chunk_id] = reason
    return out
