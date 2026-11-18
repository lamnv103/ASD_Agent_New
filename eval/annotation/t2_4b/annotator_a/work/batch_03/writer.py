import json, os, re, subprocess, sys, importlib.util

BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
PY = "D:/AI4LIFE/ASD_AGENT_FINALL/.venv/Scripts/python"
TOOL = BASE + "/tools/show_question.py"
BATCH = BASE + "/batches/batch_03.jsonl"
OUT = BASE + "/returned/batch_03"
WORK = BASE + "/work/batch_03"


def passages(qid):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run([PY, "-B", TOOL, BATCH, qid], capture_output=True, env=env).stdout.decode("utf-8")
    parts = re.split(r"^### ([0-9A-F]{10}) \|[^\n]*\n", out, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def write(qid, labels):
    ps = passages(qid)
    codes = [l[0] for l in labels]
    errs = []
    if sorted(codes) != sorted(ps.keys()) or len(set(codes)) != len(codes):
        errs.append(("code mismatch", set(ps) ^ set(codes), len(codes), len(set(codes))))
    lines = []
    for code, grade, rat, ev, conf, *rest in labels:
        nr = bool(rest and rest[0])
        note = rest[1] if len(rest) > 1 else ""
        if grade in (1, 2, 3, -1):
            if not ev or ev not in ps.get(code, ""):
                errs.append(("evidence not found", code, ev))
            if len(ev) > 300:
                errs.append(("evidence long", code))
        else:
            ev = ""
        obj = {"annotation_code": code, "grade": None if nr else grade, "rationale": rat,
               "evidence_span": ev, "confidence": conf, "needs_review": nr, "review_note": note}
        lines.append(json.dumps(obj, ensure_ascii=False))
    if errs:
        for e in errs:
            print("ERR", e)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/{qid}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    from collections import Counter
    print(qid, len(lines), Counter(l[1] for l in labels))


if __name__ == "__main__":
    qid = sys.argv[1]
    spec = importlib.util.spec_from_file_location("lab", f"{WORK}/labels_{qid}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    write(qid, m.LABELS)
