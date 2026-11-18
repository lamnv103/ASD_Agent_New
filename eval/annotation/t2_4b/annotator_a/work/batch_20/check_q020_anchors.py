import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items_q020 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q020']

item_map = {it['annotation_code']: it['content'] for it in items_q020}

# Question q020: Trẻ tự kỷ kén ăn nghiêm trọng thì đánh giá và can thiệp thế nào?
# This question asks about BOTH assessment and intervention for severe food selectivity in autistic children.
# The article "Food Selectivity in Children with Autism: Guidelines for Assessment and Clinical Interventions" covers this thoroughly:
# Assessment: medical/GI, nutritional (food diary, FFQ, BMI), questionnaires (BAMBI, BPFAS), direct observation.
# Interventions: behavioral (reinforcement, shaping, stimulus fading, non-removal of spoon), sensory, parent training, multidisciplinary.

test_spans = {
    "85543642DE": "Exploring feeding issues in ASD, we can observe either medical or sensorial/behavioral characteristics which influence food refusal or restricted food preferences of autistic children during mealtimes.",
    "451A48AF6C": "these clusters examined by authors permit clinicians to immediately detect the core symptom of a child along with the correlated variables (nutritional, medical, sensorial, behavioral, and environmental).",
    "FD9ECCFAD5": "physical changes in foods can contribute to improving sensory processing and the consequent intake of foods otherwise rejected.",
    "D120F43B7D": "The Behavior Pediatric Feeding Assessment Scale (BPFAS), the original instrument made up of 35 items, allows the calculation of four scores, relating to the four subscales of which it is composed",
    "089400003D": "Firstly, before implementing an educational intervention, the following intersected aspects such as GID, assumed foods (food diary), and growth curves as suggested by Badalyan and Schwartz [59], should be addressed.",
    "B0C8BF9CA0": "using individualized reinforcement and hierarchical exposure can increase flexibility in food intake in children with ASD.",
    "F1A8CED362": "the child learns to avoid undesirable foods by emitting challenging behaviors, as well as the parents involuntarily maintaining such behaviors by presenting only the preferred food at mealtime",
    "A6DB37EB0B": "When applied to the feeding behaviors, during the shaping procedure the tutor should gradually reinforce the successive approximations of the target feeding behavior, such as: placing food in the spoon, food near the lips",
    "BCBFA06D83": "Concerning the causes of food selectivity in children with ASD, scientists have examined diverse dimensions of altering feeding behaviors. As mentioned above, the importance of motor conditions and/or gastrointestinal complications should be addressed",
    "8A3011617F": "The Brief Autism Mealtime Behavior Inventory (BAMBI) is a tool composed of 18 items to identify the presence of aggressive and destructive behaviors during meals",
    "62369EB295": "classification in subgroups could permit clinical staff to assess the efficacy of treatment with respect to the children’s profile in the baseline (tailored treatment).",
    "58EB694D1D": "Direct measurement regards the behavior exhibited by children during mealtimes.",
    "A184E2E3BC": "food selectivity is a problem common in many children, in particular those with autism spectrum disorders.",
    "FDE1B38BC1": "In the section concerning behavioral interventions, we have listed diverse, effective techniques based on the principles of Applied Behavior Analysis (reinforcement, shaping, stimulus fading, escape extinction,",
    "F681DFCE9B": "This information could help clinicians to identify the target behaviors of the intervention, along with maintaining variables and setting events for the challenging behaviors.",
    "1D67FB6B70": "the clinicians could enrich their anamnesis of children using some direct and indirect measurement tools: (1) food diary, (2) video recording of mealtime routines, (3) parent interviews, and (4) standardized questionnaires.",
    "BD8FBA235E": "In the new edition of DSM-5 (https://www.ncbi.nlm.nih.gov/books/NBK519712/table/ch3.t18/, accessed on 9 February 2023), nutrition and eating disorders during childhood include pica, avoidant/restrictive disorder of food intake",
    "C14E67B5A5": "The clinical management of children with ASD presenting food selectivity requires a preliminary nutritional and behavioral assessment, followed by a multidisciplinary intervention.",
    "82DEF08DC1": "Concerning the nutritional assessment for children with ASD, clinicians should detect the causal nutritional deficiencies, as well as monitor the growth curves of the children over time.",
    "25B8597E69": "clinical interventions for children, adolescents, and young adults with autism have demonstrated that parent-mediated interventions, delivered face-to-face or via telehealth, are effective in improving feeding problems",
    "FB71AF5140": "The treatment of eating disorders in children is complex and necessarily multidisciplinary.",
    "2845638432": "Parent-reported food allergies were nearly 2.5 times more common in children with ASD",
    "5A07DD3133": "families can reduce the feeding issues of children (overweight, intake of junk food, and other eating disorders) increasing the consumption of healthy foods.",
    "180A3D6142": "clinicians have to examine if the feeding problem reports an organic nature or a behavioral one.",
    "0698F0B688": "Descriptions of some main questionnaires regarding feeding behaviors in children.",
    "38208CBA60": "the frequency of selective eating and nutritional deficiency was studied among 22 children with ASD compared with TDC",
    "DFE346D5D3": "parent training could be effective in improving eating habits and parent–child relationships during mealtime routines.",
    "B53DD3B76D": "This narrative review aimed to provide a comprehensive guide on the assessment and intervention for food selectivity in children with ASD.",
    "75C22FFE9E": "parent training should be recommended to reduce mealtime problem behaviors and improve nutritional intake.",
    "5AA491A7CB": "The current narrative review sheds light on how to assess food selectivity in children with ASD and how to implement clinical interventions.",
    "3BAC728961": "Representative items of the educational caregiver feeding practices questionnaire",
    "0840EF7619": "Parent training resulted in significant reductions in disruptive mealtime behavior and improvements in food acceptance."
}

for code, span in test_spans.items():
    if code not in item_map:
        print(f"MISSING: {code}")
    elif span not in item_map[code]:
        print(f"NOT FOUND: {code} -> {span[:30]}...")
    else:
        print(f"OK: {code} (len {len(span)})")

