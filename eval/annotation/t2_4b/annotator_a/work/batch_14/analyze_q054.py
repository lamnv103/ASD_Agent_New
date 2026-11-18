import json

path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_14/q054_raw.txt'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

entries = text.split('### [')
print(f"Total entries: {len(entries)-1}")
for e in entries[1:]:
    lines = e.strip().split('\n')
    header = lines[0]
    content = '\n'.join(lines[1:])
    # check keywords
    kw_hits = [w for w in ['parent', 'home', 'school', 'teacher', 'cha mẹ', 'trường', 'nhà', 'can thiệp', 'intervention'] if w in content.lower()]
    print(f"Header: {header[:60]} | hits: {kw_hits}")

