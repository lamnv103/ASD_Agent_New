"""Persist chunks for one (document, chunking profile). Replace-all per document keeps reruns idempotent."""

from __future__ import annotations

import psycopg

from app.ingest.chunking import Chunk, DocumentInfo


def chunk_id(document_id: str, profile: str, index: int) -> str:
    return f"{document_id}#{profile}#{index:04d}"


def replace_document_chunks(conn: psycopg.Connection, info: DocumentInfo, profile: str,
                            chunks: list[Chunk]) -> int:
    """Delete this document's chunks for the profile, then insert the new ones (caller's transaction)."""
    conn.execute("DELETE FROM chunks WHERE document_id = %s AND chunking_profile = %s", (info.document_id, profile))
    with conn.cursor() as cur:
        cur.executemany(
            """INSERT INTO chunks (chunk_id, document_id, chunk_index, chunking_profile, section_path, section_heading,
                   section_type, content_kind, page_start, page_end, char_start, char_end, content, language,
                   token_count, content_sha256, corpus_role, completeness_status, missing_context, retrieval_eligible)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            [(chunk_id(info.document_id, profile, c.chunk_index), info.document_id, c.chunk_index, profile,
              list(c.section_path), c.section_heading, c.section_type, c.content_kind, c.page_start, c.page_end,
              c.char_start, c.char_end, c.content, info.language, c.token_count, c.content_sha256, info.corpus_role,
              c.completeness_status, c.missing_context, c.retrieval_eligible) for c in chunks],
        )
    return len(chunks)
