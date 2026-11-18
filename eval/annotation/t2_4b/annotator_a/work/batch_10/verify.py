import sys, json, collections
sys.path.insert(0, "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_10")
from write_labels import parse, BASE
KEYS = ["annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"]
total = collections.Counter(); nr = 0; ok = True
for q in ["q008","q019","q050"]:
    passages = parse(q)
    rows = [json.loads(l) for l in open(f"{BASE}/returned/batch_10/{q}.jsonl", encoding="utf-8")]
    codes = [r["annotation_code"] for r in rows]
    if sorted(codes) != sorted(passages) or len(set(codes)) != len(codes):
        ok = False; print(q, "code mismatch")
    for r in rows:
        if list(r.keys()) != KEYS: ok = False; print(q, "keys", r)
        g = r["grade"]
        if r["needs_review"]:
            nr += 1
        else:
            if g not in (-1,0,1,2,3): ok = False; print(q, "grade", r)
            if g != 0 and (not r["evidence_span"] or r["evidence_span"] not in passages[r["annotation_code"]]):
                ok = False; print(q, "span", r["annotation_code"])
            if g == 0 and r["evidence_span"] != "": ok = False
        if r["confidence"] not in ("high","medium","low"): ok = False
    c = collections.Counter(r["grade"] for r in rows)
    total += c
    print(q, len(rows), dict(sorted(c.items(), key=lambda x: str(x[0]))))
print("TOTAL", sum(total.values()), dict(sorted(total.items(), key=lambda x: str(x[0]))), "needs_review", nr, "OK" if ok else "FAIL")
