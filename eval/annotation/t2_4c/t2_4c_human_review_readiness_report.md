# T2.4-C Human Review Readiness Report

**Conclusion: READY_WITH_CONDITIONS**

## 1. Audit results

- Package: 875 rows; 875 unique `review_id` values.
- Complete AI results: 875 rows; 875 unique IDs; package/result ID sets match: **True**.
- CSV template: 875 rows; 875 unique IDs; package/template ID sets match: **True**.
- Duplicate IDs: package 0; AI results 0; CSV template 0.
- Human fields are blank in package: **True**; blank in CSV template: **True**.
- AI review types: `{"ai_model": 875}`; records marked human reviewed: 0.
- `needs_review` records: 126; list matches complete results: **True**.
- AI results file SHA-256: `bc96c09ee0e2133b2ab0edfe7e316362a322e9fbb277391bc2cbb0cf9b8a0f0f`; matches recorded validation report and retains all original 64 records: **True**.
- Structural issues: pilot is provisional: A/B consensus/disagreement membership cannot be verified without an authorized blind stratification map. The AI result file and templates were not modified.

### Question-level templates

| Question | Present | Unresolved | Reviewer fields blank | Text matches blind package |
|---|---:|---:|---:|---:|
| q016 | True | True | True | True |
| q041 | True | True | True | True |
| q057 | True | True | True | True |

All three question-level records remain unresolved, as intended. Their question text matches the blind package; no expert decisions or evidence have been entered.

## 2. Pilot packet

A 40-row blind pilot was staged at `t2_4c_human_review_pilot_blind.csv`. It contains 12 records selected from AI `needs_review` and 28 from other AI review statuses, then shuffled. The packet preserves `review_id`, question, chunk context, and blank human fields; it contains no AI grade, rationale, reviewer metadata, selection source, rank, retriever, or score.

Pilot IDs (listed without selection strata):

`81EEC589A04849BD`, `D42ECCFEF68B44FE`, `D60032655FB24E36`, `5FE9C8AA9A88456B`, `7432E56541BD48AD`, `5D50634A5D7647A4`, `CE95954BE6E64C78`, `E582324F34ED431D`, `1B34B471C0064CCF`, `F0FAA42C5D1D4E8B`, `4EA3FE1DAD694C38`, `F4E19AA5DC0A4A0A`, `2CF28F2448644848`, `2E30304367504132`, `AE558F390EC54447`, `0C99C0EF31BE44F6`, `9F05895DCBD04F64`, `BDE16770179B41A9`, `06C6354E8DA74F09`, `6D1D952B5E044822`, `E88253A62E874992`, `BF02822305524EDE`, `E573EF61AF9C473F`, `F56E2BDEA9724F5F`, `60EAB5BAF28A4B6E`, `391D6FA7EF4D4D5C`, `5A8E041422DF4517`, `29277E9ED305410E`, `FA4535D54FF546D5`, `C4C8F9C2490C4F1B`, `A3099F90073B4E44`, `D8A1DA6A332F4B84`, `53694477808D4EBD`, `29CE5EBE6BA34340`, `CD95F180FF2C4FF3`, `365B4A7165CF4CEF`, `483EC825A6C241E1`, `31C0C8D98A364AC1`, `3718B526C19F45D8`, `0534D198A37C4690`

The private selection manifest is `t2_4c_human_review_pilot_internal_manifest.json` and must not be shared with reviewers. It records only the pilot construction, not A/B labels. The preparation note says the full package contains 662 disagreement cases and 213 sampled consensus cases, but no permitted file maps these strata to IDs. No reveal file or Agent A/B labels were inspected. Therefore this pilot cannot yet be certified as including representatives of both A/B strata; obtain a data-custodian-generated blind stratum-balanced ID list before reviewer distribution, or approve this pilot as an explicitly non-stratified usability pilot.

## 3. Instructions for reviewers

1. Review the question and supplied chunk independently. Do not consult AI labels or rationale before submitting and freezing the human judgment.
2. Assign `3` when the chunk directly supports the question; `2` when it supplies useful but partial support; `1` when it is on the same topic but weakly supportive; `0` when it does not contribute; use `needs_review` when the content is unclear, corrupted, incomplete, or cannot be judged reliably.
3. Explain the decision briefly. Copy evidence exactly from the chunk; leave evidence blank when none supports the judgment. Do not repair source text or infer evidence from a title.
4. Record reviewer ID, review date, and review status. Preserve the opaque `review_id`; do not add qid, A/B labels, rank, retriever, or score.
5. Submit and freeze the independent pilot judgments before any comparison with AI results. Resolve the three question-level decisions separately and document rationale and evidence.

## 4. Method limits

- AI output is AI-only; no record has human expert validation. The 126 `needs_review` records are candidates for particular attention, not expert decisions.
- The continuation provenance identifies lexical triage; structural checks do not establish semantic correctness. Human reviewers should assess all pilot items independently, not just flagged rows.
- Without the prohibited reveal mapping, the pilot's A/B disagreement and consensus mix is unknown. The selection categories above describe only AI review status.
- A single expert pilot provides no inter-rater reliability estimate. For full review, use at least one qualified independent expert for every item; add a second independent reviewer for a prespecified subset and adjudicate disagreements.
- q016, q041, and q057 require question-level decisions beyond pair relevance. Keep them unresolved until separately assessed.

## 5. Conditions before reviewing all 875

- Confirm the reviewer has relevant ASD evidence appraisal expertise and can review the language/content used in the package.
- Resolve the pilot sampling condition: receive a blind, authorized mapping/list covering A/B disagreement, A/B consensus, and `needs_review`, or explicitly redefine this as a non-stratified pilot.
- Freeze and hash the rubric, package, and blank template; do not edit chunk text or rubric during review.
- Run the pilot, freeze human judgments, compare with AI only afterward, document rubric ambiguities, and approve any rubric changes before the full review.
- Define second-reviewer coverage, adjudication rules, missing/`needs_review` handling, and data access controls before the full 875-row pass.
- Keep AI results immutable and maintain human results in a separate file with clear reviewer type and provenance.

## 6. Status rationale

`READY_WITH_CONDITIONS` is assigned because structure and blinding checks pass, but the stated requirement for a pilot representative of A/B disagreement and consensus cannot be demonstrated without an authorized blind stratum mapping. No AI labels have been exposed in the reviewer packet, and no human labels have been created.
