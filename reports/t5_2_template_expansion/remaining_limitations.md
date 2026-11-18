# T5.2 — Remaining Limitations

## Coverage

- **11 of 105** questions in the T5.1 content-eval set now get a real Vietnamese template answer (up
  from 12/105 at T4 — net effect smaller than +11 because 7 of the 18 permitted questions were
  deliberately rejected at the content-validation stage, not because of a code limit but because their
  evidence does not cleanly support a templated claim; see `template_specifications.md`).
- The 7 rejected questions (qe017, qe023, qe025, qe034, qe041, qe051, qe056) remain in extractive
  fallback. Of these, **qe034 (speech delay vs. ASD) is the most safety-relevant** — the corpus simply
  does not contain a clean, direct statement distinguishing speech delay from ASD; this is a genuine
  corpus/evidence gap, not a template-writing failure, and is listed here for a future corpus-expansion
  or ASD-expert decision, not silently worked around.
- The 50/105 questions blocked by T2.6 (`APPROVAL_REQUIRED`) are entirely unaffected by this task, as
  required.

## q033 (ADHD/ASD confusion) — explicitly NOT fixed in T5.2

Per the task's explicit instruction, the Evidence Gate was not touched. `tests/unit/test_q033_
isolation.py` and the live integration test `test_q033_adhd_confusion_is_still_present_and_unfixed_in_
this_task` both confirm the `NIH-NIMH-ADHD` chunk still surfaces as `direct` support for "Can thiệp do
cha mẹ thực hiện có hiệu quả không?" — unchanged. The same root cause was found again, independently, in
qe051 (home-vs-school intervention), whose best evidence source is a general child-development review,
not ASD-specific — rejected from templating for the same reason, without touching the gate.

A related, smaller finding: a purely generic parenting question with *no* ASD content at all ("Làm sao
để làm cha mẹ tốt hơn?") still routes to `asd_question` (low confidence) rather than `out_of_scope`,
because "cha mẹ" alone is a glossary term. This is the same underlying issue (a generic word used as a
query's only specific term) surfacing one layer earlier, in the router rather than the gate — documented,
not fixed, in this task.

**The lexical mitigation named in T5.1** (require the ASD anchor phrase in the chunk text, not just the
query) is characterized with a plain substring check in `test_mitigation_option_require_asd_anchor_in_
chunk_would_fix_the_false_positive` — it is **not wired into the Evidence Gate**, per instruction. It
would correctly separate the ADHD false positive from the genuine ASD case in the two fixtures tested,
but was not applied because the task requires sufficient false-positive/false-negative testing (which
this task started but did not complete to a decision-ready state) before any such change is proposed.

## Evidence normalization

- Table parsing only safely handles rows whose cell count matches the header exactly — merged/
  continuation rows (as in the real `ASD-OA-PMC7407189` sleep table, where 13 of 14 rows are
  continuations) are not parsed, by design (see `evidence_normalization_audit.md`). A more capable
  parser could recover more of these tables but risks exactly the column/row misattribution the task's
  rules forbid — not attempted.
- "Multiple audience" evidence (a single source discussing more than one condition/population) is
  handled per-template by careful wording (`adolescence_asd`), not by a general-purpose code mechanism.
  No generic multi-audience detector was built.
- The boilerplate stripper only recognizes the specific footer patterns seen in this corpus ("Keep
  Reading:", "See Also") — other corpora or future content could have different boilerplate not caught.

## Template coverage design choices, named explicitly

- `signs_by_age`, `ndbi_intervention`, `school_inclusion`, `who_caregiver_training`, `ayres_si_
  definition`, and `adolescence_asd` fire on trigger-source presence alone, with no query-term gate —
  appropriate because no other template shares their source (verified via the negative tests), but this
  is a design choice that would need revisiting if a future template is added sharing one of these
  sources.
- `mchat_screening`, `ados2_screening`, `melatonin_efficacy` require a query-term match **in addition
  to** source presence, because their sources are shared with another template. This pattern is now
  established (`_QUERY_GATED_TEMPLATES`) and should be the default for any future template whose trigger
  source already appears elsewhere in `_TOPIC_TEMPLATES`/`_NEW_TOPIC_TEMPLATES`.

## Not performed (same as prior phases, restated because still true)

- No ASD-domain clinical/educational expert reviewed any of the 10 new templates' wording.
- No live LLM/Cohere/reranking call was made or enabled.
- No browser/visual frontend test — the new templates were not specifically checked for frontend
  rendering (they return the same `topic_template` mode as the original 7, so no new frontend code path
  was needed, but this was not re-verified in a browser).

## Final status justification

`T5_2_PARTIAL`: all 8 deliverables were produced with real evidence and real code; 10 templates were
implemented, tested, and validated; one pre-existing and one newly-introduced template-collision bug
were found and fixed; the mandatory regression (T2.3, T2.6, old templates) all pass. It is `PARTIAL`
rather than `COMPLETE` because 7 of the 18 permitted questions were not templated (a quality decision,
not a failure to attempt), q033 remains open by instruction, and no ASD-expert review occurred — exactly
the kind of gap the task's acceptance criteria ask to be named, not hidden behind a `COMPLETE` label.
