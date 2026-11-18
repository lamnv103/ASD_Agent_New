import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q018':
            cands.append(obj)

print(f"Total q018 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_sst = any(k in text for k in ['social skills', 'kỹ năng xã hội', 'adolescent', 'thiếu niên', 'youth', 'peer', 'social intervention'])
    print(f"[{i+1:02d}] {c['annotation_code']} | sst:{has_sst} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")

