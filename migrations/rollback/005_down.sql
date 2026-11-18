-- Rollback for 005_chunk_status_v2_1.sql. Run as asd_rag_v2_owner, then
--   DELETE FROM asd_rag.schema_migrations WHERE version = '005';
-- Precondition: no chunk uses the four statuses added by 005 (delete section_v2_1 chunks first),
-- otherwise restoring the 004 CHECK fails — the intended safety stop.

SET search_path = asd_rag, public;
BEGIN;
ALTER TABLE chunks DROP CONSTRAINT chunks_unverified_structure_not_retrievable;
ALTER TABLE chunks DROP CONSTRAINT chunks_completeness_status_check;
ALTER TABLE chunks ADD CONSTRAINT chunks_completeness_status_check CHECK (completeness_status IN (
    'complete', 'document_has_gaps', 'references_missing_component', 'table_structure_lost'));
COMMIT;
