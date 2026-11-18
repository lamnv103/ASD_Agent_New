import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_20'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q036.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q036']

annotations = {
    "31B69079FE": (0, "Đoạn văn bàn về định nghĩa tự kỷ và bệnh đồng mắc ADHD/lo âu, không đề cập đến giấc ngủ.", ""),
    "0A031FE1FD": (0, "Đoạn văn nghiên cứu về nguy cơ đi lạc/bỏ chạy ở trẻ khuyết tật phát triển, không liên quan đến giấc ngủ.", ""),
    "00B20F2174": (2, "Đoạn văn giới thiệu các chiến lược không dùng thuốc (như vệ sinh giấc ngủ và can thiệp hành vi) là bước tiếp cận đầu tiên phổ biến nhất cho rối loạn giấc ngủ ở trẻ tự kỷ.", "Autism Spectrum Disorders (ASD) are lifelong neurodevelopmental conditions characterized by abnormal social interaction, communication, and behavior."),
    "86F68A225C": (0, "Đoạn văn thảo luận về chức năng thích ứng và triệu chứng lo âu ở trẻ tự kỷ, không liên quan đến can thiệp giấc ngủ.", ""),
    "6679E09530": (3, "Đoạn văn trình bày các can thiệp hành vi cụ thể dựa trên nguyên lý học tập nhằm phát triển thói quen ngủ tích cực và loại bỏ các hành vi cản trở giấc ngủ.", "Behavioral interventions include specific strategies, based on principles of learning and behavior with the aim of developing positive sleep-related habits, as well as relaxation a"),
    "492450E61D": (1, "Đoạn văn mô tả tiêu chuẩn lựa chọn đối tượng trong thử nghiệm melatonin phóng thích kéo dài ở trẻ tự kỷ mất ngủ.", "Children (ages 2–17.5 years) with: (1) physician-diagnosed ASD according to ICD-10 or DSM-IV/DSM-5 criteria"),
    "7E3D66D1F8": (2, "Đoạn văn đánh giá bằng chứng về các biện pháp không dùng thuốc khác như nệm âm thanh, xoa bóp massage, liệu pháp hương thơm (aromatherapy) và chế độ ăn đặc biệt.", "However, there is insufficient evidence to draw conclusions on the efficacy of other widespread remedies for sleep problems and it has been reported that only less than 20% of CAM "),
    "64FA1CEF01": (1, "Đoạn văn bàn về tỷ lệ đồng mắc ADHD và các rối loạn giấc ngủ ở trẻ tự kỷ.", "Attention-deficit/hyperactivity disorder (ADHD) is one of the most common co-o"),
    "0A82511BFA": (2, "Đoạn văn phân tích cơ sở lý thuyết và ứng dụng của liệu pháp xoa bóp (massage) đối với trẻ tự kỷ có vấn đề giấc ngủ nhằm điều hòa rối loạn xử lý cảm giác.", "The use of massage in autistic children with sleep problems is based on theoretical grounds similar to those supporting the use of weighted blankets and the above-mentioned mattres"),
    "8C1CC70B41": (2, "Đoạn văn trình bày nghiên cứu thử nghiệm công nghệ nệm tích hợp âm thanh và rung nhẹ (hệ thống STS) để cải thiện giấc ngủ ở trẻ tự kỷ quá nhạy cảm giác.", "In 2017, a preliminary randomized crossover study [56] examined efficacy and tolerability of a mattress-based technology—the STS system—in the treatment of sleep problems in 45 aut"),
    "1A9DF9EB5C": (2, "Đoạn văn phân tích tác động tích cực của hoạt động thể chất và tập thể dục đối với việc cải thiện giấc ngủ ở trẻ tự kỷ.", "Several studies examined physical activity as a variable that might influence sleep in autistic children."),
    "7B99D2262B": (1, "Đoạn văn đề cập đến chất bổ sung 5-HTP và các chất bổ sung không kê đơn cho giấc ngủ.", "Extensive analyses of several sources of 5-HTP did not find toxic contaminants or any other significant impurity"),
    "D682B9BD4C": (0, "Đoạn văn bàn về đáp ứng miễn dịch và bệnh tự miễn ở người tự kỷ, không liên quan đến giấc ngủ.", ""),
    "67A84DCEA7": (3, "Đoạn văn mô tả chi tiết các kỹ thuật can thiệp hành vi: làm mờ giờ đi ngủ (bedtime fading) và dập tắt tiêu chuẩn (standard extinction) để tăng tổng thời gian ngủ.", "This behavioral intervention has also been proven to be effective in increasing TST [42]."),
    "6EA4ED0433": (3, "Đoạn văn khẳng định nguyên tắc can thiệp không dùng thuốc là lựa chọn ưu tiên hàng đầu cho mất ngủ ở trẻ em, bắt đầu bằng giáo dục vệ sinh giấc ngủ cho cha mẹ.", "As a general tenet of pediatric practice, non-pharmacological intervention is the preferred first treatment option before initiation of pharmacologic therapies [17]. Even if sleep "),
    "B8C96D6A8C": (2, "Đoạn văn khẳng định vệ sinh giấc ngủ kết hợp can thiệp hành vi là khuyến nghị ban đầu cần cung cấp cho phụ huynh có con tự kỷ bị rối loạn giấc ngủ.", "Impact on the child: Sleep disturbances are associated with increased behavioral challenges including aggression, self-injury, anxiety, hyperactivity, irritability, inattention, in"),
    "DFF27FBC74": (2, "Đoạn văn nhấn mạnh thuốc ngủ chỉ nên xem là lựa chọn bổ sung khi các can thiệp không dùng thuốc không thành công hoặc chỉ thành công một phần.", "Sleep pills should be considered to be an additional treatment option to improve sleep in children when non-pharmacological interventions are unsuccessful [17]. However, in childre"),
    "2EEA6B31C9": (1, "Đoạn văn bàn về nồng độ ferritin và việc bổ sung sắt cho các thông số giấc ngủ ở trẻ tự kỷ.", "However, it should be noted that data correlating ferritin concentration with sleep parameters in autistic children are unclear and further research is needed. Some authors [170] d"),
    "F40F6C1F1F": (2, "Đoạn văn khẳng định can thiệp hành vi và giáo dục giấc ngủ cho cha mẹ là nền tảng điều trị đầu tay trong quản lý rối loạn giấc ngủ ở trẻ tự kỷ.", "Autism Spectrum Disorders (ASD) are a group of lifelong, heterogeneous neurodevelopmental conditions, characterized by early-onset deficits in social interaction and communication,"),
    "68A0608375": (3, "Đoạn văn hướng dẫn kết hợp giáo dục vệ sinh giấc ngủ với can thiệp hành vi tăng dần, như thiết lập quy trình đi ngủ tích cực (positive bedtime routines).", "Therefore, it is often easier and more acceptable for parents to associate sleep education with behavioral gradual interventions"),
    "B676A47D34": (1, "Bảng tổng hợp nghiên cứu khám phá mối quan hệ giữa giấc ngủ và hành vi thách thức ở trẻ tự kỷ.", "Table 2\nStudies exploring the relationship between sleep and challenging behaviors in ASD"),
    "C68E48E7AC": (1, "Bảng tổng hợp các nghiên cứu về giấc ngủ và hành vi ở trẻ tự kỷ.", "Table 2\nStudies exploring the relationship between sleep and challenging behaviors in ASD"),
    "62A647E795": (2, "Đoạn văn báo cáo thử nghiệm lâm sàng ngẫu nhiên về can thiệp yoga có cấu trúc giúp cải thiện giấc ngủ và hành vi ở trẻ tự kỷ.", "A recent RCT assessed the efficacy of a structured yoga intervention for sleep, gastrointestinal and behavioral problems in a cohort of 64 ASD children aged 5 to 16 years [62]. The"),
    "5E7BCC96AD": (1, "Đoạn văn phân tích bất thường gen trong con đường chuyển hóa melatonin ở trẻ tự kỷ chậm khởi phát giấc ngủ.", "children with ASD and comorbid sleep-onset delay showed genetic abnormalities in the metabolic pathway of melatonin"),
    "BCAB4AFE64": (1, "Đoạn văn bàn về bổ sung vitamin và khoáng chất đối với các vấn đề giấc ngủ ở trẻ tự kỷ.", "Tentative treatments with multivitamin and mineral supplements for sleep problems have also been carried out"),
    "C94A63E52A": (1, "Đoạn văn phân tích hiệu quả của công thức melatonin phóng thích kéo dài trong việc duy trì giấc ngủ.", "This is of note because the prolonged release formulation which releases melatonin throughout the night appears to be effective in improving both sleep onset and sleep maintenance "),
    "1C8E1CB258": (1, "Đoạn văn thảo luận về hiệu quả giấc ngủ (SE) trong các nghiên cứu điều trị giấc ngủ.", "Only a weak effect was found for SE, as several the studies yield negative results for this parameter"),
    "B8997A47A1": (3, "Bảng 2 trình bày các khuyến nghị thực hành giấc ngủ dựa trên bằng chứng theo ghi nhớ 'ABCs of SLEEPING' của Viện Hàn lâm Thần kinh học Hoa Kỳ (AAN).", "brainsci-10-00441-t002_Table 2Table 2\nEvidence-based pediatric sleep practice recommendations of the ‘ABCs of SLEEPING’ mnemonic."),
    "8879804D59": (2, "Đoạn văn xem xét thử nghiệm lâm sàng đánh giá tác dụng của liệu pháp hương thơm (aromatherapy) đối với giấc ngủ ở trẻ tự kỷ.", "Only one clinical trial was carried out to evaluate the effects of aromatherapy on sleep in children with ASD"),
    "11E26A2609": (2, "Đoạn văn nêu rõ các phương pháp không dùng thuốc và thảo dược/chất bổ sung không kê đơn được ưu tiên do lo ngại về độ an toàn lâu dài của thuốc kê đơn.", "Sleep disturbances in children with ASD are a challenging issue for patients, families, and clinicians. Non-pharmacological and oral non-prescription treatments are widely used to "),
    "91A5CA132B": (3, "Đoạn văn khẳng định giáo dục giấc ngủ cho phụ huynh là phương pháp tiết kiệm chi phí, dễ thực hiện và hiệu quả để cải thiện giấc ngủ cho trẻ tự kỷ.", "Parent sleep education has been found to be effective in the general pediatric population [17], and in small samples of children with ASD [26,27,28,29]. A 2017 meta-synthesis of pr"),
    "C96E18A772": (1, "Bảng tổng hợp nghiên cứu về giấc ngủ và hành vi thách thức ở trẻ tự kỷ.", "Table 2\nStudies exploring the relationship between sleep and challenging behaviors in ASD"),
    "0C373025FF": (1, "Đoạn văn chỉ ra mối liên quan giữa rối loạn giấc ngủ với kỹ năng sống và triệu chứng tiêu hóa ở trẻ tự kỷ.", "The presence of sleep problems is associated with lower levels of social cognition, daily living skills, and GIS"),
    "C803B91A60": (1, "Bảng phân loại các rối loạn giấc ngủ theo ICSD-3 ở trẻ tự kỷ.", "Table 1"),
    "8AF89C3E0B": (3, "Bảng 1 trình bày quy trình tiếp cận từng bước đối với rối loạn giấc ngủ ở trẻ em: bắt đầu từ đánh giá lâm sàng, vệ sinh giấc ngủ, can thiệp hành vi trước khi dùng melatonin.", "brainsci-10-00441-t001_Table 1Table 1\nStepwise approach to sleep disturbances in children. Adapted from Howlett et al. (2020) [10]"),
    "148569B94B": (1, "Đoạn văn thảo luận về tính an toàn dài hạn của melatonin trong điều trị giấc ngủ.", "In long-term studies (up to 104 weeks) no significant adverse event has been reported, excluding also relevant consequences on pubertal growth."),
    "8A2D29A0ED": (2, "Đoạn văn phân tích việc sử dụng chăn trọng lực (weighted blankets) như một biện pháp phi truyền thống không dùng thuốc phổ biến cho trẻ tự kỷ.", "Weighted blankets and vests are a widespread non-traditional treatment for sleep disturbances in children with ASD."),
    "7AA7AA814E": (0, "Đoạn văn nói về sự kỳ thị và bối cảnh chẩn đoán tự kỷ tại Việt Nam, không liên quan đến giấc ngủ.", ""),
    "BF0501A78B": (1, "Đoạn văn đánh giá hiệu quả dung dịch kết hợp melatonin, Trp và vitamin B6 trong việc rút ngắn thời gian khởi phát giấc ngủ.", "A solution containing melatonin, Trp and vitamin B6 proved to be significantly more effective than melatonin alone in reducing the number of tests that had to be repeated due to aw"),
    "3920769BA3": (1, "Đoạn văn mô tả phương pháp tìm kiếm tài liệu của bài tổng quan về can thiệp không dùng thuốc cho giấc ngủ.", "This study consists of a narrative review of the literature. Extensive literature searches were conducted"),
    "A5A8352F43": (3, "Đoạn văn khẳng định vai trò của giấc ngủ và hiệu quả của các can thiệp hành vi, giáo dục vệ sinh giấc ngủ và liệu pháp nhận thức hành vi mất ngủ (CBT-I) cho trẻ tự kỷ.", "Sleep is fundamental in typical development and plays a vital role in the physical and cognitive maturation of children.")
}

item_map = {it['annotation_code']: it['content'] for it in items}
results = []

for it in items:
    code = it['annotation_code']
    if code not in annotations:
        raise ValueError(f"Missing annotation for {code}")
    grade, rationale, span = annotations[code]
    content = it['content']
    if grade != 0:
        if not span:
            raise ValueError(f"Span empty for non-zero grade in {code}")
        if span not in content:
            raise ValueError(f"Span not found in content for {code}: {span}")
        if len(span) > 250:
            span_sub = span[:245]
            if span_sub not in content:
                raise ValueError(f"Truncated span not found: {span_sub}")
            span = span_sub
    else:
        span = ""
    
    obj = {
        "annotation_code": code,
        "grade": grade,
        "rationale": rationale,
        "evidence_span": span,
        "confidence": "high",
        "needs_review": False,
        "review_note": "",
        "annotation_type": "ai_generated",
        "model": "claude-sonnet-4-6",
        "prompt_version": "t2_4b_ai_v1"
    }
    results.append(obj)

with open(out_file, 'w', encoding='utf-8') as f:
    for obj in results:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')

print(f"Total entries: {len(results)}")
print(f"Successfully generated and verified {out_file} with {len(results)} annotations.")
