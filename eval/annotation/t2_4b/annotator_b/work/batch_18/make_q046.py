import json, io

rows = [
("FB77368AA7",0,"Nói về mốc phát triển 2 tháng tuổi, không phải 2 tuổi.","", "high"),
("4A2754492D",0,"Bảng mô tả các chương trình can thiệp phụ huynh, không liệt kê kỹ năng trẻ 2 tuổi.","", "high"),
("7B746F1EFD",1,"Mốc 30 tháng, gần nhưng không đúng 2 tuổi, chỉ tham khảo.","Shows simple problem-solving skills, like standing on a small stool to reach something","medium"),
("0B09058399",1,"Mô tả hành vi chơi của trẻ 2 tuổi nhưng là lời khuyên cho phụ huynh.","Children this age play next to each other, but do not know how to share and solve problems.","medium"),
("836416E9FD",0,"Nói về thiết kế thử nghiệm can thiệp sớm, không liệt kê kỹ năng trẻ 2 tuổi.","", "high"),
("427A3166E6",0,"Câu chung về mốc phát triển, thuộc trang mốc 2 tháng, không trả lời trực tiếp.","", "high"),
("5E4D96E08E",2,"Giới thiệu trực tiếp mốc phát triển trẻ 2 tuổi, dù không liệt kê chi tiết.","Learn about the developmental milestones that most children do by 2 years of age.","high"),
("34BCF18540",0,"Nói về thang đo IQ Wechsler, không liên quan khả năng trẻ 2 tuổi.","", "high"),
("408ED99647",0,"Bảng đặc điểm người tham gia nghiên cứu, không liên quan.","", "high"),
("D6EB510651",0,"Nói về sàng lọc tự kỷ ở trẻ sinh non, không mô tả khả năng trẻ 2 tuổi nói chung.","", "high"),
("CA17A2DCD0",0,"Mô tả công cụ đánh giá nhận thức DAS-II, không liên quan.","", "high"),
("2391D32E74",1,"Lời khuyên hoạt động cho trẻ 2 tuổi, gián tiếp gợi ý khả năng của trẻ.","Limit screen time (TV, tablets, phones, etc.) to no more than 1 hour a day of a children's program with an adult present.","medium"),
("CBFEB3F226",1,"Lời khuyên chăm sóc, có thông tin gián tiếp về khả năng tập ngồi bô.","Most children are not able to toilet train until 2 to 3 years old.","medium"),
("32D7DFFA4A",3,"Liệt kê trực tiếp kỹ năng vận động trẻ 2 tuổi thường làm được.","Kicks a ball","high"),
("20BA7A40B5",0,"Nói về bệnh đồng mắc và dịch tễ tự kỷ, không liên quan câu hỏi.","", "high"),
("8F79484058",0,"Thảo luận điểm mạnh/hạn chế nghiên cứu can thiệp, không liên quan.","", "high"),
("3F3E28483A",0,"Câu hỏi chia sẻ với bác sĩ cho trẻ 2 tháng, không liên quan trẻ 2 tuổi.","", "high"),
("6041955C29",0,"Mốc ngôn ngữ trẻ 2 tháng, không phải 2 tuổi.","", "high"),
("EC02995071",3,"Liệt kê trực tiếp mốc ngôn ngữ trẻ 2 tuổi thường làm được.","Says at least two words together, like \u201cMore milk.\u201d","high"),
("44A57A55F6",0,"Bảng thông tin người tham gia nghiên cứu giáo dục, không liên quan.","", "high"),
("47C64C7161",0,"Kết quả thử nghiệm can thiệp sớm, không mô tả khả năng trẻ 2 tuổi.","", "high"),
("4352A4A836",3,"Liệt kê trực tiếp mốc xã hội-cảm xúc trẻ 2 tuổi thường làm được.","Notices when others are hurt or upset, like pausing or looking sad when someone is crying","high"),
("8947D81A02",0,"Trang mốc phát triển trẻ 2 tháng, không phải 2 tuổi.","", "high"),
("980BC47699",0,"Giới thiệu chung về ASD và can thiệp sớm, không liên quan.","", "high"),
("3C4DFD62BC",3,"Liệt kê trực tiếp mốc nhận thức trẻ 2 tuổi thường làm được.","Tries to use switches, knobs, or buttons on a toy","high"),
("8503D513D8",0,"Bảng đặc điểm người tham gia nghiên cứu, không liên quan.","", "high"),
("FC06FD2E20",0,"Mô tả công cụ chẩn đoán ADI-R, không liên quan.","", "high"),
("A5734D801D",0,"Mốc xã hội-cảm xúc trẻ 2 tháng, không phải 2 tuổi.","", "high"),
("A244EF0EC1",0,"Mô tả công cụ sàng lọc ASIEP-3, không liên quan.","", "high"),
("3CCB03F1DF",0,"Mô tả công cụ sàng lọc SCQ, không liên quan.","", "high"),
("BF5D0041A6",0,"Mốc vận động trẻ 2 tháng, không phải 2 tuổi.","", "high"),
("305AB67EBF",0,"Bảng thông tin người tham gia nghiên cứu, không liên quan.","", "high"),
("6F8E7F7551",0,"Lời khuyên chăm sóc trẻ 2 tháng, không liên quan trẻ 2 tuổi.","", "high"),
("4E17E759D1",0,"Lời khuyên chăm sóc trẻ 2 tháng, không liên quan trẻ 2 tuổi.","", "high"),
("76AC7CE527",1,"Lời khuyên cho trẻ 15 tháng, có câu gián tiếp nói về trẻ 1-2 tuổi.","Children between 1 and 2 years of age need 11 to 14 hours of sleep a day (including naps).","low"),
("BA095BD284",0,"Mốc nhận thức trẻ 2 tháng, không phải 2 tuổi.","", "high"),
("58DE9273DF",0,"Nói về vitamin D và giấc ngủ ở trẻ tự kỷ, không liên quan.","", "high"),
("01434A3C85",0,"Thảo luận hiệu quả can thiệp phụ huynh theo độ tuổi, không liệt kê khả năng trẻ 2 tuổi.","", "high"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_18/q046.jsonl"
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
