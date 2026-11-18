"""Query embedding adapters for dense retrieval.

`CohereQueryEmbedder` reuses the project's single Cohere client with the profile's QUERY input type
(`search_query`), the same model and the same `output_dimension` as the document vectors.
`CachedQueryEmbedder` keeps query vectors on local disk keyed by sha256(profile|model|dim|input_type|text):
re-runs need no API call, and with no inner embedder it is strictly offline (cache miss -> fail closed).
The cache stores vectors and hashes only, never the query text.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from app.retrieval.embeddings import CohereEmbedder, EmbeddingError, EmbeddingProfile
from app.retrieval.types import RetrievalError


class QueryEmbedder(Protocol):
    profile: EmbeddingProfile

    def embed_queries(self, texts: Sequence[str]) -> list[list[float]]: ...


def check_vector(vector: object, profile: EmbeddingProfile) -> list[float]:
    if not isinstance(vector, list) or len(vector) != profile.vector_dimension:
        raise RetrievalError("dimension_mismatch", f"query vector must have {profile.vector_dimension} dimensions")
    if any(isinstance(x, bool) or not isinstance(x, int | float) or not math.isfinite(x) for x in vector):
        raise RetrievalError("dimension_mismatch", "query vector has non-numeric or non-finite values")
    values = [float(x) for x in vector]
    if not any(values):
        raise RetrievalError("dimension_mismatch", "query vector must not be zero")
    return values


class CohereQueryEmbedder:
    """Calls the Cohere Embed API. Sends only the query texts given to it."""

    def __init__(self, profile: EmbeddingProfile, client: CohereEmbedder) -> None:
        self.profile = profile
        self._client = client

    @property
    def api_calls(self) -> int:
        return self._client.calls

    def embed_queries(self, texts: Sequence[str]) -> list[list[float]]:
        try:
            vectors = self._client.embed(list(texts), self.profile.query_input_type)
        except EmbeddingError as exc:
            raise RetrievalError("embedding_failed", exc.code) from None
        return [check_vector(v, self.profile) for v in vectors]


def cache_key(profile: EmbeddingProfile, text: str) -> str:
    raw = f"{profile.profile_code}|{profile.model_id}|{profile.vector_dimension}|{profile.query_input_type}|{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class CachedQueryEmbedder:
    def __init__(self, profile: EmbeddingProfile, cache_dir: Path, inner: QueryEmbedder | None = None) -> None:
        if inner is not None and inner.profile.profile_code != profile.profile_code:
            raise RetrievalError("profile_mismatch", "inner embedder uses another embedding profile")
        self.profile = profile
        self.cache_dir = cache_dir
        self.inner = inner
        self.hits = 0
        self.misses = 0

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def _load(self, key: str) -> list[float] | None:
        path = self._path(key)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            raise RetrievalError("cache_invalid", f"cached query vector {key[:12]} is unreadable") from None
        if not isinstance(data, dict):
            raise RetrievalError("cache_invalid", f"cached query vector {key[:12]} has an invalid format")
        required = {"key", "profile_code", "model_id", "vector_dimension", "input_type", "vector"}
        if not required <= data.keys():
            raise RetrievalError("cache_invalid", f"cached query vector {key[:12]} is missing required fields")
        if (data["profile_code"], data["model_id"], data["vector_dimension"], data["input_type"]) != (
                self.profile.profile_code, self.profile.model_id, self.profile.vector_dimension,
                self.profile.query_input_type):
            raise RetrievalError("profile_mismatch", f"cached query vector {key[:12]} belongs to another profile")
        if data.get("key") != key:
            raise RetrievalError("cache_invalid", f"cached query vector {key[:12]} has a mismatched key")
        return check_vector(data["vector"], self.profile)

    def embed_queries(self, texts: Sequence[str]) -> list[list[float]]:
        keys = [cache_key(self.profile, t) for t in texts]
        found = {k: self._load(k) for k in dict.fromkeys(keys)}
        missing = [k for k, v in found.items() if v is None]
        self.hits += len(keys) - sum(1 for k in keys if k in missing)
        if missing:
            if self.inner is None:
                raise RetrievalError("embedding_unavailable",
                                     f"{len(missing)} query vectors not cached and API use is not enabled")
            todo = [texts[keys.index(k)] for k in missing]
            vectors = self.inner.embed_queries(todo)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            for k, v in zip(missing, vectors, strict=True):
                self._path(k).write_text(json.dumps({
                    "key": k, "profile_code": self.profile.profile_code, "model_id": self.profile.model_id,
                    "vector_dimension": self.profile.vector_dimension, "input_type": self.profile.query_input_type,
                    "l2_norm": math.sqrt(sum(x * x for x in v)), "vector": v}), encoding="utf-8")
                found[k] = v
            self.misses += len(missing)
        return [found[k] for k in keys]
