import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_13.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q057':
            cands.append(obj)

for i, c in enumerate(cands):
    print(f"=== {i+1}: {c['annotation_code']} ===")
    print(c['content'][:300] + ('...' if len(c['content']) > 300 else ''))
    print()

