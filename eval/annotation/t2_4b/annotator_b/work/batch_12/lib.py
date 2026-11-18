import json,re,sys
from collections import Counter
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'
def passages(q):
    t=open(W+f'work/batch_12/{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',t,flags=re.M)[1:]
    d={}
    for p in parts:
        code=p.split(' | ',1)[0].strip(); d[code]=p
    return d
def Z(r):
    return (0,r,"","high")
def write(q,labels):
    d=passages(q); out=[]
    for code,(g,rat,span,conf) in labels.items():
        assert code in d,code
        if g in (1,2,3,-1): assert span and span in d[code],(code,span)
        out.append({"annotation_code":code,"grade":g,"rationale":rat,"evidence_span":span if g!=0 else "","confidence":conf,"needs_review":False,"review_note":""})
    missing=set(d)-set(labels); assert not missing,missing
    with open(W+f'returned/batch_12/{q}.jsonl','w',encoding='utf-8') as f:
        for o in out: f.write(json.dumps(o,ensure_ascii=False)+"\n")
    print(q,len(d),len(out),sorted(Counter(o['grade'] for o in out).items()))
