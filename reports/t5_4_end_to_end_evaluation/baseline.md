# T5.4 Phase 0 — Baseline

## Code re-verified directly (not trusted from T5.1–T5.3 reports alone)

- `app/answer/answer_generator.py`: **17 templates** confirmed by direct count — 7 in `_TOPIC_TEMPLATES`
  (old, query-term-gated since T5.2/T5.3 except the catch-all `asd_definition`), 10 in
  `_QUERY_GATED_TEMPLATES`/the `signs_by_age` special case (all query-term-gated since T5.3's Phase 1
  fix). No ungated template remains except the single designated catch-all.
- `app/retrieval/evidence_gate.py`, `app/answer/evidence_normalization.py`, `app/retrieval/
  citation_validation.py`, `app/router/classifier.py`: re-read in full, unchanged since T5.3.
- T2.6 gates (`app/config.py`): unchanged, fail-loud on attempted enable, re-confirmed.
- Docker: `asd-rag-v2-db` already running; not started/stopped by this task.

## Live baseline counts (re-run, not assumed)

```
.venv\Scripts\python.exe -X utf8 scripts\eval_t5_4_e2e.py
```
Over the 105-question content-eval set (`eval/datasets/asd_qa_eval_v2.jsonl`):

| Category | Count |
|---|---:|
| `topic_template` (real Vietnamese template answer) | 20 |
| `greeting_template` | 2 |
| `extractive_fallback` | 17 |
| `out_of_scope` | 7 |
| `safety_refusal_dosing` | 5 |
| `safety_caution_unproven_cure` | 1 |
| `insufficient_evidence` | 3 |
| Blocked by cache (`QUERY_NOT_CACHED`) | 50 |
| **Total** | **105** |

This matches T5.3's own regression numbers exactly for the 20+2 "answered" categories — no drift found.
(T5.3's report cited "23 templated questions" counting across *two different datasets*: this 105-set
plus 7 questions from the separate, older 66-question `retrieval_eval_v1.jsonl` set — reconciled
explicitly here since the two numbers are not directly comparable without saying so.)

## Answer language, fallback-only (re-verified with the excerpt-level checker, not the whole-answer text)

Of the 17 `extractive_fallback` answers: **15 purely English, 2 "mixed"** (English prose containing
Vietnamese proper nouns — confirmed by spot-check to be substantively English, same caveat as T5.1).
**0 of 17 are Vietnamese-language excerpts.** Unchanged finding from T5.1/T5.2; re-confirmed, not assumed.

## The 23 previously-templated questions (two datasets)

All 23 re-verified live this task (16 from the 105-set shown above + 7 from the older 66-set:
`q001`/`q003`/`q026`/`q027`/`q024`/`q035`/`q057`). **All 23 still return `topic_template` with their
correct text.** Zero regression, consistent with T5.3's own regression report.

## Citation/evidence status spot-check

Every `topic_template` and `extractive_fallback` evidence item re-confirmed to carry a non-empty
`source_url` and `source_id` (`citation_fields_present: true` for all 37 evidence-bearing answers in the
105-set run) — structural citation validity unchanged since T4 Phase 4.
