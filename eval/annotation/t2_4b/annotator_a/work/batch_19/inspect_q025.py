import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q025':
            cands.append(obj)

print(f"Total q025 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_mchat = any(k in text for k in ['m-chat', 'mchat', 'modified checklist for autism in toddlers', 'sensitivity', 'specificity', 'độ nhạy', 'độ đặc hiệu', 'ppv', 'screening'])
    print(f"[{i+1:02d}] {c['annotation_code']} | mchat:{has_mchat} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")
    if has_mchat:
        for kw in ['m-chat', 'mchat', 'modified checklist']:
            idx = text.find(kw)
            if idx != -1:
                snip = c['content'][max(0, idx-30):min(len(c['content']), idx+70)].replace('\n', ' ')
                print(f"    [{kw}] ...{snip}...")
                break

