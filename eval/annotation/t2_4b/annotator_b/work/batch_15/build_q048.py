import json

rows = [
("CB9D56314A",0,"Nói về hạn chế nghiên cứu, không đưa hành động cụ thể cho cha mẹ.","","medium"),
("EBD7F49F67",1,"Chỉ nêu câu hỏi nghiên cứu về chăm sóc đáp ứng, không hướng dẫn cụ thể.","What is the effectiveness of responsive caregiving interventions in the first 3 years of life on ECD?","medium"),
("A7DE3309D5",3,"Đưa hành động cụ thể cha mẹ có thể làm cho trẻ 3 tuổi để thúc đẩy phát triển.","Encourage your child to solve her own problems with your support.","high"),
("7F35E9370E",1,"Chỉ nói chung các loại can thiệp nuôi dạy có lợi, không nêu hành động cụ thể.","These different types of parenting interventions have consistently shown benefits across a wide age range of children, and especially during early childhood","medium"),
("E9D59AB652",1,"Chỉ dẫn tới nơi có mẹo hoạt động, không nêu nội dung cụ thể.","Find tips and activities you can do for your 3-year-old.","medium"),
("B3B64AC6ED",0,"Về khuyến nghị nghiên cứu tương lai cho can thiệp tự kỷ, không liên quan.","","medium"),
("A5E65EBA69",1,"Khẳng định chung can thiệp nuôi dạy hiệu quả, không nêu hành động cụ thể.","Parenting interventions during the first 3 years of childhood are effective for improving ECD and caregiving.","medium"),
("A532CBF22F",1,"Mô tả loại can thiệp chăm sóc đáp ứng/học sớm được nghiên cứu, bối cảnh gián tiếp.","Caregiving interventions that only implement responsive caregiving","medium"),
("9EAE2E74AA",3,"Đưa hành động cụ thể cha mẹ làm cho trẻ 30 tháng để thúc đẩy phát triển.","Encourage \"free play,\" where your child can follow her interests, try new things, and use things in new ways.","high"),
("A0275A5537",1,"Chỉ một gợi ý nhỏ về chơi theo trình độ trẻ, bối cảnh dành cho trẻ chậm phát triển.","Begin with play routines at the right level for your child.","medium"),
("463B451075",0,"Chỉ là danh sách mốc ngôn ngữ, không phải hành động cha mẹ nên làm.","","medium"),
("F79D0B0C59",1,"Mô tả phương pháp nghiên cứu và kết quả chung, không nêu hành động cụ thể.","We included randomized controlled trials (RCTs) of parenting interventions delivered during the first 3 years of life that evaluated at least 1 ECD outcome.","medium"),
("C71AD92046",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("4F5054C900",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("FB484E16D3",3,"Danh sách chi tiết hành động cha mẹ có thể làm với trẻ 3 tuổi.","Read with your child. Ask questions, such as \"What is happening in the picture?\"","high"),
("5E79FD2FB9",0,"Giới thiệu chương trình CST cho trẻ chậm phát triển, không nêu hành động cụ thể.","","medium"),
("35A6A8C073",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("99D1E6F176",0,"Giới thiệu chung về PMI cho tự kỷ, không liên quan câu hỏi.","","medium"),
("FAC8A33AD1",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("48A6D272AE",1,"Nêu chăm sóc đáp ứng có tác động lớn hơn, nhưng không hướng dẫn cụ thể.","those with responsive caregiving components had significantly greater impacts on child cognitive development, parenting practices, and parent–child interactions","medium"),
("175783F6E0",2,"Liệt kê các nhóm can thiệp cụ thể cha mẹ có thể áp dụng để thúc đẩy phát triển.","interventions that focus on stimulation [6], shared book reading [9], attachment and parental sensitivity [10,11], behavior management [12,13], positive discipline and maltreatment prevention [14,15], and parental mental health [16,17]","high"),
("4EC93974B1",0,"Về huấn luyện cha mẹ cho kén ăn ở tự kỷ, không liên quan.","","medium"),
("D82336862D",0,"Thảo luận hạn chế nghiên cứu về cha và đo lường, không nêu hành động cụ thể.","","medium"),
("37C702EE52",1,"Khẳng định chung can thiệp nuôi dạy cải thiện phát triển, không nêu hành động cụ thể.","We found that parenting interventions improved early child cognitive, language, motor, socioemotional development, and attachment and reduced behavior problems.","medium"),
("A06A7AEFC7",3,"Khuyến nghị chính thức: cha mẹ nên chăm sóc đáp ứng và học sớm cùng trẻ trong 3 năm đầu.","All infants and children should have early learning activities with their parents and other caregivers during the first 3 years of life; parents and other caregivers should be supported to engage in early learning","high"),
("91F3A86956",1,"Khẳng định chung can thiệp nuôi dạy hiệu quả, không nêu hành động cụ thể.","Parenting interventions for children during the first 3 years of life are effective for improving ECD outcomes and enhancing parenting outcomes","medium"),
("482E100CD8",0,"Về liên hệ hệ thống can thiệp sớm khi lo ngại, không phải thúc đẩy phát triển.","","medium"),
("C9C10D5B3F",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("163D4D9D33",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("06097F696B",2,"Hướng dẫn cụ thể cách cho trẻ lựa chọn để khuyến khích tham gia hoạt động.","Start with 2 or 3 motivating choices and follow your child’s choice.","high"),
("8146F6543D",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("97E33AFECF",3,"Đưa hành động cụ thể cha mẹ làm cho trẻ 2 tuổi để thúc đẩy phát triển.","Have your child help you get ready for mealtime, by letting him carry things to the table","high"),
("5B52914E4A",0,"Mô tả thước đo kết quả nghiên cứu, không nêu hành động cụ thể.","","medium"),
("5656568400",1,"Chỉ nêu câu hỏi nghiên cứu về can thiệp nuôi dưỡng, không hướng dẫn cụ thể.","What is the effectiveness of integrated caregiving and nutrition interventions in the first 3 years of life on ECD and child growth outcomes?","medium"),
("725A032B0A",1,"Khẳng định chung can thiệp nuôi dạy cải thiện phát triển, không nêu hành động cụ thể.","We found that parenting interventions delivered during the first 3 years of life improved early child cognitive, language, motor, and socioemotional development","medium"),
("84A2BD4979",0,"Ý nghĩa chính sách chung, không nêu hành động cụ thể cho cha mẹ.","","medium"),
("DC36601955",0,"Chỉ là danh sách mốc vận động, không phải hành động cha mẹ nên làm.","","medium"),
("2F99A77E6C",0,"Về hiệu quả huấn luyện từ xa cho cha mẹ trẻ tự kỷ, không liên quan câu hỏi chung.","","medium"),
("00DDE57DFC",0,"Về xin đánh giá khi có lo ngại, không phải thúc đẩy phát triển.","","medium"),
("4070353EBE",0,"Bảng dữ liệu nghiên cứu, không liên quan trực tiếp.","","medium"),
("2289389D56",3,"Đưa hành động cụ thể cha mẹ làm cho trẻ 1 tuổi để thúc đẩy phát triển.","Talk or sing to your baby about what you're doing.","high"),
("4F792BCDC9",0,"Về nhu cầu học bơi của trẻ tự kỷ, không liên quan.","","medium"),
("16AFFC25D6",3,"Đưa hành động cụ thể cha mẹ làm cho trẻ 4 tháng để thúc đẩy phát triển.","Respond positively to your baby. Act excited, smile, and talk to him when he makes sounds.","high"),
("F6D1AD288D",0,"Về khó tìm thông tin an toàn nước, không liên quan.","","medium"),
("E2B17A15D2",1,"Định nghĩa khái niệm kích thích phát triển, bối cảnh gián tiếp không hướng dẫn cụ thể.","Stimulation Sensory information received from interactions with people and environmental variability that engages a young child’s attention and provides information","medium"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_15/q048.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
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
print("wrote", len(rows), "rows")
