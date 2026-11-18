import json
import os

os.makedirs('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_18', exist_ok=True)

questions = {}
with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_18.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        qid = obj['question_id']
        if qid not in questions:
            questions[qid] = {'vi': obj.get('question_vi'), 'items': []}
        questions[qid]['items'].append(obj)

for qid, data in sorted(questions.items()):
    print(f"{qid}: {data['vi']} ({len(data['items'])} items)")
    raw_path = f'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_18/{qid}_raw.txt'
    with open(raw_path, 'w', encoding='utf-8') as f_out:
        f_out.write(f"QUESTION {qid}: {data['vi']}  ({len(data['items'])} candidates)\n\n")
        for i, item in enumerate(data['items']):
            f_out.write(f"### [{i+1}] {item['annotation_code']} | {item.get('document_title','')} | {item.get('section','')} | page {item.get('page','')}\n")
            f_out.write(item['content'].strip() + "\n\n")

