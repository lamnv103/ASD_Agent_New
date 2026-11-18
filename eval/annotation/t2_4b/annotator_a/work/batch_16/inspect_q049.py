import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q049':
            cands.append(obj)

print(f"Total q049 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_who = 'who' in text or 'tổ chức y tế thế giới' in text
    has_rec = any(k in text for k in ['recommend', 'khuyến nghị', 'guideline', 'hướng dẫn', 'early childhood development', 'ecd', 'responsive care'])
    print(f"[{i+1:02d}] {c['annotation_code']} | who:{has_who} | rec:{has_rec} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")
    if has_who and has_rec:
        for kw in ['recommend', 'guideline', 'early childhood']:
            idx = text.find(kw)
            if idx != -1:
                snip = c['content'][max(0, idx-30):min(len(c['content']), idx+70)].replace('\n', ' ')
                print(f"    [{kw}] ...{snip}...")
                break

