# Retrieval API Implementation — T2.5-DEV-3

**Status: `QUERY_EMBEDDING_BLOCKED` for uncached/new user queries.** The thin FastAPI endpoint is implemented and real retrieval works for an authorized evaluation query whose vector is already cached. The default API cannot embed arbitrary new query text and returns 503 on a cache miss.

## API

`POST /api/retrieve`

Request body:

```json
{"query": "Rối loạn phổ tự kỷ là gì?", "top_k": 5}
```

Success response includes `query`, `retrieval_method`, `embedding_model`, `top_k`, `result_count`, `results`, and `status`. Each result maps fields from the actual `RetrievedChunk`: `rank`, `chunk_id`, `source_id`, `document_title`, `section`, `page`, `content`, and `similarity` (`cosine_similarity`). It does not synthesize metadata or expose DB connection information, hashes, authorization IDs, or internal error text.

## Reuse and authorization

- The route calls the existing `DenseRetriever`.
- Its default app factory loads `dense_baseline_v1`, `CachedQueryEmbedder(inner=None)`, and `ResearchVectorReader`.
- Cache miss: `503 embedding_unavailable`; no Cohere fallback exists in the app.
- The research reader asserts `asd_rag_v2_research_reader`, uses read-only access and reads only `asd_rag.v_research_retrieval_chunks` with the existing profile/C5 filters.
- Empty, overlong, or invalid Top-K inputs are rejected. The configured Top-K range is 1–50.
- Similarity is a ranking value, not a probability/confidence score.

## Dependencies and files

- Added runtime dependencies: FastAPI, Uvicorn, and Pydantic v2 in `pyproject.toml`.
- Added `app/api.py`, a small route module that does not restructure the existing app.
- Added mocked route tests and one integration test using the actual research reader.
- FastAPI/Uvicorn packages were installed into the workspace `.venv` after the dependency installation request was approved. No model files or query text were sent to package providers.

Run locally on loopback only:

```powershell
.venv\Scripts\uvicorn.exe app.api:app --host 127.0.0.1 --port 8000
```

This task adds no Answer Generation, frontend, production path, or external embedding fallback.

## New-query limitation

The only compatible query encoder found is remote Cohere `embed-v4.0`; current authorization covers prior evaluation questions, not arbitrary demo-user text. Cached vectors cover the existing 66-question evaluation set and cannot encode novel text. A local BERT Tiny cache is incomplete and is not compatible with the Cohere document vector space. Therefore a successful cached q001 request does not meet the new-query end-to-end readiness condition.
