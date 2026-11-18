# T5.4 Phase 6 — Full Regression

Zero code changes were made anywhere in this task (T5.4 found no severe, reproducible defect requiring a
fix — see Phases 1–5 above). This regression run therefore confirms the codebase is unchanged and
behaves identically to its T5.3 state, re-verified live rather than assumed.

## Unit tests

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q
404 passed, 50 deselected
```

## Integration tests

```
.venv\Scripts\python.exe -m pytest -m integration -q
50 passed, 404 deselected
```

**Total: 454 passed**, matching the count entering T5.4 exactly (no new tests added, no tests removed,
no tests modified, no failures).

## T2.3 dense-retrieval regression (the frozen 66-question set)

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch> --pool-out <scratch>
```
Field-by-field diff against the recorded baseline (`reports/demo_mvp/dense_retrieval_regression_metrics.json`),
ignoring only `generated_at`/`log_file`/`latency_ms`: **zero differences**. Specifically re-confirmed:
`cache_hits: 66, cache_misses: 0, api.calls: 0` (unchanged — 66/66 cache hits, 0 misses, 0 Cohere calls).
Scratch output and the generated timestamped log file were deleted after comparison, per this task's
practice of leaving no stray files in the repo.

## Zero regression on the 23 confirmed templated questions

Re-verified live in Phase 0/1/2 (`baseline.md`, `evaluation_105_questions.md`, `vietnamese_answer_quality.md`):
all 23 (16 from the 105-set + 7 from the older 66-set) still return `topic_template` with their correct,
unchanged text. **Zero regression**, satisfying the task's explicit "Không chấp nhận regression ở 23 câu
hỏi đã được xác nhận" requirement.

## T2.6 / demo-mode gates re-confirmed unchanged

`app/config.py` re-read in full this task: `DEMO_MODE = _flag("ASD_DEMO_MODE", True)`, all three
`ENABLE_LIVE_*` flags default `False`, startup `ConfigError` raised if any is set `True`. Unchanged since
T3.0. No Cohere call occurred in any script or test run this task (confirmed by the `api.calls: 0` field
above, the only place in the codebase that would make such a call).

## Ruff

```
ruff check scripts/eval_t5_4_e2e.py scripts/eval_independent_30.py
```
Clean (after the one trivial unused-import fix noted in the task summary). Pre-existing, unrelated lint
errors in `scripts/prepare_t2_4c_human_review.py` were not touched and are out of scope for this task's
`ruff check`, consistent with every prior T5.x task's practice of scoping lint checks to files actually
modified.

## Conclusion of Phase 6

Full regression clean. Zero code changes, zero new defects, zero regression on the 23 confirmed
questions, T2.3 still exactly 66/66 cache hits with 0 Cohere calls, T2.6 gates unchanged.
