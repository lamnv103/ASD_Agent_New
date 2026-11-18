# Dense Retrieval Run Guide — T2.5-DEV-1

## Current operating limits

- Research only. The configured reader is `asd_rag_v2_research_reader`, and the only allowed source is `asd_rag.v_research_retrieval_chunks`.
- Do not enable arbitrary live Cohere query embedding until the project owner explicitly authorizes that data flow and resolves the provider terms/data-handling questions recorded in `docs/provider_terms/cohere_2026-11-14.md`.
- Cache-only query embedding is the safe default. A cache miss fails closed; do not add an implicit API fallback.
- There is no HTTP route in this repository. `DenseRetriever.retrieve(query, k)` is a Python service method, not `POST /api/retrieve`.
- The prior connection attempt timed out, but subsequent diagnostics and real retrieval succeeded with the research reader. The exact transient cause is unknown; Docker container status could not be inspected because Docker daemon access was denied.

## Offline evaluation command

Run from the repository root after confirming the research database is available:

```powershell
.venv\Scripts\python scripts\dense_retrieval_eval.py `
  --metrics-out reports\demo_mvp\dense_retrieval_metrics.json `
  --pool-out reports\demo_mvp\dense_retrieval_pool.csv
```

The command uses the 66-query dataset and the local query-vector cache by default. It must fail before external calls if a vector is missing. Do not pass `--allow-api` for arbitrary user queries under the current approval state. The output paths must not already exist; the script refuses to overwrite them. The command reads through the research reader and writes evaluation artifacts/logs locally.

## Service-level construction

For a known query with a pre-existing matching cache entry, construct the service without a Cohere inner embedder:

```python
from app.retrieval.dense import DenseRetriever
from app.retrieval.query_embedding import CachedQueryEmbedder
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalProfile
from app.retrieval.embeddings import EmbeddingProfile

retrieval_profile = RetrievalProfile.load("dense_baseline_v1")
embedding_profile = EmbeddingProfile.load(retrieval_profile.embedding_profile)
query_embedder = CachedQueryEmbedder(
    embedding_profile, retrieval_profile.query_cache_dir, inner=None
)
retriever = DenseRetriever(
    retrieval_profile, query_embedder, ResearchVectorReader(retrieval_profile)
)
response = retriever.retrieve("<query already present in the approved cache>", k=5)
```

Do not print or log the raw query, credentials, or provider body. Handle `RetrievalError` by returning a fail-closed error to the caller. Use only `response.results` as retrieved evidence; do not interpret similarity as a probability. This service example is not an HTTP API implementation.

## Before enabling a demo endpoint

1. Obtain explicit authorization for external processing of arbitrary user query text, or provide an approved local query embedder.
2. Establish an existing HTTP backend/API convention and implement the route there; do not assume this repository already has one.
3. Restore database connectivity and verify the current session identity, read-only status, view access, and C5 filtering using the research reader.
4. Run a real Vietnamese query through the service and validate ordering, ranks, unique chunk IDs, finite cosine scores, empty results, and source provenance.
5. Run the 66-query offline regression with unique output paths and compare it with the frozen T2.3 baseline without changing labels or tuning retrieval parameters.
6. Keep the API research-only. Production retrieval needs separate rights/content approvals and a different authorized gate.
