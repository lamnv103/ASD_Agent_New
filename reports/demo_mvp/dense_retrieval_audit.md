# Dense Retrieval Integration Audit — T2.5-DEV-1

**Audit phase:** complete; no implementation files were changed during inspection.

## Reusable implementation

- `app/retrieval/embeddings.py` — shared Cohere Embed v2 client; profile-based payload; retries with bounded timeout; checks response count, dimension, numeric finiteness and non-zero vectors; error messages avoid returning provider bodies, query text, or API keys.
- `app/retrieval/query_embedding.py` — `CohereQueryEmbedder` selects `search_query`; `CachedQueryEmbedder` uses a SHA-256 cache keyed by profile/model/dimension/input type/text and can be constructed without an online embedder to fail closed on cache misses.
- `app/retrieval/dense.py` — T2.3 `DenseRetriever`, query and Top-K validation, vector retrieval, response/provenance checks, result metadata, and hash-only local audit events.
- `app/retrieval/research_reader.py` — fixed SQL over the authorized view, bound query-vector/profile/Top-K parameters, research reader login assertion, read-only transaction, and fail-closed database errors.
- `app/retrieval/types.py`, `app/retrieval/audit_log.py`, `app/db.py`, and `app/config.py` — typed response/error contract, query-hash-only local logging, role-specific connections and environment-backed settings.
- `config/embedding_profiles.json` and `config/retrieval_profiles.json` — existing baseline profiles.
- `scripts/dense_retrieval_eval.py` — original 66-query baseline evaluation, offline from the query vector cache unless an explicit API flag is supplied.

## Architecture and request flow

```text
query → CachedQueryEmbedder (offline by default) → DenseRetriever
      → ResearchVectorReader → asd_rag.v_research_retrieval_chunks
      → validated, ranked chunks + provenance
```

The repository contains Python application/core modules and CLI evaluation scripts. Inspection found no HTTP backend, API router, FastAPI, Flask, or Starlette dependency/route. Therefore there is no existing HTTP architecture into which `POST /api/retrieve` can be integrated without introducing a new server framework. `DenseRetriever.retrieve()` is the current service-level entry point.

## Database view and columns

The configured and allowlisted view is `asd_rag.v_research_retrieval_chunks`. `ResearchVectorReader.COLUMNS` reads:

`chunk_id`, `source_id`, `document_id`, `title`, `source_url`, `section_heading`, `section_path`, `page_start`, `page_end`, `char_start`, `char_end`, `content`, `content_sha256`, `chunking_profile`, `document_version`, `authorization_id`, `profile_code`, `model_id`, and `vector_dimension`; it also selects the computed `distance` from `embedding <=> query_vector`.

The reader filters by `profile_code`, orders by pgvector cosine distance, and applies the bound `LIMIT`. View-side C5 predicates enforce active research authorization, non-production scope, exact allowlist and hashes, current/non-quarantined documents, eligible verified chunks, matching source/document provenance, model and 1536-dimension consistency. The SQL builder rejects other views and metrics.

## Embedding configuration

- Provider/model: Cohere `embed-v4.0`.
- Vector dimension: 1536 float coordinates.
- Document input: `search_document`; query input: `search_query`.
- Metric: cosine distance (`<=>`); lower distance ranks first. Reported similarity is `1 - distance` and is a ranking signal, not a probability.
- Query preprocessing: trimmed original Vietnamese text; no expansion.
- Existing evaluation cache: 66/66 queries in `eval/datasets/retrieval_eval_v1.jsonl` have cached vectors for the configured profile. This was checked by cache-key lookup; no query was sent to Cohere.

## Authorization and privacy safeguards

- DB profile uses `research_reader`, expects user `asd_rag_v2_research_reader`, and allows only the research view. Connection code sets the transaction read-only and verifies `current_user`; the database role is documented as SELECT-only on that view with view-side authorization filters.
- `docs/research_retrieval_access.md` documents research-only access. This is not production access; production retrieval remains blocked.
- `docs/provider_terms/cohere_2026-11-14.md` documents a Cohere trial key and unresolved data-handling/terms questions. `eval/reports/embedding_run_report.md` covers only prior approved research/test query questions, not arbitrary demo users' queries.
- There is no evidence in the inspected approval records authorizing arbitrary user query text to be sent to Cohere. Live query embedding must remain disabled. Offline cache hits can be used; cache misses must fail closed. Do not rely on the presence of `COHERE_API_KEY` as authorization.
- The API key's value was not inspected or printed.

## Existing tests and evaluation

- Unit coverage: `tests/unit/test_dense_retrieval.py`, `tests/unit/test_embeddings.py` and adjacent tests cover query/Top-K validation, profile/model/dimension checks, SQL/view restrictions, read-only role assertion, database failure mapping, response ordering/metadata, cache behavior, Cohere payload and malformed vector handling.
- Integration coverage: `tests/integration/test_dense_retrieval_db.py` uses the research reader for real view access and cosine-ranking comparison; one exclusion fixture reads a vector via the owner role. That test suite will not be run as part of this task because the requested service path must not use an administrative account.
- Baseline evaluation: 66-question `retrieval_eval_v1.jsonl`; original evaluation labels are silver and will not be changed.

## Incomplete areas and risks found

1. No HTTP framework or existing route exists, so no HTTP endpoint can be reused in the current architecture.
2. Existing Cohere integration is callable, but permission to send arbitrary user queries is absent/unclear. Live embed requests cannot be enabled.
3. Malformed non-JSON Cohere success responses and malformed query-cache JSON are not consistently normalized into the typed fail-closed errors.
4. SQL orders only by cosine distance; exact ties do not have an explicit deterministic secondary key.
5. Dense result validation does not explicitly reject duplicate `chunk_id` values returned by a reader.
6. Query-vector validation checks dimension and finite numeric coordinates but does not reject zero vectors for cache-provided values.
7. Real DB availability and the current reader's live authorization have not yet been checked in this audit phase.

## Current audit conclusion

The T2.3 dense service and adapter are reusable, and the existing evaluation set can run without external embedding calls. General live demo queries are blocked by unresolved external processing authorization. HTTP API availability, database connectivity, malformed-response handling, tie ordering, and duplicate-result checks require follow-up before any `DENSE_RETRIEVAL_READY` conclusion.
