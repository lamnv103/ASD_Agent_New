import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q018':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    '0A41A35303': '• Social skills: SST, which teaches specific social skills based on behavioral principles, has consi',
    'A6FB96B825': 'This study adds to the still limited evidence for the efficacy of the culturally adapted SSTs for ad',
    'ABC96766BD': 'Findings from the meta-analysis revealed a large overall effect size comparable to previous studies',
    '1211C84D2D': 'PEERS® for Adolescents is a parent-assisted social skills training that uses cognitive-behavioral te',
    '41CE1A3AF2': 'A systematic review and meta-analysis were utilised to explore the methodological quality, program f',
    'D00BECEFAD': 'The current adaptation of the PEERS® intervention fills an important gap in evidence-based treatment',
    'F99E78970A': 'This result was further validated by similar gains in another measure of autism-related difficulties',
    '648D72B74C': 'Social skills training (SST) is the most widely researched intervention aimed at improving social sk',
    '225A8D4E15': 'Both sides underscored the concrete, structured, and practical character of the training, making it',
    'C50DCBA4ED': 'There is a clear need for future research to focus both on building autistic youth’s social competen',
    'F54674304A': 'Across this body of evidence, there is limited understanding of the impact of dosage',
    'E2FDF1FE92': 'In assessing PF, previous studies have largely relied on assessment methods with low reliability',
    '95C276A4CF': 'Although previous reviews have contributed significantly to our understanding of the efficacy of SSG',
    'E7E4192787': 'Both adolescents and their parents rated all the program components as helpful',
    '10DD92FD08': 'To test the immediate effects of the PEERS® curriculum, two-way mixed analyses of variance were cond',
    '3489521CBA': 'Means, standard deviations, and mixed ANOVAs results for treatment and waitlist control groups',
    '7B9882E05E': 'The study showed that the Treatment Group was superior to the Waitlist Control Group in most outcome',
    'A8E0F6F0A1': 'Outcome measure categories based on the outcomes used in the included studies',
    'B57D55D85E': 'Post-hoc simple effects analyses were conducted using univariate, within-subjects ANOVAs.',
    '1296D6729B': 'The TASSK-R is a self-report, criterion-referenced measure that assesses teens’ knowledge about soci',
    '197DD5B638': 'The study examined the efficacy of the Polish adaptation of the PEERS® curriculum for adolescents on',
    'F7981B5943': 'As found by previous reviews, the majority of SSGPs were delivered weekly by health professionals in',
    '47C81D29FB': 'Based on the meta-analysis, the Hedges’ g effect sizes of the nine studies providing data related to',
    '00DFC0B90D': 'The current systematic review identified 30 RCTs of PMIs for children and adolescents with ASD.',
    '942B8E427C': 'Means, standard deviations, and mixed ANOVAs results for treatment and waitlist control groups',
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
