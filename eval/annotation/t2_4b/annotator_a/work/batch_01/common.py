import json, sys, re, os
BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
def parse(qid):
    txt = open(f"{BASE}/work/batch_01/{qid}.txt", encoding="utf-8").read()
    parts = {}
    cur = None; buf = []
    for line in txt.split("\n"):
        if line.startswith("### "):
            if cur: parts[cur] = "\n".join(buf)
            cur = line[4:].split(" | ")[0].strip(); buf = []
        elif cur is not None:
            buf.append(line)
    if cur: parts[cur] = "\n".join(buf)
    return parts
def write(qid, labels):
    parts = parse(qid)
    codes = [l[0] for l in labels]
    errs = []
    if sorted(codes) != sorted(parts): errs.append(("code mismatch", set(parts)-set(codes), set(codes)-set(parts), len(codes), len(set(codes))))
    out = []
    for code, g, rat, span, conf in labels:
        if g == 0: span = ""
        else:
            if not span or span not in parts.get(code, ""): errs.append(("span", code, span[:60]))
        out.append({"annotation_code": code, "grade": g, "rationale": rat, "evidence_span": span, "confidence": conf, "needs_review": False, "review_note": ""})
    if errs:
        for e in errs: print("ERR", e)
        sys.exit(1)
    os.makedirs(f"{BASE}/returned/batch_01", exist_ok=True)
    with open(f"{BASE}/returned/batch_01/{qid}.jsonl", "w", encoding="utf-8") as f:
        for o in out: f.write(json.dumps(o, ensure_ascii=False) + "\n")
    from collections import Counter
    print(qid, len(out), Counter(o["grade"] for o in out))
