# T3.0 — Test Report (Student Demo MVP, Cache-Only)

Every result below was actually executed during this task on 2026-11-17, against the real `.venv` and the
real PostgreSQL container (`asd-rag-v2-db`, already running, not started by this task). Nothing here is
claimed without a command and its output.

## 1. Full unit suite (mocked embedder/reader, no DB, no network)

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q
```
Result: **294 passed, 44 deselected** (the 44 deselected are the `integration`-marked tests, run separately
below). 0 failed.

Includes the new files:
- `tests/unit/test_mock_answer.py` (4 tests) — mock label present, disclaimer present, no invented
  citations beyond given evidence, insufficient-evidence case stated explicitly, long excerpts truncated
  without losing the citation.
- `tests/unit/test_chat_api.py` (13 tests) — cached query → real evidence + labeled mock answer; uncached
  query → 503 `QUERY_NOT_CACHED` with no synthetic vector; database-unavailable fails closed; empty-result
  handled safely with an explicit insufficient-evidence warning; empty/overlong query rejected (422);
  invalid `top_k` rejected (422) for `0, -1, 51, 2.5, "5", True`; duplicate chunk IDs fail closed (502);
  citations map 1:1 to evidence in order; default app has no external embedder and blocks cache misses;
  `/api/system/status` reports every live provider disabled; the static frontend is served at `/`.
- `tests/unit/test_demo_config_gates.py` (5 tests) — defaults are demo-on/providers-off; each of the three
  live-provider flags fails loudly (raises) instead of silently enabling anything when set `true`; demo
  mode can be toggled independently of the provider flags.

## 2. Full integration suite (real database, real cache, no network/Cohere calls)

```
.venv\Scripts\python.exe -m pytest -m integration -q
```
Result: **44 passed, 294 deselected**. 0 failed. This includes the pre-existing dense-retrieval, FTS,
database-gate, research-embedding, and research-retrieval-access integration tests (all unaffected by this
task) plus the two new tests in `tests/integration/test_chat_api_db.py`:
- `test_cached_question_returns_real_evidence_and_mock_answer` — `POST /api/chat` with the real cached
  question `"Rối loạn phổ tự kỷ là gì?"` against the real research-reader connection: 200, 5 real evidence
  items with distinct citation ids, every item has a non-empty `source_id`/`excerpt`, citations map 1:1 to
  evidence.
- `test_uncached_question_returns_503_query_not_cached` — a novel string against the real app: 503,
  `error.code == "QUERY_NOT_CACHED"`.

## 3. Manual live verification (ad hoc, in addition to the automated suites)

Run directly against `create_app()` (the real default app, real DB, real cache) during this task:

| Check | Command/request | Result |
|---|---|---|
| System status reports all providers disabled | `GET /api/system/status` | `{"demo_mode": true, "live_query_embedding_enabled": false, "live_reranking_enabled": false, "live_llm_enabled": false, "retrieval_profile": "dense_baseline_v1", ...}` |
| Cached query returns real evidence + mock answer | `POST /api/chat {"query": "Rối loạn phổ tự kỷ là gì?", "top_k": 3}` | HTTP 200; 3 real evidence items from `NIH-NIMH-ASD-2025` / academic sources; answer text begins with `[MOCK — ...]` and ends with the exact safety sentence |
| Uncached query blocked, no synthetic vector | `POST /api/chat {"query": "một câu hỏi hoàn toàn mới chưa từng có trong cache 12345", "top_k": 3}` | HTTP 503; `error.code == "QUERY_NOT_CACHED"` |
| Frontend served from the same process | `GET /` | HTTP 200, `content-type: text/html; charset=utf-8` |

## 4. Lint

```
.venv\Scripts\ruff.exe check app tests
```
Result: **All checks passed!** (One `RUF043` finding on a regex `match=` string in the new config-gate test
was found and fixed — raw string used — before this final run.)

## 5. T2.3 regression (66/66 preserved)

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch>\metrics.json --pool-out <scratch>\pool.csv
```
Result: `questions_total: 66`, `cache_hits: 66`, `cache_misses: 0`, `calls: 0` (0 Cohere API calls) — same
as the recorded baseline `reports/demo_mvp/dense_retrieval_regression_metrics.json`. A field-by-field diff
against that recorded baseline found differences **only** in `generated_at` (timestamp), `log_file`
(timestamped log filename), and the four latency numbers (wall-clock timing noise) — every ranking,
recall/nDCG/MRR, cache-hit, and dimension/norm figure is byte-identical. Scratch output files and the new
log file created by this run were deleted afterward; the recorded baseline file
(`dense_retrieval_regression_metrics.json`) was not overwritten.

## 6. Frontend

No JavaScript test framework or bundler exists in this project (confirmed in the T3.0 preflight), and none
was added — the frontend is plain HTML/CSS/JS with no build step, so there is no "frontend build" to run.
It was exercised manually in the sense that `GET /` was verified to serve it (HTTP 200, correct
content-type) from the same backend process that was used for the live `/api/chat` checks above; the actual
rendered page in a browser was not captured as part of this automated run.

## 7. What was not run and why

- No live Cohere call was made (prohibited by T2.6/T2.3.6 scope and not needed: `calls: 0` in the
  regression run above already demonstrates this).
- No reranking or external-LLM test was run — neither exists in the codebase to test.
- Docker was not started or restarted by this task (it was already running); no Docker-lifecycle test was
  performed.

## 8. Summary

| Suite | Passed | Failed | Deselected |
|---|---:|---:|---:|
| Unit (`-m "not integration"`) | 294 | 0 | 44 |
| Integration (`-m integration`) | 44 | 0 | 294 |
| Lint (`ruff check app tests`) | — | 0 findings | — |
| T2.3 regression | 66/66 cache hits, ranking identical | — | — |

All numbers above were produced by actually running the listed commands during this task, not estimated.
