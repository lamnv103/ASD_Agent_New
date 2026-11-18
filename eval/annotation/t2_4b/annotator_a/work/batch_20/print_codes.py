import json
with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q020']

codes = ['A184E2E3BC', 'FDE1B38BC1', 'F681DFCE9B', '1D67FB6B70', 'C14E67B5A5', '82DEF08DC1', '25B8597E69', '180A3D6142', '0698F0B688', '38208CBA60', 'DFE346D5D3', 'B53DD3B76D', '75C22FFE9E', '5AA491A7CB', '3BAC728961', '0840EF7619']
item_map = {it['annotation_code']: it['content'] for it in items}

for c in codes:
    print(f"=== {c} ===")
    print(item_map[c][:250].replace('\n', ' '))

