import json,re,sys
def parse(q):
    t=open(f'{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',t,flags=re.M)[1:]
    d={}
    for p in parts:
        code=p.split(' |',1)[0].strip()
        d[code]=p.split(chr(10),1)[1]
    return d
def write(q,labels):
    d=parse(q); out=[]; bad=0
    assert set(d)==set(labels),(set(d)^set(labels))
    for code,(g,r,s,c) in labels.items():
        if g==0: s=''
        elif s not in d[code]: print('BAD SPAN',code,s); bad+=1
        out.append(json.dumps(dict(annotation_code=code,grade=g,rationale=r,evidence_span=s,confidence=c,needs_review=False,review_note=''),ensure_ascii=False))
    if bad: sys.exit(1)
    open(f'../../returned/batch_05/{q}.jsonl','w',encoding='utf-8').write('\n'.join(out)+'\n')
    from collections import Counter
    print(q,len(out),sorted(Counter(v[0] for v in labels.values()).items()))
