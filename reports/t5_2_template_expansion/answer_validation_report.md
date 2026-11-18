# T5.2 Phase D — Answer Validation Report

Each of the 11 newly-templated questions, checked live against the real database, across the 7 required
dimensions. "Citation" was additionally verified structurally via `tests/integration/test_chat_api_db.py
::test_new_t5_2_template_examples_get_real_vietnamese_answers_with_valid_citations` (real `source_url`
present for every citation, citations list matching evidence list 1:1).

| Question | Relevance | Factual support | Completeness | Language | Uncertainty shown | Citation | Safety |
|---|---|---|---|---|---|---|---|
| qe028/qe029 (signs by age) | Direct — lists exactly the age-tagged signs the evidence names | Every bullet traces verbatim to `CDC-ASD-SIGNS` | Partial by design — only age-tagged items shown, with an explicit "một dấu hiệu đơn lẻ không đủ" caveat | Natural Vietnamese + English sign text as-is (CDC's own wording, not translated) | Yes — the single-sign caveat | 1 source, real URL | Explicitly avoids implying a single sign = diagnosis |
| qe036 (M-CHAT) | Direct | Sensitivity/specificity/cutoff all verbatim from source | Complete for the question asked | Vietnamese + kept term "M-CHAT-R/F" | "Công cụ sàng lọc, không phải chẩn đoán xác định" | 2 sources, real URLs | No diagnostic claim made |
| qe037 (ADOS-2) | Direct | Reliability range verbatim | Complete | Vietnamese + kept term | "không phải công cụ tự làm tại nhà" | 2 sources, real URLs | No diagnostic claim made |
| qe044 (NDBI) | Direct | Definition + AAC finding both verbatim | Complete | Vietnamese + kept term "NDBI"/"AAC" | None needed — both claims are well-supported, stated as such | 2 sources, real URLs | No safety concern |
| qe047 (sleep, table) | Direct for the one claim made | The one cited recommendation traces exactly to the table's "Strong"-tier row | **Deliberately incomplete** — says so explicitly ("đây chỉ là một trong nhiều khuyến nghị") | Vietnamese | Yes, explicit partial-coverage statement | 1 source, real URL | No medication/dosing mentioned |
| qe048 (melatonin) | Direct | "Well established" phrase verbatim | Complete for an efficacy-only question | Vietnamese | "Không phải hướng dẫn liều dùng" | 1 source, real URL | No dose stated (deliberately removed from source) |
| qe049 (school inclusion) | Direct | Both findings (accessibility up, friendship not necessarily) verbatim | Complete — both sides of the finding included | Vietnamese | The "không nhất thiết" clause is the uncertainty signal | 1 source, real URL | No overclaim of "inclusion works" |
| qe057 (WHO caregiver) | Direct | Session numbers/topics verbatim | **Deliberately incomplete** — says "một phần, không phải toàn bộ" | Vietnamese + kept program name in English | Explicit partial-coverage statement | 2 sources, real URLs | No safety concern |
| qe024 (Ayres SI definition) | Direct for "how does it differ," not for efficacy (scope narrowed, see spec) | Definition verbatim | Complete for the narrowed scope | Vietnamese + kept name "Ayres Sensory Integration" | Implicit — question narrowed rather than flagged in-text; noted as a design choice, not hidden | 1 source, real URL | No efficacy/cost claim made (those were rejected, not templated) |
| qe031 (adolescence) | Direct | Both claims (transition difficulty, EF/social demands) verbatim | Complete for a general-overview question | Vietnamese + kept term "camouflaging" | Hedged language throughout ("có thể," "có thể gặp") | 2 sources, real URLs | No specific clinical claim beyond the source |

## Claims removed or downgraded during validation (Phase D's explicit requirement)

- `ayres_si_definition`: the original qe024 evidence included efficacy/assessment-development claims
  from the same paragraph; only the definitional sentence was templated — the rest was not carried into
  the answer because it would have required citing additional claims the specification review judged
  less cleanly verifiable in the time available (see `template_specifications.md`).
- `sleep_nonpharma`: 13 of 14 table rows were **not** included (table-parsing safety rule, not a
  validation failure) — the template text names this limitation rather than silently truncating the
  topic to one recommendation with no explanation.
- `melatonin_efficacy`: the source's specific RCT dose (3 mg/night) was deliberately excluded — a claim
  the evidence supports but which the task's own rules (no stated thresholds/doses) require removing.
- qe034, qe041, qe051, qe056 (and qe017/023/025): entire questions moved to "insufficient template
  support," not partial templates — see `template_specifications.md`'s rejection table for the claim-
  level reasoning on each.

## What this validation did not do

No ASD-domain clinical expert reviewed these 10 templates' wording for lay-audience appropriateness —
this is the same limitation named in `reports/final_hardening/final_acceptance_report.md` §"Distinguishing
evaluation types" and remains open; see `remaining_limitations.md`.
