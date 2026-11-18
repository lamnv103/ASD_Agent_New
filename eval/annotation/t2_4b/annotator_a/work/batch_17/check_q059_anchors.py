import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q059':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'EA5B8AFCE5': 'many conditions have targeted treatments that can help to reverse the neurobiological changes in the brain',
    'D72DDD136B': 'A health care provider may prescribe medication to treat specific symptoms',
    'A3822A7942': 'NIBS techniques, such as tDCS, have been recently proposed in pediatric populations to explore its effect on brain plasticity',
    '633712CDB8': 'Carnosine or L-carnosine is a dipeptide composed by alanine and histidine, which acts as an antitoxi',
    'D5600905E9': 'The use of massage in autistic children with sleep problems is based on theoretical grounds',
    'A839CC3F4A': 'Psychological approaches can help people with ASD cope with anxiety, depression, and other mental he',
    'CB4631D590': 'There are no medications that treat the core symptoms of ASD.',
}

all_ok = True
for code, anchor in anchors.items():
    c = content_map[code]
    if anchor not in c:
        print(f"FAILED: {code}")
        all_ok = False
    else:
        idx = c.find(anchor)
        sub = c[idx:idx+200]
        if '\n' in sub:
            sub = sub.split('\n')[0].strip()
        if len(sub) == 0:
            print(f"EMPTY SPAN: {code}")
            all_ok = False
        elif len(sub) > 250:
            print(f"TOO LONG: {code} ({len(sub)})")
            all_ok = False
        else:
            print(f"OK: {code} ({len(sub)})")

print(f"All anchors valid? {all_ok}")

