import json
with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q036']
item_map = {it['annotation_code']: it['content'] for it in items}

failed = ['6679E09530', '7E3D66D1F8', '0A82511BFA', '8C1CC70B41', '67A84DCEA7', '6EA4ED0433', 'B8C96D6A8C', 'DFF27FBC74', '2EEA6B31C9', 'F40F6C1F1F', '62A647E795', 'C94A63E52A', '11E26A2609', '91A5CA132B', 'C803B91A60', '148569B94B', 'BF0501A78B']
for c in failed:
    content = item_map[c]
    # take first non-empty line or substring <= 200 chars
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    span = lines[0][:180]
    print(f'"{c}": {repr(span)},')

