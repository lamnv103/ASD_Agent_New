import json
from lib import load
tot=0
for q in ['q055','q052','q006','q053']:
    d=load(q); rows=[json.loads(l) for l in open(f'../../returned/batch_07/{q}.jsonl',encoding='utf-8')]
    codes=[r['annotation_code'] for r in rows]
    assert sorted(codes)==sorted(d) and len(set(codes))==len(codes),q
    for r in rows:
        assert set(r)=={'annotation_code','grade','rationale','evidence_span','confidence','needs_review','review_note'}
        if r['grade']==0: assert r['evidence_span']==''
        else: assert r['evidence_span'] and r['evidence_span'] in d[r['annotation_code']],(q,r['annotation_code'])
    tot+=len(rows)
print('ok',tot)
