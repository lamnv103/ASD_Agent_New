import json,re,sys
qid=sys.argv[1]
txt=open(f'{qid}.txt',encoding='utf-8').read()
parts=re.split(r'\n### ',txt)[1:]
P={p.split(' | ')[0].strip():p for p in parts}
exec(open(f'{qid}_labels.py',encoding='utf-8').read())  # defines L: code->(grade,rationale,span,conf), Z default zero codes
out=[]
for c in P:
    if c in L: g,r,s,cf=L[c]
    else: g,r,s,cf=0,"Đoạn không chứa thông tin trả lời câu hỏi.","","high"
    if g>0 or g==-1: assert s and s in P[c],(c,s)
    out.append(json.dumps({"annotation_code":c,"grade":g,"rationale":r,"evidence_span":s,"confidence":cf,"needs_review":False,"review_note":""},ensure_ascii=False))
assert set(L)<=set(P)
open(f'../../returned/batch_01/{qid}.jsonl','w',encoding='utf-8').write('\n'.join(out)+'\n')
from collections import Counter
print(len(P),Counter(json.loads(o)['grade'] for o in out))
