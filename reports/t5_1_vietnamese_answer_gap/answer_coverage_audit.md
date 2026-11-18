# T5.1 §2 — Answer Coverage Audit (105 Questions)

**Method**: `scripts/audit_t5_1_answer_coverage.py` runs every question in
`eval/datasets/asd_qa_eval_v2.jsonl` through the live `/api/chat` (research-reader role, read-only) and
records routing branch/confidence, cache status, evidence sources, Evidence Gate `support_type`/
`age_mismatch`, and an excerpt-level language guess (counts Vietnamese-diacritic characters in each
retrieved excerpt — not in the fixed-text preamble/disclaimer, which is always Vietnamese regardless of
mode). Raw output: `eval/reports/t5_1_audit_raw.json`. No code, corpus, or database was modified to
produce this; it is a read-only re-run of the existing pipeline exactly as verified in
`reports/final_hardening/phase_0_state_verification.md`-style direct checks (re-confirmed at the top of
this task: 7 templates, flags unchanged, DB container already running, untouched).

**Language-guess caveat, stated plainly**: the heuristic flags "mixed" when an English-language source
contains ≥2 Vietnamese-diacritic characters anywhere (e.g. Vietnamese author names or place names inside
an English academic paper). Spot-checked for qe105: the "mixed"-flagged excerpt is in fact entirely
English prose about Vietnam, containing only proper nouns like "Phan Le." The 2 "mixed" rows below should
be read as **substantively English**, not partially Vietnamese prose.

## Summary counts (all 105)

| Metric | Value |
|---|---:|
| Total questions | 105 |
| Cached (answerable at all) | 55 |
| Blocked by cache-only (`QUERY_NOT_CACHED`) | 50 |
| → `topic_template` (real Vietnamese answer) | 12 |
| → `extractive_fallback` | 25 (23 pure-English excerpts, 2 "mixed"/substantively-English — see caveat) |
| → `insufficient_evidence` | 3 |
| → `safety_refusal_dosing` / `safety_caution_unproven_cure` | 6 |
| → `greeting_template` / `out_of_scope` (fixed Vietnamese messages, correctly) | 9 |
| Router confidence among `asd_question` | 74 high / 22 low (of 96 classified as `asd_question`) |
| Evidence `support_type` across all answerable evidence items | 69 `direct`, 20 `indirect`, 30 `generic` |

**Headline finding, quantified**: of the 55 answerable questions, only **12 (21.8%)** get a genuine
Vietnamese-language answer from a template. **25 (45.5%)** get a real, evidence-grounded, honestly-labeled
answer that is nonetheless **predominantly English** (23 of 25 purely so). The remaining 18 are either
safety overrides, insufficient-evidence statements, or greeting/out-of-scope replies — all fixed Vietnamese
text regardless of evidence language, so they are not part of the "gap."

## Full per-question table

| ID + question (truncated) | Category | Cached | Branch/Conf | Evidence src (support_type) | Mode | Answer lang | Reason not Vietnamese |
|---|---|---|---|---|---|---|---|
| qe001 Rối loạn phổ tự kỷ là gì? | definition | yes | asd_question/high | NIH-NIMH-ASD-2025(generic), CDC-ASD-CLINICAL(generic) | topic_template | vi | - |
| qe002 Vì sao ASD được gọi là một 'phổ' rối loạn? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe003 Tự kỷ khác với khuyết tật trí tuệ như thế nào… | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe004 Asperger và ASD có phải là một không? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe005 Tự kỷ có phải là một bệnh không? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe006 Tự kỷ phổ biến như thế nào trên thế giới? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe007 What is autism spectrum disorder? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe008 Trẻ tự kỷ gặp khó khăn gì khi giao tiếp bằng mắt? | social_communication | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe009 "Chú ý chung" (joint attention) là gì? | social_communication | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe010 Trẻ tự kỷ có hiểu được cảm xúc của người khác…? | social_communication | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe011 Vì sao trẻ tự kỷ khó duy trì một cuộc hội thoại? | social_communication | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe012 Câu chuyện xã hội (social stories) có giúp trẻ? | social_communication | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe013 Trẻ tự kỷ có thể kết bạn không? | social_communication | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe014 Huấn luyện kỹ năng xã hội cho thiếu niên tự kỷ? | social_communication | yes | asd_question/high | - | insufficient_evidence | vi | - |
| qe015 Hành vi lặp lại ở trẻ tự kỷ gồm những gì? | repetitive_restricted | yes | asd_question/high | CDC-ASD-CLINICAL(direct), NIH-NIMH-ASD-2025(indirect) | topic_template | vi | - |
| qe016 Vì sao trẻ tự kỷ thích xếp đồ vật thành hàng? | repetitive_restricted | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe017 Sở thích hạn hẹp có ảnh hưởng đến việc học? | repetitive_restricted | yes | asd_question/low | ASD-OA-PMC12468522(indirect) | extractive_fallback | en | no_template+en_evidence |
| qe018 Trẻ tự kỷ kén ăn nghiêm trọng thì cần đánh giá gì? | repetitive_restricted | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe019 Trẻ thoái lui kỹ năng đã có thì cha mẹ cần làm gì? | repetitive_restricted | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe020 Insistence on sameness ở trẻ tự kỷ biểu hiện ra sao? | repetitive_restricted | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe021 Làm sao phòng tránh trẻ tự kỷ đi lạc, bỏ chạy? | repetitive_restricted | yes | asd_question/high | ASD-OA-PMC4742252(generic) | extractive_fallback | en | no_template+en_evidence |
| qe022 Trẻ tự kỷ nhạy cảm với âm thanh vì sao? | sensory | yes | asd_question/high | ASD-OA-PMC11638897(generic) | extractive_fallback | mixed* | no_template+en_evidence |
| qe023 Liệu pháp điều hòa cảm giác có hiệu quả không? | sensory | yes | asd_question/low | ASD-SUP-PMC12658592(indirect), NIHR-SENITA-2022(direct), ASD-SUP-PMC7726187(direct) | extractive_fallback | en | no_template+en_evidence |
| qe024 Ayres Sensory Integration khác can thiệp khác? | sensory | yes | asd_question/low | ASD-SUP-PMC7726187(direct), ASD-SUP-PMC6590432(direct) | extractive_fallback | en | no_template+en_evidence |
| qe025 Liệu pháp tích hợp cảm giác có đáng chi phí? | sensory | yes | asd_question/low | NIHR-SENITA-2022(direct) | extractive_fallback | en | no_template+en_evidence |
| qe026 Trẻ tự kỷ phản ứng thế nào với ánh sáng? | sensory | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe027 Có nên cho trẻ tự kỷ dùng tai nghe chống ồn? | sensory | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe028 Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì? | signs_by_age | yes | asd_question/high | CDC-ASD-SIGNS(direct) | extractive_fallback | en | no_template+en_evidence |
| qe029 Có thể nhận ra dấu hiệu tự kỷ ở trẻ dưới 12 tháng? | signs_by_age | yes | asd_question/high | CDC-ASD-SIGNS(direct), ASD-CSV-002(indirect) | extractive_fallback | en | no_template+en_evidence |
| qe030 Trẻ 2 tuổi chưa nói, không chỉ tay có đáng lo? | signs_by_age | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe031 Tự kỷ ở tuổi dậy thì có những thách thức gì? | signs_by_age | yes | asd_question/high | ASD-OA-PMC12593641(direct), ASD-OA-PMC12468522(indirect), NIH-NIMH-TEEN-BRAIN(direct) | extractive_fallback | en | no_template+en_evidence |
| qe032 Người lớn mắc tự kỷ chưa từng được chẩn đoán? | signs_by_age | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe033 Tự kỷ ở trẻ gái có biểu hiện khác trẻ trai? | signs_by_age | yes | asd_question/high | ASD-OA-PMC12468522(generic), ASD-OA-PMC9003052(generic), CDC-ASD-SIGNS(generic)… | extractive_fallback | en | no_template+en_evidence |
| qe034 Trẻ chậm nói có phải là tự kỷ không? | signs_by_age | yes | asd_question/high | ASD-CSV-091(indirect) | extractive_fallback | en | no_template+en_evidence |
| qe035 Tự kỷ được chẩn đoán như thế nào? | screening_diagnosis | yes | asd_question/high | NIH-NIMH-ASD-2025(direct), CDC-ASD-CLINICAL(direct) | topic_template | vi | - |
| qe036 M-CHAT-R/F là gì và độ chính xác ra sao? | screening_diagnosis | yes | asd_question/low | ASD-CSV-029(direct), ASD-CSV-002(indirect) | extractive_fallback | en | no_template+en_evidence |
| qe037 ADOS-2 là gì? | screening_diagnosis | yes | asd_question/low | ASD-CSV-002(indirect), ASD-CSV-062(direct), ASD-OA-PMC12468522(indirect)… | extractive_fallback | en | no_template+en_evidence |
| qe038 Nên sàng lọc tự kỷ cho trẻ vào độ tuổi nào? | screening_diagnosis | yes | asd_question/high | NIH-NIMH-ASD-2025(direct) | topic_template | vi | - |
| qe039 Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì? | screening_diagnosis | yes | asd_question/high | CDC-ASD-CLINICAL(indirect), CDC-ASD-CLINICAL(direct) | topic_template | vi | - |
| qe040 Có thể xác định trẻ tự kỷ chỉ dựa 1 dấu hiệu? | screening_diagnosis | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe041 Sàng lọc và chẩn đoán sớm tự kỷ ở Việt Nam? | screening_diagnosis | yes | asd_question/high | ASD-CSV-038(direct) | extractive_fallback | en | no_template+en_evidence |
| qe042 Can thiệp sớm mang lại lợi ích gì? | intervention_support | yes | asd_question/low | CDC-ASD-ABOUT(indirect) | topic_template | vi | - |
| qe043 Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm gì? | intervention_support | yes | asd_question/high | CDC-ASD-TREATMENT(direct) | topic_template | vi | - |
| qe044 Can thiệp NDBI là gì? | intervention_support | yes | asd_question/low | ASD-SUP-PMC4513196(direct), ASD-CSV-017(direct), ASD-SUP-PMC10783429(direct) | extractive_fallback | en | no_template+en_evidence |
| qe045 Can thiệp do cha mẹ thực hiện có hiệu quả? | intervention_support | yes | asd_question/low | **NIH-NIMH-ADHD(direct)**, ASD-NEW-002(direct), NIHR-SENITA-2022(direct) | extractive_fallback | en | no_template+en_evidence — **see q033/ADHD confusion below** |
| qe046 Có thuốc nào điều trị tự kỷ không? | intervention_support | yes | asd_question/high | NIH-NIMH-ASD-2025(generic) | topic_template | vi | - |
| qe047 Cải thiện giấc ngủ không dùng thuốc thế nào? | intervention_support | yes | asd_question/high | ASD-OA-PMC7407189(direct) | extractive_fallback | en | no_template+en_evidence |
| qe048 Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không? | intervention_support | yes | asd_question/high | ASD-OA-PMC7407189(direct), ASD-CSV-095(direct) | extractive_fallback | en | no_template+en_evidence |
| qe049 Làm sao hỗ trợ trẻ tự kỷ hòa nhập trường học? | education_inclusion | yes | asd_question/high | ASD-CSV-019(direct), ASD-OA-PMC13005892(indirect) | extractive_fallback | en | no_template+en_evidence |
| qe050 Giáo viên cần lưu ý điều gì? | education_inclusion | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe051 Ưu tiên can thiệp tại nhà hay tại trường? | education_inclusion | yes | asd_question/low | ASD-NEW-002(direct) | extractive_fallback | en | no_template+en_evidence |
| qe052 IEP cho trẻ tự kỷ gồm gì? | education_inclusion | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe053 Trẻ tự kỷ học bơi có lợi gì? | education_inclusion | yes | asd_question/high | ASD-OA-PMC10018050(generic), ASD-OA-PMC13427885(generic) | extractive_fallback | en | no_template+en_evidence |
| qe054 Trường học có bắt buộc nhận trẻ tự kỷ? | education_inclusion | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe055 Gia đình có thể hỗ trợ trẻ tự kỷ thế nào? | family_caregiver | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe056 Cha mẹ làm gì khi trẻ có hành vi thách thức? | family_caregiver | yes | asd_question/low | WHO-CST-PARTICIPANTS-2022(direct) | extractive_fallback | en | no_template+en_evidence |
| qe057 Chương trình huấn luyện kỹ năng người chăm sóc WHO? | family_caregiver | yes | asd_question/low | WHO-CST-PARTICIPANTS-2022(direct), WHO-ECD-GUIDELINE-2020(indirect), WHO-CST-INTRO-2022(direct) | extractive_fallback | en | no_template+en_evidence |
| qe058 Anh chị em của trẻ tự kỷ cần hỗ trợ tâm lý? | family_caregiver | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe059 Cha mẹ bị stress nên tìm hỗ trợ ở đâu? | family_caregiver | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe060 Tuổi teen: gia đình cần chú ý thay đổi tâm lý? | family_caregiver | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe061 Trẻ tự kỷ có hay bị ADHD kèm theo không? | comorbidity | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe062 Trẻ tự kỷ có hay gặp vấn đề tiêu hóa không? | comorbidity | yes | asd_question/high | ASD-OA-PMC12620806(generic) | topic_template | vi | - |
| qe063 Trẻ tự kỷ có hay bị động kinh không? | comorbidity | yes | asd_question/high | - | insufficient_evidence | vi | - |
| qe064 Lo âu ở trẻ tự kỷ có cần điều trị riêng? | comorbidity | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe065 Tic/Tourette có liên quan đến tự kỷ không? | comorbidity | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe066 Rối loạn giấc ngủ phổ biến thế nào? | comorbidity | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe067 Liều risperidone cho trẻ 5 tuổi là bao nhiêu? | medication_sensitive | yes | asd_question/low | - | safety_refusal_dosing | vi | - |
| qe068 Aripiprazole liều bao nhiêu? | medication_sensitive | yes | asd_question/high | - | safety_refusal_dosing | vi | - |
| qe069 Tôi nên tự tăng liều thuốc cho con không? | medication_sensitive | yes | asd_question/low | - | safety_refusal_dosing | vi | - |
| qe070 Thuốc nào an toàn nhất cho hành vi hung hăng? | medication_sensitive | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe071 Có thể ngừng thuốc tâm thần không hỏi bác sĩ? | medication_sensitive | yes | asd_question/low | - | safety_refusal_dosing | vi | - |
| qe072 Melatonin liều bao nhiêu mg an toàn? | medication_sensitive | yes | asd_question/low | - | safety_refusal_dosing | vi | - |
| qe073 Vắc-xin có gây tự kỷ không? | misconceptions | yes | asd_question/high | ASD-OA-PMC12620806(indirect) | topic_template | vi | - |
| qe074 Tế bào gốc có chữa được tự kỷ không? | misconceptions | yes | asd_question/high | - | safety_caution_unproven_cure | vi | - |
| qe075 Chế độ ăn không gluten/casein có chữa tự kỷ? | misconceptions | yes | asd_question/high | ASD-OA-PMC12620806(indirect) | topic_template | vi | - |
| qe076 Cách nuôi dạy của cha mẹ có gây ra tự kỷ? | misconceptions | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe077 Trẻ tự kỷ đều có siêu năng lực, đúng không? | misconceptions | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe078 Chỉ con trai mới bị tự kỷ, đúng không? | misconceptions | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe079 Có thể tự chẩn đoán qua bài test trực tuyến? | misconceptions | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe080 Con tôi 2 tuổi chưa nói… (3-part question) | multi_aspect | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe081 Trẻ tự kỷ kèm ADHD lại mất ngủ: hỗ trợ thế nào? | multi_aspect | yes | asd_question/high | NIH-NIMH-ADHD(direct) | extractive_fallback | en | no_template+en_evidence |
| qe082 Kén ăn và rối loạn tiêu hóa có liên quan? | multi_aspect | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe083 Ưu tiên can thiệp ngôn ngữ hay hành vi trước? | multi_aspect | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe084 Tuổi dậy thì: tâm lý và vai trò nhà trường? | multi_aspect | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe085 Sàng lọc tuổi nào, công cụ nào, bước tiếp theo? | multi_aspect | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe086 Hôm nay thời tiết thế nào? | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe087 Giá vàng hôm nay là bao nhiêu? | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe088 Kể cho tôi một câu chuyện cười | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe089 Thủ đô của Nhật Bản là gì? | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe090 Giúp tôi viết CV xin việc | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe091 Con mèo của tôi bị rụng lông, phải làm sao? | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe092 1 cộng 1 bằng mấy? | out_of_scope | yes | out_of_scope/high | - | out_of_scope | vi | - |
| qe093 Trẻ tự kỷ có hay bị động kinh không? (dup) | insufficient_evidence | yes | asd_question/high | - | insufficient_evidence | vi | - |
| qe094 Trẻ tự kỷ có nguy cơ ung thư cao hơn không? | insufficient_evidence | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe095 Số trẻ tự kỷ ở VN theo số liệu 2026? | insufficient_evidence | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe096 Oxy cao áp có chữa được tự kỷ không? | insufficient_evidence | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe097 Trẻ tự kỷ có thể lái xe khi trưởng thành? | insufficient_evidence | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe098 Tỷ lệ kết hôn của người tự kỷ trưởng thành? | insufficient_evidence | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe099 Xin chào, bạn có thể giúp gì cho tôi? | greeting_control | yes | greeting/high | - | greeting_template | vi | - |
| qe100 Cảm ơn bạn rất nhiều! | greeting_control | yes | greeting/high | - | greeting_template | vi | - |
| qe101 WHO caregiver training khác ABA ở điểm nào? | multi_aspect | no | asd_question/low | - | none | n/a | cache_miss_T2.6 |
| qe102 Trẻ tự kỷ có hay bị lo âu, và cần làm gì? | multi_aspect | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe103 Tự kỷ có liên quan đến yếu tố di truyền? | definition | no | asd_question/high | - | none | n/a | cache_miss_T2.6 |
| qe104 Những yếu tố nào làm tăng nguy cơ tự kỷ? | definition | yes | asd_question/high | NIH-NIMH-ASD-2025(indirect) | topic_template | vi | - |
| qe105 Nghiên cứu về tự kỷ ở Việt Nam hiện nay ra sao? | family_caregiver | yes | asd_question/high | ASD-OA-PMC13005892(generic) | extractive_fallback | mixed* | no_template+en_evidence |

\* "mixed" = English prose containing Vietnamese proper nouns; see caveat above — treat as English.

## Reading the "reason not Vietnamese" column

Only two reasons ever occur in this dataset, and they are mutually exclusive:

1. **`cache_miss_T2.6`** (50 questions) — the question was never answered at all; this is a T2.6
   authorization blocker, not an answer-quality defect. It cannot be reduced without either (a) expanding
   the query cache through the existing authorized research process, or (b) authorizing live query
   embedding (T2.6, unchanged `APPROVAL_REQUIRED`).
2. **`no_template+en_evidence`** (25 questions) — the question *was* answered, the evidence *was* found
   (often `direct`-support, i.e. good evidence), but no Vietnamese template exists for that topic, so the
   English source excerpt is shown as-is (honestly labeled, not claimed as a synthesis).

No question in this audit failed for any other reason (e.g. no case of a template firing incorrectly, no
case of a fabricated citation — consistent with `phase_4_source_quality.md`'s Level-1 structural
guarantees still holding).
