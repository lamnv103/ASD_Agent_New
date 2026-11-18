import json,re,sys
B="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/"
def passages(q):
    t=open(B+f"work/batch_13/{q}.txt",encoding="utf-8").read()
    parts=re.split(r"^### ",t,flags=re.M)[1:]
    d={}
    for p in parts:
        head,_,body=p.partition("\n")
        d[head.split(" | ")[0].strip()]=body
    return d
def write(q,labels):
    d=passages(q); out=[]; bad=0
    assert set(d)==set(labels),(set(d)^set(labels))
    for c in d:
        g,r,s,cf=labels[c]
        if g in (1,2,3,-1):
            if s not in d[c]:
                print("BAD SPAN",q,c,repr(s)); bad+=1
        else: s=""
        out.append(dict(annotation_code=c,grade=g,rationale=r,evidence_span=s,confidence=cf,needs_review=False,review_note=""))
    if bad: sys.exit(1)
    with open(B+f"returned/batch_13/{q}.jsonl","w",encoding="utf-8") as f:
        for o in out: f.write(json.dumps(o,ensure_ascii=False)+"\n")
    from collections import Counter
    print(q,len(out),dict(Counter(o["grade"] for o in out)))
