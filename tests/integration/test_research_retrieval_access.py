"""Research retrieval access (migration 007, Phase 6.2 T2): read-only checks on the real database.

Every query runs as the read-only research role, except the catalog/control queries (owner, read-only).
Mutation-based negative cases live in scripts/verify_research_access.py --mutations (isolated DB only).
"""

import csv

import psycopg
import pytest

from app.config import REPORTS
from app.db import connect

pytestmark = pytest.mark.integration
VIEW = "v_research_retrieval_chunks"


@pytest.fixture(scope="module")
def reader():
    with connect("research_reader", "integration_tests") as conn:
        yield conn
        conn.rollback()


@pytest.fixture(scope="module")
def owner():
    with connect("owner", "integration_tests") as conn:
        conn.read_only = True
        yield conn
        conn.rollback()


@pytest.fixture(scope="module")
def d1():
    with open(REPORTS / "research_authorization_d1_exclusions_2026-11-14.csv", encoding="utf-8-sig") as f:
        return [r["chunk_id"] for r in csv.DictReader(f)]


def test_view_returns_exactly_the_active_allowlist(reader, owner):
    visible = {r[0] for r in reader.execute(f"SELECT chunk_id FROM {VIEW}")}
    allow = {r[0] for r in owner.execute("""SELECT k.chunk_id FROM research_embedding_authorization_chunks k
        JOIN research_embedding_authorizations a USING (authorization_id) WHERE a.revoked_at IS NULL""")}
    assert visible == allow and len(visible) == 2291


def test_d1_reference_list_chunks_are_not_retrievable_but_vectors_are_kept(reader, owner, d1):
    assert len(d1) == 47
    assert reader.execute(f"SELECT count(*) FROM {VIEW} WHERE chunk_id = ANY(%s)", (d1,)).fetchone()[0] == 0
    kept = owner.execute("SELECT count(*) FROM research_chunk_embeddings WHERE chunk_id = ANY(%s)", (d1,)).fetchone()[0]
    assert kept == 47


def test_filtering_happens_before_limit(reader, owner, d1):
    q = owner.execute("SELECT embedding::text FROM research_chunk_embeddings WHERE chunk_id = %s",
                      (d1[0],)).fetchone()[0]
    sql = f"SELECT chunk_id FROM {VIEW} ORDER BY embedding <=> %s::vector LIMIT 10"
    top = [r[0] for r in reader.execute(sql, (q,))]
    assert len(top) == 10 and not set(top) & set(d1)


def test_only_one_active_authorization_and_the_old_one_is_kept(owner):
    rows = owner.execute("SELECT authorization_id, revoked_at IS NULL FROM research_embedding_authorizations "
                         "ORDER BY 1").fetchall()
    assert rows == [(1, False), (2, True)]


@pytest.mark.parametrize("table", ["chunks", "research_chunk_embeddings", "research_embedding_authorizations",
                                   "v_research_embedding_candidates", "source_rights", "v_retrieval_ready_chunks",
                                   "chunk_embeddings"])
def test_reader_cannot_read_anything_else(table):
    with connect("research_reader", "integration_tests") as conn, pytest.raises(psycopg.errors.InsufficientPrivilege):
        conn.execute(f"SELECT 1 FROM {table} LIMIT 1")


def test_reader_cannot_write_even_in_a_read_write_transaction():
    with connect("research_reader", "integration_tests") as conn:
        conn.read_only = False
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("UPDATE chunks SET content = 'x' WHERE false")
        conn.rollback()
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("CREATE TABLE asd_rag.probe_reader (i int)")


def test_app_role_still_cannot_see_research_data():
    with connect("app", "integration_tests") as conn, pytest.raises(psycopg.errors.InsufficientPrivilege):
        conn.execute(f"SELECT 1 FROM {VIEW} LIMIT 1")
