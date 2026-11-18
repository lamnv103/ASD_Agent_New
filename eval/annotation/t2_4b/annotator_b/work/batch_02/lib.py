import re, json, sys
BASE='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'
def passages(q):
    t=open(BASE+f'work/batch_02/{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ([0-9A-F]{10}) \|[^\n]*\n',t,flags=re.M)
    return {parts[i]:parts[i+1] for i in range(1,len(parts),2)}
def write(q,labels):
    P=passages(q); out=[]; bad=[]
    for code,(g,rat,span,conf) in labels.items():
        if code not in P: bad.append(('nocode',code)); continue
        if g in (1,2,3,-1) and span not in P[code]: bad.append(('span',code,span))
        if g==0: span=''
        out.append(dict(annotation_code=code,grade=g,rationale=rat,evidence_span=span,confidence=conf,needs_review=False,review_note=''))
    miss=set(P)-set(labels)
    print(q,len(P),len(out),'missing',miss,'bad',bad)
    if not bad and not miss:
        with open(BASE+f'returned/batch_02/{q}.jsonl','w',encoding='utf-8') as f:
            for o in out: f.write(json.dumps(o,ensure_ascii=False)+'\n')
        from collections import Counter; print(Counter(o['grade'] for o in out))
