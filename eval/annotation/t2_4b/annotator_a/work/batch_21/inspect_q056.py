import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_21.jsonl', 'r', encoding='utf-8') as f:
    items_q056 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q056']

item_map = {it['annotation_code']: it['content'] for it in items_q056}

# Question q056: Khi trẻ tự kỷ bước vào tuổi teen, cần chú ý những thay đổi tâm lý nào?
# Key changes during transition to adolescence for autistic teens:
# - Transition to adolescence: biopsychosocial transformation, heightened emotional/social demands
# - Neuroendocrine changes, pubertal surges in sex hormones exacerbating sensory sensitivities and mood instability
# - Increased rates of internalizing disorders: depression, anxiety, social withdrawal, feelings of loneliness/isolation
# - Increased awareness of social differences, peer rejection, bullying, gender dysphoria
# - Changes in executive functioning demands, academic and daily independence expectations
# Papers: "Transition to adolescence in neurodevelopmental disorders", "Autism Spectrum Disorder: What Do We Know and Where Do We Go?", "Behavioral Interventions for Autism Spectrum Disorder", "The Teen Brain: 7 Things to Know".

for it in items_q056:
    c = it['annotation_code']
    lines = [l.strip() for l in it['content'].split('\n') if l.strip()]
    print(f'"{c}": {repr(lines[0][:150])},')

