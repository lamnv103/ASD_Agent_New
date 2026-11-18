import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q029':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'BB2EEAD92D': 'In the present study it was found that children with ASD exhibit more anxiety disorders compared to children with ADHD.',
    '7323AAAC58': 'COMORBID having at least one comorbid disorder',
    'E24FCB36DE': 'Frequency of comorbid psychiatric disorders in children with ASD and children with ADHD',
    '4E91E07F05': 'Evaluate early-life predictors of mid-childhood ASD and anxiety symptoms',
    'A203263CB7': 'adolescents with ASD have higher comorbidity for psychopathology, including ADHD',
    'CF498B95AF': 'identify comorbid psychiatric disorders in children with autism spectrum',
    '41AF38EDB4': 'All children were referred to a general outpatient mental health center',
    '2DD1AFFC0B': 'In administering the KID-SCID, a respondent is asked whether a particular DSM-IV symptom is present.',
    'E482AF8BDE': 'In individuals with ASD, a high frequency of anxiety is detected due to the stress and anxiety associated with social',
    '742512AC30': 'Children and adolescents with ASD have shown high rates of ADHD symptoms (16–85%)',
    '73478DD561': 'In the ASD sample, twenty-three chi',
    '2452FB4325': 'Youths with ASD often experience separation anxiety, social anxiety, and generalized anxiety symptom',
    'D982E5F83F': 'Research also shows a prevalence of ADHD in certain psychiatric comorbidities. It is especially high',
    '2D0537309E': 'Autism spectrum disorder (ASD) is a complex neurodevelopmental condition that manifests in early chi',
    '584719F0CC': 'When looking at ASD with and without specific comorbidities (ADHD and/or anxiety), the subgroup of A',
    '048877205C': 'The rate of clinically elevated ADHD and anxiety symptoms in ASD was 62.7 and 44.6%',
    'BB9D0DD4B8': 'This study is unique in that it aligns with our hypothesis that children with ADHD face higher level',
    'DA978FCF4B': 'Children with attention deficit hyperactivity disorder (ADHD) or autism spectrum disorder (ASD) indi',
    '3A5628FED7': 'Child psychiatric disorders can be roughly divided into two main groups: internalizing and externali',
    'B8F3E76DCD': 'Attention deficit hyperactivity disorder (ADHD) is a common neurological, and developmental comorbid',
    'C9615A7C06': 'Among psychiatric conditions commonly noted to have elevated frequencies in persons with ASD are anx',
    '7CE592312E': 'evaluate the frequency of ADHD and anxiety symptoms in the participants diagnosed with ASD',
    '6DD49FF898': 'evaluate the possible linkage between anxiety and psychiatric comorbidities in individua',
    'BE196797A7': 'Correlations between comorbidity and age',
    '78BACFAD43': 'higher frequencies of anxiety difficulties (11–84%) have been reported in children with ASD',
    'D6CD7727A2': 'We conducted a literature review on the differing levels of anxiety and psychiatric comorbidities in children with ADHD, ASD',
    '2C55E77A98': 'Children with ADHD face higher levels of anxiety than others with estimated rates of co-occurring anxiety being between',
    '26B1EBD4A3': 'first study to examine the rate of psychiatric disorders in children with ASD and',
    'EA2098FDDE': 'children with ASD and ADHD do not differ with respect to their overall comorbidity rate',
    '499BD59542': 'ADHD and anxiety symptoms are related to poore',
    '8DCDBA5677': 'Compare movement and locomotor skills between those with ADHD and ASD',
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
