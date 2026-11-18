-- Privileged rollback of deploy/db/initdb/10_research_reader.sh. Run as the superuser, connected to the
-- application database, AFTER migrations/rollback/007_down.sql (which revokes the object grants):
--   docker exec -i <container> psql -v ON_ERROR_STOP=1 -U postgres -d asd_rag_v2 < deploy/db/rollback/research_reader_down.sql
-- Removes only the research reader role and its grants; no data, no other role is touched.
REVOKE USAGE ON SCHEMA public FROM asd_rag_v2_research_reader;
REVOKE CONNECT ON DATABASE asd_rag_v2 FROM asd_rag_v2_research_reader;
ALTER ROLE asd_rag_v2_research_reader IN DATABASE asd_rag_v2 RESET ALL;
DROP ROLE asd_rag_v2_research_reader;
