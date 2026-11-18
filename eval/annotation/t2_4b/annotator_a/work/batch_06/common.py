import json, re, sys, os
BASE = "D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a"
def parse(qid):
    txt = open(f"{BASE}/work/batch_06/{qid}.txt", encoding="utf-8").read()
    parts = re.split(r"^### ", txt, flags=re.M)[1:]
    out = {}
    for p in parts:
        head, _, body = p.partition("\n")
        code = head.split(" | ")[0].strip()
        out[code] = body
    return out
def fix(span, body):
    if span in body: return span
    pat = "".join(r"[    ]" if ch == " " else re.escape(ch) for ch in span)
    m = re.search(pat, body)
    return m.group(0) if m else span
def write(qid, labels):
    passages = parse(qid)
    codes = [l[0] for l in labels]
    assert len(codes) == len(set(codes)), "dup"
    missing = set(passages) - set(codes); extra = set(codes) - set(passages)
    assert not missing and not extra, (missing, extra)
    lines = []
    for code, grade, rat, span, conf in labels:
        if grade == 0: span = ""
        else:
            span = fix(span, passages[code])
            assert span and span in passages[code], (code, span)
        lines.append(json.dumps({"annotation_code": code, "grade": grade, "rationale": rat,
            "evidence_span": span, "confidence": conf, "needs_review": False, "review_note": ""}, ensure_ascii=False))
    os.makedirs(f"{BASE}/returned/batch_06", exist_ok=True)
    open(f"{BASE}/returned/batch_06/{qid}.jsonl", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(qid, len(lines), "written")
