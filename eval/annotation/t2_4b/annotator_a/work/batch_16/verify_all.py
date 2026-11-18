import json, re, collections
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_16/'
R='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_16/'
KEYS={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
tot=collections.Counter(); nr=0
for q in ['q013','q029','q049','q042']:
    txt=open(W+q+'.txt',encoding='utf-8').read()
    parts=re.split(r'\n### ([0-9A-F]{10}) \|[^\n]*\n', '\n'+txt)
    content={parts[i]:parts[i+1] for i in range(1,len(parts),2)}
    rows=[json.loads(l) for l in open(R+q+'.jsonl',encoding='utf-8') if l.strip()]
    codes=[r['annotation_code'] for r in rows]
    probs=[]
    if len(codes)!=len(set(codes)): probs.append('dup')
    if set(codes)!=set(content): probs.append('code mismatch')
    extra=set()
    gc=collections.Counter()
    for r in rows:
        if set(r)!=KEYS: extra|=set(r)^KEYS
        g=r['grade']; gc[g]+=1; tot[g]+=1
        if r['needs_review']: nr+=1
        if g in (1,2,3,-1) and not (r['evidence_span'] and r['evidence_span'] in content[r['annotation_code']]): probs.append('span '+r['annotation_code'])
        if g==0 and r['evidence_span']: probs.append('span nonempty grade0 '+r['annotation_code'])
    print(q,len(rows),'/',len(content),dict(sorted(gc.items(),key=lambda x:str(x[0]))),'keydiff',sorted(extra),probs)
print('total',dict(tot),'needs_review',nr)
