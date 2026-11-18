-- Rollback for 004_rights_evidence_and_chunk_v2.sql. Run as asd_rag_v2_owner, then
--   DELETE FROM asd_rag.schema_migrations WHERE version = '004';
-- Precondition: no chunk uses completeness_status = 'table_structure_lost' (delete section_v2 chunks first),
-- otherwise restoring the old CHECK fails — which is the intended safety stop.
-- Data in rights_assessments and the new source_rights columns is lost: export it first if it was filled.

SET search_path = asd_rag, public;
BEGIN;

DROP VIEW v_chunk_provenance;

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
  AND r.text_mining_allowed IS TRUE
  AND r.embedding_allowed IS TRUE
  AND r.cohere_processing_allowed IS TRUE;

ALTER TABLE chunks DROP CONSTRAINT chunks_completeness_status_check;
ALTER TABLE chunks ADD CONSTRAINT chunks_completeness_status_check CHECK (completeness_status IN (
    'complete', 'document_has_gaps', 'references_missing_component'));

DROP TABLE rights_assessments;

ALTER TABLE source_rights
    DROP COLUMN license_type, DROP COLUMN license_version, DROP COLUMN rights_holder,
    DROP COLUMN archive_allowed, DROP COLUMN chunking_allowed, DROP COLUMN share_alike_required;

COMMIT;
