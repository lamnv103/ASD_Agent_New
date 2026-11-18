import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_18.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q003':
            cands.append(obj)

print(f"Total q003 cands: {len(cands)}")
for i, c in enumerate(cands):
    text = c['content'].lower()
    has_risk = any(k in text for k in ['risk', 'nguy cơ', 'factor', 'yếu tố', 'cause', 'etiolog', 'nguyên nhân', 'maternal', 'genetic', 'environmental'])
    print(f"[{i+1:02d}] {c['annotation_code']} | risk:{has_risk} | doc:{c.get('document_title','')[:30]} | sec:{c.get('section','')[:30]}")
    if has_risk:
        for kw in ['risk factor', 'risk', 'cause', 'etiolog', 'nguy cơ']:
            idx = text.find(kw)
            if idx != -1:
                snip = c['content'][max(0, idx-30):min(len(c['content']), idx+70)].replace('\n', ' ')
                print(f"    [{kw}] ...{snip}...")
                break

