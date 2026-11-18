# T2.4-C preparation status ? 2026-11-17

**Status: prepared for an independent human expert; no expert adjudication has been performed.** This AI system cannot claim a professional reviewer identity or label its own judgments as expert-reviewed.

- Blind review package: 875 pairs = all 662 disagreement/review cases plus a reproducible random sample of 213/2,129 AI-agreed pairs (seed 20261117).
- Reviewer sees question text, passage, title/section/page context and blank expert fields. Reviewer does not see question IDs, Agent A/B grades, disagreement stratum, source/chunk IDs, retrieval system, rank or score.
- After independent grading is frozen, a separate reveal file maps review IDs to qid and A/B grades. Keep `coordinator/t2_4c_reveal_after_review.jsonl` from the reviewer until then.
- Three question-level templates are provided for q016, q041 and q057; decisions remain unresolved.
- The requested `chunk_id` field is replaced by an opaque `review_id` because this preparation did not access the prohibited coordinator/source key.

A human reviewer must fill `reviewer_id`, `review_date`, grade, rationale, exact evidence span, sufficiency, context limitation, conflict flag and review status. AI output from T2.4-B is not expert validation.
