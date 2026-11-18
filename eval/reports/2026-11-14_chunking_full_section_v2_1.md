# Chunking pilot — section_v2_1 — 2026-11-14

Chưa gọi API bên ngoài. Chunk lưu trong DB nhưng tài liệu chưa được phê duyệt nên không truy xuất được.

| source_id | vai trò | chunk | eligible | bảng | token min/median/max | % giữ | trang | đầy đủ |
|---|---|---:|---:|---:|---|---:|---|---|
| ASD-CSV-002 | core | 72 | 43 | 1 | 59/440/594 | 99.2 | — | complete:68, references_missing_component:4 |
| ASD-CSV-007 | gaps | 50 | 30 | 3 | 21/328/597 | 97.2 | — | document_has_gaps:40, references_missing_component:10 |
| ASD-CSV-011 | gaps | 48 | 28 | 0 | 5/293/599 | 96.6 | — | document_has_gaps:37, references_missing_component:11 |
| ASD-CSV-017 | gaps | 85 | 77 | 13 | 20/465/598 | 98.6 | — | document_has_gaps:83, references_missing_component:2 |
| ASD-CSV-018 | gaps | 61 | 50 | 6 | 18/429/598 | 98.4 | — | document_has_gaps:55, references_missing_component:6 |
| ASD-CSV-019 | gaps | 105 | 52 | 23 | 7/464/595 | 98.2 | — | document_has_gaps:97, references_missing_component:8 |
| ASD-CSV-020 | gaps | 42 | 27 | 1 | 46/476/600 | 98.1 | — | document_has_gaps:35, references_missing_component:7 |
| ASD-CSV-029 | gaps | 43 | 33 | 2 | 4/140/576 | 97.4 | — | document_has_gaps:42, references_missing_component:1 |
| ASD-CSV-038 | gaps | 31 | 23 | 5 | 31/331/605 | 96.5 | — | document_has_gaps:29, references_missing_component:2 |
| ASD-CSV-062 | core | 62 | 51 | 13 | 9/304/590 | 97.7 | — | complete:62 |
| ASD-CSV-078 | core | 20 | 16 | 5 | 10/445/578 | 97.1 | — | complete:20 |
| ASD-CSV-081 | core | 42 | 20 | 4 | 11/367/588 | 98.2 | — | complete:41, references_missing_component:1 |
| ASD-CSV-084 | core | 42 | 27 | 10 | 15/361/580 | 98.2 | — | complete:39, references_missing_component:3 |
| ASD-CSV-088 | core | 37 | 26 | 6 | 33/419/595 | 98.9 | — | complete:37 |
| ASD-CSV-089 | gaps | 53 | 44 | 13 | 30/340/634 | 98.2 | — | document_has_gaps:43, references_missing_component:10 |
| ASD-CSV-091 | core | 65 | 49 | 5 | 7/421/624 | 99.4 | — | complete:64, references_missing_component:1 |
| ASD-CSV-095 | gaps | 51 | 37 | 9 | 11/389/598 | 97.4 | — | document_has_gaps:48, references_missing_component:3 |
| ASD-NEW-001 | gaps | 58 | 48 | 10 | 19/375/618 | 100.0 | — | document_has_gaps:46, references_missing_component:12 |
| ASD-NEW-002 | gaps | 158 | 115 | 53 | 13/506/600 | 99.2 | — | document_has_gaps:100, references_missing_component:58 |
| ASD-NEW-003 | core | 93 | 62 | 2 | 3/494/613 | 99.2 | — | complete:84, references_missing_component:9 |
| ASD-OA-PMC10018050 | core | 41 | 32 | 6 | 3/247/609 | 98.0 | — | complete:39, references_missing_component:2 |
| ASD-OA-PMC10774556 | core | 43 | 25 | 0 | 62/400/592 | 98.0 | — | complete:42, references_missing_component:1 |
| ASD-OA-PMC10900867 | core | 45 | 36 | 4 | 64/380/592 | 98.5 | — | complete:37, references_missing_component:8 |
| ASD-OA-PMC11638897 | core | 92 | 29 | 0 | 6/515/601 | 98.4 | — | complete:92 |
| ASD-OA-PMC12468522 | core | 149 | 104 | 3 | 3/100/652 | 99.1 | — | complete:149 |
| ASD-OA-PMC12593641 | core | 24 | 6 | 0 | 8/267/571 | 96.7 | — | complete:23, references_missing_component:1 |
| ASD-OA-PMC12620806 | gaps | 92 | 44 | 0 | 184/503/652 | 98.1 | — | document_has_gaps:88, references_missing_component:4 |
| ASD-OA-PMC13005892 | core | 81 | 51 | 15 | 3/486/606 | 98.6 | — | complete:71, references_missing_component:10 |
| ASD-OA-PMC13393316 | gaps | 48 | 23 | 1 | 3/416/608 | 97.0 | — | document_has_gaps:44, references_missing_component:4 |
| ASD-OA-PMC13427885 | core | 53 | 24 | 6 | 11/381/591 | 97.1 | — | complete:50, references_missing_component:3 |
| ASD-OA-PMC4271434 | core | 37 | 8 | 6 | 37/472/586 | 97.9 | — | complete:37 |
| ASD-OA-PMC4742252 | core | 38 | 22 | 11 | 18/327/593 | 97.1 | — | complete:38 |
| ASD-OA-PMC6487529 | core | 50 | 34 | 9 | 3/191/590 | 96.2 | — | complete:49, references_missing_component:1 |
| ASD-OA-PMC7407189 | core | 93 | 46 | 4 | 7/492/597 | 99.2 | — | complete:93 |
| ASD-OA-PMC9003052 | core | 63 | 44 | 9 | 7/438/604 | 98.4 | — | complete:61, references_missing_component:2 |
| ASD-SUP-PMC10783429 | gaps | 67 | 53 | 3 | 10/269/594 | 97.1 | — | document_has_gaps:55, references_missing_component:12 |
| ASD-SUP-PMC10981608 | gaps | 98 | 75 | 22 | 11/424/605 | 98.6 | — | document_has_gaps:85, references_missing_component:13 |
| ASD-SUP-PMC11754701 | core | 80 | 69 | 25 | 11/289/629 | 98.0 | — | complete:73, references_missing_component:7 |
| ASD-SUP-PMC12658592 | core | 68 | 48 | 21 | 6/355/584 | 98.1 | — | complete:62, references_missing_component:6 |
| ASD-SUP-PMC13414371 | gaps | 59 | 36 | 5 | 3/384/601 | 98.2 | — | document_has_gaps:45, references_missing_component:14 |
| ASD-SUP-PMC4513196 | core | 62 | 3 | 0 | 28/450/595 | 98.4 | — | complete:62 |
| ASD-SUP-PMC6590432 | core | 51 | 40 | 13 | 8/417/704 | 98.1 | — | complete:47, references_missing_component:4 |
| ASD-SUP-PMC7726187 | gaps | 42 | 26 | 2 | 28/463/588 | 97.8 | — | document_has_gaps:37, references_missing_component:5 |
| ASD-SUP-PMC9399988 | gaps | 55 | 38 | 8 | 23/374/605 | 98.1 | — | document_has_gaps:45, references_missing_component:10 |
| CDC-ASD-ABOUT | gaps | 17 | 17 | 0 | 17/109/332 | 99.8 | — | document_has_gaps:17 |
| CDC-ASD-CLINICAL | gaps | 8 | 8 | 0 | 33/104/552 | 99.8 | — | document_has_gaps:8 |
| CDC-ASD-SCREENING | gaps | 8 | 8 | 0 | 95/152/294 | 99.5 | — | document_has_gaps:8 |
| CDC-ASD-SIGNS | gaps | 4 | 4 | 0 | 102/170/263 | 100.0 | — | document_has_gaps:4 |
| CDC-ASD-TREATMENT | core | 11 | 11 | 0 | 22/123/237 | 100.0 | — | complete:11 |
| CDC-CONCERNED | gaps | 12 | 12 | 0 | 33/76/140 | 99.3 | — | document_has_gaps:11, references_missing_component:1 |
| CDC-EARLY-INTERVENTION | core | 4 | 4 | 0 | 14/110/355 | 98.8 | — | complete:4 |
| CDC-MILESTONES-02 | gaps | 14 | 14 | 0 | 13/46/579 | 99.5 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-04 | gaps | 14 | 14 | 0 | 14/48/587 | 99.5 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-06 | gaps | 14 | 14 | 0 | 14/45/561 | 99.5 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-09 | gaps | 14 | 14 | 0 | 14/48/600 | 99.6 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-12 | gaps | 14 | 14 | 0 | 11/49/579 | 99.6 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-15 | gaps | 14 | 14 | 0 | 14/55/615 | 99.6 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-18 | gaps | 14 | 14 | 0 | 14/56/597 | 99.6 | — | document_has_gaps:12, references_missing_component:2 |
| CDC-MILESTONES-24 | gaps | 14 | 14 | 0 | 14/54/566 | 99.6 | — | document_has_gaps:13, references_missing_component:1 |
| CDC-MILESTONES-30 | gaps | 14 | 14 | 0 | 14/61/539 | 99.6 | — | document_has_gaps:13, references_missing_component:1 |
| CDC-MILESTONES-36 | gaps | 14 | 14 | 0 | 14/49/603 | 99.5 | — | document_has_gaps:13, references_missing_component:1 |
| NIH-NIDCD-ASD-COMMUNICATION-2020 | core | 8 | 8 | 0 | 57/293/602 | 99.9 | — | complete:8 |
| NIH-NIMH-ADHD | core | 19 | 19 | 0 | 27/147/481 | 98.8 | — | complete:19 |
| NIH-NIMH-ASD-2025 | core | 17 | 17 | 0 | 12/110/405 | 98.3 | — | complete:17 |
| NIH-NIMH-MEDICATIONS | core | 12 | 12 | 0 | 53/258/644 | 100.0 | — | complete:12 |
| NIH-NIMH-TEEN-BRAIN | core | 9 | 9 | 0 | 42/85/168 | 91.7 | — | complete:9 |
| NIH-NIMH-TEEN-DEPRESSION | core | 6 | 6 | 0 | 53/83/225 | 92.5 | — | complete:6 |
| NIHR-SENITA-2022 | gaps | 354 | 190 | 0 | 1/288/657 | 87.0 | [1, 172] | document_has_gaps:183, table_structure_unrecoverable:133, references_missing_component:38 |
| WHO-CST-INTRO-2022 | gaps | 18 | 9 | 0 | 163/523/576 | 99.3 | [1, 20] | document_has_gaps:18 |
| WHO-CST-PARTICIPANTS-2022 | gaps | 156 | 73 | 0 | 2/428/617 | 94.4 | [1, 278] | table_structure_unrecoverable:20, document_has_gaps:96, text_encoding_lost:40 |
| WHO-ECD-GUIDELINE-2020 | gaps | 188 | 114 | 0 | 5/211/621 | 98.7 | [1, 80] | document_has_gaps:136, table_structure_unrecoverable:40, references_missing_component:1, table_recovered_pending_review:11 |

## Ví dụ chunk

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v2_1#0003
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Changes in Diagnostic Criteria Over Time · body · table · 195 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Diagnostic Criteria of Autism Spectrum Disorder in the DSM-5
| A. Social communication and interaction challenges: |
| 1. Deficits in social-emotional reciprocity |
| 2. Deficits in nonverbal communicative behaviors used for social interaction |
| 3. Deficits in developing, maintaining, and understanding relationships |
| B. Repetitive or stereotyped behaviors: |
| 1. Stereotyped or repetitive motor movements, use of objects, or speech |
| 2. Insistence on sameness, inflexible adherence to routines, or ritualized patterns of verbal or nonverbal behavior |
| 3. Highly restricted, fixated interests that are abnormal in intensity or focus |
| 4. Hyper- or hypo-reactivity to sensory input or unusual interest in sensory aspects of the environment |
Note. DSM-5 = Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition.
```

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v2_1#0014
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Empirically Validated Screening and Diagnostic Measures > Autism Screening > Screening Tool for Autism in Toddlers · body · text · 205 tokens · trang [None, None]
- completeness: complete

```text
The Screening Tool for Autism in Toddlers (STAT; Stone et al., 2004) is a Level 2 screening measure administered by a trained professional. It comprises 12 play-based activities to observe early social communication behaviors in children from 24 to 35 months of age that can be administered in 15 to 20 min. The total score is derived by summing the four domain scores (play, requesting, directing attention, and motor imitation), with higher scores representing greater impairment. Sensitivity for autism classification is estimated to be 0.92, and specificity is 0.85, with a test–retest reliability of 0.90 (Stone et al., 2004). The STAT has shown good discriminant validity between autism and non-spectrum (0.95; Stone et al., 2004). Nevertheless, the original study sample size was relatively small. Recent research examining its psychometrics is limited.
```

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0011
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Results > Psychiatric Comorbidities in Children and Adolescents With Autism Spectrum Disorders · results · text · 139 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×3, supplementary-material×3.

```text
Random effect analysis for each comorbidity in all pediatric populations, children and adolescents, in addition to heterogeneity for each analysis can be found in Table 1. Prevalence of ID in all pediatric populations was found as 22.9% (95% CI: 17.7- 29.2) (Figure 2). Prevalence of ADHD in all pediatric populations was found as 26.2% (Figure 3) and prevalence of anxiety disorders in all pediatric populations was found as 11.1% (Figure 4). All statistical analysis groups showed high heterogeneity as shown by I value higher than 84.
```

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0012
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Results > Psychiatric Comorbidities in Children and Adolescents With Autism Spectrum Disorders · results · table · 580 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×3, supplementary-material×3.

```text
TABLE 1
Population-based psychiatric comorbidity studies in children and adolescents with autism spectrum disorders.
|  |  |  |  |  | Heterogeneity analysis |
| Comorbidity | Study Population | Number of study groups | Total number of patients | Prevalence (95% CI) | Heterogeneity I2 | Cochran Q, p value |
|---|---|---|---|---|---|---|
| Intellectual disability | All pediatric population | 33 | 136155 | 22.9 (17.7- 29.2) | 99.76 | 13430, < 0.001 |
|  | Children | 22 | 58849 | 21.4 (15.2- 29.2) | 99.57 | 4886, < 0.001 |
|  | Adolescent | 4 | 35540 | 15.6 (5.8- 35.8) | 99.91 | 3502, < 0.001 |
| ADHD | All pediatric population | 21 | 126951 | 26.2 (22-31) | 99.72 | 7164, < 0.001 |
|  | Children | 10 | 49617 | 18.4 (12.3- 26.6) | 99.76 | 3716, < 0.001 |
|  | Adolescent | 3 | 32163 | 35.4 (21.9-51.7) | 99.86 | 1477, < 0.001 |
| Anxiety disorders | All pediatric population | 19 | 97791 | 11.1 (8.6-14.1) | 99.56 | 4117, < 0.001 |
|  | Children | 11 | 51688 | 7.8 (5.3- 11.3) | 99.4 | 1667, < 0.001 |
|  | Adolescent | 5 | 38746 | 21.5 (14-31.6) | 99.73 | 1468, < 0.001 |
```

### ASD-CSV-011@snapshot-20261017-d2b24dd227f9#section_v2_1#0009
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Methods > Outcomes > Primary Outcome · methods · text · 19 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×10, media×7, supplementary-material×7.

```text
Adaptive functioning was rated at a minimum of 8 weeks by the parent or clinician.
```

### ASD-CSV-017@PMC12208088.2; acquired 2026-10-30#section_v2_1#0013
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Results · results · table · 501 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2.

```text
Table 1
Summary of coded variables for included single-case studies
| Study authors; design | Participants | Intervention characteristics | DV characteristics | Outcomes |  |
| ID: age, gender | Language description | NDBI | Partner: context, location | AAC system | Expression or comprehension, language domain: DV | Gainscore | Tau U | Certainty of evidence |
|---|---|---|---|---|---|---|---|---|
| NDBIs Without AAC (NDBI-Only) |
| D’Agostino et al. (2020); MPP | Aaron: 4;1, M | One-word requests | IT | Teacher: play, classroom | N/A | Expression, syntactic: independent 3-word requests | + 10.2 | 1 | Strong |
| Hampton et al. (2019); MBP | Musa: 7;2, M Tahir: 5;11, M Imram: 7;10, M | < 10 spoken words | EMT | Researcher: play, playroom at school | N/A | Expression, semantic: # different words Expression, social communication: # spontaneous utterances | + 4.4 + 11.9 + 6.5 + 6.4 + 7.7 + 5.5 | 0.58 0.99 0.82 0.63 0.95 0.76 | Strong |
| Hampton et al., (2021); MBP | Ken: 4;9, M Jack: 4;9, M Sean: 3;5, M | < 25 words in 20 min | JASP + EMT | Researchers: play, clinic | N/A | Expression, social communication: # total social language utterances Expression, social communication: # spontaneous social language utterances | + 27.6 + 21.6 + 16.8 + 14.9 + 19.3 + 10.4 | 0.91 0.77 0.81 0.72 0.81 0.69 | Strong |
```

### ASD-CSV-017@PMC12208088.2; acquired 2026-10-30#section_v2_1#0028
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > NDBI-Only Studies > Study Characteristics · results · text · 224 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2.

```text
Members of the research team trained specifically for the study protocol served as interventionists for almost two thirds of NDBI-Only studies (12/19 = 63%). Most studies took place during play (12/19 = 63%), with school as the most common study context (9/19 = 47%). Almost all NDBI-Only studies cited manualized interventions as the independent variable (e.g., EMT, JASPER, PRT; 17/19 = 89%). Measures of language expression accounted for most outcome variables (32/37 = 86%), with one study including a standardized composite measure of expression and comprehension (Engelstad et al., 2020). Single-case studies mostly targeted criterion-referenced language outcome measures designed for the study, while group studies had a mixture of standardized and criterion-referenced measures. Studies mostly targeted social communication and requesting variables, though both semantic and syntactic outcomes were represented.
```

### ASD-CSV-018@snapshot-20261017-32e950efe2f1#section_v2_1#0017
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Results > Descriptive Characteristics of Participants and Interventions · results · table · 575 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×1, supplementary-material×1.

```text
Table 1
Overview of 54 studies yielding 51 independent effect sizes
| Author(s) | Country | N | Mean age (Years) | Effect size (g) | Intervention name | Relevant dependent variables |
|---|---|---|---|---|---|---|
| Aldred et al., 2004 | United Kingdom | 28 | 3.83 | 0.25 | Social communication intervention | PB, AB, L |
| Alquraini et al., 2018 | Saudi Arabia | 28 | 3.70 | 2.44 | Responsive teaching | PB, L |
| Alvarado, 2017 | United States | 30 | 3.73 | 1.31 | Sensoriaffective interactional attunement scale-guided intervention | PB |
| Amrollahi far, 2017 | Iran | 30 | 7.23 | 0.51 | Play therapy training | L |
| Bearss et al., 2015b, 2016 | United States | 180 | 4.75 | 0.36 | Behavioral interventions | MB |
| Beaudoin et al., 2019 | Canada | 19 | 2.13 | 0.00 | Parent implemented early start denver model (P-ESDM) | PB |
| Brian et al., 2017 | Canada | 62 | 2.10 | 0.99 | Social ABCs parent-mediated intervention | PB, L |
| Byford et al., 2015 | United Kingdom | 146 | 4.00 | 0.41 | Pre-School Autism Communication Trial (PACT) | L |
| Carter et al., 2011 | United States | 50 | 1.67 | 0.00 | Hanen’s ‘More Than Words’ | PB, L |
| Casenhiser et al., 2013, 2015 | Canada | 51 | 3.71 | 0.72 | Milton & ethel harris research initiative (MEHRI) | PB, L |
| Cook et al., 2019 | Australia | 31 | 5.50 | 0.00 | Cognitive behavioral therapy (CBT) | MB |
| Dekker et al., 2019 | Netherlands | 69 | 11.00 | 0.43 | Social skills group training | PB |
```

### ASD-CSV-018@snapshot-20261017-32e950efe2f1#section_v2_1#0022
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > Descriptive Characteristics of Participants and Interventions · results · text · 22 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×1, supplementary-material×1.

```text
PB positive behavior/social skills, MB maladaptive behavior, AB adaptive behavior/life skills, L language/communication
```

### ASD-CSV-019@snapshot-20261017-348b80144069#section_v2_1#0010
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Methods > Data Extraction · methods · table · 278 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1.

```text
Table 1
Overview of characteristics extracted for each reviewed study
|  | Type of question that coders addressed during data extraction |
| Type of data extracted | Open-ended question | Forced-choice question |
|---|---|---|
| i. Study characteristics | Country of origin; Inclusion/exclusion criteria; Recruitment procedure; Allocation | Study design (group or single-subject) |
| ii. Participants characteristics | Number of participants (all/autistic); Age (mean; range in years) or grade; Gender distribution (female: male); ASD diagnosis (name diagnosis, n); Additional diagnoses/disabilities (name diagnosis, n) | - |
| iii. Setting | - | School setting (primary or secondary); Inclusion method adopted by the school (individual inclusion, group inclusion, or special classes) |
| iv. Measures | Dependent variables (one entry per variable); Measurement instruments; Number and length of measurements (n baseline; n during intervention; n after intervention, n follow-up; others) | - |
| v. Intervention characteristics | Intervention approach; Number of cycles; Timeframe; Co-interventions | Targeted level of school environment (child, peers, staff, or physical environment); Interventionist/trainer (researcher or teacher/school staff) |
| vi. Outcomes | Comparison outcomes; Statistical techniques; Effect size | - |
```

### ASD-CSV-019@snapshot-20261017-348b80144069#section_v2_1#0021
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > Type of Interventions and Outcomes · results · text · 152 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1.

```text
Twelve (21%) studies applied the intervention at child level; nine (16%) at peer level; seven (13%) at staff level; and four (7%) at physical environment level. The remaining 24 (43%) studies implemented the intervention at multiple levels of the school environment: four targeting at both the child and the peers, and one at both the child and the staff; 18 targeting at the peers, but also adding an adult facilitator who was either someone from the research team (n = 6) or a school staff who received training (n = 12); and one covering all of the four levels (Chung & Douglas, 2015).
```

### ASD-CSV-020@snapshot-20261017-4e37d7309019#section_v2_1#0009
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Systematic review method > Data collection > Methodological quality of included studies · body · text · 150 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×5, media×1, supplementary-material×1.

```text
Quality was assessed using the Quality Assessment Tool for Observational Cohort and Cross-Sectional Studies (National Institutes of Health, 2016). The instrument comprises 14 items addressing aspects including the research question, study population, sample size justifications, measures, and assessment tools validity. One of three quality levels—good, fair, or low—is assigned to the study according to how these elements affected the methodological quality aspects of the study. The first author (V.P.) assessed the quality of all reports, and the third author (L.C.) assessed 47 (20%) of retrieved reports with 93% inter-rater reliability on the overall grade (Belur et al., 2021).
```

### ASD-CSV-020@snapshot-20261017-4e37d7309019#section_v2_1#0013
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Systematic review results · body · table · 105 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×5, media×1, supplementary-material×1.

```text
Table 1.
Frequent design of retrieved studies.
| Most frequent study designs | Frequency |
|---|---|
| Single case experimental design | 90 |
| Randomized controlled trial (RCT) | 28 |
| Quasi-experimental design | 23 |
| Case study | 15 |
| Qualitative design | 15 |
| Other experimental research design | 13 |
| Exploratory/pilot study | 12 |
| Mixed methods | 12 |
```

### ASD-CSV-029@snapshot-20261017-333b6e82d086#section_v2_1#0011
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Abstract > Introduction · introduction · text · 461 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1, media×1, supplementary-material×1.

```text
The urgency of early detection is underscored by the broader context of youth mental health; recent data highlights the escalating burden of neurodevelopmental and mental health disorders among children globally, and particularly in Asia, making effective primary care screening an imperative public health priority.

Recognising that comprehensive early intervention, especially before 24 months of age—such as Naturalistic Developmental Behavioural Interventions, targeted speech therapy and structured play-based therapies—can significantly enhance cognitive and adaptive skills. Hence, public health initiatives must prioritise timely and effective screening. To address this need, the Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) has become a prominent two-stage, parent-dependent screening tool. It consists of 20 yes/no questions that take approximately 5 to 10 min for a caregiver to complete, designed for toddlers aged 16 to 30 months. The revision aimed at lowering false-positive results while ensuring high sensitivity. Recent systematic reviews validate its strong psychometric attributes, showing a sensitivity rate of 78% (95% CI 0.57 to 0.91) and a specificity rate of 0.98 (95% CI 0.88 to 1.00), making it highly recommended for early ASD detection.

The M-CHAT-R/F is a key screening tool, distinct from the comprehensive diagnostic instruments required for a formal evaluation. This diagnostic landscape includes gold-standard tools like the Autism Diagnostic Observation Schedule (sensitivity 87%, specificity 75%), the Childhood Autism Rating Scale (sensitivity 89%, specificity 79%) and the Autism Diagnostic Interview-Revised diagnostic interview. While all are part of the assessment pathway, the M-CHAT-R/F stands out for its suitability for widespread primary care use because it is a concise, parent-completed tool.

Despite the M-CHAT-R/F’s broad acceptance, including its adaptation for diverse cultural contexts like Malaysia, there are still significant gaps in the compiled evidence. Current research shows a considerable variation in outcomes, attributable to differences in study designs, characteristics of the samples and methods of confirming diagnoses. This inconsistency poses challenges for healthcare professionals and policymakers in establishing screening programmes that are based on solid evidence.
```

### ASD-CSV-029@snapshot-20261017-333b6e82d086#section_v2_1#0023
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Abstract > Result > Summary of included study characteristics · abstract · table · 286 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×1, media×1, supplementary-material×1.

```text
| Study author | Year | Country | Region | Study design | Sample (12 633) | Age (months) | Quality (JBI) |
|---|---|---|---|---|---|---|---|
| Sturner et al | 2022 | USA | Americas | Prospective Case-Control | 408 | 16–20 | High |
| Choueiri et al | 2021 | USA | Americas | Cross-Sectional | 81 | 18–36 | High |
| Mata-Iturralde et al | 2025 | Ecuador | Americas | Cross-Sectional | 613 | 18–48 | High |
| Zhang et al | 2022 | China | Western Pacific | Prospective Cohort | 11 190 | 18–24 | High |
| Wong et al | 2025 | Singapore | Western Pacific | Prospective Cohort | 141 | 12, 18, 30 | High |
| Mukherjee et al | 2024 | India | South-East Asia | Cross-Sectional | 200 | 16–30 | High |
JBI, Joanna Briggs Institute.
```

### ASD-CSV-038@snapshot-20261017-3eb466122957#section_v2_1#0007
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Key words > Design and methods > Measurements of ASD > Phase II: Comprehensive diagnostic assessment · body · text · 228 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: disp-formula×1, graphic×2.

```text
Phase II aimed to confirm the ASD among the selected group of children already considered to be at high risk, that is, children with positive-screening result. These screen-positive children were invited for a further comprehensive diagnostic assessment. We used DSM-IV for diagnosis of ASD because it has been widely used in Vietnam and other countries. The newer version, DSMV, introduced in 2013, has not yet been tested in Vietnam. For each screen-positive child, two screen-negative children matched on major socio-economic factors (e.g., age group, sex and healthcare setting), were randomly selected and invited for a further assessment. As recommended by the AAP, a multi-disciplinary team, composed of a neurologist and a child psychologist, performed the comprehensive diagnostic assessment for the study. Eight professionals from Department of Psychiatry, National Hospital of Pediatrics were recruited. These professionals were experienced experts in ASD diagnosis and intervention. The team performed an ASD diagnostic assessment, identified the mimic ASD or comorbid conditions, and determined functional levels of all participants. The average length of time for the diagnosis ranged from 40 minutes to 1 hour.
```

### ASD-CSV-038@snapshot-20261017-3eb466122957#section_v2_1#0016
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Key words > Discussion · discussion · table · 576 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: disp-formula×1, graphic×2.

```text
Table 1.
Socio-economic status, parental characteristics and their association with autism spectrum disorders (ASD) in children aged 18 to 30 months.
| Variables | N (%) | ASD prevalence* |  |  |  |
|  | Frequency | Percentage | Frequency | Percentage | OR | 95%CI |
|  | (n) | (%) | (n) | (%) |  | Lower | Upper |
|---|---|---|---|---|---|---|---|
| Total number of participants | 40.243 | 100% | 305 | 0.758 |  |  |  |
| Province |  |  |  |  |  |  |  |
| Ha Noi | 5.501 | 13.7 | 46 | 0.84 | 1.18 | 0.77 | 1.79 |
| Thai Binh | 5.883 | 14.6 | 41 | 0.70 | 0.98 | 0.64 | 1.51 |
| Hoa Binh | 5.893 | 14.6 | 43 | 0.73 | 1.03 | 0.67 | 1.57 |
| Quang Nam | 5.539 | 13.8 | 45 | 0.81 | 1.14 | 0.75 | 1.74 |
| Dong Thap | 5.600 | 13.9 | 38 | 0.68 | 0.95 | 0.61 | 1.48 |
| Dong Nai | 5.922 | 14.7 | 50 | 0.84 | 1.19 | 0.79 | 1.79 |
| Dak Lak | 5.905 | 14.7 | 42 | 0.71 | 1 | - | - |
| Age group |  |  |  |  |  |  |  |
| 18-23 months | 17.193 | 42.7 | 119 | 0.69 | 0.86 | 0.68 | 1.08 |
*Result from univariate logistic regression
bstatistically significant at p<0.01
cstatistically significant at p<0.001.
```

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v2_1#0016
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Results > Parents' and Teachers' Reports of ADHD and Anxiety Symptoms · results · table · 219 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Mean standard scores of parent and teacher ratings on CRS subdomains.
|  | Parents | Teacher | F(1, 249) | η |
|---|---|---|---|---|
| CRS IA | 65.08 (11.28) | 61.26 (11.06) | 24.73*** | 0.09 |
| CRS HI | 62.59 (11.94) | 58.18 (11.26) | 31.69*** | 0.11 |
| CRS Anxiety | 61.40 (13.75) | 68.25 (13.37) | 44.14*** | 0.15 |
CRS, Conners' rating scales; IA, inattention; HI, hyperactivity/impulsivity.
***
p < 0.001.
```

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v2_1#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Results > Clinical Presentation of ASD With and Without Clinically Elevated ADHD and Anxiety Symptoms · results · text · 128 tokens · trang [None, None]
- completeness: complete

```text
We compared the four defined groups based on the CPRS ADHD index scores and the anxious-shy scores. The male:female ratio did not differ significantly among the groups in a non-parametric chi-square analysis [χ (3)2 = 3.18, p > 0.05]. As presented in Table 2, parental ages at pregnancy and educational attainment in the four examined groups were not significantly different using one-way MANOVAs. Only the ANOVA for the child's age yielded a significant main effect, however post-hoc Scheffe analysis did not reveal any significant difference between each pair of the groups.
```

### ASD-CSV-078@snapshot-20261017-e028758ec231#section_v2_1#0005
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Data compiled and results gathered · body · text · 440 tokens · trang [None, None]
- completeness: complete

```text
ADI-R = Autism Diagnostic Interview-Revised; ADHD = Attention Deficit Hyperactivity Disorder; ADOS = Autism Diagnostic Observation Schedule; ANCOVAs = Univariate Analyses of Covariance; ANOVA = Analysis of Variance; ASD = Autism Spectrum Disorder; AQ = Autism Spectrum Quotient; BAARS-IV = Barkley Adult ADHD Rating Scale-IV; BDI-II = Beck Depression Inventory II; BSID-III = Bayley Scales of Infant and Toddler Development-Third Edition; CARS-2 = Childhood Autism Rating Scale- Second Edition; CPT-II = Conners’ Continuous Performance Test II; CSI-4 = Child Symptom Inventory-4; DD = Depressive Disorder; DICA-P = Diagnostic Interview for Children and Adolescents; DISCO-10 = Diagnostic for Social and Communication Disorders-Tenth Edition; DIVA = Diagnostic Interview for ADHD in Adults; DPCR = Danish Psychiatric Central Registrar; DSM-IIIR = Diagnostic and Statistical Manual of Mental Disorders–Third Edition; DSM-IV = Diagnostic and Statistical Manual of Mental Disorders–Fourth Edition; DSM-5 = Diagnostic and Statistical Manual of Mental Disorders–Fifth Edition; ECBQ = Early Childhood Behavior Questionnaire; GAD = Generalized Anxiety Disorder; GD = Gender Dysphoria; GMDQ = Gross Motor Development Quotient; IBQ-R = Infant Behavior Questionnaire-Revised; ICD-10 = International Classification of Diseases-Tenth Revision; MASC = Multidimensional Anxiety Scale for Children; MINI interview = Mini International Neuropsychiatric Interview; OR = Odds Ratio; Rx = Prescription; SAD = Separation Anxiety Disorder; SD = Standard Deviation; SE = Standard Error; SRS-2 = Social Responsive Scale-Second Edition; SSRT = Stop-Signal Reaction Time; SUD = Substance use Disorder; TGMD-2 = Test of Gross Motor Development- Second Edition; WISC-IV = Weschler Intelligence Scale for Children-Fourth Edition; WPPSI-III = Weschler Preschool and Primary Scale of Intelligence-Third Edition; 95% CI = 95% Confidence Interval
```

### ASD-CSV-078@snapshot-20261017-e028758ec231#section_v2_1#0006
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Data compiled and results gathered · body · table · 542 tokens · trang [None, None]
- completeness: complete

```text
| Authors | Purpose of study | Participants | Study design/measures | Results |
| Jensen et al. (2014) [9] | Assess the presence of comorbid developmental disorders with ADHD | 825 individuals diagnosed with ADHD between 4-17 years of age. 79.4% males; 20.6% females. Male diagnosis (mean = 9.6, SD = 3.4), female diagnosis (mean = 10.7, SD = 3.9 years) | ICD-10 criteria; general intelligence and neurophysiological testing; teacher-reported and parent-reported behavior and functioning information collected | 1) Anxiety disorders+ADHD were identified in late childhood or early adolescence. The most common comorbid disorders in ADHD patients were conduct disorders (16.5%), specific developmental disorders of language, learning, and motor skills (15.4%), autism spectrum disorder (12.4%), and intellectual disability (7.9%). 2) Males were diagnosed with anxiety at significantly lower rates (1% vs. 2.1%; OR:0.60; 95%CI: 0.40-0.80, p<0.01). 3) After adjusting for age, females were at a higher risk for comorbid affective disorders (1.3% vs. 4.5%, p<0.01), anxiety disorders (1% vs. 2.1%, p<0.01), reactions to severe stress (2.2% vs 6.7%, p<0.01), and eating disorders (0.1% vs. 1.3%, p<0.01). 4) After adjusting for age, males were at a greater risk of for comorbid autism spectrum disorder (13.3% vs. 9.2%, p<0.01), conduct disorder (17.2% vs. 13.7%, p<0.01), tic disorders (5.3% vs. 2.9%, p<0.01), and specific disorders of development (16.1% vs. 12.8%, p<0.01). 5) Low reporting of anxiety symptoms (1.3%) and affective disorders (2%) compared to previous studies is likely due to interpretation as a reaction to life stressors, not as a disorder, as theorized by the authors. 6) ADHD/tic disorders were strongly related to anxiety disorders |
```

### ASD-CSV-081@snapshot-20261017-2953560d938b#section_v2_1#0006
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Materials and methods > Participants · methods · table · 525 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Participant demographics.
| Participants Group (N = 24) | Participant code | Mainstream Education setting | Group format | Length of interview | Gender | Age | Ethnicity; first language | Number of children | Details of children with ASD | Other information |
|---|---|---|---|---|---|---|---|---|---|---|
| Parents (N = 8) | Parent 1 | Primary | Individual | Approx. 60 mins | Female | 42 | White British; English | 4 | Son Age 8Diagnosed age 5; co-occurring speech and language difficulties, seizures |  |
|  | Parent 2 | Primary | Group 1 | 120 mins | Female | 50 | White British; English | 3 | Son age 11;Diagnosed age 10 |  |
|  | Parent 3 | Primary | Group 1 | – | Female | 44 | White British; English | 3 | Daughter age 9; diagnosed age 7; co-occurring ADHD, sensory processing difficulties, Hypermobility) | Parent of CYP1 |
|  | Parent 4 | Primary | Group 1 | – | Female | 26 | White British; English | 1 | Son age 7; diagnosed age 2yrs 10 months; co-occurring Anxiety; hypermobility) |  |
|  | Parent 5 | Primary | Group 1 | – | Female | 43 | White British;English | 3 | Daughter age 7; diagnosed age 4 |  |
|  | Parent 6 | Secondary | Individual | Approx. 60 mins | Female | 45 | White British; English | 2 | 2 sons with ASD: age 17 (diagnosed age 3; co-occurring global learning disability); age 14 (diagnosed age 9; co-occurring ADHD, dyspraxia) | Parent of CYP2 |
|  | ³Parent 7 | Secondary | Group 2 / individual | (Group2: 67 mins; individual: 64 mins) | Male | 57 | White British; English | _² | Granddaughter (NB: identifies as non-binary) age 15; Diagnosed age 8; co-occurring epilepsy) |  |
```

### ASD-CSV-081@snapshot-20261017-2953560d938b#section_v2_1#0009
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Materials and methods > Participants · methods · text · 278 tokens · trang [None, None]
- completeness: complete

```text
Diagnosed with ASD.

A hyphen indicates that the participant did not answer these questions when requested.

³Grandparent who was primary carer.

Age ranges of autistic children staff worked with.

The term ‘parent’ will be used to denote parent or grandparent primary carer; ‘staff’ to denote school SEN teaching staff; and ‘child(ren)’ or ‘young person’ to denote the young people involved in the study or the children referred to by parents and staff participants.

- twelve school SEN teaching staff (assistant head (n = 1), SENCO (n = 4), class teacher (n = 3), teaching assistant (TA)(n = 4) (mean age: 34.6; age range: 21-63)

- seven parents and one grandparent who were primary carers of ten children with ASD (mean age: 43.4; age range: 26-57; mean age of child with ASD: 10.7; eight of the children had additional needs)

- 4 children with a diagnosis of ASD (mean age: 12.3; age range: 9-15; one with co-occurring attention deficit hyperactivity disorder (ADHD) and sensory processing difficulties)
```

### ASD-CSV-084@snapshot-20261017-b09029e5368f#section_v2_1#0013
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > Effectiveness of AAC · results · text · 236 tokens · trang [None, None]
- completeness: complete

```text
AAC has also been found effective for reducing challenging behaviors.20,21,26,28,29,32,36 Interventions reported in Table 1 were of functional communication training, in which AAC was taught as a replacement behavior.1 In addition, reduction in challenging behavior has been examined as a nontargeted, but rather collateral outcome, again with the rationale that AAC would provide a functional behavior as a replacement (eg, Ganz et al28).

In many reviews, speech as an outcome, but usually not as a primary target of intervention, was examined. Results point mostly to negligible or small effects.25,28,32 The two reviews focused on speech outcomes were motivated by a concern often expressed in AAC literature about the potential for AAC to impede speech development, as well as a desire to investigate the potential for speech to be enhanced.33,34 These reviews indicate variable outcomes, with Schlosser and Wendt34 finding that, for individuals with autism, although modest gains in speech could not be attributable directly to AAC intervention, there was no evidence of loss of speech skills.
```

### ASD-CSV-084@snapshot-20261017-b09029e5368f#section_v2_1#0030
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 403 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Summaries of included reviews
| Study | Aims (review period) | Effect size indicator | Key findings |
|---|---|---|---|
| Overall effectiveness and comparison across variables |
| Ganz et al19 | Meta-analysis of ESCD for effects of AAC on communication, social skills, and CB, and differences across age and autism diagnostic categories (1980–2008) | IRD | •24 studies•Aided AAC: PECS, SGD, PIC; key outcomes included requesting (n=13), social communication (n=4), CB (n=4), vocalizations or speech (n=5), spelling (n=2), and word comprehension and production (n=1)•IRD across diagnostic groups: autism =0.83; autism + DD =0.70; autism + multiple comorbidities =0.53•IRD across age groups: preschool =0.86; elementary =0.70; secondary = 0.64 |
| Ganz et al20 | Meta-analysis of ESCD studies of individuals with autism for effects of AAC on communication, social skills, CB, and academic skills (1980–2008) | IRD | •24 studies; 64% of children•Aided AAC: PECS, PIC, SGD; key outcomes included requests (n=13), social communication (n=4), CB (n=4), vocalizations or speech (n=5), spelling (n=2), use of SGD (n=2)•Using 84% CI for IRD: overall effects =0.99; communication =0.99; social skills =0.90, CB =0.80; academic skills =0.79•PECS and SGD =0.99; PICs =0.61 |
```

### ASD-CSV-088@snapshot-20261017-4ddce5ed1e86#section_v2_1#0003
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Introduction · introduction · table · 518 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Summary of studies that have examined the prevalence rates (%) of psychiatric comorbid disorders in children with ASD using (semi-) structured diagnostic interviews
| First author | Year | Age range | ASD subtype and (sub)sample size | PSY | MDD | DYS | SOC | SAD | SPH | GAD | OCD | AGO | PAN | ADHD | ODD | CD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Amr | 2012 | 4–11 | AD (n = 55); PDD-NOS (n = 5) | 63.3 | 13.3 | NR | NR | 8.3 | 40.0 b | 10.0 | 55.0 a | NR | NR | 31.6 c | NR | 23.3 |
| de Bruin | 2007 | 6–12 | PDD-NOS (N = 94) | 80.9 | 10.6 | 2.1 | 11.7 | 8.5 | 38.3 b | 5.3 | 6.4 | 6.4 | 1.1 | 44.7 a | 37.2 c | 9.6 |
| Gjevik | 2011 | 6–18 | AD (n = 47); AS (n = 12); PDD-NOS (n = 12) | 71.8 | 1.4 | 1.4 | 7.0 | 0.0 | 30.9 a | 0.0 | 9.8 c | NR | NR | 30.9 a | 4.2 | 2.8 |
| Leyfer | 2006 | 5–17 | AUT (N = 109) | 73.0 | 10.1 | NR | 7.5 | 11.9 | 44.3 a | 2.4 | 37.2 b | NR | 0.0 | 30.6 c | 7.0 | NR |
```

### ASD-CSV-088@snapshot-20261017-4ddce5ed1e86#section_v2_1#0009
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Method > Participants · methods · text · 463 tokens · trang [None, None]
- completeness: complete

```text
1986), the ratings on the Child Behavior Check List, CBCL (Achenbach 1991), and/or the impairment of attention problems for those children in daily functioning).

Of the children with ASD, 28 (70.0 %) were diagnosed with PDD-NOS and 12 children were diagnosed with Aspergers’ Syndrome (30.0 %). Of the ADHD sample, 23 children were classified as having ADHD-combined type (57.5 %), nine as having ADHD-inattentive type (22.5 %) and five as having ADHD-hyperactivity type (12.5 %). For three children (7.5 %), DSM-IV-TR classification of ADHD was postponed (i.e. a formal diagnosis of ADHD was not received because families dropped out). However, we decided not to exclude those three children from the study because they all met DSM-IV criteria of ADHD based on the KID-SCID. None of the children in the ADHD sample were suspected of having ASD.

The ASD sample consisted of 36 boys and four girls with a mean age of 11.10 years (range = 8–18 years; SD = 2.82). The ADHD sample consisted of 37 boys and three girls and had a mean age of 11.13 years (range = 7–17 years; SD = 2.85). No group differences were found for gender, X (1) = 0.157; p = .692, or age, F (1, 78) = 0.002; p = .969. For a summary of the education level and cognitive functioning of both groups, see Table 2. No differences between groups were found for primary education level, X (1) = 0.005; p = 1.00, secondary education level, Mann-Whitney U = 43.50; p = .260, or level of cognitive functioning, Mann–Whitney U = 487.50; p = .371.
```

### ASD-CSV-089@snapshot-20261017-9ad7387ead22#section_v2_1#0010
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Methods > Information Sources · methods · table · 525 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2.

```text
Table 1
Search terms.
| Database and Search terms | Limitations | Number of abstracts |
|---|---|---|
| Subject Headings:CINAHL: (MH “autistic disorder”) or (MH “child development disorders, pervasive”) or (MH “pervasive developmental disorder—not otherwise specified”), and (MH “rural health centers”) or (MH “hospitals, rural”) or (MH “rural population”) or (MH “rural health services”) or (MH “rural areas”) or (MH “services for Australian rural and remote allied health”) or (MH “rural health”) or (MH “rural health personnel”) or (MH “telehealth”) or (MH “telemedicine”) or (MH “videoconferencing”) or (MH “teleconferencing”) | English language | 80 |
| ERIC: SU.EXACT(“Asperger syndrome”) or SU.EXACT(“pervasive developmental disorders”) or SU.EXACT(“autism”), and SU.EXACT(“rural population”) or SU.EXACT(“rural areas”) or SU.EXACT(“rural youth”) or SU.EXACT(“rural environment”) or SU.EXACT(“rural education”) or SU.EXACT(“teleconferencing”) or SU.EXACT(“telecourses”) or SU.EXACT(“videoconferencing”) or SU.EXACT(“telecommunications”) | English language | 29 |
| Embase: autism or Asperger syndrome or “pervasive developmental disorder not otherwise specified,” and (rural health care or rural area or urban rural difference or rural population) or (teleconsultation or telediagnosis or telehealth or telemedicine or telemonitoring or teletherapy or videoconferencing or teleconference or health care delivery) | English language | 406 |
| PsycINFO: autism or pervasive developmental disorders or Aspergers syndrome, and (exp rural environments or distance education) or (telemedicine or computer mediated communication or telecommunications media) | English language | 64 |
| PubMed : (“Autistic disorder” [Mesh] or “child development disorders, pervasive” [Mesh]) and (“rural population” [Mesh] or “rural health services” [Mesh] or “rural health” [Mesh] or “remote consultation” [Mesh] or “telemedicine” [Mesh] or “videoconferencing” [Mesh]) | English language | 45 |
```

### ASD-CSV-089@snapshot-20261017-9ad7387ead22#section_v2_1#0014
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Methods > Methodological Quality · methods · text · 172 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2.

```text
Methodological quality was assessed using the standard quality assessment criteria as described by Kmet et al [40]. The Kmet appraisal checklist uses a 3-point ordinal system to assess the methodological quality of research papers. The appraisal checklist creates a systematic, quantitative, and reproducible process to assess the methodological quality of a variety of research designs and make comparisons between them. Two authors independently assessed the included articles using the 14-point checklist. Scores were categorized into quality levels: >80% as strong, 70-80% as good, 50-69% adequate, and <50% as limited. The methodological scores are included in Table 2. Disagreements in methodological quality existed between the 2 authors in 2 out of the 9 articles and were resolved through discussion and consensus.
```

### ASD-CSV-091@snapshot-20261017-d0bfc4f35cad#section_v2_1#0016
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 2. Literature Review: ASD Screening Methods > 2.2. Adolescents and Adults ASD Screening Methods > The Ritvo Autism Asperger Diagnostic Scale- Revised (RAADS-R) · body · text · 380 tokens · trang [None, None]
- completeness: complete

```text
The RAADS-R is the latest and only self-scoring ASD screening tool developed for only adults (18 +). Created by Dr. Ariella Riva Ritvo in 2011, the intention was to identify undiagnosed adults with ASD and related social and communication disorders. The initial version of RAADS consists of a 78-item questionnaire covering three areas of neurodevelopment including language, social relatedness, and sensory motor. The RAADS-R is the revised version that covers an additional area of development—circumscribed interest [53] The RAADS-R version has 80 item instruments, including 78 items from the initial version. The RAADS is available online and takes approximately 20 min to complete the screening. Each item has four different parts, with different score values ranging from 0–3. These are ”true now and when I was young”, ”true only now”, ”true only when I was younger than 16”, and ”never true”. At the end of each screening, an overall score is generated based on the answers given to the questions. The users who gain an overall score below 65 are identified as the controls and the users who score above 65 are directed to further evaluations and clinical diagnosis for ASD. Further, each subscale of items is given a threshold score and anyone scoring above the threshold poses a risk of having ASD or other related disorder. The RAADS-R is considered to be an acceptable ASD screening instrument with 97% sensitivity and 100% specificity according to [53]. Further studies carried out by the authors on the validity of RAADS-R, using 779 samples, confirmed that only 3 users out of 100 receive false results from this tool, meaning that the tool generated 97% accurate information [53].
```

### ASD-CSV-091@snapshot-20261017-d0bfc4f35cad#section_v2_1#0060
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 560 tokens · trang [None, None]
- completeness: complete

```text
ijerph-16-03502-t001_Table 1Table 1
Summary of screening methods available for infants and children.
| METHOD | TYPE | FEES | ITEMS | TARGET | AGE | TIME/MINS | SENSITIVITY | SPECIFICITY | WEB | MOBILE |
|---|---|---|---|---|---|---|---|---|---|---|
| CHAT (Checklist for Autism in Toddlers) | Questionnaire | N | 14 | Toddlers | 18-24 months | 8 to 15 | 40% | 98% | X | X |
| M-CHAT & M-CHAT-RF (Modified Checklist for Autism in Toddlers & With Follow Up) | Questionnaire |  | 23 | Toddlers | 16–30 months | 10 to 20 | 95-97% | 99% | X | X |
| Q-CHAT (Quantitative CHecklist for Autism in Toddler) | Questionnaire | N | 25 | Toddlers | 18 to 24 months | 15 to 20 | 88% | 91% | Y | X |
| Q-CHAT-10 | Questionnaire | N | 10 | Toddlers | 19 to 24 months | 5 to 10 | 91% | 89% | Y | X |
| CAST (Childhood Asperger Syndrome Test) | Questionnaire | N | 37 | Children | 5 to 11 years | 15 to 25 | 100% | 97% | Y | X |
| DBD-ES (Developmental Checklist-Early Screen) | Questionnaire | Y | 17 | Toddlers | 18 to 48 months | 10 to 15 | 83% | 48% | X | X |
| ESAT (Early Screening for Autistic Traits) | Questionnaire |  | 14 | Toddlers | 16 to 30 months | 10 to 15 | 88% | 14% | X | X |
| PDDST-II (Pervasive Developmental Disorders Screening Test-Second Edition) | Questionnaire | Y | 22 | Toddlers | 18 to 48 months | 10 to 20 | 92% | 91% | X | X |
```

### ASD-CSV-095@snapshot-20261017-113db93f3075#section_v2_1#0013
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Results > Participants · methods · table · 598 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×3.

```text
Table 1
Demographic and baseline characteristics of randomized groups
|  | Circadin® | Placebo | Overall |
|  | (N = 60) | (N = 65) | (N = 125) |
|---|---|---|---|
| Age, years |  |  |  |
| Mean ± SD | 9.0 ± 4.08 | 8.4 ± 4.24 | 8.7 ± 4.15 |
| Range | 2, 17 | 2, 17 | 2, 17 |
| Sex, n (%) |  |  |  |
| Male | 45 (75.0%) | 47 (72.3%) | 92 (73.6%) |
| Female | 15 (25.0%) | 18 (27.7%) | 33 (26.4%) |
| Ethnicity, n (%) |  |  |  |
| Not Hispanic or Latino | 40 (66.7%) | 49 (75.4%) | 89 (71.2%) |
| Hispanic or Latino | 12 (20.0%) | 7 (10.8%) | 19 (15.2%) |
| Other | 8 (13.3%) | 8 (12.3%) | 16 (12.8%) |
| Unknown | 0 | 1 (1.5%) | 1 (0.8%) |
| Race, n (%) |  |  |  |
| White | 57 (95.0%) | 55 (84.6%) | 112 (89.6%) |
| Black or African American | 1 (1.7%) | 8 (12.3%) | 9 (7.2%) |
| Other | 3 (5.0%) | 3 (4.6%) | 6 (4.8%) |
| Asian | 0 | 2 (3.1%) | 2 (1.6%) |
| Height, cm |  |  |  |
| Mean ± SD | 133.4 ± 24.17 | 130.4 ± 27.20 | 131.8 ± 25.73 |
| Range | 89, 180 | 79, 197 | 79, 197 |
```

### ASD-NEW-001@snapshot-20261017-7805dc60a910#section_v2_1#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Key Points > Methods > Randomization and Blinding · methods · text · 260 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2, media×3, supplementary-material×3.

```text
Eligible participants were randomized on a 1:1 ratio via a computer algorithm run by a clinical trial coordinator (K.V.), who communicated directly with the clinical team. Infants were randomized to receive either the iBASIS-VIPP intervention plus usual community care or usual community care only. Randomization was performed by minimization stratified by site (Perth or Melbourne), infant sex (male or female), number of behaviors indicating a higher likelihood of ASD on the SACS-R (endorsement of 3, 4, or 5 behaviors), and age range at recruitment (9-11 months or 12-14 months), with randomization determined by a biased coin with a probability of 0.7. The research staff conducting the assessments (S.P., M.B., L.C., S.D., and M.H.) were independent of the clinical teams administering the iBASIS-VIPP intervention (J.D., M.R., C.R., M.G., and S.W.); they were housed in separate buildings and unaware of the nature of the iBASIS-VIPP intervention (including hypothesized treatment mechanisms), the randomization methods, and the group allocations. Because the intervention was parent-mediated, families could not be blinded to group allocation.
```

### ASD-NEW-001@snapshot-20261017-7805dc60a910#section_v2_1#0027
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Key Points > CONSORT Flow Diagram > Participant Characteristics at Baseline · abstract · table · 342 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×2, media×3, supplementary-material×3.

```text
| Characteristic | No./total No. (%) |
| Usual care group (n = 53) | iBASIS-VIPP group (n = 50) |
|---|---|
| Families |  |  |
| Annual household income ≥$50 000 | 44/50 (88.0) | 40/42 (95.2) |
| Mother completed university degree | 29/53 (54.7) | 33/50 (66.0) |
| Infant living with both biological parents | 52/53 (98.1) | 49/50 (98.0) |
| Infants |  |  |
| Sex |  |  |
| Female | 21/53 (39.6) | 12/50 (24.0) |
| Male | 32/53 (60.4) | 38/50 (76.0) |
| Older sibling with ASD | 10/53 (18.9) | 10/50 (20.0) |
| Chronological age, mean (SD), mo | 12.38 (2.02) | 12.40 (1.93) |
| Adjusted age, mean (SD), mo | 12.31 (2.00) | 12.12 (1.98) |
```

### ASD-NEW-002@snapshot-20261017-5ff219bd462c#section_v2_1#0019
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Data Availability > Results > Characteristics of included parenting interventions. · results · table · 523 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×11, media×8, supplementary-material×8.

```text
| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving | Average Child Age at Baseline | Average Program Duration | Study Design (Unit of Randomization) | Delivery | Setting | Analytic Sample | Early child development outcomes | Parenting outcomes |
| Cognitive | Language | Motor | Socio-emotional | Behavior problems | Attachment | Knowledge | Practices | Parent-child interactions | Depression |
|---|---|---|---|---|---|---|---|---|---|---|
| Abessa et al., 2019 [74] Ethiopia | A family-based psychomotor/psychosocial stimulation intervention to provide treatment for children with severe acute malnutrition. Trained intervention nurses delivered hospital-based individual and group sessions to provide stimulation for children through play and to coach caregivers on how to stimulate their children. After being discharged, families received play materials and 3 follow-up home visits from play leaders who provided continued coaching. | No | 27.4 mo | 6.5 mo | Two-arm RCT (Individual) | Individual, Group | Hospital, Home | INT: 113 CTRL: 98 |  | X | X | X |  |  |  |  |  |  |
| Abimpaye et al., 2019 [39] Rwanda | First Steps, or “Intera za Mbere”, is a parenting education program utilizing a curriculum that focuses on promoting responsive caring and bonding, providing stimulation through playful learning, supporting child health, and promoting emergent literacy in the home. Both the “light touch” and “full” intervention groups received weekly parenting education sessions facilitated by radio, supported by a local volunteer. Additional elements in the “full intervention” group included more intensive training for the local volunteer, book gifting to participating families, and support from a facilitator to guide group sessions and conduct home visits. | Yes | 6–24 mo | 4.25 mo | Three-arm Cluster-RCT (Sector) | Individual, Group | Home, Community | INT: 486 CTRL: 479 | X | X | X | X |  |  |  | X |  |  |
CTRL, control group; ECD, early child development; EI, Educación Inicial; ICDS, Integrated Child Development Services; INT, intervention group; RCT, randomized controlled trial; RFS, Responsive Feeding and Stimulation; VIP, Video Interaction Project; VIPP, video-feedback intervention to promote positive parenting;
```

### ASD-NEW-002@snapshot-20261017-5ff219bd462c#section_v2_1#0039
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Data Availability > Results > Characteristics of included parenting interventions. · results · table · 489 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×11, media×8, supplementary-material×8.

```text
| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving | Average Child Age at Baseline | Average Program Duration | Study Design (Unit of Randomization) | Delivery | Setting | Analytic Sample | Early child development outcomes | Parenting outcomes |
| Cognitive | Language | Motor | Socio-emotional | Behavior problems | Attachment | Knowledge | Practices | Parent-child interactions | Depression |
|---|---|---|---|---|---|---|---|---|---|---|
| Kaminski et al., 2013 [119] USA | The Legacy program targeted families living below the poverty line and in receipt of welfare assistance, beginning in pregnancy (Los Angeles) and at birth (Miami). The focus was to support parents to provide nurturing and supportive environments through strengthening self-efficacy for parenting behaviors, parenting support, and commitment to parenting. Topics included sensitive and responsive affection, discipline, routines, play, language promotion, and school readiness. | Yes | LA: Antenatal; Miami: 0 mo | LA: 36 mo; Miami: 60 mo | Two-arm RCT (Individual) | Individual, Group | Community, University campus | LA: INT: 126 CTRL: 78 Miami: INT: 121 CTRL: 73 |  |  |  | X | X |  |  |  |  |  |
| Khan et al., 2018 [120] Pakistan | An intervention targeting infants from poor urban localities, which aimed to improve mothers’ ability to promote age-appropriate activities for ECD, improve child nutrition, and maternal mental health. Clinic assistants provided counseling for mothers during quarterly visits using a flip-book tool. | No | 0.5 mo | 6 mo | Two-arm Cluster RCT (Clinic) | Individual | Clinic | INT: 1,037 CTRL: 920 | X | X | X | X |  |  |  |  |  | X |
CTRL, control group; ECD, early child development; EI, Educación Inicial; ICDS, Integrated Child Development Services; INT, intervention group; RCT, randomized controlled trial; RFS, Responsive Feeding and Stimulation; VIP, Video Interaction Project; VIPP, video-feedback intervention to promote positive parenting;
```

### ASD-NEW-003@snapshot-20261017-03d7bc132930#section_v2_1#0020
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: 3. Assessment > 3.2. Assessment of Feeding Issues > 3.2.1. Standardized Questionnaires: Feeding Behaviors in Children · body · table · 139 tokens · trang [None, None]
- completeness: complete

```text
ijerph-20-05092-t001_Table 1Table 1
Descriptions of some main questionnaires regarding feeding behaviors.
| ID | Description | Authors |
|---|---|---|
| BAMBI-C | Brief Autism Mealtime Behavior Inventory | [49] |
| STEPS | Screening Tool of Feeding Problems | [66] |
| CEBI-R | Children’s Eating Behavior Inventory-Revised | [67] |
| BPFAS | Behavioral Paediatrics Feeding Assessment Scale | [63] |
| PASSFP | Paediatric Assessment Scale for Severe Feeding Problems | [68] |
```

### ASD-OA-PMC10018050@PMC distributed version 1#section_v2_1#0010
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Method > Trustworthiness · methods · text · 247 tokens · trang [None, None]
- completeness: complete

```text
Epistemologically, the researcher is an occupational therapist working from an occupational science frame of reference and a trained LTS instructor. There was no connection between the researcher and participants prior to the study. The researcher is from the same broader cultural background as the participants. The background knowledge available to the researcher enabled the researcher’s engagement in the research process. Strategies including bracketing, member checking, and peer review were utilized to ensure the trustworthiness of the research (Creswell, 2014; Wirihana et al., 2018). Bracketing took place during protocol development, data collection, and analysis. The sixth and seventh step of Colaizzi’s method requires participants to validate the findings (Wirihana et al., 2018). A summary was sent through email to all participants to provide feedback. In the 2 weeks allowed to provide feedback, six of the 11 participants (four parents and two teachers) responded. All six stated that they felt the results were a true reflection of their perceptions and experiences. An occupational therapist and master’s student read and co-coded a parent and teacher interview at the beginning of the data analysis process, from which no new codes emerged.
```

### ASD-OA-PMC10018050@PMC distributed version 1#section_v2_1#0013
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Method > Results · results · table · 262 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Parent and Child Participant Demographics.
| Participant | Child’s age at time of interview | Age when starting swimming lessons | Number of years in swimming lessons | Gender (child) | Socioeconomic status/community setting | Class size, frequency, and funding |
|---|---|---|---|---|---|---|
| P104 | 8 years | 3 years | 4–5 years | Male | Johannesburg East, middle class | 1:1, weekly, privately funded |
| P106 | 5 years | 4 years | 1 year | Male | Johannesburg East, middle class | 1:1, weekly, privately funded |
| P107-1P107-2 | 5 years | 4 years | 1 year | Male | Johannesburg North, middle class | 1:1, weekly, privately funded |
| P108 | 16 years | 6 months | 15 years | Female | Johannesburg North, upper class | 1:1, weekly, privately funded |
| P110 | 5 years | 4 years | 1 year | Male | Johannesburg North, upper class | 1:1, weekly, privately funded |
```

### ASD-OA-PMC10774556@PMC distributed version 1#section_v2_1#0008
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: COMBINED SYMPTOMS > Sleep · body · text · 195 tokens · trang [None, None]
- completeness: complete

```text
Individuals with autism and their parents frequently report sleep problems as a comorbid symptom. A recent review found that behavioral interventions increased sleep time and sleep efficiency, as well as a decrease in sleep latency, compared to the control group [50,51]. Another review that analyzed behavioral interventions for sleep problems found that different techniques were recommended depending on the specific sleep problem [52]. For instance, a faded bedtime1) is effective in initiating and maintaining sleep, whereas extinction2) and scheduled awakening3) are effective during nightwaking and night terror attacks, respectively. In terms of age, faded bedtime was applied to children aged 5–9 years, and the extinction technique was applied to children aged 2–12 years, both of which were effective [52]. Sleep hygiene and behavior interventions for improving sleep habits, such as bedtime routines and sleep schedules, are not sufficient but necessary components of most behavioral sleep interventions [52,53].
```

### ASD-OA-PMC10900867@PMC distributed version 1#section_v2_1#0012
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Results > Characteristics of participants · results · table · 589 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Characteristics of participants’ intervention programs in the included studies.
| Included studies | Country | Total n(n female) | Mean age in months | Severity of ASD | Developmental measures |
|---|---|---|---|---|---|
| Anderson et al. (2004) | New Zealand | 10 (1) | 64.2 | Severe ASD(CARS M = 40.6) | Developmental delay(WISC-III: 28–86) |
| Bauminger-Zviely et al. (2017) | Israel | G1: 21 (1)G2: 30(3) | 59.3854.83 | High functioning ASD | No developmental delay(Mullen's scale: 108) |
| Bauminger-Zviely and Shefer (2021) | Israel | 50 (9) | 54.28 | Moderate(ADOS M = 6.86) | No developmental delay(Mullens scale: 97.17) |
| Boyd et al. (2011) | USA | 8 (2) | 58.88 | Moderate(CARS: M = 30.06) | Not mentioned |
| Chiang and Lin (2008) | Australia and Taiwan | Preschool age group = 14 (not mentioned) | 31–72 | Severe and Moderate(CARS > 37 and CARS <37)) | 5 with developmental delay, 3 without developmental delay, and 6 not evaluated.(ABI scale) |
| Clifford et al. (2010) | UK | 41 (3) | 45.2 | Severe(ADOS: M = 14.8) | Developmental delay(nonverbal Mullen scale: 27.5) |
| Fasano et al. (2021) | USA | 56 (22) | 50.14 | Not mentioned | Not mentioned |
| Gutierrez et al. (2007) | USA | 3 (1) | 56 | Not mentioned | Not mentioned |
| Hume et al. (2019) | USA | 53 (12) | 47.52 | ADOS used;results not mentioned | Developmental delay(Mullen scale = 65.53) |
| Jamero (2019) | Philippines | 9 (1) | 26.6 | Not mentioned | Not mentioned |
```

### ASD-OA-PMC11638897@PMC distributed version 1#section_v2_1#0009
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Lay Summary > SPECIFICITIES OF THE AUTISTIC AUDITORY PROFILE > Neural and psychoacoustic underpinnings · body · text · 273 tokens · trang [None, None]
- completeness: complete

```text
The processing of auditory information in the brain involves multiple regions and networks. Following the transduction of sound energy into electrical signals by sensory cells in the inner ear, synaptic transmission of this information to auditory nerve fibers propagates trains of action potentials unilaterally to cochlear nuclei and bilaterally to the nuclei of the superior olivary complex of the brainstem, before inputs from both sides of the brain converge through the almost obligatory midbrain nucleus of the inferior colliculus and from there to the thalamus and primary and secondary auditory cortices. Subsequent projections to the limbic system allow for emotional regulation and long‐term memory processing associated with sound. Heightened responses to auditory stimuli, reduced filtering of sensory inputs, and differences in temporal processing are some of the most reported neurological findings of auditory processing in autistic people (Chen, Sideris, Watson, Crais & Baranek, 2022; Font‐Alaminos et al., 2020; Gomes et al., 2008; Haesen et al., 2011; Kargas et al., 2015; Kuiper et al., 2019; Lucker, 2013; Park et al., 2017; Williams, 2022).
```

### ASD-OA-PMC12468522@PMC distributed version 1#section_v2_1#0034
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 5. Metabolic Features > 5.6. Dysautonomia in ASD · body · text · 99 tokens · trang [None, None]
- completeness: complete

```text
Dysautonomia, frequently reported in individuals with ASD, is classified here under metabolic dysfunction due to its strong association with mitochondrial inefficiency, oxidative stress, and impaired energy regulation. However, it is important to note that immune-mediated mechanisms (e.g., autoantibodies targeting autonomic receptors, cytokine-driven neuroinflammation) also contribute to autonomic imbalance. Thus, dysautonomia represents a cross-domain phenomenon, linking both metabolic and immune dysfunction pathways [88].
```

### ASD-OA-PMC12468522@PMC distributed version 1#section_v2_1#0108
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 341 tokens · trang [None, None]
- completeness: complete

```text
| AAC | Augmentative and alternative communication |
| ADHD | Attention-deficit/hyperactivity disorder |
| ADI-R | Autism Diagnostic Interview-Revised |
| ADOS | Autism Diagnostic Observation Schedule |
| AFQ | Automated fiber quantification |
| ASD | Autism spectrum disorder |
| CNV | Copy number variants |
| CSF | Cerebrospinal fluid |
| DTI | Diffusion tensor imaging |
| EEG | Electroencephalogram |
| EWASs | Epigenome-wide association studies |
| fMRI | Functional magnetic resonance imaging |
| GI | Gastrointestinal |
| GSH | Glutathione |
| GWASs | Genome-wide association studies |
| ID | Intellectual disability |
| IDO | Indoleamine 2,3 dioxygenase |
| IVIG | Intravenous immunoglobulin |
| MAR | Maternal antibody-related |
| MCP-1 | Monocyte chemoattractant protein-1 |
| MEG | Magnetoencephalography |
| MIA | Maternal immune activation |
| MRI | Magnetic resonance imaging |
| NDBI | Naturalistic behavioral intervention |
| NK | Natural killer cells |
| PECS | Picture exchange communication system |
| PRSs | Polygenic risk scores |
| ROS | Reactive oxygen species |
| RRB | Restrained repetitive behaviors |
| SAH | S-adenosylhomocysteine |
| SAM | S-adenosylmethionine |
| ToM | Theory of Mind |
| Treg | Regulatory T cells |
| TNF | Tumor necrosis factor-α |
| VUSs | Variants of uncertain significance |
```

### ASD-OA-PMC12593641@PMC distributed version 1#section_v2_1#0002
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Data summary · body · text · 53 tokens · trang [None, None]
- completeness: complete

```text
Adolescence represents a vital period of biopsychosocial transformation, particularly challenging for individuals with neurodevelopmental disorders (NDDs), such as autism spectrum disorder (ASD), attention-deficit/hyperactivity disorder (ADHD), and intellectual disability.
```

### ASD-OA-PMC12620806@PMC distributed version 1#section_v2_1#0014
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: AUTISM PRESENTATION ASSOCIATED WITH KNOWN ENVIRONMENTAL EXPOSURES > Neurological conditions · body · text · 504 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4.

```text
Other neurological disorders: Other CCs such as congenital nerve system abnormality, demyelinating diseases, hydrocephalus or brain injury have been studied in relation to autism, with inconsistent and heterogeneous results published.

It is important to add that some neurological complications in autism may be cared for by general pediatricians or neurologists, even prior to diagnosis of autism. The presence of these CCs can significantly impact the individual’s daily functioning and quality of life. As a result, a comprehensive approach to treatment, involving a multidisciplinary team, is often necessary to address both the core symptoms of autism and any neurological CCs. More concrete guidelines might help to clarify the clinical management for autistic individuals with neurological disorders[44]. Future research objectives may focus on the etiology, molecular and genetic mechanisms, and therapeutic approaches for better managing neurological disorders in these children. Special attention should be given to epilepsy, movement disorders and sleep disturbances, as these are the most common conditions affecting their quality of life.

Abnormal brain imaging: Some studies have shown that autistic children often exhibit increased total brain volume, atypical cortical development, and early overgrowth of the amygdala, which may be associated with the social and emotional difficulties characteristic of the disorder[62-65]. It has been reported that there is a relation between increased Gray Matter Volume (GMV) and autism. Cai et al[66] investigated structural differences between autistic individuals with normal or high IQ (> 70) and low IQ (< 70). They found that both groups showed abnormalities in the same brain regions; however, autistic individuals with low IQ exhibited more widespread neuroanatomical differences. For example, increased GMV in the left inferior temporal gyrus was observed in both groups, whereas increased GMV in the left medial temporal gyrus was unique to the low IQ group. Additionally, children with low IQ showed increased GMV in the right medial superior frontal gyrus and exhibited altered connectivity in frontal and temporal regions involved in social cognition[66]. Other studies have shown a relation between autism and altered functional networks in social cognition-related brain regions, leading to a potential neuroimaging biomarker for autism[67]. Brain imaging is not routinely done in the clinical evaluation of autism. Clinicians should indicate brain imaging when autism co-exists with developmental regression, focal neurological signs, epileptic seizures, macrocephaly or microcephaly in order to rule out structural brain abnormalities such as cortical developmental malformations.
```

### ASD-OA-PMC13005892@PMC distributed version 1#section_v2_1#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Results > Inductive trends · results · text · 45 tokens · trang [None, None]
- completeness: complete

```text
The inductive trend analysis revealed three recurrent themes across the studies, seen as being of particular importance in the Vietnamese cultural context: the centrality of family, the importance of school and education, and identifying a cause of autism.
```

### ASD-OA-PMC13005892@PMC distributed version 1#section_v2_1#0030
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: sj-docx-1-aut-10.1177_13623613261425838 – Supplemental material for Autism in Viet Nam: A systematic scoping review · body · table · 583 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Studies Included in Systematic Scoping Review.
| Study | Publication Type | Country in which the study was conducted | Study setting | Study design | Formal autism diagnosis | Thematic area |
| Thảo et al. (2022) | Peer Reviewed Journal | Viet Nam | School | Other: Pre- and post- test | Unclear | Interventions |
| Hà (2019) | Not Peer Reviewed Journal | Viet Nam | School | Other: Case study | Unclear | Services and Supports |
| Đinh et al. (2020) | Peer Reviewed Journal | Viet Nam | Other: Commune health centre | Cross sectional study | Unclear | Services and Supports |
| Thương, Do Thi, and Le Thi (2021) | Peer Reviewed Journal | Viet Nam | School; Other: Specialised centres | Cross sectional study | Unclear | Interventions |
| Kế (2020) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Services and Supports |
| Dung (2023) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Interventions |
| Phương and Phi (2019) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Infrastructure and Surveillance |
| Hằng, Hằng, Hà, and Anh (2019) | Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Biology |
| Dương (2020) | Not Peer Reviewed Journal | Viet Nam | School | Qualitative research | No | Interventions |
| Minh (2023) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Services and Supports |
| Hòa and Kế (2023) | Not Peer Reviewed Journal | Viet Nam | School; Other: Early intervention centres | Cross sectional study | No | Services and Supports |
| Minh (2020) | Not Peer Reviewed Journal | Viet Nam | School | Other: Descriptive study | Unclear | Services and Supports |
| Hài, Bền, and Tuấn (2022) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | Unclear | Interventions |
| Lan (2012a) | Peer Reviewed Journal | Viet Nam | Unclear | Cross sectional study | Unclear | Services and Supports |
| Hứa et al. (2020) | Peer Reviewed Journal | Viet Nam | Hospital | Non-randomised experimental study | No | Interventions |
| Xuân and Ngọc (2024) | Not Peer Reviewed Journal | Viet Nam | School | Cross sectional study | No | Services and Supports |
```

### ASD-OA-PMC13393316@PMC distributed version 1#section_v2_1#0008
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Methods > Study selection · methods · text · 115 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4.

```text
The first, second, and third authors independently conducted the literature search, screened the titles and abstracts of potentially eligible studies, reviewed the full texts, and extracted descriptive data, with each author responsible for a subset of studies. The review process was conducted under non-blind conditions, with any uncertainty about whether to include or exclude a study resolved through discussion and consensus among the reviewers.

For the first research aim, articles were screened based on the eligibility criteria summarized in Table 1. No time restrictions were applied, allowing for the inclusion of all studies published to date on the topic.
```

### ASD-OA-PMC13393316@PMC distributed version 1#section_v2_1#0009
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Methods > Study selection · methods · table · 147 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4.

```text
Table 1
Eligibility criteria for the first research aim.
| Inclusion criteria | Exclusion criteria |
|---|---|
| Studies written in English | Reviews, meta-analyses, dissertations, study protocols, case reports, book chapters, clinical practice guidelines |
| Studies including autistic children and adolescents | Studies solely involving non-autistic children and adolescents or autistic adults (e.g., neurotypical population, individuals with a genetic syndrome) |
| Studies focusing on the use of visual aids during healthcare procedures and involving autistic children and adolescents | Studies not focusing on the use of visual during healthcare procedures and involving autistic children and adolescents (e.g., articles focusing on epidemiologic aspects, conducted in the educational context) |
```

### ASD-OA-PMC13427885@PMC distributed version 1#section_v2_1#0008
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Methods > Data Analysis · methods · table · 486 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Water safety-related focus group questions for parents of autistic children
| What are some ways you have heard about to keep kids safer around water? What information has been particularly helpful or not helpful? |
| Where did the water safety information you heard about come from (e.g. doctor’s office, school, parenting books, therapy offices, media, personal stories or communications, etc.)? |
| In your experience, what are some ways that autism has made water safety efforts more challenging than they might have been? |
| Describe your experience with challenges in the home (such as with bathtubs, toilets), and those outside (pools, ponds, buckets). |
| How does your child’s autism shape choices you make about using safety devices, like life jackets? |
| How have water safety concerns shaped recreational or vacation plans, such as where or how often you take them swimming or where you travel? |
| What personality traits or attributes of your child might affect their water safety risk? |
| Let’s talk about times when you felt your child had or could have had a close call with drowning. Describe the situation and environment. Was there a time where nothing happened, but you realized it could have? |
| Let’s talk about times when your child was enrolled in or attending swim lessons: Describe your experience with your child taking swimming lessons. What made a swimming lesson experience difficult for your child? What helped make your child’s swimming lesson experience easier or successful? |
| If you could have created the perfect swimming lesson experience, what might have helped to make swimming lessons easier or successful for your child? |
| What are the skills you are or were most interested in your child developing during swim lessons? What made it easier or harder for them to develop these skills? |
| Did your water safety and swimming skill expectations for your child change as they got older? |
| Let’s talk about times when you tried to find or enroll your child in swim lessons: Describe your experience looking for swimming lessons for your kid with autism. What made your experience hard? Were there things that helped make your experience easier? |
| Let’s talk about other younger or older children, if you have them. How has having a sibling with autism impacted their water safety or swimming experiences? |
| Is there anything else about your water safety or swimming lesson experience related to autism that you think is important to share? |
```

### ASD-OA-PMC13427885@PMC distributed version 1#section_v2_1#0012
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > Water Safety Themes · results · table · 338 tokens · trang [None, None]
- completeness: complete

```text
Table 2
Water safety themes and subthemes identified from focus groups of parents of autistic children
| Theme 1: Characteristics of autism influence water safety risk |
| Being drawn to water |
| Poor sense of danger |
| Wandering and elopement |
| Impulsivity |
| Opposition |
| Communication difficulties |
| Theme 2: Water safety fears influence family life |
| Emotional toll of vigilance and planning |
| Water avoidance |
| Water access in travel planning |
| Theme 3: Water safety and swimming lesson information for autistic children difficult to find or access |
| Insufficient water safety information |
| Difficulty identifying specialized swimming lessons |
| Limited availability of specialized or adaptive lessons |
| Distance to specialized lessons and higher costs |
| Competing priorities |
| Racial and ethnic disparities |
| Prior negative swimming instruction experiences |
| Theme 4: Characteristics of autism affect participation in swimming lessons and other aquatic activities |
| Preparing for water activities and transitions |
| Sensory overload in pool environments |
| Water can be a negative sensory stimulus |
| Strong responses to water recreation gear |
| Water can have a positive sensory effect |
| Difficulty self-assessing sensations |
| Masking |
| Inflexibility, fixations, and obsessive rule-following |
| Other diagnoses and physical challenges |
| Theme 5: Autistic children have unique swimming lesson needs |
| Communication and learning challenges |
| Developmentally appropriate |
| Learn by observing peers |
| Dedicated learning environment |
| Parent involvement |
| Theme 6: Instructor preparedness is key to swimming lesson success for autistic children |
| Experience teaching individuals with autism |
| Knowledgeable about autism |
| Therapist skills |
```

### ASD-OA-PMC4271434@PMC distributed version 1#section_v2_1#0006
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 586 tokens · trang [None, None]
- completeness: complete

```text
Table 1
ICSD-3 Classification of sleep disorders in children with ASD including descriptions and evidence
| ICSD-3 Classification | Sleep profile | Study | Sleep measures | Significant findings in ASD population |
|---|---|---|---|---|
| Insomnia | Persistent difficulty with sleep initiation, maintenance, duration, consolidation, or quality. Includes bedtime resistance, frequent night awakenings, and/or an inability to sleep independently | Wiggs et al. [24] | Actigraphy and SQ | Increased sleep latency, night awakenings, and poor sleep efficiency |
| Malow et al. [25] | PSG and CSHQ | Poorer sleep efficiency, longer sleep latency, and frequent night awakenings (up to 2–3 h) |
| Goodlin-Jones et al. [26] | Actigraphy and SD | Less total sleep time (TST) compared to TYP children or those with a DD |
| Krakowiak et al. [27] | SQ | Higher sleep-onset factor scores and night awakenings compared to typical children |
| Souders et al. [28] | CSHQ, SD, and actigraphy | Behavioral insomnia evident in 66% of children with ASD compared to 45.9% in controls |
| Anders et al. [29] | Actigraphy and SD | ASD children aged 2–5 years slept less per 24-h period on average compared to controls |
| Giannotti et al. [30] | PSG and CSHQ | Children with regressive ASD (n = 18) had greater bedtime resistance, sleep-onset latency, and less TST than controls |
| Sivertsen et al. [31] | Parent report | Prevalence of chronic insomnia was ten times higher in children with ASD symptoms compared to controls |
| Baker et al. [32] | Actigraphy and SD | Adolescents with ASD were three times more likely to have symptoms of insomnia than their TYP peers |
| Parasomnias | Undesirable physical experiences which occur within sleep or during arousal from sleep. Includes nightmares, wake screaming, complex movements, dreams, and automatic nervous system activity | Hering et al. [33] | Actigraphy and SQ | 54% of children with ASD had multiple and early night arousals |
| Doo et al. [34] | SQ, CSHQ, and actigraphy | All reported evidence of higher rates of parasomnias in children with ASD compared to comparison groups |
| Schreck et al. [35] |
| Liu et al. [20] |
| Goldman et al. [36] | CSHQ | Younger children with ASD had more parasomnias than older children |
```

### ASD-OA-PMC4271434@PMC distributed version 1#section_v2_1#0007
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Tables · floating_table · table · 241 tokens · trang [None, None]
- completeness: complete

```text
Table 1
ICSD-3 Classification of sleep disorders in children with ASD including descriptions and evidence
| ICSD-3 Classification | Sleep profile | Study | Sleep measures | Significant findings in ASD population |
|---|---|---|---|---|
| Circadian rhythm sleep-wake disorders | Alterations of the circadian time-keeping system, its entrainment mechanisms, or misalignment of the endogenous circadian rhythm and the external environment. Manifests in difficulty initiating and maintaining sleep | Giannotti et al. [37] | PSG and CSHQ | More than 10% of children with ASD were found to have sleep problems that varied by season due to fluctuations in light/dark cycles |
| Tordjman et al. [38] | Measures of melatonin | Elevated daytime and lower nocturnal melatonin in individuals with ASD compared with controls |
| Hayashi [39] | SD, CSHQ, and PEQ | “Free-running” sleep (not entrained to 24-h), sleep-onset delay, and early morning awakening in children with ASD |
| Segawa [40] |  |  |
```

### ASD-OA-PMC4742252@PMC distributed version 1#section_v2_1#0007
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 462 tokens · trang [None, None]
- completeness: complete

```text
| Characteristic | ASD-only (% ± SE) | ASD + ID/DD (% ± SE) | ID/DD-only (% ± SE) | p-value | Combined Groups (% ± SE) |
|---|---|---|---|---|---|
| Age 6–11 years | 53.4 ± 4.0 | 55.5 ± 2.8 | 48.2 ± 2.2 | 0.087 | 50.6 ± 1.6 |
| Male | 88.1 ± 2.2 | 79.0 ± 2.4 | 62.8 ± 2.1 | <0.001* | 69.8 ± 1.5 |
| Non-Hispanic | 86.3 ± 3.7 | 86.8 ± 2.1 | 86.3 ± 1.8 | 0.987 | 86.5 ± 1.3 |
| White | 82.4 ± 3.2 | 68.7 ± 2.8 | 67.3 ± 2.3 | 0.003* | 69.4 ± 1.7 |
| Non-Hispanic white | 71.3 ± 4.2 | 62.7 ± 2.8 | 59.4 ± 2.3 | 0.047* | 61.6 ± 1.7 |
| Household income (≤100% FPL) | 10.1 ± 2.8 | 20.4 ± 2.6 | 32.0 ± 2.3 | <0.001* | 26.5 ± 1.6 |
| Household education: HS or less | 13.8 ± 3.0 | 27.9 ± 2.9 | 37.4 ± 2.3 | <0.001* | 32.3 ± 1.7 |
```

### ASD-OA-PMC4742252@PMC distributed version 1#section_v2_1#0010
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Tables · floating_table · table · 328 tokens · trang [None, None]
- completeness: complete

```text
| Location | ASD-only (% ± SE) | ASD + ID/DD (% ± SE) | ID/DD-only (% ± SE) | Entire Cohort (% ± SE) |
|---|---|---|---|---|
| Any location | 32.7 ± 4.1 | 34.6 ± 2. 8 | 22. 7 ± 2.1 | 26.7 ± 1.6 |
| Own home | 8.3 ± 2.3 | 11.7 ± 1.9 | 9.6 ± 1.9 | 9.9 ± 1.3 |
| Another home | 4.8 ± 1.7 | 6.3 ± 1.4 | 4.3 ± 1.0 | 4.8 ± 0.7 |
| Any home | 11.7 ± 2.7 | 14.2 ± 2.0 | 11.1 ± 1.9 | 11.9 ± 1.4 |
| Structured program | 10.2 ± 2.4 | 10.3 ± 1.9 | 4.1 ± 0.7 | 6.3 ± 0.7 |
| Public place | 22.5 ± 3.7 | 25.1 ± 2.7 | 15.5 ± 1.6 | 18.6 ± 1.3 |
```

### ASD-OA-PMC6487529@PMC distributed version 1#section_v2_1#0012
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Methods > Screening and diagnosis > Screening phase · methods · text · 229 tokens · trang [None, None]
- completeness: complete

```text
We used the 23 item Modified Checklist for Autism in Toddlers (M-CHAT) to screen children with high risk of ASD. M-CHAT is a screening tool for ASD which has been being used worldwide [22]. In Vietnam, M-CHAT was shown to have sensitivity of 74.4% and specificity of 99.9% in screening ASD [13]. During the research design phase, we reviewed and considered different autism screening tools, including M-CHAT and M-CHAT-R/F. After the careful consideration, we chose M-CHAT as the screening tool in our study for a number of reasons. M-CHAT had been translated and validated in the Vietnamese context [13]. M-CHAT was also used in some other previous studies in Vietnam. This tool has been also commonly used to screen autism among children in clinical settings in a number of hospitals in Vietnam. Moreover, owing to financial limitations, M-CHAT was more much appropriate for our study than M-CHAT-R/F that required follow-up after screening. The screenings were conducted at the children’s homes with the children’s parents.
```

### ASD-OA-PMC6487529@PMC distributed version 1#section_v2_1#0018
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Results · results · table · 590 tokens · trang [None, None]
- completeness: complete

```text
Table 1
General characteristics of the study participants
|  | Frequency | Percentage (%) |
|---|---|---|
| City/province |
| Ha Noi | 5501 | 31.8 |
| Thai Binh | 5883 | 34.1 |
| Hoa Binh | 5893 | 34.1 |
| Area |
| Rural | 12,754 | 73.8 |
| Urban | 4523 | 26.2 |
| Gender |
| Girl | 8009 | 46.4 |
| Boy | 9268 | 53.6 |
| Age (months) |
| 18–23 | 7128 | 41.3 |
| 24–30 | 10,149 | 58.7 |
| Mother age |
| Less than 29 | 11,649 | 67.4 |
| 29 to 39 | 4061 | 23.5 |
| 40 and older | 1567 | 9.1 |
| Mother’s education |
| Primary education | 4908 | 28.4 |
| Secondary education | 5847 | 33.8 |
| High school | 3419 | 19.8 |
| University/College | 3103 | 18.0 |
| Mother’s occupation |
| Government staff | 2816 | 16.3 |
| Private sector staff | 3787 | 21.92 |
| Farmer | 4378 | 25.34 |
| Unstable job | 5537 | 32.05 |
| Others | 759 | 4.39 |
| Father’s age |
| Less than 29 | 8647 | 50.1 |
| 29 to 39 | 7933 | 45.9 |
| 40 and older | 697 | 4.0 |
| Father’s education |
| Primary education | 5123 | 29.7 |
| Secondary education | 6345 | 36.7 |
| High school | 2756 | 16.0 |
| University/College | 3053 | 17.7 |
| Father’s occupation |
| Government staff | 2421 | 14.0 |
| Private sector staff | 3037 | 17.6 |
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v2_1#0015
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 4. Oral Over-the-Counter Medicines · body · text · 431 tokens · trang [None, None]
- completeness: complete

```text
Sleep pills should be considered to be an additional treatment option to improve sleep in children when non-pharmacological interventions are unsuccessful [17]. However, in children with ASD pharmacological treatment is sometimes convenient as a first-line strategy together with non-pharmacological approaches, given the greater severity of sleep disturbances in these patients [25]. Both prescription hypnotic drugs and OTC sleep-promoting agents might be useful in clinical practice. Due to the scarcity of controlled studies, there is no sleep medication approved by the FDA and only one—prolonged-release melatonin for the treatment of insomnia—approved by the EMA for children and adolescents with ASD. Sleep-promoting agents are therefore widely prescribed off-label, the most commonly used off-label medications being sedating antihistamines (e.g., diphenhydramine or hydroxyzine), melatonin, α2-receptor agonists (e.g., clonidine), benzodiazepines, pyrimidine derivatives (e.g., zaleplon and zolpidem), antipsychotics (e.g., risperidone and quetiapine), and sedating antidepressants (e.g., trazodone and mirtazapine) [68].

Some of the above-mentioned agents—i.e., antihistamines and melatonin—are available over the counter in many countries all over the world. Non-prescription medications—including OTC drugs, nutritional supplements, and herbal remedies—are indeed widespread therapies for sleep disturbances in children, as they are generally easily accessible and well accepted by caregivers. Furthermore, oral non-prescription treatments are often considered to be a “safe choice” by clinicians, as they usually have less significant side effects in comparison to some prescription hypnotic drugs—such as antipsychotics and antidepressants [12,69].

Here we describe the oral non-prescription treatments and nutritional supplements most commonly used for sleep problems in children with ASD: melatonin, antihistamines, tryptophan, carnosine, vitamin D, iron, other multivitamin and mineral supplements, and herbal remedies.
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v2_1#0088
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 80 tokens · trang [None, None]
- completeness: complete

```text
brainsci-10-00441-t001_Table 1Table 1
Stepwise approach to sleep disturbances in children. Adapted from Howlett et al. (2020) [10].
| Level 1 | Sleep education and implementation of healthy sleep practices |
| Level 2 | Specific behavioral strategies |
| Level 3 | Medications |
```

### ASD-OA-PMC9003052@PMC distributed version 1#section_v2_1#0014
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 3. Results > 3.3. GIS and ASD Severity · body · text · 514 tokens · trang [None, None]
- completeness: complete

```text
In this small trial with no placebo group, assessors were unblinded, and participants were receiving behavioral therapy. Children with ASD were gender/age-matched with healthy controls who were relatives. Three probiotic strains of Lactobacillus acidophilus were administered for 12 weeks.

After the treatment period, there were significant improvements in GIS with reductions in constipation (42.5%), diarrhea (37.5%), abdominal pain (60%), flatulence (57%), and improved stool consistency (16.6%). There were also significant improvements in ASD severity concerning speech and language communication, sociability, sensory cognitive awareness, health physical behavior.

Long-term improvements on GIS and ASD symptoms have also been found following interventions designed to normalize gut microbiota using microbiota transfer therapy (MTT). Kang et al. [37] investigated the safety and tolerability of MTT and its effects on microbiota, GIS, and other ASD-related symptoms. The study involved participants with ASD (n = 18) aged 7 to 17 years. Treatment involved a two-week antibiotic, a bowel cleanse, and then an extended fecal microbiota transplant (FMT). The results indicated an 80% reduction of GIS at the end of treatment, with improvements in symptoms of constipation, diarrhea, indigestion, and abdominal pain. These improvements persisted for eight weeks after treatment. Clinical assessments demonstrated that the behavioral symptoms of ASD improved significantly and that these remained improved at eight weeks follow-up. Kang et al. [38] report that these improvements were maintained two years after the treatment phase was completed. Grimaldi et al. [34] conducted a small double-blind placebo RCT that examined multiple interventions. Participants were randomly assigned for six weeks to a prebiotic and exclusion diet (n = 12) or a placebo and exclusion diet, or a prebiotic and unrestricted diet (n = 18). Those taking the prebiotic and exclusion diet had significantly lower abdominal pain (p < 0.05), bowel movements (p < 0.001), a significant increase of Lachnospiraceae family, significant changes in fecal and urine metabolites, and reduced antisocial behavior. Furthermore, the exclusion diet and prebiotic group had a higher abundance of B. Longum. Grimaldi et al. suggested that a synergistic effect on behavior resulted from the combination of prebiotic and casein/gluten-free exclusion diet.
```

### ASD-OA-PMC9003052@PMC distributed version 1#section_v2_1#0054
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Tables · floating_table · table · 504 tokens · trang [None, None]
- completeness: complete

```text
nutrients-14-01471-t001_Table 1Table 1
Summary of study details.
| Study ID | Study Design | Aim(s) | Sample–Size andAge | Measure of GI Symptoms | Results | QuADSResult |
|---|---|---|---|---|---|---|
| Babinska et al. [24] | Case-control study | Investigated the prevalence and types of GIS, frequency of food selectivity, mealtime difficulties. | n = 247 (ASD)n = 267 (TD)2–18 years | GI severity index questionnaire [25]. | Higher prevalence GIS in autistic girls than boys. High rates food selectivity 69.1% and mealtime difficulties 64.3%. Weak but significant correlation of behavior characteristics with GIS frequency, | 21 |
| Bresnahan et al. [26] | Cohort Study | Investigated GIS frequency in children registered in Norwegian Mother & Child study, and when these present during first 3 years of life. | n = 195 (ASD)n = 4636 (DD)n = 4095 (TD)6–36 months | Study Maternal report questionnaires. | Mothers of children with ASD were significantly more likely to report constipation, food allergy/intolerance in the 6–18 month and diarrhea, constipation and food allergy/intolerance in the 18–36 month periods. | 29 |
| Chaidez, et al. [8] | Population-based case-control study | Compared GI problems in children registered in the CHARGE study examining the relationship between GIS and maladaptive behaviors. | n = 499 (ASD)n = 137 (DD)n = 324 (TD)24–60 months | CHARGE GI questionnaire | Children with more severe ASD had 10% more frequent diarrhea than those with less severe ASD. ASD children more likely to have at least on frequent GIS than TD. Maladaptive behaviors correlate with GIS. | 21 |
Abbreviations: ASD = autism spectrum disorder, BCP = bovine colostrum product, DD = developmental disability, GI = gastrointestinal, GIS = gastrointestinal symptoms, ID = intellectual disability, IQ = intelligent quotient, RCT = randomized control trial, TD = typically developing.
```

### ASD-SUP-PMC10783429@PMC10783429.1; acquired 2026-10-30#section_v2_1#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Abstract > Method > Coding procedures > Intervention characteristics · methods · text · 289 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: bibliographic_version×1, graphic×5, media×1, supplementary-material×1.

```text
Intervention targets tend to center on early social communication skills that are thought to serve as a foundation for further developmental cascades. Examples include the early start Denver model, JASPER, and pivotal response teaching.

Sensory integration therapy—Interventions were described as sensory integration therapy if they were explicitly described as such or were characterized by structured exposure to several types of sensory opportunities (ie, tactile, vestibular, proprioceptive).17 18 This category included Ayres sensory integration and more general sensory integration therapy.

Sensory based interventions—Interventions were categorized as sensory based interventions if they incorporated targeted exposure to sensory stimuli with the goal of enhancing processing of sensory stimuli and theoretically related outcomes, but did not include several types of sensory opportunities. Examples include auditory integration, touch therapy, and massage.

TEACCH—Interventions were categorized as TEACCH if they were explicitly named as such. TEACCH is characterized by heavy reliance on predictable environments, structured work systems, and routines (eg, visual and picture activity schedules).

Technology based interventions —Interventions were categorized as technology based if technological mediation was described as the main change agent of the intervention. Technologies included electronic devices such as computers, iPads, or robots.

Other—Interventions that could not be adequately categorized in the previous categories were coded as other for type. These studies were excluded from summary effect estimation, but included in moderator analyses.
```

### ASD-SUP-PMC10783429@PMC10783429.1; acquired 2026-10-30#section_v2_1#0028
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Abstract > Results > Summary effects · abstract · table · 535 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: bibliographic_version×1, graphic×5, media×1, supplementary-material×1.

```text
Table 1
Estimates of variance and summary effects by intervention and outcome type with increasingly restrictive quality thresholds
| Intervention or outcome | All RCTS |  | RCTS without caregiver report |  | RCTs with low detection bias |
| 𝛕 | g (95% CI) | P |  | 𝛕 | g (95% CI) | P |  | 𝛕 | g (95% CI) | P |
|---|---|---|---|---|---|---|---|---|---|---|
| Behavioral |  |  |  |  |  |  |  |  |  |  |  |
| Social communication | 0.873 | 0.54 (–0.24 to 1.32) | 0.15 |  | — | — | — |  | — | — | — |
| Social emotional or challenging behavior | 0.334 | 0.58 (0.11 to 1.06) | 0.02 |  | — | — | — |  | — | — | — |
| Developmental |  |  |  |  |  |  |  |  |  |  |  |
| Social communication | 0.028 | 0.28 (0.12 to 0.44) | 0.003 |  | 0.037 | 0.31 (0.13 to 0.49) | 0.003 |  | — | — | — |
| NDBI |  |  |  |  |  |  |  |  |  |  |  |
| Adaptive | 0.011 | 0.23 (0.02 to 0.43) | 0.03 |  | — | — | —. |  | — | — | — |
| Cognitive | 0.028 | 0.18 (–0.02 to 0.38) | 0.07 |  | 0.029 | 0.19 (–0.02 to 0.39) | 0.07 |  | 0.000 | 0.17 (–0.02 to 0.37) | 0.07 |
```

### ASD-SUP-PMC10981608@PMC10981608.1; acquired 2026-10-30#section_v2_1#0008
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Method > Eligibility Criteria · methods · table · 348 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×7.

```text
Table 1
Inclusion and exclusion criteria and search strategy
| Eligibility criteria and search strategy |
|---|
| Inclusion criteria |
| Program | Social Skills Group programs (SSGP) targeting the socialisation success of autistic adolescents within a neurotypical context |
| Participant | Autistic adolescents diagnosed with ASD under DSM-5 or its previously recognised terms under DSM-IV (Autism, Autistic disorder, Asperger’s Syndrome, Pervasive developmental disorder-not otherwise specified). Although the preferred age range was 12 to 17 years, programs employing samples with a broader or narrower age range were also tolerated |
| Design | A randomised controlled trial focusing on adolescent outcomes |
| Documents | Scholarly articles |
| Exclusion criteria | School-based programs; Studies not targeting the social communication and interaction skills of autistic adolescents as one of the primary objectives or focussing on parent or family outcomes |
| Where | Title, abstract, and keywords |
| Search strategy | 1. ‘Social’ 2. ‘Program’ OR ‘treatment’ OR ‘training’ OR ‘therapy’ 3. ‘Teen*’ OR ‘adolescen*’ OR ‘youth’ OR ‘Juvenile’ 4. ‘Randomised controlled trial’ OR ‘RCT’ OR ‘Randomised’ 5. ‘Pervasive developmental disorder’ OR ‘autis*’ OR ‘Asperger’ OR ‘ASD’ OR ‘PDD’ 6. 1 AND 2 AND 3 AND 4 AND 5 7. Limit to 2008 to 2018/update: limit to 2018 to 2020 |
```

### ASD-SUP-PMC10981608@PMC10981608.1; acquired 2026-10-30#section_v2_1#0026
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Results > Program Fidelity Analysis · results · text · 266 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×7.

```text
All 18 studies but one (Rabin et al., 2018) reported assessing PF, with studies employing various methods, including assessing video recordings of randomly chosen sessions using a fidelity checklist (Afsharnejad et al., 2021a, 2021b; Choque Olsson et al., 2017; Jonsson et al., 2018; White et al., 2013), observing a session assessing fidelity either in reference to the program manual (Shum et al., 2019; Yoo et al., 2014) or via a checklist. The included studies demonstrated overall PF scores ranging from 0.33 to 0.90 (M = 0.52, SD = 0.15), with 17% (k = 3) demonstrating a strong overall fidelity (Afsharnejad et al., 2021a, 2021b; Choque Olsson et al., 2017; Jonsson et al., 2018). An overview of the PF scores is available via https://osf.io/n93pu/.
```

### ASD-SUP-PMC11754701@PMC11754701.1; acquired 2026-10-30#section_v2_1#0021
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Key Practitioner Message > Results · results · table · 599 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Summary of the treatment effects of all primary and secondary outcomes
| Outcome | Timing | Estimated difference (Intervention – Control) in expected value (95% CI a ) | p‐Value a |
|---|---|---|---|
| Primary outcome |
| SRS‐2 | Week 6 | −1.14 (−3.35 to 1.06) | .310 |
| Month 6 (primary) | −1.61 (−4.18 to 0.96) | .220 |
| Secondary outcomes |
| SRS‐2 total raw score (teacher) | Week 6 | −3.37 (−9.41 to 2.67) | .274 |
| Month 6 | −3.32 (−10.28 to 3.63) | .349 |
| Goal‐based outcome (teacher) | Week 6 | 0.84 (0.14 to 1.54) | .018 |
| Month 6 | 0.97 (0.21 to 1.73) | .012 |
| SRS‐2 total T‐score (parent) | Week 6 | 0.43 (−0.83 to 1.70) | .504 |
| Month 6 | 0.35 (−1.26 to 1.97) | .668 |
| SRS‐2 total raw (parent) | Week 6 | 2.37 (−1.41 to 6.16) | .219 |
| Month 6 | 1.21 (−3.65 to 6.08) | .625 |
| RCADS total score (parent) | Week 6 | 1.10 (−1.81 to 4.02) | .458 |
| Month 6 | 2.35 (−1.37 to 6.06) | .215 |
| PSI total stress score | Week 6 | −1.42 (−4.92 to 2.09) | .428 |
| Month 6 | −1.49 (−5.43 to 2.46) | .460 |
| EQ‐5D‐Y VAS (parent) | Week 6 | −0.63 (−4.93 to 3.66) | .772 |
| Month 6 | −1.92 (−6.70 to 2.86) | .432 |
```

### ASD-SUP-PMC11754701@PMC11754701.1; acquired 2026-10-30#section_v2_1#0023
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Key Practitioner Message > Results · results · table · 187 tokens · trang [None, None]
- completeness: complete

```text
Table 2
SRS‐2 CACE estimates at 6 weeks and 6 months post‐randomisation from the planned analysis models
|  | Control (N = 120) | Intervention (N = 129) | CACE estimate (95% CI) | p‐Value |
|---|---|---|---|---|
| Week 6 | 110 (91.7%) | 79 (61.2%) | −2.35 (−5.44 to 0.73) | .134 |
| Month 6 | 108 (90.0%) | 76 (58.9%) | −3.37 (−6.65 to −0.10) | .043 |
```

### ASD-SUP-PMC12658592@PMC12658592.1; acquired 2026-10-30#section_v2_1#0009
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Methods > Information sources and search strategy · methods · table · 441 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Search terms.
| Question | Search terms |
|---|---|
| Population/Problem | Sensation disorders, somatosensory disorders, sensory integration disorders, sensory processing disorders, sensation disorders, somatosensory disorders, clumsy child syndrome, developmental coordination disorder, developmental dyspraxia, disorder of attention, motor, and perception, fine motor deficits, gross motor deficits, learning disabilities, nonverbal learning disorder, perceptual motor deficits, regulatory disorder, sensory integrative dysfunction, sensory modulation disorder, sensory modulation dysfunction, sensory motor deficit |
| Intervention | Activities of daily living, activity, activity groups, adaptive behavior, adaptive equipment, assistive technology, Astronaut training, attention, auditory integration training, augmentative communication, ball chairs, bilateral coordination, bilateral intervention, coaching, cognitive-behavioral therapy, cognitive intervention, consultation, context, contextual, CO-OP, decision-making skills training, early intervening, early intervention, emotional regulation, employment, environment, environmental modification, executive function, exercise, family centered care, family coping, coping skills, family interaction/participation, friendship, friendship group, functional approaches, handwriting, instrumental activities of daily living, integrated listening systems, job coaching, job training, Kawar protocol, leisure, life coaching, massage, motor planning, multisensory integration, natural environment intervention, neurodevelopmental treatment, neuromotor occupational therapy, occupational therapy, occupation-based, ocular motor skills, oral sensorimotor programs, parent/teacher mediated, parent training, peer group, peer interaction, peer mediated, perceptual motor learning, play, praxis, pressure vest, prevocational, priming, problem-solving skills training, relationship-based intervention, rest, routines-based interventions, self-care, self-management, sensory diet, sensorimotor integration, sensory integration, sensory integrative, SI, sleep, social competence, social participation, social skills training, social stories, strengths-based, supported education, supported employment, tactile stimulation, therapeutic listening, time management, touch pressure, transitioning, transitions, vestibular stimulation, weighted blankets, weighted items, weighted materials, weighted vests, Wilbarger protocol, work, yoga |
```

### ASD-SUP-PMC12658592@PMC12658592.1; acquired 2026-10-30#section_v2_1#0016
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Methods > Analysis · methods · table · 269 tokens · trang [None, None]
- completeness: complete

```text
Table 2
Strength of evidence.
| Level | Description |
|---|---|
| Strong | - Two or more Level I studies - The available evidence includes consistent results from well-designed, well-conducted studies. The findings are strong and unlikely to be called into question in future studies |
| Moderate | - At least one Level I study or multiple high-quality Level II - The available evidence is sufficient to determine the effects on health outcomes, but confidence in the estimate is constrained by factors such as: - - The number, size, and quality of individual studies - - Inconsistency of findings across the individual studies - As more information (other research findings) becomes available, the magnitude or direction of the observed effect could change, and this change may be large enough to alter the conclusion related to the usefulness of the intervention |
| Low | - Small number of low-level studies, flaws in the studies, and so on - The available evidence is insufficient to assess effects on health and other outcomes of relevance to occupational therapy. Evidence is insufficient because of - - a limited number or size of studies, - - important flaws in study design or methods, - - inconsistency of findings across individual studies, and - - lack of information on important health outcomes. - More information may allow estimation of effects on health and other outcomes of relevance to occupational therapy |
```

### ASD-SUP-PMC13414371@PMC13414371.1; acquired 2026-10-30#section_v2_1#0012
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 3. Results > 3.3. Outcome Measures and Targeted Results · body · text · 568 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×3, media×1, supplementary-material×1.

```text
The included studies used a wide range of instruments to assess communication and language outcomes, indicating substantial methodological heterogeneity. Both standardized and observational tools were employed. The most frequent measures were the MacArthur CDI (n.4; 22.2%), MSEL (n.3; 16.6%), and VABS (n.3; 16.6%). Other instruments included PPVT, Reynell Developmental Language Scales (RDLS), Preschool Language Scale, and Expressive One-Word Picture Vocabulary Test (each n.2; 11.1%) [39,40,41]. Observational approaches were also common, including NLS video coding, Structured Play Assessment, and Early Social Communication Scales (each n.4; 22.2%), as well as parent/peer/teacher–child interaction measures (n.9; 50%) and intervention-session coding (n.2; 11.1%). Sixteen studies assessed expressive and receptive language, primarily via standardized or structured tools (10/16; 62.5%), followed by video-based coding (5/16; 31.2%), parent questionnaires (4/16; 25%), and semi-structured interviews (3/16; 18.7%). Expressive language refers to conveying meaning through speech, gestures, or signs, whereas receptive language involves understanding communication through auditory and visual input [42].

Spontaneous communication refers to unprompted communicative acts [43] and was examined in 11 studies (61.1%), mainly using video recordings (11/18), sometimes supported by questionnaires or structured tools (each 2/11; 18.2%). Social communication reflects context-appropriate verbal and nonverbal interaction [44] and was investigated in 10 studies (55.5%), using structured observations (5/10; 50%), interviews (3/10; 30%), questionnaires (2/10; 20%), video recordings (2/10; 20%), and one standardized test (10%). Play skills were assessed in 6 studies, mostly via video coding (5/6), with 1 study combining standardized and parent-report measures (1/6; 16.6%). Play skills involve functional and symbolic object use, peer interaction, and support cognitive, social, and language development [45].

Two studies also examined speech sound accuracy (video-based) [46] and phonological/phonemic awareness (non-standardized parent questionnaire) [47]. A detailed overview of outcome measures is provided in Table 1.
```

### ASD-SUP-PMC13414371@PMC13414371.1; acquired 2026-10-30#section_v2_1#0023
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: 3. Results > 3.11. Summary of Main Findings · body · table · 568 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×3, media×1, supplementary-material×1.

```text
medsci-14-00388-t001_Table 1Table 1
Outcome assessment and main results.
| ID | Author | Measurement Instrument | Outcome Domain | Assessment Type | Main Results |
|---|---|---|---|---|---|
| 1 | Abdi S. et al., 2023 [62] | CDI-1 | Expressive and receptive | Parent-reported measure | Significant improvements in expressive vocabulary and receptive language, maintained at follow-up. |
| 2 | Almirall D. et al., 2016 [48] | NLS-videocoding | Spontaneous Communicative B. | Observational measure | JASP+EMT+SGDs significantly increased spontaneous communicative utterances; no between-group differences in novel word acquisition. |
| Structured Play Assessment | Play skills | Observational measure | No significant between-group differences in play; no significant change over time. |
| Early Social Communication Scales | Social communication skills | Structured observational measure | SGDs improved joint attention; behavioral regulation improved similarly across all groups and was maintained over time. |
| 3 | Barrett, AC et al., 2020 [53] | Parent–child interaction | Spontaneous Communicative B.; Expressive and receptive | Observational measure | Intervention improved social responsiveness and utterance length. Baseline social responsiveness predicted later language outcomes. |
| 4 | Bauminger-Zviely, N. et al., 2020 [63] | Peers–child interaction | Spontaneous Communicative B., Play Skills | Observational measure | Collaboration group showed greater active participation and reduced passivity; no group differences in play skills. |
| Social Conversation Scale | Spontaneous Communicative B. | Observational measure | Both groups improved conversation quality; collaboration group showed greater gains in gestures, eye contact, and peer relevance. |
| VABS | Expressive and receptive; Social communication skills | Semi-structured interview | No significant improvement in communication. Socialization improved mainly in the conversation group. |
| 5 | Chang YC et al., 2018 [49] | PPVT-4 | Expressive and receptive | standardized measure | Play skills were positively associated with expressive language. |
| Structured Play Assessment | Play skills | Observational measure | Both groups improved play skills over six months. |
| 6 | Chenausky, K.V. et al., 2022 [46] | % Syllables Approximately Correct, % Consonants Correct, % Vowels Correct | Speech sound accuracy | Observational measure | AMMT produced greater improvements in speech sound accuracy than SRT. |
```

### ASD-SUP-PMC4513196@PMC4513196.1; acquired 2026-10-30#section_v2_1#0038
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Conclusion · conclusion · text · 541 tokens · trang [None, None]
- completeness: complete

```text
The field of autism early intervention has changed dramatically in the last 30 years. Since the development of the first empirically-validated and highly-structured ABA interventions that changed the lives of children with autism, continued research has expanded these efforts by moving towards more naturalistic interventions that integrate principles identified by developmental science with ABA principles. Whereas behavioral and developmental research and treatment in ASD initially proceeded separately, the increasing emphasis and evidence on autism intervention during the early childhood period have brought these fields together. These NDBIs represent the integration of ABA and developmental science and they not only allow us to achieve more substantial and accelerated child learning and behavior change, but they are particularly well suited to the infant and toddler autism population now being served.

The various NDBIs share essential features, including implementing intervention in the context of naturally-occurring social activities within natural environments. All are more child-directed than previous ABA approaches, involve intrinsic rewards for learning and participating, allow for sampling a wide range of antecedent stimuli and acceptable responses during the teaching interaction, and use strategies to promote spontaneity, initiative, and generalization, including incorporation of family members in the interventions. They focus on developmentally based learning targets and important foundational social learning skills like joint attention and imitation known to facilitate acquisition of language and other higher-level skills.

Because NDBIs enjoy a strong research base that substantiates their efficacy for improving meaningful outcomes in young children with ASD, it is critical to disseminate this message and share this record of results with the research communities and the public sector. The public sector definition of “applied behavior analysis” is oftentimes wrongly equated with a specific method of ABA, DTT, rather than being understood as an umbrella of empirically based practices that are built on operant learning procedures. The remarkable work of many researchers, working in parallel in different locations and publishing independent and converging results on a wide range of NBDI approaches, have created a new generation of early intervention models whose common features and efficacy may not yet be widely known to parents, clinicians, physicians, and to funding agencies.

Confusion about the actual definition of ABA, and its incorrect interpretation as massed or discrete trial teaching may lead referrers and funders, including health insurance companies, to mistakenly restrict coverage for autism treatment to only one type of ABA, DTT, thus denying the full range of effective intervention approaches based on ABA to consumers. The NDBIs described in this paper are efficacious treatments based firmly in ABA and supported by a large body of evidence. It can be solidly argued that funding that provides coverage of ABA treatment should cover NDBIs.
```

### ASD-SUP-PMC6590432@PMC6590432.1; acquired 2026-10-30#section_v2_1#0012
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Abstract > Methods > Stage One: Search Process · methods · table · 157 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Databases Searched and Records Identified
| Database | Records identified | Number of records after de‐duplication |
|---|---|---|
| CINAHL | 1058 | 641 |
| Cochrane Reviews | 5 | 3 |
| Cochrane Trials | 342 | 131 |
| Embase | 2057 | 1530 |
| ERIC | 310 | 152 |
| Medline | 1096 | 1029 |
| PsycINFO | 1969 | 1444 |
| Total | 6837 | 4930 |
```

### ASD-SUP-PMC6590432@PMC6590432.1; acquired 2026-10-30#section_v2_1#0013
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Abstract > Methods > Stage One: Search Process · methods · table · 296 tokens · trang [None, None]
- completeness: complete

```text
Table 2
Studies Excluded from CEC Analysis
| Article | Reason(s) for exclusion | Comments |
|---|---|---|
| Sankar [2015] | Not ASI | Ambiguity regarding intervention employed. Authors described intervention as “sensory integration” and provide examples of several activities consistent with this approach, however, there is insufficient evidence that ASI principles were followed. No fidelity, no training of interventionists, no statistics reported |
| Dunbar, Carr‐Hertel, Lieberman, Perez, and Ricks [2012] | Study Type; Descriptive | Ambiguity regarding methodology employed. Descriptive study with no statistical analyses employed |
| Piravej, Tangtrongchitr, Chandarasiri, Paothong, and Sukprasong [2009] | SI included In both groups | Authors described intervention as “sensory integration therapy,” however, because both groups received SI (e.g. SI vs Massage & SI) effects of SI alone could not be judged |
Note. Exclusion Criteria. IQ = Participants IQ not below 65. Diagnosis = Participants did not have Autism Spectrum Disorder. Study Type = Study was not a group comparison or appropriate single‐subject design examining effectiveness of ASI. Not ASI = Intervention did not meet criteria for Ayres Sensory Integration© intervention. ASI = Ayres Sensory Integration© intervention.
```

### ASD-SUP-PMC7726187@PMC7726187.1; acquired 2026-10-30#section_v2_1#0008
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Theory of Change for Sensory Integration/Sensory Processing Treatment · body · text · 490 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×8.

```text
Hundreds of publications have described SI/SP-T since 1964, though the literature continues to contain relatively few large-scale randomized trials directly testing the intervention (Ayres, 1972; Kimball, 1993; Kinnealey and Miller, 1993; Parham, 1998; Miller et al., 2001, 2007b; Bundy et al., 2002; Pfeiffer et al., 2011, 2018; Schaaf et al., 2014, 2018). Most of the literature on this topic includes inconsistent terminology between studies as well as limited high-quality evidence, and design limitations (see Miller et al., 2007c; Schaaf et al., 2018). Additionally, because authors often utilize terminology, theoretical constructs, and observational frameworks that are inconsistent (see Schaaf and Davies, 2010), it can be difficult to aggregate studies and to specify consistent outcome measures. Thus, although some studies provide credible evidence of treatment effects, SI/SP-T does not yet have a strong evidence-base. For example, Schoen et al. (2019) conducted a systematic review of Ayres Sensory Integration (ASI) treatment and found only two studies that met a majority of quality indicators and one additional study that met a “plurality” of quality metrics. In contrast, reviews of NBDIs include dozens or even hundreds of studies (e.g., Sandbank et al., 2020). For purposes of this review, we are using the SI/SP-T nosology by Miller et al. (2007a), and we have adapted the conceptual theory of change from Miller et al. (2001) as an example of a testable SI/SP-T framework (see Table 1). To be sure Ayres Sensory Integration (e.g., the review of ASI in Watling and Hauer, 2015; Schoen et al., 2019) or any other well-defined approach within the broad rubric of SI/SP-T could also be tested, we utilize the framework of Miller et al. (2001) herein as an example of how this can be accomplished.
```

### ASD-SUP-PMC7726187@PMC7726187.1; acquired 2026-10-30#section_v2_1#0009
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Theory of Change for Sensory Integration/Sensory Processing Treatment · body · table · 276 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×8.

```text
Table 1
Hypothesized social and behavioral effects of sensory disruptions.
| Dimensions | Behaviors observed |
|---|---|
| Sensory symptoms Results in [Original asset: fnint-14-556660-i0001.jpg; see source article] Original asset file | Difficulty regulating sensory input: over or under responsivity (Tactile, Movement, Taste, Smell, Auditory, or Visual stimuli); difficulty interpreting internal sensations (body awareness, interoception), and difficulty discriminating external sensations (from the environment). |
| Motor symptoms Results in [Original asset: fnint-14-556660-i0001.jpg; see source article] Original asset file | Poor coordination, Clumsiness, Awkwardness, Poor posture, Limited planning and sequencing of motor skills; Inability to perform multistep tasks. |
| Behavioral symptoms Results in [Original asset: fnint-14-556660-i0001.jpg; see source article] Original asset file | Aggression, Anger, Dysregulation, Tearfulness, Withdrawal. Anxiety, Poor attention, Hyperactivity, Poor impulse control. |
| Social symptoms | Social isolation, Withdrawal, Poor social relationships with peers and adults, Discomfort in social situations. |
```

### ASD-SUP-PMC9399988@PMC9399988.2; acquired 2026-10-30#section_v2_1#0008
- lý do chọn: first retrievable table · retrieval_eligible: True
- section: Keywords > Methods > Recruitment and participants · methods · table · 568 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×3, media×1, supplementary-material×1.

```text
Table 1
Characteristics of participants at baseline (T1)
| Variables | Treatment Group (n = 12) | Waitlist Control Group (n = 17) |
| M (SD) | M (SD) | p |
|---|---|---|
| Age (years) | 14.6 (1.0) | 14.3 (1.2) | ns |
| Gender (% male) | 66.7 | 58.8 | ns |
| ASD diagnosis (%) |  |  | ns |
| Asperger Syndome | 75.0 | 94.1 |  |
| Childhood autism | 25.0 | 5.9 |  |
| Comorbid psychiatric disorders (%) | 33.3 | 35.3 | ns |
| On medication (%) | 41.7 | 23.5 | ns |
| Parental age (years) | 46.8 (5.7) | 47.3 (4.4) | ns |
| Parental education (% tertiary) | 100.0 | 70.6 | ns |
| Baseline Measures |  |  |  |
| ADOS-2 Comparison Score | 6.67 (2.00) | 5.93 (1.53) | ns |
| Stanford-Binet 5 Matrices | 10.22 (1.56) | 11.58 (2.31) | ns |
| Stanford-Binet 5 Vocabulary | 11.00 (2.06) | 12.58 (3.37) | ns |
| Stanford-Binet 5 Total IQ | 104.67 (7.31) | 113.50 (14.46) | ns |
| ABAS-3 Communication | 52.90 (8.19) | 56.82 (6.13) | ns |
| ABAS-3 Social | 46.70 (8.82) | 51.35 (9.01) | ns |
Note. ns = statistically non-significant. TASSK-R = Test of Adolescent Social Skills Knowledge (Revised); QSQA/P-R = Quality of Socialization Questionnaire (Revised); SRS-2 = Social Responsiveness Scale-2; ASRS = Autism Spectrum Rating Scale
```

### ASD-SUP-PMC9399988@PMC9399988.2; acquired 2026-10-30#section_v2_1#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Keywords > Methods > Treatment fidelity · methods · text · 183 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×3, media×1, supplementary-material×1.

```text
All the sessions were videotaped and the quality of the treatment implementation was monitored by the first author (PEERS® Certified Provider). Participants’ adherence to treatment was controlled by recording teens’ and social coaches’ attendance and rates of completion of homework assignments. In both TG and WCG, participants attended a median number of 15 out of 16 sessions (93.8%), including those with low attendance. Waitlist control groups were conducted fully in person, but during illness and quarantine, participants could still participate online. Teens used this opportunity, on average, once during a program. The homework completion rate was high, regardless of the treatment delivery mode. For example, for six consecutive weeks teens were asked to call another participant, exchange information, and find common interests. In TG and WCG, completion rates of this homework were 95.2% and 98.0%, respectively.
```

### CDC-ASD-ABOUT@snapshot-20261017-2e3ce2c4559e#section_v2_1#0005
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Risk factors · body · text · 199 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
There is not just one cause of ASD. Many different factors have been identified that may make a child more likely to have ASD, including environmental, biologic, and genetic factors.

Although we know little about specific causes, the available evidence suggests that the following may put children at greater risk for developing ASD:

* Having a sibling with ASD

* Having certain genetic or chromosomal conditions, such as fragile X syndrome or tuberous sclerosis

* Experiencing complications at birth

* Being born to older parents

CDC is currently working on one of the largest US studies to date on ASD. This study, called Study to Explore Early Development (SEED) was designed to look at the risk factors and behaviors related to ASD among young children (ages 2-5 years) in the US. CDC is now conducting a follow-up study of older children who were previously enrolled in SEED to determine the health, functioning, and needs of people with ASD and other developmental disabilities as they mature.
```

### CDC-ASD-CLINICAL@snapshot-20261017-982fb2058ee3#section_v2_1#0002
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Diagnostic Tools for ASD > DSM-5 Diagnostic Criteria for Autism Spectrum Disorder · body · text · 33 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
In addition to diagnostic tools, the American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD.
```

### CDC-ASD-SCREENING@October 1, 2026#section_v2_1#0002
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Developmental monitoring > Information for families · body · text · 148 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Explore CDC's Milestone Tracker app, milestone checklists, and other materials. Access these free tools and more to help you track your child's milestones.

When you take your child to a well visit, your child's doctor or nurse will also do developmental monitoring. The doctor or nurse might ask you questions about your child's development or will talk and play with your child to see if they are developing and meeting milestones.

Your child's doctor or nurse may also ask about your child's family history. Be sure to let the doctor or nurse know about any conditions that your child's family members have, including ASD, learning disorders, intellectual disability, or attention-deficit/hyperactivity disorder (ADHD).

Keep Reading Developmental Monitoring and Screening
```

### CDC-ASD-SIGNS@snapshot-20261017-0fdf29dfc057#section_v2_1#0001
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Signs and symptoms > Social communication and interaction skills · body · text · 263 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Social communication and interaction skills can be challenging for people with ASD.

Examples of social communication and social interaction characteristics related to ASD can include

* Avoids or does not keep eye contact

* Does not respond to name by 9 months of age

* Does not show facial expressions such as happy, sad, angry, and surprised by 9 months of age

* Does not play simple interactive games like pat-a-cake by 12 months of age

* Uses few or no gestures by 12 months of age (for example, does not wave goodbye)

* Does not share interests with others by 15 months of age (for example, shows you an object that they like)

* Does not point to show you something interesting by 18 months of age

* Does not notice when others are hurt or upset by 24 months (2 years) of age

* Does not notice other children and join them in play by 36 months (3 years) of age

* Does not pretend to be something else, like a teacher or superhero, during play by 48 months (4 years) of age

* Does not sing, dance, or act for you by 60 months (5 years) of age

Keep Reading: Screening for Autism Spectrum Disorder
```

### CDC-ASD-TREATMENT@CDC public article reader captured 2026-10-30#section_v2_1#0003
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Types of Treatments > Developmental approaches · body · text · 237 tokens · trang [None, None]
- completeness: complete

```text
Developmental approaches focus on improving specific developmental skills, such as language skills or physical skills, or a broader range of interconnected developmental abilities. Developmental approaches are often combined with behavioral approaches.

The most common developmental therapy for people with ASD is speech and language therapy. Speech and language therapy helps to improve the person's understanding and use of speech and language. Some people with ASD communicate verbally. Others may communicate through the use of signs, gestures, pictures, or an electronic communication device.

Occupational therapy teaches skills that help the person live as independently as possible. Skills may include dressing, eating, bathing, and relating to people. Occupational therapy can also include

* Sensory integration therapy to help improve responses to sensory input that may be restrictive or overwhelming.

* Physical therapy can help improve physical skills, such as fine movements of the fingers or larger movements of the trunk and body.

The Early Start Denver Model (ESDM) is a broad developmental approach based on the principles of ABA. It is used with children 12–48 months of age. Parents and therapists use play, social exchanges, and shared attention in natural settings to improve language, social, and learning skills.
```

### CDC-CONCERNED@February 17, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Ask For a Referral · body · text · 120 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
If you or the doctor thinks there might be a delay, ask the doctor for a referral to a specialist who can do a more in-depth evaluation of your child.

Image: A mother holds her child on her lap while talking to a healthcare provider

Ask Your Doctor for a Referral

Doctors your child might be referred to include:

* Developmental pediatricians. These doctors have special training in child development and children with special needs.

* Child neurologists. These doctors work on the brain, spine, and nerves.

* Child psychologists or psychiatrists. These doctors know about the human mind.
```

### CDC-EARLY-INTERVENTION@CDC public article reader captured 2026-10-30#section_v2_1#0001
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What is "Early Intervention"? > Early Intervention... · body · text · 110 tokens · trang [None, None]
- completeness: complete

```text
* Is the term used to describe services and supports available to babies and young children with developmental delays and disabilities and their families.

* May include speech therapy, physical therapy, occupational therapy, and other types of therapies or services based on the needs of the child and family.

* Can have a significant impact on a child's ability to learn new skills and overcome challenges and can increase success in school and life.

* Programs are available in every state and territory. These publicly funded programs provide services for free or at reduced cost for any child who is eligible.
```

### CDC-MILESTONES-02@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most babies do by 2 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-04@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most babies do by 4 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-06@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most babies do by 6 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-09@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most babies do by 9 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-12@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most babies do by 1 year · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-15@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most children do by 15 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-18@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most children do by 18 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-24@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most children do by 2 years · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-30@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most children do by 30 months · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### CDC-MILESTONES-36@May 16, 2026#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What most children do by 3 years · body · text · 14 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: link_targets_and_multimedia×1.

```text
Click the links below to view a photo or video of each milestone.
```

### NIH-NIDCD-ASD-COMMUNICATION-2020@NIH Pub. No. 97–4315; April 2020#section_v2_1#0002
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Who is affected by ASD? · body · text · 60 tokens · trang [None, None]
- completeness: complete

```text
ASD affects people of every race, ethnic group, and socioeconomic background. It is four times more common among boys than among girls. The Centers for Disease Control and Prevention (CDC) estimates that about 1 in every 54 children in the U.S. has been identified as having ASD.
```

### NIH-NIMH-ADHD@NIH Publication No. 24-MH-8300; Revised 2024#section_v2_1#0006
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: How is ADHD treated? > Medication · body · text · 208 tokens · trang [None, None]
- completeness: complete

```text
Stimulants are the most common type of medication used to treat ADHD, and research shows them to be highly effective. They work by increasing levels of brain chemicals involved in thinking and attention.

Like all medications, stimulants can have side effects and must be prescribed and monitored by a health care provider. Tell the provider about other medications you or your child are taking. Medications for common health problems, such as diabetes, anxiety, and depression, can interact with stimulants, in which case, a provider can suggest other medication options.

Health care providers sometimes prescribe nonstimulant medications like antidepressants to treat ADHD. However, the U.S. Food and Drug Administration (FDA) has not approved these medications specifically for ADHD. Sometimes, a person must try several different medications or dosages before finding the one that works for them.

Learn more about stimulants and other mental health medications. You can learn more about specific medications, including the latest approvals, side effects, warnings, and patient information, on the FDA website.
```

### NIH-NIMH-ASD-2025@NIH Publication No. 25-MH-8084; Revised 2025#section_v2_1#0005
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: How is ASD diagnosed? > Diagnosis in young children > Stage 1: General developmental screening during well-child checkups · body · text · 186 tokens · trang [None, None]
- completeness: complete

```text
Every child should receive well-child checkups with a pediatrician or an early childhood health care provider. The American Academy of Pediatrics recommends that all children receive screening for developmental delays at their 9-, 18-, and 24- or 30-month well-child visits, with specific autism screenings at the 18- and 24-month well-child visits. A child may receive additional screenings if they have an increased likelihood of developing ASD or developmental problems.

Considering caregivers’ experiences and concerns is an important part of the screening process for young children. The health care provider may ask questions about the child’s behaviors and evaluate those answers together with information from ASD screening tools and clinical observations of the child. Learn more about ASD screening on the Centers for Disease Control and Prevention (CDC) website.

The health care provider may refer the child for additional evaluation if they show developmental differences in behavior or functioning during this screening process.
```

### NIH-NIMH-MEDICATIONS@snapshot-20261017-265ac64c9bc6#section_v2_1#0004
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What are antipsychotics? · body · text · 449 tokens · trang [None, None]
- completeness: complete

```text
Antipsychotic medications are typically used to treat psychosis, a condition that involves some loss of contact with reality. People experiencing a psychotic episode often experience delusions (false beliefs) or hallucinations. Psychosis can be related to drug use or a mental disorder such as schizophrenia, bipolar disorder, or severe depression (also known as psychotic depression).

Health care providers may also prescribe antipsychotics in combination with other medications to relieve symptoms of delirium, dementia, or other mental health conditions that are more common in older adults. The FDA requires that all antipsychotics include a black box warning stating that the medications are associated with increased rates of stroke and death in older adults with dementia.

Older, first-generation antipsychotic medications are sometimes called typical antipsychotics (or neuroleptics). Long-term use of typical antipsychotics may lead to a condition involving uncontrollable muscle movements called tardive dyskinesia, which can range from mild to severe. People who think they might have tardive dyskinesia should check with a health care provider before stopping their medication.

Newer, second-generation medications are sometimes called atypical antipsychotics. Several atypical antipsychotics are available. They are commonly used because they treat a broader range of symptoms compared with older medications. For example, atypical antipsychotics are sometimes used to treat bipolar depression or depression in people that have not responded to antidepressant medication alone. Health care providers may ask people taking atypical antipsychotics to participate in regular monitoring of weight, glucose levels, and lipid levels.

Some symptoms, such as agitation and hallucinations, typically go away within days of starting antipsychotic medication. Other symptoms, such as delusions, usually go away within a few weeks. However, people may not experience the full effects of antipsychotic medication for up to 6 weeks.

If a person’s symptoms do not improve with usual antipsychotic medications, they may be prescribed an atypical antipsychotic called clozapine. People who take clozapine must have regular blood tests to check for a potentially dangerous side effect that occurs in 1%–2% of people.
```

### NIH-NIMH-TEEN-BRAIN@NIH Publication No. 23-MH-8078; Revised 2023#section_v2_1#0003
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 4. Teen brains may respond differently to stress. · body · text · 57 tokens · trang [None, None]
- completeness: complete

```text
Because the teen brain is still developing, teens may respond to stress differently than adults. This could increase teens’ chances of developing stress-related mental illnesses such as anxiety and depression. Recognizing possible triggers and practicing effective coping techniques can help teens deal with stress. Learn more about managing stress.
```

### NIH-NIMH-TEEN-DEPRESSION@snapshot-20261017-d2d5221849f2#section_v2_1#0002
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: How do I get help for depression? · body · text · 225 tokens · trang [None, None]
- completeness: complete

```text
- **Talk to a trusted adult** (such as your parent or guardian, teacher, or school counselor) about how you’ve been feeling. - **Ask your doctor** about options for professional help. Depression can be treated with psychotherapy (also called “talk therapy”), medication, or a combination of medication and talk therapy. - **Try to spend time with friends or family,** even if you don’t feel like you want to. - **Stay active and exercise,** even if it’s just going for a walk. Physical activity releases chemicals, such as endorphins, in your brain that can help you feel better. - **Try to keep a regular sleep schedule.** - **Eat healthy foods.**

You’re not alone, and help is available. You can feel better. To get help, call or text the 988 Suicide & Crisis Lifeline at **988** or chat at **988lifeline.org.**

U.S. DEPARTMENT OF HEALTH AND HUMAN SERVICES National Institutes of Health NIMH Identification No. OM 22-4321
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2_1#0006
- lý do chọn: retrievable · abstract · section recovered by layout pass · retrieval_eligible: True
- section: Abstract · abstract · text · 505 tokens · trang [10, 10]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
at 6 months to examine mediation effects); and cost-effectiveness (assessed using the Client Service Receipt Inventory). Every effort was made to ensure that outcome assessors were blind to allocation. Results: A total of 138 participants were randomised ( n = 69 per group). Usual care was significantly different from the intervention, which was delivered with good fidelity and adherence and minimal contamination, and was associated with no adverse effects. Trial procedures and outcome measures were acceptable. Carers and therapists reported improvement in daily functioning. The primary analysis included 106 participants. There were no significant main effects of the intervention at 6 or 12 months. The adjusted mean difference between groups on the Aberrant Behavior Checklist – irritability at 6 months post randomisation was 0.40 (95% confidence interval –2.33 to 3.14; p = 0.77). Subgroup differences in irritability/agitation at 6 months were observed for sex of child (intervention × female = 6.42, 95% confidence interval 0.00 to 12.85; p = 0.050) and attention deficit hyperactivity disorder (intervention × attention deficit hyperactivity disorder = –6.77, 95% confidence interval –13.55 to –0.01; p = 0.050). There was an effect on carer stress at 6 months by region (intervention × South England = 7.01, 95% confidence interval 0.45 to 13.56; p = 0.04) and other neurodevelopmental/ genetic conditions (intervention × neurodevelopmental/genetic condition = –9.53, 95% confidence interval –18.08 to –0.98; p = 0.030). Carer-rated goal performance and satisfaction increased across sessions ( p < 0.001), with a mean change of 2.75 (95% confidence interval 2.14 to 3.37) for performance and a mean change of 3.34 (95% confidence interval 2.63 to 4.40) for satisfaction. Health economic evaluation suggests that sensory integration therapy is not cost-effective compared with usual care alone.
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2_1#0036
- lý do chọn: retrievable · methods · section recovered by layout pass · retrieval_eligible: True
- section: Methods · methods · text · 483 tokens · trang [25, 26]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
Design The SenITA trial was a two-arm individual RCT of SIT for children with autism and SPDs. Setting and population Children with autism and SPDs were recruited from child and adolescent mental health and paediatric services, schools and social services and via self-referral. Therapy was delivered in clinics meeting manualised fidelity criteria. Inclusion criteria were as follows: diagnosis of autism spectrum disorder or a related condition (e.g. social communication disorder), in and likely to remain in mainstream primary education for the duration of the trial (and aged 4 –11 years), definite/probable SPDs and carer consent/ child assent. Exclusion criteria were as follows: receipt of current/previous SIT and receipt of current applied behaviour analysis therapy.

xxiii

Intervention and comparator The intervention comprised Ayres Sensory Integration ® therapy delivered in 26 1-hour sessions over 26 weeks [i.e. two sessions per week for 10 weeks (intensive phase), followed by two sessions per month for 2 months and then one telephone session per month for 2 months (tailoring phase)]. The comparator was usual care, which was defined as awaiting services or receiving sensory-based intervention not meeting fidelity criteria for sensory integration. Pre-trial focus groups and interviews carried out with parents/carers and therapists allowed us to define usual care in trial regions and, to some extent, across the UK more broadly.

Sample size and randomisation A total of 138 participants were randomised in a 1 : 1 ratio based on 90% power, a 5% significance level and a moderate standardised effect size of 0.5 (inflated by 20% for dropout). Online randomisation utilised random permuted blocks stratified by region and severity of SPD. Costs and outcomes Sensory processing difficulties were assessed at screening and at 6 months. An Autism Diagnostic Observation Schedule was carried out at baseline to characterise the sample in terms of autism symptoms only and not for diagnostic purposes. Outcomes were measured at 6 and 12 months post randomisation. The primary outcome was irritability/agitation (as measured by the corresponding Aberrant Behavior Checklist subscale), indicative of challenging behaviour, at 6 months. Secondary outcomes included other problem behaviours, adaptive behaviours and functioning, socialisation, carer stress and quality of life.
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2_1#0193
- lý do chọn: excluded from retrieval · body · retrieval_eligible: False
- section: QUANTITATIVE RESULTS · body · text · 535 tokens · trang [99, 99]
- completeness: table_structure_unrecoverable — Bảng trong PDF mất cấu trúc hàng/cột và không dựng lại được một cách tin cậy; không dùng số liệu từ đoạn này. Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
TABLE 25 Subgroup analyses for Carer Stress at 6-months Subgroup analysis Variable Estimate 95% CI p-value Region (reference group = South Wales) SIT main effect –2.25 –6.05 to 1.56 0.24 S-WE region main effect –4.02 –9.30 to 1.26 0.13 SIT × S-WE region interaction 7.01 0.45 to 13.56 0.04 Age (continuous variable) SIT main effect 9.69 –4.79 to 24.18 0.19 Age main effect 0.65 –0.73 to 2.03 0.35 SIT × age interaction –1.24 –3.08 to 0.60 0.18 Sex (reference group = male) SIT main effect 0.03 –3.46 to 3.52 0.99 Female main effect 0.66 –5.34 to 6.66 0.83 SIT × female interaction 0.73 –7.24 to 8.70 0.86 SPM range (reference group = some problems) SIT main effect 2.73 –3.58 to 9.04 0.39 Definite dysfunction main effect 1.21 –4.58 to 7.00 0.68 SIT × definite dysfunction interaction –3.40 –10.67 to 3.87 0.36 Comorbiditya (reference group = no comorbidity) SIT main effect 1.31 –3.45 to 6.08 0.58 Comorbidity present main effect 3.65 –1.69 to 8.99 0.18 SIT × comorbidity present interaction –4.02 –10.78 to 2.74 0.24 ADHD a (reference group = no ADHD) SIT main effect –0.19 –4.08 to 3.69 0.92 ADHD present main effect 2.14 –4.35 to 8.62 0.51 SIT × ADHD present interaction –2.83
```

### WHO-CST-INTRO-2022@2022 English edition#section_v2_1#0004
- lý do chọn: excluded from retrieval · contributors_detected · retrieval_eligible: False
- section: (không có heading) · contributors_detected · text · 539 tokens · trang [7, 8]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Alonso-Rivera (International Pediatric Association, Mexico), Ana Andreeva-Sapundzhieva (Center for Social Rehabilitation and Integration, Bulgaria), Maria Paz Araya (Ministry of Health, Chile), Anara Asanalieva (Center for Children with Autism, Kyrgyzstan), Gulnaz Azhymambetova (Department of Health, Kyrgyzstan), Alexandra Bagney (Médecins sans Frontières, Spain), Merry Barua (Action for Autism, India), Tolulope Bella-Awusah (University of Ibadan, Nigeria), Erlinda Borromeo (Autism Hearts Foundation, USA), Daniel Bulte (University of Oxford, United Kingdom of Great Britain and Northern Ireland (United Kingdom)), July Caballero (Ministry of Mental Health, Peru), Carmen Julissa Cayo Medina (Instituto Nacional de Salud Mental, Peru), Ya-Chih Chang (Autism Speaks, USA), Tony Charman (King’s College London, United Kingdom), Biyuan Chen (Sun Yat-Sen University, China), Mariana Chervenkova (Autism Today Association, Bulgaria), Chung-Hsin Chiang (NCU, Taipei), Youngmin Choi (Republic of Korea), Brian Cort (Canada), Carla Cortez (Peru), Sebastián Cukier (PANAACEA, Argentina), Cristiane Silvestre de Paula (Mackenzie Presbyterian University, Brazil), Luc de Montigny (McGill University, Canada), Petrus De Vries (University of Cape Town, South Africa), Limia Dewan (BRAC Centre, Bangladesh), Marie-Charlotte Dextraze (Madawaska Valley Homeschoolers, Canada), Gauri Divan (Sangath, India), Pamela Dixon (Autism Speaks, USA), Winnie Dorego (Eastern Visayas Centre for Health Development, Philippines), Svyatoslav Dovbnya (Naked Heart Foundation, Russian Federation), Dzhamilia Dunganova (Kyrgyz State University, Kyrgyzstan), Patrick Dwyer (University of California, Davis, USA), Julian Eaton (CBM West Africa, Togo), Aala El- Khani (University of Manchester, United Kingdom), Mayada Elsabbagh (McGill University, Canada), Mohamed Ali AbdulFattah Mohamed ElShazly (International Medical Corps, Turkey), Camilla Ferrante (University of Milano-Bicocca, Italy), Magdalene Foo (Institute of Mental Health, Singapore), Natsuko Fukuda (Republic of Korea), Daniel Fung Shuen Sheng
```

### WHO-CST-INTRO-2022@2022 English edition#section_v2_1#0009
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: Background · introduction · text · 573 tokens · trang [11, 12]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
The five-part Caregiver skills training for families of children with developmental delays or disabilities (CST) package was developed to facilitate access to parenting support for caregivers of children with developmental delays or disabilities. The development of the training package materials was based on evidence on parenting and parent-mediated interventions for children with developmental disabilities and, in particular, on evidence on strategies targeting the caregivers of children with delays or impairment in social and communication domains. The training package was developed in consultation with – and informed by feedback from –international experts, service providers, caregivers and family advocates, with extensive field-testing across regions. Who is the caregiver skills training package for?

The intended audience is caregivers of children aged 2–9 years with developmental delays or disabilities, with a specific focus on caregivers of children with delays or impairments in social and communication domains – although the age range can be adjusted slightly, depending on the needs of the setting. Importantly, a diagnosis is not required to access the training course. The lack of a diagnostic requirement means that the training package can be provided to families once a developmental delay has been identified. This may reduce other potential barriers – including the potential reluctance of caregivers to identify themselves as the parents of children with developmental disabilities and experiences of stigma from attending a course labelled as being exclusively for caregivers of children with developmental conditions. The expectation is that primary health-care providers, community health workers, educational providers or specialists will recommend the caregiver skills training course to families.

Format of the caregiver skills training package The course is designed to be delivered in nine core group sessions for caregivers and three home visits. The group sessions can be provided at a health facility, school or other community-based facility. Each group session lasts 2.5 to 3 hours, including a break. Sessions can be scheduled either weekly or every two weeks depending on what is most feasible for caregivers in the local context. Home visits are scheduled at the beginning, middle and end of the course – i.e. before group session 1, between sessions 5 and 6, and after the final group session. Home visits are typically conducted in caregivers’ homes and last 1.5 to 2 hours each, although they can be offered in a community setting if home visits are not feasible due to geographical distance, safety concerns or other challenges. Typically, two caregivers per household are invited to participate in the group sessions. The core 9-session course has also been adapted for virtual delivery through videoconferencing for group sessions and home visits.

Additional group sessions and home visits can be offered to allow more time to acquire strategies related to caregiver well-being and strategies tailored to the needs of caregivers of children who have little or no spoken language.

Caregiver skills training implementation tools In addition to this introduction, there are four subsequent parts of the caregiver skills training package while two additional parts are being developed:
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2_1#0010
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: Background · introduction · text · 530 tokens · trang [9, 9]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
WHO’s caregiver skills training was developed to facilitate access to parenting skills and strategies for caregivers of children with developmental delays or disabilities. The target audience is caregivers of children aged 2–9 years with developmental delays or disabilities, with a specific focus on the caregivers of children with delays and impairments in social and communication domains. However, a child does not need to have a diagnosis for caregiver skills training to be used, and the age range can be adjusted slightly depending on the needs of the setting. Overview of CST structure The caregiver skills training intervention is designed to be delivered in nine group sessions and three home visits by trained and supervised non-specialist facilitators. Additional group sessions and home visits can be offered to allow more time for strategies on caregiver wellbeing and for strategies tailored to the needs of caregivers of children who have little or no spoken language. Materials There are five parts of the caregiver skills training package while two additional parts are being developed:  Introduction;  Adaptation and implementation guide;  Facilitators’ guide: group sessions 1–9;  Participants’ guide: group sessions 1–9;  Home visit guide for facilitators;  Caregivers of children who have little or no spoken language: facilitators’ and participants’ guides (forthcoming);  Caregiver wellbeing: facilitators’ and participants’ guides (forthcoming). The introduction provides information on how to use the different materials. How to use this guide This guide is meant to be used by caregivers who are participating in WHO’s caregiver skills training. The guide provides content that will be used during each of the caregiver skills training core group sessions (sessions 1–9). It contains illustrated descriptions of the key messages and tips (skills and strategies) taught in each session as well as goal-setting activities, questions to check your own learning and a template for sharing information on local resources for families (to be adapted to the local context). Content of the group sessions Sessions 1 and 2 focus on getting children engaged in activities (both daily home activities and play) and keeping them engaged. Session 3 focuses on the development of play and home routines as a means of encouraging engagement, communication, positive behaviour and skills for daily living and play. Sessions 4 and 5 focus on recognizing a child’s communication abilities and creating opportunities to promote communication. Session 6 focuses on teaching skills for everyday living in small steps using different levels of help. Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging behaviours. Session 9 focuses on caregiver well-being, problem-solving and setting goals for ongoing practice. Introduction
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2_1#0064
- lý do chọn: excluded from retrieval · body · retrieval_eligible: False
- section: Session 3: Helping children to share engagement in play and home routines · body · text · 525 tokens · trang [95, 96]
- completeness: text_encoding_lost — Văn bản trích xuất chứa mã glyph (/gidNNNNN) thay vì chữ — font PDF thiếu bảng ánh xạ ký tự; có bản trích xuất lại đề xuất trong data/extractions, chờ người duyệt. Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
/gid00035/gid00032 /gid00031/gid00042/gid00032/gid00046 /gid00036/gid00047/gid00164 /gid00046/gid00035/gid00032 /gid00030/gid00028/gid00041 /gid00034/gid00042 /gid00041/gid00032/gid00051/gid00047 /gid00047/gid00042 /gid00030/gid00045/gid00032/gid00028/gid00047/gid00032 /gid00028 /gid00029/gid00028/gid00030/gid00038/gid00183/gid00028/gid00041/gid00031/gid00183/gid00033/gid00042/gid00045/gid00047/gid00035 /gid00043/gid00028/gid00047/gid00047/gid00032/gid00045/gid00041/gid00163 /gid00006/gid00028/gid00030/gid00035 /gid00047/gid00036/gid00040/gid00032 /gid00028 /gid00046/gid00047/gid00036/gid00030/gid00038 /gid00034/gid00042/gid00032/gid00046 /gid00036/gid00041 /gid00047/gid00035/gid00032
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2_1#0143
- lý do chọn: retrievable · appendix · section recovered by layout pass · retrieval_eligible: True
- section: Annex 1: Summary of tips and key messages · appendix · text · 109 tokens · trang [272, 272]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Tips

1. Set up the space: remove distractions and make a safe place to interact.

2. Start with 2 or 3 motivating choices and follow your child’s choice.

3. Move in front of your child, get down to your child’s level, and have the activity between you and the child.

Key messages  All children can learn and develop skills.  Children learn best when they are calm and cool.  You can help your child to develop by engaging with her/him in everyday activities and games.
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2_1#0014
- lý do chọn: retrievable · recommendations · section recovered by layout pass · retrieval_eligible: True
- section: RECOMMENDATIONS · recommendations · text · 220 tokens · trang [11, 12]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
In order to improve early childhood development, WHO recommends: All infants and children should receive responsive care during the first 3 years of life; parents and other caregivers should be supported to provide responsive care. Strength of recommendation: Strong Quality of evidence: Moderate (for responsive care) RESPONSIVE CAREGIVING1 All infants and children should have early learning activities with their parents and other caregivers during the first 3 years of life; parents and other caregivers should be supported to engage in early learning with their infants and children. Strength of recommendation: Strong Quality of evidence: Moderate (for early learning) PROMOTE EARL Y LEARNING2 INTEGRATE CAREGIVING AND NUTRITION INTERVENTIONS3 Support for responsive care and early learning should be included as part of interventions for optimal nutrition of infants and young children. Strength of recommendation: Strong Quality of evidence: Moderate Psychosocial interventions to support maternal mental health should be integrated into early childhood health and development services.

Strength of recommendation: Strong Quality of evidence: Moderate SUPPORT MATERNAL MENTAL HEALTH4 viii ix

x 1
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2_1#0015
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: BACKGROUND · introduction · text · 411 tokens · trang [13, 13]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Enabling young children to achieve their full developmental potential is a human right and a critical requisite for sustainable development. Evidence in the Lancet series Advancing early childhood development: from science to scale (Lancet, 2017) highlights the profound benefits of investing in ECD for learning, productivity, health and social cohesion along the life course. The series highlighted the critical importance of the early years and coined the term ‘nurturing care’ as a central tenet of what is required to achieve optimal development, namely health, nutrition, security and safety, responsive caregiving and opportunities for early learning. The Nurturing Care Framework for early childhood development (WHO, UNICEF & World Bank Group, 2018) was launched at the World Health Assembly in 2018 to provide a roadmap for action. The Framework builds on state-of-the-art evidence about how child development outcomes are influenced and how they can be improved by policies and interventions. Nurturing care is characterized by a stable environment that promotes health and optimal nutrition, protects children from threats, and gives them opportunities for early learning, through affectionate interactions and relationships ( Figure). It describes how a whole-of-government and a whole-of-society approach can promote nurturing care for young children and outlines guiding principles, strategic actions and ways of monitoring progress. The Framework focuses on the period from pregnancy to age 3 within a life-course approach and addresses all relevant sectors, but with a spotlight on the health sector. ECD refers to the process of cognitive, physical, language, temperament, socioemotional and motor development of children that starts at the time of conception until 8 years of age. The earliest years are especially important, being the time when the brain develops rapidly; it is therefore a critical period for the fetus and child to receive nurturing care. It is also the period when the fetus and child are most sensitive to interventions (Lancet, 2017). Being at the forefront of providing nurturing care, parents and other primary
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2_1#0123
- lý do chọn: excluded from retrieval · noise · retrieval_eligible: False
- section: GUIDELINE DEVELOPMENT GROUP · noise · text · 5 tokens · trang [63, 63]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
ANNEX 5:
```
