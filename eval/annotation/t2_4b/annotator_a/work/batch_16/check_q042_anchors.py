import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q042':
            content_map[obj['annotation_code']] = obj['content']

anchors = {
    'B753B846F9': 'Sensory‐based interventions stand in contrast to ASI in that their application often contradicts many of the core principles of ASI.',
    '6C82E2DDD8': 'ASI intervention requires direct, active engagement of the child in individually tailored sensory‐motor activities',
    'B303A2D698': 'studies of ASI intervention',
    '273AD0AE2B': 'Sensory-based interventions (SBIs)',
    'ABCA692D0A': 'Ayres Sensory Integration (ASI) intervention',
    '8E0ECAE98E': 'ASI intervention in ASD requires fidelity to the core principles',
    'DD0E1D7D75': 'Sensory integration therapy (SIT) was developed by Jean Ayres',
    'F916609B2D': 'results of studies evaluating ASI intervention',
    '3CC6275DDE': 'Ayres Sensory Integration® (ASI) intervention',
    'F755605EF7': 'ASI intervention meets criteria for an evidence‐based practice',
    '34E03728B1': 'outcomes measured in existing studies vary widely and may not be sensitive to the changes expected following ASI intervention',
    'DF8A2F72E8': 'Occupational therapy using the principles of Ayres Sensory Integration® (ASI) intervention is among the most req',
    '8339FB9707': 'confounding interpretation of the evidence on ASI intervention is that past reviews and meta‐analyses include studies that failed to provide an adequate description',
    '92660C11F2': 'studies meeting criteria for ASI intervention',
    '9343C68FAA': 'Ayres Sensory Integration intervention',
    '84B8D028AA': 'core principles of ASI intervention include therapist adherence to the Ayres Sensory Integration Fidelity Measure',
    '176141A06F': 'fidelity to ASI intervention',
    '3145B16616': 'Ayres Sensory Integration® (ASI) intervention for children with autism spectrum disorders',
    'E344862663': 'Ayres sensory integration (ASI) approach',
    '031CD1F188': 'criteria for ASI intervention',
    '2BDD94BC08': 'Ayres (1972, p. 4) described sensory integration dysfunction as a problem in the ability to “organize sensory information for use”',
    'CEBA798D0A': 'However, sensory-based interventions, as well as sensory strategies and environmental adaptations, are currently reported by many professionals',
    '5818E33BAF': 'Sensory integration and processing (SI/SP) differences are estimated to affect 5%–25% of children',
    '463BC15E4B': 'They lack many of the key ingredients of the ASI such as individual‐tailoring, active engagement of the child',
    '42DA2AA3C6': 'findings on ASI intervention',
    'ED2A2CB334': 'To distinguish SIT from other sensory-based interventions, a set of fidelity principles to guide delivery was developed and registered as ASI.',
    '29059574FD': 'evaluation of ASI intervention studies',
    '5B0BC275DE': 'studies evaluating ASI intervention',
    'D4B5E3C78B': 'Ayres Sensory Integration',
    '3A0D46CD87': 'ASI intervention fidelity',
}

for code, anchor in anchors.items():
    c = content_map[code]
    if anchor not in c:
        print(f"FAILED: {code}")
        # print first line
        lines = [l.strip() for l in c.split('\n') if len(l.strip()) > 30]
        for l in lines[:2]:
            print(f"  cand: '{l[:100]}'")
    else:
        idx = c.find(anchor)
        sub = c[idx:idx+200]
        if '\n' in sub:
            sub = sub.split('\n')[0].strip()
        print(f"OK: {code} ({len(sub)})")

