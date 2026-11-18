import json, collections
from writer import parse
KEYS={"annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"}
tot=collections.Counter(); nr=0; ok=True
for q in ["q024","q014","q062"]:
    d=parse(q)
    rows=[json.loads(l) for l in open(f'../../returned/batch_07/{q}.jsonl',encoding='utf-8')]
    codes=[r["annotation_code"] for r in rows]
    c=collections.Counter(codes)
    if set(codes)!=set(d) or any(v!=1 for v in c.values()):
        ok=False; print("COVERAGE FAIL",q)
    g=collections.Counter()
    for r in rows:
        if set(r)!=KEYS: ok=False; print("KEYS",q,r["annotation_code"])
        if r["needs_review"]: nr+=1
        if r["grade"] in (1,2,3,-1):
            if not r["evidence_span"] or r["evidence_span"] not in d[r["annotation_code"]]:
                ok=False; print("SPAN FAIL",q,r["annotation_code"])
        elif r["grade"]==0 and r["evidence_span"]!="": ok=False; print("SPAN0",q)
        if r["confidence"] not in ("high","medium","low"): ok=False
        g[r["grade"]]+=1; tot[r["grade"]]+=1
    print(q,len(rows),dict(sorted(g.items())))
print("TOTAL",dict(sorted(tot.items())),"needs_review",nr,"OK" if ok else "FAIL")
