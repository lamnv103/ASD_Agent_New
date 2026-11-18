# T5.3 Phase 1 — Template Selection Audit

## Selection mechanism (as it exists after this task's fix)

```
generate(query, evidence):
  1. is_dosing_question / is_unproven_cure_question  (safety overrides, unconditional, unchanged)
  2. if not evidence: insufficient_evidence
  3. _template_for(query, source_ids)        — the 7 old templates, each requiring BOTH its trigger
                                                source(s) AND a topic-specific query term, except the
                                                catch-all `asd_definition`, checked LAST
  4. _new_template_for(query, evidence)      — signs_by_age (query must contain "dấu hiệu" AND a named
                                                age), then the 9 remaining new templates, ALL now
                                                requiring both their trigger source(s) AND a
                                                topic-specific query term (T5.3 fix — see below)
  5. extractive fallback
```

**Rule now enforced for all 17 templates**: no template fires on source presence alone unless it is the
single designated catch-all (`asd_definition`), which is explicitly last-resort and only answers the
generic "what is ASD" shape of question. This directly satisfies the task's requirement that "source
overlap alone" must never be sufficient justification.

## Two real defects found and fixed in this phase

### Defect 1 — `signs_by_age` firing on co-occurring evidence for an unrelated (sleep) question

**Reproduction** (exact code, run live before the fix):
```python
evidence = [chunk(source="CDC-ASD-SIGNS", excerpt="<age-tagged signs list>"),
            chunk(source="ASD-OA-PMC7407189", excerpt="<sleep paragraph>")]
generate("Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?", evidence)
# -> answer_mode "topic_template", text = "Theo CDC, một số dấu hiệu cảnh báo ..." (WRONG TOPIC)
```
Root cause: `signs_by_age` was checked first among the new templates and fired whenever a
`CDC-ASD-SIGNS` chunk appeared in the evidence list, regardless of what the query actually asked.
**Fixed**: now requires the query to contain "dấu hiệu" AND a named age (`_render_signs_by_age_gated`).
Re-run after fix: correctly returns the `sleep_nonpharma` answer, no mention of "9 months" (test
`test_3_sleep_vs_developmental_signs`).

### Defect 2 — `ndbi_intervention` firing on co-occurring evidence for a generic intervention question

**Reproduction**:
```python
evidence = [chunk(source="CDC-ASD-TREATMENT", excerpt="<ABA paragraph>"),
            chunk(source="ASD-SUP-PMC4513196", excerpt="<NDBI paragraph>")]
generate("Can thiệp nào cho trẻ tự kỷ hiệu quả nhất?", evidence)
# -> answer_mode "topic_template", text = "Can thiệp hành vi phát triển tự nhiên (NDBI)..." (NOT ASKED FOR)
```
**Fixed**: now requires the query to contain "ndbi". Re-run after fix: a generic question with no
"ABA"/"hành vi"/"NDBI" wording at all correctly falls to `extractive_fallback`
(`test_8_...`/`test_generic_intervention_question_with_no_specific_term_at_all_falls_back_honestly`); a
question naming ABA specifically gets the ABA answer even with the NDBI source co-occurring
(`test_6...`/`test_generic_intervention_question_with_a_co_occurring_ndbi_source_gets_the_aba_answer`).

The same class of fix (adding a required query term) was applied to the other 5 templates that had no
gate (`sleep_nonpharma`, `school_inclusion`, `who_caregiver_training`, `ayres_si_definition`,
`adolescence_asd`) pre-emptively, since the same vulnerability pattern applies to all of them even
though a live-reproducible co-occurrence wasn't separately constructed for each — see
`template_implementation_report.md`-style disclosure: these 4 were fixed on the strength of the
*pattern* found in Defects 1–2, not because each one was individually proven to misfire today.

## Per-template audit (all 17)

| # | Template | Trigger source(s) | Query gate (after fix) | Own question | Cross-template question | Shared-source question | Multi-source | Partial evidence | Conflicting support type | Age mismatch | Overlapping terms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | risk_factors | CDC-ASD-ABOUT, NIH-NIMH-ASD-2025 | "nguy cơ"/"yếu tố" | ✓ | ✓ declines for DSM-5/screening/diagnosis questions | ✓ wins over asd_definition | ✓ (q003 baseline: 2 sources) | n/a | n/a | n/a | ✓ resolved deterministically vs. diagnosis_process (test 7) |
| 2 | screening_age | CDC-ASD-SCREENING, CDC-CONCERNED, NIH-NIMH-ASD-2025 | "sàng lọc"/"độ tuổi"/"tuổi nào" | ✓ | ✓ | ✓ wins over asd_definition | ✓ (4 sources in baseline) | n/a | n/a | n/a | — |
| 3 | dsm5_criteria | CDC-ASD-CLINICAL | "dsm" | ✓ | ✓ declines for definition/diagnosis questions | ✓ wins over asd_definition AND diagnosis_process (checked first) | ✓ | n/a | n/a | n/a | — |
| 4 | diagnosis_process | NIH-NIMH-ASD-2025, CDC-ASD-CLINICAL | "chẩn đoán" | ✓ | ✓ | ✓ wins over asd_definition | ✓ (4 sources) | n/a | n/a | n/a | ✓ loses to risk_factors in multi-intent test (documented, not a bug) |
| 5 | aba_intervention | CDC-ASD-TREATMENT | "aba"/"hành vi" | ✓ | ✓ declines for generic/NDBI questions | n/a (no other template uses this source) | n/a | n/a | n/a | n/a | ✓ wins over NDBI when co-occurring (Defect 2 fix) |
| 6 | vaccine_myth | ASD-OA-PMC12620806 | "vắc xin"/"vacxin"/"tiêm chủng" | ✓ | n/a | n/a (shared with GFCF-diet template at the SOURCE level — see note below) | n/a | ✓ (1 of 5 original chunks was the relevant one — T4 finding, unchanged) | n/a | n/a | n/a |
| 7 | asd_definition | NIH-NIMH-ASD-2025, CDC-ASD-CLINICAL | none (catch-all, checked LAST) | ✓ | ✓ correctly loses to all 3 specific templates sharing its sources | n/a (it IS the shared-source case) | ✓ | n/a | n/a | n/a | — |
| 8 | signs_by_age | CDC-ASD-SIGNS | "dấu hiệu" + a named age | ✓ (both qe028/qe029) | ✓ **Defect 1, fixed** | n/a | n/a | ✓ only age-tagged items rendered | n/a | ✓ excerpt-side age-tag check (unchanged from T5.2) + query-side age check (new) | ✓ |
| 9 | mchat_screening | ASD-CSV-029, ASD-CSV-002 | "m-chat"/"mchat" | ✓ | ✓ declines for ADOS-2 (shares ASD-CSV-002) | ✓ (fixed in T5.2) | n/a | n/a | n/a | n/a | — |
| 10 | ados2_screening | ASD-CSV-062, ASD-CSV-002 | "ados" | ✓ | ✓ | ✓ (fixed in T5.2) | n/a | n/a | n/a | n/a | — |
| 11 | ndbi_intervention | ASD-SUP-PMC4513196, ASD-CSV-017 | "ndbi" | ✓ | ✓ **Defect 2, fixed** | n/a | ✓ (2 sources) | n/a | n/a | n/a | ✓ |
| 12 | sleep_nonpharma | ASD-OA-PMC7407189 | "giấc ngủ"/"ngủ" | ✓ | ✓ declines for melatonin-specific questions (checked after melatonin) | ✓ (shares source with melatonin, fixed in T5.2) | n/a | ✓ only 1 of 14 table rows cited, explicitly | n/a | n/a | — |
| 13 | melatonin_efficacy | ASD-OA-PMC7407189 | "melatonin" | ✓ | ✓ | ✓ | n/a | n/a | n/a | n/a | — |
| 14 | school_inclusion | ASD-CSV-019 | "hòa nhập"/"trường học"/"trường phổ thông" | ✓ | ✓ (gate added pre-emptively) | n/a | n/a | n/a | n/a | n/a | — |
| 15 | who_caregiver_training | WHO-CST-PARTICIPANTS-2022, WHO-CST-INTRO-2022 | "who"/"người chăm sóc" | ✓ | ✓ (gate added pre-emptively) | n/a | ✓ (2 sources) | ✓ names only sessions 6-9, explicitly | n/a | n/a | — |
| 16 | ayres_si_definition | ASD-SUP-PMC7726187 | "ayres" | ✓ | ✓ (gate added pre-emptively) | n/a | n/a | n/a | n/a | n/a | — |
| 17 | adolescence_asd | ASD-OA-PMC12593641, NIH-NIMH-TEEN-BRAIN | "dậy thì"/"thiếu niên" | ✓ | ✓ (gate added pre-emptively) | n/a | ✓ (2 sources) | n/a | n/a | n/a | — |

**Note on `vaccine_myth`**: `ASD-OA-PMC12620806` is also the trigger source for the GFCF-diet myth
template added in T5.2 — wait, re-checked: GFCF diet was templated under `vaccine_myth`'s own source in
T5.2's `_TOPIC_TEMPLATES`? Re-verified directly in code: **no**, `vaccine_myth` is the only old template
using `ASD-OA-PMC12620806`; the GFCF-diet question (q060/qe075) was never given its own template — it
answers via `vaccine_myth`'s text being inapplicable and the question actually falls through to
`extractive_fallback` in the current code (re-verified live: `qe075` is not among the 23 templated
questions in this task's baseline). This note corrects an assumption that would have been wrong if left
unchecked — direct verification, not an inference.

## Conclusion of Phase 1

Before this phase, 6 of 17 templates could in principle fire on source co-occurrence alone. Two were
proven to do so with a realistic, reproducible scenario; the other 5 were fixed under the same
pattern without each needing its own proof, which is disclosed as a judgment call (fixing a class of
defect from 2 confirmed instances) rather than 6 independently confirmed bugs. All 17 templates now
require a topic-specific query term except the single designated catch-all.
