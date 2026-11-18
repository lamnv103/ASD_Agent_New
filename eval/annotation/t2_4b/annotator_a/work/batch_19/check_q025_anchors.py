import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q025':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    '3E4646EF66': 'Phase I using M-CHAT to identify high-risk children in the general population',
    'A487BF7A4C': 'M-CHAT-R/F’s primary weakness',
    'DF93F65E6F': 'Modified Checklist for Autism in Toddlers (M-CHAT) to screen children with high risk of ASD.',
    'A42E36C02C': 'comparative analysis of the M-CHAT-R/F against other prominent screening tools',
    '16B5D90BFD': 'This systematic review concluded that the M-CHAT-R/F did not demonstrate consistent, universal utili',
    '5C80771546': 'comparative screening accuracy of the M-CHAT-R/F',
    '5080D46133': 'Current research shows a considerable variation in outcomes',
    'F44C10F5AD': 'compared the accuracy metrics of the M-CHAT-R/F with alternative screening tools',
    'D66041F695': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) a widely adopted tool globally',
    '7C87F80894': 'From 172 identified articles, six high-quality studies encompassing',
    'D8C5675D52': 'direct comparison between the M-CHAT-R/F and an alternative screening tool',
    '626A5794AC': 'M-CHAT-R/F exhibits variable sensitivity, a persistently low positive predictive value',
    '4C01A2AC56': 'sensitivity, specificity, PPV and NPV for both the M-CHAT-R/F and its comparator tools',
    'DE580D95CB': 'The M-CHAT was later shortened to ten questions in order to make it more convenient',
    'EBAE3184C8': 'The M-CHAT, AQ, and CBSL are the screening methods most commonly used',
    'FF6B46CD06': 'M-CHAT-R/F performed poorly, with low sensitivity and PPV',
    'AFDD171B87': 'follow-up interviews to improve the PPV and minimize the false-positiv',
    '2A0BB83C4F': 'Modified Checklist for Autism in Toddlers (M-CHAT), while widely used, shows limitations in the ex-preterm population',
    '8F620C1C02': 'A systematic literature search was conducted across four databases',
    '740D779A5E': 'The tools such as M-CHAT, FYI, GADS, and ASAS',
    '26322AAE81': 'In this study, we used M-CHAT for screening ASD among the studied children as it has been widely use',
    'F47CAAD305': 'how the M-CHAT-R/F compares with newly developed and digitally enhanced screening tools',
    '5C7A1F5907': 'Modified Checklist for Autism in Toddlers (M-CHAT) was utilized for the screening phase of our study.',
    '836DAB3FE9': 'comparative advantage of the M-CHAT-R/F’s predictive value is increasingly challenged',
    'C0DF942964': 'The M-CHAT-R/F takes about 10 min to complete.',
    'C0EAB0686F': 'screening accuracy of the M-CHAT-R/F to that of other screening tools',
    'FDEEFB0261': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) has become a prominent two-stage, parent-dependent screening tool',
    '0962FBC376': 'All six included studies demonstrated high methodological quality',
    '1CD05755ED': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) maintain reliable diagnostic accuracy',
    '05261F4569': 'the M-CHAT-R/F functions as a highly sensitive, yet low specificity, screening tool',
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
