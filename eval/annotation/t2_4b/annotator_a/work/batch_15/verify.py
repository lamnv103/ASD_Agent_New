import json,re,collections
R="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_15/"
tot=collections.Counter();ok=True
for q in ["q047","q004","q005","q063"]:
    txt=open(q+".txt",encoding="utf-8").read()
    parts=re.split(r"^### ([0-9A-F]{10}) \|[^\n]*\n",txt,flags=re.M)
    P={parts[i]:parts[i+1] for i in range(1,len(parts),2)}
    rows=[json.loads(l) for l in open(R+q+".jsonl",encoding="utf-8")]
    codes=[r["annotation_code"] for r in rows]
    if sorted(codes)!=sorted(P) or len(codes)!=len(set(codes)): ok=False;print(q,"CODE MISMATCH")
    for r in rows:
        assert set(r)=={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
        g=r["grade"];tot[g]+=1
        if g!=0 and (not r["evidence_span"] or r["evidence_span"] not in P[r["annotation_code"]]): ok=False;print(q,r["annotation_code"],"SPAN FAIL")
        if g==0 and r["evidence_span"]: ok=False
    print(q,len(rows),collections.Counter(r["grade"] for r in rows))
print("TOTAL",dict(tot),"OK" if ok else "FAIL")
