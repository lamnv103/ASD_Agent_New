import json, re, sys
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_18/'
R='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_18/'
def load(q):
    txt=open(W+q+'.txt',encoding='utf-8').read()
    parts=re.split(r'^### ([0-9A-F]{10}) \|[^\n]*\n',txt,flags=re.M)
    return {parts[i]:parts[i+1] for i in range(1,len(parts),2)}
def write(q,rows):
    c=load(q); out=[]
    codes=[r[0] for r in rows]
    assert sorted(codes)==sorted(c), (set(c)-set(codes), set(codes)-set(c))
    for code,g,rat,span,conf in rows:
        if g==0: assert span==''
        else: assert span and span in c[code], (code,span)
        out.append(json.dumps({"annotation_code":code,"grade":g,"rationale":rat,"evidence_span":span,"confidence":conf,"needs_review":False,"review_note":""},ensure_ascii=False))
    open(R+q+'.jsonl','w',encoding='utf-8').write('\n'.join(out)+'\n'); print(q,len(out))
