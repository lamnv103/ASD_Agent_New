"""Read-only access to the authorized research retrieval view (migration 007).

Connects only as the research reader role and fails closed: the session user is asserted, every database
error maps to a RetrievalError, and there is no fallback to another role or to the base tables.
The SQL text is fixed: the view and the distance operator come from whitelists, and the query vector,
profile and k are bound parameters. All authorization/eligibility filters (C5) live inside the view, so
`ORDER BY … LIMIT k` runs on already-filtered rows.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import psycopg

from app.db import connect
from app.retrieval.types import RetrievalError, RetrievalProfile

ALLOWED_VIEWS = {"asd_rag.v_research_retrieval_chunks"}
DISTANCE_OPERATORS = {"cosine": "<=>"}  # pgvector cosine distance, range [0, 2]
COLUMNS = ("chunk_id", "source_id", "document_id", "title", "source_url", "section_heading", "section_path",
           "page_start", "page_end", "char_start", "char_end", "content", "content_sha256", "chunking_profile",
           "document_version", "authorization_id", "profile_code", "model_id", "vector_dimension")


def build_sql(profile: RetrievalProfile) -> str:
    if profile.view not in ALLOWED_VIEWS:
        raise RetrievalError("configuration_error", "view is not an authorized retrieval view")
    op = DISTANCE_OPERATORS.get(profile.similarity_metric)
    if op is None:
        raise RetrievalError("configuration_error", f"unsupported metric {profile.similarity_metric!r}")
    return (f"SELECT {', '.join(COLUMNS)}, (embedding {op} %(q)s::vector) AS distance "
            f"FROM {profile.view} WHERE profile_code = %(profile)s "
            f"ORDER BY embedding {op} %(q)s::vector ASC, chunk_id ASC LIMIT %(k)s")


def vector_literal(vector: Sequence[float]) -> str:
    return "[" + ",".join(repr(float(x)) for x in vector) + "]"


class ResearchVectorReader:
    def __init__(self, profile: RetrievalProfile,
                 connect_fn: Callable[[], psycopg.Connection] | None = None) -> None:
        self.profile = profile
        self.sql = build_sql(profile)
        self._connect = connect_fn or (lambda: connect(profile.db_role, f"retrieval:{profile.code}"))  # type: ignore[arg-type]

    def search(self, vector: Sequence[float], k: int) -> list[dict]:
        try:
            conn = self._connect()
        except psycopg.OperationalError:
            raise RetrievalError("database_unavailable", "cannot connect as the research reader") from None
        try:
            with conn:
                conn.read_only = True
                user = conn.execute("SELECT current_user").fetchone()[0]
                if user != self.profile.expected_db_user:
                    raise RetrievalError("wrong_role", "connection is not the research reader role")
                cur = conn.execute(self.sql, {"q": vector_literal(vector), "profile": self.profile.embedding_profile,
                                              "k": k})
                names = [d.name for d in cur.description]
                return [dict(zip(names, row, strict=True)) for row in cur.fetchall()]
        except RetrievalError:
            raise
        except psycopg.errors.InsufficientPrivilege:
            raise RetrievalError("permission_denied", "research reader lacks access to the retrieval view") from None
        except psycopg.errors.UndefinedTable:
            raise RetrievalError("view_missing", "retrieval view does not exist") from None
        except psycopg.errors.QueryCanceled:
            raise RetrievalError("query_timeout", "retrieval query exceeded the statement timeout") from None
        except psycopg.OperationalError:
            raise RetrievalError("database_unavailable", "database connection failed during retrieval") from None
        except psycopg.Error as exc:
            raise RetrievalError("database_error", type(exc).__name__) from None
