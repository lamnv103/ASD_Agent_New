"""HTTP contract tests for the demo chat endpoint; all embedder/reader dependencies are mocked."""

import hashlib

import pytest
from fastapi.testclient import TestClient

from app.api import create_app
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import EmbeddingProfile
from app.retrieval.types import RetrievalError, RetrievalProfile

EP = EmbeddingProfile.load("cohere_embed_v4_1536_v1")
RP = RetrievalProfile.load("dense_baseline_v1")

ASD_QUERY = "Trẻ tự kỷ có dấu hiệu giao tiếp nào?"


def unit_vector() -> list[float]:
    return [1.0] + [0.0] * (EP.vector_dimension - 1)


def make_row(chunk_id: str = "C1", **changes) -> dict:
    content = changes.pop("content", (
        "Autism spectrum disorder (ASD) signs and symptoms include difficulty with social "
        "communication and interaction, as described in the DSM-5 criteria."))
    row = {
        "chunk_id": chunk_id, "source_id": "S1", "document_id": "D1", "title": "Signs and Symptoms of ASD",
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


def test_cached_asd_query_returns_real_evidence_and_a_grounded_answer():
    resp = client([make_row()]).post("/api/chat", json={"query": ASD_QUERY, "top_k": 1})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["answer_mode"] in {"topic_template", "extractive_fallback"}
    assert "C1" not in body["answer"]  # no bare chunk-code dumped into the answer prose
    assert body["retrieval_status"] == "ok"
    assert body["error"] is None
    assert body["evidence"] and body["evidence"][0]["source_id"] == "S1"
    assert body["evidence"][0]["source_url"] == "https://example.org/source"
    assert body["citations"][0]["source_url"] == "https://example.org/source"
    assert any("Nguyên mẫu nghiên cứu" in w for w in body["warnings"])


def test_out_of_scope_query_never_reaches_retrieval_or_returns_asd_evidence():
    resp = client([make_row()]).post("/api/chat", json={"query": "Hôm nay thời tiết thế nào?", "top_k": 5})
    assert resp.status_code == 200
    body = resp.json()
    assert body["retrieval_status"] == "out_of_scope"
    assert body["evidence"] == [] and body["citations"] == []


def test_greeting_never_calls_embedder_or_database():
    resp = client(embed_error=RuntimeError("must not be called"),
                  reader_error=RuntimeError("must not be called")).post(
        "/api/chat", json={"query": "Xin chào, bạn có thể giúp gì cho tôi?", "top_k": 5})
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer_mode"] == "greeting_template"
    assert body["retrieval_status"] == "skipped_greeting"
    assert "tự kỷ" in body["answer"].lower() or "asd" in body["answer"].lower()


def test_mixed_intent_greeting_plus_asd_question_answers_the_real_question():
    resp = client([make_row()]).post(
        "/api/chat", json={"query": "Chào bạn, " + ASD_QUERY, "top_k": 1})
    body = resp.json()
    assert body["retrieval_status"] == "ok"
    assert body["evidence"]


def test_uncached_asd_query_returns_503_query_not_cached_without_a_synthetic_vector():
    resp = client(embed_error=RetrievalError("embedding_unavailable", "cache miss")).post(
        "/api/chat", json={"query": ASD_QUERY, "top_k": 5})
    assert resp.status_code == 503
    body = resp.json()
    assert body["status"] == "blocked"
    assert body["answer"] is None
    assert body["answer_mode"] == "none"
    assert body["retrieval_status"] == "blocked_uncached"
    assert body["evidence"] == [] and body["citations"] == []
    assert body["error"]["code"] == "QUERY_NOT_CACHED"


def test_database_unavailable_fails_closed_through_chat():
    resp = client(reader_error=RetrievalError("database_unavailable", "offline")).post(
        "/api/chat", json={"query": ASD_QUERY, "top_k": 5})
    assert resp.status_code == 503
    assert resp.json()["error"]["code"] == "DB_UNAVAILABLE"
    assert resp.json()["status"] == "error"


def test_no_results_is_handled_safely_with_insufficient_evidence():
    resp = client([]).post("/api/chat", json={"query": ASD_QUERY, "top_k": 5})
    assert resp.status_code == 200
    body = resp.json()
    assert body["retrieval_status"] == "insufficient_evidence"
    assert body["evidence"] == []
    assert body["answer_mode"] == "insufficient_evidence"
    assert any("không đủ" in w.lower() or "chưa đủ" in body["answer"].lower() for w in body["warnings"])


def test_irrelevant_evidence_is_rejected_by_the_gate_even_when_retrieval_returns_rows():
    # The chunk is about ADHD medication, not ASD communication signs — the Evidence Gate must not
    # treat a Top-K hit as automatically sufficient.
    row = make_row(content="ADHD medication includes stimulants such as methylphenidate.")
    resp = client([row]).post("/api/chat", json={"query": "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?",
                                                  "top_k": 1})
    body = resp.json()
    assert body["answer_mode"] == "safety_refusal_dosing"
    assert body["evidence"] == []


def test_dosing_question_is_refused_before_retrieval_even_when_uncached():
    # embed_error would normally mean a cache-miss 503 — but a dosing question must never reach the
    # embedder at all, so the fake embedder's configured error never fires.
    resp = client(embed_error=RuntimeError("must not be called")).post(
        "/api/chat", json={"query": "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?", "top_k": 5})
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer_mode"] == "safety_refusal_dosing"
    assert body["retrieval_status"] == "refused_before_retrieval"


def test_generic_medication_adjustment_question_is_refused_with_no_drug_named():
    resp = client(embed_error=RuntimeError("must not be called")).post(
        "/api/chat", json={"query": "Có thể ngừng thuốc tâm thần cho con mà không hỏi bác sĩ không?",
                           "top_k": 5})
    body = resp.json()
    assert body["answer_mode"] == "safety_refusal_dosing"


@pytest.mark.parametrize("query", ["", "   "])
def test_empty_query_is_rejected(query):
    resp = client().post("/api/chat", json={"query": query, "top_k": 5})
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "INVALID_QUERY"


def test_query_over_limit_is_rejected():
    resp = client().post("/api/chat", json={"query": "x" * (RP.max_query_chars + 1), "top_k": 5})
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "INVALID_QUERY"


@pytest.mark.parametrize("top_k", [0, -1, 51, 2.5, "5", True])
def test_invalid_top_k_is_rejected(top_k):
    resp = client().post("/api/chat", json={"query": ASD_QUERY, "top_k": top_k})
    assert resp.status_code == 422


def test_duplicate_chunk_ids_fail_closed_through_chat():
    row = make_row()
    resp = client([row, row]).post("/api/chat", json={"query": ASD_QUERY, "top_k": 2})
    assert resp.status_code == 502
    assert resp.json()["error"]["code"] == "PROVENANCE_INVALID"


def test_citations_map_exactly_to_evidence_actually_used_in_the_answer():
    rows = [make_row("C1", page_start=1, page_end=1), make_row("C2", source_id="S2", page_start=2, page_end=2)]
    resp = client(rows).post("/api/chat", json={"query": ASD_QUERY, "top_k": 2})
    body = resp.json()
    assert [e["citation_id"] for e in body["evidence"]] == [c["citation_id"] for c in body["citations"]]
    assert [e["source_id"] for e in body["evidence"]] == [c["source_id"] for c in body["citations"]]


def test_default_app_chat_has_no_external_embedder_and_cache_miss_is_blocked():
    app = create_app()
    assert app.state.dense_retriever.embedder.inner is None
    resp = TestClient(app).post("/api/chat", json={"query": ASD_QUERY + " unique uncached 9fd2a7", "top_k": 5})
    assert resp.status_code == 503
    assert resp.json()["error"]["code"] == "QUERY_NOT_CACHED"


def test_system_status_reports_all_live_providers_disabled():
    resp = TestClient(create_app()).get("/api/system/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["demo_mode"] is True
    assert body["live_query_embedding_enabled"] is False
    assert body["live_reranking_enabled"] is False
    assert body["live_llm_enabled"] is False


def test_frontend_is_served_at_root():
    resp = TestClient(create_app()).get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
