import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items_q036 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q036']

item_map = {it['annotation_code']: it['content'] for it in items_q036}

spans = {
    "00B20F2174": "Autism Spectrum Disorders (ASD) are lifelong neurodevelopmental conditions characterized by abnormal social interaction, communication, and behavior.",
    "6679E09530": "Behavioral interventions include specific strategies, based on principles of learning and behavior with the aim of developing positive sleep-related habits and eliminating sleep-interfering behaviors.",
    "492450E61D": "Children (ages 2–17.5 years) with: (1) physician-diagnosed ASD according to ICD-10 or DSM-IV/DSM-5 criteria",
    "7E3D66D1F8": "there is insufficient evidence to draw conclusions on the efficacy of other widespread remedies for sleep problems and its consequences, such as sound-to-sleep mattress, massage, aromatherapy, and special diets.",
    "0A82511BFA": "The use of massage in autistic children with sleep problems is based on theoretical grounds similar to those supporting the use of other sensory interventions",
    "8C1CC70B41": "a preliminary randomized crossover study [56] examined efficacy and tolerability of a mattress-based technology—the STS somatosensory system—in children with ASD and sensory over-responsivity (SOR).",
    "1A9DF9EB5C": "Several studies examined physical activity as a variable that might influence sleep in autistic children.",
    "7B99D2262B": "Extensive analyses of several sources of 5-HTP did not find toxic contaminants or any other significant impurity",
    "67A84DCEA7": "- Bedtime fading. Putting children to bed only when they are drowsy by temporarily shifting bedtime later",
    "6EA4ED0433": "non-pharmacological intervention is the preferred first treatment option before initiation of pharmacologic treatments for pediatric insomnia [15]. Parents should be provided with basic information regarding sleep hygiene",
    "B8C96D6A8C": "A systematic review and meta-analysis conducted by Cuomo et al[79] concluded that sleep hygiene should be the initial recommendation provided to parents, along with behavioral interventions",
    "DFF27FBC74": "Sleep pills should be considered to be an additional treatment option to improve sleep in children when non-pharmacological interventions are unsuccessful or partially successful.",
    "2EEA6B31C9": "data correlating ferritin concentration with sleep parameters in autistic children are unclear and sometimes conflicting",
    "F40F6C1F1F": "Behavioral interventions and parent sleep education represent the first line in managing sleep disturbances in children with ASD.",
    "68A0608375": "Therefore, it is often easier and more acceptable for parents to associate sleep education with behavioral gradual interventions",
    "62A647E795": "A recent RCT assessed the efficacy of a structured yoga intervention for sleep, gastrointestinal and behavioral problems in a cohort of children with ASD",
    "5E7BCC96AD": "children with ASD and comorbid sleep-onset delay showed genetic abnormalities in the metabolic pathway of melatonin",
    "BCAB4AFE64": "Tentative treatments with multivitamin and mineral supplements for sleep problems have also been carried out",
    "C94A63E52A": "the prolonged release formulation which releases melatonin throughout the night appears to be effective in improving maintenance",
    "1C8E1CB258": "Only a weak effect was found for SE, as several the studies yield negative results for this parameter",
    "B8997A47A1": "brainsci-10-00441-t002_Table 2Table 2\nEvidence-based pediatric sleep practice recommendations of the ‘ABCs of SLEEPING’ mnemonic.",
    "8879804D59": "Only one clinical trial was carried out to evaluate the effects of aromatherapy on sleep in children with ASD",
    "11E26A2609": "Non-pharmacological and oral over-the-counter treatments are the preferred options for clinicians and caregivers, due to the concerns about the safety and tolerance of long-term prescription sleep medication in children.",
    "91A5CA132B": "Parent sleep education has been found to be effective in the general pediatric population [17], and in small samples of children with ASD [18], being cost-effective and easy to administer.",
    "0C373025FF": "The presence of sleep problems is associated with lower levels of social cognition, daily living skills, and GIS",
    "C803B91A60": "Table 1 ICSD-3 Classification of sleep disorders in children with ASD including descriptions and evidence",
    "8AF89C3E0B": "brainsci-10-00441-t001_Table 1Table 1\nStepwise approach to sleep disturbances in children. Adapted from Howlett et al. (2020) [10]",
    "148569B94B": "In long-term studies (up to 104 weeks) no significant adverse event has been reported, excluding also relevant consequences on pubertal development",
    "8A2D29A0ED": "Weighted blankets and vests are a widespread non-traditional treatment for sleep disturbances in children with ASD.",
    "BF0501A78B": "A solution containing melatonin, Trp and vitamin B6 proved to be significantly more effective than melatonin alone in reducing the sleep-onset delay",
    "3920769BA3": "This study consists of a narrative review of the literature. Extensive literature searches were conducted",
    "A5A8352F43": "Sleep is fundamental in typical development and plays a vital role in the physical and cognitive maturation of children."
}

for code, span in spans.items():
    if span not in item_map[code]:
        print(f"FAILED: {code} -> {span[:30]}...")
    else:
        print(f"OK: {code} (len {len(span)})")

