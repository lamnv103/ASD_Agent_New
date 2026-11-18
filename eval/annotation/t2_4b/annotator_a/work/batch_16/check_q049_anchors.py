import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q049':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'FD25F8AA2C': 'Based on the review, the findings for maternal outcomes',
    'DCF6057E3D': 'based on other WHO guidelines and statements',
    'E749CFCA70': 'five areas for development of recommendations to improve ECD outcomes:',
    '1984C117D6': 'Evidence and recommendations',
    '361CC4B3C8': 'Key questions',
    '3EF7AA5FA3': 'Caregiving interventions to support early child development in the first three years of life',
    '562D186B27': 'likely to be affected by the recommendations will be specifically reviewed',
    '1C8375B813': 'This guideline provides global, evidence-informed recommendations on improving ECD.',
    'D4EC3BF01D': 'The recommendation reflects the evidence demonstrating the efficacy of int',
    'AE7A946933': 'This guideline contains recommendations for a specific high-risk population',
    '5589C37261': 'WHO recommendations for improving infant and child health are included in',
    '17EDB88FFE': 'Summary of the considerations of the members of the GDG for determining the direction and strength',
    '41BF54556C': 'WHO recommendations for improving infant and child health are included in',
    '714C3F1BFF': 'This guideline directly affects all parents and primary caregivers',
    'FEF56568A5': 'The discussion points around each of the key questions are presented',
    'BE9B0C2F91': 'there are presently no WHO recommendations focussed on ECD-specific interventions',
    'D0E0652381': '“Care for child development” recommends play and communication activities for families to stimulate',
    'D8486E48B2': 'This publication recommends that nurses work in partnership with families, teach caregi',
    '03FC082C1C': 'In order to improve early childhood development, WHO recommends: All infants and children should receive responsive care',
    '1D823B0DC1': 'provides global, evidenceinformed recommendations on approaches to improve ECD',
    '41B41C1F77': 'Recommendations address timing, number and place of postnatal contacts',
    '658D04AABA': 'provide a comprehensive global review of the effectiveness of parenting interventions',
    '295BC64679': 'Feasibility The group concluded that it was probably feasible to implement the interventions.',
    'D39D6156DF': 'intervention packages is recommended in the literature',
    '1BCE9C1A5F': 'The recommendation reflects the evidence which demonstrates the efficacy o',
}

all_ok = True
for code, anchor in anchors.items():
    c = content_map[code]
    if anchor not in c:
        print(f"FAILED: {code}")
        all_ok = False
    else:
        idx = c.find(anchor)
        sub = c[idx:idx+200]
        if '\n' in sub:
            sub = sub.split('\n')[0].strip()
        if len(sub) == 0:
            print(f"EMPTY SPAN: {code}")
            all_ok = False
        elif len(sub) > 250:
            print(f"TOO LONG: {code} ({len(sub)})")
            all_ok = False

print(f"All anchors valid? {all_ok}")
