import json, re
def parse(path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'^### ', txt, flags=re.M)[1:]
    m = {}
    for p in parts:
        header, _, body = p.partition('\n')
        code = header.split(' | ')[0].strip()
        m[code] = body
    return m
def write(qid, labels):
    content = parse(qid + '.txt')
    out = []
    for code, g, rat, span, conf in labels:
        assert code in content, code
        if g == 0: span = ''
        else: assert span and span in content[code], (code, span)
        out.append(json.dumps({"annotation_code": code, "grade": g, "rationale": rat, "evidence_span": span,
            "confidence": conf, "needs_review": False, "review_note": ""}, ensure_ascii=False))
    assert len(labels) == len(content) == len({l[0] for l in labels}), (len(labels), len(content))
    open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_12/%s.jsonl' % qid, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(qid, len(out))
