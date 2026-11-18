import json, sys, re, importlib.util, pathlib

WORK = pathlib.Path(r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_02")
OUT = pathlib.Path(r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_02")


def parse(qid):
    text = (WORK / f"{qid}.txt").read_text(encoding="utf-8-sig")
    passages = {}
    cur = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^### ([0-9A-F]{10}) \|", line)
        if m:
            if cur:
                passages[cur] = "\n".join(buf)
            cur = m.group(1)
            buf = []
        elif cur:
            buf.append(line)
    if cur:
        passages[cur] = "\n".join(buf)
    return passages


def main(qid):
    spec = importlib.util.spec_from_file_location("lab", WORK / f"labels_{qid}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    labels = mod.LABELS
    passages = parse(qid)
    problems = []
    codes = [l[0] for l in labels]
    if len(codes) != len(set(codes)):
        problems.append("duplicate codes")
    missing = set(passages) - set(codes)
    extra = set(codes) - set(passages)
    if missing:
        problems.append(f"missing {missing}")
    if extra:
        problems.append(f"extra {extra}")
    lines = []
    for code, grade, rat, span, conf in labels:
        if grade in (1, 2, 3, -1):
            if not span or span not in passages.get(code, ""):
                problems.append(f"span not found {code}: {span[:60]}")
        else:
            span = ""
        obj = {"annotation_code": code, "grade": grade, "rationale": rat,
               "evidence_span": span, "confidence": conf,
               "needs_review": False, "review_note": ""}
        lines.append(json.dumps(obj, ensure_ascii=False))
    if problems:
        print("PROBLEMS:", *problems, sep="\n")
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{qid}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    from collections import Counter
    print(qid, len(lines), "passages", len(passages), Counter(l[1] for l in labels))


if __name__ == "__main__":
    main(sys.argv[1])
