import json, re, sys, os
W = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_08"
R = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_08"
def passages(qid):
    txt = open(f"{W}/{qid}.txt", encoding="utf-8").read()
    parts = re.split(r"^### ", txt, flags=re.M)[1:]
    out = {}
    for p in parts:
        head, _, body = p.partition("\n")
        code = head.split(" | ")[0].strip()
        out[code] = body
    return out
def write(qid, labels):
    ps = passages(qid)
    errs = []
    codes = [l[0] for l in labels]
    if sorted(codes) != sorted(ps) or len(set(codes)) != len(codes):
        errs.append(f"code mismatch: missing={set(ps)-set(codes)} extra={set(codes)-set(ps)} dup={len(codes)-len(set(codes))}")
    lines = []
    for code, grade, rat, span, conf in labels:
        if grade in (1,2,3,-1):
            if not span or span not in ps.get(code, ""):
                errs.append(f"span not found {code}: {span[:60]}")
        else:
            span = ""
        lines.append(json.dumps({"annotation_code": code, "grade": grade, "rationale": rat, "evidence_span": span, "confidence": conf, "needs_review": False, "review_note": ""}, ensure_ascii=False))
    if errs:
        print("\n".join(errs)); sys.exit(1)
    os.makedirs(R, exist_ok=True)
    open(f"{R}/{qid}.jsonl", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(qid, "written", len(lines))
