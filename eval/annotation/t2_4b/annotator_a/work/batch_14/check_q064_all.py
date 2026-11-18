import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q064':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    '8B954FBF2C': 'If a doctor suspects a child has ASD or another developmental disability, he or she usually will refer the child to a variety of specialists, including a speech-language pathologist.',
    '478FD48AD4': 'confirmed in ~10% of ASD cases, linked to language delay and macrocephaly',
    'D249B7FADF': 'some degree of impaired social behavior, communication and language, and a narrow range of interests and activities',
    'E8F6E08785': 'constipation was associated with speech problems in both age groups',
    'F6BD7A0ACA': 'Autism Spectrum Disorder (ASD) is a neurodevelopmental condition characterized by challenges in social interaction and communication and the presence of restricted interests and repetitive behaviors',
    '29E2726699': 'Some children with ASD may not be able to communicate using speech or language, and some may have very limited speaking skills. Others may have rich vocabularies',
    'E03AE499C2': 'CSCS-DP, to identify the risk of communication and symbolic functioning disabilities in infants',
    'D74BBD0072': 'These behaviors or interests set ASD apart from conditions defined by problems with social communication and interaction only.',
    '1E001C07FA': 'Autism spectrum disorder (ASD) is a developmental disability that can cause significant social, communication, and behavioral challenges.',
    '0F86ABCC42': 'Taken together, these difficulties affect the ability of children with ASD to interact with others',
    '8444D4DB14': 'definitions of verbal status (such as “functional” or “intelligible” speech) reduce comparability.',
    '800915582B': 'the focus of ICT is on predicting language delays before the child is even starting to talk.',
    '4D2A261C92': 'Speech delay is often an early marker of ASD, but heterogeneity is high: some children acquire age-appropriate vocabulary yet struggle with pragmatics',
    'CEF03DA6E0': 'Salley et al. reported that people with ASD demonstrated the highest communication and social interaction deficit',
    '754EF61E05': 'Speech and language impairments are among the most recognizable features of ASD. Difficulties include delays in first words, limited phrase speech, and atypical prosody',
    '6FD27D62A6': 'hinders an individual’s skills in socialisation, creates repetitive behaviours, and impacts expressive or verbal communication',
    '045C3839F5': 'speech-language pathologist, and developmental–behavioral pediatrician',
    'E64B9329C9': 'Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors',
    '23C8D88642': 'characterized by persistent difficulties in social communication and restricted, repetitive behaviors',
    'A6DB820AC7': 'Social communication and interaction skills can be challenging for people with ASD.',
    'DAF86C5DEC': 'Some of these studies involve children with ASD who have limited speech and language skills',
    'F942A0E2E3': 'Individuals who have marked deficits in social communication, but whose symptoms do not otherwise meet criteria for autism spectrum disorder, should be evaluated for social (pragmatic) communication disorder.',
    '8029411FE1': 'Little is known about the impact of epilepsy on social and cognitive function in autistic children, making our understanding of how epilepsy influences social communication',
    'C423D96C93': 'prioritize the social communication and behavioral needs of children',
    '83AD866396': 'with more impaired social and communication domains.',
    'CD14707E4A': 'Difficulty with social communication and interaction with other people',
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
