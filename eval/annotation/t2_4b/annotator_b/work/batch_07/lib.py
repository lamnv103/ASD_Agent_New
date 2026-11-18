import re,json,sys
def load(q):
    t=open(f'{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',t,flags=re.M)[1:]
    d={}
    for p in parts:
        h,_,body=p.partition('\n')
        d[h.split(' | ')[0].strip()]=body.strip()
    return d
def write(q,rows,n=160):
    d=load(q); out=[]; seen=set()
    for code,g,rat,start,*c in rows:
        conf=c[0] if c else 'high'
        body=d[code]; seen.add(code)
        span=''
        if g!=0:
            i=body.find(start)
            assert i>=0,(code,start)
            span=body[i:i+n]
            if len(span)==n:
                j=span.rfind(' '); span=span[:j] if j>60 else span
        out.append(dict(annotation_code=code,grade=g,rationale=rat,evidence_span=span,confidence=conf,needs_review=False,review_note=''))
    assert seen==set(d),(set(d)-seen,seen-set(d))
    assert len(rows)==len(d)
    p=f'../../returned/batch_07/{q}.jsonl'
    open(p,'w',encoding='utf-8').write(''.join(json.dumps(o,ensure_ascii=False)+'\n' for o in out))
    from collections import Counter
    print(q,len(out),sorted(Counter(o['grade'] for o in out).items()))
