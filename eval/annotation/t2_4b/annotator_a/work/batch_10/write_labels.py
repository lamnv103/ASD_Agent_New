import json, re, sys, os
BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
def parse(qid):
    txt = open(f"{BASE}/work/batch_10/{qid}.txt", encoding="utf-8").read()
    parts = re.split(r"^### ", txt, flags=re.M)[1:]
    d = {}
    for p in parts:
        header, _, body = p.partition("\n")
        code = header.split(" | ")[0].strip()
        d[code] = body
    return d
def write(qid, labels):
    passages = parse(qid)
    out = []
    seen = set()
    for code, grade, rat, span, conf in labels:
        assert code in passages, code
        assert code not in seen, code
        seen.add(code)
        if grade == 0: span = ""
        else:
            assert span and span in passages[code], (code, span)
        out.append({"annotation_code": code, "grade": grade, "rationale": rat, "evidence_span": span, "confidence": conf, "needs_review": False, "review_note": ""})
    missing = set(passages) - seen
    assert not missing, missing
    os.makedirs(f"{BASE}/returned/batch_10", exist_ok=True)
    with open(f"{BASE}/returned/batch_10/{qid}.jsonl", "w", encoding="utf-8") as f:
        for o in out: f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(qid, len(out), "written")
