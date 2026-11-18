# ruff: noqa: E501
"""FTS retriever against the live database (research reader role, read-only). Run: pytest -m integration."""

import csv
import io

import psycopg
import pytest

from app.config import ROOT
from app.db import connect
from app.retrieval.fts import FtsProfile, FtsRetriever, Glossary

pytestmark = pytest.mark.integration
GLOSSARY = Glossary(ROOT / "config" / "query_glossary_vi_en_v1.json")
EXCLUDED = {r["chunk_id"] for r in csv.DictReader(io.StringIO(
    (ROOT / "eval" / "reports" / "research_authorization_d1_exclusions_2026-11-14.csv").read_text(encoding="utf-8-sig")))}


@pytest.fixture(scope="module")
def view_ids():
    with connect("research_reader", "test_fts") as c:
        ids = {r[0] for r in c.execute("SELECT chunk_id FROM asd_rag.v_research_retrieval_chunks")}
        c.rollback()
    return ids


def retr(code):
    return FtsRetriever(FtsProfile.load(code), glossary=GLOSSARY)


def test_injection_text_is_harmless_and_returns_normally():
    r = retr("fts_b_glossary_and_v1").retrieve("x'); DROP TABLE asd_rag.chunks; -- & !a | b:*", k=5)
    assert r.status in ("ok", "no_results")
    with connect("research_reader", "test_fts") as c:  # the view still answers
        assert c.execute("SELECT count(*) FROM asd_rag.v_research_retrieval_chunks").fetchone()[0] > 0
        c.rollback()


@pytest.mark.parametrize("q", ["Journal of Autism and Developmental Disorders doi", "systematic review autism",
                               "Trẻ tự kỷ có hay bị động kinh không?"])
def test_results_stay_inside_the_authorized_view(q, view_ids):
    for code in ("fts_a_baseline_v1", "fts_b_glossary_and_v1", "fts_c_glossary_or_v1"):
        r = FtsRetriever(FtsProfile.load(code), glossary=GLOSSARY).retrieve(q, k=50)
        ids = {h.chunk_id for h in r.results}
        assert ids <= view_ids and not ids & EXCLUDED
        assert all(h.authorization_version == 2 for h in r.results)


def test_reader_cannot_read_base_tables_or_write():
    with connect("research_reader", "test_fts") as c:
        assert c.execute("SELECT current_user").fetchone()[0] == "asd_rag_v2_research_reader"
        c.rollback()
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            c.execute("SELECT content_tsv FROM asd_rag.chunks LIMIT 1")
        c.rollback()


def test_top_k_order_and_determinism():
    r = retr("fts_c_glossary_or_v1")
    a, b = r.retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=7), r.retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=7)
    assert len(a.results) == 7 and [h.chunk_id for h in a.results] == [h.chunk_id for h in b.results]
    keys = [(-h.score, h.chunk_id) for h in a.results]
    assert keys == sorted(keys)


def test_ranking_matches_an_independent_sql_query():
    r = retr("fts_b_glossary_and_v1").retrieve("Con tôi hay nhại lại lời người khác, đó là gì?", k=20)
    with connect("research_reader", "test_fts") as c:
        rows = c.execute("SELECT chunk_id, ts_rank_cd(content_tsv, %(q)s::tsquery, 0) FROM asd_rag.v_research_retrieval_chunks "
                         "WHERE content_tsv @@ %(q)s::tsquery", {"q": r.tsquery}).fetchall()
        c.rollback()
    assert [h.chunk_id for h in r.results] == [cid for cid, _ in sorted(rows, key=lambda x: (-x[1], x[0]))][:20]


def test_vietnamese_baseline_returns_nothing_but_unaccented_expansion_matches_accented():
    assert retr("fts_a_baseline_v1").retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=5).status == "no_results"
    a = retr("fts_b_glossary_and_v1").retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=10)
    b = retr("fts_b_glossary_and_v1").retrieve("Tre tu ky co hay bi dong kinh khong?", k=10)
    assert [h.chunk_id for h in a.results] == [h.chunk_id for h in b.results] and a.results
