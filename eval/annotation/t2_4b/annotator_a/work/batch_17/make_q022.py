import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_17'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q022.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q022':
            content_map[obj['annotation_code']] = obj['content']

def get_span(code, anchor, max_len=200):
    if not anchor:
        return ""
    c = content_map[code]
    idx = c.find(anchor)
    if idx == -1:
        raise ValueError(f"Anchor '{anchor}' not found in {code}")
    sub = c[idx:idx+max_len]
    if '\n' in sub:
        sub = sub.split('\n')[0].strip()
    return sub

raw = [
    {
        'code': '44C4F5517D',
        'grade': 0,
        'rationale': 'Bài tập tình huống về dạy trẻ hành vi thay thế khi tức giận, không đề cập đến phòng tránh đi lạc, bỏ chạy.',
        'anchor': '',
    },
    {
        'code': '9CCBE5326A',
        'grade': 0,
        'rationale': 'Bảng thống kê tỷ lệ phần trăm mẫu khảo sát Pathways, không chứa biện pháp phòng tránh đi lạc.',
        'anchor': '',
    },
    {
        'code': '07157B38C7',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các vấn đề giấc ngủ và động kinh ở trẻ tự kỷ, không liên quan đến hành vi đi lạc.',
        'anchor': '',
    },
    {
        'code': '593CBA446E',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về hệ vi sinh đường ruột và triệu chứng tiêu hóa ở trẻ tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '5915D62558',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu các công cụ theo dõi mốc phát triển của CDC, không đề cập đến phòng ngừa đi lạc.',
        'anchor': '',
    },
    {
        'code': '053CEB1147',
        'grade': 0,
        'rationale': 'Tổng quan về chẩn đoán và sàng lọc tự kỷ theo DSM-5-TR, không chứa thông tin về đi lạc, bỏ chạy.',
        'anchor': '',
    },
    {
        'code': 'B3B9F56FCA',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh mức độ lo âu và kỹ năng vận động ở trẻ tự kỷ và ADHD, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '43432257D1',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu các viện nghiên cứu thuộc NIH tài trợ cho nghiên cứu giao tiếp ở tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '4DF0144243',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các triệu chứng ADHD và lo âu đồng mắc ở trẻ tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '9D57762846',
        'grade': 2,
        'rationale': 'Bảng phân tích góc nhìn của phụ huynh về các nguy cơ an toàn nước và đi lạc/bỏ chạy ở trẻ tự kỷ, nhấn mạnh sự cần thiết của các biện pháp bảo vệ.',
        'anchor': 'Wandering and elopement',
    },
    {
        'code': '0B97103D58',
        'grade': 0,
        'rationale': 'Bảng thống kê tỷ lệ đi lang thang theo đặc điểm nhân khẩu, không có biện pháp phòng ngừa.',
        'anchor': '',
    },
    {
        'code': 'D15943B598',
        'grade': 0,
        'rationale': 'Tài liệu tập huấn người chăm sóc về xác định mục tiêu phản ứng với hành vi thách thức, không đề cập đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '21DBAE7790',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích các rối loạn vận động và hội chứng Tourette ở người tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': 'E3390DA872',
        'grade': 0,
        'rationale': 'Lời khuyên cho phụ huynh về cách giúp đỡ trẻ mắc ADHD (tạo thói quen, khen ngợi), không chứa biện pháp phòng tránh đi lạc.',
        'anchor': '',
    },
    {
        'code': 'B0AE87836A',
        'grade': 1,
        'rationale': 'Mô tả phương pháp tính toán tỷ lệ đi lang thang trong 12 tháng trước đó ở trẻ khuyết tật phát triển tại Mỹ.',
        'anchor': 'The prevalence of elopement within the previous 12 months was calculated separately',
    },
    {
        'code': 'C0E5940A78',
        'grade': 0,
        'rationale': 'Bảng tỷ lệ đi lang thang theo phân nhóm chẩn đoán, không chứa biện pháp phòng tránh.',
        'anchor': '',
    },
    {
        'code': '4B1C6180FA',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả đặc điểm nhân khẩu học và tôn giáo tại Việt Nam, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': 'F4C836E374',
        'grade': 2,
        'rationale': 'Tóm tắt nghiên cứu chỉ ra các đặc điểm như đi lang thang, xung động và giảm nhận thức nguy hiểm ở trẻ tự kỷ, đặt ra nhu cầu can thiệp an toàn nước.',
        'anchor': 'Attributes such as wandering, sensory issues, impulsivity, and a limited sense of danger',
    },
    {
        'code': '3C61FA80DB',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến hành vi đi lạc.',
        'anchor': '',
    },
    {
        'code': 'BA80E65C45',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ trẻ tự kỷ có nguy cơ đuối nước cao do hành vi đi lang thang và thích nước, từ đó việc học bơi được xem như biện pháp an toàn sống còn.',
        'anchor': 'typically developing children due to wandering behavior, decreased risk awareness, and attraction to water',
    },
    {
        'code': '3B1679C218',
        'grade': 2,
        'rationale': 'Đoạn thảo luận nhấn mạnh hành vi đi lang thang khiến trẻ gặp nguy cơ chấn thương nghiêm trọng hoặc tử vong, và là nghiên cứu đại diện quốc gia đầu tiên về vấn đề này.',
        'anchor': 'Elopement places children with developmental disabilities at risk of serious injury or even death',
    },
    {
        'code': '9235465B32',
        'grade': 0,
        'rationale': 'Lời khuyên nuôi dạy con chung cho trẻ 6 tháng tuổi của CDC, không liên quan đến tự kỷ hay đi lạc.',
        'anchor': '',
    },
    {
        'code': '68866CC763',
        'grade': 0,
        'rationale': 'Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '0330D7EFDF',
        'grade': 2,
        'rationale': 'Tóm tắt bài báo nghiên cứu chỉ ra sự thiếu hụt nghiên cứu về hành vi bỏ chạy/đi lạc và báo cáo tỷ lệ hiện mắc cũng như các yếu tố liên quan ở trẻ em.',
        'anchor': 'This is the first study to examine and report the prevalence and correlates of elopement',
    },
    {
        'code': '1EB18D123C',
        'grade': 3,
        'rationale': 'Đoạn văn chỉ rõ việc hiểu rõ nguyên nhân đi lạc giúp phát triển các chiến lược phòng ngừa (biến đổi môi trường, can thiệp hành vi và kế hoạch an toàn) để giảm thiểu rủi ro.',
        'anchor': 'understanding of the causes of elopement in this population may aid in the development of strategies',
    },
    {
        'code': 'D95E2C828B',
        'grade': 3,
        'rationale': 'Đoạn văn giới thiệu các chương trình cụ thể như "Water and Wandering Program" của Autism on the Spectrum giúp tăng cường sự an toàn và phòng ngừa trẻ tự kỷ đi lạc xuống nước.',
        'anchor': 'Water and Wandering Program are two examples of programming that can increase the',
    },
    {
        'code': '5113127097',
        'grade': 2,
        'rationale': 'Đoạn thảo luận khẳng định hành vi bỏ chạy/đi lạc là vấn đề phổ biến và cần sự quan tâm đặc biệt của gia đình và nhà trường.',
        'anchor': 'these findings suggest that elopement is a common problem among U.S. children with developmental',
    },
    {
        'code': '2F35A3A846',
        'grade': 2,
        'rationale': 'Bảng trích dẫn ý kiến phụ huynh về thách thức giữ trẻ tự kỷ ở lại với nhóm để ngăn ngừa việc trẻ bỏ chạy hoặc đi lang thang.',
        'anchor': 'Wandering and elopement',
    },
    {
        'code': '9928627B36',
        'grade': 0,
        'rationale': 'Đoạn tóm tắt nghiên cứu về triệu chứng ADHD và lo âu ở người tự kỷ, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': 'ADD1E448CB',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': 'C8838F8909',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu về các công cụ sàng lọc và chẩn đoán tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '492551FF3B',
        'grade': 2,
        'rationale': 'Phần mở đầu nêu rõ sự chú ý ngày càng tăng của cộng đồng đối với hành vi đi lang thang hoặc bỏ chạy như một nguyên nhân tiềm ẩn gây thương tích ở trẻ em khuyết tật phát triển.',
        'anchor': 'drawn attention to wandering, or elopement, as a potential cause of injury in children with development',
    },
    {
        'code': '99562B5604',
        'grade': 0,
        'rationale': 'Lời khuyên nuôi dạy con cho trẻ 30 tháng tuổi của CDC, không chứa thông tin chuyên biệt về phòng chống tự kỷ bỏ chạy.',
        'anchor': '',
    },
    {
        'code': '8703D82AE7',
        'grade': 0,
        'rationale': 'Tài liệu hướng dẫn kỹ năng người chăm sóc về các bước ứng phó hành vi thách thức, không trực tiếp thảo luận đi lạc.',
        'anchor': '',
    },
    {
        'code': '5123CE8AC1',
        'grade': 0,
        'rationale': 'Đoạn thảo luận về phân loại khuyết tật trí tuệ và chậm phát triển trong mẫu khảo sát Pathways, không chứa biện pháp phòng tránh đi lạc.',
        'anchor': '',
    },
    {
        'code': 'D9E2C021A2',
        'grade': 0,
        'rationale': 'Bảng thống kê tỷ lệ đi lang thang theo tuổi và giới tính, không có biện pháp phòng ngừa.',
        'anchor': '',
    },
    {
        'code': '7BFC5881E4',
        'grade': 2,
        'rationale': 'Chia sẻ trải nghiệm căng thẳng của phụ huynh khi con tự kỷ bỏ chạy (eloped) ra khỏi tầm mắt gần nguồn nước và sự cần thiết của các biện pháp bảo đảm an toàn.',
        'anchor': 'learning can also affect water safety. One parent recalled a very stressful moment when her child elo',
    },
    {
        'code': 'F032E3A349',
        'grade': 0,
        'rationale': 'Bảng thống kê các yếu tố nguy cơ đi lang thang, không có văn bản hướng dẫn phòng tránh.',
        'anchor': '',
    },
    {
        'code': 'D4854D6A29',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả 4 câu hỏi khảo sát lịch sử đi lang thang của trẻ và mức độ lo lắng của phụ huynh.',
        'anchor': 'Elopement was assessed based on four questions about the child’s histo',
    },
    {
        'code': '556343BAC2',
        'grade': 2,
        'rationale': 'Đoạn phương pháp phân tích 15 mục trong bảng hỏi CSBQ liên quan trực tiếp đến sự an toàn của trẻ hay đi lang thang (khả năng gọi tên, nhận biết an toàn đường phố).',
        'anchor': 'Fifteen items from the CSBQ were identified as being exceptionally relevant to the safety of children who wander',
    },
    {
        'code': '0BD5854AC4',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bệnh tâm thần đồng mắc và lo âu ở thanh thiếu niên tự kỷ, không liên quan đến đi lạc.',
        'anchor': '',
    },
    {
        'code': '12A760D39A',
        'grade': 0,
        'rationale': 'Bảng số liệu thống kê mức độ an toàn và đi lang thang, không chứa hướng dẫn phòng ngừa.',
        'anchor': '',
    },
]

print(f"Total entries: {len(raw)}")
assert len(raw) == len(content_map), f"Mismatch: {len(raw)} != {len(content_map)}"

output_lines = []
for item in raw:
    code = item['code']
    assert code in content_map, f"Code {code} not in content_map"
    grade = item['grade']
    span = get_span(code, item['anchor'])
    if grade != 0:
        assert len(span) > 0, f"Span must not be empty for grade {grade} in {code}"
        assert span in content_map[code], f"Span not verbatim in {code}"
        assert len(span) <= 250, f"Span too long: {len(span)} chars in {code}"
    else:
        assert span == "", f"Span must be empty for grade 0 in {code}"
    
    obj = {
        'annotation_code': code,
        'grade': grade,
        'rationale': item['rationale'],
        'evidence_span': span,
        'confidence': 'high',
        'needs_review': False,
        'review_note': '',
        'annotation_type': 'ai_generated',
        'model': 'claude-sonnet-4-6',
        'prompt_version': 't2_4b_ai_v1',
    }
    output_lines.append(json.dumps(obj, ensure_ascii=False))

with open(returned_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"Successfully generated and verified {returned_path} with {len(output_lines)} annotations.")

