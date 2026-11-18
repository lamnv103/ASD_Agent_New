import json,re,collections
W="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_11/"
R="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_11/"
tot=collections.Counter();nr=0;prob=[]
for q in ["q041","q006","q002"]:
    txt=open(W+q+".txt",encoding="utf-8-sig").read()
    parts=re.split(r"^### ",txt,flags=re.M)[1:]
    P={}
    for p in parts:
        head,_,body=p.partition("\n"); P[head.split(" | ")[0].strip()]=body
    rows=[json.loads(l) for l in open(R+q+".jsonl",encoding="utf-8") if l.strip()]
    codes=[r["annotation_code"] for r in rows]
    if sorted(codes)!=sorted(P) or len(set(codes))!=len(codes): prob.append((q,"codes mismatch",len(codes),len(P)))
    c=collections.Counter()
    for r in rows:
        K={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
        if set(r)!=K: prob.append((q,r["annotation_code"],"extra keys:"+",".join(sorted(set(r)-K))))
        c[r["grade"]]+=1; nr+=r["needs_review"]
        g=r["grade"]
        if g in (1,2,3,-1):
            if not r["evidence_span"] or r["evidence_span"] not in P.get(r["annotation_code"],""): prob.append((q,r["annotation_code"],"span"))
        elif g==0 and r["evidence_span"]: prob.append((q,r["annotation_code"],"span on 0"))
    tot+=c; print(q,len(rows),dict(c))
print("total",dict(tot),"needs_review",nr,"problems",prob)
