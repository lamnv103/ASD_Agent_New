import json, re
W='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/work/batch_16/'
R='D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_16/q013.jsonl'
txt=open(W+'q013.txt',encoding='utf-8').read()
parts=re.split(r'\n### ([0-9A-F]{10}) \|[^\n]*\n', '\n'+txt)
content={parts[i]:parts[i+1] for i in range(1,len(parts),2)}
L=[
("2537953024",1,"Đoạn chủ yếu về lo âu; chỉ nhắc khó khăn chức năng xã hội ở trẻ tự kỷ.","social functioning difficulties (22) that children with an ASD often face","medium"),
("A1A3926369",0,"Về triệu chứng tiêu hoá và vi khuẩn đường ruột, không nói giao tiếp.","","high"),
("C100555CD2",1,"Khó khăn giao tiếp trong bối cảnh y tế, khó diễn đạt nhu cầu.","Variations in communication can make it less straightforward for autistic individuals to express their needs","medium"),
("2A04422911",0,"Ghi chú mã hoá chẩn đoán và tài liệu tham khảo, không mô tả khó khăn giao tiếp.","","medium"),
("10DE26EBE0",1,"Chỉ định nghĩa chung: suy giảm hành vi xã hội, giao tiếp và ngôn ngữ.","impaired social behavior, communication and language","high"),
("D82C7B513D",1,"Nêu trẻ tự kỷ thiếu hụt giao tiếp nặng nhất, nhưng trọng tâm là lo âu.","people with ASD demonstrated the highest communication and social interaction deficit","medium"),
("024651584C",0,"Về động kinh và tự kỷ, không trả lời khó khăn giao tiếp.","","high"),
("B91E86091D",1,"Giới thiệu chung ASD gây thách thức xã hội, giao tiếp; không chi tiết.","can cause significant social, communication, and behavioral challenges","high"),
("0FE9CFA46E",1,"Chỉ định nghĩa ASD có thiếu hụt giao tiếp xã hội; chủ yếu về ADHD.","defined by social- communication deficits and restricted and repetitive behaviors","medium"),
("899EB69164",0,"Tóm tắt nghiên cứu ADHD và lo âu kèm theo, không mô tả khó khăn giao tiếp.","","high"),
("C937BDE854",0,"Về kén ăn và xử lý giác quan.","","high"),
("85E6C837B4",0,"Về bỏ trốn/đi lạc và khuyết tật trí tuệ.","","high"),
("76E3FAF5EA",2,"Nêu 20–30% trẻ ít lời; khó khăn cả giao tiếp phi ngôn ngữ, chú ý chung, cử chỉ.","Their difficulties extend beyond spoken language, affecting nonverbal communication channels such as joint attention, gestures","high"),
("177DC4C8B1",1,"Chủ yếu về tiêu hoá; nhắc trẻ không lời khó diễn đạt đau.","Many autistic children may be nonverbal or minimally verbal, making it difficult for them to clearly communicate","medium"),
("6D1D4048C9",1,"Bảng chủ đề an toàn nước chỉ liệt kê mục khó khăn giao tiếp.","Communication and learning challenges","medium"),
("E14185130B",0,"Về công cụ AAC trong kích thích não, không mô tả khó khăn giao tiếp cụ thể.","","medium"),
("E7E969EBAC",1,"Về nghiên cứu NIH; chỉ nhắc trẻ hạn chế lời nói, ngôn ngữ.","Some of these studies involve children with ASD who have limited speech and language skills","medium"),
("60DFD21FA5",0,"Hạn chế y văn về bệnh đồng mắc.","","high"),
("DE6583DCDE",0,"Về sự tham gia cộng đồng trong nghiên cứu ở Việt Nam.","","high"),
("E27F448E50",1,"Trích dẫn phụ huynh: trẻ khó làm theo và hiểu hướng dẫn.","Following directions and comprehending what the instructor is telling them to do is hard.","medium"),
("1CEED85EB3",2,"Nêu người tự kỷ thường khó khăn ngôn ngữ biểu đạt, tiếp nhận và ngữ dụng.","Autistic individuals frequently face challenges in expressive, receptive, and pragmatic language compared to neurotypical peers","high"),
("13EBC51A6C",1,"Công cụ sàng lọc chậm ngôn ngữ, giao tiếp; gián tiếp liên quan.","recognising language and communication impairment in infants aged from 6 to 24 months","low"),
("3A048AED8D",0,"Về bệnh tâm thần đồng mắc, không nói khó khăn giao tiếp.","","high"),
("F81E8F029A",0,"Về kỳ thị tự kỷ ở Việt Nam.","","high"),
("14BB55992C",3,"Mô tả trực tiếp khó khăn ngôn ngữ, hiểu lời, giao tiếp phi ngôn ngữ của trẻ.","They also often have difficulty communicating nonverbally, such as through hand gestures, eye contact, and facial expressions.","high"),
("08EEC7DFE9",3,"Liệt kê dấu hiệu giao tiếp xã hội: tránh mắt, không đáp tên, ít cử chỉ.","Avoids or does not keep eye contact","high"),
("BEEC71D9ED",0,"Về vấn đề tiêu hoá ở trẻ tự kỷ.","","high"),
("E5506AC6AD",1,"Về điều trị lời nói; nhắc một số trẻ không phát triển lời nói.","Some children with ASD may never develop oral speech and language skills.","medium"),
("7E18551324",0,"Về miễn dịch và bệnh tự miễn.","","high"),
("DD1BCA5B6E",3,"Tiêu chí DSM: thiếu hụt tương tác qua lại, giao tiếp phi ngôn ngữ, quan hệ.","Deficits in nonverbal communicative behaviors used for social interaction","high"),
("4B16826EA8",3,"Nêu chậm nói, ngữ điệu bất thường, nhại lời, thiếu hụt ngữ dụng.","Difficulties include delays in first words, limited phrase speech, and atypical prosody","high"),
("8C0EC0A4BF",0,"Mô tả công cụ sàng lọc CAST, không mô tả khó khăn giao tiếp.","","medium"),
("6EB7D23449",0,"Về vấn đề ăn uống, tiêu hoá.","","high"),
("A3D00723C7",3,"Liệt kê hành vi giao tiếp xã hội: ít giao tiếp mắt, khó hội thoại qua lại.","Having difficulties with the back and forth of conversation","high"),
("606C7FE710",1,"Chủ yếu hành vi lặp lại; có nhắc lặp lại từ ngữ (nhại lời).","Repeats words or phrases over and over (called echolalia)","medium"),
("F9F6CBA4A6",0,"Về lo âu và bệnh đồng mắc, không mô tả khó khăn giao tiếp.","","medium"),
("5D87C67D8A",1,"Hướng dẫn chung cho trẻ chậm phát triển: trẻ dùng hành vi thách thức để giao tiếp.","Children may use challenging behaviour to communicate when other ways of communicating are difficult.","medium"),
("9327692146",1,"Định nghĩa chung: ảnh hưởng giao tiếp biểu đạt hoặc lời nói.","impacts expressive or verbal communication","medium"),
("7A38F5F883",3,"Mô tả mẫu ngôn ngữ: lặp lại, nhại lời, phát triển không đều, kém phi ngôn ngữ.","Children with ASD are often unable to use gestures—such as pointing to an object—to give meaning to their speech.","high"),
("01376CDDCA",3,"Mô tả khiếm khuyết ngữ dụng: hội thoại qua lại, duy trì chủ đề, nghĩa bóng.","Pragmatic impairments include challenges in conversational reciprocity, topic maintenance, and adjusting language to context","high"),
("6171D4056B",1,"Chỉ định nghĩa chung về thách thức tương tác xã hội và giao tiếp.","characterized by challenges in social interaction and communication","medium"),
("D2159A1A54",0,"Mục tiêu và giả thuyết nghiên cứu ADHD, lo âu.","","high"),
("D7B059A85C",2,"Xử lý thính giác gây khó theo dõi hội thoại nơi ồn, ảnh hưởng giao tiếp.","“Cocktail party listening”—the ability to follow a conversation in an acoustically challenging environment","medium"),
("44FA2C5F30",2,"Trẻ mẫu giáo tự kỷ ít khởi xướng chú ý chung, khó giao tiếp khẳng định.","autistic children attending preschool-inclusive contexts initiated few joint attentional states at the age of two","medium"),
("FD00F0AB16",1,"Chủ yếu về tai mũi họng; nhắc mất thính lực làm nặng phát triển ngôn ngữ.","Hearing loss can delay autism diagnosis and also compound language development and social skills","medium"),
("B5A8C5C57D",1,"Nêu chung người tự kỷ có vấn đề giao tiếp xã hội, không chi tiết.","People with ASD often have problems with social communication and interaction","high"),
("9B88033254",0,"Về khoảng trống nghiên cứu tự kỷ ở Việt Nam.","","high"),
]
codes=[x[0] for x in L]
assert len(codes)==len(set(codes))==len(content)==47, (len(codes),len(content))
assert set(codes)==set(content)
with open(R,'w',encoding='utf-8') as f:
    for c,g,r,s,conf in L:
        if g!=0: assert s and s in content[c], c
        else: assert s==''
        f.write(json.dumps({"annotation_code":c,"grade":g,"rationale":r,"evidence_span":s,"confidence":conf,"needs_review":False,"review_note":""},ensure_ascii=False)+'\n')
print('ok')
