import json,re,glob,os
base='../../returned/batch_14'
for qf in ['q003','q042','q022']:
    txt=open(qf+'.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',txt,flags=re.M)[1:]
    P={p.split(' |')[0]:p for p in parts}
    rows=[json.loads(l) for l in open(os.path.join(base,qf+'.jsonl'),encoding='utf-8') if l.strip()]
    codes=[r['annotation_code'] for r in rows]
    assert len(codes)==len(set(codes)), f"{qf} dup codes"
    assert set(codes)==set(P), f"{qf} code mismatch {set(codes)^set(P)}"
    for r in rows:
        g=r['grade']
        if r['needs_review']:
            assert g is None
            continue
        if g!=0:
            e=r['evidence_span']
            assert e and e in P[r['annotation_code']], (qf,r['annotation_code'],e)
    print(qf,'OK',len(rows))
