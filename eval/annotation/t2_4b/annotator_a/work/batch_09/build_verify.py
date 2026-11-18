import json, os, re, subprocess, sys, importlib.util
from collections import Counter

BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
WORK = BASE + "/work/batch_09"
RET = BASE + "/returned/batch_09"
PY = "D:/AI4LIFE/ASD_AGENT_FINALL/.venv/Scripts/python"
HELPER = BASE + "/tools/show_question.py"
BATCH = BASE + "/batches/batch_09.jsonl"


def passages(qid):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run([PY, "-B", HELPER, BATCH, qid], capture_output=True, env=env).stdout.decode("utf-8")
    blocks = {}
    cur = None
    for line in out.split("\n"):
        m = re.match(r"^### ([0-9A-F]{10}) \|", line)
        if m:
            cur = m.group(1)
            blocks[cur] = []
        elif cur:
            blocks[cur].append(line)
    return {k: "\n".join(v) for k, v in blocks.items()}


def load(qid):
    spec = importlib.util.spec_from_file_location("l" + qid, f"{WORK}/labels_{qid}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.L


# build only questions without an existing returned file
for qid in sys.argv[1:]:
    path = f"{RET}/{qid}.jsonl"
    if os.path.exists(path):
        print("skip existing", qid)
        continue
    with open(path, "w", encoding="utf-8") as f:
        for code, g, rat, span, conf in load(qid):
            obj = {"annotation_code": code, "grade": g, "rationale": rat, "evidence_span": span,
                   "confidence": conf, "needs_review": False, "review_note": ""}
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print("wrote", qid)

# verify all
ok = True
for qid in ["q033", "q065", "q001"]:
    P = passages(qid)
    rows = [json.loads(l) for l in open(f"{RET}/{qid}.jsonl", encoding="utf-8") if l.strip()]
    codes = Counter(r["annotation_code"] for r in rows)
    probs = []
    if set(codes) != set(P):
        probs.append(f"code mismatch missing={set(P)-set(codes)} extra={set(codes)-set(P)}")
    probs += [f"dup {c}" for c, n in codes.items() if n != 1]
    keys = {"annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"}
    for r in rows:
        if set(r) != keys:
            probs.append(f"keys {r['annotation_code']}")
        g = r["grade"]
        if r["needs_review"]:
            if g is not None or not r["review_note"]:
                probs.append(f"nr {r['annotation_code']}")
        elif g not in (-1, 0, 1, 2, 3):
            probs.append(f"grade {r['annotation_code']}")
        if g in (-1, 1, 2, 3):
            if not r["evidence_span"] or r["evidence_span"] not in P.get(r["annotation_code"], ""):
                probs.append(f"span {r['annotation_code']}")
        if g == 0 and r["evidence_span"] != "":
            probs.append(f"span0 {r['annotation_code']}")
        if r["confidence"] not in ("high", "medium", "low"):
            probs.append(f"conf {r['annotation_code']}")
    dist = Counter(r["grade"] for r in rows)
    nr = sum(1 for r in rows if r["needs_review"])
    print(qid, len(P), "passages", len(rows), "labels", dict(sorted(dist.items(), key=lambda x: str(x[0]))), "needs_review", nr, "PROBLEMS:", probs or "none")
    ok = ok and not probs
print("ALL OK" if ok else "ERRORS")
