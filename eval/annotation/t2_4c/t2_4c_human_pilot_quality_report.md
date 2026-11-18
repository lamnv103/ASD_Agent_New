# T2.4-C Human Pilot Quality Audit

**Conclusion: `PILOT_BLOCKED`**

## Scope and evidence

The audit checked the available blind pilot CSV and expert review package. A completed file returned by the expert was not present in `eval/annotation/t2_4c/`, and a workspace search under `eval/` found no T2.4-C pilot return file. The existing pilot CSV is still blank. No expert annotations were created or inferred for this report.

## Checks

| Check | Result |
|---|---|
| Pilot input contains 40 rows | Pass: 40 |
| Pilot `review_id` values are unique | Pass: 40 unique |
| Every pilot ID is in the expert review package | Pass |
| Expert grade and rationale validity in returned results | Not assessable: no returned results file |
| Evidence spans match chunks in returned results | Not assessable: no returned results file |
| Reviewer ID/date and status consistency | Not assessable: no returned results file |
| AI/retriever information in the returned expert file | Not assessable: no returned results file |
| Question and chunk preserved in pilot input | Pass: `question_vi`, title, section, page, and content exactly match the package |
| Human fields in the pilot input remain blank | Pass |
| AI results unchanged | Pass: complete-results SHA-256 matches the previously recorded value |

The pilot CSV has only these columns: `review_id`, `question_vi`, `document_title`, `section`, `page`, `content`, `expert_grade`, `expert_rationale`, `expert_evidence_span`, `evidence_sufficiency`, `context_limitation`, `conflict_flag`, `review_status`, `reviewer_id`, and `review_date`. It contains no AI label, AI rationale, retriever, rank, score, or stratum column. This verifies the blind input, not an absent returned file.

## Grade distribution and process analysis

The grade distribution cannot be calculated: there are no completed expert grades to count. This is not a zero-grade result. The expert’s difficulties, unclear rubric points, and cases requiring discussion or adjudication are also unknown until the expert return is available.

The 40-row file is ready for process-only use, but the actual review and return workflow has not been exercised. Therefore, feasibility of completing all 875 reviews cannot yet be concluded from pilot evidence. Do not use this file to estimate AI accuracy or claim dataset representativeness.

## Integrity records

- Pilot CSV: 40 rows; SHA-256 `345f23919d6789b9ef141e6ad8e304bba50d27efbc4264853ed259586941b9d1`.
- Expert review package: SHA-256 `ce78ed103442269e3285fbd31172d251b2cd0ea2f42759600a3c4a35d4e4cc3a`.
- Complete AI results: SHA-256 `bc96c09ee0e2133b2ab0edfe7e316362a322e9fbb277391bc2cbb0cf9b8a0f0f`.
- Original 64 AI results: SHA-256 `ecf732798d874c6264fcfa2207c57bd79f3f7beec189bcb26da00b46ada0f6b8`.

The AI results hash is unchanged from the recorded pilot handoff audit. This audit did not write to the database, corpus, package, pilot CSV, or AI results. The coordinator reveal file was not opened.

## Required next step

Place the expert’s completed 40-row CSV in the workspace as a separate returned artifact, preserving the original blind pilot CSV. Then rerun all requested checks against the return and package. Until that file is available and passes validation, the pilot is `PILOT_BLOCKED` and the full 875-row review should not be treated as process-validated.
