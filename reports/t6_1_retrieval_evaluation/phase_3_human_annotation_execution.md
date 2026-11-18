# T6.1 Phase 3 - Human annotation execution status

**Status: `PENDING_HUMAN_REVIEW`.** The annotation package and instructions are prepared; no human annotator results were supplied in this workspace. No human judgments were created, inferred, or approved by the system agent.

Two independent core sheets (1,631 pairs each) and two separate variant sheets (230 pairs each) have blank grade, rationale, evidence, reviewer, disagreement, and adjudication fields. All rows currently say `PENDING_HUMAN_REVIEW`. No completed annotations, disagreement rate, inter-annotator agreement, or adjudication report can be presented.

The independent annotators should return their assigned CSVs with original `annotation_id`, `query_id`, and `chunk_id` intact. Completed numeric grades must be one of 0-3; where not assessable, leave numeric grade blank and use `NEEDS_ADJUDICATION` with a reason. Do not merge the two sheets before both submissions are locked. After intake, validate exact pair coverage and evidence spans against source content, then calculate agreement and prepare adjudication queue.

**Deliverables pending:** actual human annotations, inter-annotator disagreement report, adjudication report (if disagreements occur), and final human-judged metric report. The current pool is ready to hand to qualified reviewers subject to calibration and secure transfer arrangements.

## Artifact generation and validation

- Build command: `.venv\Scripts\python.exe reports/t6_1_retrieval_evaluation/build_t6_1_artifacts.py` (read-only authorized-view SELECT; no external embedding).
- Structural validation command: `.venv\Scripts\python.exe reports/t6_1_retrieval_evaluation/validate_t6_1_artifacts.py`.
- Result: `PASS_STRUCTURAL_VALIDATION`; details in [`artifact_validation_report.json`](artifact_validation_report.json). This validates package structure and hashes only; it is not a human relevance or application test.
- The exact builder script hash is recorded in [`artifact_build_summary.json`](artifact_build_summary.json).
