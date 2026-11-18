"""Dense retrieval against the real database, as the research reader, with VECTOR FIXTURES (no API call).

Query vectors are document vectors read through the authorized view (or, for the D-1 neighbourhood test,
one excluded chunk's vector read by the owner in a read-only transaction). The SQL ordering is checked
against an independent brute-force cosine computation in Python over every vector the view exposes.
"""

import csv
import hashlib
import math

import psycopg
import pytest

from app.config import REPORTS
from app.db import connect
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import EmbeddingProfile
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalError, RetrievalProfile

pytestmark = pytest.mark.integration
EP = EmbeddingProfile.load("cohere_embed_v4_1536_v1")
RP = RetrievalProfile.load("dense_baseline_v1")


class NoEmbedder:
    """The DB half is tested with vectors; any attempt to embed text would be a test bug."""
    profile = EP

    def embed_queries(self, texts):
        raise AssertionError("integration tests must not call an embedding API")


def parse(text: str) -> list[float]:
    return [float(x) for x in text.strip("[]").split(",")]


@pytest.fixture(scope="module")
def corpus():
    with connect("research_reader", "integration_tests") as conn:
        rows = conn.execute("SELECT chunk_id, embedding::text FROM v_research_retrieval_chunks").fetchall()
        conn.rollback()
    return {cid: parse(v) for cid, v in rows}


@pytest.fixture(scope="module")
def d1():
    with open(REPORTS / "research_authorization_d1_exclusions_2026-11-14.csv", encoding="utf-8-sig") as f:
        return [r["chunk_id"] for r in csv.DictReader(f)]


@pytest.fixture(scope="module")
def dense():
    return DenseRetriever(RP, NoEmbedder(), ResearchVectorReader(RP))


def brute_force(corpus, q, k):
    qn = math.sqrt(sum(x * x for x in q))
    sims = {cid: sum(a * b for a, b in zip(q, v, strict=True)) / (qn * math.sqrt(sum(x * x for x in v)))
            for cid, v in corpus.items()}
    return sorted(sims, key=lambda c: (-sims[c], c))[:k], sims


def test_view_scope_is_the_authorized_2291_chunks(corpus):
    assert len(corpus) == 2291 and all(len(v) == 1536 for v in corpus.values())


@pytest.mark.parametrize("k", [5, 10, 20])
def test_top_k_matches_independent_brute_force_cosine(dense, corpus, k):
    fixtures = sorted(corpus)[::400][:5]
    for cid in fixtures:
        r = dense.retrieve_by_vector(corpus[cid], k=k, question_id="fixture")
        expected, sims = brute_force(corpus, corpus[cid], k)
        got = [c.chunk_id for c in r.results]
        assert len(got) == k and [c.rank for c in r.results] == list(range(1, k + 1))
        assert got[0] == cid and r.results[0].score == pytest.approx(0.0, abs=1e-5)
        # same set and same order up to floating-point ties
        assert {c for c in got} == set(expected) or all(
            abs(sims[a] - sims[b]) < 1e-6 for a, b in zip(got, expected, strict=True) if a != b)
        for c in r.results:
            assert c.cosine_similarity == pytest.approx(sims[c.chunk_id], abs=1e-5)
            assert c.score == pytest.approx(1 - sims[c.chunk_id], abs=1e-5)
        assert [c.score for c in r.results] == sorted(c.score for c in r.results)


def test_results_carry_valid_provenance(dense, corpus):
    r = dense.retrieve_by_vector(corpus[sorted(corpus)[7]], k=20)
    assert r.authorization_version == 2 and r.embedding_profile == EP.profile_code and r.status == "ok"
    for c in r.results:
        assert c.chunk_id and c.source_id and c.document_id and c.title and c.source_url.startswith("http")
        assert c.page is not None or c.char_range is not None
        assert hashlib.sha256(c.content.encode("utf-8")).hexdigest() == c.content_sha256
        assert c.model_id == "embed-v4.0" and c.corpus_version.startswith("section_v2_1@")
        assert c.score_type == "cosine_distance" and 0 <= c.score <= 2


def test_d1_excluded_chunks_never_come_back_even_for_their_own_vector(dense, d1):
    with connect("owner", "integration_tests") as owner:
        owner.read_only = True
        q = parse(owner.execute("SELECT embedding::text FROM research_chunk_embeddings WHERE chunk_id = %s",
                                (d1[0],)).fetchone()[0])
        owner.rollback()
    r = dense.retrieve_by_vector(q, k=20)
    assert len(r.results) == 20 and not {c.chunk_id for c in r.results} & set(d1)


def test_reader_session_is_the_research_reader_and_read_only():
    with connect("research_reader", "integration_tests") as conn:
        assert conn.execute("SELECT current_user, current_setting('default_transaction_read_only')").fetchone() == (
            "asd_rag_v2_research_reader", "on")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("SELECT 1 FROM research_chunk_embeddings LIMIT 1")


def test_reader_refuses_a_connection_with_another_role():
    reader = ResearchVectorReader(RP, lambda: connect("ingest", "integration_tests"))
    with pytest.raises(RetrievalError) as e:
        reader.search([0.0] * 1535 + [1.0], 5)
    assert e.value.category == "wrong_role"


def test_text_query_without_cache_or_api_fails_closed(tmp_path):
    from app.retrieval.query_embedding import CachedQueryEmbedder
    dense = DenseRetriever(RP, CachedQueryEmbedder(EP, tmp_path), ResearchVectorReader(RP))
    with pytest.raises(RetrievalError) as e:
        dense.retrieve("Dấu hiệu sớm của tự kỷ là gì?", k=5)
    assert e.value.category == "embedding_unavailable"
