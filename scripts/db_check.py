"""Verify the asd_rag_v2 database: structure, least-privilege grants, and loaded data.

Every permission probe runs inside a transaction that is always rolled back, so the check
never changes data. Exit code 0 only when every check passes.

Usage:
  python -B scripts/db_check.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import CORPUS_MANIFEST, SOURCE_CATALOG
from app.db import connect

EXPECTED_TABLES = {
    "sources", "source_rights", "documents", "chunks", "embedding_profiles", "chunk_embeddings",
    "ingestion_runs", "ingestion_run_documents", "retrieval_logs", "retrieval_results", "answer_runs",
    "schema_migrations",
}
EXPECTED_VIEWS = {"v_embedding_eligible_documents", "v_retrieval_ready_chunks"}
QUARANTINED = {"ASD-CSV-077", "NIH-NIMH-CHILDREN"}

# (role, statement, should_succeed). Statements use WHERE false where possible: privilege errors
# are raised at planning time, so no row needs to match.
PERMISSION_PROBES = [
    ("app", "SELECT 1 FROM v_retrieval_ready_chunks LIMIT 1", True),
    ("app", "SELECT 1 FROM sources LIMIT 1", True),
    ("app", "SELECT 1 FROM chunks LIMIT 1", False),
    ("app", "INSERT INTO retrieval_logs (query_hash, retrieval_method) VALUES (repeat('0', 64), 'probe')", True),
    ("app", "UPDATE retrieval_logs SET top_k = 1 WHERE false", False),
    ("app", "INSERT INTO sources (source_id, title, corpus_role, scope_status, catalog_payload) "
            "VALUES ('probe', 'probe', 'excluded', 'probe', '{}')", False),
    ("app", "UPDATE documents SET approved_for_retrieval = true WHERE false", False),
    ("ingest", "INSERT INTO sources (source_id, title, corpus_role, scope_status, catalog_payload) "
               "VALUES ('probe', 'probe', 'excluded', 'probe', '{}')", True),
    ("ingest", "UPDATE documents SET approved_for_embedding = true WHERE false", False),
    ("ingest", "UPDATE documents SET content_review_status = 'approved' WHERE false", False),
    ("ingest", "UPDATE source_rights SET embedding_allowed = true WHERE false", False),
    ("ingest", "UPDATE source_rights SET cohere_processing_allowed = true WHERE false", False),
    ("ingest", "UPDATE embedding_profiles SET is_active = true WHERE false", False),
    ("ingest", "SELECT 1 FROM schema_migrations", False),
    ("ingest", "DELETE FROM sources WHERE false", False),
    ("owner", "UPDATE documents SET approved_for_embedding = false WHERE false", True),
]
# Objects and probes added by migration 004 (checked only once it is applied).
EXPECTED_TABLES_004 = {"rights_assessments"}
EXPECTED_VIEWS_004 = {"v_chunk_provenance"}
PERMISSION_PROBES_004 = [
    ("ingest", "UPDATE source_rights SET license_type = 'CC BY' WHERE false", True),
    ("ingest", "UPDATE source_rights SET chunking_allowed = true WHERE false", False),
    ("ingest", "UPDATE source_rights SET archive_allowed = true WHERE false", False),
    ("ingest", "UPDATE source_rights SET share_alike_required = true WHERE false", False),
    ("ingest", "INSERT INTO rights_assessments (source_id, action, basis, assessment, assessed_by) "
               "SELECT source_id, 'embedding_allowed', 'source_license', 'unknown', 'probe' "
               "FROM sources LIMIT 1", True),
    ("ingest", "SELECT 1 FROM v_chunk_provenance LIMIT 1", True),
    ("app", "SELECT 1 FROM rights_assessments LIMIT 1", False),
    ("app", "SELECT 1 FROM v_chunk_provenance LIMIT 1", False),
    ("owner", "UPDATE source_rights SET chunking_allowed = NULL WHERE false", True),
]
# Research embedding track (006): separate from production approval; the app role sees none of it.
EXPECTED_TABLES_006 = {"research_embedding_authorizations", "research_embedding_authorization_sources",
                       "research_embedding_authorization_chunks", "research_chunk_embeddings"}
EXPECTED_VIEWS_006 = {"v_research_embedding_candidates"}
PERMISSION_PROBES_006 = [
    ("ingest", "SELECT 1 FROM v_research_embedding_candidates LIMIT 1", True),
    ("ingest", "SELECT 1 FROM research_chunk_embeddings LIMIT 1", True),
    ("ingest", "UPDATE research_chunk_embeddings SET vector_norm = 1 WHERE false", False),
    ("ingest", "DELETE FROM research_chunk_embeddings WHERE false", False),
    ("ingest", "INSERT INTO research_embedding_authorizations (scope, authorized_by, recorded_by, basis, "
               "profile_code, chunking_profile, manifest_sha256) "
               "SELECT 'research_test', 'p', 'p', 'p', 'p', 'p', 'p' WHERE false", False),
    ("ingest", "INSERT INTO research_embedding_authorization_chunks SELECT * FROM "
               "research_embedding_authorization_chunks WHERE false", False),
    ("app", "SELECT 1 FROM research_chunk_embeddings LIMIT 1", False),
    ("app", "SELECT 1 FROM v_research_embedding_candidates LIMIT 1", False),
    ("app", "SELECT 1 FROM research_embedding_authorizations LIMIT 1", False),
]
# Read-only research retrieval role (007): SELECT on v_research_retrieval_chunks and nothing else.
EXPECTED_VIEWS_007 = {"v_research_retrieval_chunks"}
_READER_DENIED_READS = [
    "chunks", "research_chunk_embeddings", "research_embedding_authorizations",
    "research_embedding_authorization_chunks",
    "research_embedding_authorization_sources", "v_research_embedding_candidates", "chunk_embeddings", "documents",
    "sources", "source_rights", "rights_assessments", "embedding_profiles", "v_retrieval_ready_chunks",
    "v_embedding_eligible_documents", "v_chunk_provenance", "retrieval_logs", "ingestion_runs", "schema_migrations"]
PERMISSION_PROBES_007 = [
    ("research_reader", "SELECT chunk_id, embedding, content FROM v_research_retrieval_chunks LIMIT 1", True),
    *[("research_reader", f"SELECT 1 FROM {t} LIMIT 1", False) for t in _READER_DENIED_READS],
    ("research_reader",
     "INSERT INTO retrieval_logs (query_hash, retrieval_method) VALUES (repeat('0', 64), 'probe')", False),
    # writes on base tables (a join view is not updatable, so writing through the view cannot show a
    # privilege error; the view's write privileges are checked in scripts/verify_research_access.py)
    ("research_reader", "UPDATE chunks SET content = 'x' WHERE false", False),
    ("research_reader", "DELETE FROM research_chunk_embeddings WHERE false", False),
    ("research_reader", "UPDATE research_embedding_authorizations SET revoked_at = NULL WHERE false", False),
    ("research_reader", "TRUNCATE chunks", False),
    ("research_reader", "CREATE TABLE asd_rag.probe_reader (i int)", False),
    ("research_reader", "CREATE TABLE public.probe_reader (i int)", False),
    ("research_reader", "CREATE TEMP TABLE probe_reader (i int)", False),
    ("research_reader", "CREATE VIEW asd_rag.probe_reader AS SELECT 1", False),
    ("research_reader", "ALTER VIEW v_research_retrieval_chunks RENAME TO probe_reader", False),
    ("research_reader", "DROP VIEW v_research_retrieval_chunks", False),
    ("app", "SELECT 1 FROM v_research_retrieval_chunks LIMIT 1", False),
    ("ingest", "SELECT 1 FROM v_research_retrieval_chunks LIMIT 1", False),
]


def probe(role: str, statement: str) -> tuple[bool, str]:
    """Run one statement as `role` in a READ WRITE transaction that is always rolled back.

    READ WRITE is explicit so a privilege check is observed even for roles whose default transaction is
    read-only (the research reader): a read-only default is defence in depth, not an access control.
    Only a privilege error counts as "denied"; any other error is reported and fails a deny probe.
    """
    with connect(role, "db_check_probe") as conn:  # type: ignore[arg-type]
        conn.read_only = False
        try:
            conn.execute(statement)
            return True, "ok"
        except psycopg.errors.InsufficientPrivilege as exc:
            return False, f"denied: {exc.diag.message_primary}"
        except psycopg.Error as exc:
            return True, f"NOT a privilege error ({type(exc).__name__}): {exc.diag.message_primary}"
        finally:
            conn.rollback()


def structure(conn: psycopg.Connection) -> dict:
    tables = {r[0] for r in conn.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='asd_rag' AND table_type='BASE TABLE'")}
    views = {r[0] for r in conn.execute(
        "SELECT table_name FROM information_schema.views WHERE table_schema='asd_rag'")}
    indexes = [r[0] for r in conn.execute("SELECT indexname FROM pg_indexes WHERE schemaname='asd_rag' ORDER BY 1")]
    ext = conn.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()
    pg = conn.execute("SHOW server_version").fetchone()[0]
    dim = conn.execute("""SELECT format_type(a.atttypid, a.atttypmod) FROM pg_attribute a
                          WHERE a.attrelid = 'asd_rag.chunk_embeddings'::regclass
                            AND a.attname = 'embedding'""").fetchone()
    migrations = [r[0] for r in conn.execute("SELECT version FROM schema_migrations ORDER BY 1")]
    constraints = {r[0] for r in conn.execute(
        "SELECT conname FROM pg_constraint WHERE conrelid = 'asd_rag.chunks'::regclass AND contype = 'c'")}
    # 005: unverified structure can never be retrievable (enforced in the table, not only in code).
    violations = conn.execute("""SELECT count(*) FROM chunks WHERE retrieval_eligible AND completeness_status IN
        ('table_structure_lost', 'table_structure_unrecoverable', 'table_recovered_pending_review',
         'page_provenance_incomplete', 'text_encoding_lost')""").fetchone()[0]
    expected_tables = EXPECTED_TABLES | (EXPECTED_TABLES_004 if "004" in migrations else set()) | (
        EXPECTED_TABLES_006 if "006" in migrations else set())
    expected_views = EXPECTED_VIEWS | (EXPECTED_VIEWS_004 if "004" in migrations else set()) | (
        EXPECTED_VIEWS_006 if "006" in migrations else set()) | (EXPECTED_VIEWS_007 if "007" in migrations else set())
    research_guard = "006" not in migrations or bool(conn.execute(
        "SELECT 1 FROM pg_trigger WHERE tgname = 'research_chunk_embeddings_guard' AND NOT tgisinternal").fetchone())
    return {
        "research_guard_trigger": research_guard,
        "chunk_guard_constraint": "005" not in migrations
        or "chunks_unverified_structure_not_retrievable" in constraints,
        "retrievable_unverified_chunks": violations,
        "postgres": pg, "pgvector": ext[0] if ext else None, "embedding_column": dim[0] if dim else None,
        "migrations_applied": migrations,
        "missing_tables": sorted(expected_tables - tables),
        "missing_views": sorted(expected_views - views),
        "index_count": len(indexes), "hnsw_or_ivf_indexes": [i for i in indexes if "hnsw" in i or "ivf" in i],
    }


def data(conn: psycopg.Connection) -> dict:
    def q(sql: str) -> list[tuple]:
        return conn.execute(sql).fetchall()

    manifest = {
        (m := json.loads(line))["source_id"]: m
        for line in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()
    }
    catalog = [json.loads(line) for line in SOURCE_CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    db_docs = {sid: sha for sid, sha in q("SELECT source_id, file_sha256 FROM documents WHERE is_current")}
    return {
        "sources": q("SELECT count(*) FROM sources")[0][0],
        "sources_by_role": dict(q("SELECT corpus_role, count(*) FROM sources GROUP BY 1 ORDER BY 1")),
        "expected_by_role": dict(sorted(Counter(s["tier"] for s in catalog).items())),
        "source_rights": q("SELECT count(*) FROM source_rights")[0][0],
        "rights_processing_flags_set": q("""SELECT count(*) FROM source_rights WHERE text_mining_allowed IS NOT NULL
            OR embedding_allowed IS NOT NULL OR cohere_processing_allowed IS NOT NULL
            OR external_llm_processing_allowed IS NOT NULL""")[0][0],
        "documents_current": len(db_docs),
        "document_hash_mismatches": sorted(s for s, m in manifest.items() if db_docs.get(s) != m["sha256"]),
        "documents_not_in_manifest": sorted(set(db_docs) - set(manifest)),
        "quarantined": sorted(
            r[0] for r in q("SELECT source_id FROM documents WHERE content_review_status = 'quarantined'")),
        "approved_for_embedding": q("SELECT count(*) FROM documents WHERE approved_for_embedding")[0][0],
        "approved_for_retrieval": q("SELECT count(*) FROM documents WHERE approved_for_retrieval")[0][0],
        "embedding_eligible_documents": q("SELECT count(*) FROM v_embedding_eligible_documents")[0][0],
        "retrieval_ready_chunks": q("SELECT count(*) FROM v_retrieval_ready_chunks")[0][0],
        "chunks_by_profile": dict(q("SELECT chunking_profile, count(*) FROM chunks GROUP BY 1")),
        "chunk_embeddings": q("SELECT count(*) FROM chunk_embeddings")[0][0],
    } | (research(conn) if q("SELECT to_regclass('asd_rag.research_chunk_embeddings') IS NOT NULL")[0][0] else {})


def research(conn: psycopg.Connection) -> dict:
    """Research vectors (006) and research retrieval (007).

    Creation: every vector was stored under an authorization whose allowlist held that chunk with the same
    content hash (provenance; still true after that authorization is revoked).
    Retrieval: only the single active authorization per profile decides what v_research_retrieval_chunks returns.
    """
    def one(sql: str) -> int:
        return conn.execute(sql).fetchone()[0]

    retrieval = {}
    if one("SELECT to_regclass('asd_rag.v_research_retrieval_chunks') IS NOT NULL"):
        retrieval = {
            "research_retrievable_chunks": one("SELECT count(*) FROM v_research_retrieval_chunks"),
            "research_retrievable_outside_active_allowlist": one("""SELECT count(*) FROM v_research_retrieval_chunks v
                WHERE NOT EXISTS (SELECT 1 FROM research_embedding_authorization_chunks k
                  JOIN research_embedding_authorizations a USING (authorization_id)
                  WHERE a.revoked_at IS NULL AND k.chunk_id = v.chunk_id AND k.content_sha256 = v.content_sha256)"""),
            "research_retrievable_duplicate_chunk": one("""SELECT count(*) FROM (SELECT chunk_id, profile_code
                FROM v_research_retrieval_chunks GROUP BY 1, 2 HAVING count(*) > 1) x"""),
            "research_retrievable_unverified_status": one("""SELECT count(*) FROM v_research_retrieval_chunks
                WHERE completeness_status NOT IN ('complete', 'document_has_gaps', 'references_missing_component')"""),
        }
    return retrieval | {
        "research_active_authorizations": one(
            "SELECT count(*) FROM research_embedding_authorizations WHERE revoked_at IS NULL"),
        "research_profiles_with_multiple_active": one("""SELECT count(*) FROM (SELECT profile_code
            FROM research_embedding_authorizations WHERE revoked_at IS NULL GROUP BY 1 HAVING count(*) > 1) x"""),
        "research_authorizations": one("SELECT count(*) FROM research_embedding_authorizations"),
        "research_authorizations_production": one(
            "SELECT count(*) FROM research_embedding_authorizations WHERE production_approval"),
        "research_vectors": one("SELECT count(*) FROM research_chunk_embeddings"),
        "research_vectors_bad_dimension": one(
            "SELECT count(*) FROM research_chunk_embeddings WHERE vector_dims(embedding) <> 1536"),
        "research_vectors_without_creation_authorization": one("""SELECT count(*) FROM research_chunk_embeddings e
            WHERE NOT EXISTS (SELECT 1 FROM research_embedding_authorization_chunks k
                              WHERE k.authorization_id = e.authorization_id AND k.chunk_id = e.chunk_id
                                AND k.content_sha256 = e.content_sha256)"""),
        "research_vectors_duplicate_chunk": one("""SELECT count(*) FROM (SELECT chunk_id, profile_id
            FROM research_chunk_embeddings GROUP BY 1, 2 HAVING count(*) > 1) x"""),
    }


def main() -> int:
    with connect("owner", "db_check") as conn:
        report = {"structure": structure(conn), "data": data(conn)}
    report["permissions"] = []
    applied = report["structure"]["migrations_applied"]
    probes = PERMISSION_PROBES + (PERMISSION_PROBES_004 if "004" in applied else []) + (
        PERMISSION_PROBES_006 if "006" in applied else []) + (PERMISSION_PROBES_007 if "007" in applied else [])
    for role, stmt, expected in probes:
        ok, detail = probe(role, stmt)
        report["permissions"].append({"role": role, "statement": stmt[:90], "expected": "allow" if expected else "deny",
                                      "pass": ok == expected, "detail": detail})

    s, d = report["structure"], report["data"]
    expected_roles = d["expected_by_role"]
    checks = {
        "tables_and_views_present": not s["missing_tables"] and not s["missing_views"],
        "embedding_dimension_1536": s["embedding_column"] == "vector(1536)",
        "unverified_structure_never_retrievable":
            s["chunk_guard_constraint"] and s["retrievable_unverified_chunks"] == 0,
        "no_ann_index_yet": not s["hnsw_or_ivf_indexes"],
        "permissions_least_privilege": all(p["pass"] for p in report["permissions"]),
    }
    if "research_vectors" in d:
        checks["research_vectors_valid"] = s["research_guard_trigger"] and not any(
            d[k] for k in ("research_authorizations_production", "research_vectors_bad_dimension",
                           "research_vectors_without_creation_authorization", "research_vectors_duplicate_chunk",
                           "research_profiles_with_multiple_active"))
    if "research_retrievable_chunks" in d:
        checks["research_retrieval_view_scoped"] = not any(
            d[k] for k in ("research_retrievable_outside_active_allowlist", "research_retrievable_duplicate_chunk",
                           "research_retrievable_unverified_status"))
    if d["sources"]:
        checks |= {
            "source_count_174": d["sources"] == 174 and d["source_rights"] == 174,
            "role_split_matches_catalog": d["sources_by_role"] == expected_roles,
            "documents_73_hashes_match": d["documents_current"] == 73 and not d["document_hash_mismatches"]
                                         and not d["documents_not_in_manifest"],
            "warning_documents_quarantined": set(d["quarantined"]) == QUARANTINED,
            "no_automatic_approvals": d["approved_for_embedding"] == 0 and d["approved_for_retrieval"] == 0,
            "processing_rights_unset": d["rights_processing_flags_set"] == 0,
        }
    report["checks"] = checks
    report["ok"] = all(checks.values())
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
