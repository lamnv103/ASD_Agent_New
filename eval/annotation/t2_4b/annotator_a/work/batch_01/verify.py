import json, sys
sys.path.insert(0, "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_01")
from common import parse, BASE
from collections import Counter
KEYS = ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
tot = Counter(); ok = True
for q in ["q055", "q061", "q066"]:
    parts = parse(q)
    rows = [json.loads(l) for l in open(f"{BASE}/returned/batch_01/{q}.jsonl", encoding="utf-8") if l.strip()]
    codes = [r["annotation_code"] for r in rows]
    if len(codes) != len(set(codes)) or set(codes) != set(parts): ok = False; print("code problem", q)
    for r in rows:
        if list(r.keys()) != KEYS: ok = False; print("keys", q, r["annotation_code"])
        g = r["grade"]
        if g not in (-1, 0, 1, 2, 3) or r["needs_review"]: ok = False; print("grade", q, r)
        if g != 0 and (not r["evidence_span"] or r["evidence_span"] not in parts[r["annotation_code"]]): ok = False; print("span", q, r["annotation_code"])
        if g == 0 and r["evidence_span"] != "": ok = False; print("span0", q)
        if r["confidence"] not in ("high", "medium", "low"): ok = False
        if len(r["evidence_span"]) > 260: print("long span", q, r["annotation_code"], len(r["evidence_span"]))
        tot[g] += 1
    print(q, len(rows), Counter(r["grade"] for r in rows))
print("ALL OK" if ok else "PROBLEMS", dict(tot))
