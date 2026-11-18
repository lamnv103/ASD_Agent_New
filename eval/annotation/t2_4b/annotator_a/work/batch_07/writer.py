import json, sys, re
def parse(qid):
    txt=open(f'{qid}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ([0-9A-F]{10}) \|[^\n]*\n', txt, flags=re.M)
    d={}
    for i in range(1,len(parts),2):
        d[parts[i]]=parts[i+1]
    return d
def write(qid, labels):
    d=parse(qid)
    out=[]
    for code,(g,rat,span,conf) in labels.items():
        assert code in d, code
        if g in (1,2,3,-1):
            assert span and span in d[code], (code, span)
        else:
            assert span=="", code
        out.append({"annotation_code":code,"grade":g,"rationale":rat,"evidence_span":span,"confidence":conf,"needs_review":False,"review_note":""})
    assert set(labels)==set(d), (set(d)-set(labels), set(labels)-set(d))
    with open(f'../../returned/batch_07/{qid}.jsonl','w',encoding='utf-8') as f:
        for o in out: f.write(json.dumps(o,ensure_ascii=False)+'\n')
    print(qid, len(out))
