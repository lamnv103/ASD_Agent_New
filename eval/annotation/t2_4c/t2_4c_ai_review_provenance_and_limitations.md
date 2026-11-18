# T2.4-C AI review provenance and limitations

Continuation generated 2026-11-17 for the 811 IDs absent from the pre-existing 64-record file. The original file was read and retained unchanged; the complete 875-row output is a separate file.

- Reviewer type: AI model for all rows; no human expert review is represented.
- Existing 64 rows retain their original fields and provenance. Their record does not include model, prompt, or version fields; none were inferred.
- Continuation provenance: GPT-6 session (exact deployment/version unavailable); task instructions plus 0-3 rubric; no standalone prompt/version identifier was supplied.
- Continuation method: conservative lexical triage v1. Chunk text is used for evidence selection; title/section are not treated as evidence.
- Evidence spans are copied verbatim from the corresponding chunk. Grades are provisional and lexical coverage does not establish semantic correctness.
- `needs_review` records need human confirmation, especially possible negatives, ambiguous cases, or damaged/incomplete content.
- The 0-3 scale used: 3 direct answer evidence; 2 substantial contribution; 1 partial/contextual contribution; 0 no contribution. Grade -1 is not used.
- Status `AI_REVIEW_COMPLETE_PENDING_HUMAN_EXPERT_REVIEW` describes complete structural coverage only; it does not claim T2.4-C complete or expert adjudication.
