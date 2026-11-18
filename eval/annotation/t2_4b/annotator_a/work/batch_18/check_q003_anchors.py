import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_18.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q003':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    '194EA8D361': 'A recurrent theme and narrative in the review was identifying causes of (and factors associated with) autism',
    '93F5871761': 'Researchers do not know the primary causes of ASD, but studies suggest that a person’s genes and asp',
    '6E2D8FCA3E': 'Genome-wide association studies (GWASs) have identified dozens of common variants associated with au',
    '255F3A5C5F': 'There is not just one cause of ASD. Many different factors have been identified that may make a child more likely to have ASD',
    'F6DAE16231': 'The historical context of Viet Nam provides a unique focus on the causes of autism, notably dioxin exposure',
    '1731A1F532': 'Shared genetic risk between autism and phenotypes are seen with DDX3X-related neurodevelopmental disorder',
    '8892EDE8DF': 'Hygiene practices commonly in urban areas lowered microbial exposure in pregnancy',
    'C818B0CBC5': 'common genetic etiology between both conditions. The genes NRXN1, CNTNAP2 and SLITRK5',
    '25AA0EAAEC': 'high-risk children (for example, younger siblings of children with ASD)',
    '2F8596E024': 'Maternal immune activation during pregnancy is one of the best-established immunological risk factor',
    '9A8D172E60': 'Evaluate early-life predictors of mid-childhood ASD and anxiety sympto',
    '47F677CF80': 'Another association between autoimmunity and autism has been found with regard to the risk of autism in children from families with a history of autoimmunity.',
    '64156F07F2': 'While epidemiological and animal data remain promising, prenatal infection, autoimmune disease',
    'AA11AF9D17': 'Gestational factors play a critical role in shaping ASD risk. Maternal immune activation (MIA) has b',
    '6206BBBD3D': 'Allergic disorders are caused by dysregulated responses of the immune system to allergens in the env',
    '355083BAD1': '>200 ASD risk genes; both common polygenic and rare de novo variants implicated',
    '59B7914590': 'ASD is among the most heritable neurodevelopmental conditions, with twin and family studies estimati',
    '25C63E5DCB': 'This finding suggests a possible relationship between ASD and farming practice, especially the common use of pesticides in Vietnam.',
    '2741BAE743': 'Autism can be associated with known environmental factors that can include exposures such as valproate, intrauterine alcohol exposure, prematurity, etc.',
    'BB91336BD5': 'Rare genetic variants—including copy number variants (CNVs) and de novo single-nucleotide variants—c',
    '7D0D49DE57': 'While genetics play a dominant role, gene–environment interactions contribute to ASD risk. Recent st',
    'F2DA1BA748': 'global understandings of autism recognise the aetiology of autism to be complex, with interactive genetic and environmental factors',
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
