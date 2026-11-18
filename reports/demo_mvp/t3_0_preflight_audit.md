# T3.0 — Preflight Audit (Student Demo MVP, Cache-Only)

Read-only inspection performed before any code was written for T3.0. No file was changed while producing
this report.

## 1. Authorization state carried over from T2.6

- `reports/demo_mvp/t2_6_cohere_license_review.md`, `t2_6_authorization_decision_matrix.md`,
  `t2_6_approval_request.md`: final status **`APPROVAL_REQUIRED`**. No scenario authorizing live Cohere
  query embedding, live reranking, or external LLM processing has been approved. This audit treats that
  as still true; T3.0 does not re-decide it.
- Consequence for T3.0: the demo must run entirely on already-cached query vectors and real retrieval
  results; any uncached query must fail closed, not be faked.

## 2. Existing retrieval stack (reused as-is, not reimplemented)

| Component | File | Role |
|---|---|---|
| HTTP API | `app/api.py` | `POST /api/retrieve`; builds a `DenseRetriever` with `CachedQueryEmbedder(inner=None)` — already cache-only, already fails closed on cache miss with `embedding_unavailable` → HTTP 503. |
| Dense retrieval service | `app/retrieval/dense.py` | `DenseRetriever.retrieve()`: validates query/`top_k`, embeds, searches, validates provenance of every returned row (duplicate IDs, missing metadata, cross-authorization mixing, out-of-range distance all raise `RetrievalError`). |
| Query embedding | `app/retrieval/query_embedding.py` | `CachedQueryEmbedder` (sha256-keyed on-disk cache, vectors+hashes only, never raw query text) and `CohereQueryEmbedder` (not wired as `inner` anywhere in the app). |
| Database access | `app/retrieval/research_reader.py` | `ResearchVectorReader`: connects only as `asd_rag_v2_research_reader`, asserts `current_user`, sets `read_only = True`, runs one fixed parameterized SQL statement against the allowlisted view `asd_rag.v_research_retrieval_chunks`, maps every psycopg error to a typed `RetrievalError`. |
| Contracts | `app/retrieval/types.py` | `RetrievalError` (closed category set), `RetrievalProfile`, `RetrievedChunk`, `RetrievalResponse`. Docstring explicitly: internal ids/scores "must not show them" to a user-facing answer. |
| Config | `app/config.py` | `ROOT`, DB role credentials from `.env`, no demo/feature-flag mechanism existed before this task. |

**Decision: do not recreate any of the above.** T3.0 only adds a new route (`/api/chat`), a new mock-answer
module, demo authorization-gate flags, and a frontend — all composed on top of the existing, already-tested
retrieval stack.

## 3. What did not exist yet

- No `/api/chat` or any structured chat-style response contract — only the raw `/api/retrieve` passthrough.
- No answer-generation module: `app/answer/` contained only a `.gitkeep`.
- No frontend of any kind (`grep` for `.html`/`.tsx`/`.jsx`/"frontend" across the repo found nothing besides
  raw source-document snapshots under `data/raw/`).
- No demo-mode / live-provider feature flags in `app/config.py`.
- No test coverage for any of the above (none existed to find).

## 4. Existing tests inspected (to match conventions, not duplicate them)

- `tests/unit/test_retrieval_api.py` — HTTP contract tests for `/api/retrieve` using `FakeEmbedder`/`FakeReader`
  mocks (fast, no DB). New chat-endpoint tests in `tests/unit/test_chat_api.py` reuse the same fakes and the
  same request/row-building helpers, by design.
- `tests/integration/test_retrieval_api_db.py` — one real-DB smoke test using cached evaluation query `q001`.
  A matching `tests/integration/test_chat_api_db.py` was added for `/api/chat`.
- `tests/unit/test_dense_retrieval.py`, `test_embeddings.py` — cover the lower layers already; untouched.

## 5. Dataset and cache state (read-only checks)

- `eval/datasets/retrieval_eval_v1.jsonl`: 66 questions, each with an exact `question_vi` string used to
  build the on-disk cache key (`scripts/dense_retrieval_eval.py:125`: `r["question_vi"].strip()`).
- `data/index/query_embeddings/`: 66 cached vector files — one per evaluation question, confirmed by file
  count before any change.
- `reports/demo_mvp/dense_retrieval_regression_metrics.json`: existing baseline records
  `"cache_hits": 66, "cache_misses": 0, "calls": 0"` — i.e. the current 66-question regression already runs
  with zero Cohere calls. This is the number T3.0 must not regress.

## 6. Environment checks

- Python 3.12.4, `.venv` has FastAPI 0.163.1, Starlette 1.10.0 (includes `StaticFiles`, usable for the
  frontend with no new dependency), Pydantic 2.14.3, psycopg 3.3.9 — all already present from the T2.5
  retrieval-API work. No new package was installed for T3.0.
- `docker ps` shows `asd-rag-v2-db` already **Up (healthy)** on `127.0.0.1:5433`. Docker was not started by
  this task; it was already running when the audit began.
- `.venv/Lib/site-packages` still has no `torch`/`transformers`/`sentence_transformers`/`onnxruntime`/
  `fastembed`/Cohere SDK, consistent with the T2.5 finding — no local encoder exists to accidentally fall
  back to.

## 7. Conclusion

The retrieval, embedding-cache, and database layers are reusable without modification. T3.0's work is
additive: a chat-shaped endpoint over the existing `DenseRetriever`, a mock-answer generator, explicit
authorization-gate flags that default to (and enforce) disabled, and a static frontend. Proceeding to
implementation under the constraints in `t2_6_authorization_decision_matrix.md` Scenario A (cache-only).
