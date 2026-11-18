"""Cohere embedding client (the only module that calls the embedding API).

Never logs or returns input texts or the API key. Raises EmbeddingError with a code instead of
leaking provider response bodies. Vectors are validated (dimension, finiteness) before use; a
vector is never truncated or padded to fit.
"""

from __future__ import annotations

import json
import math
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import httpx

from app.config import ROOT

PROFILES_FILE = ROOT / "config" / "embedding_profiles.json"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class EmbeddingError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class EmbeddingProfile:
    profile_code: str
    provider: str
    model_id: str
    model_revision: str | None
    api_version: str
    endpoint: str
    vector_dimension: int
    document_input_type: str
    query_input_type: str
    similarity_metric: str
    truncate: str
    max_texts_per_call: int
    input_template: str
    chunking_profile: str
    max_attempts: int
    base_delay_seconds: float
    max_delay_seconds: float
    timeout_seconds: float

    @classmethod
    def load(cls, code: str, path: Path = PROFILES_FILE) -> EmbeddingProfile:
        cfg = json.loads(path.read_text(encoding="utf-8"))[code]
        if cfg["embedding_types"] != ["float"]:
            raise ValueError("only float embeddings are supported")
        return cls(profile_code=code, provider=cfg["provider"], model_id=cfg["model_id"],
                   model_revision=cfg["model_revision"], api_version=cfg["api_version"], endpoint=cfg["endpoint"],
                   vector_dimension=cfg["vector_dimension"], document_input_type=cfg["document_input_type"],
                   query_input_type=cfg["query_input_type"], similarity_metric=cfg["similarity_metric"],
                   truncate=cfg["truncate"], max_texts_per_call=cfg["max_texts_per_call"],
                   input_template=cfg["input_template"], chunking_profile=cfg["chunking_profile"],
                   max_attempts=cfg["retry"]["max_attempts"], base_delay_seconds=cfg["retry"]["base_delay_seconds"],
                   max_delay_seconds=cfg["retry"]["max_delay_seconds"], timeout_seconds=cfg["timeout_seconds"])

    def payload(self, texts: Sequence[str], input_type: str) -> dict:
        return {"model": self.model_id, "texts": list(texts), "input_type": input_type, "embedding_types": ["float"],
                "output_dimension": self.vector_dimension, "truncate": self.truncate}


def validate_vector(vector: object, dimension: int) -> list[float]:
    if not isinstance(vector, list) or len(vector) != dimension:
        raise EmbeddingError("invalid_vector", f"expected {dimension} coordinates")
    if any(isinstance(x, bool) or not isinstance(x, int | float) or not math.isfinite(x) for x in vector):
        raise EmbeddingError("invalid_vector", "non-numeric or non-finite coordinate")
    if not any(vector):
        raise EmbeddingError("invalid_vector", "zero vector")
    return [float(x) for x in vector]


class CohereEmbedder:
    def __init__(self, profile: EmbeddingProfile, api_key: str, transport: httpx.BaseTransport | None = None,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        if not api_key:
            raise EmbeddingError("missing_key", "COHERE_API_KEY is not set")
        self.profile = profile
        self._client = httpx.Client(timeout=profile.timeout_seconds, transport=transport,
                                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
        self._sleep = sleep
        self.calls = 0  # HTTP requests, retries included
        self.billed_input_tokens = 0  # from the provider's meta.billed_units, when reported

    def close(self) -> None:
        self._client.close()

    def embed(self, texts: Sequence[str], input_type: str) -> list[list[float]]:
        """Embed in batches of max_texts_per_call; order is preserved."""
        out: list[list[float]] = []
        step = self.profile.max_texts_per_call
        for i in range(0, len(texts), step):
            out.extend(self._call(texts[i:i + step], input_type))
        return out

    def _call(self, texts: Sequence[str], input_type: str) -> list[list[float]]:
        delay = self.profile.base_delay_seconds
        for attempt in range(1, self.profile.max_attempts + 1):
            self.calls += 1
            try:
                response = self._client.post(self.profile.endpoint, json=self.profile.payload(texts, input_type))
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                if attempt == self.profile.max_attempts:
                    raise EmbeddingError("provider_network", type(exc).__name__) from None
            else:
                if response.status_code == 200:
                    try:
                        body = response.json()
                    except (ValueError, TypeError):
                        raise EmbeddingError("invalid_response", "provider returned malformed JSON") from None
                    if not isinstance(body, dict):
                        raise EmbeddingError("invalid_response", "provider response must be an object")
                    embeddings = body.get("embeddings")
                    vectors = embeddings.get("float") if isinstance(embeddings, dict) else None
                    if not isinstance(vectors, list) or len(vectors) != len(texts):
                        raise EmbeddingError("invalid_response", "embedding count does not match input count")
                    billed = ((body.get("meta") or {}).get("billed_units") or {}).get("input_tokens")
                    if isinstance(billed, int | float):
                        self.billed_input_tokens += int(billed)
                    return [validate_vector(v, self.profile.vector_dimension) for v in vectors]
                if response.status_code in (401, 403):
                    raise EmbeddingError("provider_auth", f"HTTP {response.status_code}")
                if response.status_code not in RETRYABLE_STATUS or attempt == self.profile.max_attempts:
                    raise EmbeddingError("provider_http", f"HTTP {response.status_code}")
            self._sleep(min(delay, self.profile.max_delay_seconds))
            delay *= 2
        raise EmbeddingError("provider_http", "retries exhausted")  # pragma: no cover
