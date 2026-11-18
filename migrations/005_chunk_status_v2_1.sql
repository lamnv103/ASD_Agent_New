-- 005_chunk_status_v2_1.sql
-- chunks.completeness_status gains the statuses produced by chunking profile section_v2_1:
--   table_structure_unrecoverable   flattened PDF table, no structure that passes automated checks
--   table_recovered_pending_review  a structured candidate exists in data/extractions, awaiting a human reviewer
--   page_provenance_incomplete      PDF-derived text whose page cannot be established from a verified page map
--   text_encoding_lost              extracted text holds glyph ids (/gidNNNNN) instead of characters
-- All four are excluded from retrieval: by the chunker and by the CHECK below. No data is written.
-- Rollback: migrations/rollback/005_down.sql

SET search_path = asd_rag, public;

ALTER TABLE chunks DROP CONSTRAINT chunks_completeness_status_check;
ALTER TABLE chunks ADD CONSTRAINT chunks_completeness_status_check CHECK (completeness_status IN (
    'complete', 'document_has_gaps', 'references_missing_component', 'table_structure_lost',
    'table_structure_unrecoverable', 'table_recovered_pending_review', 'page_provenance_incomplete',
    'text_encoding_lost'));

-- These statuses can never be retrievable: enforce it in the table, not only in the chunker.
ALTER TABLE chunks ADD CONSTRAINT chunks_unverified_structure_not_retrievable CHECK (
    NOT retrieval_eligible OR completeness_status NOT IN (
        'table_structure_lost', 'table_structure_unrecoverable', 'table_recovered_pending_review',
        'page_provenance_incomplete', 'text_encoding_lost'));
