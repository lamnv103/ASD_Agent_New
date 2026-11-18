import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            cands.append(obj)

for i, c in enumerate(cands):
    print(f"ID: {i+1} | Code: {c['annotation_code']}")
    print(f"Doc: {c.get('document_title','')}")
    print(f"Sec: {c.get('section','')}")
    text = c['content'].strip()
    first_few = '\n'.join([line for line in text.split('\n') if line.strip()][:4])
    print(f"Text sample:\n{first_few[:300]}")
    print("="*60)

