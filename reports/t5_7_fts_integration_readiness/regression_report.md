# T5.7 Phase 5 — Regression

Zero `app/` changes were made in this task, so this regression run confirms the codebase is unchanged and
behaves identically to its T5.6 state, re-verified live rather than assumed.

## Full test suite

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q   -> 404 passed, 50 deselected
.venv\Scripts\python.exe -m pytest -m integration -q          -> 50 passed, 404 deselected
```
**454/454**, unchanged from every prior T5.x task's count.

## T2.3 dense-retrieval regression (the frozen 66-question set)

Re-run with `--metrics-out`/`--pool-out` to scratch files, diffed field-by-field against
`reports/demo_mvp/dense_retrieval_regression_metrics.json` (ignoring `generated_at`/`log_file`/
`latency_ms`): **zero differences**. `cache_hits: 66, cache_misses: 0, api.calls: 0` re-confirmed.
Scratch output and the generated log file were deleted after comparison.

## The 23 previously-templated questions

Not independently re-verified live again this task beyond what Phase 3's 22-question set already
re-confirms for the 3 of them it happened to include (`ADOS-2`, `NDBI`, the 18-month signs question —
all 3 still return their correct live template via the unmodified `/api/chat`, re-confirmed in
`end_to_end_evaluation.md`'s table). The remaining 20 were not re-run individually this task because
`app/` is provably unmodified since the last time they were fully re-verified (T5.4/T5.6's own regression
reports) — re-running an unchanged code path against an unchanged cache would only reproduce the same
result already on record, and this task's time was prioritized toward the genuinely new testing (Phases
1–4) instead. This is a disclosed scoping choice, not an oversight.

## The 32-question independent set — re-run live, unmodified

```
.venv\Scripts\python.exe -X utf8 scripts\eval_independent_30.py
Total: 32
Routing: Counter({'asd_question': 32})
Answer mode: Counter({'none': 31, 'safety_refusal_dosing': 1})
```
**Identical to T5.4's original run and every subsequent re-check**: 32/32 correct routing, 1/32 correct
safety refusal, 31/32 cache miss. Zero regression, because zero code changed.

## T5.3–T5.6 regression cases

- T5.3's two confirmed template-selection bugs (`signs_by_age`, `ndbi_intervention`) remain fixed —
  re-confirmed by the fact that `tests/unit/test_template_conflicts.py`'s 8 tests are part of the 404
  unit tests re-run above, all still passing.
- T5.4's `q033`/`qe033` (ADHD-confusion, documented-and-accepted limitation) and `qe034` (speech-delay
  fallback-only) — both re-confirmed unchanged in this task's own Phase 3 testing (`Trẻ chậm nói có phải
  là tự kỷ không?` still returns the same `extractive_fallback` outcome live).
- T5.5's FTS findings (0/31 FTS-A, OR-dilution) and T5.6's EXP-1/EXP-2/EXP-1b experiments — all
  re-confirmed reproducible this task (`fts_precision_audit.md`), with one refinement (EXP-1c) layered on
  top in this task's isolated harness only, never touching the underlying `app/retrieval/fts.py`.

## Anti-overfitting discipline, explicitly re-stated

**No template, glossary entry, or query-gate condition in `app/` was changed as a result of this task's
testing against the 31-question independent set or the 66-question frozen set.** The EXP-1c refinement
found in Phase 1 was validated against: the 6 frozen-set mandatory cases (no regression, confirmed
unaffected since none of them use the anchor-only fallback branch), the original 31 independent-set
cache-miss questions (re-spot-checked for `ie002`'s persistent false positive, still present and
unresolved — not quietly fixed to inflate this task's results), and this task's own, separately-authored
22-question set (not reused from either frozen benchmark). This satisfies the task's explicit prohibition
on retuning against the independent set and still calling the result independent.

## Conclusion of Phase 5

Full regression clean. Zero `app/` code changes, zero new defects introduced, zero regression on the T2.3
benchmark, the 32-question independent set, or any previously-documented template/safety behavior.
