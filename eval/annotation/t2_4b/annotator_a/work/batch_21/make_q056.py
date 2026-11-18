import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_21.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_21'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q056.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q056']

annotations = {
    "96CE466129": (0, "Đạo luật Autism CARES Act năm 2014 và chính sách nghiên cứu tại Mỹ, không mô tả các thay đổi tâm lý tuổi teen.", ""),
    "CDE2247933": (1, "Đoạn văn nhận định về sự phát triển não bộ tuổi vị thành niên và khả năng phục hồi của thanh thiếu niên.", "Despite the stresses and challenges that come with adolescence, most teens go on to become healthy adults."),
    "F964E8218E": (2, "Đoạn văn phân tích sự khác biệt về chức năng điều hành (EF) - nền tảng tâm lý quan trọng ảnh hưởng đến khả năng lập kế hoạch và thích ứng khi bước vào tuổi teen.", "Executive function (EF) differences are among the most replicated psychological features of ASD."),
    "4D0A9D08D6": (0, "Đoạn văn định nghĩa tổng quan về tự ký và bệnh đồng mắc ADHD, không tập trung vào tuổi teen.", ""),
    "C5A5190B6F": (3, "Đoạn văn nhấn mạnh tuổi vị thành niên là giai đoạn chuyển đổi tâm sinh lý xã hội trọng yếu, đặc biệt thách thức với cá nhân mắc rối loạn phát triển thần kinh do áp lực hòa nhập xã hội và thay đổi thể chất.", "Adolescence represents a vital period of biopsychosocial transformation, particularly challenging for individuals with neurodevelopmental disorders (N"),
    "D3B6895195": (0, "Mô tả thử nghiệm can thiệp điều hòa cảm giác SenITA ở trẻ em, không bàn về tâm lý tuổi teen.", ""),
    "F30E1D9230": (0, "Đoạn văn nói về triệu chứng tiêu hóa và hệ vi sinh vật đường ruột, không liên quan đến tâm lý tuổi dậy thì.", ""),
    "7BB79290C9": (2, "Đoạn văn giải thích não bộ tuổi teen phản ứng với căng thẳng (stress) khác người lớn, làm tăng nguy cơ mắc các rối loạn liên quan đến stress như trầm cảm và lo âu.", "Because the teen brain is still developing, teens may respond to stress differently than adults. This could increase teens’ chances of developing stre"),
    "68E66B774F": (1, "Đoạn văn nói về các tình trạng đồng mắc ảnh hưởng đến chức năng hàng ngày của người tự kỷ.", "Autistic individuals are frequently reported to experience CCs that affect their daily functioning and well-being. The presence of CCs can also influe"),
    "D697B25BE2": (0, "Tiêu đề về can thiệp sớm cho trẻ sơ sinh, không liên quan đến tuổi dậy thì.", ""),
    "DDA59FEBD5": (1, "Đoạn văn nhắc đến can thiệp hành vi và trị liệu tâm lý cho trẻ em và thiếu niên tự kỷ mắc hội chứng căng trương lực hoặc rối loạn tâm trạng.", "In general, treatment in autistic children and teenagers typically involves behavioral interventions, speech therapy to promote effective communicatio"),
    "56C2D06914": (0, "Đoạn văn thảo luận phương pháp phân tích mạng nơ-ron và hình ảnh học thần kinh, không có nội dung tâm lý tuổi teen.", ""),
    "EADCE09DC0": (0, "Đoạn văn nói về suy giảm chức năng thích ứng và triệu chứng ADHD/lo âu ở trẻ tự kỷ, không nói về tuổi teen.", ""),
    "35BD385746": (2, "Đoạn văn giải thích sự hoàn thiện và tái cấu trúc các khớp thần kinh của não bộ tuổi teen trong việc ra quyết định và kiểm soát xung động.", "Although the brain stops growing in size by early adolescence, the teen years are all about fine-tuning how the brain works."),
    "12FA9B4FD7": (0, "Đoạn văn nghiên cứu về đồng mắc ADHD và lo âu ở trẻ em tự kỷ, không tập trung vào giai đoạn vị thành niên.", ""),
    "20CAFD3231": (2, "Đoạn văn chỉ ra khoảng trống nghiên cứu dịch tễ học về các bệnh tâm thần đồng mắc ở nhóm thanh thiếu niên tự kỷ.", "Our review shows a critical gap in the field for population-based comorbidity studies focusing in particular on adolescents with ASD."),
    "A052FC3816": (1, "Đoạn văn đề cập đến việc nhận biết triệu chứng tự kỷ ở trẻ lớn và thanh thiếu niên tại trường học.", "Caregivers and teachers are often the first to recognize ASD symptoms in older children and adolescents."),
    "85A649C07C": (0, "Đoạn văn thảo luận về các mức độ lo âu và bệnh đồng mắc tâm thần nói chung, không tập trung vào tuổi teen.", ""),
    "F6EF9228A7": (0, "Đoạn văn định nghĩa rối loạn phát triển thần kinh theo DSM-5, không bàn về tuổi dậy thì.", ""),
    "021501E99E": (0, "Đoạn văn tổng quan về sàng lọc và chẩn đoán tự kỷ ở trẻ nhỏ, không liên quan đến tuổi teen.", ""),
    "D1DCADD252": (0, "Đoạn văn nói về sự kỳ thị tự kỷ tại Việt Nam, không liên quan đến tâm lý tuổi dậy thì.", ""),
    "64AE94950A": (2, "Đoạn văn mô tả sự thay đổi của các vùng não chịu trách nhiệm xử lý xã hội ở tuổi teen, khiến trẻ chú trọng nhiều hơn vào mối quan hệ bạn bè và trải nghiệm xã hội.", "Changes to the areas of the brain responsible for social processes can lead teens to focus more on peer relationships and social experiences."),
    "EC658889A4": (1, "Đoạn văn nói về tính mềm dẻo của não bộ tuổi teen thích ứng với trải nghiệm mới.", "The teen brain has an amazing ability to adapt and respond to new experiences and situations."),
    "330A9D857F": (0, "Đoạn văn tổng quan về định nghĩa và chẩn đoán tự kỷ theo DSM-5-TR, không bàn về tuổi teen.", ""),
    "4E125F798E": (0, "Đoạn văn nói về triệu chứng đau bụng và táo bón ở trẻ tự kỷ, không liên quan đến tuổi dậy thì.", ""),
    "CBC19C5351": (1, "Đoạn văn nhấn mạnh tầm quan trọng của việc điều chỉnh can thiệp theo bệnh đồng mắc ở trẻ em và vị thành niên.", "Knowledge gained in population based estimates of comorbidity is therefore not only practically important in tailoring interventions according to the "),
    "4B85F38C6C": (0, "Đoạn văn nói về động kinh và rối loạn giấc ngủ ở trẻ tự kỷ, không liên quan đến tâm lý tuổi teen.", ""),
    "0E6AAE1B10": (2, "Đoạn văn mô tả các rối loạn phát triển thần kinh và sự gia tăng các thách thức xã hội khi bước vào tuổi vị thành niên.", "Neurodevelopmental disorders (NDDs) are childhood-onset conditions characterized by deficits in cognitive, behavioral, and social development, includi"),
    "1C1FECF095": (0, "Đoạn văn bàn về sàng lọc tự kỷ cho trẻ nhỏ và người lớn, không mô tả thay đổi tâm lý tuổi dậy thì.", ""),
    "A9147D7B5C": (2, "Đoạn văn khẳng định sự cần thiết của dịch vụ y tế toàn diện, liên tục để hỗ trợ sức khỏe tâm thần và hòa nhập xã hội cho thanh thiếu niên có rối loạn phát triển.", "Integrated, person-centered, continuous, and collaborative health care is essential to promote the well-being and inclusion of these adolescents."),
    "C1A766D98C": (2, "Đoạn văn phân tích rối loạn trầm cảm chủ yếu (MDD) - tình trạng tâm lý gia tăng đáng kể ở thanh thiếu niên tự kỷ.", "MDD is characterized by persistent sadness or depressed mood, accompanied by somatic or cognitive symptoms affecting their daily functioning[1]."),
    "D9AE942963": (0, "Đoạn văn bàn về đáp ứng miễn dịch T cell trong tự kỷ, không liên quan đến tâm lý tuổi dậy thì.", ""),
    "A5343F6469": (1, "Đoạn văn bàn về tần suất lo âu cao liên quan đến căng thẳng trong tương tác xã hội ở người tự kỷ, đặc biệt gia tăng khi lớn lên.", "In individuals with ASD, a high frequency of anxiety is detected due to the stress and anxiety associated with social interactions [4]. Identifying ea"),
    "AB641842F9": (3, "Đoạn văn nhấn mạnh tuổi vị thành niên là giai đoạn phát triển nhanh chóng, định hình bản sắc cá nhân trong môi trường xã hội, nơi thanh thiếu niên tự kỷ phải đối mặt với nguy cơ cô lập và bắt nạt.", "Adolescence is a period of rapid development during which youth continue to define themselves in relation to their social environment, form their self"),
    "518D2AA7D5": (0, "Đoạn văn tổng quan về triệu chứng tiêu hóa, không liên quan đến tâm lý tuổi teen.", ""),
    "1365883A7C": (3, "Đoạn văn chỉ rõ khi bước vào tuổi vị thành niên, thanh thiếu niên tự kỷ phải đối mặt với các kỳ vọng xã hội phức tạp hơn, nhu cầu tình dục xuất hiện, và nhận thức rõ hơn về sự khác biệt của bản thân, dẫn đến gia tăng lo âu và trầm cảm.", "In childhood, cognitive differences manifest as literal interpretation, preference for routines, and variable imaginative play. Adolescents face heigh"),
    "5D9E46F48D": (1, "Đoạn văn giới thiệu các tiếp cận can thiệp cho người tự kỷ qua các giai đoạn phát triển.", "Intervention approaches for individuals with autism spectrum disorder (ASD) encompass educational practices, developmental perspectives, and behaviora"),
    "E5E84878C4": (0, "Nghiên cứu thử nghiệm Câu chuyện Xã hội (Social Stories) tại trường học, không bàn về thay đổi tâm lý tuổi teen.", ""),
    "AA4D7E23D1": (0, "Đoạn văn nói về tiêu chuẩn chuyển đổi từ DSM-IV sang DSM-5, không có nội dung tuổi teen.", ""),
    "754447D9E2": (3, "Đoạn văn chỉ ra khi lớn lên bước vào tuổi vị thành niên, người tự kỷ thường báo cáo các khó khăn cảm xúc sâu sắc như trầm cảm, lo âu và giận dữ do tăng nhận thức về các trở ngại xã hội.", "As children with autism grow into adolescence and adulthood, they often report emotional difficulties, such as depression, anxiety, and anger, in addi"),
    "BE80E0F300": (3, "Đoạn văn nêu rõ tuổi vị thành niên đem đến sự thay đổi thần kinh nội tiết sâu sắc, lượng hormone sinh dục tăng vọt làm trầm trọng thêm các triệu chứng tự kỷ, gồm rối loạn điều hòa cảm xúc, xung động, nhạy cảm giác và khó khăn thích ứng.", "Adolescence introduces profound neuroendocrine changes. Pubertal surges in sex steroids can exacerbate ASD symptoms, including emotional dysregulation"),
    "5766F5C239": (2, "Đoạn văn nhấn mạnh nhu cầu xây dựng năng lực xã hội và thúc đẩy sự chấp nhận đa dạng thần kinh cho thanh thiếu niên tự kỷ.", "There is a clear need for future research to focus both on building autistic youth’s social competence and promoting the acceptance of neurodiverse in"),
    "D3D467D6F7": (3, "Đoạn văn tổng quan mô tả toàn diện các khía cạnh lâm sàng, cảm xúc, giáo dục và xã hội trong quá trình chuyển tiếp sang tuổi vị thành niên ở trẻ có rối loạn phát triển thần kinh.", "This review article describes the main clinical, emotional, educational, and social aspects involved in the transition to adolescence for individuals "),
    "C3F262F45B": (3, "Đoạn văn chỉ ra triệu chứng lo âu tăng lên rõ rệt ở tuổi vị thành niên do nhận thức xã hội tăng, dẫn đến cảm giác tự ti, cô lập và né tránh tương tác xã hội.", "Existing literature also suggest different presentation based on age and gender. For instance, anxiety symptoms have been reported to increase in adol"),
    "9100F2F965": (1, "Đoạn văn nói về sự thay đổi của melatonin và nhịp sinh học giấc ngủ ở thanh thiếu niên.", "Research shows that the sleep hormone melatonin works differently in teens than in children and adults. In adolescence, melatonin levels stay high lat"),
    "AE8E9EF27F": (0, "Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến tâm lý tuổi teen.", ""),
    "FE111D0929": (0, "Ý kiến người chăm sóc về can thiệp cảm giác tại trường học, không bàn về tâm lý tuổi teen.", ""),
    "593060C3DF": (0, "Khuyến nghị của WHO về sức khỏe tâm thần của người mẹ, không liên quan đến trẻ tự kỷ tuổi teen.", ""),
    "2F1305C4D7": (0, "Nghiên cứu về hành vi đi lạc/bỏ chạy, không mô tả các thay đổi tâm lý vị thành niên.", ""),
    "FDBDFE5FA5": (0, "Tuyển dụng người tham gia khóa huấn luyện kỹ năng xã hội cho thanh thiếu niên, không có nội dung thay đổi tâm lý.", ""),
    "1827C1B4DA": (2, "Đoạn văn chỉ ra sự biến đổi liên tục của não bộ cùng những thay đổi về thể chất, cảm xúc và xã hội khiến thanh thiếu niên dễ tổn thương trước các vấn đề sức khỏe tâm thần.", "Ongoing changes in the brain, along with physical, emotional, and social changes, can make teens more likely to experience mental health problems. The"),
    "94856C8DCA": (3, "Đoạn văn so sánh đặc điểm từ thời thơ ấu đến tuổi teen: trẻ vị thành niên tự kỷ phải đối mặt với các mối quan hệ xã hội phức tạp hơn, áp lực tình bạn, nhận thức về sự khác biệt và nguy cơ gia tăng rối loạn khí sắc.", "In childhood, key features include literal interpretation, circumscribed interests, difficulty with group transitions, and sensory-related distress. E"),
    "6DAC5518FC": (0, "Đoạn văn nói về giả thuyết nghiên cứu triệu chứng lo âu và ADHD ở trẻ tự kỷ, không tập trung vào tuổi teen.", ""),
    "56DDEFF676": (2, "Danh sách các dấu hiệu cảnh báo trầm cảm tuổi teen: cảm thấy buồn bã, lo âu, trống rỗng, mất hứng thú, dễ cáu gắt và thay đổi giấc ngủ.", "- Do you often feel sad, anxious, worthless, or even “empty”? - Have you lost interest in activities you used to enjoy? - Do you get easily frustrated")
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

