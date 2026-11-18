import json, re, sys, io
BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
WORK = BASE + "/work/batch_04"
OUT = BASE + "/returned/batch_04"


def parse(qid):
    txt = io.open(f"{WORK}/{qid}.txt", encoding="utf-8-sig").read()
    parts = re.split(r"^### ", txt, flags=re.M)
    res = {}
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        code = head.split("|")[0].strip()
        res[code] = body
    return res


def write(qid, labels):
    passages = parse(qid)
    errs = []
    if set(labels) != set(passages):
        errs.append(("code mismatch", set(passages) - set(labels), set(labels) - set(passages)))
    lines = []
    for code in passages:
        if code not in labels:
            continue
        g, rat, span, conf = labels[code]
        if g in (1, 2, 3, -1):
            if not span or span not in passages[code]:
                errs.append(("span not found", code, span))
        else:
            span = ""
        obj = {"annotation_code": code, "grade": g, "rationale": rat, "evidence_span": span,
               "confidence": conf, "needs_review": False, "review_note": ""}
        lines.append(json.dumps(obj, ensure_ascii=False))
    if errs:
        for e in errs:
            print("ERROR", e)
        sys.exit(1)
    io.open(f"{OUT}/{qid}.jsonl", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    from collections import Counter
    print(qid, len(lines), Counter(labels[c][0] for c in labels))
