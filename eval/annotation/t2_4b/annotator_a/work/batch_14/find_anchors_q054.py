import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            content_map[obj['annotation_code']] = obj['content']

codes = [
    'F3E7C010A6', 'CD96696424', '9BD9686709', '1C142A6214', '65258C986B',
    '938A9D4D00', 'F847B74588', '5C063B1D3C', 'D69D4702A2', '5EB92E9C78',
    '2448787093', '97380982B8', '6270EBF763', '35C44C9657', '25386C582F',
    'D06392E3F5', 'D52EA62D51', 'FBEF5560C7', '4D4078C351', 'C483851B3E',
    '9F70CC7CBE', '5E7C872323', '84EBBE3EFF', '1A7B4345C4', 'AB42AA8AB7',
    '643227B07C', 'CCF6B7138E', '75180AAA4D', 'E1A83E8208'
]

for c in codes:
    text = content_map[c]
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
    print(f"=== {c} ===")
    for line in lines[:2]:
        print(f"   '{line[:100]}'")

