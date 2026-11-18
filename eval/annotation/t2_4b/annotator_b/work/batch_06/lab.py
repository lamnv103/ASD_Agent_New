import json,re,sys,os
from collections import Counter
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'
def parse(q):
    t=open(W+'work/batch_06/%s.txt'%q,encoding='utf-8').read()
    parts=re.split(r'^### ',t,flags=re.M)[1:]
    d={}
    for p in parts:
        head,_,body=p.partition('\n')
        d[head.split(' | ')[0].strip()]=body
    return d
def write(q,L):
    d=parse(q); out=[]; seen=set()
    for code,g,rat,span,conf in L:
        assert code in d,code
        assert code not in seen,code; seen.add(code)
        if g==0: span=''
        else: assert span in d[code],(code,span)
        out.append(dict(annotation_code=code,grade=g,rationale=rat,evidence_span=span,confidence=conf,needs_review=False,review_note=''))
    assert seen==set(d),(set(d)-seen,len(d))
    os.makedirs(W+'returned/batch_06',exist_ok=True)
    with open(W+'returned/batch_06/%s.jsonl'%q,'w',encoding='utf-8') as f:
        for o in out: f.write(json.dumps(o,ensure_ascii=False)+'\n')
    print(q,len(out),sorted(Counter(o['grade'] for o in out).items()))
