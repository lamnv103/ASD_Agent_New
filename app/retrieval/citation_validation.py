"""Citation Validation (Phase 4): the last check before a source is shown to the user as a citation.

Checks, each required by the task brief:
1. The source exists — it must correspond to an actual `RetrievedChunk` from this response, not a
   fabricated entry.
2/3. The name/URL shown are exactly what the database returned for that chunk — never edited, never
   invented — by comparing field-for-field against the chunk the evidence item claims to come from.
4/5/6. The source actually supports the content — enforced upstream by only ever calling this with
   chunks that already passed the Evidence Sufficiency Gate (`evidence_gate.assess().supported`), so a
   chunk that merely appeared in the Top-K without being judged topically supporting never reaches here.

A citation that fails any check is dropped rather than shown "as if verified" — silence, not a guess.
"""

from __future__ import annotations

from app.retrieval.types import RetrievedChunk


def validate(evidence_items: list[dict], supported_chunks: list[RetrievedChunk]) -> list[dict]:
    by_citation = {f"C{c.rank}": c for c in supported_chunks}
    valid: list[dict] = []
    for item in evidence_items:
        chunk = by_citation.get(item.get("citation_id"))
        if chunk is None:
            continue  # not among the chunks the Evidence Gate judged supporting -> never shown
        if (item.get("source_id") != chunk.source_id or item.get("title") != (chunk.title or None)
                or item.get("source_url") != (chunk.source_url or None) or item.get("excerpt") != chunk.content):
            continue  # name/URL/content do not match the database record exactly -> never shown
        valid.append(item)
    return valid
