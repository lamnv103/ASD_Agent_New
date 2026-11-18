import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

cands = []
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            cands.append(obj)

for i, c in enumerate(cands):
    text = c['content']
    # check for both home and school in text
    has_home = 'home' in text.lower() or 'nhà' in text.lower()
    has_school = 'school' in text.lower() or 'trường' in text.lower() or 'classroom' in text.lower()
    has_parent = 'parent' in text.lower() or 'caregiver' in text.lower() or 'cha mẹ' in text.lower()
    print(f"[{i+1:02d}] {c['annotation_code']} | home:{has_home} | school:{has_school} | parent:{has_parent} | len:{len(text)}")

