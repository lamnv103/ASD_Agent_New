"""HTTP contract tests; all embedder/reader dependencies are mocked."""

import hashlib

import pytest
from fastapi.testclient import TestClient

from app.api import create_app
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import EmbeddingProfile
from app.retrieval.types import RetrievalError, RetrievalProfile

EP = EmbeddingProfile.load("cohere_embed_v4_1536_v1")
RP = RetrievalProfile.load("dense_baseline_v1")


def unit_vector() -> list[float]:
    return [1.0] + [0.0] * (EP.vector_dimension - 1)


def make_row(chunk_id: str = "C1", **changes) -> dict:
    content = "Evidence-backed source passage."
    row = {
        "chunk_id": chunk_id, "source_id": "S1", "document_id": "D1", "title": "Source title",
        "source_url": "https://example.org/source", "section_heading": "Results", "section_path": ["Results"],
        "page_start": 4, "page_end": 4, "char_start": None, "char_end": None, "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "chunking_profile": "section_v2_1", "document_version": "v1", "authorization_id": 2,
        "profile_code": EP.profile_code, "model_id": EP.model_id, "vector_dimension": EP.vector_dimension,
        "distance": 0.2,
    }
    return row | changes


class FakeEmbedder:
    profile = EP

    def __init__(self, error=None):
        self.error = error

    def embed_queries(self, texts):
        if self.error:
            raise self.error
        return [unit_vector() for _ in texts]


class FakeReader:
    def __init__(self, rows=None, error=None):
        self.rows = rows or []
        self.error = error

    def search(self, vector, k):
        if self.error:
            raise self.error
        return self.rows[:k]


def client(rows=None, embed_error=None, reader_error=None):
    service = DenseRetriever(RP, FakeEmbedder(embed_error), FakeReader(rows, reader_error))
    return TestClient(create_app(service))


def test_valid_new_vietnamese_query_returns_actual_available_fields():
    response = client([make_row()]).post(
        "/api/retrieve", json={"query": "Trẻ tự kỷ có dấu hiệu giao tiếp nào?", "top_k": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success" and body["result_count"] == 1
    assert body["retrieval_method"] == "dense_baseline_v1" and body["embedding_model"] == "embed-v4.0"
    assert body["results"][0] == {
        "rank": 1, "chunk_id": "C1", "source_id": "S1", "document_title": "Source title",
        "section": "Results", "page": "4", "content": "Evidence-backed source passage.", "similarity": 0.8,
    }


@pytest.mark.parametrize("query", ["", "   "])
def test_empty_query_is_rejected(query):
    assert client().post("/api/retrieve", json={"query": query, "top_k": 5}).status_code == 422


def test_query_over_limit_is_rejected():
    assert client().post("/api/retrieve", json={"query": "x" * (RP.max_query_chars + 1), "top_k": 5}).status_code == 422


@pytest.mark.parametrize("top_k", [0, -1, 51, 2.5, "5", True])
def test_invalid_top_k_is_rejected(top_k):
    assert client().post("/api/retrieve", json={"query": "câu hỏi", "top_k": top_k}).status_code == 422


def test_embedding_unavailable_fails_closed():
    resp = client(embed_error=RetrievalError("embedding_unavailable", "cache miss")).post(
        "/api/retrieve", json={"query": "một câu hỏi mới chưa có cache", "top_k": 5})
    assert resp.status_code == 503 and resp.json()["detail"]["code"] == "embedding_unavailable"


def test_database_unavailable_fails_closed():
    resp = client(reader_error=RetrievalError("database_unavailable", "offline")).post(
        "/api/retrieve", json={"query": "câu hỏi", "top_k": 5})
    assert resp.status_code == 503 and resp.json()["detail"]["code"] == "database_unavailable"


def test_empty_retrieval_is_explicit():
    resp = client().post("/api/retrieve", json={"query": "câu hỏi", "top_k": 5})
    assert resp.status_code == 200 and resp.json()["status"] == "no_results"
    assert resp.json()["result_count"] == 0 and resp.json()["results"] == []


def test_duplicate_chunk_ids_fail_closed():
    row = make_row()
    resp = client([row, row]).post("/api/retrieve", json={"query": "câu hỏi", "top_k": 2})
    assert resp.status_code == 502 and resp.json()["detail"]["code"] == "provenance_invalid"


def test_missing_metadata_fails_closed():
    resp = client([make_row(source_id=None)]).post("/api/retrieve", json={"query": "câu hỏi", "top_k": 1})
    assert resp.status_code == 502 and resp.json()["detail"]["code"] == "provenance_invalid"


def test_default_app_has_no_external_embedder_and_cache_miss_is_unavailable():
    app = create_app()
    assert app.state.dense_retriever.embedder.inner is None
    resp = TestClient(app).post("/api/retrieve", json={"query": "unique uncached query 9fd2a7", "top_k": 5})
    assert resp.status_code == 503 and resp.json()["detail"]["code"] == "embedding_unavailable"
