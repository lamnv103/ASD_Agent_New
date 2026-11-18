import json, io

rows = [
("F794748D17",1,"Giới thiệu mục tiêu thử nghiệm SenITA, chưa phải kết quả.","to evaluate the clinical effectiveness of manualised ASI therapy","medium"),
("CE5B71C754",2,"Kết quả về số buổi điều trị và an toàn của thử nghiệm.","The median number of SIT sessions received was 20 (IQR 16 \u201321).","high"),
("66F0F321A0",0,"Thuộc thử nghiệm ASSSIST-2 khác, không phải SenITA.","", "high"),
("CF4A2A0BA0",3,"Nêu trực tiếp kết luận kết quả thử nghiệm SenITA.","the results of the SenITA trial indicate that SIT shows no clinical benefit across a range of outcomes","high"),
("7B323CCBBE",0,"Mô tả thu thập dữ liệu định tính, không phải kết quả.","", "high"),
("66FDFE543E",1,"Chỉ nêu số lượng mẫu tham gia, không phải kết quả hiệu quả.","Control arm, n = 69; intervention arm, n = 69; all participants, n = 138.","medium"),
("A1B7278139",0,"Mô tả quy trình thu thập dữ liệu can thiệp, không phải kết quả.","", "high"),
("60B7954930",0,"Thuộc thử nghiệm ASSSIST-2 khác, không phải SenITA.","", "high"),
("43DB34DFE5",3,"Tóm tắt kết quả và kết luận chính của thử nghiệm SenITA.","The intervention did not demonstrate clinical benefit above standard care.","high"),
("ED57D41569",0,"Đoạn văn bị cắt không có nội dung kết quả.","", "high"),
("D76928E84E",0,"Thuộc nghiên cứu khác về can thiệp phụ huynh, không phải SenITA.","", "high"),
("9C80594383",1,"Thảo luận điểm mạnh và mục tiêu đo lường, chưa nêu số liệu kết quả.","The trial was sufficiently powered to determine effectiveness of manualised SIT on the primary outcome","medium"),
("65D52D34E4",1,"Tóm tắt khoa học mô tả bối cảnh và mục tiêu, chưa có kết quả cụ thể.","Outcomes, which were assessed at 6 and 12 months, included behavioural, functional and socialisation outcomes","medium"),
("AFA6AA7354",0,"Mô tả quy trình phỏng vấn người chăm sóc, không phải kết quả.","", "high"),
("7EF9E22871",3,"Tóm tắt chi tiết các kết quả chính của thử nghiệm SenITA.","there were, however, no statistically significant effects of SIT on any behavioural, functional, qualityof-life or well-being outcomes","high"),
("B651749CAB",1,"Chỉ nêu số liệu bệnh đồng mắc thiếu, không phải kết quả hiệu quả.","Comorbidities of interest are ADHD, ID or other neurodevelopmental/genetic conditions.","low"),
("7546B7C900",0,"Mục lục tóm tắt của báo cáo, không chứa kết quả.","", "high"),
("F22E038BDD",0,"Trải nghiệm người chăm sóc về thông tin thử nghiệm, không phải kết quả hiệu quả.","", "high"),
("7126F9F6C9",3,"Kết luận trực tiếp: không có hiệu quả can thiệp chính được quan sát.","No main intervention effects were observed, and sensitivity analyses did not alter the interpretation of results.","high"),
("1ED2A6D8D6",0,"Mô tả quy trình đồng ý tham gia, không phải kết quả.","", "high"),
("8797629106",1,"Tiêu chí tiến triển của pilot nội bộ được đáp ứng, kết quả phụ.","Formal progression criteria relating to recruitment and retention were met.","medium"),
("1C9437F042",0,"Lý do người chăm sóc tham gia thử nghiệm, không phải kết quả.","", "high"),
("BD9623EDDF",0,"Mô tả phương pháp thống kê, không phải kết quả cụ thể.","", "high"),
("893420DFBC",0,"Thông tin chung về thử nghiệm lâm sàng, không liên quan SenITA.","", "high"),
("C14417E948",0,"Mô tả giám sát và đào tạo thử nghiệm, không phải kết quả.","", "high"),
("9DF1AED825",0,"Thuộc thử nghiệm iBASIS-VIPP khác, không phải SenITA.","", "high"),
("D7692ED874",0,"Tiêu chí loại trừ và quy trình đồng ý, không phải kết quả.","", "high"),
("70137C0998",0,"Mô tả thiết kế thử nghiệm, không phải kết quả.","", "high"),
("57194BCD19",0,"Thuộc thử nghiệm iBASIS khác, không phải SenITA.","", "high"),
("006703356A",1,"Mô tả thiết kế và outcome đo lường, chưa có số liệu kết quả.","The primary outcome was irritability/agitation (as measured by the corresponding Aberrant Behavior Checklist subscale)","medium"),
("4BEA2B5042",2,"Kết quả độ trung thực can thiệp và mức độ hài lòng của người chăm sóc.","144 (92.3%) participants achieved a Global Impression Score of 1","high"),
("4B8887305F",0,"Danh mục mục quy trình nghiên cứu, không phải kết quả.","", "high"),
("17211E2188",0,"Mô tả phương pháp phân tích dữ liệu, không phải kết quả.","", "high"),
("7FA589F080",0,"Giới thiệu chương đánh giá pilot nội bộ, không phải kết quả.","", "high"),
("2463A78255",3,"Tóm tắt điểm mạnh/hạn chế và kết luận kết quả thử nghiệm.","the results suggest that SIT did not demonstrate clinical benefit across a range of outcomes","high"),
("4443FD5E72",2,"Kết quả tỉ lệ duy trì tham gia theo dõi của thử nghiệm.","Of 138 participants, 107 (77.5%) provided follow-up data at this time point.","high"),
("BB6F386DC2",0,"Mô tả phương pháp xây dựng mục tiêu can thiệp, không phải kết quả.","", "high"),
("CA3C0FF50F",0,"Định nghĩa SPD và công cụ đánh giá, không phải kết quả.","", "high"),
("61DE53023F",2,"Kết quả độ trung thực quy trình can thiệp đạt ngưỡng.","The SIT delivered in the SenITA trial met fidelity, with 10 out of 12 therapists scoring, on average, at least 80 out of 100","high"),
("EBA0ACDE74",1,"Kết quả khảo sát về chăm sóc thông thường, không phải hiệu quả can thiệp.","the SenITA trial intervention was significantly different from usual care in trial regions","medium"),
("F5B37275FC",0,"Tiêu chí lựa chọn tham gia, không phải kết quả.","", "high"),
("5385AAA5A1",0,"Trải nghiệm người chăm sóc và vấn đề kỹ thuật, không phải kết quả hiệu quả.","", "high"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_18/q044.jsonl"
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
