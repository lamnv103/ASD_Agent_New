# T5.8 — Safety Hardening & Retrieval Interaction Audit — Final Report

## Scope re-stated

Fix and verify the T5.7-discovered safety-bypass risk: the unproven-cure caution was conditioned on
`evidence` being empty, so FTS's broader lexical recall could silently suppress it. Goal: safety
behavior stable before and after retrieval, never driven by whether any chunk happened to be found. This
task explicitly does not integrate FTS into the demo API and does not claim
`DEMO_READY_FOR_USER_VALIDATION`.

## What was done, by phase

- **Phase 0**: re-read T5.7's final report and safety audit, T2.6 (unchanged), the original T3.1–T3.6
  safety-override design intent, and T5.3's template audit; re-verified the exact code path and its
  evidence-dependence directly; **reproduced the T5.7 bug twice** — once live via the isolated T5.7
  harness, once as a new permanent unit test confirmed to fail against the pre-fix code.
- **Phase 1**: built the required A/B/C taxonomy, with Group C specifically designed to prove the fix
  does not over-sweep ordinary medication/vitamin/intervention questions into a refusal — and the task's
  required 4-state distinction (mentions / evaluates / bounded efficacy / proven cure) made explicit.
- **Phase 2**: found the exact root cause (`and not evidence` on the cure-caution branch only — the
  dosing-refusal branch was never affected); applied a minimal, isolated fix (~15 added lines, one
  changed conditional, in one file) satisfying all 6 stated design principles; verified before/after at
  the unit-test level, the live-harness level, and against 4 unrelated, unaffected live answers.
- **Phase 3**: **31 new, independently-authored adversarial test cases** (exceeding the required 30),
  covering diacritics, no-diacritics, natural phrasing, and multi-intent framing. **Found 5 additional,
  real, pre-existing classifier gaps** beyond the original T5.7 bug (A5: "chữa dứt điểm" phrasing; B2:
  "tự điều chỉnh liều"; B5/B9: drug-to-drug switching phrasing; B6: a stated mg dose with no word "liều").
  **Fixed 4 of the 5** with narrow, targeted additions, each with its own before/after regression test.
  **Deliberately left 1 (B8) unfixed and disclosed**, because the only available fix would have required
  broadening a trigger in a way that risked sweeping in legitimate research/efficacy questions — exactly
  what this task's own principles forbid. Final adversarial pass rate: **30/31**, with the 1 failure
  named, explained, and justified rather than hidden.
- **Phase 4**: the same 3 representative queries (Group A, Group B, Group C) run under **6 controlled
  evidence conditions** each. **Group A and Group B: 100% stable** (1 mode each, across all 6
  conditions, for both queries) — the fix's core guarantee, verified directly rather than inferred from
  Phase 3's broader sweep. **Group C: appropriately variable**, confirming the fix did not also freeze
  ordinary evidence-based answering, which must still respond to what is actually retrieved.
- **Phase 5**: full regression — 464/464 tests (10 new, 0 removed, 0 unrelated changes), T2.3 byte-
  identical, the 32-question independent set unchanged, 6 spot-checked live templates across definition/
  signs/sleep/screening/intervention all unaffected, honest fallback still honestly labeled.

## Direct answer to the final-status gating question

**"Chỉ được kết luận Safety hardening hoàn thành khi lỗi T5.7 được tái hiện trước sửa, được sửa, và vượt
qua các kiểm thử trước/sau."** — satisfied exactly:
- Reproduced before the fix: ✓ (live harness + a unit test that failed with the exact pre-fix behavior).
- Fixed: ✓ (`app/answer/answer_generator.py`, minimal, isolated, documented).
- Passes the before/after test: ✓ (the same unit test now passes; the live harness now returns
  `safety_caution_unproven_cure` for the vitamin-B6 case instead of `extractive_fallback`).

## What remains open, disclosed rather than smoothed over

- **B8** (generic "which drug and what dose" with no drug named) is not caught, by a reasoned decision to
  avoid a higher-risk fix, not an oversight.
- No ASD clinical expert has reviewed any of this task's wording, taxonomy, or fix — consistent with
  every prior T5.x task's standing disclosure, and the explicit instruction not to claim readiness for
  real users without that review.
- FTS is still not wired into the live `/api/chat` (by this task's own explicit protected boundary) — this
  task hardens the *answer-generation* logic against the *scenario* FTS integration would create, but
  does not itself change what the live demo does today for any already-cached question.

## Protected boundaries — compliance re-confirmed

- No Cohere/LLM call; no live query embedding enabled; `ASD_DEMO_MODE=true` and all `ENABLE_LIVE_*` flags
  `False`, unchanged.
- No write to production; no change to the 2,338 vectors, the corpus, or any frozen benchmark; no
  sealed/reveal access; no DB schema/permission change; Docker was already running throughout (not
  started/stopped by this task); no Git commit/push.
- **FTS was not integrated into the demo API** — the only `app/` file changed is
  `app/answer/answer_generator.py`, and the change is entirely about how `generate()` reasons about
  evidence it is given, not about what retriever supplies that evidence.
- Every change has the before/after evidence and rollback path this task's boundaries require, detailed
  in `root_cause_analysis.md` and `implementation_changes.md`.

## Final status

```
T5_8_COMPLETE
```

**Rationale**: the task's own explicit completion gate (reproduce → fix → pass before/after) is met for
the T5.7 finding, with concrete, re-checkable evidence at every step, not asserted. The additional
adversarial-testing work (Phase 3/4) found and fixed 4 further real gaps with the same rigor, and
honestly disclosed the 1 it chose not to fix and why. Full regression is clean across every benchmark
this project has accumulated. This status is specifically about **safety-hardening completion**, not
about the broader FTS-integration readiness question (still `T5_7_PARTIAL`, unchanged by this task) or
about readiness for real users — this report does **not** claim `DEMO_READY_FOR_USER_VALIDATION`, and
explicitly does not claim readiness for real-user testing in the absence of an ASD clinical expert
review, which has still not occurred at any point in this project.
