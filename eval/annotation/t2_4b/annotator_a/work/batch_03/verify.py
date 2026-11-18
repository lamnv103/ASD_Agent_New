import json, sys
sys.path.insert(0, "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_03")
from writer import passages, OUT
KEYS = ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
ok = True
for q in ["q012", "q034", "q035"]:
    ps = passages(q)
    rows = [json.loads(l) for l in open(f"{OUT}/{q}.jsonl", encoding="utf-8") if l.strip()]
    codes = [r["annotation_code"] for r in rows]
    if sorted(codes) != sorted(ps) or len(set(codes)) != len(codes):
        ok = False; print(q, "code problem")
    for r in rows:
        if list(r.keys()) != KEYS: ok = False; print(q, "keys", r)
        g = r["grade"]
        if r["needs_review"] is False and g not in (-1, 0, 1, 2, 3): ok = False; print("grade", r)
        if g in (-1, 1, 2, 3) and (not r["evidence_span"] or r["evidence_span"] not in ps[r["annotation_code"]]):
            ok = False; print("span", r["annotation_code"])
        if g == 0 and r["evidence_span"] != "": ok = False
    print(q, len(rows), len(ps))
print("OK" if ok else "FAIL")
