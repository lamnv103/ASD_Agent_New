import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q022':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    '9D57762846': 'Wandering and elopement',
    'B0AE87836A': 'The prevalence of elopement within the previous 12 months was calculated separately',
    'F4C836E374': 'Attributes such as wandering, sensory issues, impulsivity, and a limited sense of danger',
    'BA80E65C45': 'typically developing children due to wandering behavior, decreased risk awareness, and attraction to water',
    '3B1679C218': 'Elopement places children with developmental disabilities at risk of serious injury or even death',
    '0330D7EFDF': 'This is the first study to examine and report the prevalence and correlates of elopement',
    '1EB18D123C': 'understanding of the causes of elopement in this population may aid in the development of strategies',
    'D95E2C828B': 'Water and Wandering Program are two examples of programming that can increase the',
    '5113127097': 'these findings suggest that elopement is a common problem among U.S. children with developmental',
    '2F35A3A846': 'Wandering and elopement',
    '492551FF3B': 'drawn attention to wandering, or elopement, as a potential cause of injury in children with development',
    '7BFC5881E4': 'learning can also affect water safety. One parent recalled a very stressful moment when her child elo',
    'D4854D6A29': 'Elopement was assessed based on four questions about the child’s histo',
    '556343BAC2': 'Fifteen items from the CSBQ were identified as being exceptionally relevant to the safety of children who wander',
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
