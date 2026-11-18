# T5.2 Final Report — Controlled Vietnamese Template Expansion

**Status: `T5_2_PARTIAL`**

Not `T5_2_COMPLETE` (7 of 18 permitted questions were deliberately not templated — a quality decision,
documented, not a code failure) and not `T5_2_BLOCKED` (no authorization/data blocker stopped the work
that was in scope; the one real blocker encountered — Docker Desktop's daemon being down — was resolved
by the user starting it, and work resumed within the same task). Not raised to
`DEMO_READY_FOR_USER_VALIDATION` — that was never this task's target status.

## What was implemented

- **10 new Vietnamese answer templates** covering **11 of the 18** questions T5.1 identified as
  template-ready-without-new-authorization: `signs_by_age` (dynamic, age-aware), `mchat_screening`,
  `ados2_screening`, `ndbi_intervention`, `sleep_nonpharma` (table-derived), `melatonin_efficacy`,
  `school_inclusion`, `who_caregiver_training`, `ayres_si_definition`, `adolescence_asd`.
- **New evidence-normalization module** (`app/answer/evidence_normalization.py`) distinguishing table,
  list, and paragraph evidence, with age extraction and boilerplate stripping — built and tested against
  the actual corpus shapes (a real 14-row sleep-recommendation table, a real age-tagged CDC signs list).
- **Two template-collision bugs found and fixed**: one pre-existing (4 of the original 7 templates were
  being silently hijacked by the generic `asd_definition` template whenever they shared a source — found
  by this task's own regression testing, not previously caught), one newly introduced and caught within
  this same task (ADOS-2/M-CHAT sharing a source). Both fixed with a query-term-gating pattern; the 7 old
  templates' Vietnamese text is unchanged.
- **q033 isolation tests** (5 tests) characterizing the ADHD/ASD false positive, a related low-
  confidence-routing finding, and a lexical mitigation option — **without changing the Evidence Gate**,
  per instruction.
- **39 new tests** total (10 normalization + 5 q033 + 10 negative/diacritic + 2 live-DB integration + 12
  template-firing/collision-regression), on top of 404 pre-existing tests — **443 total, all passing**.

## Numbers

| Metric | T4/T5.1 | After T5.2 |
|---|---:|---:|
| Questions with a real Vietnamese template answer (of 105) | 12 | 23 (12 old + 11 new) |
| Questions correctly identified as not-yet-template-ready, with documented reasons | — | 7 |
| T2.3 regression | 66/66 | 66/66, re-confirmed twice |
| Old templates verified bug-free under realistic multi-source evidence | not previously tested this way | 7/7, after fixing 1 found bug |

## Where the 7 unused "permitted" questions went, and why

`template_specifications.md`'s rejection table: qe017/qe023/qe025 (evidence too tangential/methodological
to the literal claim), qe034 (safety-relevant — corpus genuinely lacks the clean distinguishing claim),
qe041 (one study's methodology, risk of overgeneralizing to "Vietnam's approach"), qe051/qe056 (same
root-cause family as q033 — non-ASD-specific or boilerplate evidence). None were force-fit into a
template.

## What still needs T2.6 or an ASD expert

Unchanged from T5.1/T4: the 50/105 cache-blocked questions need T2.6 authorization or cache expansion;
none of the 10 new templates' wording has been reviewed by a qualified ASD clinical/educational expert;
q033's actual fix (the anchor-requirement rule, or an owner-approved trade-off) needs a product decision
this task was explicitly told not to make unilaterally.

## Acceptance criteria, checked one by one

- Every new template has a specification and evidence mapping — yes (`template_specifications.md`).
- No important claim lacks evidence — yes; claims not supported by evidence were excluded, not
  templated (`answer_validation_report.md`).
- No fabricated or irrelevant citation — yes, re-verified live (`regression_report.md`).
- The 7 old templates not degraded — **initially found degraded (pre-existing bug), fixed, now verified
  not degraded** — disclosed as a finding, not swept under "no regression."
- Safety behavior unchanged — yes (dosing/cure-claim overrides untouched, re-tested).
- Table evidence not misrepresented — yes, enforced by refusing to parse malformed rows rather than
  guessing.
- Test suite and T2.3 regression pass — yes, 443/443, 66/66.
- Report states how many questions improved and how many remain unanswerable — yes, in this report and
  `remaining_limitations.md`.

No claim of `DEMO_READY_FOR_USER_VALIDATION` is made anywhere in these deliverables.
