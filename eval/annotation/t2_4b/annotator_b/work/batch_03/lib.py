import json, re
from collections import Counter
B = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'


def passages(q):
    t = open(B + f'work/batch_03/{q}.txt', encoding='utf-8').read()
    parts = re.split(r'^### ', t, flags=re.M)[1:]
    d = {}
    for p in parts:
        code = p.split(' |', 1)[0].strip()
        d[code] = p.split('\n', 1)[1]
    return d


def write(q, rows):
    d = passages(q)
    out = []
    seen = set()
    for code, g, rat, span, conf in rows:
        assert code in d, code
        assert code not in seen, code
        seen.add(code)
        if g in (1, 2, 3, -1):
            assert span and span in d[code], (code, span)
        else:
            span = ""
        out.append(json.dumps(dict(annotation_code=code, grade=g, rationale=rat, evidence_span=span,
                                   confidence=conf, needs_review=False, review_note=""), ensure_ascii=False))
    assert seen == set(d), (set(d) - seen)
    open(B + f'returned/batch_03/{q}.jsonl', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(q, len(out), sorted(Counter(json.loads(x)['grade'] for x in out).items()))
