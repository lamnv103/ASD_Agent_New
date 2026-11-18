-- 004_rights_evidence_and_chunk_v2.sql
-- Purpose (see eval/reports/license_audit_2026-11-14.md and 2026-11-14_chunking_section_v2.md):
--   1. Licence facts and the remaining per-action permissions on source_rights. New permission columns are
--      NULL (= not verified = not allowed); only the owner role may set them.
--   2. rights_assessments: per-action EVIDENCE (what the licence / provider terms say), kept separate from
--      the owner's DECISION in source_rights.*_allowed.
--   3. chunks.completeness_status gains 'table_structure_lost' (PDF tables flattened during extraction).
--   4. The embedding gate also requires archive and chunking permission.
--   5. v_chunk_provenance: chunks with inherited document/source metadata, for ingest/owner review.
-- No data is written by this migration. Rollback: migrations/rollback/004_down.sql.

SET search_path = asd_rag, public;

-- 1 ------------------------------------------------------------------------------------------------
ALTER TABLE source_rights
    ADD COLUMN license_type text CHECK (license_type IN (
        'CC BY', 'CC BY-NC', 'CC BY-NC-SA', 'Public Domain', 'Publisher-specific', 'Copyright', 'Unknown', 'Other')),
    ADD COLUMN license_version      text,
    ADD COLUMN rights_holder        text,
    ADD COLUMN archive_allowed      boolean,
    ADD COLUMN chunking_allowed     boolean,
    ADD COLUMN share_alike_required boolean;

-- 2 ------------------------------------------------------------------------------------------------
CREATE TABLE rights_assessments (
    source_id         text NOT NULL REFERENCES sources (source_id) ON DELETE RESTRICT,
    action            text NOT NULL CHECK (action IN (
        'archive_allowed', 'text_mining_allowed', 'chunking_allowed', 'embedding_allowed',
        'cohere_processing_allowed', 'external_llm_processing_allowed', 'commercial_use_allowed',
        'attribution_required', 'share_alike_required')),
    basis             text NOT NULL CHECK (basis IN ('source_license', 'provider_terms')),
    assessment        text NOT NULL CHECK (assessment IN (
        'yes_by_license', 'nc_only_by_license', 'no_by_license', 'conditional', 'pending_decision', 'blocked',
        'unknown')),
    evidence_url      text,
    evidence_location text,
    evidence_excerpt  text,
    assessed_by       text NOT NULL,
    assessed_at       timestamptz NOT NULL DEFAULT now(),
    notes             text,
    PRIMARY KEY (source_id, action, basis)
);
COMMENT ON TABLE rights_assessments IS
    'Evidence only. The effective permission is source_rights.<action>, set by the owner; an assessment never grants it.';

-- 3 ------------------------------------------------------------------------------------------------
ALTER TABLE chunks DROP CONSTRAINT chunks_completeness_status_check;
ALTER TABLE chunks ADD CONSTRAINT chunks_completeness_status_check CHECK (completeness_status IN (
    'complete', 'document_has_gaps', 'references_missing_component', 'table_structure_lost'));

-- 4 ------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_embedding_eligible_documents AS
SELECT d.*
FROM documents d
JOIN sources s       ON s.source_id = d.source_id
JOIN source_rights r ON r.source_id = d.source_id
WHERE d.is_current
  AND d.approved_for_embedding
  AND d.content_review_status = 'approved'
  AND d.content_warning IS NULL
  AND s.corpus_role IN ('core', 'gaps')
  AND r.archive_allowed IS TRUE
  AND r.text_mining_allowed IS TRUE
  AND r.chunking_allowed IS TRUE
  AND r.embedding_allowed IS TRUE
  AND r.cohere_processing_allowed IS TRUE;

-- 5 ------------------------------------------------------------------------------------------------
CREATE VIEW v_chunk_provenance AS
SELECT c.chunk_id, c.chunk_index, c.chunking_profile, c.document_id, d.source_id, s.title,
       c.section_path, c.section_type, c.content_kind, c.page_start, c.page_end, c.char_start, c.char_end,
       s.corpus_role, d.text_completeness, d.missing_components, c.completeness_status, c.missing_context,
       c.content_sha256, c.token_count, c.retrieval_eligible,
       d.content_review_status, d.content_warning, d.approved_for_embedding, d.approved_for_retrieval,
       r.license_type, r.rights_status
FROM chunks c
JOIN documents d     ON d.document_id = c.document_id
JOIN sources s       ON s.source_id = d.source_id
JOIN source_rights r ON r.source_id = d.source_id;

-- 6 grants ------------------------------------------------------------------------------------------
GRANT INSERT (license_type, license_version, rights_holder),
      UPDATE (license_type, license_version, rights_holder)
   ON source_rights TO asd_rag_v2_ingest;
GRANT SELECT, INSERT ON rights_assessments TO asd_rag_v2_ingest;
GRANT UPDATE (assessment, evidence_url, evidence_location, evidence_excerpt, assessed_by, assessed_at, notes)
   ON rights_assessments TO asd_rag_v2_ingest;
GRANT SELECT ON v_chunk_provenance TO asd_rag_v2_ingest;
