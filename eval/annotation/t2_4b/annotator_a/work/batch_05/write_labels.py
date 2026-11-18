import json, sys, re
WD = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_05/"
OUT = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_05/"
def parse(q):
    txt = open(WD + q + ".txt", encoding="utf-8").read()
    parts = re.split(r"^### ([0-9A-F]{10}) \|[^\n]*\n", txt, flags=re.M)
    return {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}
def write(q, labels):
    passages = parse(q)
    codes = [l[0] for l in labels]
    assert len(codes) == len(set(codes)), "dup"
    assert set(codes) == set(passages), (set(passages) - set(codes), set(codes) - set(passages))
    with open(OUT + q + ".jsonl", "w", encoding="utf-8") as f:
        for code, grade, rat, span, conf in labels:
            if grade != 0:
                assert span and span in passages[code], (code, span)
            else:
                span = ""
            obj = {"annotation_code": code, "grade": grade, "rationale": rat, "evidence_span": span,
                   "confidence": conf, "needs_review": False, "review_note": ""}
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(q, len(labels), "ok")
