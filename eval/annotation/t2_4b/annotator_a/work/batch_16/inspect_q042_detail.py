import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q042':
            cands.append(obj)

test_codes = ['B753B846F9', '34E03728B1', 'DF8A2F72E8', '8339FB9707', '2BDD94BC08', 'CEBA798D0A', '5818E33BAF', '463BC15E4B', 'ED2A2CB334']
for c in cands:
    if c['annotation_code'] in test_codes:
        print(f"=== {c['annotation_code']} | {c.get('document_title','')} | {c.get('section','')} ===")
        print(c['content'][:600])
        print("="*70)

