-- 002_indexes.sql — lookup and full-text indexes.
-- No ANN (HNSW/IVFFlat) index here on purpose: exact cosine search is the baseline until
-- a benchmark shows it is too slow (an ANN index would be a later, separate migration).

SET search_path = asd_rag, public;

CREATE INDEX sources_corpus_role_idx            ON sources (corpus_role);
CREATE INDEX sources_subject_areas_idx          ON sources USING gin (subject_areas);
CREATE INDEX sources_title_fts_idx              ON sources USING gin (to_tsvector('english', title));

CREATE INDEX chunks_document_idx                ON chunks (document_id, chunking_profile);
CREATE INDEX chunks_content_tsv_idx             ON chunks USING gin (content_tsv);

CREATE INDEX chunk_embeddings_profile_idx       ON chunk_embeddings (profile_id);

CREATE INDEX ingestion_run_documents_doc_idx    ON ingestion_run_documents (document_id);

CREATE INDEX retrieval_logs_created_idx         ON retrieval_logs (created_at);
CREATE INDEX retrieval_results_chunk_idx        ON retrieval_results (chunk_id);
CREATE INDEX retrieval_results_source_idx       ON retrieval_results (source_id);
CREATE INDEX answer_runs_retrieval_idx          ON answer_runs (retrieval_id);
CREATE INDEX answer_runs_created_idx            ON answer_runs (created_at);
