# T3.0 — Implementation Report (Student Demo MVP, Cache-Only)

**Final status: `DEMO_MVP_READY_CACHE_ONLY`** (scope: the 7 listed deliverables, in cache-only mode only —
see §6 for exactly what this does and does not cover).

## 1. What was actually implemented

1. **Demo authorization gates** (`app/config.py`): `ASD_DEMO_MODE` (default `true`),
   `ASD_ENABLE_LIVE_QUERY_EMBEDDING` / `ASD_ENABLE_LIVE_RERANKING` / `ASD_ENABLE_LIVE_LLM` (all default
   `false`). Setting any of the three live-provider flags to `true` raises `ConfigError` at import time —
   there is no code path that would use them to construct a live adapter, so "enabling" one cannot
   silently turn anything on; it can only fail the whole process loudly. This satisfies "must default to
   disabled" and "do not create a hidden bypass or silently enable a provider" at the same time.
2. **`POST /api/chat`** (`app/api.py`): the new demo chat endpoint. Calls the same `DenseRetriever` instance
   `/api/retrieve` already used (no second retrieval stack). Returns exactly the 8 required top-level
   fields: `status`, `answer`, `answer_mode`, `retrieval_status`, `evidence`, `citations`, `warnings`,
   `error`.
3. **`GET /api/system/status`** (`app/api.py`, new): reports the live values of the four flags above plus
   the active retrieval profile and the safety notice, so the frontend (and tests) can verify disabled
   state without hardcoding it.
4. **`MockAnswerGenerator`** (`app/answer/mock_answer.py`, new): builds a `[MOCK …]`-labeled answer string
   strictly from the evidence excerpts it is given. Empty evidence → explicit "insufficient evidence"
   text, no invented content. Every generated answer ends with the exact required safety sentence. No
   network call; no diagnosis/treatment language of any kind is generated (the text is excerpt + fixed
   disclaimer, nothing else).
5. **Frontend** (`frontend/index.html`, `style.css`, `app.js`, new, no build step): a static single page
   served by FastAPI itself via `StaticFiles` mounted at `/`, so one backend process serves both the API
   and the UI. Vietnamese labels, white background with teal accents, conversation panel, evidence/citation
   side panel, always-visible DEMO MODE / CACHE-ONLY badges (populated live from `/api/system/status`),
   the exact required safety notice banner, 6 suggested questions (5 real cached evaluation questions
   spanning different `query_category` values, plus one deliberately out-of-scope question to demonstrate
   the "insufficient evidence" / off-topic path), loading state, and a distinct error bubble style for
   blocked/error responses.
6. **Tests**: `tests/unit/test_mock_answer.py`, `tests/unit/test_chat_api.py`, `tests/unit/test_demo_config_gates.py`
   (new, mocked, no DB), and `tests/integration/test_chat_api_db.py` (new, real DB). See
   `t3_0_test_report.md` for execution results.

## 2. Exact files changed

**Modified:**
- `app/config.py` — added `_flag()`, `DEMO_MODE`, `ENABLE_LIVE_QUERY_EMBEDDING`, `ENABLE_LIVE_RERANKING`,
  `ENABLE_LIVE_LLM`, and the fail-loud guard.
- `app/api.py` — added `ChatRequest`, `CHAT_ERRORS`, `_chat_evidence`, `_chat_citations`,
  `_blocked_chat_response`, the `/api/chat` and `/api/system/status` routes, and the `StaticFiles` mount.
  `/api/retrieve` and `build_offline_retriever()` are unchanged.

**New:**
- `app/answer/__init__.py`, `app/answer/mock_answer.py`
- `frontend/index.html`, `frontend/style.css`, `frontend/app.js`
- `tests/unit/test_mock_answer.py`, `tests/unit/test_chat_api.py`, `tests/unit/test_demo_config_gates.py`
- `tests/integration/test_chat_api_db.py`

**Not changed:** anything under `app/retrieval/`, `app/ingest/`, `migrations/`, `config/*.json`,
`eval/datasets/`, `data/index/query_embeddings/` (cache read-only), any report from T2.3–T2.6.

## 3. Chat response contract (as actually returned)

Success (cached query, evidence found):
```json
{
  "status": "ok",
  "answer": "[MOCK — ...]\nTrích đoạn bằng chứng đã truy xuất...\nC1 ...\nNguyên mẫu nghiên cứu/sinh viên. ...",
  "answer_mode": "mock",
  "retrieval_status": "ok",
  "evidence": [
    {"citation_id": "C1", "source_id": "NIH-NIMH-ASD-2025", "title": "Autism Spectrum Disorder",
     "section": "What is autism spectrum disorder?", "page": null, "char_range": "1403-2750",
     "excerpt": "Autism spectrum disorder (ASD) is a neurological and developmental disorder...", "rank": 1}
  ],
  "citations": [{"citation_id": "C1", "source_id": "NIH-NIMH-ASD-2025", "title": "Autism Spectrum Disorder",
                  "locator": "1403-2750"}],
  "warnings": ["Nguyên mẫu nghiên cứu/sinh viên. Nội dung chưa được thẩm định lâm sàng. ..."],
  "error": null
}
```
(verified against the live research database with the query `"Rối loạn phổ tự kỷ là gì?"` during this task —
not a mocked example.)

Uncached query (HTTP 503):
```json
{"status": "blocked", "answer": null, "answer_mode": "none", "retrieval_status": "blocked_uncached",
 "evidence": [], "citations": [], "warnings": ["..."],
 "error": {"code": "QUERY_NOT_CACHED", "message": "Câu hỏi này chưa có vector truy vấn trong cache cục bộ ..."}}
```
(also verified live: a novel query string returned exactly this shape with HTTP 503.)

No synthetic or incompatible vector is ever generated: `CachedQueryEmbedder(inner=None)` raises
`RetrievalError("embedding_unavailable", …)` on a cache miss, which `/api/chat` maps 1:1 to this response —
the same fail-closed behavior `/api/retrieve` already had, just reshaped into the structured contract.

## 4. Safety/UX properties actually enforced in code (not just described)

- `MockAnswerGenerator` only ever reads from the `evidence` list passed to it — there is no code path by
  which it could reference chunk text that was not already returned, validated, and provenance-checked by
  `DenseRetriever`.
- Internal fields (`chunk_id`, `content_sha256`, `authorization_version`, `embedding_profile`, `model_id`,
  `corpus_version`, raw cosine score) are never placed into the chat response — `_chat_evidence` only reads
  `citation_id`/`source_id`/`title`/`section`/`page`/`char_range`/`excerpt`/`rank` off the already-validated
  `RetrievedChunk`.
- No database credential, connection string, or local file path is ever placed in a response — every chat
  error message is a fixed Vietnamese string from `CHAT_ERRORS`, never `str(exception)`.
- No conversation text is persisted server-side: `build_offline_retriever()` still passes `log=None` to
  `DenseRetriever` (unchanged), so no retrieval log file is written by the demo path. The frontend keeps
  message history only in the page's in-memory DOM; it uses no `localStorage`/`sessionStorage` and sends no
  data anywhere except same-origin `fetch()` calls to this backend.
- `/api/system/status` and the startup-time `ConfigError` guard make the "all live providers disabled"
  claim independently checkable rather than asserted — see `test_system_status_reports_all_live_providers_disabled`
  and `test_enabling_a_live_provider_flag_fails_loudly_instead_of_silently_enabling` in the test suite.

## 5. How to run it

See `demo_user_guide.md` for the exact PowerShell commands. Summary: one `uvicorn` process serves both
`/api/*` and the static frontend at `http://127.0.0.1:8000/`; no separate frontend server or build step is
needed because the frontend is plain HTML/CSS/JS with no bundler.

## 6. Scope boundary — what `DEMO_MVP_READY_CACHE_ONLY` means here

Ready for: demonstrating the real retrieval pipeline (real embeddings already in the database, real
cosine search, real evidence with real citations) over the 66 pre-cached evaluation questions (or any
other text whose vector is manually added to the cache the same way), with a clearly-labeled mock answer
and a clean fail-closed path for anything else.

Not ready for, and not attempted: free-text queries outside the cache (blocked by design, pending T2.6),
a real AI-generated answer (explicitly out of scope — mock only), reranking, or any external LLM step.

## 7. Confirmation: all live external services remain disabled

- No Cohere API call was made at any point during this task (query embedding, document embedding, or
  otherwise) — confirmed by inspection of the code path (`inner=None` throughout) and by the chat
  endpoint's own observed behavior (uncached query → 503, not a live call).
- No reranking code exists or was added.
- No external LLM call exists or was added; `MockAnswerGenerator` makes no network request.
- `ENABLE_LIVE_QUERY_EMBEDDING` / `ENABLE_LIVE_RERANKING` / `ENABLE_LIVE_LLM` are `false` by default and
  verified `false` via `/api/system/status` in a live test run (§ test report).
- No row was written to the production database; the research-reader connection is read-only
  (`conn.read_only = True`, unchanged, asserted by `ResearchVectorReader`).
- No `git` command was run (the workspace is not a Git repository).
