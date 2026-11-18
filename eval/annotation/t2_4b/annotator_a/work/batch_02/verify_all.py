import json, pathlib, sys
from collections import Counter
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from write_labels import parse, OUT

KEYS = ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
total = Counter()
ok = True
for q in ["q038", "q021", "q051"]:
    passages = parse(q)
    rows = [json.loads(l) for l in (OUT / f"{q}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    codes = [r["annotation_code"] for r in rows]
    if sorted(codes) != sorted(passages) or len(codes) != len(set(codes)):
        ok = False; print(q, "code mismatch")
    for r in rows:
        if list(r.keys()) != KEYS:
            ok = False; print(q, "keys", r["annotation_code"])
        g = r["grade"]
        if g not in (-1, 0, 1, 2, 3):
            ok = False; print(q, "grade", r["annotation_code"])
        if g in (-1, 1, 2, 3) and (not r["evidence_span"] or r["evidence_span"] not in passages[r["annotation_code"]]):
            ok = False; print(q, "span", r["annotation_code"])
        if g == 0 and r["evidence_span"] != "":
            ok = False; print(q, "span on 0", r["annotation_code"])
    c = Counter(r["grade"] for r in rows)
    total += c
    print(q, len(rows), dict(sorted(c.items())), "needs_review", sum(r["needs_review"] for r in rows))
print("TOTAL", dict(sorted(total.items())), "OK" if ok else "FAIL")
