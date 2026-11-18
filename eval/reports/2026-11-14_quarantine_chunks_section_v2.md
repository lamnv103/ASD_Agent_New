# Chunking pilot — section_v2 — 2026-11-14

Chưa gọi API bên ngoài. Chunk lưu trong DB nhưng tài liệu chưa được phê duyệt nên không truy xuất được.

| source_id | vai trò | chunk | eligible | bảng | token min/median/max | % giữ | trang | đầy đủ |
|---|---|---:|---:|---:|---|---:|---|---|
| ASD-CSV-077 | gaps | 53 | 30 | 13 | 7/494/600 | 98.3 | — | document_has_gaps:51, references_missing_component:2 |
| NIH-NIMH-CHILDREN | gaps | 14 | 14 | 1 | 27/145/301 | 98.3 | — | document_has_gaps:13, references_missing_component:1 |

## Ví dụ chunk

### ASD-CSV-077@snapshot-20261017-e72907221967#section_v2#0010
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 3. Results > 3.2. Overview of the Studies and Measures · body · text · 521 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1, text_fidelity×1.

```text
PDD-NOS vs. ODD), or, finally, (c) compare children from the general population with children with an ASD diagnosis. Eleven studies were longitudinal and 19 had cross-sectional design.

The sensitivity, specificity, PPV, and NPV of the measures are extensively reported in the validation studies of the M-CHAT, M-CHAT R/F, and ADEC. For other measures (i.e., CESDD, JA-OBS, POEMS, DBC-ES, and TIDOS) there is only one study, each containing information of the NPV and PPV. All the other measures did not report any positive or negative predictive values. Overall considered, the measures for which the PPVs and NPVs were reported, demonstrated from moderate to high predictive values, although for the M-CHAT results can be considered more stable compared to other measures that need further and deeper exploration of these properties. Quality of assessment of the studies

Table 3 shows the results of the evaluation of each psychometric properties of the studies through the application of the COSMIN checklist. For each box, we reported a summary of the assigned scores.

The quality of assessment revealed a heterogeneous picture. Specifically, 24 studies out of 52 received an evaluation of the internal consistency (Box A) and the scores were fair or poor, with the exception of the studies on FYI and the Q-CHAT, which received excellent scores. The reliability (Box B) was evaluated in 17 studies and the majority of the scores rating from fair to poor. Only studies considering the CHAT and POEMS received respectively an excellent and good evaluation. The measurement error (Box C) was assessed in 5 longitudinal studies and received poor or fair evaluations.

The Box D (i.e., content validity) was evaluated in 9 studies and it received excellent evaluations for studies considering AOSI, BISCUIT, CHAT, FYI, M-CHAT, POEMS, Q-CHAT, SEEK, and TIDOS. Structural validity (Box E) was evaluated in 7 studies, but only 3 received excellent scores regarding two measures (i.e., M-CHAT and Q- CHAT). The Hypothesis testing (Box F) was evaluated for several studies, which received fair or poor scores, whereas those on FYI and the M-CHAT-R/F received good evaluations, and that on M-CHAT was evaluated as excellent. For the studies on JA-OBS, the SEEK, and the YATCH-18 the property was not evaluated.
```

### ASD-CSV-077@snapshot-20261017-e72907221967#section_v2#0038
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 569 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1, text_fidelity×1.

```text
brainsci-10-00180-t001_Table 1Table 1
Descriptive details of Level 1 and 2 screening tools include in systematic review.
| Measure Name (Short Name) | Short Description of the Dimension(s) Measured | Admin. Age (Months) | Number of Items | Type of Answer | Admin. Time (Minute) | Admin. Method | Cut-Off | N° of Validation Studies Included |
|---|---|---|---|---|---|---|---|---|
| Autism Detection in Early Childhood (ADEC) | Social interaction behaviors and social communication behaviors. | 12–36 | 16 | 3-point Likert scale | 10 | Observational checklist for professionals | 11 | 4 |
| Autism Observation Scale for Infants (AOSI) | Social communication behaviors, non- social behaviors, | 6–18 | 18 | 3-point Likert scale | 15-20 | Observational checklist for professionals | n.s. | 3 |
| Baby and Infants Screen for Children with aUtIsm Traits (BISCUIT) | Part 1 ASD symptoms;Part 2 comorbid psychopathology;Part 3 behavioral problems. | 17–37 | Part 1: 62;Part 2: 65;Part 3: 17. | 3-point Likert scale | 15 | Parent-interview | Part 1: 17;Part 2: 39;Part 3: 17. | 5 |
| Checklist for Early Signs of Developmental Disorders | Language and social functioning. | 3–39 | 25 | Yes/No | Not declared | Parent-reportedquestionnaire | 2 | 1 |
| CHecklist for Autism in Toddlers (CHAT) | Social play, social interest, pretend play, joint-attention, proto-declarative pointing, imitation; B functional play, proto-imperative pointing, motor development, rough and tumble play. | 18 | Part A: 9;Part B: 5 | Yes/No | 15 | Part A: parent- reported questionnaire;Part B: professionals- reported questionnaire | 3 key item | 2 |
| Developmental Behavior Checklist: Early Screen (DBC-ES) | Social, verbal, and non-verbal communication, restricted and repetitive behaviors and interests | 18–48 | 17 | 3-point Likert scale | 5–10 | Parent-reported questionnaire | 11 | 1 |
Note: n.s. = not specified.
```

### NIH-NIMH-CHILDREN@NIH Publication No. 24-MH-8085; Revised 2024#section_v2#0003
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: When might children benefit from an evaluation? · body · table · 278 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: text_fidelity×2.

```text
| Younger children | Older children |
| Have frequent tantrums or are irritable much of the time; Often seem fearful or worried; Complain about frequent stomachaches or headaches with no known medical cause; Are in constant motion and cannot sit quietly (except when they are engaged in an activity they enjoy, such as watching videos or playing video games); Sleep too much or too little, have frequent nightmares, or seem sleepy during the day; Are not interested in playing with other children or have difficulty making friends; Struggle academically or have experienced a recent decline in grades; Repeat actions or check things many times (for example, repeatedly checking to make sure a door is locked) out of fear that something bad may happen | Have lost interest in things that they used to enjoy; Have low energy; Sleep too much or too little or seem sleepy throughout the day; Have periods of highly elevated energy and activity and require much less sleep than usual; Spend more and more time alone and avoid social activities with friends or family; Diet or exercise excessively or fear gaining weight; Engage in self-harm behaviors (such as cutting or burning their skin); Smoke, drink, or use drugs; Engage in risky or destructive behavior alone or with friends; Have thoughts of suicide; Say that they think someone is trying to control their mind or that they hear things that other people cannot hear |
```

### NIH-NIMH-CHILDREN@NIH Publication No. 24-MH-8085; Revised 2024#section_v2#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: When might children benefit from an evaluation? > Get Immediate Help · body · text · 61 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: text_fidelity×2.

```text
If you, your child, or someone you know is struggling or having thoughts of suicide, call or text the **988** Suicide & Crisis Lifeline at 988 or chat at 988lifeline.org. In life-threatening situations, call **911**.
```
