# Chunking pilot — section_v2 — 2026-11-14

Chưa gọi API bên ngoài. Chunk lưu trong DB nhưng tài liệu chưa được phê duyệt nên không truy xuất được.

| source_id | vai trò | chunk | eligible | bảng | token min/median/max | % giữ | trang | đầy đủ |
|---|---|---:|---:|---:|---|---:|---|---|
| ASD-CSV-002 | core | 72 | 43 | 1 | 59/440/594 | 99.2 | — | complete:68, references_missing_component:4 |
| ASD-CSV-062 | core | 62 | 51 | 13 | 9/304/590 | 97.7 | — | complete:62 |
| ASD-OA-PMC7407189 | core | 93 | 46 | 4 | 7/492/597 | 99.2 | — | complete:93 |
| CDC-EARLY-INTERVENTION | core | 4 | 4 | 0 | 14/110/355 | 98.8 | — | complete:4 |
| NIH-NIMH-MEDICATIONS | core | 12 | 12 | 0 | 53/258/644 | 100.0 | — | complete:12 |
| ASD-CSV-007 | gaps | 50 | 30 | 3 | 21/328/597 | 97.2 | — | document_has_gaps:40, references_missing_component:10 |
| NIHR-SENITA-2022 | gaps | 324 | 232 | 0 | 3/382/657 | 86.8 | [1, 172] | document_has_gaps:216, table_structure_lost:55, references_missing_component:53 |
| WHO-CST-INTRO-2022 | gaps | 20 | 9 | 0 | 28/513/576 | 99.7 | — | table_structure_lost:2, document_has_gaps:18 |
| WHO-CST-PARTICIPANTS-2022 | gaps | 261 | 174 | 0 | 2/48/609 | 92.7 | — | table_structure_lost:59, document_has_gaps:202 |
| WHO-ECD-GUIDELINE-2020 | gaps | 233 | 128 | 0 | 5/99/621 | 98.7 | — | document_has_gaps:170, table_structure_lost:62, references_missing_component:1 |

## Ví dụ chunk

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v2#0003
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

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v2#0014
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Empirically Validated Screening and Diagnostic Measures > Autism Screening > Screening Tool for Autism in Toddlers · body · text · 205 tokens · trang [None, None]
- completeness: complete

```text
The Screening Tool for Autism in Toddlers (STAT; Stone et al., 2004) is a Level 2 screening measure administered by a trained professional. It comprises 12 play-based activities to observe early social communication behaviors in children from 24 to 35 months of age that can be administered in 15 to 20 min. The total score is derived by summing the four domain scores (play, requesting, directing attention, and motor imitation), with higher scores representing greater impairment. Sensitivity for autism classification is estimated to be 0.92, and specificity is 0.85, with a test–retest reliability of 0.90 (Stone et al., 2004). The STAT has shown good discriminant validity between autism and non-spectrum (0.95; Stone et al., 2004). Nevertheless, the original study sample size was relatively small. Recent research examining its psychometrics is limited.
```

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v2#0016
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

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v2#0017
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Results > Clinical Presentation of ASD With and Without Clinically Elevated ADHD and Anxiety Symptoms · results · text · 128 tokens · trang [None, None]
- completeness: complete

```text
We compared the four defined groups based on the CPRS ADHD index scores and the anxious-shy scores. The male:female ratio did not differ significantly among the groups in a non-parametric chi-square analysis [χ (3)2 = 3.18, p > 0.05]. As presented in Table 2, parental ages at pregnancy and educational attainment in the four examined groups were not significantly different using one-way MANOVAs. Only the ANOVA for the child's age yielded a significant main effect, however post-hoc Scheffe analysis did not reveal any significant difference between each pair of the groups.
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v2#0015
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: 4. Oral Over-the-Counter Medicines · body · text · 431 tokens · trang [None, None]
- completeness: complete

```text
Sleep pills should be considered to be an additional treatment option to improve sleep in children when non-pharmacological interventions are unsuccessful [17]. However, in children with ASD pharmacological treatment is sometimes convenient as a first-line strategy together with non-pharmacological approaches, given the greater severity of sleep disturbances in these patients [25]. Both prescription hypnotic drugs and OTC sleep-promoting agents might be useful in clinical practice. Due to the scarcity of controlled studies, there is no sleep medication approved by the FDA and only one—prolonged-release melatonin for the treatment of insomnia—approved by the EMA for children and adolescents with ASD. Sleep-promoting agents are therefore widely prescribed off-label, the most commonly used off-label medications being sedating antihistamines (e.g., diphenhydramine or hydroxyzine), melatonin, α2-receptor agonists (e.g., clonidine), benzodiazepines, pyrimidine derivatives (e.g., zaleplon and zolpidem), antipsychotics (e.g., risperidone and quetiapine), and sedating antidepressants (e.g., trazodone and mirtazapine) [68].

Some of the above-mentioned agents—i.e., antihistamines and melatonin—are available over the counter in many countries all over the world. Non-prescription medications—including OTC drugs, nutritional supplements, and herbal remedies—are indeed widespread therapies for sleep disturbances in children, as they are generally easily accessible and well accepted by caregivers. Furthermore, oral non-prescription treatments are often considered to be a “safe choice” by clinicians, as they usually have less significant side effects in comparison to some prescription hypnotic drugs—such as antipsychotics and antidepressants [12,69].

Here we describe the oral non-prescription treatments and nutritional supplements most commonly used for sleep problems in children with ASD: melatonin, antihistamines, tryptophan, carnosine, vitamin D, iron, other multivitamin and mineral supplements, and herbal remedies.
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v2#0088
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

### CDC-EARLY-INTERVENTION@CDC public article reader captured 2026-10-30#section_v2#0001
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: What is "Early Intervention"? > Early Intervention... · body · text · 110 tokens · trang [None, None]
- completeness: complete

```text
* Is the term used to describe services and supports available to babies and young children with developmental delays and disabilities and their families.

* May include speech therapy, physical therapy, occupational therapy, and other types of therapies or services based on the needs of the child and family.

* Can have a significant impact on a child's ability to learn new skills and overcome challenges and can increase success in school and life.

* Programs are available in every state and territory. These publicly funded programs provide services for free or at reduced cost for any child who is eligible.
```

### NIH-NIMH-MEDICATIONS@snapshot-20261017-265ac64c9bc6#section_v2#0004
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

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2#0011
- lý do chọn: retrievable body chunk · retrieval_eligible: True
- section: Results > Psychiatric Comorbidities in Children and Adolescents With Autism Spectrum Disorders · results · text · 139 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×3, supplementary-material×3.

```text
Random effect analysis for each comorbidity in all pediatric populations, children and adolescents, in addition to heterogeneity for each analysis can be found in Table 1. Prevalence of ID in all pediatric populations was found as 22.9% (95% CI: 17.7- 29.2) (Figure 2). Prevalence of ADHD in all pediatric populations was found as 26.2% (Figure 3) and prevalence of anxiety disorders in all pediatric populations was found as 11.1% (Figure 4). All statistical analysis groups showed high heterogeneity as shown by I value higher than 84.
```

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2#0012
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

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2#0006
- lý do chọn: retrievable · abstract · section recovered by layout pass · retrieval_eligible: True
- section: Abstract · abstract · text · 505 tokens · trang [10, 10]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
at 6 months to examine mediation effects); and cost-effectiveness (assessed using the Client Service Receipt Inventory). Every effort was made to ensure that outcome assessors were blind to allocation. Results: A total of 138 participants were randomised ( n = 69 per group). Usual care was significantly different from the intervention, which was delivered with good fidelity and adherence and minimal contamination, and was associated with no adverse effects. Trial procedures and outcome measures were acceptable. Carers and therapists reported improvement in daily functioning. The primary analysis included 106 participants. There were no significant main effects of the intervention at 6 or 12 months. The adjusted mean difference between groups on the Aberrant Behavior Checklist – irritability at 6 months post randomisation was 0.40 (95% confidence interval –2.33 to 3.14; p = 0.77). Subgroup differences in irritability/agitation at 6 months were observed for sex of child (intervention × female = 6.42, 95% confidence interval 0.00 to 12.85; p = 0.050) and attention deficit hyperactivity disorder (intervention × attention deficit hyperactivity disorder = –6.77, 95% confidence interval –13.55 to –0.01; p = 0.050). There was an effect on carer stress at 6 months by region (intervention × South England = 7.01, 95% confidence interval 0.45 to 13.56; p = 0.04) and other neurodevelopmental/ genetic conditions (intervention × neurodevelopmental/genetic condition = –9.53, 95% confidence interval –18.08 to –0.98; p = 0.030). Carer-rated goal performance and satisfaction increased across sessions ( p < 0.001), with a mean change of 2.75 (95% confidence interval 2.14 to 3.37) for performance and a mean change of 3.34 (95% confidence interval 2.63 to 4.40) for satisfaction. Health economic evaluation suggests that sensory integration therapy is not cost-effective compared with usual care alone.
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2#0008
- lý do chọn: excluded · flattened PDF table (table_structure_lost) · retrieval_eligible: False
- section: Abstract · abstract · text · 36 tokens · trang [10, 11]
- completeness: table_structure_lost — Bảng trong PDF đã mất cấu trúc hàng/cột khi trích xuất; không dùng số liệu từ đoạn này. Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
ABSTRACT viii

Contents List of tables xv List of figures xvii List of abbreviations xix Plain English summary xxi Scientific summary xxiii Chapter 1 Introduction 1
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2#0037
- lý do chọn: retrievable · methods · section recovered by layout pass · retrieval_eligible: True
- section: Methods · methods · text · 483 tokens · trang [25, 26]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
Design The SenITA trial was a two-arm individual RCT of SIT for children with autism and SPDs. Setting and population Children with autism and SPDs were recruited from child and adolescent mental health and paediatric services, schools and social services and via self-referral. Therapy was delivered in clinics meeting manualised fidelity criteria. Inclusion criteria were as follows: diagnosis of autism spectrum disorder or a related condition (e.g. social communication disorder), in and likely to remain in mainstream primary education for the duration of the trial (and aged 4 –11 years), definite/probable SPDs and carer consent/ child assent. Exclusion criteria were as follows: receipt of current/previous SIT and receipt of current applied behaviour analysis therapy.

xxiii

Intervention and comparator The intervention comprised Ayres Sensory Integration ® therapy delivered in 26 1-hour sessions over 26 weeks [i.e. two sessions per week for 10 weeks (intensive phase), followed by two sessions per month for 2 months and then one telephone session per month for 2 months (tailoring phase)]. The comparator was usual care, which was defined as awaiting services or receiving sensory-based intervention not meeting fidelity criteria for sensory integration. Pre-trial focus groups and interviews carried out with parents/carers and therapists allowed us to define usual care in trial regions and, to some extent, across the UK more broadly.

Sample size and randomisation A total of 138 participants were randomised in a 1 : 1 ratio based on 90% power, a 5% significance level and a moderate standardised effect size of 0.5 (inflated by 20% for dropout). Online randomisation utilised random permuted blocks stratified by region and severity of SPD. Costs and outcomes Sensory processing difficulties were assessed at screening and at 6 months. An Autism Diagnostic Observation Schedule was carried out at baseline to characterise the sample in terms of autism symptoms only and not for diagnostic purposes. Outcomes were measured at 6 and 12 months post randomisation. The primary outcome was irritability/agitation (as measured by the corresponding Aberrant Behavior Checklist subscale), indicative of challenging behaviour, at 6 months. Secondary outcomes included other problem behaviours, adaptive behaviours and functioning, socialisation, carer stress and quality of life.
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v2#0235
- lý do chọn: excluded from retrieval · noise · retrieval_eligible: False
- section: (không có heading) · noise · text · 42 tokens · trang [121, 121]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
0 100 200 300 400 500 600 700 800 900 1000
```

### WHO-CST-INTRO-2022@2022 English edition#section_v2#0000
- lý do chọn: excluded · flattened PDF table (table_structure_lost) · retrieval_eligible: False
- section: (không có heading) · unclassified · text · 28 tokens · trang [None, None]
- completeness: table_structure_lost — Bảng trong PDF đã mất cấu trúc hàng/cột khi trích xuất; không dùng số liệu từ đoạn này. Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Caregiver skills training for families of children with developmental delays or disabilities Caregiver skills training for families of children with developmental delays or disabilities
```

### WHO-CST-INTRO-2022@2022 English edition#section_v2#0005
- lý do chọn: excluded from retrieval · contributors_detected · retrieval_eligible: False
- section: (không có heading) · contributors_detected · text · 539 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Alonso-Rivera (International Pediatric Association, Mexico), Ana Andreeva-Sapundzhieva (Center for Social Rehabilitation and Integration, Bulgaria), Maria Paz Araya (Ministry of Health, Chile), Anara Asanalieva (Center for Children with Autism, Kyrgyzstan), Gulnaz Azhymambetova (Department of Health, Kyrgyzstan), Alexandra Bagney (Médecins sans Frontières, Spain), Merry Barua (Action for Autism, India), Tolulope Bella-Awusah (University of Ibadan, Nigeria), Erlinda Borromeo (Autism Hearts Foundation, USA), Daniel Bulte (University of Oxford, United Kingdom of Great Britain and Northern Ireland (United Kingdom)), July Caballero (Ministry of Mental Health, Peru), Carmen Julissa Cayo Medina (Instituto Nacional de Salud Mental, Peru), Ya-Chih Chang (Autism Speaks, USA), Tony Charman (King’s College London, United Kingdom), Biyuan Chen (Sun Yat-Sen University, China), Mariana Chervenkova (Autism Today Association, Bulgaria), Chung-Hsin Chiang (NCU, Taipei), Youngmin Choi (Republic of Korea), Brian Cort (Canada), Carla Cortez (Peru), Sebastián Cukier (PANAACEA, Argentina), Cristiane Silvestre de Paula (Mackenzie Presbyterian University, Brazil), Luc de Montigny (McGill University, Canada), Petrus De Vries (University of Cape Town, South Africa), Limia Dewan (BRAC Centre, Bangladesh), Marie-Charlotte Dextraze (Madawaska Valley Homeschoolers, Canada), Gauri Divan (Sangath, India), Pamela Dixon (Autism Speaks, USA), Winnie Dorego (Eastern Visayas Centre for Health Development, Philippines), Svyatoslav Dovbnya (Naked Heart Foundation, Russian Federation), Dzhamilia Dunganova (Kyrgyz State University, Kyrgyzstan), Patrick Dwyer (University of California, Davis, USA), Julian Eaton (CBM West Africa, Togo), Aala El- Khani (University of Manchester, United Kingdom), Mayada Elsabbagh (McGill University, Canada), Mohamed Ali AbdulFattah Mohamed ElShazly (International Medical Corps, Turkey), Camilla Ferrante (University of Milano-Bicocca, Italy), Magdalene Foo (Institute of Mental Health, Singapore), Natsuko Fukuda (Republic of Korea), Daniel Fung Shuen Sheng
```

### WHO-CST-INTRO-2022@2022 English edition#section_v2#0010
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: Background · introduction · text · 574 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
The five-part Caregiver skills training for families of children with developmental delays or disabilities (CST) package was developed to facilitate access to parenting support for caregivers of children with developmental delays or disabilities. The development of the training package materials was based on evidence on parenting and parent-mediated interventions for children with developmental disabilities and, in particular, on evidence on strategies targeting the caregivers of children with delays or impairment in social and communication domains. The training package was developed in consultation with – and informed by feedback from –international experts, service providers, caregivers and family advocates, with extensive field-testing across regions. Who is the caregiver skills training package for?

The intended audience is caregivers of children aged 2–9 years with developmental delays or disabilities, with a specific focus on caregivers of children with delays or impairments in social and communication domains – although the age range can be adjusted slightly, depending on the needs of the setting. Importantly, a diagnosis is not required to access the training course. The lack of a diagnostic requirement means that the training package can be provided to families once a developmental delay has been identified. This may reduce other potential barriers – including the potential reluctance of caregivers to identify themselves as the parents of children with developmental disabilities and experiences of stigma from attending a course labelled as being exclusively for caregivers of children with developmental conditions. The expectation is that primary health-care providers, community health workers, educational providers or specialists will recommend the caregiver skills training course to families.

Format of the caregiver skills training package The course is designed to be delivered in nine core group sessions for caregivers and three home visits. The group sessions can be provided at a health facility, school or other community-based facility. Each group session lasts 2.5 to 3 hours, including a break. Sessions can be scheduled either weekly or every two weeks depending on what is most feasible for caregivers in the local context. Home visits are scheduled at the beginning, middle and end of the course – i.e. before group session 1, between sessions 5 and 6, and after the final group session. Home visits are typically conducted in caregivers’ homes and last 1.5 to 2 hours each, although they can be offered in a community setting if home visits are not feasible due to geographical distance, safety concerns or other challenges. Typically, two caregivers per household are invited to participate in the group sessions. The core 9-session course has also been adapted for virtual delivery through videoconferencing for group sessions and home visits.

Additional group sessions and home visits can be offered to allow more time to acquire strategies related to caregiver well-being and strategies tailored to the needs of caregivers of children who have little or no spoken language.

2 Caregiver skills training implementation tools In addition to this introduction, there are four subsequent parts of the caregiver skills training package while two additional parts are being developed:
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2#0000
- lý do chọn: excluded · flattened PDF table (table_structure_lost) · retrieval_eligible: False
- section: (không có heading) · unclassified · text · 47 tokens · trang [None, None]
- completeness: table_structure_lost — Bảng trong PDF đã mất cấu trúc hàng/cột khi trích xuất; không dùng số liệu từ đoạn này. Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Participants’ guide group sessions 1–9 Caregiver skills training for families of children with developmental delays or disabilities

Participants’ guide group sessions 1–9 Caregiver skills training for families of children with developmental delays or disabilities
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2#0010
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: Background · introduction · text · 530 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
WHO’s caregiver skills training was developed to facilitate access to parenting skills and strategies for caregivers of children with developmental delays or disabilities. The target audience is caregivers of children aged 2–9 years with developmental delays or disabilities, with a specific focus on the caregivers of children with delays and impairments in social and communication domains. However, a child does not need to have a diagnosis for caregiver skills training to be used, and the age range can be adjusted slightly depending on the needs of the setting. Overview of CST structure The caregiver skills training intervention is designed to be delivered in nine group sessions and three home visits by trained and supervised non-specialist facilitators. Additional group sessions and home visits can be offered to allow more time for strategies on caregiver wellbeing and for strategies tailored to the needs of caregivers of children who have little or no spoken language. Materials There are five parts of the caregiver skills training package while two additional parts are being developed:  Introduction;  Adaptation and implementation guide;  Facilitators’ guide: group sessions 1–9;  Participants’ guide: group sessions 1–9;  Home visit guide for facilitators;  Caregivers of children who have little or no spoken language: facilitators’ and participants’ guides (forthcoming);  Caregiver wellbeing: facilitators’ and participants’ guides (forthcoming). The introduction provides information on how to use the different materials. How to use this guide This guide is meant to be used by caregivers who are participating in WHO’s caregiver skills training. The guide provides content that will be used during each of the caregiver skills training core group sessions (sessions 1–9). It contains illustrated descriptions of the key messages and tips (skills and strategies) taught in each session as well as goal-setting activities, questions to check your own learning and a template for sharing information on local resources for families (to be adapted to the local context). Content of the group sessions Sessions 1 and 2 focus on getting children engaged in activities (both daily home activities and play) and keeping them engaged. Session 3 focuses on the development of play and home routines as a means of encouraging engagement, communication, positive behaviour and skills for daily living and play. Sessions 4 and 5 focus on recognizing a child’s communication abilities and creating opportunities to promote communication. Session 6 focuses on teaching skills for everyday living in small steps using different levels of help. Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging behaviours. Session 9 focuses on caregiver well-being, problem-solving and setting goals for ongoing practice. Introduction
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2#0124
- lý do chọn: excluded from retrieval · front_matter_detected · retrieval_eligible: False
- section: Session 5: Promoting communication · front_matter_detected · text · 37 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
What we will learn today ..................................................................................................120 Personal goals .................................................................................................................121 Fernando’s story: Helping Anna learn to request what she needs ..................................122
```

### WHO-CST-PARTICIPANTS-2022@2022 English edition#section_v2#0251
- lý do chọn: retrievable · appendix · section recovered by layout pass · retrieval_eligible: True
- section: Annex 1: Summary of tips and key messages · appendix · text · 123 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Session 7: Preventing challenging behaviour – helping children to stay engaged and regulated

1. Respond to skills and appropriate behaviour with praise and encouragement.

2. Look and listen for signals before the challenging behaviour.

3. Arrange your environment and give warnings before changing activities to help your child stay cool.

4. If your child has a “meltdown” or “tantrum”, stay calm and wait for the child to calm down.

Then think about the reason for the behaviour  Children can communicate by using challenging behaviour to get access or attention, to avoid something or to get a sensation.

266
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2#0002
- lý do chọn: excluded · flattened PDF table (table_structure_lost) · retrieval_eligible: False
- section: IMPROVING · body · text · 32 tokens · trang [None, None]
- completeness: table_structure_lost — Bảng trong PDF đã mất cấu trúc hàng/cột khi trích xuất; không dùng số liệu từ đoạn này. Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Design: Eddy Hill Design Printed in Switzerland ii iii

Financial support ii Acronyms iv Glossary of terms v Acknowledgements vi Executive summary viii
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2#0014
- lý do chọn: retrievable · recommendations · section recovered by layout pass · retrieval_eligible: True
- section: RECOMMENDATIONS · recommendations · text · 220 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
In order to improve early childhood development, WHO recommends: All infants and children should receive responsive care during the first 3 years of life; parents and other caregivers should be supported to provide responsive care. Strength of recommendation: Strong Quality of evidence: Moderate (for responsive care) RESPONSIVE CAREGIVING1 All infants and children should have early learning activities with their parents and other caregivers during the first 3 years of life; parents and other caregivers should be supported to engage in early learning with their infants and children. Strength of recommendation: Strong Quality of evidence: Moderate (for early learning) PROMOTE EARL Y LEARNING2 INTEGRATE CAREGIVING AND NUTRITION INTERVENTIONS3 Support for responsive care and early learning should be included as part of interventions for optimal nutrition of infants and young children. Strength of recommendation: Strong Quality of evidence: Moderate Psychosocial interventions to support maternal mental health should be integrated into early childhood health and development services.

Strength of recommendation: Strong Quality of evidence: Moderate SUPPORT MATERNAL MENTAL HEALTH4 viii ix

x 1
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2#0015
- lý do chọn: retrievable · introduction · section recovered by layout pass · retrieval_eligible: True
- section: BACKGROUND · introduction · text · 411 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
Enabling young children to achieve their full developmental potential is a human right and a critical requisite for sustainable development. Evidence in the Lancet series Advancing early childhood development: from science to scale (Lancet, 2017) highlights the profound benefits of investing in ECD for learning, productivity, health and social cohesion along the life course. The series highlighted the critical importance of the early years and coined the term ‘nurturing care’ as a central tenet of what is required to achieve optimal development, namely health, nutrition, security and safety, responsive caregiving and opportunities for early learning. The Nurturing Care Framework for early childhood development (WHO, UNICEF & World Bank Group, 2018) was launched at the World Health Assembly in 2018 to provide a roadmap for action. The Framework builds on state-of-the-art evidence about how child development outcomes are influenced and how they can be improved by policies and interventions. Nurturing care is characterized by a stable environment that promotes health and optimal nutrition, protects children from threats, and gives them opportunities for early learning, through affectionate interactions and relationships ( Figure). It describes how a whole-of-government and a whole-of-society approach can promote nurturing care for young children and outlines guiding principles, strategic actions and ways of monitoring progress. The Framework focuses on the period from pregnancy to age 3 within a life-course approach and addresses all relevant sectors, but with a spotlight on the health sector. ECD refers to the process of cognitive, physical, language, temperament, socioemotional and motor development of children that starts at the time of conception until 8 years of age. The earliest years are especially important, being the time when the brain develops rapidly; it is therefore a critical period for the fetus and child to receive nurturing care. It is also the period when the fetus and child are most sensitive to interventions (Lancet, 2017). Being at the forefront of providing nurturing care, parents and other primary
```

### WHO-ECD-GUIDELINE-2020@2020 English edition#section_v2#0125
- lý do chọn: excluded from retrieval · back_matter · retrieval_eligible: False
- section: ANNEX 6: > DECLARATIONS OF CONFLICTS OF INTEREST · back_matter · text · 8 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
WAZ 1 RCT No serious
```
