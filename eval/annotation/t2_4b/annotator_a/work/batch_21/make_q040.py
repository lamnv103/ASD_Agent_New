import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_21.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_21'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q040.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q040']

annotations = {
    "155DCE5B64": (0, "Đoạn văn thảo luận về lo âu và thiếu hụt tương tác xã hội ở trẻ tự kỷ, không liên quan đến học bơi hay an toàn dưới nước.", ""),
    "466A1FAC8B": (3, "Đoạn văn nhấn mạnh các bài học bơi cần điều chỉnh thích ứng với các thách thức giao tiếp và học tập của trẻ tự kỷ, như chia nhỏ hướng dẫn và hỗ trợ ngôn ngữ.", "Parents reported that swimming lessons need to adapt to communication and learning challenges. A parent noted of her son: “He doesn’t have any ability"),
    "36563FCCF9": (0, "Bảng nhân khẩu học của giáo viên dạy bơi tham gia nghiên cứu, không chứa thông tin lợi ích hay an toàn.", ""),
    "6D60615045": (1, "Đoạn văn bàn về hành vi bỏ chạy/đi lạc (elopement) ở trẻ khuyết tật phát triển - yếu tố nguy cơ hàng đầu dẫn đến đuối nước.", "Elopement places children with developmental disabilities at risk of serious injury or even death. Despite its clear relevance to the safety and well-"),
    "0B20FCAEA8": (1, "Bảng câu hỏi phỏng vấn phụ huynh về an toàn dưới nước và việc tiếp cận các lớp học bơi cho trẻ tự kỷ.", "Table 1"),
    "CCC0EB63A8": (0, "Mô tả tuyển dụng người tham gia nghiên cứu về an toàn dưới nước, không có nội dung can thiệp.", ""),
    "C69939EE88": (2, "Đoạn văn nhấn mạnh nhu cầu đào tạo cho các trường dạy bơi và giáo viên để nâng cao nhận thức về an toàn và kỹ năng dạy bơi cho trẻ tự kỷ.", "However, there is a lot more progress needed to make swim schools aware of such programs and to coordinate and fund training."),
    "E34C1A70B6": (0, "Đoạn văn tổng quan về lo âu và các bệnh đồng mắc tâm thần, không đề cập đến bơi lội.", ""),
    "998ED85F8E": (0, "Đoạn văn bàn về chức năng thích ứng và triệu chứng ADHD/lo âu ở trẻ tự kỷ, không liên quan đến bơi lội.", ""),
    "C3DF1B279E": (0, "Đoạn văn nói về đáp ứng miễn dịch bất thường trong tự kỷ, không liên quan đến bơi lội.", ""),
    "A4CD820F07": (3, "Đoạn văn khẳng định bơi lội là hoạt động có ý nghĩa trị liệu, mang lại niềm vui, cải thiện kỹ năng vận động và sự tự tin cho trẻ tự kỷ và gia đình.", "Swimming proved a meaningful occupation for children with autism and their families. Parent’s experiences, similar to teachers, were dynamic, especial"),
    "4D292E998C": (0, "Đoạn văn nói về tỷ lệ đồng mắc ADHD và lo âu trong tự kỷ, không liên quan đến bơi lội.", ""),
    "D1EF10353D": (2, "Bảng trích dẫn các chia sẻ của phụ huynh về các rào cản an toàn nước, nguy cơ đuối nước và tầm quan trọng của việc học bơi thích ứng.", "Table 3: Quotes from caregivers of autistic children on themes and subthemes related to water safety"),
    "4F70D8D700": (2, "Đoạn văn phân tích kinh nghiệm của giáo viên dạy bơi và sự cần thiết phải có hiểu biết chuyên sâu về tự kỷ để đảm bảo an toàn và hiệu quả dạy bơi.", "Swimming teachers’ experiences in teaching children with autism have not been well explored in existing research (Murphy & Hennebach, 2020). Due to th"),
    "A59373B924": (3, "Đoạn văn nêu rõ lợi ích trị liệu của môi trường nước: áp lực nước giúp làm dịu cảm giác, điều hòa giác quan và tạo không gian vận động tích cực cho trẻ tự kỷ.", "Many parents (and some teachers) noted that the aquatic environment is inherently therapeutic. It was noted that the sensory qualities of the water he"),
    "162880B42C": (0, "Bảng nhân khẩu học của phụ huynh và trẻ tham gia nghiên cứu, không có nội dung học bơi.", ""),
    "576D0054B0": (1, "Bảng kết quả phân tích chủ đề về trải nghiệm học bơi của trẻ tự kỷ và giáo viên dạy bơi.", "Table 3."),
    "91CC2CB89C": (2, "Đoạn văn phân tích trải nghiệm của cha mẹ khi cho con học bơi, từ lo âu ban đầu đến sự tiến bộ vượt bậc về kỹ năng dưới nước và sự an tâm về an toàn.", "Gold"),
    "BEC6A9FCCA": (2, "Bảng tổng hợp các chủ đề về an toàn nước: nguy cơ đuối nước do đi lạc, rào cản tiếp cận lớp học bơi và các chiến lược bảo vệ an toàn.", "Table 2"),
    "C56A95F906": (3, "Đoạn văn tổng kết trải nghiệm an toàn nước của phụ huynh, nhấn mạnh nhu cầu giám sát liên tục, rào chắn an toàn và học bơi để phòng tránh đuối nước.", "This qualitative assessment of water safety experiences revealed that parents’ experience of having a child with autism and navigating water safety ca"),
    "8C92995478": (0, "Danh sách dữ liệu nhân khẩu học cần thu thập trong nghiên cứu, không chứa nội dung khoa học.", ""),
    "2E2D3FBF12": (3, "Đoạn văn chỉ ra lợi ích điều hòa cảm giác của môi trường nước, giúp trẻ bình tĩnh, điều hòa giác quan và tìm thấy niềm vui thích khi vận động dưới nước.", "This sensory input can have a regulating effect on their child. As another parent pointed out, water is his son’s “happy place, and it’s a good ground"),
    "3A2896DFE1": (0, "Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến bơi lội.", ""),
    "156C3A8D13": (3, "Đoạn văn nêu rõ đuối nước là nguyên nhân gây tử vong hàng đầu ở trẻ tự kỷ dưới 14 tuổi do xu hướng đi lạc, bị nước thu hút và giảm nhận thức nguy hiểm.", "Among children with autism, drowning is the leading cause of death through 14 years old. Attributes such as wandering, sensory issues, impulsivity, an"),
    "DA5A4BACAA": (0, "Đoạn văn tổng quan về chẩn đoán và đánh giá tự kỷ theo DSM-5-TR, không đề cập đến bơi lội.", ""),
    "CD696440C9": (2, "Đoạn văn mô tả cách các giáo viên dạy bơi tiếp cận, xây dựng lòng tin và thiết lập quy trình dạy bơi an toàn từng bước cho trẻ tự kỷ.", "to the Starting Blocks"),
    "3E4936A518": (2, "Đoạn văn thảo luận các thách thức an toàn nước mà cha mẹ phải đối mặt và các chiến lược thích ứng nhằm bảo vệ trẻ khỏi tai nạn đuối nước.", "This study contributes to the small existing body of literature on water safety and autism by elucidating challenges that parents face keeping their a"),
    "0340F2E564": (2, "Bảng trích dẫn chia sẻ của phụ huynh về việc trẻ tự kỷ bị cuốn hút bởi nước nhưng không nhận thức được nguy hiểm, đòi hỏi sự an toàn và giám sát cao độ.", "Table 3: Quotes from caregivers of autistic children on themes and subthemes related to water safety"),
    "05DDD28B33": (3, "Đoạn văn chỉ ra các thách thức an toàn khi trẻ học bơi (khó tập trung, bốc đồng, giảm nhận thức nguy hiểm) và sự cần thiết của giáo viên được đào tạo chuyên biệt.", "When parents overcome barriers and successfully access swimming lessons, they report that challenges may still arise due to common characteristics of "),
    "6CCB566BDF": (0, "Đoạn văn bàn về sự kỳ thị tự kỷ tại Việt Nam, không liên quan đến an toàn dưới nước.", ""),
    "EC15B84E9C": (3, "Đoạn văn nêu bật lợi ích của bơi lội như một hoạt động thể chất và giải trí quan trọng giúp cải thiện thể lực, kỹ năng vận động và sự hòa nhập cho trẻ tự kỷ.", "Children with autism are reported to participate in fewer leisure activities than typically developing children (Askari et al., 2015), leading them to"),
    "CF0185F99C": (3, "Đoạn văn nhấn mạnh trẻ tự kỷ có nguy cơ đuối nước cao hơn trẻ bình thường do hành vi đi lạc, giảm nhận thức nguy cơ và sự hấp dẫn của nước, đòi hỏi phải dạy kỹ năng sinh tồn.", "Autistic children are thought to be at a higher risk of drowning than typically developing children due to wandering behavior, decreased risk awarenes"),
    "3C593DBB35": (0, "Đoạn văn định nghĩa tự kỷ và bệnh đồng mắc ADHD, không liên quan đến bơi lội.", ""),
    "C827026D97": (3, "Đoạn văn nêu rõ dù có nguy cơ đuối nước cao, học bơi mang lại lợi ích to lớn về sức khỏe, sự tự tin và là biện pháp thiết yếu để ngăn ngừa tai nạn dưới nước.", "Despite the increased risk of drowning among autistic children and water safety risks impacting activity and travel planning, parents generally report")
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

