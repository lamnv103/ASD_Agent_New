import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl', 'r', encoding='utf-8') as f:
    items_q027 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q027']

print(f"Total q027 items: {len(items_q027)}")
for i, it in enumerate(items_q027):
    code = it['annotation_code']
    text = it['content'].replace('\n', ' ')
    print(f"[{i+1}] {code} | {text[:120]}...")

