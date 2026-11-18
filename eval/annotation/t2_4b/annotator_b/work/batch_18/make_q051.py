import json, io

rows = [
("4C4C3D2254",0,"Nói về triệu chứng tiêu hóa và mức độ ASD, không phải dấu hiệu chậm phát triển 4 tháng.","", "high"),
("6245449AA2",0,"Đặc điểm phát triển của trẻ mầm non trong nghiên cứu khác, không phải trẻ 4 tháng.","", "high"),
("38D1238C7C",1,"Liệt kê mốc xã hội-cảm xúc trẻ 4 tháng, dùng để so sánh phát hiện chậm.","Smiles on his own to get your attention","medium"),
("5E299268B8",0,"Bảng tổng hợp nghiên cứu về AAC, không liên quan.","", "high"),
("292D22AD9B",0,"Mô tả dấu hiệu kích động của trẻ chậm phát triển nói chung, không phải 4 tháng.","", "high"),
("1B541F32FE",1,"Giới thiệu mốc phát triển trẻ 4 tháng, không nêu dấu hiệu chậm cụ thể.","Learn about the developmental milestones that most babies do by four months of age.","medium"),
("4D6CF5C074",2,"Nêu rõ chậm mốc phát triển là dấu hiệu của ASD, áp dụng chung mọi tuổi.","A delay in any of these areas could be a sign of ASD or other developmental disability.","high"),
("233B690AB1",0,"Về can thiệp giao tiếp bằng âm nhạc, không liên quan dấu hiệu chậm 4 tháng.","", "high"),
("2BE58244FE",1,"Công cụ checklist theo dõi mốc 4 tháng, gián tiếp giúp phát hiện chậm.","Check the milestones your baby has reached by 4 months by completing a checklist","medium"),
("06CDC969A6",1,"Công cụ Bayley đánh giá chậm phát triển, bao gồm độ tuổi 4 tháng nhưng không cụ thể.","is used to identify developmental delays","medium"),
("DED4D36139",0,"Lời khuyên chăm sóc trẻ 2 tháng, không phải 4 tháng.","", "high"),
("0493A4C922",0,"Lời khuyên hoạt động cho trẻ 4 tháng, không nêu dấu hiệu chậm phát triển.","", "high"),
("EC1DEA020C",0,"Công cụ M-CHAT-R/F dùng cho trẻ lớn hơn (toddlers), không phải 4 tháng.","", "high"),
("1F2B3C7527",2,"Liệt kê mốc vận động trẻ 4 tháng, cơ sở nhận biết chậm phát triển.","Holds head steady without support when you are holding him","high"),
("8D0238A773",0,"Bảng tổng hợp nghiên cứu AAC, không liên quan.","", "high"),
("943DF3AA9C",2,"Liệt kê mốc nhận thức trẻ 4 tháng, cơ sở nhận biết chậm phát triển.","Looks at her hands with interest","high"),
("C1AB25A717",0,"Về công cụ đo giấc ngủ, không liên quan dấu hiệu chậm phát triển 4 tháng.","", "high"),
("D5806C014A",0,"Câu hỏi chia sẻ bác sĩ cho trẻ 2 tháng, không phải 4 tháng.","", "high"),
("F1833D6C69",0,"Phương pháp tuyển chọn thử nghiệm SenITA, không liên quan.","", "high"),
("DDCAAAA54C",0,"Lời khuyên hoạt động cho trẻ 4 tháng, không nêu dấu hiệu chậm.","", "high"),
("D7F48826DB",1,"Dấu hiệu ASD theo mốc tuổi khác (9-60 tháng), không có mốc 4 tháng.","Does not respond to name by 9 months of age","medium"),
("A2E4DE4400",1,"Chương trình theo dõi mốc phát triển chung, không nêu dấu hiệu cụ thể 4 tháng.","CDC has developed materials to help you track your child's developmental milestones","low"),
("E7CE0E9C08",2,"Liệt kê mốc ngôn ngữ trẻ 4 tháng, cơ sở nhận biết chậm phát triển.","Makes sounds like \u201coooo\u201d, \u201caahh\u201d (cooing)","high"),
("8E54BAB504",0,"Giới thiệu chương trình huấn luyện cho trẻ 2-9 tuổi, không phải 4 tháng.","", "high"),
("29007349B2",0,"Bảng đặc điểm nghiên cứu trẻ mầm non, không liên quan.","", "high"),
("14D4640A83",0,"Thảo luận phân loại can thiệp AAC, không liên quan.","", "high"),
("2FB83D7353",0,"Bảng tổng hợp nghiên cứu PECS/AAC, không liên quan.","", "high"),
("221DF6FA49",0,"Hướng dẫn giao tiếp cho trẻ chậm phát triển nói chung, không nêu dấu hiệu 4 tháng.","", "high"),
("BF81A6A7B1",0,"Lời khuyên hoạt động cho trẻ 6 tháng, không phải 4 tháng.","", "high"),
("D37F5595C5",0,"Bảng đặc điểm nghiên cứu trẻ mầm non, không liên quan.","", "high"),
("3F90707F6E",0,"Hiệu quả AAC ở trẻ tự kỷ, không liên quan dấu hiệu chậm phát triển.","", "high"),
("84397C9F09",0,"Cách trẻ chậm phát triển giao tiếp nói chung, không nêu dấu hiệu 4 tháng.","", "high"),
("05F8643E40",0,"Hàm ý lâm sàng của AAC, không liên quan.","", "high"),
("EBC52A239D",0,"Câu hỏi chia sẻ bác sĩ cho trẻ 15 tháng, không phải 4 tháng.","", "high"),
("AD10E9F621",0,"Giới thiệu dịch vụ can thiệp sớm cho trẻ 2 tháng, không phải 4 tháng.","", "high"),
("91F6567370",0,"Kết quả can thiệp dinh dưỡng/chăm sóc với phát triển, không liên quan dấu hiệu chậm 4 tháng.","", "high"),
("8C5CB3CC52",0,"Hình thức giao tiếp trẻ mầm non tự kỷ, không liên quan trẻ 4 tháng.","", "high"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_18/q051.jsonl"
with io.open(out_path, "w", encoding="utf-8") as f:
    for code, grade, rationale, span, conf in rows:
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
print("wrote", len(rows))
