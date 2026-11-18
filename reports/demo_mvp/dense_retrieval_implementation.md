# Dense Retrieval Implementation — T2.5-DEV-1

**Status: DENSE_RETRIEVAL_READY_WITH_LIMITATIONS for the service-level research path.** The T2.3 service and adapter are reused and hardened. A real Top-5/Top-10 retrieval and the 66-query offline regression subsequently succeeded through the research reader. No HTTP API was added because the repository has no existing HTTP backend or routing framework; the task explicitly conditions an endpoint on existing architecture support.

## Reused baseline

- `DenseRetriever` in `app/retrieval/dense.py` remains the service entry point.
- `CohereQueryEmbedder` and `CachedQueryEmbedder` in `app/retrieval/query_embedding.py` preserve the configured `search_query` mode and offline cache behavior.
- `ResearchVectorReader` in `app/retrieval/research_reader.py` remains the only dense SQL reader.
- Existing profile: `dense_baseline_v1` → `cohere_embed_v4_1536_v1` → Cohere `embed-v4.0`, 1536 dimensions, cosine distance, Top-K default 10 and maximum 50.

## Changes made

- `app/retrieval/embeddings.py`: malformed successful provider JSON and non-object responses now produce a safe `invalid_response` error without exposing response content.
- `app/retrieval/query_embedding.py`: cached vectors must have the expected metadata and cache key; unreadable/malformed cache entries fail closed as `cache_invalid`; zero vectors are rejected.
- `app/retrieval/types.py`: added the typed `cache_invalid` error category.
- `app/retrieval/research_reader.py`: added `chunk_id ASC` as a deterministic tie-break after the unchanged cosine-distance ordering.
- `app/retrieval/dense.py`: malformed embedder vector counts and missing/duplicate chunk IDs now fail closed.
- Unit tests cover malformed provider JSON, malformed cache, zero vectors, duplicate result IDs, Top-K upper bound, and deterministic SQL ordering.

## API and live-query authorization

No `POST /api/retrieve` route was implemented. The repository has no existing HTTP server/router architecture; adding an unrelated server framework would create a new application surface outside the current backend. `DenseRetriever.retrieve(query, k)` is the reusable service-level interface.

Live Cohere query embedding remains disabled for arbitrary users. Previous approval covers research/test questions, not arbitrary demo-user text. Cache-only mode is fail-closed: a cache miss raises `embedding_unavailable`. A Cohere key being present in the environment is not authorization.

## Retrieval safety and response behavior

The reader uses only `asd_rag.v_research_retrieval_chunks`; checks the expected research reader login; uses a read-only transaction; binds vector, profile, and Top-K; and relies on C5 authorization predicates in the view before ranking/limit. Only cosine distance is supported. Results retain chunk/source/document IDs, title, URL, section, page/character location, content hash, model/profile, authorization version, and corpus version. Empty results return `no_results`. Distance/similarity are ranking signals, not confidence values.

## Remaining blockers

1. The earlier PostgreSQL connection timeout was transient; subsequent authenticated read-only access and retrieval succeeded. The exact transient cause is unknown, and Docker container health could not be inspected because Docker daemon access was denied.
2. No HTTP backend exists to host the requested endpoint.
3. Arbitrary user query transmission to Cohere is not authorized by the inspected records; cache misses remain unavailable.

No database writes, embedding writes, source/corpus changes, or T2.4-C changes were made.
