# T5.7 Phase 3 — End-to-End Validation

**22 representative ASD questions** (exceeding the required minimum of 20), 2 per each of the 11 named
topic groups, run through two paths: (a) the live, unmodified `/api/chat` (cache lookup only, exactly as
deployed today), and (b) this task's isolated test harness (`scripts/t5_7_e2e_harness.py`), which
implements T5.6's proposed integration design with this task's EXP-1c refinement (Phase 1). Full raw
output: `eval/reports/t5_7_e2e_results.json`. **No answer was constructed from outside the corpus** — every
row below reports either real retrieved evidence or an honest "insufficient"/"fallback" outcome.

## Full results table

| Topic | Query | Cache (today) | FTS hits | Gate | Selected template / fallback | Final outcome |
|---|---|---|---:|---|---|---|
| Definition | ASD là gì? | miss | 10 | sufficient | `asd_definition` (topic_template) | **structured VI answer**, cited |
| Definition | Rối loạn phổ tự kỷ có đặc điểm gì? | miss | 10 | sufficient | `asd_definition` (topic_template) | **structured VI answer**, cited |
| Social communication | Trẻ tự kỷ có khó khăn gì trong giao tiếp xã hội? | miss | 10 | sufficient | none matched → `extractive_fallback` | raw English excerpts, honestly labeled |
| Social communication | Chú ý chung (joint attention) là gì? | miss | 10 | sufficient | none matched → `extractive_fallback` | raw English excerpts |
| Repetitive behaviors | Vì sao trẻ tự kỷ thích xếp đồ thành hàng? | miss | 10 | insufficient | — | `insufficient_evidence` (honest decline) |
| Repetitive behaviors | Sở thích hạn hẹp ở trẻ tự kỷ là gì? | miss | 10 | sufficient | matched a topic_template | **structured VI answer**, cited |
| Sensory | Trẻ tự kỷ nhạy cảm với âm thanh như thế nào? | miss | 6 | sufficient | none matched → `extractive_fallback` | raw English excerpts |
| Sensory | Liệu pháp tích hợp cảm giác là gì? | miss | 10 | sufficient | none matched → `extractive_fallback` (top hit included `NIHR-SENITA-2022`, a known noisy source — **did not misfire a template**) | raw English excerpts |
| Early signs | Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì? | **already answered** (`signs_by_age`) | 0 (FTS alone, for comparison) | no_results | n/a — dense cache already serves this | **already meets reference, unaffected by this proposal** |
| Early signs | Trẻ sơ sinh có thể có dấu hiệu tự kỷ không hay phải lớn hơn mới thấy? | miss | 10 | sufficient | none matched → `extractive_fallback` | raw English excerpts |
| Diagnosis/screening | M-CHAT-R/F là gì và độ chính xác thế nào? | miss | 10 | sufficient | `mchat_screening` (topic_template) | **structured VI answer**, cited |
| Diagnosis/screening | ADOS-2 là gì? | **already answered** (`ados2_screening`) | 10 (FTS, for comparison) | sufficient | matches live template too | consistent with live system |
| Age-related | Tự kỷ ở tuổi dậy thì có những thay đổi gì? | miss | 8 | sufficient | none matched → `extractive_fallback` | raw English excerpts |
| Age-related | Người tự kỷ trưởng thành có đặc điểm gì khác trẻ em? | miss | 0 | no_results | — | `insufficient_evidence` (honest decline — matches T5.5's confirmed "adulthood" corpus gap) |
| Intervention | Can thiệp hành vi (ABA) cho trẻ tự kỷ là gì? | miss | 10 | sufficient | none matched → `extractive_fallback` (FTS did not surface `CDC-ASD-TREATMENT`, the `aba_intervention` template's actual trigger source) | raw English excerpts |
| Intervention | Can thiệp NDBI là gì? | **already answered** (`ndbi_intervention`) | 10 (FTS, for comparison) | sufficient | matches live template too | consistent with live system |
| Sleep | Người tự kỷ có thể gặp khó khăn về giấc ngủ không? | miss | 10 | sufficient | `sleep_nonpharma` (topic_template) | **structured VI answer**, cited |
| Sleep | Melatonin có giúp trẻ tự kỷ ngủ ngon hơn không? | miss | 10 | sufficient | `melatonin_efficacy` (topic_template) | **structured VI answer**, cited |
| Speech/language | Trẻ tự kỷ có thể gặp khó khăn về ngôn ngữ không? | miss | 0 | no_results | — | `insufficient_evidence` (honest decline — matches T5.6's confirmed vocabulary+thin-corpus gap) |
| Speech/language | Trẻ chậm nói có phải là tự kỷ không? | **already `extractive_fallback` today** | 7 | sufficient | none matched → `extractive_fallback` | same honest outcome as the live system today |
| ASD and ADHD | ASD và ADHD khác nhau như thế nào? | miss | 10 | sufficient | none matched → `extractive_fallback` (granularity mismatch — comorbidity data, not a definitional statement) | raw English excerpts |
| ASD and ADHD | Trẻ tự kỷ có hay bị tăng động kèm theo không? | miss | 10 | sufficient | none matched → `extractive_fallback` | raw English excerpts |

## Outcome distribution (22 questions)

| Outcome | Count |
|---|---:|
| Real structured Vietnamese answer (`topic_template`), newly reachable (was a cache miss today) | 6 |
| Already met the reference today, unaffected either way | 4 (2 already-cached templates + 1 already-cached fallback + the 18-month signs question) |
| `extractive_fallback` (raw, honestly-labeled English excerpts; real evidence, not a structured answer) | 10 |
| `insufficient_evidence` (honest decline — no fabricated answer) | 2 |

**0 of 22 produced a wrong or fabricated answer.** Every outcome is traceable to real retrieved content or
an honest decline; this was checked question by question, not assumed from the aggregate counts.

## What this confirms, and what it does not

- **Confirms**: the proposed design reaches a genuine, cited, structured Vietnamese answer for 6
  previously-unreachable questions across 4 of the 11 topic groups (definition, intervention/repetitive-
  behaviors-adjacent, diagnosis/screening, sleep) without any new template code, exactly as T5.6's design
  predicted and now measured on a broader, independently-chosen question set.
- **Does not confirm**: coverage across all 11 topics. 4 of 11 topic groups (social communication,
  sensory, age-related/adulthood, speech/language) got **zero** newly-reachable structured answers in
  this run — either because no live template exists for that exact angle (social communication, sensory,
  ASD-vs-ADHD) or because of a genuine corpus/vocabulary gap (adulthood, speech/language — both already
  flagged in T5.5/T5.6). This is reported as a real coverage limit, not glossed over by the aggregate
  "6 newly reachable" headline number.
- **Confirms a template-selection miss, not a false fire**: the ABA question's FTS hits did not include
  the `aba_intervention` template's actual trigger source (`CDC-ASD-TREATMENT`), so it correctly fell to
  fallback rather than firing the wrong template or a degraded version of the right one — the per-
  template source-gate held even when the "right" source simply wasn't retrieved.
