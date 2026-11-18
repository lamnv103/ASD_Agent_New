import json, collections
from writer import load, R
KEYS={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
for q in ['q003','q011','q015','q046']:
    c=load(q); rows=[json.loads(l) for l in open(R+q+'.jsonl',encoding='utf-8') if l.strip()]
    codes=[r['annotation_code'] for r in rows]
    cnt=collections.Counter(r['grade'] for r in rows); probs=[]
    if sorted(codes)!=sorted(c) or len(set(codes))!=len(codes): probs.append('code mismatch')
    for r in rows:
        if set(r)!=KEYS: probs.append('keys '+r['annotation_code']+str(sorted(set(r)-KEYS)))
        if r['grade']!=0 and r['grade'] is not None and r['evidence_span'] not in c[r['annotation_code']]: probs.append('span '+r['annotation_code'])
        if r['grade']!=0 and not r['evidence_span']: probs.append('empty '+r['annotation_code'])
    print(q,len(rows),'/',len(c),dict(sorted(cnt.items(),key=lambda x:str(x))),'nr',sum(r['needs_review'] for r in rows),probs[:3],len(probs))
