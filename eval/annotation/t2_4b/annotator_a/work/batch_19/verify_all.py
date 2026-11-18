import json, collections
base = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/"
items = collections.defaultdict(dict)
for line in open(base+"batches/batch_19.jsonl", encoding="utf-8"):
    o = json.loads(line); items[o["question_id"]][o["annotation_code"]] = o["content"]
req = ["annotation_code","grade","rationale","evidence_span","confidence","needs_review","review_note"]
for q, cand in sorted(items.items()):
    rows = [json.loads(l) for l in open(base+f"returned/batch_19/{q}.jsonl", encoding="utf-8") if l.strip()]
    cnt = collections.Counter(r["annotation_code"] for r in rows)
    probs = []
    if set(cnt) != set(cand) or any(v != 1 for v in cnt.values()): probs.append("code coverage mismatch")
    grades = collections.Counter()
    nr = 0
    extra = set()
    for r in rows:
        extra |= set(r) - set(req)
        if any(k not in r for k in req): probs.append(f"missing key {r['annotation_code']}")
        g = r["grade"]; grades[g] += 1
        if r["needs_review"]: nr += 1
        if g in (1,2,3,-1):
            es = r["evidence_span"]
            if not es or es not in cand.get(r["annotation_code"], ""): probs.append(f"span not substring {r['annotation_code']}")
        elif g is None and not r["needs_review"]: probs.append("null grade w/o review")
    print(q, len(rows), "/", len(cand), dict(sorted(grades.items(), key=lambda x: str(x[0]))), "needs_review", nr, "extra_keys", sorted(extra), probs or "OK")
