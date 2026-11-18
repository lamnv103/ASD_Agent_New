import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q036']

item_map = {it['annotation_code']: it['content'] for it in items}

# Let's inspect each candidate's exact text for q036
for it in items:
    code = it['annotation_code']
    text = it['content'].replace('\n', ' ')
    print(f"[{code}] {text[:130]}...")

