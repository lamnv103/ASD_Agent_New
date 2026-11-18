# T5.7 Phase 0 — Baseline Audit

Re-read this task: `reports/t5_5_retrieval_coverage_analysis/t5_5_final_report.md`,
`reports/t5_6_retrieval_improvement/t5_6_final_report.md`,
`reports/t5_6_retrieval_improvement/t5_6_glossary_reconciliation.md`,
`reports/t5_6_retrieval_improvement/t5_6_fts_experiments.md`,
`reports/t5_6_retrieval_improvement/t5_6_answer_quality_evaluation.md` (the "T5.6 end-to-end test
results"), the T2.3 regression artifact (`reports/demo_mvp/dense_retrieval_regression_metrics.json`), and
the T2.6 authorization status (unchanged `APPROVAL_REQUIRED`, confirmed by `app/config.py`'s fail-loud
gate, not by re-reading an old report's prose).

**Code was re-verified directly this task, not inferred from any of the above reports.**

## 1. `app/` is unmodified since T5.5/T5.6

Confirmed via `find app -newer reports/t5_5_retrieval_coverage_analysis/t5_5_final_report.md -type f`:
zero files. `app/api.py`, `app/retrieval/fts.py`, `app/retrieval/evidence_gate.py`,
`app/answer/answer_generator.py`, `app/retrieval/citation_validation.py`, both glossary files — all
re-read in full or in relevant part this task; all match T5.6's own description exactly.

## 2. T5.6's experimental script still exists, unchanged, and still isolated

`scripts/t5_6_fts_experimental.py` (EXP-1, EXP-2, and the EXP-1b addendum) is present and was re-run this
task to confirm its output is still reproducible (`scripts/t5_6_fts_experimental.py`'s own output,
re-generated, matches the per-question source lists already published in
`t5_6_fts_experiments.md`/`t5_6_answer_quality_evaluation.md` for the cases spot-checked).

## 3. T2.3 regression — re-run, not assumed

```
.venv\Scripts\python.exe -X utf8 scripts\dense_retrieval_eval.py --metrics-out <scratch> --pool-out <scratch>
```
Field-by-field diff against `reports/demo_mvp/dense_retrieval_regression_metrics.json` (ignoring
`generated_at`/`log_file`/`latency_ms`): **zero differences**. `cache_hits: 66, cache_misses: 0,
api.calls: 0` re-confirmed. Scratch output deleted after comparison.

## 4. T2.6 — re-confirmed unchanged, not re-litigated

`app/config.py:57-65`: `ENABLE_LIVE_QUERY_EMBEDDING` defaults `False`; the startup `ConfigError` still
fires if it (or the other two `ENABLE_LIVE_*` flags) is set `True`. No attempt was made in this task, or
any prior task, to change this. T2.6's authorization decision itself remains outside every T5.x task's
scope — this task does not propose or imply a position on it.

## 5. What T5.6 actually demonstrated, re-confirmed by independently re-running its own test cases

- `ie015` (melatonin) and the sleep-difficulty reference question → `sleep_nonpharma`/related templates
  fire correctly through the adapter path — re-run this task, same result.
- "ASD là gì?" → T5.6 reported this firing `asd_definition` via "EXP-1b." **Re-running T5.6's own code
  this task surfaces a problem T5.6 did not catch**: using T5.6's exact EXP-1b logic as described
  (anchor concept's full term list, unfiltered), the live top-ranked chunk for "ASD là gì?" is in fact
  the same generic-boilerplate pair (`ASD-OA-PMC4742252`/`ASD-CSV-062`) EXP-1 was built to avoid — T5.6's
  own worked example in `t5_6_answer_quality_evaluation.md` used a hand-constructed tsquery for its
  manual demonstration that excluded the bare "ASD" acronym term without documenting that exclusion as a
  deliberate, generalizable rule. This task's Phase 1 (`fts_precision_audit.md`) finds and fixes the
  actual root cause (a bare short acronym term is exactly as generic/high-frequency as "autism" alone,
  regardless of which named concept it is filed under) — stated here as a correction to what this task
  found when re-verifying T5.6's work directly, not as a criticism to dwell on.

## 6. Protected boundaries — re-confirmed before any further work

- `ASD_DEMO_MODE=true`, all `ENABLE_LIVE_*` flags `False` (unchanged).
- DB already running; `research_reader` connection confirmed at the start of this task without starting
  Docker.
- No corpus/embedding/schema/role/permission change made by this task or any prior one still in effect.
