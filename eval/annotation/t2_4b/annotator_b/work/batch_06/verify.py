import sys,json,glob
sys.path.insert(0,'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_06')
from lab import parse,W
from collections import Counter
tot=Counter(); n=0
for f in sorted(glob.glob(W+'returned/batch_06/*.jsonl')):
    q=f.replace(chr(92),'/').split('/')[-1][:-6]
    d=parse(q); rows=[json.loads(l) for l in open(f,encoding='utf-8')]
    codes=[r['annotation_code'] for r in rows]
    assert sorted(codes)==sorted(d) and len(set(codes))==len(codes)
    for r in rows:
        assert r['grade'] is not None and not r['needs_review']
        assert r['grade']==0 or r['evidence_span'] in d[r['annotation_code']]
        tot[r['grade']]+=1
    n+=len(rows)
    print(q,len(rows),'ok')
print(n,sorted(tot.items()))
