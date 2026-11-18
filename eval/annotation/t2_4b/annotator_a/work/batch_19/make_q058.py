import json
codes = """3F9EEBE2DA A3866CCBD4 CC6061C382 1E0BFFBE62 28CA134CA8 6EF1D37280 0440FDD2E6 BAF3D6DAAB 38842129E2 288798D129 D507F5FAB4 611F62233F 7FDAAF414D C38B2C52ED 5D7C32F39A 78B2206117 8C9AF85F3A 867DFB2E3A C8CA8BB0CC 73F19EBFC8 23FCA96F6C 6067E5211B 596BBEC1D4 0DD98ED7E3 89C6ED89D3 91BA4533CB 34076FD7DC 2DB811FA5E 113022146B 3FAC8EE555 019D0A3447 778B1016FB""".split()
special = {
 "34076FD7DC": "Chỉ nhắc risperidone dùng off-label cho giấc ngủ, không có liều.",
}
melatonin = {"3F9EEBE2DA","A3866CCBD4","CC6061C382","1E0BFFBE62","BAF3D6DAAB","5D7C32F39A","6067E5211B","596BBEC1D4","019D0A3447"}
out = []
for c in codes:
    if c in special:
        r = special[c]; conf = "medium"
    elif c in melatonin:
        r = "Nói về liều melatonin, không phải risperidone."; conf = "high"
    else:
        r = "Không đề cập risperidone hay liều risperidone cho trẻ."; conf = "high"
    out.append({"annotation_code": c, "grade": 0, "rationale": r, "evidence_span": "", "confidence": conf, "needs_review": False, "review_note": ""})
with open("D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_19/q058.jsonl","w",encoding="utf-8") as f:
    for o in out: f.write(json.dumps(o, ensure_ascii=False)+"\n")
print(len(out))
