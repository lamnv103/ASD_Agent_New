import sys,json,collections; sys.path.insert(0,'.')
from writer import passages,R
K={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
for q in ['q009','q057','q053']:
    P=passages(q); rows=[json.loads(l) for l in open(R+q+'.jsonl',encoding='utf-8') if l.strip()]
    c=collections.Counter(r['annotation_code'] for r in rows)
    probs=[]
    if set(c)!=set(P) or any(v!=1 for v in c.values()): probs.append('coverage')
    extra=set().union(*[set(r)-K for r in rows]); miss=set().union(*[K-set(r) for r in rows])
    for r in rows:
        g=r['grade']
        if g in (1,2,3,-1) and (not r['evidence_span'] or r['evidence_span'] not in P[r['annotation_code']]): probs.append('span '+r['annotation_code'])
        if g==0 and r['evidence_span']: probs.append('span0 '+r['annotation_code'])
    print(q,len(rows),len(P),dict(sorted(collections.Counter(r['grade'] for r in rows).items(),key=lambda x:str(x[0]))),'NR',sum(r['needs_review'] for r in rows),'extra',extra,'missing',miss,probs)
