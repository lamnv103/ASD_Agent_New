import re, json, os
from collections import Counter
OUT="D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_10"
os.makedirs(OUT, exist_ok=True)
L={}
L['q065']={
'D77C176EC2':(1,"Đoạn chủ yếu nói về BOSA, chỉ nhắc ADOS-2 do bác sĩ lâm sàng được đào tạo thực hiện để so sánh.","the ADOS-2 is administered by trained clinicians who are skilled at eliciting social initiations","medium"),
'3E09C1DE1D':(1,"Bảng nghiên cứu cho thấy ADOS dùng để phân biệt ASD với ADHD, không giải thích ADOS là gì.","Study provides novel evidence for utilization of the ADOS for distinguishing ADHD only youth vs. ASD alone or co-occurring ASD+ADHD","medium"),
'3B3A11E364':(1,"Chỉ có chú giải viết tắt ADOS là lịch quan sát chẩn đoán tự kỷ trong bảng điểm.","ADOS, autism diagnosis observation schedule","medium"),
'9104E64FE1':(2,"Mô tả ADOS-2 là thước đo hành vi ASD, có các module theo ngôn ngữ và điểm tổng/điểm mức độ.","The Autism Diagnostic Observation Schedule, second edition (ADOS-2), was used at the 12-month and 24-month postbaseline assessments to measure ASD behaviors.","high"),
'CB54E2B176':(1,"Chỉ nêu ADOS-2 cùng ADI-R vẫn là chuẩn mực, kèm hạn chế về văn hoá.","ADOS-2) and Autism Diagnostic Interview-Revised (ADI-R) remain standards","medium"),
'508BCCF182':(1,"ADOS được dùng ở đầu nghiên cứu để mô tả triệu chứng tự kỷ, không phải để chẩn đoán.","An ADOS assessment was completed at baseline to characterise the sample according to autism symptoms.","medium"),
'7C76BDF1B2':(2,"Nêu phân loại chẩn đoán, độ tin cậy, độ nhạy và độ đặc hiệu của ADOS-2.","The ADOS-2 has been shown to have good interrater reliability","high"),
'139DF8BC6D':(1,"Nói BOSA được chuyển thể từ ADOS-2, không giải thích ADOS-2.","Adapted from the Brief Observation of Social Communication Change (Grzadzinski et al., 2016) and ADOS-2 (Lord et al., 2012)","medium"),
'BB57B24C19':(3,"Mô tả trực tiếp ADOS là lịch bán cấu trúc, tương tác, do chuyên gia thực hiện để đánh giá giao tiếp xã hội ở người có thể bị ASD.","A semi-structured, interactive schedule conducted by skilled professionals designed to assess social and communicative functioning in individuals who may have ASD","high"),
'F0994B6F0A':(1,"ADOS chỉ được nhắc là công cụ chuẩn hoá dùng khi đánh giá ASD trong nghiên cứu.","the Autism Diagnosis Observation Schedule (ADOS) (29)","medium"),
'A2AAB48F51':(2,"Mô tả ADOS là đánh giá chuyên gia ngắn, quan sát trực tiếp trong phòng khám 1:1, so với ADI-R dựa trên phụ huynh.","the ADOS is a relatively short “snapshot” in real time of a child's observed behaviors in a quiet clinical room 1:1 with a professional","high"),
'1CF3A02234':(1,"Chỉ là bảng chú giải viết tắt, có ADOS = Autism Diagnostic Observation Schedule.","ADOS = Autism Diagnostic Observation Schedule","medium"),
'42FF5F6CB7':(1,"Chú thích bảng giải nghĩa ADOS-2 và thang điểm tổng/điểm mức độ.","ADOS-2, Autism Diagnostic Observation Schedule, second edition","medium"),
'12E40EE1EC':(1,"Chỉ nói ADOS được dùng trong 15 nghiên cứu, thường như công cụ sàng lọc.","The Autism Diagnostic Observation Schedule (ADOS; Lord et al., 2000) was used in 15 studies, most often as a screening tool.","medium"),
'62EF83B3F4':(3,"Định nghĩa ADOS-2 là chuẩn vàng quan sát bán cấu trúc, mô tả phiên bản, 5 module, thời gian và kết quả.","The Autism Diagnostic Observation Schedule (ADOS; Lord et al., 1999, 2012) is considered the “gold-standard” semi-structured, interaction-based, observational evaluation for autism.","high"),
'7890913815':(1,"Nhắc ADOS là phương pháp lâm sàng giúp phân biệt tự kỷ, kèm hạn chế tốn thời gian, cần chuyên gia.","The techniques, like ADI-R and ADOS, have been clinically proven to be effective instruments in differentiating autism from other related developmental disorders","medium"),
}
L['q060']={
'2CC5FFDB94':(2,"Bảng RCT cho thấy chế độ không gluten giảm triệu chứng tiêu hoá và rối loạn hành vi ở trẻ ASD, không nói chữa khỏi.","Gluten-free diet resulted in a significant decrease in behavioral disorders","medium"),
'B1F0E982CD':(2,"Nêu bằng chứng về gluten/celiac còn gây tranh cãi và ít bằng chứng hiệu quả của liệu pháp ăn uống.","some studies have found little evidence of the efficacy of nutritional supplements and dietary therapies","medium"),
'9B665A3CDE':(1,"Chỉ báo 21,2% trẻ ASD theo chế độ ăn hạn chế gluten và sữa, không đánh giá hiệu quả điều trị.","21.2% of subjects followed a diet, mostly based on gluten and milk restriction","medium"),
'B62F84136A':(1,"Chỉ nói trẻ tự kỷ có thể nhạy cảm gluten cao hơn, không bàn về hiệu quả chế độ ăn.","autistic children may be at higher risk for gluten sensitivity","medium"),
'6BF9173564':(2,"Nêu chế độ loại trừ casein/gluten kết hợp prebiotic có tác dụng hiệp đồng lên hành vi (một nghiên cứu).","a synergistic effect on behavior resulted from the combination of prebiotic and casein/gluten-free exclusion diet","medium"),
'48EE3833EC':(1,"Chỉ khuyên gia đình báo cho nhân viên y tế nếu trẻ ăn không gluten/casein, thuộc đánh giá ăn uống.","if the child assumes a gluten/casein-free diet","medium"),
'7D4DA31456':(3,"Tổng quan hệ thống kết luận các nghiên cứu không ủng hộ dùng chế độ GFCF để điều trị ASD, còn có tác hại.","the published studies they identified do not support the use of these diets in the treatment of ASD","high"),
'A074394C4B':(1,"Chỉ nói các khuyến nghị ăn uống phổ biến trong cộng đồng tự kỷ cần nghiên cứu thêm để xác nhận.","further investigation is warranted to better validate their use","low"),
'1B6D023AC0':(2,"RCT nhỏ, không làm mù, cho thấy chế độ không gluten 6 tuần giảm triệu chứng tiêu hoá và rối loạn hành vi.","Ghalichi et al. [32] conducted a small RCT that investigated the effect of a six-week gluten-free diet on GIS and behavioral indices in children with ASD (n = 80).","medium"),
'BA0FB408FB':(3,"Nêu chế độ loại trừ gluten và casein chưa được chứng minh bằng nghiên cứu thực nghiệm khi dùng điều trị tự kỷ.","Dietary interventions like elimination diets (e.g., gluten- and casein-free diets), nutritional supplements, enzymes, and antimicrobial cocktails continue to be explored as autism-focused treatments, though their use has not been substantiated by empirical investigation","high"),
}
L['q038']={
'DCD1263173':(1,"Nói về thuốc kháng histamine cho giấc ngủ ở trẻ ASD, không nên dùng đầu tay; không phải điều trị tự kỷ.","antihistamines should not be used as a first-line approach for the pharmacological treatment of sleep disturbances in children and adolescents with ASD","medium"),
'9079C56B1C':(2,"Thử nghiệm carnosine ở trẻ ASD cải thiện giấc ngủ nhưng không ảnh hưởng mức độ tự kỷ.","the supplementation was found to have no effect on autism severity","medium"),
'2AEF876D9D':(3,"Trả lời trực tiếp: không có thuốc điều trị triệu chứng cốt lõi của ASD, chỉ có thuốc cho triệu chứng đi kèm.","There are no medications that treat the core symptoms of ASD.","high"),
'062639AEA5':(1,"Nói về thuốc ngủ cho trẻ ASD; chưa có thuốc ngủ được FDA phê duyệt, chỉ là thuốc cho một vấn đề đi kèm.","there is no sleep medication approved by the FDA","medium"),
'21F01A0FBF':(1,"Về thuốc kháng histamine cho giấc ngủ ở trẻ em, thiếu RCT, đặc biệt ở ASD.","randomized controlled studies in children are lacking [18], and this is even more true in ASD [19]","low"),
'21B90D2A65':(2,"Thuốc chống động kinh có tác dụng tốt ở trẻ tự kỷ có động kinh, là thuốc cho bệnh đi kèm.","Antiepileptic medication in these children has positive effects, while controlling seizures","medium"),
'0955B6B0F5':(1,"Nêu melatonin và thuốc khác dùng cho rối loạn giấc ngủ ở trẻ tự kỷ, chỉ là bệnh đi kèm.","Melatonin is commonly prescribed to regulate sleep-wake cycles.","medium"),
'05CBC12280':(2,"Thải kim loại (chelation) từng được cho là điều trị tự kỷ nhưng thử nghiệm cho thấy không cải thiện triệu chứng và gây hại.","chelation not only failed to improve symptoms of ASD, but also caused adverse reactions","medium"),
'59600E2E24':(1,"Giới thiệu thuốc không kê đơn như kháng histamine, melatonin cho mất ngủ ở trẻ ASD.","Some non-prescription drugs—such as some antihistamines and melatonin—are among the most used substances for managing insomnia in children","medium"),
'0851CA148A':(1,"Kết luận melatonin hiệu quả cho giấc ngủ ở trẻ ASD, không phải điều trị tự kỷ.","a prolonged-release formulation of melatonin has been approved for use in children with ASD","medium"),
'C5ED4CD0FA':(3,"Nêu bác sĩ có thể kê thuốc cho các triệu chứng cụ thể của ASD như hung hăng, lo âu, tăng động.","A health care provider may prescribe medication to treat specific symptoms","high"),
'F14CAB1DAC':(1,"Tóm tắt các điều trị giấc ngủ gồm melatonin, thuốc không kê đơn ở trẻ ASD.","Treatment options range from lifestyle modifications to pharmacological therapy.","low"),
'E93DCE8BF3':(2,"Nêu các nhóm thuốc dùng cho tic và lo âu đi kèm ở người tự kỷ.","pharmacological approaches recommended are: Dopamine antagonists (aripiprazole or risperidone)","medium"),
'A3A280820E':(2,"Nêu một số thuốc (SSRI, thuốc chống loạn thần không điển hình) có hiệu quả với lo âu, trầm cảm ở người tự kỷ.","Several medications have shown effectiveness in treating anxiety and depressive symptoms such as SSRIs","medium"),
'E415C984EB':(1,"Nói về vitamin, thảo dược cho giấc ngủ ở trẻ ASD, bằng chứng không ủng hộ.","the available evidence does not support this kind of treatment","low"),
'B6340C2B02':(1,"RCT melatonin phóng thích có kiểm soát cải thiện giấc ngủ ở trẻ tự kỷ.","controlled-release melatonin at the dosage of 3 mg/night","medium"),
'E7C717BBBC':(1,"Nói không có thuốc ngủ nào được FDA phê duyệt cho trẻ ASD, chỉ kê ngoài chỉ định.","none of these sleep-promoting drugs is approved by the Food and Drug Administration (FDA) for children and adolescents with ASD","medium"),
'BFF4EC1985':(1,"Chỉ nêu chỉ định điều trị bằng thuốc cho tic nặng, liên quan gián tiếp.","Indications for pharmacological treatment include severe complex tics","low"),
}
bad=0
for q,labs in L.items():
    txt=open(q+'.txt',encoding='utf-8').read()
    parts=re.split(r'^### ',txt,flags=re.M)[1:]
    cands={}
    for p in parts:
        head,_,body=p.partition('\n')
        cands[head.split(' | ')[0].strip()]=body
    exp=int(re.search(r'\((\d+) candidates\)',txt).group(1))
    assert len(cands)==exp,(q,len(cands),exp)
    for c in labs: assert c in cands,(q,c)
    with open(f"{OUT}/{q}.jsonl",'w',encoding='utf-8') as f:
        for c,body in cands.items():
            if c in labs:
                g,r,s,cf=labs[c]
                if s not in body:
                    print("SPAN FAIL",q,c); bad+=1
            else:
                g,r,s,cf=0,"Đoạn không chứa thông tin trả lời câu hỏi này.","","high"
            f.write(json.dumps({"annotation_code":c,"grade":g,"rationale":r,"evidence_span":s,"confidence":cf,"needs_review":False,"review_note":""},ensure_ascii=False)+"\n")
    rows=[json.loads(l) for l in open(f"{OUT}/{q}.jsonl",encoding='utf-8')]
    print(q,len(rows),sorted(Counter(r['grade'] for r in rows).items()),len({r['annotation_code'] for r in rows}))
print("bad",bad)
