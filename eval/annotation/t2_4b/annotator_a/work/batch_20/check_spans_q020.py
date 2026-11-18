import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items_q020 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q020']

item_map = {it['annotation_code']: it['content'] for it in items_q020}

spans = {
    "A184E2E3BC": "Concluding, food selectivity is a problem common in many children, in particular those with autism symptoms. Therefore, families along with clinical staff should establish concurrent causes of feeding issues in their child through a correct assessmen",
    "FDE1B38BC1": "In the section concerning behavioral interventions, we have listed diverse, effective techniques based on ABA principles displaying some examples of their implementation",
    "F681DFCE9B": "This information could help clinicians to identify the target behaviors of the intervention, along with the contextual factors that might constitute specific advantages and possible barriers to adequate food intake.",
    "1D67FB6B70": "Starting with interviews of families, the clinicians could enrich their anamnesis of children using well-structured instruments such as questionnaires and measure scales.",
    "C14E67B5A5": "Seventy-eight percent consumed a diet at risk of five or more inadequacies. Risk for specific inadequacies included vitamin D (97% of the sample), fiber (91%), vitamin E (83%), and calcium (71%).",
    "82DEF08DC1": "Concerning the nutritional assessment for children with ASD, clinicians should detect the causal nutritional inadequacies connected to the restricted intake",
    "25B8597E69": "The clinical interventions for children, adolescents, and young adults with autism have demonstrated gains in different developmental domains where parent inclusion and related training have been largely suggested and recommended",
    "180A3D6142": "Conversely, a severe symptom of food refusal could be characterized by dysfunctional behaviors that have the function to obtain social attention or escape [14].",
    "0698F0B688": "ijerph-20-05092-t001_Table 1Table 1 Descriptions of some main questionnaires regarding feeding behaviors.",
    "38208CBA60": "Firstly, the frequency of selective eating and nutritional deficiency was studied among 22 children with autism and an age-matched TDC group. Children with autism ate fewer foods on average than TDC.",
    "DFE346D5D3": "Since a restricted diet can influence the nutritional intake of children, causing significant stress to the families [32,51], feeding problems should be considered as a severe burden for families and therapists",
    "B53DD3B76D": "Autisms Spectrum Disorders (ASD) are characterized by core symptoms (social communication and restricted and repetitive behaviors) and related comorbidities, including sensory anomalies, feeding issues, and challenging behaviors.",
    "75C22FFE9E": "Generally, parental involvement can change depending on familiar resources and the type of the intervention (e.g., behavior-based or sensory-based approaches) and providers (e.g., occupational therapists, psychologists, or speech therapists).",
    "5AA491A7CB": "The current narrative review sheds light on how to assess food selectivity in children with ASD and how to plan effective and individualized interventions.",
    "3BAC728961": "ijerph-20-05092-t002_Table 2Table 2 Representative items of the educational caregiver feeding practices.",
    "0840EF7619": "Results comparing time one to time two indicated no change in food selectivity level and a stable, significant relationship between food selectivity and sensory over-responsiveness"
}

for code, span in spans.items():
    if span not in item_map[code]:
        print(f"FAILED: {code}")
    else:
        print(f"OK: {code} (len {len(span)})")

