import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_21.jsonl', 'r', encoding='utf-8') as f:
    items_q040 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q040']

item_map = {it['annotation_code']: it['content'] for it in items_q040}

# Question q040: Trẻ tự kỷ học bơi có lợi gì và cần lưu ý an toàn gì?
# Benefits of swimming: therapeutic aquatic environment, sensory regulation, physical activity, social inclusion, fun, confidence, motor skills.
# Safety concerns: drowning is leading cause of death (<14 yrs), lack of danger awareness, elopement/wandering to water bodies, need for adaptive swimming lessons, 1-on-1 instruction, visual aids, trained instructors.

for it in items_q040:
    c = it['annotation_code']
    lines = [l.strip() for l in it['content'].split('\n') if l.strip()]
    print(f'"{c}": {repr(lines[0][:150])},')

