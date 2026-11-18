"""Read-only checks of the research embedding track (migration 006). Run with:  pytest -m integration"""

import csv

import psycopg
import pytest

from app.config import REPORTS
from app.db import connect

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def ingest():
    with connect("ingest", "integration_tests") as conn:
        conn.read_only = True
        yield conn
        conn.rollback()


@pytest.fixture(scope="module")
def manifest():
    with open(REPORTS / "embedding_manifest.csv", encoding="utf-8-sig") as f:
        return {r["chunk_id"]: r for r in csv.DictReader(f)}


def test_every_manifest_chunk_has_exactly_one_valid_vector(ingest, manifest):
    rows = ingest.execute("""SELECT chunk_id, vector_dims(embedding), vector_dimension, model_id, input_type,
                                    content_sha256, embedding_input_hash FROM research_chunk_embeddings""").fetchall()
    assert len(rows) == len({r[0] for r in rows}) == len(manifest)
    for chunk_id, dims, dim, model, input_type, content_hash, input_hash in rows:
        m = manifest[chunk_id]
        assert (dims, dim, model, input_type) == (1536, 1536, "embed-v4.0", "search_document")
        assert (content_hash, input_hash) == (m["content_hash"], m["input_sha256"])


def test_no_vector_for_excluded_or_non_candidate_chunks(ingest):
    with open(REPORTS / "embedding_excluded.csv", encoding="utf-8-sig") as f:
        excluded = [r["chunk_id"] for r in csv.DictReader(f) if r["chunk_id"]]
    assert ingest.execute("SELECT count(*) FROM research_chunk_embeddings WHERE chunk_id = ANY(%s)",
                          (excluded,)).fetchone()[0] == 0
    # provenance: every vector was created under an authorization that allowlisted that exact content
    # (still true after that authorization is revoked; retrieval scope: test_research_retrieval_access.py)
    assert ingest.execute("""SELECT count(*) FROM research_chunk_embeddings e WHERE NOT EXISTS (
        SELECT 1 FROM research_embedding_authorization_chunks k WHERE k.authorization_id = e.authorization_id
          AND k.chunk_id = e.chunk_id AND k.content_sha256 = e.content_sha256)""").fetchone()[0] == 0


def test_research_track_is_not_production(ingest):
    assert ingest.execute("SELECT count(*) FROM research_embedding_authorizations "
                          "WHERE production_approval OR scope <> 'research_test'").fetchone()[0] == 0
    assert ingest.execute("SELECT count(*) FROM chunk_embeddings").fetchone()[0] == 0
    assert ingest.execute("SELECT count(*) FROM v_retrieval_ready_chunks").fetchone()[0] == 0


def test_app_role_cannot_read_research_vectors():
    with connect("app", "integration_tests") as app, pytest.raises(psycopg.errors.InsufficientPrivilege):
        app.execute("SELECT 1 FROM research_chunk_embeddings LIMIT 1")
