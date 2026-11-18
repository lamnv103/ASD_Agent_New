import json

found = False
with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if 'stem' in obj['content'].lower() or 'tế bào gốc' in obj['content'].lower():
            print(f"Found in {obj['annotation_code']} ({obj['question_id']})")
            found = True
if not found:
    print('None found in entire batch 17!')

