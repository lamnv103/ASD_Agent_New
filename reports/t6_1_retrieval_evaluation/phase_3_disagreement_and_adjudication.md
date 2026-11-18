# T6.1 - Disagreement and adjudication status

No human submissions are present. Therefore disagreement count, agreement statistics, and adjudication outcomes are **not available**. No disagreements are presumed absent.

When both locked submissions arrive:

1. Match rows by `annotation_id` and verify that both have the same 1,631 core pairs (and separately the same 230 diagnostic variant pairs).
2. Validate each grade/status, rationale, reviewer ID, and exact evidence-span substring. Preserve submitted files unchanged; make a separate normalized analysis copy if needed.
3. Report numeric exact agreement, weighted Cohen's kappa with quadratic weights plus its limitations, grade-wise confusion matrix, and counts of non-assessable/blank records. Do not fold needs-adjudication into numeric grades.
4. Queue grade disagreements, contradiction flags, evidence disputes, and either annotator's needs-adjudication cases for an independent adjudicator. Preserve both initial grades and record adjudicator ID, decision, rationale, and date.
5. Keep system provenance hidden until judgments and adjudication are locked. Then unblind to conduct retrieval-specific error analysis.

No statistical value or adjudication result is claimed in this report.
