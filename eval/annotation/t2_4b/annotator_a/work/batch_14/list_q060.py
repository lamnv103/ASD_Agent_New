import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q060':
            cands.append(obj)

for i, c in enumerate(cands):
    print(f"[{i+1:02d}] {c['annotation_code']}: {c.get('document_title','')} | {c.get('section','')}")

