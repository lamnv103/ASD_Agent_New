# Phase 6 — End-to-End Testing & Regression

All commands below were actually executed during this task; results are copied from real output.

## 6.1 — Intent routing tests

`tests/unit/test_intent_classifier.py` (15 tests) + live verification via `TestClient` for: greeting,
thanks, information lookup (ASD definition), ASD symptoms, age-specific question, medication question,
out-of-scope question, mixed-intent question. All passed. See `phase_1_intent_routing.md` for the specific
cases and the live-call results table.

## 6.2 — Retrieval tests (the 22-question set from the independent expert evaluation, re-run live)

Re-ran all 4 previously-confirmed failure cases plus the weather/greeting cases plus the standard-question
baseline, against the real database, after all Phase 1–4 code was in place:

| Case | Before (independent_expert_evaluation.md) | After (this task, live) |
|---|---|---|
| Vaccine | `retrieval_status: "ok"`, Top-5 shown as if all usable, no flag that most of it was off-topic | `retrieval_status: "ok"`, **but only the 1 chunk that actually discusses vaccination is kept and cited**; answer states the vaccine-autism claim traces to a retracted study |
| Risperidone dosing | `retrieval_status: "ok"` with unrelated sleep-medication evidence shown as if usable | `answer_mode: "safety_refusal_dosing"`, evidence empty, user told to consult a doctor |
| Stem cells | `retrieval_status: "ok"` with unrelated evidence | `answer_mode: "safety_caution_unproven_cure"`, evidence empty, explicit "not enough evidence" caution |
| Epilepsy comorbidity | `retrieval_status: "ok"` with unrelated anxiety/ADHD evidence | `retrieval_status: "insufficient_evidence"`, evidence empty, explicit statement that there isn't enough evidence — no fabricated comorbidity rate |
| Weather | `retrieval_status: "ok"` with 5 unrelated ASD chunks | `retrieval_status: "out_of_scope"`, never reaches the database |
| Greeting | `503 QUERY_NOT_CACHED` (routed through embedding/retrieval) | `retrieval_status: "skipped_greeting"`, never reaches the embedder or database |
| Standard questions (definition, DSM-5, screening age, ABA) | Retrieval "ok" but evidence included off-topic padding (e.g. comorbidity/tic text for the definition question) | Evidence Gate narrows to only the topically-supporting chunks; grounded Vietnamese templates produced for all four |

## 6.3 — Answer tests

Each of the live cases above was inspected against: correctness (template text matches what the
underlying evidence actually says — manually cross-checked against the retrieved excerpts, see
`phase_3_answer_generation.md`), relevance (Evidence-Gate-filtered, not raw Top-K), completeness (short
templates match the task's "1–2 short paragraphs" format for definitions), conciseness (templates are
1–3 sentences, not chunk dumps), Vietnamese clarity (hand-written Vietnamese, not machine-translated
excerpt text), evidence grounding (every template requires its trigger source to be present), citation
accuracy (Phase 4 validation + narrowing to actually-cited sources), safety (dosing/unproven-cure
overrides). This is a direct inspection of real output, not a numeric LLM-judge score — no such judge is
authorized or built.

## 6.4 — Regression tests (T2.3, mandatory)

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch> --pool-out <scratch>
```
Result: **66/66 cache hits, 0 cache misses, 0 Cohere API calls** — field-by-field identical to the
recorded baseline `reports/demo_mvp/dense_retrieval_regression_metrics.json` except for the timestamp, the
timestamped log filename, and wall-clock latency numbers (expected, non-deterministic fields). This run
was executed **after** all Phase 1–4 code changes, confirming the new router/gate/answer-generator/
citation layers — none of which touch `app/retrieval/dense.py`, `embeddings.py`, `query_embedding.py`, or
`config/embedding_profiles.json` — leave the benchmark byte-for-byte unaffected. Scratch output files and
the generated log file were deleted after comparison; the recorded baseline file was not modified.

## 6.5 — System tests

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q   -> 343 passed, 48 deselected
.venv\Scripts\python.exe -m pytest -m integration -q         -> 48 passed, 343 deselected
.venv\Scripts\ruff.exe check app tests                         -> All checks passed!
```

Breakdown of what the 343+48 = 391 tests actually cover (new test files from this task in **bold**):

| File | Tests | Covers |
|---|---:|---|
| **`tests/unit/test_intent_classifier.py`** | 15 | Phase 1 routing |
| **`tests/unit/test_evidence_gate.py`** | 11 | Phase 2 gate |
| **`tests/unit/test_answer_generator.py`** | 7 | Phase 3 generation |
| **`tests/unit/test_citation_validation.py`** | 6 | Phase 4 validation |
| `tests/unit/test_chat_api.py` (rewritten) | 22 | `/api/chat` HTTP contract end-to-end, with the fakes using realistic ASD-domain query text |
| `tests/integration/test_chat_api_db.py` (rewritten) | 6 | Real DB: definition template + links, vaccine evidence, risperidone refusal, weather rejection, greeting skip, uncached 503 |
| All pre-existing T2.3/T2.5/T3.0 suites | 324 | Unaffected; all still pass |

Cache hit / cache miss / read-only-DB / error-handling / Evidence-Gate / greeting-routing / provider-
authorization-gate behaviors are each covered by at least one of the above and were also exercised live
via direct `TestClient` calls during development (see the phase reports for the literal request/response
pairs).

## Bugs found and fixed during testing (disclosed, not hidden)

1. Router ran *before* input validation, so an empty/oversized query or an out-of-range `top_k` silently
   became a 200 "out_of_scope" response instead of the required 422 — fixed by validating via
   `DenseRetriever.validate_query`/`validate_k` first, classifying second.
2. A test-only `"thời tiết"` glossary entry leaked into the router's domain-signal check, which would have
   let the weather question reach the database anyway (the gate still caught it, but the router was
   supposed to short-circuit first) — removed.
3. `chunk_matches_terms` only checked chunk body text, missing topic signals that live in the title/section
   heading (e.g. "Signs and Symptoms of ASD") — fixed to check title + section + content together.
4. Short greeting words ("hi") and short glossary terms matched as raw substrings inside unrelated words
   (e.g. "hi" inside "nhiêu", "thích") — fixed with word-boundary matching (`contains_word`).
5. The `extractive_fallback` answer text printed bare `"C1 ..."` codes in the prose, violating the task's
   explicit "no C1/C2/C3" rule just as directly as the old Mock format did — fixed to a plain numbered
   list.
6. A test-helper bug (`tests/unit/test_chat_api.py`'s `make_row`) computed `content_sha256` from the
   *default* content before an override replaced `content`, causing a real (and correctly caught)
   provenance-hash mismatch in one new test — fixed in the test helper, not in production code.

## Not run

No browser-based visual test (no tooling exists for this, per Phase 5). No live Cohere/LLM/reranking call
of any kind (none is authorized; this was verified, not merely assumed, by `/api/system/status` returning
all three flags `false` throughout, and by `config.py` raising `ConfigError` if any is set `true`).
