# T5.1 Final Report — Vietnamese Answer Gap Analysis

**Status: `T5_1_ANALYSIS_COMPLETE`**

Analysis only. No code, corpus, or database was changed. `app/retrieval/evidence_gate.py`,
`app/answer/answer_generator.py`, `app/router/classifier.py`, and `app/nlp/text_match.py` were read and
traced against live data, not edited. T2.6 remains `APPROVAL_REQUIRED`; `ASD_DEMO_MODE=true`; all three
`ASD_ENABLE_LIVE_*` flags remain `false` (re-verified: `app/config.py` still raises `ConfigError` if any
is set `true`). The Docker container (`asd-rag-v2-db`) was already running and was not started, stopped,
or reconfigured. No Git action was taken.

All numbers below are computed directly from `eval/reports/t5_1_audit_raw.json` (the output of
`scripts/audit_t5_1_answer_coverage.py` run live against the real database during this task), not
estimated or copied from prior reports without re-verification.

## Direct answers to the task's required questions

**Bao nhiêu câu hỏi có thể trả lời bằng tiếng Việt với template hiện tại?**
**12 / 105** (= 12 of the 55 currently-cached/answerable questions). These are exactly the 12 questions
listed in `topic_gap_matrix.md` Group A, using the 7 templates that existed before this task — no new
template was added.

**Bao nhiêu câu bị fallback?**
**25 / 105** (= 25 / 55 answerable). Of these, **23 are entirely English-language excerpts and 2 are
"mixed"** (English prose containing Vietnamese proper nouns, substantively still English — see the
caveat in `answer_coverage_audit.md`). **0 of the 25 fallback answers are in Vietnamese.**

**Bao nhiêu câu có evidence tốt nhưng chưa có template?**
**20 / 105** (Group C in `topic_gap_matrix.md`) — fallback cases whose evidence includes at least one
`direct` or `indirect` (not purely `generic`) supporting chunk. The remaining 5 fallback cases (Group E)
have only `generic` (similarity-only, topically-unconfirmed) evidence and are not good template
candidates as-is.

**Chủ đề nào nên triển khai trước?**
The 18-question Tier 1 list in `template_expansion_plan.md` (Group C minus the 2 ADHD-confusion cases),
with **speech-delay-vs-ASD (qe034) prioritized within that tier** for safety reasons (it is exactly the
"chậm nói ≠ tự kỷ" distinction flagged as a correctness risk in the original independent expert
evaluation), followed by early-signs-by-age, screening-tool (M-CHAT/ADOS), and intervention-topic
templates — see the full priority table and per-topic notes there.

**Có thể hoàn thành bao nhiêu phần mà không cần xin quyền mới?**
All of it, with one exception. The entire Tier 1 template list (18 questions), the Evidence-to-Answer
architecture's Stages 1/3/4/5/7 (normalization, sentence construction, citation mapping, uncertainty
display, extractive fallback), and the q033 lexical mitigation option (requiring the ASD anchor to
appear in the chunk, not just the query) are all pure lexical/template work on already-retrieved,
already-approved evidence — no live Cohere, no LLM, no new data processing. **The one exception**: Group
F (50 cache-blocked questions) cannot be touched without either T2.6 authorization for live query
embedding or an authorized expansion of the existing query cache.

**Những phần nào cần chuyên gia ASD?**
Per `topic_gap_matrix.md` Group G: (1) the two ADHD-confusion templates (qe045, qe081) — whether to
accept the trade-off of excluding legitimate ASD+ADHD-comorbidity content; (2) qe033 (sex differences in
presentation) — whether a generic/partial answer is acceptable or this should stay "insufficient
evidence"; (3) wording review of the vaccine-myth and GFCF-diet-myth templates for a lay Vietnamese
audience; (4) wording review of the medication-refusal message's clinical terminology; (5) whether the
epilepsy-comorbidity "insufficient evidence" result reflects a real corpus gap that should be flagged for
future source expansion.

**Những phần nào bắt buộc phải chờ T2.6?**
Group F in full (50 of 105 questions, ~48% of this representative set) — any question not already in the
query cache. This is unchanged from T4's finding and is re-confirmed, not re-estimated, by this task's
live run.

## What this analysis adds beyond the T4 reports

1. **Precise quantification** where T4 only had qualitative statements: 12/55 templated, 25/55 fallback
   (23 pure-English), 50/105 cache-blocked — T4's `final_acceptance_report.md` named the English-fallback
   problem but did not count it.
2. **A corrected, authoritative Group-C count (20, not an earlier hand-count of 17)** — found and fixed
   during this task by re-deriving the count programmatically from the raw audit data instead of
   hand-tallying a table, a useful methodological lesson recorded here rather than silently corrected.
3. **A traced, evidence-level explanation of exactly why q033-class failures happen** (the section
   heading "Parent education and support" literally contains the word "parent," which is the query's only
   specific term and is not ASD-discriminating) — deeper than T4's "needs semantic understanding"
   statement, with a concrete, bounded lexical mitigation option and its known trade-off named explicitly.
4. **A concrete, evidence-grounded (not hypothetical) architecture proposal** with 5 worked examples, each
   built from real retrieved text, including one (the sleep-table example) that surfaces a new design
   requirement — table-structured evidence — not previously identified in T3/T4.

## Final status justification

`T5_1_ANALYSIS_COMPLETE`, not `T5_1_PARTIAL`: all 6 required deliverables were produced, grounded in a
live re-run of the actual pipeline (not assumed from old reports), with numeric cross-checks, real code
inspection, and a reasoned, risk-flagged implementation plan. Nothing here declares
`DEMO_READY_FOR_USER_VALIDATION` or any clinical claim — this report's scope is strictly "where is the
gap and what would closing it require," per the task brief.
