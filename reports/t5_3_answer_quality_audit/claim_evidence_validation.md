# T5.3 Phase 2 — Claim-to-Evidence Validation (All 17 Templates)

Each claim checked against the literal evidence text (re-fetched live during this task, not assumed
from T4/T5.2 reports), for topical AND factual support — i.e. "does the evidence actually say this,"
not "is the evidence about the same general subject."

## Old 7 (text unchanged since T4; re-verified, not re-trusted)

| Template | Claims | Evidence | Flags |
|---|---|---|---|
| asd_definition | Developmental disorder; affects communication/social interaction; may show restricted/repetitive behaviors; presentation varies by person | NIH-NIMH-ASD-2025 + CDC-ASD-CLINICAL, direct, verbatim | None |
| risk_factors | No single cause; genetic/biologic/environmental factors; sibling with ASD, genetic/chromosomal conditions, birth complications, older parents; one risk factor ≠ certain diagnosis | CDC-ASD-ABOUT, direct, verbatim | None |
| screening_age | AAP: general screening 9/18/30mo; ASD-specific 18/24mo; or anytime a concern arises | CDC-ASD-SCREENING/CDC-CONCERNED, direct, verbatim | None |
| dsm5_criteria | 2-domain structure; ≥2 of 4 restricted/repetitive criteria; 3 severity levels | CDC-ASD-CLINICAL, direct, verbatim | None |
| diagnosis_process | No single medical test; behavior/development observation; reliable from age 2; self-test/home observation cannot replace professional evaluation | NIH-NIMH-ASD-2025, direct, verbatim | None |
| aba_intervention | Behavioral approaches focus on antecedent/consequence; most evidence for core ASD symptoms | CDC-ASD-TREATMENT, direct, verbatim ("most evidence" is the source's own wording, not an invented superlative) | None |
| vaccine_myth | No literature evidence linking vaccines to autism; claim traces to a retracted study | ASD-OA-PMC12620806, `indirect` (term in body, not heading), verbatim ("a now retracted study") | **Support type is `indirect`, not `direct`** — correctly surfaced to the user via the `support_type` field (T4 Phase 2), not hidden; this is a single secondary-source narrative review, not an exhaustive vaccine-safety literature review — the template's wording ("các tổng quan y văn") is appropriately hedged, not an absolute claim |

## New 10 (re-verified in this task after the Phase 1 gating fix — confirmed fix did not change which evidence each template cites, only when it fires)

| Template | Claims | Evidence | Flags |
|---|---|---|---|
| signs_by_age | Only the age-tagged signs actually listed, for the ages actually present in the excerpt | CDC-ASD-SIGNS, direct, verbatim per item | None — age mismatch impossible by construction (only age-tagged items are ever rendered) |
| mchat_screening | ~10 min; sensitivity 0.85; specificity 0.99; cutoff ≥8; screening ≠ diagnosis | ASD-CSV-029/ASD-CSV-002, direct/indirect, verbatim numbers | None |
| ados2_screening | Semi-structured observation; "gold standard"; interrater reliability 0.79–0.98; part of a larger process | ASD-CSV-062/ASD-CSV-002, direct/indirect, verbatim | None |
| ndbi_intervention | Natural setting, shared control, natural contingencies; AAC+NDBI shows additional language benefit over NDBI alone | ASD-SUP-PMC4513196/ASD-CSV-017, direct, verbatim | None |
| sleep_nonpharma | Sleep disturbance 50–80% comorbidity; non-pharma tried first; **one** "Strong"-tier recommendation (consistent sleep/wake/nap timing) | ASD-OA-PMC7407189, direct | **Evidence truncation, disclosed in-text**: 13 of 14 table rows could not be safely parsed (continuation rows, see Phase 5); template explicitly states it names only one of several recommendations — not an unsupported completeness claim |
| melatonin_efficacy | Melatonin + behavioral interventions are among the few well-established-efficacy treatments for ASD sleep problems | ASD-OA-PMC7407189, direct, verbatim ("well established in the literature") | **Missing qualifier avoided deliberately**: the source's specific dose (3 mg/night) exists but is excluded — this is a claim removed on purpose, not an oversight |
| school_inclusion | 56-study review: increases activity accessibility; does NOT necessarily improve friendship/reciprocity | ASD-CSV-019, direct, verbatim, **both** the positive and limiting finding included | None — this is the template that most actively avoids overgeneralization |
| who_caregiver_training | Sessions 6–9 topics (daily living, positive behavior, caregiver well-being) | WHO-CST-PARTICIPANTS-2022/WHO-CST-INTRO-2022, direct, verbatim | **Evidence truncation, disclosed in-text**: only sessions 6–9 are named (not 1–9); template explicitly says "một phần, không phải toàn bộ" |
| ayres_si_definition | Ayres' definition of SI dysfunction; distinct theoretical basis/assessment vs. other sensory therapies | ASD-SUP-PMC7726187, direct, verbatim | **Scope narrowed on purpose**: no efficacy/cost claim made (those were rejected in T5.2 for qe023/qe025, different questions, not templated) |
| adolescence_asd | Adolescence = significant transition; autistic teens may have heightened EF/social demands vs. childhood; may contribute to anxiety/camouflaging | ASD-OA-PMC12593641/ASD-OA-PMC12468522, direct/indirect, hedged language ("có thể," not "sẽ") | None |

## Citation mapping verification

Re-confirmed live via `tests/integration/test_chat_api_db.py::test_new_t5_2_template_examples_get_real_
vietnamese_answers_with_valid_citations` (6 templates spot-checked against the real database) plus
`app/retrieval/citation_validation.py`'s structural guarantees (unchanged, re-read this task): every
citation's `source_id`/`title`/`source_url`/`excerpt` is compared field-for-field against the actual
`RetrievedChunk`, and only sources the Evidence Gate already judged supporting ever reach this check —
no template in this audit was found citing a source it did not actually use.

## Overgeneralization / wrong-population / age-mismatch flags — summary

**Zero unsupported claims found.** Two templates (`sleep_nonpharma`, `who_caregiver_training`)
explicitly flag their own partial coverage in-text — found during T5.2, re-confirmed here, not newly
discovered. One template (`vaccine_myth`) has `indirect` (not `direct`) support, surfaced via the
existing `support_type` field, also not newly discovered. No age-mismatch case was found across the 17
(the one template with per-item age logic, `signs_by_age`, only ever renders age-tagged items, making a
mismatch structurally impossible, not just unlikely). No wrong-population claim was found in the 17
templates themselves — the wrong-population problem (q033) exists in the **evidence retrieved**, not in
any template's claim text, and is tracked separately in `special_case_review.md`.
