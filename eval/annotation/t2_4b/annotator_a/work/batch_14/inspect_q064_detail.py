import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q064':
            cands.append(obj)

inspect_codes = ['4D2A261C92', '754EF61E05', 'F942A0E2E3', 'D74BBD0072', '29E2726699', 'A6DB820AC7']
for c in cands:
    if c['annotation_code'] in inspect_codes:
        print(f"=== {c['annotation_code']} | {c.get('section','')} ===")
        print(c['content'])
        print("="*70)

