import sys,re,json,os
def run(q,labels):
    txt=open(f'{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',txt,flags=re.M)[1:]
    pas={}
    for p in parts:
        head,_,body=p.partition('\n')
        pas[head.split(' | ')[0].strip()]=body
    os.makedirs('../../returned/batch_11',exist_ok=True)
    out=[]
    for c in pas:
        g,rat,ev,conf=labels.get(c,(0,'Đoạn không đề cập đến nội dung câu hỏi hỏi.','','high'))
        if g!=0: assert ev in pas[c],(c,ev)
        else: ev=''
        out.append(dict(annotation_code=c,grade=g,rationale=rat,evidence_span=ev,confidence=conf,needs_review=False,review_note=''))
    for c in labels: assert c in pas,c
    with open(f'../../returned/batch_11/{q}.jsonl','w',encoding='utf-8') as f:
        for o in out: f.write(json.dumps(o,ensure_ascii=False)+'\n')
    from collections import Counter
    print(q,len(out),sorted(Counter(o['grade'] for o in out).items()))
