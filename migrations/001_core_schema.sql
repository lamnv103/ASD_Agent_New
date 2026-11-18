-- 001_core_schema.sql — tables and views for asd_rag_v2 (schema asd_rag).
-- Runs as asd_rag_v2_owner through scripts/db_migrate.py, inside one transaction.
-- Conventions:
--   * NULL in a permission/decision column means "not verified yet" and is treated as NOT allowed.
--   * Approval flags default to false and are only set by a reviewer (owner role), never by ingest.

SET search_path = asd_rag, public;

-- ---------------------------------------------------------------- sources (174)
CREATE TABLE sources (
    source_id        text PRIMARY KEY,
    title            text NOT NULL,
    authors          text[] NOT NULL DEFAULT '{}',
    publisher        text,
    publication_year integer CHECK (publication_year BETWEEN 1900 AND 2100),
    doi              text,
    source_url       text,
    source_type      text,
    subject_areas    text[] NOT NULL DEFAULT '{}',
    corpus_role      text NOT NULL CHECK (corpus_role IN ('core', 'gaps', 'metadata_only', 'excluded')),
    scope_status     text NOT NULL,
    content_warning  text,
    catalog_payload  jsonb NOT NULL,
    created_at       timestamptz NOT NULL DEFAULT now(),
    updated_at       timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN sources.corpus_role IS 'Tier from scripts/build_corpus.py. Says what content exists, NOT what use is permitted (see source_rights).';
COMMENT ON COLUMN sources.catalog_payload IS 'Full raw catalog record from data/raw/source_library/catalog.jsonl, kept for audit.';

-- ---------------------------------------------------------------- source_rights (1:1 with sources)
CREATE TABLE source_rights (
    source_id                       text PRIMARY KEY REFERENCES sources (source_id) ON DELETE RESTRICT,
    rights_status                   text NOT NULL,
    license_name                    text,
    license_url                     text,
    text_mining_allowed             boolean,
    embedding_allowed               boolean,
    cohere_processing_allowed       boolean,
    external_llm_processing_allowed boolean,
    commercial_use_allowed          boolean,
    attribution_required            boolean,
    permitted_use_notes             text,
    evidence_url                    text,
    verified_by                     text,
    verified_at                     timestamptz,
    updated_at                      timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE source_rights IS 'NULL in *_allowed = not verified = not allowed. Processing permissions are a human decision, never inferred from the licence label.';

-- ---------------------------------------------------------------- documents (73 full-text, versioned)
CREATE TABLE documents (
    document_id            text PRIMARY KEY,
    source_id              text NOT NULL REFERENCES sources (source_id) ON DELETE RESTRICT,
    document_version       text NOT NULL,
    raw_relative_path      text NOT NULL,
    corpus_relative_path   text NOT NULL,
    original_file_name     text,
    file_format            text,
    file_sha256            text NOT NULL CHECK (file_sha256 ~ '^[0-9a-f]{64}$'),
    original_sha256        text CHECK (original_sha256 ~ '^[0-9a-f]{64}$'),
    character_count        integer NOT NULL CHECK (character_count > 0),
    page_count             integer CHECK (page_count > 0),
    text_completeness      text NOT NULL CHECK (text_completeness IN ('complete', 'partial')),
    missing_components     jsonb NOT NULL DEFAULT '{}',
    extraction_status      text NOT NULL,
    content_review_status  text NOT NULL DEFAULT 'pending'
                           CHECK (content_review_status IN ('pending', 'quarantined', 'approved', 'rejected')),
    approved_for_embedding boolean NOT NULL DEFAULT false,
    approved_for_retrieval boolean NOT NULL DEFAULT false,
    content_warning        text,
    extraction_tool        text,
    extraction_version     text,
    is_current             boolean NOT NULL DEFAULT true,
    registered_at          timestamptz NOT NULL DEFAULT now(),
    updated_at             timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, document_version),
    -- An approval can only exist on reviewed, warning-free content.
    CONSTRAINT approval_requires_review CHECK (
        NOT (approved_for_embedding OR approved_for_retrieval)
        OR (content_review_status = 'approved' AND content_warning IS NULL)
    ),
    CONSTRAINT quarantine_has_reason CHECK (content_review_status <> 'quarantined' OR content_warning IS NOT NULL)
);
CREATE UNIQUE INDEX documents_one_current_per_source ON documents (source_id) WHERE is_current;

-- ---------------------------------------------------------------- chunks
CREATE TABLE chunks (
    chunk_id            text PRIMARY KEY,
    document_id         text NOT NULL REFERENCES documents (document_id) ON DELETE RESTRICT,
    chunk_index         integer NOT NULL CHECK (chunk_index >= 0),
    chunking_profile    text NOT NULL,
    section_path        text[] NOT NULL DEFAULT '{}',
    section_heading     text NOT NULL DEFAULT '',
    section_type        text NOT NULL,
    content_kind        text NOT NULL CHECK (content_kind IN ('text', 'table')),
    page_start          integer CHECK (page_start > 0),
    page_end            integer CHECK (page_end >= page_start),
    char_start          integer NOT NULL CHECK (char_start >= 0),
    char_end            integer NOT NULL CHECK (char_end > char_start),
    content             text NOT NULL CHECK (length(content) > 0),
    language            text NOT NULL,
    token_count         integer NOT NULL CHECK (token_count > 0),
    content_sha256      text NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    corpus_role         text NOT NULL CHECK (corpus_role IN ('core', 'gaps')),
    completeness_status text NOT NULL
                        CHECK (completeness_status IN ('complete', 'document_has_gaps', 'references_missing_component')),
    missing_context     text,
    retrieval_eligible  boolean NOT NULL DEFAULT false,
    content_tsv         tsvector GENERATED ALWAYS AS (
                            setweight(to_tsvector('english', section_heading), 'B')
                            || setweight(to_tsvector('english', content), 'A')
                        ) STORED,
    created_at          timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, chunking_profile, chunk_index)
);
COMMENT ON COLUMN chunks.section_heading IS 'section_path joined with " > " (kept as text because generated tsvector columns need immutable input).';
COMMENT ON COLUMN chunks.char_start IS 'Offset into the corpus file (data/corpus/<tier>/<source_id>.md) for provenance checks.';
COMMENT ON COLUMN chunks.retrieval_eligible IS 'Chunk-level gate (e.g. false for references/back matter). Document and rights gates are applied in v_retrieval_ready_chunks.';

-- ---------------------------------------------------------------- embedding_profiles
CREATE TABLE embedding_profiles (
    profile_id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    profile_code        text NOT NULL UNIQUE,
    provider            text NOT NULL,
    model_id            text NOT NULL,
    model_revision      text,
    vector_dimension    integer NOT NULL CHECK (vector_dimension = 1536),
    document_input_type text NOT NULL,
    query_input_type    text NOT NULL,
    similarity_metric   text NOT NULL CHECK (similarity_metric = 'cosine'),
    api_version         text NOT NULL,
    configuration       jsonb NOT NULL DEFAULT '{}',
    is_active           boolean NOT NULL DEFAULT false,
    created_at          timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX embedding_profiles_one_active ON embedding_profiles (is_active) WHERE is_active;

-- ---------------------------------------------------------------- chunk_embeddings
CREATE TABLE chunk_embeddings (
    embedding_id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chunk_id             text NOT NULL REFERENCES chunks (chunk_id) ON DELETE CASCADE,
    profile_id           integer NOT NULL REFERENCES embedding_profiles (profile_id) ON DELETE RESTRICT,
    embedding            public.vector(1536) NOT NULL,
    vector_norm          real NOT NULL CHECK (vector_norm > 0),
    embedding_input_hash text NOT NULL CHECK (embedding_input_hash ~ '^[0-9a-f]{64}$'),
    created_at           timestamptz NOT NULL DEFAULT now(),
    UNIQUE (chunk_id, profile_id)
);

-- ---------------------------------------------------------------- ingestion audit
CREATE TABLE ingestion_runs (
    run_id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    run_type          text NOT NULL,
    status            text NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'succeeded', 'failed', 'partial')),
    started_at        timestamptz NOT NULL DEFAULT now(),
    finished_at       timestamptz,
    code_version      text,
    input_fingerprint text,
    configuration     jsonb NOT NULL DEFAULT '{}',
    stats             jsonb NOT NULL DEFAULT '{}',
    error_summary     text,
    CHECK ((status = 'running') = (finished_at IS NULL))
);

CREATE TABLE ingestion_run_documents (
    run_id         uuid NOT NULL REFERENCES ingestion_runs (run_id) ON DELETE CASCADE,
    document_id    text NOT NULL REFERENCES documents (document_id) ON DELETE RESTRICT,
    status         text NOT NULL CHECK (status IN ('succeeded', 'failed', 'skipped')),
    chunk_count    integer,
    embedded_count integer,
    error_code     text,
    error_detail   text,
    processed_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, document_id)
);

-- ---------------------------------------------------------------- retrieval / answer audit (no raw user text)
CREATE TABLE retrieval_logs (
    retrieval_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at       timestamptz NOT NULL DEFAULT now(),
    query_hash       text NOT NULL CHECK (query_hash ~ '^[0-9a-f]{64}$'),
    query_language   text,
    query_variants   text[] NOT NULL DEFAULT '{}',
    retrieval_method text NOT NULL,
    profile_id       integer REFERENCES embedding_profiles (profile_id),
    top_k            integer,
    candidate_count  integer NOT NULL DEFAULT 0,
    selected_count   integer NOT NULL DEFAULT 0,
    evidence_status  text CHECK (evidence_status IN ('sufficient', 'partial', 'conflicting', 'insufficient', 'blocked')),
    latency_ms       integer,
    configuration    jsonb NOT NULL DEFAULT '{}'
);
COMMENT ON TABLE retrieval_logs IS 'Stores a hash of the question, never the question text.';

CREATE TABLE retrieval_results (
    retrieval_id         uuid NOT NULL REFERENCES retrieval_logs (retrieval_id) ON DELETE CASCADE,
    chunk_id             text NOT NULL REFERENCES chunks (chunk_id) ON DELETE RESTRICT,
    source_id            text NOT NULL REFERENCES sources (source_id),
    retrieval_rank       integer NOT NULL,
    dense_rank           integer,
    sparse_rank          integer,
    dense_score          real,
    sparse_score         real,
    fused_score          real,
    rerank_score         real,
    selected_for_context boolean NOT NULL DEFAULT false,
    PRIMARY KEY (retrieval_id, chunk_id)
);

CREATE TABLE answer_runs (
    answer_id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    retrieval_id               uuid REFERENCES retrieval_logs (retrieval_id) ON DELETE SET NULL,
    created_at                 timestamptz NOT NULL DEFAULT now(),
    route                      text NOT NULL,
    model_provider             text,
    model_id                   text,
    prompt_version             text,
    configuration              jsonb NOT NULL DEFAULT '{}',
    evidence_status            text CHECK (evidence_status IN ('sufficient', 'partial', 'conflicting', 'insufficient', 'blocked')),
    answer_status              text NOT NULL CHECK (answer_status IN ('answered', 'partial', 'abstained', 'refused', 'error')),
    citation_validation_status text NOT NULL DEFAULT 'pending'
                               CHECK (citation_validation_status IN ('pending', 'valid', 'invalid', 'not_applicable')),
    cited_source_ids           text[] NOT NULL DEFAULT '{}',
    cited_chunk_ids            text[] NOT NULL DEFAULT '{}',
    answer_sha256              text,
    latency_ms                 integer,
    usage                      jsonb NOT NULL DEFAULT '{}'
);

-- ---------------------------------------------------------------- gate views
-- A document may be embedded only if content review passed AND rights explicitly allow
-- text mining, embedding and sending text to Cohere.
CREATE VIEW v_embedding_eligible_documents AS
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

-- A chunk may reach an answer only if its document passed the embedding gate, retrieval is approved,
-- the chunk itself is eligible, and its text may be sent to an external LLM (answer) and Cohere (rerank).
CREATE VIEW v_retrieval_ready_chunks AS
SELECT c.*, s.title AS source_title, s.source_url
FROM chunks c
JOIN v_embedding_eligible_documents d ON d.document_id = c.document_id
JOIN sources s       ON s.source_id = d.source_id
JOIN source_rights r ON r.source_id = d.source_id
WHERE c.retrieval_eligible
  AND d.approved_for_retrieval
  AND r.external_llm_processing_allowed IS TRUE;
