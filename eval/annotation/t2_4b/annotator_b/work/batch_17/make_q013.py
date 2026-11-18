import json

rows = [
("11B55A3163",0,"Về ADHD lo âu, không liên quan khó khăn giao tiếp.","","high"),
("C090074A06",1,"Chỉ nhắc chung khó khăn giao tiếp khi dùng AAC, không chi tiết.","infer information about the well-being, sensations, and feelings of individuals with communication difficulties","medium"),
("408CE3540C",2,"Nêu khó khăn diễn đạt nhu cầu do khác biệt giao tiếp.","Variations in communication can make it less straightforward for autistic individuals to express their needs","medium"),
("0AB46B05AB",3,"Mô tả trực tiếp các khó khăn ngôn ngữ, lời nói, ngữ dụng.","deficits in pragmatic language\u2014the social use of communication\u2014are nearly universal","high"),
("FCC0B4A2AE",1,"Chỉ nhắc ngắn thách thức giao tiếp, chủ yếu về tài trợ nghiên cứu.","communication challenges faced by many with ASD","medium"),
("DB01650EB7",1,"Chỉ định nghĩa chung, không mô tả cụ thể khó khăn giao tiếp.","challenges in social interaction and communication and the presence of restricted interests","medium"),
("7955E1215D",0,"Về bệnh tự miễn, không liên quan giao tiếp.","","high"),
("7531CD7BA5",1,"Chỉ định nghĩa ASD có khiếm khuyết giao tiếp, không chi tiết.","neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors","medium"),
("EDA7B9D33D",0,"Về vấn đề ăn uống/GI, không liên quan giao tiếp.","","high"),
("22B6E6FB6D",2,"Trẻ không lời/ít lời khó diễn đạt đau đớn, khó khăn giao tiếp cụ thể.","may be nonverbal or minimally verbal, making it difficult for them to clearly communicate information about pain","medium"),
("AC4EF8E054",0,"Về khoảng trống nghiên cứu VN, không liên quan giao tiếp.","","high"),
("A59647D7D4",0,"Về công cụ sàng lọc CAST, không mô tả khó khăn giao tiếp.","","high"),
("E06705EAC5",2,"Nêu trẻ ASD có thiếu hụt giao tiếp và tương tác xã hội cao nhất.","people with ASD demonstrated the highest communication and social interaction deficit","medium"),
("A5AC33CA5E",0,"Về triệu chứng tiêu hóa, không liên quan giao tiếp.","","high"),
("6CA3DDDA43",0,"Về ADHD lo âu, không liên quan giao tiếp.","","high"),
("DFD71F86FC",1,"Chỉ nhắc chung khiếm khuyết giao tiếp trong định nghĩa ASD.","impaired social behavior, communication and language","medium"),
("9D512B26B7",3,"Mô tả trực tiếp trẻ tự kỷ ít lời/không lời, khó giao tiếp.","individuals on the autism spectrum remain minimally verbal (MV), meaning they use few or no functional spoken words","high"),
("77A5758B62",3,"Mô tả cụ thể khó khăn trong chú ý chung và giao tiếp của trẻ.","autistic children attending preschool-inclusive contexts initiated few joint attentional states at the age of two","high"),
("FB58361BD1",0,"Về triệu chứng tiêu hóa, không liên quan giao tiếp.","","high"),
("FC5B23DA75",3,"Mô tả cụ thể ngôn ngữ lặp lại, echolalia, khó khăn giao tiếp.","children with ASD who can speak will say things that have no meaning or that do not relate to the conversations","high"),
("48C4239D3C",3,"Tiêu chí DSM-5 mô tả trực tiếp khiếm khuyết giao tiếp xã hội.","Deficits in social-emotional reciprocity, ranging, for example, from abnormal social approach","high"),
("23D91C0D2B",2,"Trích lời phụ huynh về khó khăn giao tiếp cụ thể của trẻ.","Following directions and comprehending what the instructor is telling them to do is hard.","medium"),
("50E23C9390",0,"Về động kinh, không liên quan giao tiếp.","","high"),
("A00E6DC5DF",2,"Nêu giao tiếp là rào cản chính do khó khăn ngôn ngữ.","A major barrier to healthcare access is communication, since difficulties in both receptive and expressive language","medium"),
("04A8C5B4D8",3,"Mô tả trực tiếp khiếm khuyết ngữ dụng trong giao tiếp.","Pragmatic impairments include challenges in conversational reciprocity, topic maintenance","high"),
("B970986691",3,"Liệt kê trực tiếp các khó khăn giao tiếp xã hội của trẻ ASD.","Avoids or does not keep eye contact","high"),
("75EC99C1AC",0,"Về tham gia cộng đồng tự kỷ VN, không liên quan giao tiếp.","","high"),
("ECEBA121A1",0,"Về ADHD lo âu đồng mắc, không liên quan giao tiếp.","","high"),
("6C7C3CC463",0,"Về kỳ thị tự kỷ VN, không liên quan giao tiếp.","","high"),
("C3C2935AC4",2,"Nêu khó khăn xử lý âm thanh ảnh hưởng giao tiếp xã hội.","autistic people can have challenges processing, filtering, and ignoring irrelevant background sounds","medium"),
("58E2F227E6",0,"Về chọn lọc thức ăn, không liên quan giao tiếp.","","high"),
("FD2EA9E3A1",1,"Chỉ nhắc ngắn ảnh hưởng đến giao tiếp lời nói.","impacts expressive or verbal communication with disruptions ranging from moderate to severe","medium"),
("83C8D78F3C",1,"Về công cụ sàng lọc ngôn ngữ, không mô tả khó khăn cụ thể.","ICT is one component of the Communication and Symbolic Behaviour Scale","medium"),
("35ABC854DB",1,"Chỉ nhắc khó khăn giao tiếp trong bàn về hạn chế nghiên cứu.","presence of communication difficulties and atypical symptom presentations complicating the identification","medium"),
("7EFEB2C4B1",0,"Về hành vi lặp lại/thu hẹp, không liên quan giao tiếp.","","high"),
("CBBFE476D9",0,"Về mã chẩn đoán DSM-5, không mô tả khó khăn giao tiếp.","","high"),
("92A6B6C942",2,"Mất thính lực làm chậm phát triển ngôn ngữ và kỹ năng xã hội.","Hearing loss can delay autism diagnosis and also compound language development and social skills","medium"),
("F0F823656F",3,"Mô tả trực tiếp trẻ dùng hành vi để giao tiếp khi khó khăn.","Children may use challenging behaviour to communicate when other ways of communicating are difficult.","high"),
("ECE34FA528",1,"Chỉ nhắc chung thách thức giao tiếp trong định nghĩa ASD.","can cause significant social, communication, and behavioral challenges","medium"),
("876E89DE7A",1,"Chỉ nhắc chung vấn đề giao tiếp xã hội, không chi tiết.","People with ASD often have problems with social communication and interaction","medium"),
("92D416D684",3,"Liệt kê trực tiếp các hành vi giao tiếp xã hội khó khăn.","Making little or inconsistent eye contact","high"),
("3B1FB5A71A",2,"Nêu một số trẻ ASD không phát triển được lời nói/ngôn ngữ.","Some children with ASD may never develop oral speech and language skills.","medium"),
("DEE936A3D6",0,"Về đi lạc ở trẻ khuyết tật phát triển, không liên quan giao tiếp.","","high"),
("9DA33DF9AA",0,"Về ADHD lo âu đồng mắc, không liên quan giao tiếp.","","high"),
("A5519B42BB",0,"Về đồng mắc tâm thần, không liên quan giao tiếp.","","high"),
("4EB03726C5",1,"Chỉ nêu tên chủ đề \"khó khăn giao tiếp\" trong bảng, không chi tiết.","Communication difficulties","medium"),
("220129CCE7",3,"Mô tả trực tiếp khó khăn phát triển ngôn ngữ và hiểu lời nói.","Children with ASD may have difficulty developing language skills and understanding what others say to them.","high"),
]

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_17/q013.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for code, grade, rationale, span, conf in rows:
        obj = {
            "annotation_code": code,
            "grade": grade,
            "rationale": rationale,
            "evidence_span": span,
            "confidence": conf,
            "needs_review": False,
            "review_note": "",
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("wrote", len(rows), "rows")
