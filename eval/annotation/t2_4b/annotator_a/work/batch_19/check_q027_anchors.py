import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl', 'r', encoding='utf-8') as f:
    items_q027 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q027']

item_map = {it['annotation_code']: it['content'] for it in items_q027}

# Candidate annotations for q027
# Question: Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?
# Criteria: Category A (deficits in social communication/interaction: A1 reciprocity, A2 nonverbal, A3 relationships - all 3 required)
# Category B (restricted, repetitive patterns of behavior, interests, activities: B1 stereotyped/repetitive motor, B2 sameness/routines, B3 fixated interests, B4 sensory - at least 2 required)
# Severity levels 1-3, age of onset / early developmental period, functional impairment.

# Let's check each item:
# [1] E15F37AD7A: mentions Category A (social interaction and communication) and Category B (at least 2 criteria from Category B - Restricted and Reparative Behaviour). Grade: 2.
# [2] 7DD437F629: stigma in Vietnam, not DSM-5 criteria. Grade: 0.
# [3] 8C7B389E73: DSM-5 diagnostic criteria overview: persistent challenges in social communication and interaction across multiple settings and restricted, repetitive patterns of behaviors. Grade: 2.
# [4] 636B19CCDC: randomized trial reporting odds of meeting DSM-5 criteria A1, B1, B4. Mentions specific criteria in passing. Grade: 1.
# [5] 6120526FFF: ADHD and anxiety comorbidity. Grade: 0.
# [6] 4BC0244DB3: ASD defined by social-communication deficits and restricted/repetitive behaviors, mentions DSM-5 allowing comorbid ADHD. Grade: 1.
# [7] 6932932EEF: anxiety and ADHD comorbidities. Grade: 0.
# [8] 8FA463304E: GIS in ASD, gut microbiota. Grade: 0.
# [9] 1B85BCF617: comorbid ADHD and anxiety in ASD. Grade: 0.
# [10] 98EF6A3F2A: copyright / reprints notice. Grade: -1.
# [11] 732C62F9D9: screening tools review, mentions DSM-5 criteria in passing. Grade: 1.
# [12] F0F50C4368: screening tools do not fully align with DSM-5. Grade: 1.
# [13] D131F504D5: table of category counts in chart cache. Grade: 0.
# [14] 41C5A70D36: autoimmune conditions in ASD. Grade: 0.
# [15] C1FF04F071: "In addition to diagnostic tools, the American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD." Mentions DSM-5 provides criteria but doesn't list them. Grade: 1.
# [16] D7BD0DA199: catatonia and behavioral interventions. Grade: 0.
# [17] 97589F5090: explicitly lists all 7 criteria of DSM-5: A1 (deficits in social-emotional reciprocity), A2 (deficits in nonverbal communicative behaviors...), A3 (deficits in developing, maintaining, and understanding relationships), B1 (stereotyped or repetitive motor movements...), B2 (insistence on sameness...), B3 (highly restricted fixated interests...), B4 (hyperreactivity or hyporeactivity sensory input...). Grade: 3!
# [18] 64CF120CE2: details Criterion A (A1, A2, A3) and severity levels 1, 2, 3! Grade: 3!
# [19] 174C35B22F: overview of DSM-5-TR, challenges in social interaction and communication and restricted interests/repetitive behaviors. Grade: 2.
# [20] 9E8FD1CFDE: comparison DSM-IV vs DSM-5, grouping 5 PDDs into ASD. Grade: 1.
# [21] E13F6956C2: key points, mentions DSM-5 provides standardized criteria. Grade: 1.
# [22] 4CF50E1153: Table 1 Diagnostic Criteria of ASD in DSM-5: full list of A1, A2, A3 and B1, B2, B3, B4! Grade: 3!
# [23] 2E6A75C631: inclusion/exclusion criteria for social skills groups. Grade: 0.
# [24] BD2403ADC8: explains DSM-5 criteria structure: consolidation of PDDs, two domains (social communication and restricted/repetitive behaviors), addition of sensory symptoms, severity scale Levels 1-3, and DSM-5-TR requiring all 3 social communication symptoms. Grade: 3!
# [25] 8488D91E82: preemptive intervention clinical trial. Grade: 0.
# [26] 345292C1A4: review of 37 screening tools, mentions DSM-5 specifications. Grade: 1.
# [27] D5472BF1A3: abbreviation list. Grade: 0.
# [28] 925B934DDF: diagnostic criteria note (Criterion E, specifiers: with/without intellectual impairment, language impairment, etc.). Grade: 2.
# [29] 8F03594A70: study on ADHD and anxiety comorbidity. Grade: 0.
# [30] AB14022D41: autism community involvement in research. Grade: 0.
# [31] 6586637843: screening tools compliance with DSM-5. Grade: 1.
# [32] 7508E32FBA: elopement in developmental disabilities. Grade: 0.
# [33] 67E499A230: DSM-5 eating disorders (ARFID). Grade: 0.
# [34] C082447E90: ADHD/anxiety study procedure. Grade: 0.
# [35] F125B9B37A: NIMH overview: according to DSM-5, social communication and interaction difficulty, restricted interests and repetitive behaviors, symptoms affecting functioning. Grade: 2.
# [36] EA3CE1631E: epilepsy and autism. Grade: 0.
# [37] A2A22E1557: KID-SCID instrument for DSM-IV. Grade: 0.
# [38] 60398D00B7: Criterion B (B1, B2, B3, B4) and severity levels 1, 2, 3! Grade: 3!
# [39] 4ED216920C: meta-analysis methodology. Grade: 0.
# [40] 192344232C: anxiety and ADHD in ASD. Grade: 0.
# [41] 79F26D1C52: DSM-IV to DSM-5 transition in screening context. Grade: 1.
# [42] F8BD5B9A56: ADHD prevalence in ASD under DSM-IV vs DSM-5. Grade: 1.
# [43] 02325880DC: Figure 4 count table. Grade: 0.
# [44] 5DF1AA9340: core DSM-5 requirement: persistent deficits in each of 3 areas of social communication and interaction (A.1-A.3) plus at least 2 of 4 types of restricted, repetitive behaviors (B.1-B.4). Grade: 3!
# [45] 33B362108E: meta-analysis inclusion criteria. Grade: 0.

test_spans = {
    "E15F37AD7A": "items in the existing screening methods should cover social interaction and social communication (Category A) in the DSM-5 manual and at least two criteria from Category B (Restricted and Reparative Behaviour).",
    "8C7B389E73": "According to the DSM-5 (APA, 2013), to meet the diagnostic criteria, an individual must exhibit persistent challenges in social communication and interaction across multiple settings and also demonstrate symptoms in the restricted, repetitive patterns",
    "636B19CCDC": "the 7 criteria for ASD (Table 3). A logistic regression analysis incorporating covariates identified reduced odds of meeting DSM-5 criteria A1 among the iBASIS-VIPP group (deficits in social-emotional reciprocity",
    "4BC0244DB3": "Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors",
    "98EF6A3F2A": "The information in this publication is in the public domain and may be reused or copied without permission.",
    "732C62F9D9": "none of the reviews emphasise the importance of the DSM-5 criteria for evaluating the reliability of ASD screening.",
    "F0F50C4368": "the majority of these screening tools do not fully align with the new criteria for ASD developed under the DSM-5. Therefore, the need for revised methods that adhere to the standards of the DSM-5 have arisen.",
    "C1FF04F071": "the American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD.",
    "97589F5090": "these criteria were A1 (deficits in social-emotional reciprocity), A2 (deficits in nonverbal communicative behaviors used for social interaction), A3 (deficits in developing, maintaining, and understanding relationships)",
    "64CF120CE2": "1. Deficits in social-emotional reciprocity, ranging, for example, from abnormal social approach and failure of normal back-and-forth conversation; to reduced sharing of interests, emotions, or affect; to failure to initiate or respond to social",
    "174C35B22F": "Autism Spectrum Disorder (ASD) is a neurodevelopmental condition characterized by challenges in social interaction and communication, and the presence of restricted interests and repetitive behaviors (Diagnostic and Statistical Manual",
    "9E8FD1CFDE": "The most recent version of the DSM (DSM-5) groups the five PDDs, consisting of Asperger syndrome (AS), pervasive development disorder–not otherwise specified (PDD-NOS), Rett syndrome (RS), and childhood disintegrative disorder (CDD), into ASD",
    "E13F6956C2": "The American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD.",
    "4CF50E1153": "Table 1.\nDiagnostic Criteria of Autism Spectrum Disorder in the DSM-5\n| A. Social communication and interaction challenges: |\n| 1. Deficits in social-emotional reciprocity |\n| 2. Deficits in nonverbal communicative behaviors used for social interaction",
    "BD2403ADC8": "the three symptom categories of social impairment, language/communication impairment, and repetitive/restricted behaviors were merged into two symptom domains: persistent deficits in social communication and interaction and restricted",
    "345292C1A4": "the fulfilment of Diagnostic and Statistical Manual of Mental Disorders (DSM-5) specifications",
    "925B934DDF": "Individuals with a well-established DSM-IV diagnosis of autistic disorder, Asperger's disorder, or pervasive developmental disorder not otherwise specified should be given the diagnosis of autism spectrum disorder.",
    "6586637843": "Many of the available screening tools, especially the short versions, comply only partly with the ASD criteria of the DSM-5 introduced in 2013.",
    "F125B9B37A": "According to the *Diagnostic and Statistical Manual of Mental Disorders (DSM-5)*, a guide created by the American Psychiatric Association that health care providers use to diagnose mental disorders and developmental disorders, people with ASD often have:",
    "60398D00B7": "1. Stereotyped or repetitive motor movements, use of objects, or speech (e.g., simple motor stereotypes, lining up toys or flipping objects, echolalia, idiosyncratic phrases).",
    "79F26D1C52": "In 2013, the DSM-IV was revised, which posed a significant challenge to the way individuals are assessed as being on the ASD spectrum and necessitated refinements of existing diagnosis as well as screening techniques.",
    "F8BD5B9A56": "Studies using DSM-IV reported lower rates of ADHD in contrast to ones using DSM-5 criteria.",
    "5DF1AA9340": "To meet diagnostic criteria for ASD according to DSM-5, a child must have persistent deficits in each of three areas of social communication and interaction (see A.1. through A.3. below) plus at least two of four types of restricted, repetitive behaviors",
}

for code, span in test_spans.items():
    if code not in item_map:
        print(f"MISSING CODE: {code}")
    elif span not in item_map[code]:
        print(f"SPAN NOT FOUND IN {code}: {span[:40]}...")
    else:
        print(f"OK: {code} (len {len(span)})")

