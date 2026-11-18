import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            content_map[obj['annotation_code']] = obj['content']

from make_q054 import raw

for item in raw:
    code = item['code']
    grade = item['grade']
    anchor = item['anchor']
    if grade != 0:
        c = content_map[code]
        if anchor not in c:
            print(f"FAILED: {code} (grade {grade}) - anchor not found: '{anchor[:40]}...'")
            # find good snippet
            lines = [l.strip() for l in c.split('\n') if len(l.strip()) > 30]
            if lines:
                print(f"   Suggestion from text: '{lines[0][:100]}'")
        else:
            idx = c.find(anchor)
            sub = c[idx:idx+200]
            if '\n' in sub:
                sub = sub.split('\n')[0].strip()
            if len(sub) == 0:
                print(f"EMPTY SPAN: {code}")
            elif len(sub) > 250:
                print(f"SPAN TOO LONG ({len(sub)}): {code}")
            else:
                print(f"OK: {code} (len {len(sub)})")

