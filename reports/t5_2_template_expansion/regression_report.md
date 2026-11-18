# T5.2 Phase F — Regression Report

All commands below were actually executed during this task, after every code change, on the real
database (research-reader role, read-only).

## Full suite (final run)

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q   -> 393 passed, 50 deselected
.venv\Scripts\python.exe -m pytest -m integration -q         -> 50 passed, 393 deselected
.venv\Scripts\ruff.exe check app tests                         -> All checks passed!
```

443 total tests, 0 failures. New this task: 10 (evidence normalization) + 5 (q033 isolation) + 10
(negative/diacritic cases) + 2 (integration: new templates + q033 live) + 7 (old-template-collision
regression) + 5 (new-template firing, in `test_answer_generator.py`) = 39 new tests; the rest are
pre-existing T2.3–T4 suites, unaffected.

## T2.3 regression

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch> --pool-out <scratch>
```
Run **twice** during this task (after the template additions, and again after the collision fix), both
times: **66/66 cache hits, 0 misses, 0 Cohere calls**, field-by-field identical to
`reports/demo_mvp/dense_retrieval_regression_metrics.json` except timestamp/log-filename/latency. Neither
`app/retrieval/dense.py`, `embeddings.py`, `query_embedding.py`, nor any embedding config was touched —
by construction, this script (which calls those modules directly, never `app/answer/*`) cannot see any
T5.2 change.

## T2.6 authorization gates

Re-confirmed unchanged: `app/config.py` still raises `ConfigError` if any `ASD_ENABLE_LIVE_*` flag is set
`true`; `grep` of `app/answer/evidence_normalization.py` and the new template code shows no network
client import, no Cohere/LLM call. `ASD_DEMO_MODE` default unchanged.

## The 18 permitted questions (not used alone to claim generalization)

Covered by `tests/integration/test_chat_api_db.py::test_new_t5_2_template_examples_get_real_vietnamese_
answers_with_valid_citations` (6 of the 11 templated questions, spot-checked live) plus
`tests/unit/test_answer_generator.py`'s mocked-evidence tests for all 10 templates. Per the task's
explicit instruction, these are **not** treated as sufficient on their own — see the independent sets
below.

## Independent negative/regression test sets (Phase F's explicit requirement)

- `tests/unit/test_template_negative_cases.py` (10 tests): different queries and source combinations
  than the 18 permitted questions, checking templates do **not** fire on keyword presence alone without
  the matching source, and vice versa; 2 diacritics-robustness tests confirm identical behavior with and
  without Vietnamese diacritics.
- `tests/unit/test_q033_isolation.py` (5 tests): 4 scenarios named in the task brief (ASD parent
  intervention — accepted; ADHD parent education — reproduces the known false positive; ASD+ADHD
  comorbidity — confirmed NOT a false positive, a real trade-off case; "cha mẹ" with no ASD context —
  documents it is routed `asd_question`/low-confidence, not rejected, a related finding).
- Table/list normalization: `tests/unit/test_evidence_normalization.py` (10 tests) using the real
  corpus table/list shapes, including a malformed-row case and a mid-document-marker case.

## Bugs found during regression testing (disclosed, fixed, re-verified)

1. **Old-template collision** (pre-existing, not introduced by T5.2): `asd_definition`'s broad trigger
   silently overrode `risk_factors`/`screening_age`/`dsm5_criteria`/`diagnosis_process` whenever a shared
   source appeared. Found by live-testing all 7 old templates with their real current evidence (not
   previously done with full rigor — T4's `phase_3_answer_quality.md` checked each template in isolation
   with its own trigger source only, never the realistic case of two templates' sources co-occurring).
   Fixed with query-term gating; before/after:
   ```
   Before: q003 (risk factors) -> "Rối loạn phổ tự kỷ (ASD) là một rối loạn phát triển thần kinh..." (WRONG — the generic definition)
   After:  q003 (risk factors) -> "Hiện chưa xác định được một nguyên nhân duy nhất gây ra tự kỷ..." (correct)
   ```
   (same pattern verified for q026, q027, q024 — see `template_implementation_report.md`)
2. **New-template collision** (introduced and caught within this same task, before being left in):
   ADOS-2 question returning the M-CHAT template text because both share `ASD-CSV-002`. Fixed the same
   way, before any test was written against the buggy behavior.

## Explicitly not re-weakened

No existing test assertion was loosened to make this pass; no baseline file was edited; the 7 old
templates' Vietnamese text is byte-for-byte unchanged (only matching order/conditions changed).
