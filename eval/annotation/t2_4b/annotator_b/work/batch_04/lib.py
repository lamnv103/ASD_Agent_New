import json, re, os
from collections import Counter

def run(q, rows, default_zero=None):
    d = os.path.dirname(os.path.abspath(__file__))
    txt = open(os.path.join(d, q + '.txt'), encoding='utf-8').read()
    parts = re.split(r'^### ', txt, flags=re.M)[1:]
    pas = {p.split(' | ', 1)[0].strip(): p for p in parts}
    rows = list(rows)
    if default_zero:
        have = {r[0] for r in rows}
        for c in pas:
            if c not in have:
                rows.append((c, 0, default_zero, '', 'high'))
    out = []; seen = set(); bad = 0
    for code, g, rat, span, conf in rows:
        assert code in pas, code
        assert code not in seen, code
        seen.add(code)
        if g in (1, 2, 3, -1):
            if span not in pas[code]:
                print('BAD SPAN', code); bad += 1
        else:
            span = ''
        out.append(dict(annotation_code=code, grade=g, rationale=rat, evidence_span=span,
                        confidence=conf, needs_review=False, review_note=''))
    miss = set(pas) - seen
    print(q, len(out), 'of', len(pas), 'missing', miss, 'bad', bad)
    if not miss and not bad:
        p = os.path.join(d, '..', '..', 'returned', 'batch_04', q + '.jsonl')
        with open(p, 'w', encoding='utf-8') as f:
            for o in out:
                f.write(json.dumps(o, ensure_ascii=False) + '\n')
        print(Counter(o['grade'] for o in out))
