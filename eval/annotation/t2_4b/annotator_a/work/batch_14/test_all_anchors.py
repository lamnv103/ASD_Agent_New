import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            content_map[obj['annotation_code']] = obj['content']

# Test anchor function:
def test_anchor(code, anchor):
    c = content_map[code]
    if anchor not in c:
        print(f"FAILED ANCHOR in {code}: {anchor[:40]}")
        # print snippet
        print(f"  Available content: {c[:150]}")
        return False
    return True

