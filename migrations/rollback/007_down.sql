-- Rollback for 007_research_retrieval_access.sql. Run as asd_rag_v2_owner, then
--   DELETE FROM asd_rag.schema_migrations WHERE version = '007';
-- then (superuser) deploy/db/rollback/research_reader_down.sql to drop the role itself.
-- Non-destructive: removes only the view, the partial unique index and the reader's grants. No table data,
-- no vector, no authorization row is touched (authorization revisions are reverted separately with
-- scripts/research_authorization_revise.py --restore).
-- Precondition: at most one active authorization per profile is NOT required by the rollback.

SET search_path = asd_rag, public;
BEGIN;
REVOKE SELECT ON v_research_retrieval_chunks FROM asd_rag_v2_research_reader;
REVOKE USAGE ON SCHEMA asd_rag FROM asd_rag_v2_research_reader;
DROP VIEW v_research_retrieval_chunks;
DROP INDEX research_authorizations_one_active_per_profile;
COMMIT;
