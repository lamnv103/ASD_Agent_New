import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            cands.append(obj)

selected = [0, 3, 5, 8, 9, 14, 15, 17, 21, 23, 24, 27, 31, 33, 34, 36, 43, 48, 49, 50, 52]
for idx in selected:
    c = cands[idx]
    print(f"=== [{idx+1}] {c['annotation_code']} | {c.get('document_title','')} | {c.get('section','')} ===")
    print(c['content'][:500] + '...\n')

