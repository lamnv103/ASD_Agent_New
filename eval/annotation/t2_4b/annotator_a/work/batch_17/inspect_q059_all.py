import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q059':
            cands.append(obj)

for i, c in enumerate(cands):
    text = c['content'].lower()
    treat = any(k in text for k in ['treat', 'cure', 'therap', 'chữa', 'điều trị', 'stem', 'cell', 'tế bào', 'gene'])
    print(f"[{i+1:02d}] {c['annotation_code']} | doc:{c.get('document_title','')[:25]} | sec:{c.get('section','')[:25]}")
    lines = [l.strip() for l in c['content'].split('\n') if l.strip()]
    if lines:
        print(f"    first line: {lines[0][:100]}")

