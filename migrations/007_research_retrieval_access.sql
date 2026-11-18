-- 007_research_retrieval_access.sql — read-only research retrieval access (Phase 6.2 T2.1, decisions C1 + C5).
--
-- Adds, for the research track only:
--   1. research_authorizations_one_active_per_profile: at most ONE active (not revoked) research authorization
--      per embedding profile, so "the current authorization" is unambiguous (authorization revisions = revoke old,
--      insert new, in one transaction).
--   2. v_research_retrieval_chunks (security_barrier): vectors + chunk text + provenance, with every C5 filter
--      applied inside the view, so no caller can take Top-K before filtering.
--   3. Grants: asd_rag_v2_research_reader gets USAGE on schema asd_rag and SELECT on that one view. Nothing else.
-- Precondition: the role exists (privileged step deploy/db/initdb/10_research_reader.sh — the owner role cannot
-- create roles) and has no privileged attribute, no membership and no privilege in asd_rag yet.
-- Unchanged: every table, every existing view (production gates included), every existing grant; app/ingest
-- privileges; research vectors; chunks. No SECURITY DEFINER function is created.
-- Rollback: migrations/rollback/007_down.sql, then deploy/db/rollback/research_reader_down.sql (superuser).

SET search_path = asd_rag, public;

-- 0. preconditions ---------------------------------------------------------------------------------
DO $$
DECLARE r pg_roles%ROWTYPE;
BEGIN
    SELECT * INTO r FROM pg_roles WHERE rolname = 'asd_rag_v2_research_reader';
    IF NOT FOUND THEN
        RAISE EXCEPTION '007 precondition: role asd_rag_v2_research_reader missing (run deploy/db/initdb/10_research_reader.sh)';
    END IF;
    IF r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolinherit OR r.rolreplication OR r.rolbypassrls THEN
        RAISE EXCEPTION '007 precondition: research reader role has a privileged attribute';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_auth_members m WHERE m.member = r.oid OR m.roleid = r.oid) THEN
        RAISE EXCEPTION '007 precondition: research reader role has role memberships';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_class c WHERE c.relnamespace = 'asd_rag'::regnamespace AND c.relkind IN ('r', 'v', 'm', 'p')
               AND has_table_privilege(r.oid, c.oid, 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')) THEN
        RAISE EXCEPTION '007 precondition: research reader already holds table privileges in asd_rag';
    END IF;
    IF to_regclass('asd_rag.research_chunk_embeddings') IS NULL
       OR to_regclass('asd_rag.research_embedding_authorization_chunks') IS NULL THEN
        RAISE EXCEPTION '007 precondition: migration 006 objects missing';
    END IF;
    IF EXISTS (SELECT 1 FROM research_embedding_authorizations WHERE revoked_at IS NULL
               GROUP BY profile_code HAVING count(*) > 1) THEN
        RAISE EXCEPTION '007 precondition: more than one active research authorization for one profile';
    END IF;
END $$;

-- 1. one active authorization per profile -------------------------------------------------------------
CREATE UNIQUE INDEX research_authorizations_one_active_per_profile
    ON research_embedding_authorizations (profile_code) WHERE revoked_at IS NULL;

-- 2. retrieval view: every C5 condition lives here (T0 report, section C5) ------------------------------
CREATE VIEW v_research_retrieval_chunks WITH (security_barrier = true) AS
SELECT e.research_embedding_id, a.authorization_id, p.profile_code, e.model_id, e.vector_dimension,
       e.embedding, e.vector_norm, e.embedding_input_hash, e.run_id AS embedding_run_id,
       c.chunk_id, c.chunk_index, c.document_id, d.source_id, d.document_version, s.title, s.source_url,
       s.publisher, s.source_type, s.corpus_role, x.group_membership,
       c.chunking_profile, c.section_path, c.section_heading, c.section_type, c.content_kind,
       c.page_start, c.page_end, c.char_start, c.char_end,
       c.content, c.content_tsv, c.content_sha256, c.token_count, c.completeness_status, c.missing_context
FROM research_embedding_authorizations a
JOIN embedding_profiles p                        ON p.profile_code = a.profile_code                  -- C5-3
JOIN research_embedding_authorization_sources x  ON x.authorization_id = a.authorization_id
JOIN research_embedding_authorization_chunks k   ON k.authorization_id = x.authorization_id         -- C5-2
                                                AND k.source_id = x.source_id
JOIN chunks c                                    ON c.chunk_id = k.chunk_id
                                                AND c.content_sha256 = k.content_sha256             -- C5-7
                                                AND c.chunking_profile = a.chunking_profile         -- C5-7
JOIN documents d                                 ON d.document_id = c.document_id
                                                AND d.source_id = x.source_id                       -- C5-10
JOIN sources s                                   ON s.source_id = d.source_id                        -- C5-10
JOIN research_chunk_embeddings e                 ON e.chunk_id = c.chunk_id
                                                AND e.profile_id = p.profile_id                     -- C5-3
WHERE a.revoked_at IS NULL                                                                           -- C5-1
  AND a.scope = 'research_test' AND NOT a.production_approval
  AND e.model_id = p.model_id                                                                        -- C5-4
  AND e.vector_dimension = p.vector_dimension AND vector_dims(e.embedding) = p.vector_dimension      -- C5-5
  AND e.input_type = p.document_input_type
  AND e.content_sha256 = c.content_sha256                       -- the vector embeds the current chunk text
  AND d.is_current                                                                                   -- C5-6
  AND d.content_review_status <> 'quarantined'                                                       -- C5-8
  AND s.corpus_role IN ('core', 'gaps')
  AND c.retrieval_eligible                                                                           -- C5-9
  AND c.completeness_status IN ('complete', 'document_has_gaps', 'references_missing_component');   -- C5-9
COMMENT ON VIEW v_research_retrieval_chunks IS
    'Research retrieval only (never production). All authorization and eligibility filters (C5) are applied here, '
    'so ORDER BY … LIMIT k runs on already-filtered rows. security_barrier stops caller predicates from being '
    'evaluated on filtered-out rows.';

-- 3. grants (new role + new view only) ------------------------------------------------------------------
REVOKE ALL ON v_research_retrieval_chunks FROM PUBLIC;
GRANT USAGE ON SCHEMA asd_rag TO asd_rag_v2_research_reader;
GRANT SELECT ON v_research_retrieval_chunks TO asd_rag_v2_research_reader;

-- 4. postconditions -------------------------------------------------------------------------------------
DO $$
DECLARE reader oid := 'asd_rag_v2_research_reader'::regrole;
BEGIN
    IF NOT has_table_privilege(reader, 'asd_rag.v_research_retrieval_chunks', 'SELECT') THEN
        RAISE EXCEPTION '007 postcondition: reader cannot SELECT the retrieval view';
    END IF;
    IF has_table_privilege(reader, 'asd_rag.v_research_retrieval_chunks', 'INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER') THEN
        RAISE EXCEPTION '007 postcondition: reader has a write privilege on the retrieval view';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_class c WHERE c.relnamespace = 'asd_rag'::regnamespace AND c.relkind IN ('r', 'v', 'm', 'p')
               AND c.relname <> 'v_research_retrieval_chunks'
               AND has_table_privilege(reader, c.oid, 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')) THEN
        RAISE EXCEPTION '007 postcondition: reader holds privileges on another relation';
    END IF;
    IF has_schema_privilege(reader, 'asd_rag', 'CREATE') OR has_schema_privilege(reader, 'public', 'CREATE')
       OR has_database_privilege(reader, current_database(), 'CREATE, TEMPORARY') THEN
        RAISE EXCEPTION '007 postcondition: reader can create objects';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_proc WHERE pronamespace = 'asd_rag'::regnamespace AND prosecdef) THEN
        RAISE EXCEPTION '007 postcondition: SECURITY DEFINER function present in asd_rag';
    END IF;
END $$;
