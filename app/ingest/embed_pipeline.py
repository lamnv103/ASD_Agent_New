"""Select embeddable chunks through the database gate, and store vectors idempotently.

Only chunks whose document is in v_embedding_eligible_documents (content approved, warning-free,
archive/text-mining/chunking/embedding/Cohere permissions all TRUE) are ever selected, so the
pipeline cannot send unapproved text to the provider. Each batch commits on its own (checkpoint);
a chunk that already has a vector for the profile with the same input hash is skipped (resume).
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Sequence
from dataclasses import dataclass

import psycopg

from app.retrieval.embeddings import EmbeddingProfile

ELIGIBLE_CHUNKS = """
SELECT c.chunk_id, c.document_id, s.title, c.section_heading, c.content
FROM chunks c
JOIN v_embedding_eligible_documents d ON d.document_id = c.document_id
JOIN sources s ON s.source_id = d.source_id
WHERE c.chunking_profile = %(chunking_profile)s AND c.retrieval_eligible
ORDER BY c.chunk_id
"""

BLOCKERS = """
SELECT d.source_id,
       d.content_review_status, d.content_warning, d.approved_for_embedding,
       r.archive_allowed, r.text_mining_allowed, r.chunking_allowed, r.embedding_allowed, r.cohere_processing_allowed,
       count(c.chunk_id) FILTER (WHERE c.retrieval_eligible) AS eligible_chunks,
       coalesce(sum(c.token_count) FILTER (WHERE c.retrieval_eligible), 0) AS eligible_tokens
FROM documents d
JOIN source_rights r ON r.source_id = d.source_id
LEFT JOIN chunks c ON c.document_id = d.document_id AND c.chunking_profile = %(chunking_profile)s
WHERE d.is_current
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9
ORDER BY 1
"""


@dataclass(frozen=True)
class EmbeddingInput:
    chunk_id: str
    document_id: str
    text: str
    input_hash: str


def build_input(profile: EmbeddingProfile, title: str, section_heading: str, content: str) -> str:
    return profile.input_template.format(title=title, section_heading=section_heading, content=content).strip()


def input_hash(profile: EmbeddingProfile, text: str) -> str:
    """Changes whenever the text, the model or the requested dimension changes."""
    key = f"{profile.provider}|{profile.model_id}|{profile.vector_dimension}|{profile.document_input_type}|{text}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def l2_norm(vector: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in vector))


def eligible_inputs(conn: psycopg.Connection, profile: EmbeddingProfile) -> list[EmbeddingInput]:
    rows = conn.execute(ELIGIBLE_CHUNKS, {"chunking_profile": profile.chunking_profile}).fetchall()
    out = []
    for chunk_id, document_id, title, heading, content in rows:
        text = build_input(profile, title, heading, content)
        out.append(EmbeddingInput(chunk_id, document_id, text, input_hash(profile, text)))
    return out


def pending(conn: psycopg.Connection, inputs: list[EmbeddingInput], profile_id: int) -> list[EmbeddingInput]:
    """Inputs without a stored vector for this profile and input hash (resume after interruption)."""
    done = {(cid, h) for cid, h in conn.execute(
        "SELECT chunk_id, embedding_input_hash FROM chunk_embeddings WHERE profile_id = %s", (profile_id,))}
    return [x for x in inputs if (x.chunk_id, x.input_hash) not in done]


def blockers(conn: psycopg.Connection, profile: EmbeddingProfile) -> list[dict]:
    cur = conn.execute(BLOCKERS, {"chunking_profile": profile.chunking_profile})
    names = [d.name for d in cur.description]
    rows = [dict(zip(names, r, strict=True)) for r in cur.fetchall()]
    for row in rows:
        reasons = []
        if row["content_review_status"] != "approved":
            reasons.append(f"content_review_status={row['content_review_status']}")
        if row["content_warning"]:
            reasons.append(f"warning={row['content_warning']}")
        if not row["approved_for_embedding"]:
            reasons.append("approved_for_embedding=false")
        for flag in ("archive_allowed", "text_mining_allowed", "chunking_allowed", "embedding_allowed",
                     "cohere_processing_allowed"):
            if row[flag] is not True:
                reasons.append(f"{flag}={'NULL' if row[flag] is None else row[flag]}")
        row["blocked_by"] = reasons
    return rows
