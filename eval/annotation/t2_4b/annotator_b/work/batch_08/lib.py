import json,re,sys
from collections import Counter
R="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/"
def passages(q):
    t=open(R+f"work/batch_08/{q}.txt",encoding="utf-8").read()
    parts=re.split(r"^### ",t,flags=re.M)[1:]
    d={}
    for p in parts:
        h,_,body=p.partition("\n"); d[h.split(" |")[0].strip()]=body
    return d
def write(q,rows):
    d=passages(q); out=[]; seen=set(); bad=0
    for code,g,rat,span,conf in rows:
        assert code in d and code not in seen,code; seen.add(code)
        if g in(1,2,3,-1) and span not in d[code]: print("BAD SPAN",code,span); bad+=1
        out.append(dict(annotation_code=code,grade=g,rationale=rat,evidence_span=span if g!=0 else "",confidence=conf,needs_review=False,review_note=""))
    miss=set(d)-seen
    print(q,len(d),len(out),"missing",miss,"bad",bad)
    if not miss and not bad:
        with open(R+f"returned/batch_08/{q}.jsonl","w",encoding="utf-8") as f:
            for o in out: f.write(json.dumps(o,ensure_ascii=False)+"\n")
        print(Counter(o["grade"] for o in out))
