import json,sys
def write(qid, rows):
    out=f"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_15/{qid}.jsonl"
    with open(out,"w",encoding="utf-8") as f:
        for code,g,rat,ev,conf in rows:
            f.write(json.dumps({"annotation_code":code,"grade":g,"rationale":rat,"evidence_span":ev if g!=0 else "","confidence":conf,"needs_review":False,"review_note":""},ensure_ascii=False)+"\n")
    print(qid,len(rows))
