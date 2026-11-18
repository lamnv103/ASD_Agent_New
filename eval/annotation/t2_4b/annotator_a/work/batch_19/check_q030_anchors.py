import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl', 'r', encoding='utf-8') as f:
    items_q030 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q030']

item_map = {it['annotation_code']: it['content'] for it in items_q030}

# Candidate annotations for q030
# Question: Trẻ tự kỷ có hay gặp vấn đề tiêu hóa không?

test_spans = {
    "D9C4BB20B8": "At least one severe GI symptom or FS in 40.5% of participants.",
    "2D24400159": "Neumeyer et al. [47] found that constipation correlated with sleep disorders in younger children",
    "F862F73D3C": "Babinska et al. [24] found GIS more common in girls with ASD than in boys (97.1% to 87.6% 2 = 13.57, p = 0.009), and 70.6% of girls and 44.5% of boys experienced GIS several times weekly or every day.",
    "661C284A98": "Increased rates of constipation are also likely affected by food selectivity in this population, as dietary patterns in autism are frequently characterized by minimal intake of fiber-containing foods",
    "12781F13D2": "ASD + GIS associated with more severe ASD core symptoms than those without GIS.",
    "8432E3AAC9": "Sign more sleep disorder s/s for children with GI problems (64.1%; 150/234) than for those without GI problems (50.8%; 156/307).",
    "3853A5AC6A": "Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors",
    "5880ACC3B2": "GI abnormalities in 53.9%. In the gluten-free diet group, the prevalence of GIS decreased significantly to 17.10%.",
    "0FF9B42FD6": "Significant improvements in constipation, diarrhea, indigestion, and abdominal pain.",
    "0D00A7252C": "Preschool children with ASD with GIS were found to have substantially more internalizing and externalizing symptoms, significantly different emotional/behavioral problems, and restrictive/repetitive behaviors than those without GIS",
    "6192667D7F": "GIS are experienced by between 9 and 91% of children with ASD, and individuals with GIS have a lower quality of life compared to that of those with no GIS",
    "221868F75F": "Challenging behaviors are common, and they occur in between 40% and 65% of children with ASD who have at least one GIS",
    "8272CD28A0": "GI problems are frequently reported among autistic children. These conditions contribute significantly to the disease burden associated with autism, though estimates of their prevalence vary substantially due to differences in sampling and measurement",
    "434A3E2846": "The research reviewed on GIS and sleep problems concurs with previous work that sleep problems are common and are associated with GIS",
    "A85CA5F1B9": "the diet was effective in improving the behaviors of children with ASD showing gastrointestinal symptoms (in particular, constipation and diarrhea)",
    "7E338C45C8": "Integrated microbiome–metabolome analyses (fecal SCFAs, bile acids, aromatic amino acid catabolites) reveal distinct clusters in ASD that associate with GI symptoms and adaptive behavior",
    "DF77CECB38": "Studies vary regarding the proportion of children with ASD in samples reported to experience at least one GIS. The prevalence of GIS in autistic samples has been reported to be 30–37.4% [30,59] and 82.4% in the previous three months",
    "A87A62B77A": "Higher prevalence GIS in autistic girls than boys. High rates food selectivity 69.1% and mealtime difficulties 64.3%.",
    "CD9ABCBC0D": "The ASD GI group produced increased mucosa-relevant cytokines compared to ASD no GI group.",
    "F5C448B082": "Review of the scientific literature does indicate that a greater risk for GI concerns (e.g., abdominal pain, diarrhea, constipation) exists in these patients, though the etiology of these observations remains unclear.",
    "926C3C2DAE": "The presence of challenging behaviors may reflect the expression of abdominal discomfort in preschool children with ASD",
    "206C64A381": "The results showed the microbiota composition of the children with GIS differed from that of those without GIS and they produced increased levels of mucosa-relevant cytokines.",
    "91297D9B52": "food refusal was associated with lower BMI, sensory issues, and dysfunctional behavior. They concluded that food selectivity involves GIS, individual hypersensitivity, parental behavior, and environmental factors.",
    "CD3D8A3776": "Key factors and their association to GIS.\n| Relationship | Factor |\n|---|---|\n| No Association | Age [8,14,24] |\n| Contradictory Evidence | Positive Association [47] | Language and Communication Ability |\n| No Association [49] |\n| Positive Association [36,40,44,50] | ASD Severity",
    "EE6188D2E1": "However, the etiology of GIS in ASD remains poorly understood [14]. A detailed understanding of the nature of GIS and how they are associated with co-occurring conditions is required to facilitate the diagnosis of ASD and the treatment of GIS",
    "6DE642F3A5": "Food selectivity has been associated with the presence of at least one GIS, higher levels of SIB, and anxiety problems",
    "AB7EB0D26C": "We note a significant need for increased methodological rigor when defining and assessing GI symptoms in autistic patients.",
    "45B886E05B": "The most common GI concerns among autistic individuals include constipation, diarrhea, and abdominal pain, all of which have been found to be more common among autistic children compared to neurotypical peers",
    "AE4DB20CAF": "ASD children with GIS had more anxiety problems, somatic complaints, externalizing, and total problems than those without GIS.",
    "5A07ACB701": "Symptoms affecting the lower GI tract include constipation, diarrhea, and pain on stooling. Constipation occurred in 22.1–24.1% of children with ASD in some samples [46,48] and 47.1–65% in other samples"
}

for code, span in test_spans.items():
    if code not in item_map:
        print(f"MISSING: {code}")
    elif span not in item_map[code]:
        print(f"SPAN NOT FOUND: {code} -> {span[:30]}...")
    else:
        print(f"OK: {code} (len {len(span)})")

