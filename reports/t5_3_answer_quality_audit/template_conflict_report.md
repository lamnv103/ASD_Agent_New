# T5.3 Phase 3 — Template Conflict Report

New file: `tests/unit/test_template_conflicts.py`, 8 tests, one per category named in the task brief,
run and passing. Supplementary conflict/negative tests also live in `test_template_negative_cases.py`
and `test_answer_generator.py` (cross-referenced below).

| # | Category | Test | Result |
|---|---|---|---|
| 1 | DSM-5 vs. ASD definition | `test_1_dsm5_vs_asd_definition` | DSM-5 question gets DSM-5 text, not the generic definition, despite sharing `CDC-ASD-CLINICAL` |
| 2 | ADOS-2 vs. M-CHAT | `test_2_ados2_vs_mchat` | Each gets its own text, despite sharing `ASD-CSV-002` |
| 3 | Sleep vs. developmental signs | `test_3_sleep_vs_developmental_signs` | **Real bug reproduced and fixed this phase** — see `template_selection_audit.md` Defect 1 |
| 4 | ASD vs. ADHD parent education | `test_4_asd_vs_adhd_parent_education` | **Confirmed still open, unfixed by instruction** — the Evidence Gate still accepts the ADHD chunk as `direct` support; this test exists specifically so a future accidental fix shows up as a diff here |
| 5 | Multiple templates sharing one source | `test_5_multiple_templates_sharing_one_source` | All 3 specific templates sharing `NIH-NIMH-ASD-2025` with the catch-all correctly win over it |
| 6 | Generic template vs. specific template | `test_6_generic_template_vs_specific_template` | Catch-all only fires when nothing specific matches |
| 7 | Multi-intent question | `test_7_multi_intent_question` | A question naming two topics resolves deterministically to the first-priority match; documented as a design choice (no way to know which the user meant more without an LLM), not "fixed" |
| 8 | Template candidate with insufficient evidence | `test_8_template_candidate_with_insufficient_evidence_never_reaches_the_template_at_all` | Structurally guaranteed — `generate()` only ever receives evidence the gate already judged sufficient; empty evidence short-circuits to `insufficient_evidence` before any template is even considered |

## Additional conflict coverage (not re-duplicated here, cross-referenced)

- `test_template_negative_cases.py`: 12 tests, including the two T5.3 regression tests for Defects 1–2
  (`test_sleep_question_with_a_co_occurring_signs_chunk_...`,
  `test_generic_intervention_question_with_a_co_occurring_ndbi_source_...`) and
  `test_generic_intervention_question_with_no_specific_term_at_all_falls_back_honestly`.
- `test_answer_generator.py`: the original T5.2 collision-fix tests for the old 7 templates
  (`test_risk_factors_template_fires_not_the_generic_definition_despite_shared_source`, etc.) — re-run
  this phase, still passing, confirming the Phase 1 fix did not disturb them.

## Net result

Before this phase: 2 of 17 templates had a *confirmed* cross-topic false-positive risk (one newly found
in T5.2, since fixed before T5.2 shipped; one newly found in T5.3, fixed in this phase). After this
phase: 0 templates fire on source presence alone except the single designated catch-all, and this is
now enforced consistently, not template-by-template as issues happen to be noticed.
