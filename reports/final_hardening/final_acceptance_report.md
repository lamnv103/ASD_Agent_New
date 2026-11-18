# Final Independent Acceptance Report — T4 Hardening

**Final status: `PARTIAL_HARDENING`**

Not `DEMO_READY_FOR_USER_VALIDATION`. Real, verified progress was made on 13 of the 15 acceptance
conditions in the task brief (§16) — but conditions 6 and 7 ("câu trả lời tiếng Việt đúng trọng tâm,"
"không còn là danh sách raw chunks") are only **partially** met, for a reason that is structural, not a
bug: most of the corpus is English-language source text, and only 7 of the many question topics have a
hand-authored Vietnamese template. Every other answerable question falls to `extractive_fallback`, which
shows real, honestly-labeled, numbered excerpts — but those excerpts are frequently **in English**, not
Vietnamese, because that is what the underlying source document is written in. This is an improvement
over T3 (no bare `C1`/`C2` codes, real citations, evidence filtering) but it does not satisfy "câu trả
lời tiếng Việt đúng trọng tâm" for the majority of answerable questions. Raising the status to
`DEMO_READY_FOR_USER_VALIDATION` without fixing this would be the kind of self-graded inflation the task
explicitly prohibits.

## Scoring (0–5, with evidence — automated + internal manual review only, see §3)

| Criterion | Weight | Score | Evidence |
|---|---:|---:|---|
| Độ chính xác câu trả lời | 25% | 3.5 | 7 templates individually fact-checked against their trigger evidence (`phase_3_answer_quality.md` §9.1, 0 corrections needed); but the documented q033 ADHD/ASD lexical-confusion case (`phase_6_failure_analysis.md`) is a real, unresolved accuracy risk for non-templated answers |
| Đúng trọng tâm | 20% | 3.5 | Evidence Gate's `support_type`/`age_mismatch` classification (`tests/unit/test_evidence_gate.py`, 17 tests) measurably narrows evidence to on-topic chunks (e.g. q061 went from 5 mixed chunks to 1 correctly-targeted chunk this task); q033 remains an open miss |
| Độ đầy đủ | 15% | 3.0 | Templates are short-but-complete for their scope (`phase_3_answer_quality.md` §9.4); multi-part questions are not decomposed (no template covers compound questions — `remaining_issues.md`) |
| Retrieval và Evidence | 15% | 4.0 | `phase_2_evidence_gate_audit.md`: direct/indirect/generic classification, age-mismatch detection, all 4 original safety-sensitive cases now correctly handled, re-verified live |
| Citation và nguồn | 10% | 4.0 | `source_url` present and validated (`tests/unit/test_citation_validation.py`, 6 tests); Level 2 semantic validation explicitly stated as partial, not claimed as complete (`phase_4_source_quality.md`) |
| Diễn đạt tiếng Việt | 5% | 2.5 | Templates: natural, correct Vietnamese. `extractive_fallback` (the majority of answerable, non-templated questions): literal excerpts, often in English — this pulls the average down significantly, and is named here rather than averaged away |
| An toàn | 10% | 4.5 | Dosing refusal now fires **before** any retrieval attempt, covers drug-named and un-named phrasings (`tests/unit/test_answer_generator.py`, 3 new parametrized cases); unproven-cure caution; insufficient-evidence honesty for epilepsy/stem-cell/risperidone — all re-verified live this task |
| **Weighted total** | 100% | **3.6 / 5 (72%)** | — |

## Distinguishing evaluation types (per the task's explicit requirement)

- **Automated evaluation**: 406 pytest tests (358 unit + 48 integration), `ruff check` clean, T2.3
  regression 66/66 identical, 2 independent eval-harness scripts (`scripts/eval_intent_routing.py`:
  102/105 = 97.1%; `scripts/eval_asd_qa.py`: 57/105 answerable under cache-only constraints). All numbers
  in this report trace to one of these.
- **Human review**: performed by this task's author(s) — manual template fact-checking
  (`phase_3_answer_quality.md`), manual safety-policy table construction for the 4 sensitive topics
  (`phase_2_evidence_gate_audit.md` §8.3), manual frontend checklist walkthrough (`phase_7_frontend_quality.md`).
  This is a competent technical review, **not** a substitute for domain expertise.
- **ASD-domain expert review**: **not performed.** No person with confirmed ASD clinical/educational
  expertise reviewed any output in this task. The role described in the task brief's §1 item 7 ("Chuyên
  gia nội dung ASD... trong phạm vi năng lực được xác nhận") was not filled by an actual qualified person
  — this report does not claim otherwise, and no score above should be read as expert-validated.
- **Clinical validation**: **not performed and not claimed.** Nothing in this project has been validated
  as a clinical or diagnostic tool. The safety notice banner, unchanged since T3, states this on every
  page and every response.

## What `PARTIAL_HARDENING` means concretely

Safe, tested, and ready to **demo as a research prototype** with the understanding that: (a) 7 topics get
a polished Vietnamese answer, (b) most other answerable topics get an honestly-labeled but English-
excerpt-heavy fallback, (c) ~46% of a representative 105-question set is blocked outright by the
cache-only constraint (T2.6), and (d) one specific, named accuracy limitation (q033) remains open. None of
this is hidden — seeing all four is exactly what distinguishes `PARTIAL_HARDENING` from a status that
would overclaim readiness.
