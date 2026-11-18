import json, io, sys
sys.path.insert(0, "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_04")
from common import parse, OUT
KEYS = ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
ok = True
for q in ["q032", "q044", "q039"]:
    p = parse(q)
    rows = [json.loads(l) for l in io.open(f"{OUT}/{q}.jsonl", encoding="utf-8") if l.strip()]
    codes = [r["annotation_code"] for r in rows]
    if sorted(codes) != sorted(p) or len(set(codes)) != len(codes):
        ok = False; print(q, "code mismatch")
    for r in rows:
        if list(r.keys()) != KEYS: ok = False; print(q, "keys", r["annotation_code"])
        if r["grade"] not in (-1, 0, 1, 2, 3): ok = False; print(q, "grade", r)
        if r["grade"] != 0 and r["evidence_span"] not in p[r["annotation_code"]]: ok = False; print(q, "span", r["annotation_code"])
        if r["grade"] != 0 and not r["evidence_span"]: ok = False
        if r["grade"] == 0 and r["evidence_span"] != "": ok = False
        if r["confidence"] not in ("high", "medium", "low"): ok = False
    print(q, len(rows), "rows")
print("ALL OK" if ok else "PROBLEMS")
