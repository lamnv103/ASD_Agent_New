import json, sys, collections
sys.path.insert(0, "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_05")
from write_labels import parse, OUT
KEYS = ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
tot = collections.Counter(); nr = 0; problems = []
for q in ["q052", "q016", "q031"]:
    passages = parse(q)
    rows = [json.loads(l) for l in open(OUT + q + ".jsonl", encoding="utf-8") if l.strip()]
    codes = [r["annotation_code"] for r in rows]
    if len(codes) != len(set(codes)) or set(codes) != set(passages):
        problems.append(q + " code coverage mismatch")
    c = collections.Counter()
    for r in rows:
        if list(r.keys()) != KEYS: problems.append(q + " keys " + r["annotation_code"])
        g = r["grade"]
        if r["needs_review"]: nr += 1
        elif g not in (-1, 0, 1, 2, 3): problems.append(q + " grade " + r["annotation_code"])
        if g in (-1, 1, 2, 3) and (not r["evidence_span"] or r["evidence_span"] not in passages[r["annotation_code"]]):
            problems.append(q + " span " + r["annotation_code"])
        if g == 0 and r["evidence_span"] != "": problems.append(q + " span0 " + r["annotation_code"])
        c[g] += 1
    tot += c
    print(q, len(rows), "of", len(passages), dict(sorted(c.items(), key=lambda x: str(x[0]))))
print("total", dict(sorted(tot.items(), key=lambda x: str(x[0]))), "needs_review", nr, "problems", problems)
