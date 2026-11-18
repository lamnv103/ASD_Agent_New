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
    '6C82E2DDD8': 'studies such as these should be excluded from evidence‐based reviews of ASI',
    'ABCA692D0A': 'The intervention comprised Ayres Sensory Integration ® therapy delivered',
    '8E0ECAE98E': 'The findings from this review diverge from those of earlier reviews',
    'DD0E1D7D75': 'The primary goal of OT intervention is to enable participation in activities of everyday life',
    'F916609B2D': 'Iwanaga et al. [2014] is a nonrandomized study that compares outcomes data from children with ASD who received 9 months ASI intervention',
    '3CC6275DDE': 'In Stage Two, the 19 studies were further examined to determine if they met the following criteria',
    'F755605EF7': 'Ayres Sensory Integration intervention is frequently requested by parents and is often utilized by occupational therapists',
    '34E03728B1': 'outcomes measured in existing studies vary widely and may not be sensitive to the changes expected following ASI intervention',
    'DF8A2F72E8': 'Occupational therapy using the principles of Ayres Sensory Integration® (ASI) intervention is among the most req',
    '8339FB9707': 'confounding interpretation of the evidence on ASI intervention is that past reviews and meta‐analyses include studies that failed to provide an adequate description',
    '84B8D028AA': 'Our study indicates that ASI intervention meets criteria for an evidence‐based practice',
    '3145B16616': 'Sensory integration is one of the most highly utilized interventions in autism',
    'E344862663': 'Multisensory integration is defined as the study of how the brain integrates and interprets input fr',
    '2BDD94BC08': 'Ayres (1972, p. 4) described sensory integration dysfunction as a problem in the ability to “organize sensory information for use”',
    'CEBA798D0A': 'However, sensory-based interventions, as well as sensory strategies and environmental adaptations, are currently reported by many professionals',
    '5818E33BAF': 'Sensory integration and processing (SI/SP) differences are estimated to affect 5%–25% of children',
    '463BC15E4B': 'They lack many of the key ingredients of the ASI such as individual‐tailoring, active engagement of the child',
    '42DA2AA3C6': 'Pfeiffer et al. [2011] is a randomized controlled trial comparing two occupational therapy intervent',
    'ED2A2CB334': 'To distinguish SIT from other sensory-based interventions, a set of fidelity principles to guide delivery was developed and registered as ASI.',
    '29059574FD': 'Schaaf et al. [2014] is a randomized controlled trial of 32 children with ASD, 6–9 years old, who re',
    'D4B5E3C78B': 'In Stage One, searches were conducted in CINAHL, Cochrane Reviews, Cochrane Trials, Embase, ERIC, Medline',
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
