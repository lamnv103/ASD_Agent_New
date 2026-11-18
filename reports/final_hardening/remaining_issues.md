# Remaining Issues (T4)

## Critical path to `DEMO_READY_FOR_USER_VALIDATION`

1. **English-language extractive fallback is the real blocker, not a cosmetic issue.** Most answerable
   questions outside the 7 templates show literal (often English) excerpts to a Vietnamese-speaking user.
   Two independent ways to close this, neither executable in this task:
   - Expand template coverage substantially (more hand-authored Vietnamese paragraphs, each gated behind
     its real trigger source, following the exact method in `phase_3_answer_quality.md`) — safe,
     incremental, no new authorization needed, but labor-intensive one topic at a time.
   - Get T2.6 authorization for a translation/synthesis step (an LLM or a dedicated translation API) —
     faster, but requires the project owner's approval (`reports/project_repair/t2_6_approval_request.md`
     equivalent would need to be re-raised for this specific, narrower use case: Vietnamese translation
     of already-approved, already-retrieved evidence, not new document/query processing). **Not attempted
     in this task** — no live external call was made.
2. **q033-class ADHD-vs-ASD lexical confusion** (`phase_6_failure_analysis.md`) — needs real semantic
   understanding (same authorization gate as above) to resolve fully; a lexical mitigation was
   considered and rejected as unreliable (see `phase_2_evidence_gate_audit.md`).

## Hard blockers (unchanged, require authorization not sought or granted in this task)

3. T2.6 `APPROVAL_REQUIRED` — cache-only remains in force; 48/105 questions in the Phase 5 content-eval
   set are blocked purely by this, not by a quality defect.
4. ASD-domain clinical/educational expert review — not performed (see `final_acceptance_report.md`).

## Soft limitations (disclosed, lower priority)

5. Template coverage is 7 topics; extractive fallback is correct-but-plain for everything else.
6. Multi-part questions are not decomposed into per-part answers.
7. No contradiction detection between sources (considered, rejected as unreliable without an LLM).
8. No true semantic citation validation — only structural validation plus a lexical support-strength hint
   (`support_type`), explicitly not claimed as more (`phase_4_source_quality.md`).
9. No browser/device/accessibility-tool testing exists for the frontend (`phase_7_frontend_quality.md`).
10. The `eval/datasets/asd_qa_eval_v2.jsonl` routing-related numbers have disclosed test-set leakage
    (vocabulary was extended after seeing its failures) — its answer-quality observations remain clean,
    since no template was altered in response to it.

## What was fixed this task (not blockers anymore)

- Self-medication-adjustment questions with no drug named (previously misrouted or cache-blocked instead
  of refused) — now refused before any retrieval attempt.
- Melatonin dosing question — now covered by the refusal.
- "Joint attention," "sở thích hạn hẹp," "không chỉ tay," "chưa nói" vocabulary gaps that sent real ASD
  questions to `out_of_scope` — fixed (with disclosed leakage, see above).
- q061-style milestone/signs evidence mixing — fixed via the new glossary term + existing
  direct/indirect classification.
- Router's confidence is now explicit (`high`/`low`) instead of hidden behind one always-confident
  decision.
