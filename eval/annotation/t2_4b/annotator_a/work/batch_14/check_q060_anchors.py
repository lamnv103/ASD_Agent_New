import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q060':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'B304E1BF52': 'Ghalichi et al. [32] conducted a small RCT that investigated the effect of a six-week gluten-free diet on GIS and behavioral indices in children with ASD',
    '793D7B696B': 'some studies have found little evidence of the efficacy of nutritional supplements and dietary therapies',
    '20770E4247': 'subjects followed a diet, mostly based on gluten and milk restriction, including individuals exhibiting food selectivity.',
    '98BC9B2B51': 'Though some studies suggest that autistic children may be at higher risk for gluten sensitivity, lactase deficiencies, and even intestinal inflammation',
    'B0D24992E5': 'with clinical staff if the child assumes a gluten/casein-free diet and if he refuses some ingredients such as legumes, vegetables, and fruit.',
    'F721BC12C7': 'Given the popularity of many of these dietary recommendations among the autism community at large, further investigation is warranted to better validate their use.',
    '9AEEDA1523': 'interventions like elimination diets (e.g., gluten- and casein-free diets), nutritional supplements, enzymes, and antimicrobials',
    'A3CC929567': 'synergistic effect on behavior resulted from the combination of prebiotic and casein/gluten-free exclusion diet.',
    '05765581B4': 'Mulloy et al. [80] conducted a systematic review of GFCF diets when implemented in the treatment of ASD, concluding that the published studies they identified do not support the use of these diets in the treatment of ASD.',
    'D8E99B679D': 'Several studies highlighted that children with ASD may show food selectivity and inadequate nutrient intake.',
    'DC453289E2': 'Investigated the effect of a gluten-free diet on GIS and behavior in ASD children.',
    '04B448BCBD': 'food selectivity in this population, as dietary patterns in autism are frequently characterized by minimal intake of fiber-rich foods',
}

for code, anchor in anchors.items():
    c = content_map[code]
    if anchor not in c:
        print(f"FAILED: {code}")
        # find matching line
        for l in c.split('\n'):
            if any(w in l.lower() for w in ['gluten', 'diet', 'casein']):
                print(f"   cand line: '{l[:100]}'")
    else:
        idx = c.find(anchor)
        sub = c[idx:idx+200]
        if '\n' in sub:
            sub = sub.split('\n')[0].strip()
        print(f"OK: {code} (len {len(sub)})")

