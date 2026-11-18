import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_14'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q064.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q064':
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
        'code': '27E1E5E7D5',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về hệ vi sinh đường ruột và các triệu chứng tiêu hóa ở trẻ tự kỷ, không đề cập đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '8B954FBF2C',
        'grade': 1,
        'rationale': 'Đoạn văn hướng dẫn bác sĩ chuyển tuyến trẻ nghi ngờ tự kỷ hoặc khuyết tật phát triển đến chuyên viên ngôn ngữ trị liệu để đánh giá kỹ năng giao tiếp.',
        'anchor': 'If a doctor suspects a child has ASD or another developmental disability, he or she usually will refer the child to a variety of specialists, including a speech-language pathologist.',
    },
    {
        'code': '478FD48AD4',
        'grade': 1,
        'rationale': 'Đoạn văn đề cập đến các kháng thể tự miễn ở mẹ liên quan đến chậm phát triển ngôn ngữ và đầu to ở khoảng 10% trường hợp tự kỷ.',
        'anchor': 'confirmed in ~10% of ASD cases, linked to language delay and macrocephaly',
    },
    {
        'code': 'D249B7FADF',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu định nghĩa tự kỷ bao gồm khiếm khuyết về hành vi xã hội, giao tiếp và ngôn ngữ kèm theo các hành vi lặp lại.',
        'anchor': 'some degree of impaired social behavior, communication and language, and a narrow range of interests and activities',
    },
    {
        'code': 'E8F6E08785',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về mối liên hệ giữa táo bón và các vấn đề lời nói ở trẻ tự kỷ, không trả lời việc trẻ chậm nói có phải tự kỷ không.',
        'anchor': '',
    },
    {
        'code': '131D096F81',
        'grade': 0,
        'rationale': 'Đoạn tóm tắt nghiên cứu về triệu chứng ADHD và lo âu ở người tự kỷ, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': 'F6BD7A0ACA',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa tự kỷ theo DSM-5-TR với các thách thức về tương tác xã hội và giao tiếp, cung cấp bối cảnh lâm sàng.',
        'anchor': 'Autism Spectrum Disorder (ASD) is a neurodevelopmental condition characterized by challenges in social interaction and communication and the presence of restricted interests and repetitive behaviors',
    },
    {
        'code': '29E2726699',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích chi tiết ảnh hưởng của tự kỷ lên khả năng giao tiếp: một số trẻ tự kỷ không thể nói hoặc kỹ năng nói rất hạn chế, trong khi những trẻ khác lại có vốn từ phong phú.',
        'anchor': 'Some children with ASD may not be able to communicate using speech or language, and some may have very limited speaking skills. Others may have rich vocabularies',
    },
    {
        'code': 'E03AE499C2',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu công cụ sàng lọc CSCS-DP nhằm phát hiện sớm nguy cơ khuyết tật giao tiếp và chức năng biểu tượng ở trẻ nhỏ.',
        'anchor': 'CSCS-DP, to identify the risk of communication and symbolic functioning disabilities in infants',
    },
    {
        'code': 'D74BBD0072',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích rõ rằng các hành vi và sở thích hạn chế, lặp lại chính là điểm khác biệt cốt lõi phân biệt tự kỷ với các tình trạng chỉ có vấn đề về giao tiếp xã hội thuần túy.',
        'anchor': 'These behaviors or interests set ASD apart from conditions defined by problems with social communication and interaction only.',
    },
    {
        'code': 'A852A492E5',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích về tính kén ăn và các giả thuyết đa chiều ở trẻ tự kỷ, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': 'F330FE4593',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận khoảng trống nghiên cứu tự kỷ tại Việt Nam, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': 'E44B8978F2',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh mức độ lo âu giữa các nhóm trẻ tự kỷ và ADHD, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '8C47C4D855',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về tỷ lệ đi lang thang ở trẻ khuyết tật phát triển tại Mỹ, không đề cập đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '9FF0EEDB76',
        'grade': 0,
        'rationale': 'Lời khuyên chung về việc trao đổi với bác sĩ nếu lo lắng về sự phát triển của trẻ, không chứa thông tin phân biệt chậm nói và tự kỷ.',
        'anchor': '',
    },
    {
        'code': '08B90E5549',
        'grade': 0,
        'rationale': 'Thông tin liên hệ của CDC khi có lo lắng về sự phát triển của trẻ, không chứa nội dung chuyên môn về chậm nói.',
        'anchor': '',
    },
    {
        'code': '1E001C07FA',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa phổ tự kỷ gây ra các thách thức đáng kể về xã hội, giao tiếp và hành vi, cung cấp bối cảnh chẩn đoán.',
        'anchor': 'Autism spectrum disorder (ASD) is a developmental disability that can cause significant social, communication, and behavioral challenges.',
    },
    {
        'code': '0F86ABCC42',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả các đặc điểm bất thường về giọng điệu và cách sử dụng lời nói rập khuôn ở trẻ tự kỷ.',
        'anchor': 'Taken together, these difficulties affect the ability of children with ASD to interact with others',
    },
    {
        'code': '8444D4DB14',
        'grade': 0,
        'rationale': 'Đoạn văn bàn luận về hạn chế định nghĩa "ít lời nói" trong các nghiên cứu can thiệp, không giúp trả lời trẻ chậm nói có phải tự kỷ không.',
        'anchor': '',
    },
    {
        'code': '800915582B',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu công cụ sàng lọc ICT tập trung vào việc dự đoán tình trạng chậm phát triển ngôn ngữ trước khi trẻ bắt đầu biết nói.',
        'anchor': 'the focus of ICT is on predicting language delays before the child is even starting to talk.',
    },
    {
        'code': '3D6188CAEA',
        'grade': 0,
        'rationale': 'Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '952FD6D7DA',
        'grade': 0,
        'rationale': 'Bảng phụ lục thống kê số lượng mẫu trong tài liệu tổng quan, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '4D2A261C92',
        'grade': 3,
        'rationale': 'Đoạn văn trả lời trực tiếp câu hỏi: nêu rõ chậm nói thường là dấu hiệu nhận biết sớm của tự kỷ, nhưng có tính không đồng nhất cao (một số trẻ có vốn từ bình thường nhưng gặp khó khăn về thực hành ngữ dụng, số khác bị suy giảm ngôn ngữ toàn diện).',
        'anchor': 'Speech delay is often an early marker of ASD, but heterogeneity is high: some children acquire age-appropriate vocabulary yet struggle with pragmatics',
    },
    {
        'code': 'CEF03DA6E0',
        'grade': 1,
        'rationale': 'Đoạn văn trích dẫn kết quả nghiên cứu cho thấy trẻ tự kỷ có mức độ suy giảm giao tiếp và tương tác xã hội cao nhất so với nhóm ADHD.',
        'anchor': 'Salley et al. reported that people with ASD demonstrated the highest communication and social interaction deficit',
    },
    {
        'code': 'A0804B2C9C',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu về các triệu chứng lo âu và ADHD đồng mắc ở trẻ tự kỷ, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '9516772F64',
        'grade': 0,
        'rationale': 'Tài liệu tập huấn kỹ năng người chăm sóc hướng dẫn các bước lôi cuốn trẻ tham gia hoạt động, không phân biệt chậm nói và tự kỷ.',
        'anchor': '',
    },
    {
        'code': '754EF61E05',
        'grade': 3,
        'rationale': 'Đoạn văn phân tích toàn diện về khiếm khuyết ngôn ngữ và lời nói ở tự kỷ: chậm nói từ đơn và câu ngắn rất phổ biến, nhưng khiếm khuyết ngữ dụng xã hội mới là đặc điểm gần như phổ quát ở mọi cá nhân tự kỷ.',
        'anchor': 'Speech and language impairments are among the most recognizable features of ASD. Difficulties include delays in first words, limited phrase speech, and atypical prosody',
    },
    {
        'code': '6FD27D62A6',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu về các triệu chứng tự kỷ ảnh hưởng đến kỹ năng xã hội hóa, hành vi lặp lại và giao tiếp bằng lời nói hoặc biểu cảm.',
        'anchor': 'hinders an individual’s skills in socialisation, creates repetitive behaviours, and impacts expressive or verbal communication',
    },
    {
        'code': '045C3839F5',
        'grade': 1,
        'rationale': 'Đoạn văn nêu rõ quy trình đánh giá chẩn đoán đa chuyên khoa bao gồm chuyên viên âm ngữ trị liệu và bác sĩ nhi phát triển.',
        'anchor': 'speech-language pathologist, and developmental–behavioral pediatrician',
    },
    {
        'code': 'E64B9329C9',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa tự kỷ là rối loạn hành vi thần kinh với các khiếm khuyết về giao tiếp xã hội và hành vi lặp lại.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors',
    },
    {
        'code': 'AE348CDE1F',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu chương trình theo dõi mốc phát triển của CDC "Learn the Signs. Act Early.", không phân tích chuyên sâu về chẩn đoán phân biệt.',
        'anchor': '',
    },
    {
        'code': 'BC68559C27',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích các bệnh lý tâm thần đồng mắc ở người tự kỷ, không thảo luận về chậm nói.',
        'anchor': '',
    },
    {
        'code': 'B380440051',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả đặc điểm nhân khẩu học và bối cảnh văn hóa Việt Nam, không đề cập đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '23C8D88642',
        'grade': 1,
        'rationale': 'Đoạn văn nêu rõ định nghĩa tự kỷ bao gồm các khó khăn dai dẳng về giao tiếp xã hội và các hành vi định hình lặp lại.',
        'anchor': 'characterized by persistent difficulties in social communication and restricted, repetitive behaviors',
    },
    {
        'code': '66D499C5C8',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bệnh tâm thần đồng mắc và lo âu ở thanh thiếu niên tự kỷ, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': 'A6DB820AC7',
        'grade': 2,
        'rationale': 'Đoạn tài liệu của CDC liệt kê các dấu hiệu cảnh báo cụ thể về kỹ năng giao tiếp và tương tác xã hội ở trẻ tự kỷ theo từng mốc tháng tuổi (không đáp lại tên, không có biểu cảm khuôn mặt, không chỉ trỏ).',
        'anchor': 'Social communication and interaction skills can be challenging for people with ASD.',
    },
    {
        'code': 'DAF86C5DEC',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu các nghiên cứu can thiệp nâng cao khả năng giao tiếp ở trẻ tự kỷ có kỹ năng ngôn ngữ và lời nói bị hạn chế.',
        'anchor': 'Some of these studies involve children with ASD who have limited speech and language skills',
    },
    {
        'code': 'F942A0E2E3',
        'grade': 2,
        'rationale': 'Tiêu chuẩn chẩn đoán DSM chỉ rõ: những trẻ có khiếm khuyết rõ rệt về giao tiếp xã hội nhưng không đáp ứng tiêu chuẩn tự kỷ (không có hành vi lặp lại) cần được đánh giá rối loạn giao tiếp xã hội (ngữ dụng); đồng thời cần ghi rõ tự kỷ có kèm theo suy giảm ngôn ngữ hay không.',
        'anchor': 'Individuals who have marked deficits in social communication, but whose symptoms do not otherwise meet criteria for autism spectrum disorder, should be evaluated for social (pragmatic) communication disorder.',
    },
    {
        'code': '8029411FE1',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về ảnh hưởng của bệnh động kinh lên chức năng nhận thức và xã hội ở trẻ tự kỷ, không giúp phân biệt chậm nói và tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'C423D96C93',
        'grade': 0,
        'rationale': 'Đoạn kết luận chung của bài viết về việc điều trị các bệnh đồng mắc ở trẻ tự kỷ, không đề cập đến chậm nói.',
        'anchor': '',
    },
    {
        'code': '83AD866396',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả các hành vi định hình vận động tay/ngón tay ở trẻ tự kỷ, không thảo luận về chậm nói.',
        'anchor': '',
    },
    {
        'code': 'CC650D38CC',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bất thường dẫn truyền thần kinh và xét nghiệm gen ở bệnh nhân tự kỷ, không liên quan đến chậm nói.',
        'anchor': '',
    },
    {
        'code': 'CD14707E4A',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa tổng quát tự kỷ bao gồm khó khăn về giao tiếp xã hội và tương tác với người khác, cùng với sở thích hạn hẹp.',
        'anchor': 'Difficulty with social communication and interaction with other people',
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

