# T5.2 Phase 0 — Preflight

## Docker blocker (disclosed, not hidden)

At the start of this task, Docker Desktop's daemon was not running at all (`docker ps` failed to connect
to the API, not just "container stopped"). Per the task's explicit prohibition on starting/stopping
Docker, the agent stopped and asked the user, who started Docker Desktop themselves. Work resumed once
`docker ps` showed `asd-rag-v2-db` healthy again. No Docker command was run by the agent at any point.

## Re-verification of current code (not assumed from T5.1's reports)

Read directly, in full, before any change: `app/answer/answer_generator.py`, `app/retrieval/
evidence_gate.py`, `app/router/classifier.py`, `app/nlp/text_match.py`, `app/retrieval/citation_
validation.py`, and the existing test files for each. Confirmed: 7 fixed-text topic templates, lexical
Evidence Gate with `support_type`/`age_mismatch` (T4), intent router with `high`/`low` confidence (T4),
no table/list-aware evidence normalization existed yet (T5.2's Phase C gap, confirmed empty before this
task added `app/answer/evidence_normalization.py`).

## Re-retrieval of the 18 permitted questions against live evidence (not assumed from T5.1's snapshot)

All 18 were re-run through the live `/api/chat` pipeline during this task
(`eval/reports/t5_2_fresh_evidence.json`, generated then inspected and discarded as a scratch file —
its findings are reproduced in `template_specifications.md`). Result: evidence sources and
`support_type` classifications matched T5.1's snapshot exactly, with one exception caused by the
author's own transcription error (qe051 was queried with a shortened paraphrase instead of the exact
cached text and returned `QUERY_NOT_CACHED`; re-run with the exact dataset text, it matched T5.1 again).
This confirms the corpus/cache/gate behavior is stable since T5.1 — the gap analysis's numbers were not
stale.

## Scope decision, made in this phase and carried through the rest of T5.2

Re-reading the 18 questions' *actual* evidence content (not just their `support_type` label) during
specification work (Phase A) found that several, despite passing the Evidence Gate's topical check, do
not have evidence that cleanly supports a templated claim — e.g. methodology-only text, workbook
boilerplate, or evidence about a different (non-ASD-specific) population. This is exactly the
"chất lượng quan trọng hơn coverage" instruction in action: **11 of the 18 were built into 10 templates;
7 were deliberately left as extractive fallback**, each with a documented reason in
`template_specifications.md`. This was decided in Phase 0/A, before any template code was written, not
discovered after the fact.
