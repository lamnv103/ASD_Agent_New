#!/bin/bash
# Phase 6.2 T2.1 — privileged step for migration 007 (needs CREATEROLE, which asd_rag_v2_owner does not have).
# Creates the read-only research retrieval role. Idempotent: safe to re-run; it re-asserts the attributes.
#   * fresh volume : runs automatically after 00_bootstrap.sh (docker-entrypoint-initdb.d)
#   * existing DB  : docker exec -i -e ASD_RAG_DB_NAME -e ASD_RAG_RESEARCH_READER_PASSWORD <container> \
#                      bash -s < deploy/db/initdb/10_research_reader.sh
# Grants on schema asd_rag and on the retrieval view are NOT here: migration 007 (owner) does them.
# Rollback: deploy/db/rollback/research_reader_down.sql (after migrations/rollback/007_down.sql).
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER:-postgres}" --dbname postgres \
  -v db_name="$ASD_RAG_DB_NAME" \
  -v reader_pw="$ASD_RAG_RESEARCH_READER_PASSWORD" <<'SQL'
SELECT 'CREATE ROLE asd_rag_v2_research_reader'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'asd_rag_v2_research_reader') \gexec

-- least privilege: can log in (the research retriever connects directly), nothing else
ALTER ROLE asd_rag_v2_research_reader LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS
    CONNECTION LIMIT 5 PASSWORD :'reader_pw';
ALTER ROLE asd_rag_v2_research_reader IN DATABASE :"db_name" SET search_path = asd_rag, public;
ALTER ROLE asd_rag_v2_research_reader IN DATABASE :"db_name" SET default_transaction_read_only = on;
ALTER ROLE asd_rag_v2_research_reader IN DATABASE :"db_name" SET statement_timeout = '60s';
GRANT CONNECT ON DATABASE :"db_name" TO asd_rag_v2_research_reader;

\connect :"db_name"
-- the vector type and the <=> operator live in schema public (pgvector)
GRANT USAGE ON SCHEMA public TO asd_rag_v2_research_reader;
SQL
