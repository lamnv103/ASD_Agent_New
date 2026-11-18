# Chunking pilot — section_v1 — 2026-11-14

Chưa gọi API bên ngoài. Chunk lưu trong DB nhưng tài liệu chưa được phê duyệt nên không truy xuất được.

| source_id | vai trò | chunk | eligible | bảng | token min/median/max | % giữ | trang | đầy đủ |
|---|---|---:|---:|---:|---|---:|---|---|
| ASD-CSV-002 | core | 72 | 43 | 1 | 59/440/594 | 99.2 | — | complete:68, references_missing_component:4 |
| ASD-CSV-062 | core | 62 | 52 | 13 | 9/291/593 | 97.7 | — | complete:62 |
| ASD-OA-PMC7407189 | core | 93 | 46 | 4 | 7/492/597 | 99.2 | — | complete:93 |
| CDC-EARLY-INTERVENTION | core | 4 | 4 | 0 | 14/110/355 | 98.8 | — | complete:4 |
| NIH-NIMH-MEDICATIONS | core | 12 | 12 | 0 | 53/258/644 | 100.0 | — | complete:12 |
| ASD-CSV-007 | gaps | 50 | 30 | 3 | 21/328/597 | 97.2 | — | document_has_gaps:40, references_missing_component:10 |
| NIHR-SENITA-2022 | gaps | 286 | 286 | 0 | 44/509/647 | 100.0 | [1, 172] | document_has_gaps:239, references_missing_component:47 |
| WHO-CST-INTRO-2022 | gaps | 20 | 20 | 0 | 60/484/600 | 100.0 | — | document_has_gaps:20 |

## Ví dụ chunk

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v1#0003
- section: Changes in Diagnostic Criteria Over Time · body · table · 177 tokens · trang [None, None]
- completeness: complete

```text
Table 1.
Diagnostic Criteria of Autism Spectrum Disorder in the DSM-5
A. Social communication and interaction challenges:
1. Deficits in social-emotional reciprocity
2. Deficits in nonverbal communicative behaviors used for social interaction
3. Deficits in developing, maintaining, and understanding relationships
B. Repetitive or stereotyped behaviors:
1. Stereotyped or repetitive motor movements, use of objects, or speech
2. Insistence on sameness, inflexible adherence to routines, or ritualized patterns of verbal or nonverbal behavior
3. Highly restricted, fixated interests that are abnormal in intensity or focus
4. Hyper- or hypo-reactivity to sensory input or unusual interest in sensory aspects of the environment
Note. DSM-5 = Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition.
```

### ASD-CSV-002@snapshot-20261017-21dc8929f5a6#section_v1#0014
- section: Empirically Validated Screening and Diagnostic Measures > Autism Screening > Screening Tool for Autism in Toddlers · body · text · 205 tokens · trang [None, None]
- completeness: complete

```text
The Screening Tool for Autism in Toddlers (STAT; Stone et al., 2004) is a Level 2 screening measure administered by a trained professional. It comprises 12 play-based activities to observe early social communication behaviors in children from 24 to 35 months of age that can be administered in 15 to 20 min. The total score is derived by summing the four domain scores (play, requesting, directing attention, and motor imitation), with higher scores representing greater impairment. Sensitivity for autism classification is estimated to be 0.92, and specificity is 0.85, with a test–retest reliability of 0.90 (Stone et al., 2004). The STAT has shown good discriminant validity between autism and non-spectrum (0.95; Stone et al., 2004). Nevertheless, the original study sample size was relatively small. Recent research examining its psychometrics is limited.
```

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v1#0016
- section: Results > Parents' and Teachers' Reports of ADHD and Anxiety Symptoms · results · table · 206 tokens · trang [None, None]
- completeness: complete

```text
Table 1
Mean standard scores of parent and teacher ratings on CRS subdomains.
 | Parents | Teacher | F(1, 249) | η
CRS IA | 65.08 (11.28) | 61.26 (11.06) | 24.73*** | 0.09
CRS HI | 62.59 (11.94) | 58.18 (11.26) | 31.69*** | 0.11
CRS Anxiety | 61.40 (13.75) | 68.25 (13.37) | 44.14*** | 0.15
CRS, Conners' rating scales; IA, inattention; HI, hyperactivity/impulsivity.
***
p < 0.001.
```

### ASD-CSV-062@snapshot-20261017-ae3af4714e9d#section_v1#0017
- section: Results > Clinical Presentation of ASD With and Without Clinically Elevated ADHD and Anxiety Symptoms · results · text · 128 tokens · trang [None, None]
- completeness: complete

```text
We compared the four defined groups based on the CPRS ADHD index scores and the anxious-shy scores. The male:female ratio did not differ significantly among the groups in a non-parametric chi-square analysis [χ (3)2 = 3.18, p > 0.05]. As presented in Table 2, parental ages at pregnancy and educational attainment in the four examined groups were not significantly different using one-way MANOVAs. Only the ANOVA for the child's age yielded a significant main effect, however post-hoc Scheffe analysis did not reveal any significant difference between each pair of the groups.
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v1#0015
- section: 4. Oral Over-the-Counter Medicines · body · text · 431 tokens · trang [None, None]
- completeness: complete

```text
Sleep pills should be considered to be an additional treatment option to improve sleep in children when non-pharmacological interventions are unsuccessful [17]. However, in children with ASD pharmacological treatment is sometimes convenient as a first-line strategy together with non-pharmacological approaches, given the greater severity of sleep disturbances in these patients [25]. Both prescription hypnotic drugs and OTC sleep-promoting agents might be useful in clinical practice. Due to the scarcity of controlled studies, there is no sleep medication approved by the FDA and only one—prolonged-release melatonin for the treatment of insomnia—approved by the EMA for children and adolescents with ASD. Sleep-promoting agents are therefore widely prescribed off-label, the most commonly used off-label medications being sedating antihistamines (e.g., diphenhydramine or hydroxyzine), melatonin, α2-receptor agonists (e.g., clonidine), benzodiazepines, pyrimidine derivatives (e.g., zaleplon and zolpidem), antipsychotics (e.g., risperidone and quetiapine), and sedating antidepressants (e.g., trazodone and mirtazapine) [68].

Some of the above-mentioned agents—i.e., antihistamines and melatonin—are available over the counter in many countries all over the world. Non-prescription medications—including OTC drugs, nutritional supplements, and herbal remedies—are indeed widespread therapies for sleep disturbances in children, as they are generally easily accessible and well accepted by caregivers. Furthermore, oral non-prescription treatments are often considered to be a “safe choice” by clinicians, as they usually have less significant side effects in comparison to some prescription hypnotic drugs—such as antipsychotics and antidepressants [12,69].

Here we describe the oral non-prescription treatments and nutritional supplements most commonly used for sleep problems in children with ASD: melatonin, antihistamines, tryptophan, carnosine, vitamin D, iron, other multivitamin and mineral supplements, and herbal remedies.
```

### ASD-OA-PMC7407189@PMC distributed version 1#section_v1#0088
- section: Tables · floating_table · table · 76 tokens · trang [None, None]
- completeness: complete

```text
brainsci-10-00441-t001_Table 1Table 1
Stepwise approach to sleep disturbances in children. Adapted from Howlett et al. (2020) [10].
Level 1 | Sleep education and implementation of healthy sleep practices
Level 2 | Specific behavioral strategies
Level 3 | Medications
```

### CDC-EARLY-INTERVENTION@CDC public article reader captured 2026-10-30#section_v1#0001
- section: What is "Early Intervention"? > Early Intervention... · body · text · 110 tokens · trang [None, None]
- completeness: complete

```text
* Is the term used to describe services and supports available to babies and young children with developmental delays and disabilities and their families.

* May include speech therapy, physical therapy, occupational therapy, and other types of therapies or services based on the needs of the child and family.

* Can have a significant impact on a child's ability to learn new skills and overcome challenges and can increase success in school and life.

* Programs are available in every state and territory. These publicly funded programs provide services for free or at reduced cost for any child who is eligible.
```

### NIH-NIMH-MEDICATIONS@snapshot-20261017-265ac64c9bc6#section_v1#0004
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

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v1#0011
- section: Results > Psychiatric Comorbidities in Children and Adolescents With Autism Spectrum Disorders · results · text · 139 tokens · trang [None, None]
- completeness: references_missing_component — Đoạn này nhắc tới hình/phụ lục/media không có ở dạng văn bản. Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×3, supplementary-material×3.

```text
Random effect analysis for each comorbidity in all pediatric populations, children and adolescents, in addition to heterogeneity for each analysis can be found in Table 1. Prevalence of ID in all pediatric populations was found as 22.9% (95% CI: 17.7- 29.2) (Figure 2). Prevalence of ADHD in all pediatric populations was found as 26.2% (Figure 3) and prevalence of anxiety disorders in all pediatric populations was found as 11.1% (Figure 4). All statistical analysis groups showed high heterogeneity as shown by I value higher than 84.
```

### ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v1#0012
- section: Results > Psychiatric Comorbidities in Children and Adolescents With Autism Spectrum Disorders · results · table · 549 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: graphic×4, media×3, supplementary-material×3.

```text
TABLE 1
Population-based psychiatric comorbidity studies in children and adolescents with autism spectrum disorders.
 |  |  |  |  | Heterogeneity analysis
Comorbidity | Study Population | Number of study groups | Total number of patients | Prevalence (95% CI) | Heterogeneity I2 | Cochran Q, p value
Intellectual disability | All pediatric population | 33 | 136155 | 22.9 (17.7- 29.2) | 99.76 | 13430, < 0.001
 | Children | 22 | 58849 | 21.4 (15.2- 29.2) | 99.57 | 4886, < 0.001
 | Adolescent | 4 | 35540 | 15.6 (5.8- 35.8) | 99.91 | 3502, < 0.001
ADHD | All pediatric population | 21 | 126951 | 26.2 (22-31) | 99.72 | 7164, < 0.001
 | Children | 10 | 49617 | 18.4 (12.3- 26.6) | 99.76 | 3716, < 0.001
 | Adolescent | 3 | 32163 | 35.4 (21.9-51.7) | 99.86 | 1477, < 0.001
Anxiety disorders | All pediatric population | 19 | 97791 | 11.1 (8.6-14.1) | 99.56 | 4117, < 0.001
 | Children | 11 | 51688 | 7.8 (5.3- 11.3) | 99.4 | 1667, < 0.001
 | Adolescent | 5 | 38746 | 21.5 (14-31.6) | 99.73 | 1468, < 0.001
```

### NIHR-SENITA-2022@Health Technology Assessment 26(29), June 2022; PDF acquired 2026-10-30#section_v1#0095
- section: (không có heading) · body · text · 284 tokens · trang [67, 67]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: figures×1, pdf_layout×1.

```text
Each clinic was also assessed for suitability (of environment and equipment) prior to participant recruitment.

23 Sample size assumptions To confirm the accuracy of the sample size calculation and other features of our proposed design, we obtained an estimate of the following: the proportion of participants providing primary outcome data, the SD of the ABC-I 67 at the primary outcome time point (i.e. 6 months) in both trial arms, and the intracluster correlation coefficient (ICC) of therapists within participants for the ABC-I at the primary outcome time point (intervention arm only). DOI: 10.3310/TQGE0020 Health Technology Assessment 2022 Vol. 26 No. 29 Copyright © 2022 Randell et al. This work was produced by Randell et al. under the terms of a commissioning contract issued by the Secretary of State for Health and Social Care. This is an Open Access publication distributed under the terms of the Creative Commons Attribution CC BY 4.0 licence, which permits unrestricted use, distribution, reproduction and adaption in any medium and for any purpose provided that it is properly attributed. See: https://creativecommons.org/licenses/by/4.0/. For attribution the title, original author(s), the publication source – NIHR Journals Library, and the DOI of the publication must be cited. 37
```

### WHO-CST-INTRO-2022@2022 English edition#section_v1#0006
- section: (không có heading) · body · text · 600 tokens · trang [None, None]
- completeness: document_has_gaps — Tài liệu gốc có phần chưa chuyển thành văn bản: pdf_layout_and_visuals×1.

```text
(Institute of Mental Health, Singapore), Galiya Gaas (Hand in Hand, Kyrgyzstan), Eman Gaber (Cairo University, Egypt), Fe Garcia (World Vision International, USA), Ricardo Garcia (University of Chile, Chile), Jason Garner (Dubai Health Care City,

Introduction vi United Arab Emirates), Tewodros Getye (Nehemiah Autism Center, Ethiopia), Mehdi Ghanadzade (VRF Institute, the Islamic Republic of Iran), Lucky Ghose (BRAC Centre, Bangladesh), Deepa Grover (UNICEF), Sudhanshu Grover (Action for Autism, India), Fiorella Guerrero (University of Florida, USA), Hailiang Guo (China Women’s Development Foundation, China), Syed Usman Hamdani (Human Development Research Foundation, Pakistan), Charlotte Hanlon (Addis Ababa University, Ethiopia), Sarah Louise Harrison (International Medical Corps, Turkey), Homayoun Hashemi (State Welfare Organization of Iran, the Islamic Republic of Iran), Paola Hebe Jelonche (Fundación Visibilia, Argentina), Rosa Hoekstra (King’s College London, United Kingdom), Maria del Milagro Huaman Lu (Soy Austista y Que!, Peru), Yasmin Hussain (SEAMEO SEN, Malaysia), Judy Hutchings (Bangor University, United Kingdom), Alaa Ibrahim (McGill University, Canada), Ivan Ivanov (Community Support Centre, Bulgaria), Seokyeon Ji (Republic of Korea), Sazlina Kamaralzaman (Universiti Kebangsaan, Malaysia), Tsveta Kamensky (UNICEF Bulgaria), Connie Kasari (University of California, USA), Raheleh Khansari (State Welfare Organization of Iran, the Islamic Republic of Iran), Leekyung Kim (Republic of Korea), Yeni Kim (Republic of Korea), Yongjik Kim (Autism Society of Korea, Republic of Korea), Margarita Kinshina (Ministry of Health, Russian Federation), Phiona Naserian Koyiet (World Vision, Kenya), Vibha Krishnamurthy (Ummeed Child Development Center, India), Kim Kwang-Hee (Republic of Korea), Samer Laila (International Medical Corps, Turkey), Pierina Landolfi (PANAACEA, Argentina), Layma Lankmane (The Way Out Fund, Russian Federation), Janet Lau (University of Hong Kong, China, Hong Kong SAR), Rachel Leung (China, Hong Kong SAR), Janice Light (Penn State University, USA), Miroslava Macheva (Community Centre for Child and Parent Support, Bulgaria), Milena Marinova (UNICEF Bulgaria), Rositsa Markova (Centre for Complex Care for Children with Disabilities and Chronic Conditions, Bulgaria), Helen McConachie (Newcastle University, United Kingdom), Sharynne
```
