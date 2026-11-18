import json, io

rows = [
("F3F448C718",2,"Giới thiệu nghiên cứu tỷ lệ tự kỷ ở Việt Nam, mô tả bối cảnh nghiên cứu.","Autism spectrum disorders are increasing worldwide and in Vietnam.","high"),
("9AAC8DBA77",3,"Kết quả tổng quan về mức độ tham gia cộng đồng tự kỷ trong nghiên cứu VN.","The vast majority of studies did not state any autism community involvement","high"),
("18339B1D28",2,"Phát hiện cụ thể về yếu tố nguy cơ tự kỷ trong một nghiên cứu tại VN.","higher odds of ASD among children whose mothers worked as farmers","high"),
("37DF13B35F",3,"Tóm tắt tổng quan trực tiếp về bối cảnh nghiên cứu tự kỷ ở Việt Nam.","A total of 137 studies met our inclusion criteria.","high"),
("59E08D9E6F",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam, minh họa quy mô nghiên cứu.","Ha, Nguyen, Nguyen, and Tran Thien (2024)","medium"),
("345E2B755A",1,"Mô tả phương pháp trích xuất dữ liệu của tổng quan, không nêu hiện trạng cụ thể.","Data extraction was completed by the first author","medium"),
("B2010F0FDA",3,"Thảo luận xu hướng nghiên cứu tự kỷ tăng tại Việt Nam.","there has been a steady increase in autism research that focuses heavily on Services and Supports","high"),
("9F747141F8",2,"Thảo luận về sự tham gia cộng đồng tự kỷ trong nghiên cứu còn mơ hồ.","ambiguity was often found where studies recognised involvement of members of the autism community","medium"),
("FC8E9D7829",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Lo and Bui (2020)","medium"),
("357AE0220F",0,"Về hướng nghiên cứu tiêu hóa ASD nói chung, không liên quan Việt Nam.","", "high"),
("06768B7043",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Anh and H\u1eb1ng (2018)","medium"),
("E435336CC1",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam, bao gồm nghiên cứu gần đây.","Xu et al. (2025)","medium"),
("EC971AF5FD",0,"Về ADHD và lo âu ở ASD nói chung, không liên quan Việt Nam.","", "high"),
("36A937EA93",1,"Mô tả câu hỏi nghiên cứu của tổng quan, chưa nêu kết quả cụ thể.","Research question 1, the inquiry into the landscape of autism research","medium"),
("DE23E8572E",3,"Kết quả tỷ lệ tự kỷ cụ thể tại Việt Nam và so sánh quốc tế.","the prevalence of ASD among children aged 18\u201330 months in northern Vietnam was 0.752%","high"),
("DC06A114D3",1,"Bảng số liệu thô về quy mô mẫu nghiên cứu, thiếu diễn giải.","101-200","low"),
("1AE6ABE7E1",3,"Mô tả số liệu lịch sử về tự kỷ tại Việt Nam qua các năm.","the number of cases of ASD admitted to the National Pediatrics Hospital increased more than threefold during the period 2000\u20132007","high"),
("2F32E4D4C0",3,"Kết luận nghiên cứu về tỷ lệ tự kỷ và nhu cầu nghiên cứu thêm tại VN.","there is clearly also a need to develop more effective and more widely available early screening/detection, diagnosis and interventions programs for ASD in Vietnam","high"),
("C1062C79D7",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Pham-The et al. (2022)","medium"),
("6413664A46",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Bui (2017)","medium"),
("2DF37F8F7F",3,"Kết luận tổng quan: nghiên cứu tự kỷ tại Việt Nam đang được quan tâm ngày càng tăng.","autism research within Vietnamese cultural contexts is of increasing interest","high"),
("36B6716970",0,"Về bỏ trốn ở trẻ khuyết tật tại Mỹ, không liên quan Việt Nam.","", "high"),
("B406DED2E8",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Palmer et al. (2015)","medium"),
("724A3160F6",3,"Tóm tắt dễ hiểu về hiện trạng nghiên cứu tự kỷ tại Việt Nam.","most of this research was conducted in Viet Nam","high"),
("028B9D3E4F",3,"Thảo luận các chủ đề chính của nghiên cứu tự kỷ tại Việt Nam.","the centrality of family, the importance of school and education, and identifying a cause of autism","high"),
("F5937362FC",2,"Bối cảnh pháp lý về tự kỷ tại Việt Nam liên quan đến nghiên cứu và hỗ trợ.","Autism as a singular diagnosis is not legislatively recognised as a disability in Viet Nam","medium"),
("41EC7F5144",0,"Về bệnh đồng mắc tâm thần ở ASD nói chung, không liên quan Việt Nam.","", "high"),
("5A74DE3A80",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Phạm and Huỳnh (2017)","medium"),
("1B5CEE4C3C",3,"Thảo luận hạn chế về chất lượng nghiên cứu và bình duyệt tại Việt Nam.","the difficulty in determining the reliability of the peer review process in Vietnamese journals","high"),
("5AE8D535FE",1,"Bối cảnh văn hóa kỳ thị tự kỷ tại Việt Nam, không phải hiện trạng nghiên cứu.","due to the stigmatisation of autism in Viet Nam","medium"),
("5F55E8D194",0,"Về nghiên cứu ASD tại Mỹ do NIH tài trợ, không liên quan Việt Nam.","", "high"),
("33EC7D2BBD",0,"Về bệnh tự miễn ở ASD nói chung, không liên quan Việt Nam.","", "high"),
("FC007372D3",2,"Mô tả công cụ sàng lọc M-CHAT dùng trong nghiên cứu tại Việt Nam.","M-CHAT is currently being used as the main screening tool in clinical settings by physicians at the Vietnam National Pediatric Hospital","high"),
("F9884F853D",3,"Nêu rõ khoảng trống nghiên cứu: chưa có tổng quan về tự kỷ tại Việt Nam.","there exists no published review of autism in Vietnamese cultural contexts","high"),
("7E246D2252",3,"Kết quả mô tả đặc điểm các nghiên cứu tự kỷ tại Việt Nam.","Most studies were conducted in Viet Nam (87%, n = 120)","high"),
("BF5BDD43AD",2,"Bảng danh sách các nghiên cứu tự kỷ tại Việt Nam.","Thảo et al. (2022)","medium"),
("4D2AEE1380",3,"Khẳng định cần nghiên cứu tự kỷ tại Việt Nam nhiều hơn, nêu bối cảnh quốc gia.","A targeted inquiry into autism research in Vietnamese cultural contexts is lacking, but much needed.","high"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_18/q005.jsonl"
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
