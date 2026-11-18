# T5.3 Phase 6 — Regression Report

All commands actually executed, final run, after all T5.3 code changes.

```
.venv\Scripts\ruff.exe check app tests scripts\audit_t5_1_answer_coverage.py scripts\eval_intent_routing.py scripts\eval_asd_qa.py
                                                               -> All checks passed!
.venv\Scripts\python.exe -m pytest -m "not integration" -q   -> 404 passed, 50 deselected
.venv\Scripts\python.exe -m pytest -m integration -q         -> 50 passed, 404 deselected
```

454 total tests, 0 failures. New this task: 8 (`test_template_conflicts.py`) + 3 new regression tests
in `test_template_negative_cases.py` (2 rewritten to assert the fixed behavior, 3 new co-occurrence
tests) — net +11 over T5.2's 443.

## T2.3 regression

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch> --pool-out <scratch>
```
**66/66 cache hits, 0 misses, 0 Cohere calls**, field-by-field identical to
`reports/demo_mvp/dense_retrieval_regression_metrics.json` except timestamp/log/latency. Run once at
the end of this task's code changes (the Phase 1 fix touches only `app/answer/answer_generator.py` and
`app/answer/evidence_normalization.py`, neither of which this script's call path — `DenseRetriever`/
`CachedQueryEmbedder`/`ResearchVectorReader` — ever imports).

## T2.6 gates

Re-confirmed unchanged: `app/config.py`'s fail-loud `ConfigError` guard untouched; `grep` of every file
changed this task shows no network-client import, no Cohere/LLM/translation call.

## Before/after comparison — all 23 previously-templated questions

Captured live before the Phase 1 fix (preserved in the task transcript; the snapshot file was
inadvertently overwritten by the "after" capture — disclosed, not hidden — see `phase_0_baseline.md`)
and again after. **Result: identical for all 23** — every question still returns `answer_mode:
"topic_template"` with the same answer text as before (confirmed by re-reading each answer's opening
sentence against the pre-fix transcript output). The Phase 1 fix removed exactly 2 confirmed
cross-topic false positives and the latent risk in 4 more templates, while changing **zero** correct
answers among the 23 real cached questions.

## Before/after — 8 representative non-templated/special cases

| Case | Before | After |
|---|---|---|
| qe034 (speech delay) | `extractive_fallback` | `extractive_fallback` — unchanged |
| qe063 (epilepsy) | `insufficient_evidence` | `insufficient_evidence` — unchanged |
| qe062 (weather) | `out_of_scope` | `out_of_scope` — unchanged |
| qe067 (risperidone) | `safety_refusal_dosing` | `safety_refusal_dosing` — unchanged |
| qe074 (stem cell) | `safety_caution_unproven_cure` | `safety_caution_unproven_cure` — unchanged |
| q033 (parent intervention) | `extractive_fallback`, ADHD chunk present | `extractive_fallback`, ADHD chunk present — unchanged (by instruction) |
| uncached paraphrase | `blocked_uncached` (503) | `blocked_uncached` (503) — unchanged |
| greeting | `greeting_template`, `skipped_greeting` | `greeting_template`, `skipped_greeting` — unchanged |

## No test weakened, no baseline edited

No existing assertion was loosened; the 2 tests that needed updating
(`test_a_vague_question_with_the_ndbi_source_present_...`,
`test_signs_by_age_source_present_but_query_about_a_totally_different_topic_...`) were rewritten to
assert the **newly correct** (stricter) behavior, with their old names/docstrings replaced to explain
why, not deleted or silently passed-through.
