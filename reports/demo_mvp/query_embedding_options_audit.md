# Query Embedding Options Audit — T2.5-DEV-3

**Audit conclusion: `QUERY_EMBEDDING_BLOCKED` for new arbitrary user queries.** No locally available, compatible query encoder or explicit authorization for live Cohere queries was found. No query was sent externally and no model was downloaded.

## Options inspected

| Option | Provider/model | Dimension | Query/document compatibility | Local files/runtime | External transfer | Authorization | Limitation |
|---|---|---:|---|---|---|---|---|
| Existing Dense baseline adapter | Cohere `embed-v4.0`, profile `cohere_embed_v4_1536_v1` | 1536 | Compatible profile: documents use `search_document`; queries use `search_query`; exact same provider/model/profile | Adapter and profile exist. No model weights are local; inference is remote. | Yes, sends query text to Cohere on cache miss. | Existing records document prior research/evaluation questions only. No approval for arbitrary demo-user queries found; trial data terms remain unresolved. | Do not enable for arbitrary new queries until explicit authorization and data-handling review. |
| Existing query-vector cache | Vectors generated for Cohere `embed-v4.0` with `search_query` | 1536 | Exact compatibility for the cached texts/profile only | `data/index/query_embeddings/` contains cached vectors, not a model. The current evaluation dataset has 66/66 cache hits. | No transfer on cache hit. | Existing evaluation cache is available for the approved evaluation set. | Cannot encode a new query; cache misses fail closed. A cache hit does not establish support for arbitrary queries. |
| Hugging Face cache `prajjwal1/bert-tiny` | BERT Tiny checkpoint | Config lists hidden size 128; no usable model type/architecture metadata found | No repository implementation for query/document pooling or shared dense encoding; not the Cohere document encoder and not demonstrated compatible with the stored vectors | A cache directory exists, but only a small config/tokenizer metadata set was found; no model weights. `transformers` and PyTorch are absent. | No, if complete local inference were available. | No approval/model selection for retrieval use found. | Not a sentence-embedding model in this project; dimension and vector space differ. Matching dimensions would not establish compatibility. |
| Other local embedding model/runtime | None found | — | — | No local model files in workspace; no `sentence-transformers`, `transformers`, PyTorch, ONNX Runtime, FastEmbed, or Cohere SDK in `.venv` | — | — | No candidate. No model was downloaded. |
| Other approved embedding service | None found | — | — | No adapter/config discovered beyond the Cohere baseline | Depends on provider | No explicit authorization discovered | No usable option. |

## Application/deployment audit

- Existing adapters: `app/retrieval/query_embedding.py` provides `CohereQueryEmbedder` and `CachedQueryEmbedder`; `app/retrieval/embeddings.py` implements the remote Cohere client.
- Existing HTTP backend: none found. No route, FastAPI, Starlette, Flask, or Uvicorn dependency was present in `pyproject.toml` or `.venv`.
- Deployment: current configuration is PostgreSQL-focused; no app service or web-server container is defined.
- At audit time, FastAPI/Uvicorn were absent from `.venv`; a minimal module could be added without restructuring the existing core. The initial sandbox package install was blocked (`WinError 10013`).

Implementation follow-up: FastAPI, Uvicorn, and Pydantic v2 were added as project dependencies and installed into the workspace `.venv` after the package network operation was approved. A minimal route was then exercised over loopback. This does not change the embedding-option decision: arbitrary uncached queries still have no authorized compatible encoder.

## Authorization evidence and decision

`eval/reports/embedding_run_report.md` states the previous Cohere query input was test questions and cached them for offline reruns. `docs/provider_terms/cohere_2026-11-14.md` records a trial key and unresolved terms/data-handling issues. Neither authorizes arbitrary demo-user query text. The presence of an API key in environment configuration is not authorization and was not inspected or printed.

Therefore the implementation must use `CachedQueryEmbedder` with no remote inner embedder. Existing cached evaluation texts can retrieve; uncached queries must return an explicit unavailable error. A successful retrieval for q001 is not evidence that a new query can be embedded. The task's new-query end-to-end readiness condition remains unmet.
