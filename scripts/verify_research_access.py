# ruff: noqa: E501  -- long SQL literals are kept whole so each security check reads as one auditable statement
"""Independent security verification of the research retrieval access (Phase 6.2 T2.2).

  python -B scripts/verify_research_access.py                       # live-safe: reads + rolled-back probes only
  python -B scripts/verify_research_access.py --mutations           # ALSO negative tests that mutate data inside
                                                                    # rolled-back transactions; refuses on port 5433
  python -B scripts/verify_research_access.py --fingerprint-only    # print the integrity fingerprint and exit

A. permissions — connects AS asd_rag_v2_research_reader (READ WRITE transactions, always rolled back)
B. authorization — what the view returns vs the active allowlist; D-1 exclusions; filter-before-LIMIT proof
C. privilege leaks — catalog: memberships, attributes, schema/table/column/sequence/function/database privileges,
   SECURITY DEFINER functions, default ACLs, view dependencies
D. negative cases by mutation (isolated database only)
E. integrity fingerprint — counts, content/vector hashes, schema, views, per-role ACLs
Never prints passwords or connection strings.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg

from app.config import REPORTS, db_settings
from app.db import connect

READER = "asd_rag_v2_research_reader"
VIEW = "v_research_retrieval_chunks"
D1_MANIFEST = REPORTS / "research_authorization_d1_exclusions_2026-11-14.csv"
LIVE_PORT = 5433
results: list[dict] = []


def check(group: str, name: str, ok: bool, detail: object = "") -> None:
    results.append({"group": group, "check": name, "pass": bool(ok), "detail": detail})


# ------------------------------------------------------------------------------------------------- A
def reader_try(statement: str, params: tuple = ()) -> tuple[str, str]:
    with connect("research_reader", "verify_research_access") as conn:
        conn.read_only = False  # observe privilege checks, not the read-only default
        try:
            conn.execute(statement, params or None)
            return "allowed", ""
        except psycopg.errors.InsufficientPrivilege as exc:
            return "denied", exc.diag.message_primary or ""
        except psycopg.Error as exc:
            return f"error:{type(exc).__name__}", exc.diag.message_primary or ""
        finally:
            conn.rollback()


def permissions() -> None:
    allowed = ["SELECT chunk_id, embedding, content, content_tsv FROM v_research_retrieval_chunks LIMIT 3"]
    denied = [
        "SELECT 1 FROM chunks LIMIT 1", "SELECT 1 FROM research_chunk_embeddings LIMIT 1",
        "SELECT 1 FROM research_embedding_authorizations LIMIT 1", "SELECT 1 FROM research_embedding_authorization_chunks",
        "SELECT 1 FROM v_research_embedding_candidates LIMIT 1", "SELECT 1 FROM chunk_embeddings LIMIT 1",
        "SELECT 1 FROM documents LIMIT 1", "SELECT 1 FROM sources LIMIT 1", "SELECT 1 FROM source_rights LIMIT 1",
        "SELECT 1 FROM rights_assessments LIMIT 1", "SELECT 1 FROM v_retrieval_ready_chunks LIMIT 1",
        "SELECT 1 FROM v_embedding_eligible_documents LIMIT 1", "SELECT 1 FROM v_chunk_provenance LIMIT 1",
        "SELECT 1 FROM retrieval_logs LIMIT 1", "SELECT 1 FROM schema_migrations LIMIT 1",
        "INSERT INTO retrieval_logs (query_hash, retrieval_method) VALUES (repeat('0', 64), 'probe')",
        "UPDATE chunks SET content = 'x' WHERE false", "DELETE FROM research_chunk_embeddings WHERE false",
        "UPDATE research_embedding_authorizations SET revoked_at = NULL WHERE false",
        "INSERT INTO research_embedding_authorization_chunks SELECT * FROM research_embedding_authorization_chunks WHERE false",
        "TRUNCATE chunks", "TRUNCATE research_chunk_embeddings",
        "CREATE TABLE asd_rag.probe_reader (i int)", "CREATE TABLE public.probe_reader (i int)",
        "CREATE TEMP TABLE probe_reader (i int)", "CREATE VIEW asd_rag.probe_reader AS SELECT 1",
        "CREATE FUNCTION asd_rag.probe_reader() RETURNS int LANGUAGE sql AS 'SELECT 1'",
        "ALTER VIEW v_research_retrieval_chunks RENAME TO probe_reader", "DROP VIEW v_research_retrieval_chunks",
        "ALTER TABLE chunks ADD COLUMN probe int", "DROP TABLE chunks",
        "SET ROLE asd_rag_v2_ingest", "SET ROLE asd_rag_v2_owner", "SET ROLE asd_rag_v2_app",
        "SELECT pg_read_file('postgresql.conf')", "COPY (SELECT 1) TO PROGRAM 'true'",
        "SELECT lo_import('/etc/hostname')", "CREATE SCHEMA probe_reader",
    ]
    for st in allowed:
        outcome, msg = reader_try(st)
        check("A_permissions", f"allow: {st[:70]}", outcome == "allowed", outcome)
    for st in denied:
        outcome, msg = reader_try(st)
        check("A_permissions", f"deny: {st[:70]}", outcome == "denied", f"{outcome} {msg}"[:160])
    # writing THROUGH the view: refused twice — no privilege (catalog, group C) and the join view is not updatable
    for st in ("UPDATE v_research_retrieval_chunks SET content = 'x' WHERE false",
               "DELETE FROM v_research_retrieval_chunks WHERE false",
               "INSERT INTO v_research_retrieval_chunks (chunk_id) VALUES ('x')"):
        outcome, msg = reader_try(st)
        check("A_permissions", f"refused (non-updatable view): {st[:55]}", outcome != "allowed", f"{outcome} {msg}"[:160])
    # GRANT without grant option is a no-op in PostgreSQL (WARNING, no error): prove the ACL does not change
    with connect("research_reader", "verify_research_access") as conn:
        conn.read_only = False
        notes: list[str] = []
        conn.add_notice_handler(lambda d: notes.append(d.message_primary or ""))
        acl_sql = "SELECT relacl::text FROM pg_class WHERE oid = 'asd_rag.v_research_retrieval_chunks'::regclass"
        before = conn.execute(acl_sql).fetchone()[0]
        try:
            conn.execute("GRANT SELECT ON v_research_retrieval_chunks TO PUBLIC")
            after = conn.execute(acl_sql).fetchone()[0]
        except psycopg.Error as exc:
            after = f"error:{type(exc).__name__}"
        conn.rollback()
    check("A_permissions", "GRANT … TO PUBLIC by the reader changes nothing", before == after or after.startswith("error"),
          {"warning": notes[:1], "acl_unchanged": before == after})
    # the read-only default is real (but is defence in depth, not the access control)
    with connect("research_reader", "verify_research_access") as conn:
        setting = conn.execute("SHOW default_transaction_read_only").fetchone()[0]
        who = conn.execute("SELECT current_user, session_user").fetchone()
        conn.rollback()
    check("A_permissions", "session runs as the reader itself", who == (READER, READER), list(who))
    check("A_permissions", "default_transaction_read_only = on", setting == "on", setting)


# ------------------------------------------------------------------------------------------------- B
def authorization(owner: psycopg.Connection) -> None:
    active = owner.execute("SELECT authorization_id, profile_code FROM research_embedding_authorizations "
                           "WHERE revoked_at IS NULL").fetchall()
    check("B_authorization", "exactly one active authorization", len(active) == 1, active)
    allow = {r[0] for r in owner.execute("""SELECT k.chunk_id FROM research_embedding_authorization_chunks k
                                             JOIN research_embedding_authorizations a USING (authorization_id)
                                             WHERE a.revoked_at IS NULL""")}
    with open(D1_MANIFEST, encoding="utf-8-sig") as f:
        d1 = [r["chunk_id"] for r in csv.DictReader(f)]
    with connect("research_reader", "verify_research_access") as rc:
        rows = rc.execute(f"SELECT chunk_id, profile_code, model_id, vector_dimension, vector_dims(embedding), "
                          f"completeness_status, authorization_id FROM {VIEW}").fetchall()
        visible = {r[0] for r in rows}
        check("B_authorization", "view rows == active allowlist (with vectors)", visible == allow,
              {"view": len(visible), "allowlist": len(allow), "extra": len(visible - allow), "missing": len(allow - visible)})
        check("B_authorization", "one row per chunk", len(rows) == len(visible), len(rows))
        check("B_authorization", "D-1 chunks absent (47)", not (set(d1) & visible), {"d1": len(d1), "visible": len(set(d1) & visible)})
        check("B_authorization", "only active authorization id", {r[6] for r in rows} == {a[0] for a in active},
              sorted({r[6] for r in rows}))
        check("B_authorization", "profile/model/dimension correct",
              all(r[1] == "cohere_embed_v4_1536_v1" and r[2] == "embed-v4.0" and r[3] == 1536 and r[4] == 1536 for r in rows))
        check("B_authorization", "verified completeness only",
              all(r[5] in ("complete", "document_has_gaps", "references_missing_component") for r in rows))
        # filter before LIMIT: query with the vector of an EXCLUDED chunk; its near-duplicate neighbours are other
        # reference-list chunks. Unfiltered top-10 (owner, base table) contains excluded chunks; the view's does not.
        qvec = owner.execute("SELECT embedding::text FROM research_chunk_embeddings WHERE chunk_id = %s", (d1[0],)).fetchone()[0]
        raw = [r[0] for r in owner.execute("SELECT chunk_id FROM research_chunk_embeddings ORDER BY embedding <=> %s::vector "
                                           "LIMIT 10", (qvec,))]
        top = [r[0] for r in rc.execute(f"SELECT chunk_id FROM {VIEW} ORDER BY embedding <=> %s::vector LIMIT 10", (qvec,))]
        check("B_authorization", "unfiltered top-10 contains excluded chunks (control)", len(set(raw) & set(d1)) >= 5,
              len(set(raw) & set(d1)))
        check("B_authorization", "view top-10: 10 rows, none excluded (filter before LIMIT)",
              len(top) == 10 and not (set(top) & set(d1)) and set(top) <= allow, {"rows": len(top)})
        # quarantined / non-current documents never appear
        qdocs = {r[0] for r in owner.execute("SELECT document_id FROM documents WHERE content_review_status = 'quarantined' "
                                             "OR NOT is_current")}
        vdocs = {r[0] for r in rc.execute(f"SELECT DISTINCT document_id FROM {VIEW}")}
        check("B_authorization", "no quarantined or non-current document", not (qdocs & vdocs), len(qdocs))
        rc.rollback()
    # the filters are part of the view definition (SQL layer), and the plan applies them below the Limit
    viewdef = owner.execute(f"SELECT pg_get_viewdef('asd_rag.{VIEW}'::regclass, true)").fetchone()[0]
    needed = ["revoked_at IS NULL", "content_sha256", "chunking_profile", "is_current", "content_review_status",
              "retrieval_eligible", "completeness_status", "vector_dims", "model_id", "profile_id"]
    check("B_authorization", "all C5 predicates in view definition", all(n in viewdef for n in needed),
          [n for n in needed if n not in viewdef])
    opts = owner.execute("SELECT reloptions FROM pg_class WHERE oid = %s::regclass", (f"asd_rag.{VIEW}",)).fetchone()[0]
    check("B_authorization", "security_barrier view", opts == ["security_barrier=true"], opts)
    plan = "\n".join(r[0] for r in owner.execute(
        f"EXPLAIN SELECT chunk_id FROM {VIEW} ORDER BY embedding <=> %s::vector LIMIT 10", (qvec,)))
    lim = plan.find("Limit")
    below = plan[lim:] if lim != -1 else ""
    partial_current = owner.execute("SELECT indexdef FROM pg_indexes WHERE indexname = 'documents_one_current_per_source'"
                                    ).fetchone()
    current_ok = "is_current" in below or (
        "documents_one_current_per_source" in below and partial_current and "WHERE is_current" in partial_current[0])
    check("B_authorization", "plan: all filters evaluated under the Limit node (top node = Limit)",
          plan.lstrip().startswith("Limit") and all(f in below for f in ("revoked_at IS NULL", "content_review_status",
                                                                          "retrieval_eligible", "completeness_status",
                                                                          "vector_dims", "corpus_role")) and current_ok,
          {"is_current_via": "filter" if "is_current" in below else "partial index documents_one_current_per_source"})


# ------------------------------------------------------------------------------------------------- C
def leaks(owner: psycopg.Connection) -> None:
    q = lambda s, *p: owner.execute(s, p or None).fetchall()  # noqa: E731
    attrs = q("SELECT rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin, rolreplication, rolbypassrls, "
              "rolconnlimit FROM pg_roles WHERE rolname = %s", READER)[0]
    check("C_leaks", "role attributes least-privilege",
          attrs == (False, False, False, False, True, False, False, 5), list(attrs))
    mem = q("SELECT r.rolname, m.rolname FROM pg_auth_members a JOIN pg_roles r ON r.oid = a.member "
            "JOIN pg_roles m ON m.oid = a.roleid WHERE r.rolname = %s OR m.rolname = %s", READER, READER)
    check("C_leaks", "no role membership (either direction)", not mem, mem)
    rels = q("""SELECT n.nspname || '.' || c.relname, c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg_toast%%'
                  AND c.relkind IN ('r', 'v', 'm', 'p', 'f')
                  AND has_table_privilege(%s, c.oid, 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')""",
             READER)
    check("C_leaks", "table privileges: only the retrieval view", rels == [(f"asd_rag.{VIEW}", "v")], rels)
    write_on_view = q("SELECT has_table_privilege(%s, %s, 'INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')",
                      READER, f"asd_rag.{VIEW}")[0][0]
    check("C_leaks", "no write privilege on the view", not write_on_view)
    cols = q("""SELECT table_schema, table_name, column_name, privilege_type FROM information_schema.column_privileges
                WHERE grantee = %s AND table_name <> %s""", READER, VIEW)
    check("C_leaks", "no column-level grants elsewhere", not cols, cols)
    seqs = q("""SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind = 'S'
                AND n.nspname NOT IN ('pg_catalog', 'information_schema')
                AND CASE WHEN c.relkind = 'S' THEN has_sequence_privilege(%s, c.oid, 'USAGE, SELECT, UPDATE') ELSE false END""", READER)
    check("C_leaks", "no sequence privileges", not seqs, seqs)
    schemas = q("""SELECT nspname, has_schema_privilege(%s, oid, 'USAGE'), has_schema_privilege(%s, oid, 'CREATE')
                   FROM pg_namespace WHERE nspname NOT IN ('pg_catalog', 'information_schema') AND nspname NOT LIKE 'pg_%%'""",
                READER, READER)
    check("C_leaks", "schema: USAGE on asd_rag + public only, CREATE nowhere",
          sorted(s for s, u, c in schemas if u) == ["asd_rag", "public"] and not any(c for _, _, c in schemas), schemas)
    db = q("SELECT has_database_privilege(%s, current_database(), 'CONNECT'), "
           "has_database_privilege(%s, current_database(), 'CREATE'), has_database_privilege(%s, current_database(), 'TEMP')",
           READER, READER, READER)[0]
    check("C_leaks", "database: CONNECT only (no CREATE, no TEMP)", db == (True, False, False), list(db))
    secdef = q("""SELECT n.nspname || '.' || p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
                  WHERE p.prosecdef AND n.nspname NOT IN ('pg_catalog', 'information_schema')""")
    check("C_leaks", "no SECURITY DEFINER function outside pg_catalog", not secdef, secdef)
    fn = q("""SELECT p.proname FROM pg_proc p WHERE p.pronamespace = 'asd_rag'::regnamespace
              AND has_function_privilege(%s, p.oid, 'EXECUTE')""", READER)
    check("C_leaks", "executable asd_rag functions = trigger function only (PUBLIC default, not callable)",
          [f[0] for f in fn] in ([], ["research_embedding_guard"]), fn)
    defacl = q("SELECT defaclrole::regrole::text, defaclobjtype, defaclacl::text FROM pg_default_acl")
    check("C_leaks", "no default privileges", not defacl, defacl)
    deps = sorted({r[0] for r in q("""SELECT DISTINCT t.relname FROM pg_depend d JOIN pg_rewrite rw ON rw.oid = d.objid
                                       JOIN pg_class t ON t.oid = d.refobjid WHERE rw.ev_class = %s::regclass
                                       AND t.oid <> rw.ev_class""", f"asd_rag.{VIEW}")})
    expected = ["chunks", "documents", "embedding_profiles", "research_chunk_embeddings",
                "research_embedding_authorization_chunks", "research_embedding_authorization_sources",
                "research_embedding_authorizations", "sources"]
    check("C_leaks", "view depends only on research + corpus tables (no production/rights objects)",
          deps == expected, deps)
    prod_dep = q("""SELECT DISTINCT v.relname FROM pg_depend d JOIN pg_rewrite rw ON rw.oid = d.objid
                    JOIN pg_class v ON v.oid = rw.ev_class JOIN pg_class t ON t.oid = d.refobjid
                    WHERE t.relname IN ('research_chunk_embeddings', %s) AND v.relname IN
                    ('v_retrieval_ready_chunks', 'v_embedding_eligible_documents', 'v_chunk_provenance')""", VIEW)
    check("C_leaks", "production views do not reference research objects", not prod_dep, prod_dep)
    for role in ("asd_rag_v2_app", "asd_rag_v2_ingest"):
        r = q("SELECT has_table_privilege(%s, %s, 'SELECT')", role, f"asd_rag.{VIEW}")[0][0]
        check("C_leaks", f"{role} cannot read the retrieval view", not r)
    settings = q("SELECT setconfig FROM pg_db_role_setting WHERE setrole = %s::regrole", READER)
    check("C_leaks", "role settings recorded", bool(settings), settings)


# ------------------------------------------------------------------------------------------------- D
def mutations() -> None:
    port = db_settings("owner").port
    if port == LIVE_PORT:
        raise SystemExit("--mutations refuses to run against the live database port")
    with connect("owner", "verify_research_access_mutations") as conn:
        base = conn.execute(f"SELECT count(*) FROM {VIEW}").fetchone()[0]
        conn.rollback()
        sample = conn.execute(f"SELECT chunk_id, document_id, source_id FROM {VIEW} ORDER BY chunk_id LIMIT 1").fetchone()
        conn.rollback()
        cid, did, sid = sample
        other_src = conn.execute("SELECT source_id FROM sources WHERE corpus_role = 'metadata_only' LIMIT 1").fetchone()[0]
        conn.rollback()

        def case(name: str, statements: list[tuple[str, tuple]], expect_absent: bool = True, expect_total: int | None = None):
            try:
                for st, params in statements:
                    conn.execute(st, params or None)
                total = conn.execute(f"SELECT count(*) FROM {VIEW}").fetchone()[0]
                present = conn.execute(f"SELECT count(*) FROM {VIEW} WHERE chunk_id = %s", (cid,)).fetchone()[0]
                ok = (present == 0) if expect_absent else (present == 1)
                if expect_total is not None:
                    ok = ok and total == expect_total
                check("D_negative_cases", name, ok, {"present": present, "total": total, "baseline": base})
            except psycopg.Error as exc:
                check("D_negative_cases", name, False, f"{type(exc).__name__}: {exc.diag.message_primary}")
            finally:
                conn.rollback()

        off = ("ALTER TABLE research_chunk_embeddings DISABLE TRIGGER research_chunk_embeddings_guard", ())
        case("positive control: allowed chunk present", [], expect_absent=False, expect_total=base)
        case("authorization revoked → nothing visible",
             [("UPDATE research_embedding_authorizations SET revoked_at = now() WHERE revoked_at IS NULL", ())],
             expect_total=0)
        case("chunk removed from allowlist (exclusion) → absent",
             [("DELETE FROM research_embedding_authorization_chunks k USING research_embedding_authorizations a "
               "WHERE a.authorization_id = k.authorization_id AND a.revoked_at IS NULL AND k.chunk_id = %s", (cid,))],
             expect_total=base - 1)
        case("allowlist hash ≠ chunk hash → absent",
             [("UPDATE research_embedding_authorization_chunks SET content_sha256 = repeat('0', 64) WHERE chunk_id = %s",
               (cid,))])
        case("document quarantined → absent",
             [("UPDATE documents SET content_review_status = 'quarantined', content_warning = 'probe' "
               "WHERE document_id = %s", (did,))])
        case("document not current → absent", [("UPDATE documents SET is_current = false WHERE document_id = %s", (did,))])
        case("chunk not retrieval-eligible → absent",
             [("UPDATE chunks SET retrieval_eligible = false WHERE chunk_id = %s", (cid,))])
        case("unverified structure status → absent",
             [("UPDATE chunks SET retrieval_eligible = false, completeness_status = 'text_encoding_lost' "
               "WHERE chunk_id = %s", (cid,))])
        case("wrong corpus version (authorization chunking_profile) → nothing visible",
             [("UPDATE research_embedding_authorizations SET chunking_profile = 'section_v2' WHERE revoked_at IS NULL", ())],
             expect_total=0)
        case("vector embeds other content (vector hash ≠ chunk hash) → absent",
             [off, ("UPDATE research_chunk_embeddings SET content_sha256 = repeat('0', 64) WHERE chunk_id = %s", (cid,))])
        case("wrong model id on vector → absent",
             [off, ("UPDATE research_chunk_embeddings SET model_id = 'embed-english-v3.0' WHERE chunk_id = %s", (cid,))])
        case("vector under another embedding profile → absent",
             [off, ("INSERT INTO embedding_profiles (profile_code, provider, model_id, vector_dimension, document_input_type, "
                    "query_input_type, similarity_metric, api_version) VALUES ('probe_profile', 'cohere', 'embed-v4.0', 1536, "
                    "'search_document', 'search_query', 'cosine', 'v2')", ()),
              ("UPDATE research_chunk_embeddings SET profile_id = (SELECT profile_id FROM embedding_profiles "
               "WHERE profile_code = 'probe_profile') WHERE chunk_id = %s", (cid,))])
        case("provenance broken (document moved to another source) → absent",
             [("UPDATE documents SET source_id = %s WHERE document_id = %s", (other_src, did))])
        case("source not core/gaps → absent",
             [("UPDATE sources SET corpus_role = 'metadata_only' WHERE source_id = %s", (sid,))])
        case("research row of a non-allowlisted chunk with a vector stays invisible",
             [("DELETE FROM research_embedding_authorization_chunks WHERE chunk_id = %s", (cid,))])
        case("second active authorization for the profile is rejected (unique index)",
             [("INSERT INTO research_embedding_authorizations (scope, authorized_by, recorded_by, basis, profile_code, "
               "chunking_profile, manifest_sha256) VALUES ('research_test', 'p', 'p', 'p', 'cohere_embed_v4_1536_v1', "
               "'section_v2_1', repeat('0', 64))", ())], expect_absent=False)
        # the last case must FAIL with a unique violation: flip its meaning
        last = results[-1]
        last["pass"] = "UniqueViolation" in str(last["detail"])


# ------------------------------------------------------------------------------------------------- E
def fingerprint(owner: psycopg.Connection) -> dict:
    one = lambda s: owner.execute(s).fetchone()[0]  # noqa: E731

    def acl_of(role: str) -> str:
        rows = owner.execute("""
            SELECT 'rel:' || n.nspname || '.' || c.relname || ':' || a.privilege_type
            FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace, aclexplode(c.relacl) a
            WHERE a.grantee = (SELECT oid FROM pg_roles WHERE rolname = %(r)s) AND n.nspname NOT LIKE 'pg_%%'
            UNION ALL
            SELECT 'col:' || c.relname || '.' || at.attname || ':' || a.privilege_type
            FROM pg_attribute at JOIN pg_class c ON c.oid = at.attrelid, aclexplode(at.attacl) a
            WHERE a.grantee = (SELECT oid FROM pg_roles WHERE rolname = %(r)s)
            UNION ALL
            SELECT 'nsp:' || n.nspname || ':' || a.privilege_type FROM pg_namespace n, aclexplode(n.nspacl) a
            WHERE a.grantee = (SELECT oid FROM pg_roles WHERE rolname = %(r)s)
            UNION ALL
            SELECT 'db:' || d.datname || ':' || a.privilege_type FROM pg_database d, aclexplode(d.datacl) a
            WHERE a.grantee = (SELECT oid FROM pg_roles WHERE rolname = %(r)s)
            UNION ALL
            SELECT 'fn:' || p.proname || ':' || a.privilege_type FROM pg_proc p, aclexplode(p.proacl) a
            WHERE a.grantee = (SELECT oid FROM pg_roles WHERE rolname = %(r)s)
            ORDER BY 1""", {"r": role}).fetchall()
        return hashlib.md5("|".join(r[0] for r in rows).encode()).hexdigest()

    prod_views = "('v_retrieval_ready_chunks', 'v_embedding_eligible_documents', 'v_chunk_provenance')"
    return {
        "chunks": one("SELECT count(*) FROM chunks"),
        "research_vectors": one("SELECT count(*) FROM research_chunk_embeddings"),
        "production_vectors": one("SELECT count(*) FROM chunk_embeddings"),
        "chunks_md5": one("SELECT md5(string_agg(chunk_id || content_sha256 || retrieval_eligible::text || "
                          "completeness_status, ',' ORDER BY chunk_id)) FROM chunks"),
        "vectors_md5": one("SELECT md5(string_agg(chunk_id || embedding_input_hash || vector_norm::text || embedding::text "
                           "|| authorization_id::text, ',' ORDER BY chunk_id)) FROM research_chunk_embeddings"),
        "columns_md5": one("""SELECT md5(string_agg(table_name || '.' || column_name || ':' || data_type, ','
                              ORDER BY table_name, column_name)) FROM information_schema.columns
                              WHERE table_schema = 'asd_rag' AND table_name <> 'v_research_retrieval_chunks'"""),
        "production_views_md5": one(f"""SELECT md5(string_agg(relname || pg_get_viewdef(oid), ',' ORDER BY relname))
                                       FROM pg_class WHERE relnamespace = 'asd_rag'::regnamespace AND relname IN {prod_views}"""),
        "research_006_view_md5": one("SELECT md5(pg_get_viewdef('asd_rag.v_research_embedding_candidates'::regclass))"),
        "approvals_and_rights_flags": one("""SELECT (SELECT count(*) FROM documents WHERE approved_for_embedding OR
              approved_for_retrieval) + (SELECT count(*) FROM source_rights WHERE coalesce(archive_allowed, text_mining_allowed,
              chunking_allowed, embedding_allowed, cohere_processing_allowed, external_llm_processing_allowed) IS NOT NULL)"""),
        "acl_app": acl_of("asd_rag_v2_app"), "acl_ingest": acl_of("asd_rag_v2_ingest"),
        "acl_owner": acl_of("asd_rag_v2_owner"),
        "acl_public_relations": one("""SELECT md5(coalesce(string_agg(c.relname || ':' || a.privilege_type, ',' ORDER BY 1), ''))
              FROM pg_class c, aclexplode(c.relacl) a WHERE a.grantee = 0 AND c.relnamespace = 'asd_rag'::regnamespace"""),
        "roles": one("SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname LIKE 'asd_rag%%'"),
        "authorizations": owner.execute("SELECT authorization_id, revoked_at IS NULL, manifest_sha256 FROM "
                                        "research_embedding_authorizations ORDER BY 1").fetchall(),
        "migrations": [r[0] for r in owner.execute("SELECT version FROM schema_migrations ORDER BY 1")],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--fingerprint-only", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    with connect("owner", "verify_research_access") as owner:
        owner.read_only = True
        fp = fingerprint(owner)
        if args.fingerprint_only:
            print(json.dumps(fp, indent=1, default=str))
            return 0
        permissions()
        authorization(owner)
        leaks(owner)
    if args.mutations:
        mutations()
    summary = {"port_is_live": db_settings("owner").port == LIVE_PORT, "checks": len(results),
               "passed": sum(r["pass"] for r in results), "failed": [r for r in results if not r["pass"]],
               "by_group": {g: f"{sum(r['pass'] for r in results if r['group'] == g)}/"
                               f"{sum(1 for r in results if r['group'] == g)}" for g in dict.fromkeys(r["group"] for r in results)},
               "fingerprint": fp, "results": results}
    text = json.dumps(summary, ensure_ascii=False, indent=1, default=str)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("port_is_live", "checks", "passed", "failed", "by_group")},
                     ensure_ascii=False, indent=1, default=str))
    return 0 if not summary["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
