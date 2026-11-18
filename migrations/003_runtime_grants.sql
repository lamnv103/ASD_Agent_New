-- 003_runtime_grants.sql — least-privilege access for the ingest and app roles.
-- owner  : owns everything, runs migrations, is the only role that can set approvals and
--          processing permissions (human review decisions).
-- ingest : loads catalog/documents/chunks/embeddings; cannot approve anything.
-- app    : read-only on curated data (chunks only through the gate view); writes audit logs.

SET search_path = asd_rag, public;

REVOKE ALL ON ALL TABLES IN SCHEMA asd_rag FROM PUBLIC;
GRANT USAGE ON SCHEMA asd_rag TO asd_rag_v2_ingest, asd_rag_v2_app;

-- ---------------------------------------------------------------- ingest
GRANT SELECT ON ALL TABLES IN SCHEMA asd_rag TO asd_rag_v2_ingest;
REVOKE SELECT ON schema_migrations FROM asd_rag_v2_ingest;

GRANT INSERT, UPDATE ON sources TO asd_rag_v2_ingest;

GRANT INSERT (source_id, rights_status, license_name, license_url, permitted_use_notes, evidence_url),
      UPDATE (rights_status, license_name, license_url, permitted_use_notes, evidence_url, updated_at)
   ON source_rights TO asd_rag_v2_ingest;

GRANT INSERT (document_id, source_id, document_version, raw_relative_path, corpus_relative_path,
              original_file_name, file_format, file_sha256, original_sha256, character_count, page_count,
              text_completeness, missing_components, extraction_status, content_review_status,
              content_warning, extraction_tool, extraction_version, is_current),
      UPDATE (raw_relative_path, corpus_relative_path, original_file_name, file_format, file_sha256,
              original_sha256, character_count, page_count, text_completeness, missing_components,
              extraction_status, extraction_tool, extraction_version, is_current, updated_at)
   ON documents TO asd_rag_v2_ingest;

GRANT INSERT, DELETE ON chunks, chunk_embeddings TO asd_rag_v2_ingest;

GRANT INSERT (profile_code, provider, model_id, model_revision, vector_dimension, document_input_type,
              query_input_type, similarity_metric, api_version, configuration)
   ON embedding_profiles TO asd_rag_v2_ingest;

GRANT INSERT, UPDATE (status, finished_at, stats, error_summary) ON ingestion_runs TO asd_rag_v2_ingest;
GRANT INSERT ON ingestion_run_documents TO asd_rag_v2_ingest;

-- ---------------------------------------------------------------- app
GRANT SELECT ON sources, source_rights, documents, embedding_profiles, chunk_embeddings,
                v_embedding_eligible_documents, v_retrieval_ready_chunks
   TO asd_rag_v2_app;
GRANT INSERT ON retrieval_logs, retrieval_results, answer_runs TO asd_rag_v2_app;
