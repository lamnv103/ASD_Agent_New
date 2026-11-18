import json,re
from collections import Counter
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'
total_needs_review=0
for q in ['q019','q063','q024']:
    t=open(W+f'work/batch_12/{q}.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',t,flags=re.M)[1:]
    d={}
    for p in parts:
        code=p.split(' | ',1)[0].strip(); d[code]=p
    rows=[json.loads(l) for l in open(W+f'returned/batch_12/{q}.jsonl',encoding='utf-8') if l.strip()]
    codes=[r['annotation_code'] for r in rows]
    assert len(codes)==len(set(codes)), f"{q} dup codes"
    assert set(codes)==set(d), f"{q} mismatch: missing={set(d)-set(codes)} extra={set(codes)-set(d)}"
    for r in rows:
        if r['grade'] in (1,2,3,-1):
            assert r['evidence_span'] and r['evidence_span'] in d[r['annotation_code']], (q,r['annotation_code'],r['evidence_span'])
        if r.get('needs_review'):
            total_needs_review+=1
    print(q, 'OK', len(rows), sorted(Counter(r['grade'] for r in rows).items()))
print('needs_review total:', total_needs_review)
