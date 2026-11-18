import sys,json,re,importlib.util
q=sys.argv[1]
base='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/'
spec=importlib.util.spec_from_file_location('lab',base+f'work/batch_09/lab_{q}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
txt=open(base+f'work/batch_09/{q}.txt',encoding='utf-8').read()
parts=re.split(r'^### ',txt,flags=re.M)[1:]
P={}
for p in parts:
    h,_,body=p.partition('\n'); P[h.split(' | ')[0].strip()]=h+'\n'+body
codes=list(P); got=[l[0] for l in m.L]
bad=False
if sorted(codes)!=sorted(got) or len(set(got))!=len(got): print('CODE MISMATCH',set(codes)^set(got)); bad=True
out=[]
for c,g,r,s,cf in m.L:
    if g>0 or g==-1:
        if not s or s not in P[c]: print('SPAN FAIL',c,s); bad=True
    out.append(json.dumps(dict(annotation_code=c,grade=g,rationale=r,evidence_span=s,confidence=cf,needs_review=False,review_note=''),ensure_ascii=False))
if not bad:
    open(base+f'returned/batch_09/{q}.jsonl','w',encoding='utf-8').write('\n'.join(out)+'\n'); print('written',q,len(out))
