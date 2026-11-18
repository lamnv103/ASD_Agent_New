"""Read-only checks against the running asd_rag_v2 database. Run with:  pytest -m integration

Nothing is written; every query runs as the role a real component would use.
"""

import json

import pytest

from app.config import CORPUS_MANIFEST, ROOT
from app.db import connect
from app.ingest.chunking import ChunkingProfile, DocumentInfo, HFTokenCounter, chunk_document

pytestmark = pytest.mark.integration
QUARANTINED = {"ASD-CSV-077", "NIH-NIMH-CHILDREN"}
PDF_SOURCES = {"NIHR-SENITA-2022", "WHO-CST-INTRO-2022", "WHO-CST-PARTICIPANTS-2022", "WHO-ECD-GUIDELINE-2020"}
UNVERIFIED = ("table_structure_lost", "table_structure_unrecoverable", "table_recovered_pending_review",
              "page_provenance_incomplete", "text_encoding_lost")


@pytest.fixture(scope="module")
def owner():
    with connect("owner", "integration_tests") as conn:
        yield conn
        conn.rollback()


def test_nothing_passes_the_gates_without_owner_decisions(owner):
    assert owner.execute("SELECT count(*) FROM v_embedding_eligible_documents").fetchone()[0] == 0
    assert owner.execute("SELECT count(*) FROM v_retrieval_ready_chunks").fetchone()[0] == 0
    flags = owner.execute("""SELECT count(*) FROM source_rights WHERE coalesce(archive_allowed, text_mining_allowed,
        chunking_allowed, embedding_allowed, cohere_processing_allowed, external_llm_processing_allowed,
        commercial_use_allowed, attribution_required, share_alike_required) IS NOT NULL
        OR verified_by IS NOT NULL OR verified_at IS NOT NULL""").fetchone()[0]
    assert flags == 0


def test_quarantined_documents_stay_quarantined_and_unchunked(owner):
    rows = dict(owner.execute("SELECT source_id, content_review_status FROM documents WHERE is_current "
                              "AND source_id = ANY(%s)", (list(QUARANTINED),)).fetchall())
    assert rows == dict.fromkeys(QUARANTINED, "quarantined")
    assert owner.execute("""SELECT count(*) FROM chunks c JOIN documents d USING (document_id)
                            WHERE d.source_id = ANY(%s)""", (list(QUARANTINED),)).fetchone()[0] == 0


def test_unverified_structure_is_never_retrievable_and_the_table_enforces_it(owner):
    assert owner.execute("SELECT count(*) FROM chunks WHERE retrieval_eligible AND completeness_status = ANY(%s)",
                         (list(UNVERIFIED),)).fetchone()[0] == 0
    constraints = {r[0] for r in owner.execute(
        "SELECT conname FROM pg_constraint WHERE conrelid = 'asd_rag.chunks'::regclass")}
    assert "chunks_unverified_structure_not_retrievable" in constraints


def test_pdf_chunks_of_section_v2_1_have_page_provenance(owner):
    missing = owner.execute("""SELECT count(*) FROM v_chunk_provenance WHERE chunking_profile = 'section_v2_1'
                               AND source_id = ANY(%s) AND page_start IS NULL""", (list(PDF_SOURCES),)).fetchone()[0]
    total = owner.execute("""SELECT count(*) FROM v_chunk_provenance WHERE chunking_profile = 'section_v2_1'
                             AND source_id = ANY(%s)""", (list(PDF_SOURCES),)).fetchone()[0]
    assert total > 0 and missing == 0


def test_licence_classification_matches_the_curation(owner):
    curated = [json.loads(x) for x in (ROOT / "data" / "curation" / "license_corrections.jsonl")
               .read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = dict(owner.execute("SELECT source_id, rights_status || '|' || coalesce(license_type, '') FROM source_rights")
                .fetchall())
    assert len(curated) == 35
    assert all(rows[c["source_id"]] == f"verified_cc_by|{c['license_type']}" for c in curated)
    corpus = {json.loads(x)["source_id"] for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()}
    nc = [s for s in corpus if rows[s].startswith("verified_noncommercial_research")]
    assert len(nc) == 13


def test_stored_section_v2_1_chunks_reproduce_from_the_corpus(owner):
    sid = "WHO-ECD-GUIDELINE-2020"
    doc_id, rel, title, role, stype, gaps = owner.execute(
        """SELECT d.document_id, d.corpus_relative_path, s.title, s.corpus_role, s.source_type, d.missing_components
           FROM documents d JOIN sources s USING (source_id) WHERE d.is_current AND d.source_id = %s""",
        (sid,)).fetchone()
    stored = [r[0] for r in owner.execute("""SELECT content_sha256 FROM chunks WHERE document_id = %s
        AND chunking_profile = 'section_v2_1' ORDER BY chunk_index""", (doc_id,))]
    profile = ChunkingProfile.load("section_v2_1")
    counter = HFTokenCounter(profile.tokenizer_path, profile.tokenizer_sha256)
    info = DocumentInfo(sid, doc_id, title, role, stype, "en", gaps or {})
    fresh = chunk_document((ROOT / rel).read_text(encoding="utf-8-sig"), info, profile, counter).chunks
    assert stored == [c.content_sha256 for c in fresh]


def test_app_role_cannot_read_unvetted_chunks_or_rights_evidence():
    import psycopg

    with connect("app", "integration_tests") as app:
        for table in ("chunks", "rights_assessments", "v_chunk_provenance"):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                app.execute(f"SELECT 1 FROM {table} LIMIT 1")
            app.rollback()
