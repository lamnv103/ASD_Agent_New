# T2.4-C Human Expert Pilot Handoff

**Purpose label:** `PROCESS_ONLY_PILOT`  
**Conclusion:** `READY_FOR_PROCESS_PILOT`

## 1. Pilot objective

Use the 40-row blind CSV to check that an expert can understand the task, apply the relevance rubric, record evidence consistently, and return a complete file. This pilot assesses the review process only. It does not estimate AI accuracy or establish that the pilot represents the 875-row package.

## 2. Pilot size and review IDs

The existing pilot file contains 40 rows and 40 unique IDs. All IDs occur in the expert review package. The CSV was checked against that package: question, title, section, page, and chunk content match exactly. The file contains no AI label, AI rationale, retriever, rank, score, or stratum fields. All human review fields are blank.

Keep `review_id` unchanged. Pilot IDs:

```text
81EEC589A04849BD
D42ECCFEF68B44FE
D60032655FB24E36
5FE9C8AA9A88456B
7432E56541BD48AD
5D50634A5D7647A4
CE95954BE6E64C78
E582324F34ED431D
1B34B471C0064CCF
F0FAA42C5D1D4E8B
4EA3FE1DAD694C38
F4E19AA5DC0A4A0A
2CF28F2448644848
2E30304367504132
AE558F390EC54447
0C99C0EF31BE44F6
9F05895DCBD04F64
BDE16770179B41A9
06C6354E8DA74F09
6D1D952B5E044822
E88253A62E874992
BF02822305524EDE
E573EF61AF9C473F
F56E2BDEA9724F5F
60EAB5BAF28A4B6E
391D6FA7EF4D4D5C
5A8E041422DF4517
29277E9ED305410E
FA4535D54FF546D5
C4C8F9C2490C4F1B
A3099F90073B4E44
D8A1DA6A332F4B84
53694477808D4EBD
29CE5EBE6BA34340
CD95F180FF2C4FF3
365B4A7165CF4CEF
483EC825A6C241E1
31C0C8D98A364AC1
3718B526C19F45D8
0534D198A37C4690
```

## 3. Instructions for the expert

### Goal and scope

Judge how well the supplied passage supports the supplied question for retrieval evaluation. Judge only the content shown in the row. This is not a clinical assessment, medical advice review, or validation of a diagnosis or treatment.

### Relevance rubric

- **3:** The chunk directly supports the question.
- **2:** It is relevant and useful, but supports only part of the question.
- **1:** It is on the same topic but offers weak support.
- **0:** It does not contribute to answering the question.
- **`needs_review`:** The content is unclear, corrupted, incomplete, or cannot be judged reliably.

### Recording guidance

- Write a concise rationale that connects the grade to what the chunk says. For grade 0, state that the chunk does not provide useful support; do not rely on a matching title or keyword alone.
- Copy `expert_evidence_span` as an exact, contiguous verbatim substring of `content`. Do not paraphrase, correct spelling, translate, or repair source text. Leave it blank if no supporting span exists.
- If only part of a multi-part question is supported, identify that limit in `context_limitation` and use a partial evidence sufficiency value.
- If the content cannot be assessed reliably, use `needs_review` and explain why. Do not guess a grade or reconstruct missing evidence.
- Do not use AI labels, AI rationales, or AI status to guide the independent judgment. Freeze and return the human file before any AI comparison.

## 4. Fields to complete

| Field | What to enter |
|---|---|
| `expert_grade` | `0`, `1`, `2`, `3`, or `needs_review` |
| `expert_rationale` | Short reason for the grade |
| `expert_evidence_span` | Exact supporting text from the chunk, or blank when absent |
| `evidence_sufficiency` | `sufficient`, `partial`, or `insufficient` |
| `context_limitation` | Missing scope/context, or why the item needs review |
| `conflict_flag` | `true` if the chunk itself contains material conflicting claims; otherwise `false` |
| `review_status` | `completed` or `needs_review` |
| `reviewer_id` | Assigned expert identifier |
| `review_date` | Date reviewed, `YYYY-MM-DD` |

Keep `review_id` and all question/chunk fields unchanged. For `expert_grade=needs_review`, set `review_status=needs_review` and explain the issue. Do not add question IDs, AI labels, stratum, rank, retriever, or score.

## 5. Return process

1. The coordinator gives the expert only [the pilot CSV](t2_4c_human_review_pilot_blind.csv) and this handoff.
2. The expert completes the fields above without seeing AI outputs and saves a separate returned copy. Do not edit the source package or AI results.
3. The expert returns the completed CSV through the project’s approved secure channel. The coordinator records its receipt date and SHA-256, then checks row count, unique IDs, valid values, required fields, and exact evidence spans against the unchanged package.
4. Freeze the human pilot file before comparing it with AI results. Record disagreements and usability/rubric issues separately. Any rubric changes must be approved and versioned before the full review; do not retroactively alter the frozen pilot.

## 6. Pilot completion criteria

The process pilot is complete when all 40 IDs are returned exactly once; each row has a reviewer ID, date, status, and rationale; grades/status values are valid; evidence spans are verbatim or blank when unsupported; `needs_review` cases explain the limitation; and the expert confirms the instructions and fields were usable. Report counts and process issues only. Do not report this pilot as an AI accuracy estimate or a representative sample result.

## 7. Method limits

The pilot’s balance across AI consensus and disagreement strata has not been verified. No stratum was inferred from row content or ID order, and no reveal file was opened. This is a process-only sample and must not be described as representative of all 875 cases. Retrieval relevance is not medical validation. AI review outputs remain AI-only; the pilot creates no expert labels until a qualified human completes and returns it.

## 8. Before reviewing all 875 cases

- Confirm reviewer qualifications, language ability, secure handling, and workload.
- Complete and freeze the process pilot; resolve ambiguous rubric instructions and version any approved changes.
- Freeze and hash the 875-row package, final rubric, and blank review template.
- Define whether all 875 receive one independent expert judgment and set a second-reviewer subset and adjudication process in advance.
- Establish handling for missing rows, invalid values, exact evidence mismatches, and `needs_review` records.
- Keep human judgments separate from immutable AI results. Compare only after human judgments are frozen, and preserve reviewer type and provenance.
- Review q016, q041, and q057 at question level in addition to pair-level labels; keep their decisions unresolved until experts complete them.

## 9. Audit evidence

The preparation audit found 40 pilot rows, 40 unique IDs, all IDs present in the expert review package, exact question/chunk field matches, and all human fields blank. No AI/rationale, rank, score, retriever, or stratum column is present. The AI results file was not modified; its SHA-256 at audit was `bc96c09ee0e2133b2ab0edfe7e316362a322e9fbb277391bc2cbb0cf9b8a0f0f`.
