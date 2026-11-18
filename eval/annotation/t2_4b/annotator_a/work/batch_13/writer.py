import json, re, sys
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_13/'
R='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_13/'
def passages(q):
    txt=open(W+q+'.txt',encoding='utf-8').read()
    parts=re.split(r'^### ([0-9A-F]{10}) \|[^\n]*\n',txt,flags=re.M)
    return {parts[i]:parts[i+1] for i in range(1,len(parts),2)}
def write(q,labels):
    P=passages(q)
    assert set(P)==set(l[0] for l in labels) and len(labels)==len(P),(set(P)^set(l[0] for l in labels))
    out=[]
    for code,g,rat,span,conf in labels:
        if g==0: span=''
        else: assert span and span in P[code],(code,span)
        out.append(json.dumps({"annotation_code":code,"grade":g,"rationale":rat,"evidence_span":span,"confidence":conf,"needs_review":False,"review_note":""},ensure_ascii=False))
    open(R+q+'.jsonl','w',encoding='utf-8').write('\n'.join(out)+'\n')
    print(q,len(out))
