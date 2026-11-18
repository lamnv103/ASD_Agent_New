-- Rollback for 006_research_embedding_track.sql. Run as asd_rag_v2_owner, then
--   DELETE FROM asd_rag.schema_migrations WHERE version = '006';
-- DESTRUCTIVE for research vectors and research authorizations: take a pg_dump first.
-- Production objects (chunk_embeddings, gate views, source_rights, grants) are not touched.

SET search_path = asd_rag, public;
BEGIN;
DROP TRIGGER research_chunk_embeddings_guard ON research_chunk_embeddings;
DROP FUNCTION research_embedding_guard();
DROP TABLE research_chunk_embeddings;
DROP VIEW v_research_embedding_candidates;
DROP TABLE research_embedding_authorization_chunks;
DROP TABLE research_embedding_authorization_sources;
DROP TABLE research_embedding_authorizations;
COMMIT;
