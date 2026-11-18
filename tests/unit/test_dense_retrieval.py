"""Dense retrieval baseline: unit tests with fake embedders, readers and connections (no network, no DB)."""

import hashlib
import json
import re
from dataclasses import replace

import httpx
import psycopg
import pytest

from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import CohereEmbedder, EmbeddingProfile
from app.retrieval.query_embedding import CachedQueryEmbedder, CohereQueryEmbedder, cache_key
from app.retrieval.research_reader import ResearchVectorReader, build_sql
from app.retrieval.types import RetrievalError, RetrievalProfile

EP = EmbeddingProfile.load("cohere_embed_v4_1536_v1")
RP = RetrievalProfile.load("dense_baseline_v1")
DIM = EP.vector_dimension


def unit(i: int = 0) -> list[float]:
    v = [0.0] * DIM
    v[i] = 1.0
    return v


class FakeEmbedder:
    def __init__(self, vector=None, profile=EP, error=None):
        self.profile, self.vector, self.error, self.seen = profile, vector or unit(), error, []

    def embed_queries(self, texts):
        self.seen += list(texts)
        if self.error:
            raise self.error
        return [self.vector for _ in texts]


def row(i: int, distance: float = 0.1, **kw) -> dict:
    content = f"chunk content {i}"
    base = {"chunk_id": f"D{i}#section_v2_1#{i:04d}", "source_id": f"S{i}", "document_id": f"D{i}", "title": "T",
            "source_url": "https://example.org", "section_heading": "Results", "section_path": ["Results"],
            "page_start": None, "page_end": None, "char_start": 0, "char_end": 10, "content": content,
            "content_sha256": hashlib.sha256(content.encode()).hexdigest(), "chunking_profile": "section_v2_1",
            "document_version": "v1", "authorization_id": 2, "profile_code": EP.profile_code,
            "model_id": EP.model_id, "vector_dimension": DIM, "distance": distance}
    return base | kw


class FakeReader:
    def __init__(self, rows=None, error=None):
        self.rows, self.error, self.calls = rows if rows is not None else [row(1, 0.1), row(2, 0.2)], error, []

    def search(self, vector, k):
        self.calls.append((len(vector), k))
        if self.error:
            raise self.error
        return self.rows[:k]


def retriever(reader=None, embedder=None, log=None):
    return DenseRetriever(RP, embedder or FakeEmbedder(), reader or FakeReader(), log=log)


# --------------------------------------------------------------------------- configuration / validation
def test_profiles_are_consistent_with_the_verified_embedding_profile():
    assert (RP.embedding_profile, RP.similarity_metric, RP.score_type) == (EP.profile_code, "cosine", "cosine_distance")
    assert RP.k_probe == (5, 10, 20) and not RP.query_expansion and RP.db_role == "research_reader"


@pytest.mark.parametrize("query", ["", "   ", None, 12])
def test_empty_or_non_text_query_is_rejected(query):
    with pytest.raises(RetrievalError) as e:
        retriever().retrieve(query)
    assert e.value.category == "invalid_query"


def test_too_long_query_is_rejected_before_any_embedding():
    emb = FakeEmbedder()
    with pytest.raises(RetrievalError) as e:
        retriever(embedder=emb).retrieve("x" * (RP.max_query_chars + 1))
    assert e.value.category == "invalid_query" and emb.seen == []


@pytest.mark.parametrize("k", [0, -1, RP.k_max + 1, 2.5, True, "5"])
def test_invalid_k_is_rejected(k):
    with pytest.raises(RetrievalError) as e:
        retriever().retrieve("tự kỷ là gì", k=k)
    assert e.value.category == "invalid_k"


def test_profile_mismatch_is_rejected_at_construction():
    other = replace(EP, profile_code="other_profile")
    with pytest.raises(RetrievalError) as e:
        DenseRetriever(RP, FakeEmbedder(profile=other), FakeReader())
    assert e.value.category == "profile_mismatch"


def test_wrong_query_dimension_fails_closed():
    reader = FakeReader()
    with pytest.raises(RetrievalError) as e:
        retriever(reader=reader, embedder=FakeEmbedder(vector=[0.1] * 1024)).retrieve("tự kỷ")
    assert e.value.category == "dimension_mismatch" and reader.calls == []


def test_zero_query_vector_fails_closed():
    with pytest.raises(RetrievalError) as e:
        retriever(embedder=FakeEmbedder(vector=[0.0] * DIM)).retrieve("q")
    assert e.value.category == "dimension_mismatch"


def test_embedding_failure_fails_closed():
    reader = FakeReader()
    with pytest.raises(RetrievalError) as e:
        retriever(reader=reader, embedder=FakeEmbedder(error=RetrievalError("embedding_failed", "x"))).retrieve("q")
    assert e.value.category == "embedding_failed" and reader.calls == []


# --------------------------------------------------------------------------- SQL
def test_sql_is_parameterized_and_uses_only_the_view_and_cosine_operator():
    sql = build_sql(RP)
    assert "FROM asd_rag.v_research_retrieval_chunks" in sql and "<=>" in sql
    assert "%(q)s::vector" in sql and "%(k)s" in sql and "%(profile)s" in sql
    assert sql.index("ORDER BY") < sql.index("LIMIT")
    assert "chunk_id ASC" in sql
    assert re.findall(r"FROM\s+(\S+)", sql) == ["asd_rag.v_research_retrieval_chunks"]
    assert "JOIN" not in sql.upper() and "research_chunk_embeddings" not in sql


def test_unknown_view_or_metric_is_refused():
    with pytest.raises(RetrievalError):
        build_sql(replace(RP, view="asd_rag.chunks"))
    with pytest.raises(RetrievalError):
        build_sql(replace(RP, similarity_metric="l2"))


class FakeCursor:
    def __init__(self, rows, names):
        self._rows, self.description = rows, [type("D", (), {"name": n}) for n in names]

    def fetchone(self):
        return self._rows[0]

    def fetchall(self):
        return self._rows


class FakeConn:
    def __init__(self, user="asd_rag_v2_research_reader", error=None, rows=()):
        self.user, self.error, self.rows, self.executed, self.read_only = user, error, list(rows), [], None

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        if sql == "SELECT current_user":
            return FakeCursor([(self.user,)], ["current_user"])
        if self.error:
            raise self.error
        names = list(self.rows[0]) if self.rows else ["chunk_id"]
        return FakeCursor([tuple(r.values()) for r in self.rows], names)


def test_reader_binds_query_text_free_parameters_and_sets_read_only():
    conn = FakeConn(rows=[row(1)])
    out = ResearchVectorReader(RP, lambda: conn).search(unit(3), 5)
    sql, params = conn.executed[-1]
    assert conn.read_only is True and out[0]["chunk_id"] == row(1)["chunk_id"]
    assert params["k"] == 5 and params["profile"] == EP.profile_code and params["q"].startswith("[")
    assert params["q"] not in sql


def test_reader_refuses_any_role_other_than_the_research_reader():
    conn = FakeConn(user="asd_rag_v2_ingest")
    with pytest.raises(RetrievalError) as e:
        ResearchVectorReader(RP, lambda: conn).search(unit(), 5)
    assert e.value.category == "wrong_role" and len(conn.executed) == 1


@pytest.mark.parametrize("error,category", [
    (psycopg.errors.InsufficientPrivilege("x"), "permission_denied"),
    (psycopg.errors.UndefinedTable("x"), "view_missing"),
    (psycopg.errors.QueryCanceled("x"), "query_timeout"),
    (psycopg.OperationalError("x"), "database_unavailable"),
    (psycopg.errors.DataException("x"), "database_error")])
def test_database_errors_map_to_fail_closed_categories(error, category):
    with pytest.raises(RetrievalError) as e:
        ResearchVectorReader(RP, lambda: FakeConn(error=error)).search(unit(), 5)
    assert e.value.category == category


def test_connection_failure_does_not_fall_back_to_another_role():
    def refuse():
        raise psycopg.OperationalError("down")
    with pytest.raises(RetrievalError) as e:
        ResearchVectorReader(RP, refuse).search(unit(), 5)
    assert e.value.category == "database_unavailable"


# --------------------------------------------------------------------------- results / provenance
def test_response_schema_ranks_and_score_semantics():
    r = retriever().retrieve("Dấu hiệu sớm của tự kỷ?", k=2, question_id="q007")
    assert r.status == "ok" and r.k_requested == 2 and r.question_id == "q007" and r.authorization_version == 2
    assert r.query_expansion is False
    assert r.query_sha256 == hashlib.sha256("Dấu hiệu sớm của tự kỷ?".encode()).hexdigest()
    first = r.results[0]
    assert [c.rank for c in r.results] == [1, 2]
    assert first.score_type == "cosine_distance" and first.score == 0.1
    assert first.cosine_similarity == pytest.approx(0.9)
    assert first.corpus_version == "section_v2_1@v1" and first.char_range == "0-10" and first.page is None
    assert first.section == "Results" and first.embedding_profile == EP.profile_code


def test_top_k_upper_boundary_is_accepted():
    r = retriever(reader=FakeReader([row(i) for i in range(RP.k_max)])).retrieve("q", k=RP.k_max)
    assert len(r.results) == RP.k_max and [x.rank for x in r.results] == list(range(1, RP.k_max + 1))


def test_page_range_formatting():
    r = retriever(reader=FakeReader([row(1, page_start=3, page_end=4, char_start=None, char_end=None)])).retrieve("q")
    assert r.results[0].page == "3-4" and r.results[0].char_range is None


@pytest.mark.parametrize("bad", [
    {"source_id": None}, {"content_sha256": "0" * 64}, {"model_id": "embed-english-v3.0"},
    {"vector_dimension": 1024}, {"char_start": None, "char_end": None}, {"distance": 2.5},
    {"distance": float("nan")}, {"authorization_id": None}])
def test_invalid_provenance_fails_the_whole_response(bad):
    with pytest.raises(RetrievalError) as e:
        retriever(reader=FakeReader([row(1), row(2, **bad)])).retrieve("q", k=2)
    assert e.value.category == "provenance_invalid"


def test_mixed_authorizations_fail():
    with pytest.raises(RetrievalError) as e:
        retriever(reader=FakeReader([row(1), row(2, authorization_id=1)])).retrieve("q", k=2)
    assert e.value.category == "provenance_invalid"


def test_duplicate_chunk_ids_fail_closed():
    duplicate = row(1)
    with pytest.raises(RetrievalError) as e:
        retriever(reader=FakeReader([duplicate, duplicate])).retrieve("q", k=2)
    assert e.value.category == "provenance_invalid"


def test_no_results_is_explicit():
    r = retriever(reader=FakeReader([])).retrieve("q", k=5)
    assert r.status == "no_results" and r.results == [] and r.authorization_version is None


def test_reader_error_propagates_without_partial_results():
    with pytest.raises(RetrievalError) as e:
        retriever(reader=FakeReader(error=RetrievalError("permission_denied", "x"))).retrieve("q")
    assert e.value.category == "permission_denied"


# --------------------------------------------------------------------------- logging
def test_log_never_contains_the_query_text_and_records_errors(tmp_path):
    log = JsonlRetrievalLog(tmp_path, "t.jsonl")
    retriever(log=log).retrieve("bí mật câu hỏi", k=1, question_id="q001")
    with pytest.raises(RetrievalError):
        retriever(log=log).retrieve("", k=1)
    lines = [json.loads(x) for x in (tmp_path / "t.jsonl").read_text(encoding="utf-8").splitlines()]
    assert "bí mật" not in (tmp_path / "t.jsonl").read_text(encoding="utf-8")
    assert lines[0]["status"] == "ok" and lines[0]["query_expansion"] is False and lines[0]["returned"][0]["rank"] == 1
    assert lines[1]["status"] == "error" and lines[1]["error_category"] == "invalid_query"
    with pytest.raises(ValueError):
        log.write({"query": "x"})


# --------------------------------------------------------------------------- query embedding adapters
def test_cohere_query_embedder_uses_search_query_and_1536_dims():
    seen = []

    def handler(request):
        body = json.loads(request.content)
        seen.append(body)
        return httpx.Response(200, json={"embeddings": {"float": [unit() for _ in body["texts"]]}})

    client = CohereEmbedder(EP, "test-key-not-real", transport=httpx.MockTransport(handler), sleep=lambda s: None)
    out = CohereQueryEmbedder(EP, client).embed_queries(["a", "b"])
    assert len(out) == 2 and len(out[0]) == DIM
    assert seen[0]["input_type"] == "search_query" and seen[0]["output_dimension"] == 1536
    assert seen[0]["model"] == "embed-v4.0" and seen[0]["texts"] == ["a", "b"]


def test_cohere_errors_become_embedding_failed():
    client = CohereEmbedder(EP, "k", transport=httpx.MockTransport(lambda r: httpx.Response(401)), sleep=lambda s: None)
    with pytest.raises(RetrievalError) as e:
        CohereQueryEmbedder(EP, client).embed_queries(["a"])
    assert e.value.category == "embedding_failed"


def test_cache_is_offline_by_default_and_never_stores_text(tmp_path):
    with pytest.raises(RetrievalError) as e:
        CachedQueryEmbedder(EP, tmp_path).embed_queries(["chưa có"])
    assert e.value.category == "embedding_unavailable"
    inner = FakeEmbedder(vector=unit(7))
    cached = CachedQueryEmbedder(EP, tmp_path, inner)
    assert cached.embed_queries(["câu hỏi", "câu hỏi"]) == [unit(7), unit(7)]
    assert inner.seen == ["câu hỏi"] and cached.misses == 1
    offline = CachedQueryEmbedder(EP, tmp_path)
    assert offline.embed_queries(["câu hỏi"]) == [unit(7)] and offline.hits == 1
    stored = (tmp_path / f"{cache_key(EP, 'câu hỏi')}.json").read_text(encoding="utf-8")
    assert "câu hỏi" not in stored and '"input_type": "search_query"' in stored


def test_cache_entry_from_another_profile_is_rejected(tmp_path):
    key = cache_key(EP, "q")
    (tmp_path / f"{key}.json").write_text(json.dumps({"key": key, "profile_code": EP.profile_code,
        "model_id": "other", "vector_dimension": DIM, "input_type": "search_query", "vector": unit()}))
    with pytest.raises(RetrievalError) as e:
        CachedQueryEmbedder(EP, tmp_path).embed_queries(["q"])
    assert e.value.category == "profile_mismatch"


def test_malformed_cache_fails_closed(tmp_path):
    key = cache_key(EP, "q")
    (tmp_path / f"{key}.json").write_text("not-json", encoding="utf-8")
    with pytest.raises(RetrievalError) as e:
        CachedQueryEmbedder(EP, tmp_path).embed_queries(["q"])
    assert e.value.category == "cache_invalid"
