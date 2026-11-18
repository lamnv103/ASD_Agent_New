# T5.3 — Remaining Blockers

## Not blockers anymore (fixed this task)

- `signs_by_age` and `ndbi_intervention` firing on co-occurring, off-topic source presence — fixed,
  regression-tested.
- 5 more templates (`sleep_nonpharma`, `school_inclusion`, `who_caregiver_training`,
  `ayres_si_definition`, `adolescence_asd`) with the same latent vulnerability pattern — pre-emptively
  gated under the same fix.

## Hard blockers (unchanged, no authorization sought)

1. T2.6 `APPROVAL_REQUIRED` — cache-only remains in force. Unaffected by this task.
2. No ASD-domain clinical/educational expert has reviewed any of the 17 templates' wording. Unaffected
   by this task — carried forward from T4/T5.1/T5.2.

## Open decisions (preserved, not resolved, by instruction)

3. **q033** — the ASD-anchor-only mitigation remains uncommitted. It is characterized (a plain substring
   check, not wired in) but not adopted, because its false-negative risk on ASD+ADHD comorbidity
   questions has only 1 test case, not the broader false-positive/false-negative coverage the task
   requires before proposing it. Needs either (a) a larger test suite specifically targeting this
   trade-off, or (b) a project-owner decision on whether excluding comorbidity content is an acceptable
   cost.
4. **qe034** (speech delay vs. ASD) — still has no template. The corpus does not contain a direct
   statement of the distinction; the closest content (an ICT screening-tool description) does not
   support the specific claim. Needs either new source material or an ASD-expert ruling on whether the
   adjacent content is an acceptable partial answer.
5. **Multi-intent questions** — resolved deterministically (first-priority-match wins) but not
   "correctly" in any semantic sense; this needs real language understanding (an authorized LLM) to do
   better, same conclusion as T4/T5.1.

## Soft limitations (unchanged from T5.2, restated because still true)

6. Table parsing only recovers rows whose cell count matches the header exactly — the 14-row sleep
   table still yields only 1 safely-parsed row.
7. 50/105 questions in the T5.1 content-eval set remain blocked by the cache-only constraint, unrelated
   to template quality.
8. No browser/visual frontend test exists for any of the 17 templates.

## Final status justification

`T5_3_PARTIAL`: all 9 deliverables were produced with real evidence; 2 real defects were found and
fixed with a disclosed, tested, zero-regression change; all 17 templates were individually audited
across the required 8 test dimensions; all mandatory regression (T2.3, T2.6, the 23 existing answers)
passes. Not `T5_3_COMPLETE` because q033 and qe034 remain open by instruction and no ASD-expert review
occurred — the same honesty standard applied throughout T5.1/T5.2 continues here rather than being
relaxed now that the numbers look better. Not `T5_3_BLOCKED` because no authorization or data gap
stopped any part of the work that was actually in scope.
