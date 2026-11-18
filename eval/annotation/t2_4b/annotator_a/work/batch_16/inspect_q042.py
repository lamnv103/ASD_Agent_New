import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q042':
            cands.append(obj)

print(f"Total q042 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_asi = any(k in text for k in ['ayres', 'asi', 'sensory integration', 'sensory-based', 'sbi'])
    print(f"[{i+1:02d}] {c['annotation_code']} | asi:{has_asi} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")

