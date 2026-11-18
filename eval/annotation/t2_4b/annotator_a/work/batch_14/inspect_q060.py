import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q060':
            cands.append(obj)

print(f"Total q060 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_diet = any(k in text for k in ['gluten', 'casein', 'diet', 'ăn kiêng', 'dinh dưỡng', 'gfcf', 'food selectivity', 'gut'])
    print(f"[{i+1:02d}] {c['annotation_code']} | diet:{has_diet} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")
    if has_diet:
        # print snippet
        for kw in ['gluten', 'casein', 'gfcf', 'diet']:
            idx = text.find(kw)
            if idx != -1:
                snip = c['content'][max(0, idx-40):min(len(c['content']), idx+80)].replace('\n', ' ')
                print(f"     [{kw}] ...{snip}...")
                break

