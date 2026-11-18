# T5.4 — End-to-End Vietnamese Answer Evaluation — Final Report

## Scope re-stated

Full end-to-end evaluation of the ASD Knowledge Assistant demo across all 6 required phases: baseline
re-verification, 105-question re-run, Vietnamese answer quality (8 dimensions, 23 templates), claim-level
citation validation, safety/negative evaluation (10 scenarios), and a fresh, frozen, independent
32-question set — followed by full regression. Strictly read-mostly: **zero code changes were made in
this task**, consistent with the instruction to only modify code for a severe, reproducible defect, none
of which was found.

## Acceptance-criteria checklist

| Criterion | Status |
|---|---|
| All 105 questions evaluated with full required field set | ✓ `evaluation_105_questions.md` |
| 6-way Answered/Partially-answered/Insufficient-evidence/Cache-miss/Out-of-scope/Safety-refusal distinction applied, cache miss not counted as a professional-accuracy error | ✓ |
| All 23 templated questions quality-evaluated across the 8 named dimensions | ✓ `vietnamese_answer_quality.md`, 0 defects found |
| Fallback evaluated separately for raw-English-excerpt honesty | ✓ (15 English + 2 mixed, 0 overstated conclusions) |
| Claim-level citation validation (not just source-ID existence) | ✓ `claim_citation_validation.md`, 0 defects found; 1 dataset-coverage gap disclosed (age-mismatch) |
| Negative/safety evaluation, 10 named scenarios | ✓ `safety_negative_evaluation.md`, 9/10 directly demonstrated live, 1/10 mechanism-verified via unit test (no live cached case exists) |
| ≥30 new, independent, frozen, non-tuning-influencing questions | ✓ `independent_30_question_set.md`, 32 created, 0 overlap, hash-verified frozen |
| Independent-set results reported honestly, no retuning | ✓ `independent_30_question_results.md` — 32/32 correct routing, 1/32 correct safety refusal, 31/32 cache miss (coverage limitation, explicitly disclosed, not hidden) |
| Full regression: unit + integration + T2.3 66/66 + 23 templated + safety + citation + fallback | ✓ `regression_report.md` — 454/454 tests, T2.3 identical to baseline, zero regression on the 23 |
| Remaining limitations publicly disclosed | ✓ `remaining_blockers.md`, 7 open items |
| T2.6 = `APPROVAL_REQUIRED` unchanged | ✓ re-confirmed, no attempt to alter |
| `ASD_DEMO_MODE=true`, all `ENABLE_LIVE_*` false, fail-loud gates unchanged | ✓ re-confirmed |
| No corpus/embedding/DB/Docker/Git changes | ✓ none made |
| Never self-promote to `DEMO_READY_FOR_USER_VALIDATION` | ✓ not claimed below |

## Summary of findings

1. **No new defect found.** Every phase's conclusion was "0 defects found" for the mechanisms actually
   re-tested. T5.3's two real template-selection bugs (`signs_by_age`, `ndbi_intervention`) remain fixed
   and show zero regression. This task's job was to re-verify, not re-trust, and re-verification held.
2. **The single dominant, honestly-quantified limitation is cache coverage**, not answer quality. On the
   brand-new, never-seen 32-question independent set, 31/32 questions cache-missed. This is the most
   important number in this entire report: it is direct evidence that the demo's real-world usefulness is
   currently bottlenecked by the cache-only constraint (T2.6), not by template correctness, citation
   integrity, or safety handling — all of which performed cleanly on every question the system actually
   attempted, across both the 105-set and the 32-set, with zero fabricated or wrong answers found anywhere.
3. **Safety and citation integrity held under fresh adversarial-style testing.** The self-dosing-
   adjustment scenario correctly refused on a brand-new phrasing (`ie016`) never seen before. No citation
   was found to be fabricated, mismatched, or claim-unsupported across 37 evidence-bearing answers. The
   ordering guarantee (safety check before retrieval) held on every tested scenario.
4. **Three disclosed, unaddressed gaps remain** (see `remaining_blockers.md`): zero live demonstration of
   a true age-mismatch case (mechanism verified by unit test, not by a live cached example), three
   uncovered topic areas (adolescent sex education, adult ASD/marriage, Vietnamese folk-belief myths), and
   the long-standing lack of any clinical/ASD-expert review of any claim in this project to date.

## Final status

```
T5_4_PARTIAL
```

**Rationale**: all 6 phases were completed and all required deliverable files were produced, with no
severe reproducible defect found and zero regression — but the task cannot be marked `T5_4_COMPLETE`
because real, disclosed gaps remain open (cache coverage is narrow enough that most new real-world
questions fail closed rather than answer; no clinical expert has ever reviewed any claim; one evaluation
dimension — live age-mismatch — could only be verified at the unit-test level, not end-to-end). None of
these gaps are code defects this task is licensed to "complete away" without either a new local/Cohere
embedding authorization (T2.6) or a human clinical reviewer — both outside this task's scope. This status
is **not** `DEMO_READY_FOR_USER_VALIDATION`, which this report does not claim, consistent with every
prior T5.x task in this project.
