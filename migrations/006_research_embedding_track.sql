-- 006_research_embedding_track.sql — research/test embedding track, separate from production approval.
--
-- Why: the production gate (v_embedding_eligible_documents) requires owner rights decisions
-- (source_rights.*_allowed = TRUE) and content approval; none exist. The project owner instructed a
-- research/test embedding of groups A/B/C. This migration records that instruction as a *research
-- authorization* without touching any production decision:
--   1. research_embedding_authorizations        who authorized what, why, for which profile; never production
--   2. research_embedding_authorization_sources the authorized sources and their group membership (A/B/C)
--   3. research_embedding_authorization_chunks  the exact preflight allowlist (chunk_id + content hash)
--   4. v_research_embedding_candidates          allowlist ∩ structural rules (defence in depth)
--   5. research_chunk_embeddings                research vectors with model, dimension, run, content hash
--   6. guard trigger: a research vector can only be stored for a current candidate with the same content
--      hash, the profile's model and dimension
-- Unchanged: source_rights, documents approvals, chunks, chunk_embeddings, v_embedding_eligible_documents,
-- v_retrieval_ready_chunks, every existing grant. The app role gets NO access to anything created here, so
-- research vectors cannot reach production retrieval.
-- Rollback: migrations/rollback/006_down.sql (drops research vectors — back up first).

SET search_path = asd_rag, public;

-- 1 ------------------------------------------------------------------------------------------------
CREATE TABLE research_embedding_authorizations (
    authorization_id    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    scope               text NOT NULL CHECK (scope = 'research_test'),
    production_approval boolean NOT NULL DEFAULT false CHECK (production_approval = false),
    authorized_by       text NOT NULL CHECK (btrim(authorized_by) <> ''),
    recorded_by         text NOT NULL CHECK (btrim(recorded_by) <> ''),
    basis               text NOT NULL CHECK (btrim(basis) <> ''),
    profile_code        text NOT NULL REFERENCES embedding_profiles (profile_code) ON DELETE RESTRICT,
    chunking_profile    text NOT NULL,
    manifest_sha256     text NOT NULL CHECK (manifest_sha256 ~ '^[0-9a-f]{64}$'),
    authorized_at       timestamptz NOT NULL DEFAULT now(),
    revoked_at          timestamptz,
    notes               text
);
COMMENT ON TABLE research_embedding_authorizations IS
    'Research/test embedding only. Not a rights decision: never sets source_rights.*_allowed, never approves '
    'content, embedding or retrieval for production, never marks clinical review.';

-- 2 ------------------------------------------------------------------------------------------------
CREATE TABLE research_embedding_authorization_sources (
    authorization_id integer NOT NULL REFERENCES research_embedding_authorizations ON DELETE RESTRICT,
    source_id        text NOT NULL REFERENCES sources (source_id) ON DELETE RESTRICT,
    group_membership text[] NOT NULL
        CHECK (cardinality(group_membership) > 0 AND group_membership <@ ARRAY['A', 'B', 'C']),
    PRIMARY KEY (authorization_id, source_id)
);

-- 3 ------------------------------------------------------------------------------------------------
CREATE TABLE research_embedding_authorization_chunks (
    authorization_id integer NOT NULL,
    source_id        text NOT NULL,
    chunk_id         text NOT NULL REFERENCES chunks (chunk_id) ON DELETE RESTRICT,
    content_sha256   text NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    PRIMARY KEY (authorization_id, chunk_id),
    FOREIGN KEY (authorization_id, source_id)
        REFERENCES research_embedding_authorization_sources (authorization_id, source_id) ON DELETE RESTRICT
);

-- 4 ------------------------------------------------------------------------------------------------
CREATE VIEW v_research_embedding_candidates AS
SELECT a.authorization_id, a.profile_code, x.group_membership, d.source_id, c.document_id, c.chunk_id,
       s.title, c.section_heading, c.content, c.content_sha256
FROM research_embedding_authorizations a
JOIN research_embedding_authorization_sources x ON x.authorization_id = a.authorization_id
JOIN research_embedding_authorization_chunks k
  ON k.authorization_id = x.authorization_id AND k.source_id = x.source_id
JOIN chunks c    ON c.chunk_id = k.chunk_id AND c.content_sha256 = k.content_sha256
                AND c.chunking_profile = a.chunking_profile
JOIN documents d ON d.document_id = c.document_id AND d.source_id = x.source_id
JOIN sources s   ON s.source_id = d.source_id
WHERE a.revoked_at IS NULL
  AND d.is_current
  AND d.content_review_status <> 'quarantined'
  AND s.corpus_role IN ('core', 'gaps')
  AND c.retrieval_eligible
  AND c.completeness_status IN ('complete', 'document_has_gaps', 'references_missing_component');

-- 5 ------------------------------------------------------------------------------------------------
CREATE TABLE research_chunk_embeddings (
    research_embedding_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chunk_id             text NOT NULL REFERENCES chunks (chunk_id) ON DELETE RESTRICT,
    profile_id           integer NOT NULL REFERENCES embedding_profiles ON DELETE RESTRICT,
    authorization_id     integer NOT NULL REFERENCES research_embedding_authorizations ON DELETE RESTRICT,
    run_id               uuid NOT NULL REFERENCES ingestion_runs ON DELETE RESTRICT,
    model_id             text NOT NULL,
    vector_dimension     integer NOT NULL CHECK (vector_dimension = 1536),
    input_type           text NOT NULL CHECK (input_type = 'search_document'),
    embedding            vector(1536) NOT NULL,
    vector_norm          real NOT NULL CHECK (vector_norm > 0),
    content_sha256       text NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    embedding_input_hash text NOT NULL CHECK (embedding_input_hash ~ '^[0-9a-f]{64}$'),
    created_at           timestamptz NOT NULL DEFAULT now(),
    UNIQUE (chunk_id, profile_id),
    CHECK (vector_dims(embedding) = vector_dimension)
);
CREATE INDEX research_chunk_embeddings_run ON research_chunk_embeddings (run_id);
COMMENT ON TABLE research_chunk_embeddings IS
    'Research/test vectors. Not readable by the app role; never used by production retrieval views.';

-- 6 ------------------------------------------------------------------------------------------------
CREATE FUNCTION research_embedding_guard() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM v_research_embedding_candidates v
                   JOIN embedding_profiles p ON p.profile_code = v.profile_code
                   WHERE v.authorization_id = NEW.authorization_id AND v.chunk_id = NEW.chunk_id
                     AND v.content_sha256 = NEW.content_sha256 AND p.profile_id = NEW.profile_id
                     AND p.model_id = NEW.model_id AND p.vector_dimension = NEW.vector_dimension
                     AND p.document_input_type = NEW.input_type) THEN
        RAISE EXCEPTION 'research embedding for % is not an authorized current candidate', NEW.chunk_id
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER research_chunk_embeddings_guard BEFORE INSERT OR UPDATE ON research_chunk_embeddings
    FOR EACH ROW EXECUTE FUNCTION research_embedding_guard();

-- grants (new objects only; app gets nothing) -----------------------------------------------------
GRANT SELECT ON research_embedding_authorizations, research_embedding_authorization_sources,
                research_embedding_authorization_chunks, v_research_embedding_candidates
   TO asd_rag_v2_ingest;
GRANT SELECT, INSERT ON research_chunk_embeddings TO asd_rag_v2_ingest;
