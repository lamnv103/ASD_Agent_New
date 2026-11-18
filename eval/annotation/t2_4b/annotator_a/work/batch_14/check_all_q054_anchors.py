import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'F3E7C010A6': 'Further research into the feasibility, efficacy, and appropriateness of the methods of delivery for',
    'CD96696424': 'And the number of parents that say oh if only we had known this.',
    '9BD9686709': 'SBIs may be implemented by caregivers and other team members or accessed independently by the child',
    '1C142A6214': 'Parenting interventions during the first 3 years of childhood are effective for improving ECD and caregiving.',
    '65258C986B': 'For some children, teachers had also commented that their confidence, skills and general behaviour had improved.',
    '938A9D4D00': 'In LMICs, community health worker and primary health care facilities were the platforms for implementation.',
    'F847B74588': 'Early learning and development Interventions that enhance caregivers’ access, knowledge, attitudes, practices or skills',
    '5C063B1D3C': 'Second, we analyzed the impact of parenting interventions on parents themselves',
    'D69D4702A2': 'Most of the described interventions were implemented directly in mainstream classroom settings',
    '5EB92E9C78': 'You can carry out 30-odd sessions, but once that intervention finished it ’s finished, unless the parent and the child',
    '2448787093': 'Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging behaviours.',
    '97380982B8': 'Out of the total 102 interventions, 70 (69%) had some degree of a responsive caregiving component',
    '6270EBF763': '- We conducted a systematic review and meta-analysis of 102 randomized controlled trials of parenting interventions',
    'FBEF5560C7': 'PMIs are advantageous because they reduce the demands on children with ASD compared to behavioral approaches and bring treatment into a home and community setting',
    '4D4078C351': 'More research is needed to determine how to optimize the design and delivery of parenting programs',
    'C483851B3E': 'NDBIs are naturalistic in that they take place in environments and within routines that are already likely to occur in the child’s life',
    '9F70CC7CBE': 'All infants and children should receive responsive care during the first 3 years of life; parents and other caregivers should be supported to provide responsive care.',
    '5E7C872323': 'Increased confidence and independence It was commonly identified by both carers and therapists that children',
    '84EBBE3EFF': 'Findings of this systematic review provide preliminary evidence that parent-mediated intervention training',
    '1A7B4345C4': 'To the best of our knowledge, this is the largest and most comprehensive systematic review and meta-analysis that synthesized 102 parenting interventions',
    '643227B07C': 'Twelve (21%) studies applied the intervention at child level; nine (16%) at peer level; seven (13%) at staff level; and four (7%) at physical environment level.',
    'CCF6B7138E': 'The clinical interventions for children, adolescents, and young adults with autism have demonstrated gains in different developmental domains where parent inclusion',
    '75180AAA4D': 'our review suggests that parental engagement and support programs may indeed have universal benefits on child and parent outcomes irrespective of child age or the timing of introduction.',
    'E1A83E8208': 'The course is designed to be delivered in nine core group sessions for caregivers and three home visits. The group sessions can be provided at a health facility, school or other community-based facility.',
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

print(f"All anchors valid? {all_ok}")
