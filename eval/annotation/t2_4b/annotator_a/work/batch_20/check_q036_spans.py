import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items_q036 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q036']

item_map = {it['annotation_code']: it['content'] for it in items_q036}

# Question q036: Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?
# Non-pharmacological management of sleep disturbances in ASD.
# Key paper: "Sleeping without Prescription: Management of Sleep Disturbances in Children with Autism with Non-Pharmacological Strategies and Over-the-Counter Treatments"
# Non-pharmacological approaches:
# - Sleep hygiene & parent education (regular bedtime routine, bedtime fading, stimulus control)
# - Behavioral interventions (standard extinction, graduated extinction, positive bedtime routine)
# - Physical activity / exercise, yoga, massage therapy
# - Sensory adaptations (mattress, weighted blankets - note evidence is mixed)

test_spans = {
    "00B20F2174": "Non-pharmacological strategies (such as sleep hygiene and behavioral interventions) and over-the-counter (OTC) drugs (such as melatonin) are the most frequent initial approaches",
    "6679E09530": "Behavioral interventions include specific strategies, based on principles of learning and behavior which aim at modifying maladaptive behaviors related to sleep.",
    "7E3D66D1F8": "there is insufficient evidence to draw conclusions on the efficacy of other widespread remedies (such as weighted blankets, sound-to-sleep mattress, aromatherapy, and special diets).",
    "0A82511BFA": "The use of massage in autistic children with sleep problems is based on theoretical grounds similar to other sensory interventions, since sensory processing dysfunctions have been demonstrated in up to 90% of children with ASD",
    "8C1CC70B41": "a preliminary randomized crossover study [56] examined efficacy and tolerability of a mattress that used gentle sound and vibration to promote sleep in children with ASD and sensory over-responsivity.",
    "1A9DF9EB5C": "Several studies examined physical activity as a variable that might influence sleep in autistic children.",
    "67A84DCEA7": "- Bedtime fading: The goal of bedtime fading is to produce a state of sleepiness by adjusting bedtime to the child’s natural sleep latency. - Standard extinction: It is based on the premise that crying, tantrums, calling out at bedtime",
    "6EA4ED0433": "non-pharmacological intervention is the preferred first treatment choice for pediatric sleep disorders [15]. Parents should be provided with basic information regarding sleep hygiene, as well as an explanation of sleep problems",
    "B8C96D6A8C": "A systematic review and meta-analysis conducted by Cuomo et al[79] concluded that sleep hygiene should be the initial recommendation provided to parents, along with behavioral interventions",
    "DFF27FBC74": "Sleep hygiene and behavioral interventions are generally recommended as first line treatments, before using prescription sleep medication.",
    "F40F6C1F1F": "Behavioral interventions and parent education are the cornerstones of non-pharmacological management of sleep problems in ASD.",
    "68A0608375": "Therefore, it is often easier and more acceptable for parents to associate sleep education with behavioral interventions, such as positive bedtime routines.",
    "62A647E795": "A recent RCT assessed the efficacy of a structured yoga intervention for sleep, gastrointestinal and core autistic symptoms in children with ASD",
    "B8997A47A1": "Evidence-based pediatric sleep practice recommendations of the American Academy of Neurology (AAN)",
    "8879804D59": "Only one clinical trial was carried out to evaluate the effects of aromatherapy on sleep in children with ASD",
    "11E26A2609": "Given the potential long-term side-effects of drugs, behavioral interventions and non-prescription treatments are often preferred by parents and clinicians.",
    "91A5CA132B": "Parent sleep education has been found to be effective in the general pediatric population [17], and can be delivered in a variety of ways, including group sessions, individual face-to-face sessions, or via written materials",
    "8AF89C3E0B": "Stepwise approach to sleep disturbances in children. Adapted from Cuomo et al.",
    "8A2D29A0ED": "Weighted blankets and vests are a widespread non-traditional treatment for sleep disturbances in children with ASD.",
    "3920769BA3": "This narrative review focuses on non-pharmacological interventions and over-the-counter treatments for sleep disturbances in ASD.",
    "A5A8352F43": "Behavioral interventions, sleep hygiene education, and cognitive behavioral therapy for insomnia (CBT-I) have demonstrated efficacy in improving sleep in children with autism."
}

for code, span in test_spans.items():
    if span not in item_map[code]:
        print(f"FAILED: {code}")
    else:
        print(f"OK: {code} (len {len(span)})")

