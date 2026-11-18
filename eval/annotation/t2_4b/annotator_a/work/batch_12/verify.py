import json, collections
from common import parse
R='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_12/'
KEYS={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
for q in ['q026','q010','q007']:
    c=parse(q+'.txt'); rows=[json.loads(l) for l in open(R+q+'.jsonl',encoding='utf-8') if l.strip()]
    codes=[r['annotation_code'] for r in rows]; probs=[]
    if sorted(codes)!=sorted(c) or len(set(codes))!=len(codes): probs.append('code mismatch')
    for r in rows:
        if set(r)!=KEYS: probs.append('keys '+r['annotation_code']+' '+str(sorted(set(r)-KEYS)))
        g=r['grade']
        if g in (1,2,3,-1) and (not r['evidence_span'] or r['evidence_span'] not in c[r['annotation_code']]): probs.append('span '+r['annotation_code'])
        if g==0 and r['evidence_span']: probs.append('span on 0 '+r['annotation_code'])
    print(q,len(rows),dict(collections.Counter(r['grade'] for r in rows)),'nr',sum(r['needs_review'] for r in rows),probs[:3],len(probs))
