# T5.3 Final Report — Answer Quality Audit & Template Selection Hardening

**Status: `T5_3_PARTIAL`**

Not `T5_3_COMPLETE` (q033 and qe034 remain explicitly open, by instruction; no ASD-expert review
occurred). Not `T5_3_BLOCKED` (no authorization/data gap stopped any in-scope work — the one external
blocker, Docker Desktop's daemon being down at the very start, was resolved by the user and work
resumed within this same task). No status is raised to `DEMO_READY_FOR_USER_VALIDATION`.

## What was audited

All **17** Vietnamese answer templates (7 from T4, 10 from T5.2), individually, across the 8 test
dimensions named in the task brief: own question, other templates' questions, shared-source questions,
multi-source retrieval, partial evidence, conflicting support types, age mismatch, overlapping
terminology. Full table in `template_selection_audit.md`. Every factual claim in every template was
re-mapped to its literal evidence text in `claim_evidence_validation.md` — not re-trusted from T4/T5.2's
own claims of correctness.

## What was found and fixed

**Two real, reproducible template-selection defects**, found by testing exactly the pattern the task
asked for ("the selection mechanism must not use source overlap alone as sufficient justification"):

1. A sleep-focused question whose gate-filtered evidence happened to also include a `CDC-ASD-SIGNS`
   chunk got the **wrong answer** (the age-based signs template) instead of the sleep answer, because
   `signs_by_age` had no query-side gate.
2. A generic "which intervention works best" question whose evidence included both the ABA source and
   the NDBI source got the **NDBI-specific answer**, which it never asked for, because
   `ndbi_intervention` had no query-side gate.

**Fix**: added a required topic-specific query term to all 7 previously-ungated templates
(`signs_by_age`, `ndbi_intervention`, `sleep_nonpharma`, `school_inclusion`, `who_caregiver_training`,
`ayres_si_definition`, `adolescence_asd`), following the exact pattern already established for the 3
templates T5.2 had already gated (`mchat_screening`, `ados2_screening`, `melatonin_efficacy`) and the
pattern T5.2 separately applied to the old 7. **No template's Vietnamese text changed** — only when
each one is allowed to fire.

## Verified zero regression

All 23 previously-templated questions return the exact same `topic_template` answer text after the fix
as before it (`regression_report.md`). 454 tests pass (11 new this task). T2.3 regression re-confirmed
66/66, byte-identical to the recorded baseline. T2.6 gates, safety overrides, and fallback behavior all
re-verified unchanged.

## What remains explicitly open (not resolved, by instruction)

- **q033** (ADHD/ASD confusion): preserved exactly, re-confirmed still present. The anchor-only
  mitigation was not adopted — insufficient false-positive/false-negative test coverage exists to
  responsibly propose it, and the task explicitly forbade introducing it without that coverage.
- **qe034** (speech delay vs. ASD): still not templated. The corpus genuinely lacks a direct statement
  of the distinction; recorded again, not newly discovered.
- Table evidence: the 14-row sleep table still yields only 1 safely-parsed row, by design (never
  guessing a row/column relationship it cannot verify).

## Acceptance criteria, checked one by one

- All 17 templates individually audited — yes (`template_selection_audit.md`).
- No silent template override remains in tested cases — yes; 2 were found and fixed, re-verified by
  dedicated regression tests.
- All factual claims have explicit evidence mappings — yes (`claim_evidence_validation.md`); 2 templates'
  disclosed partial-coverage statements and 1 template's `indirect` support-type label were re-confirmed,
  not newly found.
- Citation correctness verified — yes, live.
- Fallback limitations honest and visible — yes (`fallback_quality_audit.md`).
- q033 and qe034 remain explicitly controlled — yes (`special_case_review.md`).
- Existing 23 template answers have no regressions — yes, confirmed identical.
- All tests pass — yes, 454/454.
- T2.3 remains 66/66 — yes.
- T2.6 gates unchanged — yes.

No claim of `DEMO_READY_FOR_USER_VALIDATION` appears anywhere in these deliverables.
