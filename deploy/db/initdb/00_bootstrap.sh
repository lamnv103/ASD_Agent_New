#!/bin/bash
# Runs once, on an empty data volume, as the container superuser.
# Creates the three roles, the application database, pgvector and the asd_rag schema.
# Tables/views/grants are NOT created here: they come from versioned files in migrations/.
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
  -v db_name="$ASD_RAG_DB_NAME" \
  -v owner_pw="$ASD_RAG_OWNER_PASSWORD" \
  -v ingest_pw="$ASD_RAG_INGEST_PASSWORD" \
  -v app_pw="$ASD_RAG_APP_PASSWORD" <<'SQL'
CREATE ROLE asd_rag_v2_owner  LOGIN PASSWORD :'owner_pw';
CREATE ROLE asd_rag_v2_ingest LOGIN PASSWORD :'ingest_pw';
CREATE ROLE asd_rag_v2_app    LOGIN PASSWORD :'app_pw';

CREATE DATABASE :"db_name" OWNER asd_rag_v2_owner;
REVOKE ALL ON DATABASE :"db_name" FROM PUBLIC;
GRANT CONNECT ON DATABASE :"db_name" TO asd_rag_v2_ingest, asd_rag_v2_app;
ALTER ROLE asd_rag_v2_owner  IN DATABASE :"db_name" SET search_path = asd_rag, public;
ALTER ROLE asd_rag_v2_ingest IN DATABASE :"db_name" SET search_path = asd_rag, public;
ALTER ROLE asd_rag_v2_app    IN DATABASE :"db_name" SET search_path = asd_rag, public;

\connect :"db_name"
CREATE EXTENSION IF NOT EXISTS vector;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO asd_rag_v2_owner, asd_rag_v2_ingest, asd_rag_v2_app;
CREATE SCHEMA asd_rag AUTHORIZATION asd_rag_v2_owner;
SQL
