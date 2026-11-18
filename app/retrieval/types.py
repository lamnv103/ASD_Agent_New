"""Retrieval contracts shared by every retriever (dense now; FTS / hybrid / rerank later).

Scores are named for what they are: `score_type = "cosine_distance"` (pgvector `<=>`, range [0, 2], lower is
closer). `cosine_similarity = 1 - distance` (range [-1, 1]). Neither is a probability of relevance.
Internal ids and scores are for evaluation and audit only; a user-facing answer must not show them.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from app.config import ROOT

PROFILES_FILE = ROOT / "config" / "retrieval_profiles.json"

ERROR_CATEGORIES = frozenset({
    "invalid_query", "invalid_k", "embedding_unavailable", "embedding_failed", "dimension_mismatch",
    "profile_mismatch", "database_unavailable", "permission_denied", "view_missing", "wrong_role",
    "query_timeout", "database_error", "provenance_invalid", "configuration_error", "cache_invalid",
})


class RetrievalError(RuntimeError):
    """Fail-closed error. `category` is one of ERROR_CATEGORIES; the message never contains secrets or the query."""

    def __init__(self, category: str, message: str) -> None:
        if category not in ERROR_CATEGORIES:
            raise ValueError(f"unknown retrieval error category {category!r}")
        self.category = category
        super().__init__(f"{category}: {message}")


@dataclass(frozen=True)
class RetrievalProfile:
    code: str
    retriever: str
    embedding_profile: str
    db_role: str
    expected_db_user: str
    view: str
    similarity_metric: str
    score_type: str
    k_default: int
    k_max: int
    k_probe: tuple[int, ...]
    max_query_chars: int
    query_expansion: bool
    query_cache_dir: Path
    log_dir: Path

    @classmethod
    def load(cls, code: str, path: Path = PROFILES_FILE) -> RetrievalProfile:
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))[code]
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            raise RetrievalError("configuration_error", f"retrieval profile {code!r} not loadable") from exc
        if cfg["query_expansion"]:
            raise RetrievalError("configuration_error", "query expansion is not part of the dense baseline")
        return cls(code=code, retriever=cfg["retriever"], embedding_profile=cfg["embedding_profile"],
                   db_role=cfg["db_role"], expected_db_user=cfg["expected_db_user"], view=cfg["view"],
                   similarity_metric=cfg["similarity_metric"], score_type=cfg["score_type"],
                   k_default=cfg["k_default"], k_max=cfg["k_max"], k_probe=tuple(cfg["k_probe"]),
                   max_query_chars=cfg["max_query_chars"], query_expansion=cfg["query_expansion"],
                   query_cache_dir=ROOT / cfg["query_cache_dir"], log_dir=ROOT / cfg["log_dir"])


@dataclass(frozen=True)
class RetrievedChunk:
    rank: int
    chunk_id: str
    source_id: str
    document_id: str
    title: str
    source_url: str
    content: str
    content_sha256: str
    section: str
    page: str | None
    char_range: str | None
    score_type: str
    score: float
    cosine_similarity: float
    authorization_version: int
    embedding_profile: str
    model_id: str
    corpus_version: str


@dataclass(frozen=True)
class RetrievalResponse:
    request_id: str
    question_id: str | None
    retriever: str
    status: str  # "ok" | "no_results"
    k_requested: int
    query_sha256: str
    query_expansion: bool
    embedding_profile: str
    authorization_version: int | None
    results: list[RetrievedChunk] = field(default_factory=list)
    latency_ms: dict[str, float] = field(default_factory=dict)
    timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
