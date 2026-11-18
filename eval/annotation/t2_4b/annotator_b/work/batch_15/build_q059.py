import json

codes = ["9A5DF5F947","7E22C7EAA3","3CCC2EE6CA","84C4827E8C","F73A226DEB","2FDDD54E90",
"480D2364B8","9EF134094A","FF2E77F1F9","A44AFD0298","9A3EBBC32D","E59DA0922F",
"33E97A3269","C00B47B20D","86A4B9E84D","4A0517F238","0D35C1614E","2583264657",
"4EE252CBB0","EB9C484A86","DB74C425D1","EA32D8C893","FE59A4C231","81FEE6DD18",
"D067B5E6A3","A5D3D6FFE6","08C26ECF7A","95B98C0BE1","468A531DE1","54302C8FEA",
"C72EF37C73","316BD3BCD0","3711BDB2FD","C9585C86ED","4820E36D34","8AA558A4EB",
"A0E538371D","B8CF42F271","41084BA116"]

special = {
 "C00B47B20D": (1,"Nói không có thuốc chữa triệu chứng cốt lõi của tự kỷ, bối cảnh gián tiếp cho câu hỏi chữa khỏi.","There are no medications that treat the core symptoms of ASD.","medium"),
}

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_15/q059.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for code in codes:
        if code in special:
            grade, rationale, span, conf = special[code]
        else:
            grade, rationale, span, conf = 0, "Không đề cập tế bào gốc hay việc chữa tự kỷ bằng phương pháp này.", "", "medium"
        obj = {
            "annotation_code": code,
            "grade": grade,
            "rationale": rationale,
            "evidence_span": span,
            "confidence": conf,
            "needs_review": False,
            "review_note": ""
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
print("wrote", len(codes), "rows")
