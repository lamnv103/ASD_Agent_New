import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_19'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q025.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q025':
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
        'code': '9F133A5309',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về phỏng vấn chẩn đoán ADI-R, không đề cập đến công cụ sàng lọc M-CHAT-R/F.',
        'anchor': '',
    },
    {
        'code': '3E4646EF66',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả quy trình sàng lọc hai giai đoạn trong đó Giai đoạn 1 sử dụng M-CHAT để xác định trẻ có nguy cơ cao trong cộng đồng.',
        'anchor': 'Phase I using M-CHAT to identify high-risk children in the general population',
    },
    {
        'code': 'A487BF7A4C',
        'grade': 3,
        'rationale': 'Đoạn văn nêu rõ điểm yếu cốt lõi về độ chính xác của M-CHAT-R/F là giá trị dự đoán dương tính (PPV) thấp dai dẳng, dẫn đến tỷ lệ dương tính giả cao.',
        'anchor': 'M-CHAT-R/F’s primary weakness',
    },
    {
        'code': 'DF93F65E6F',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu M-CHAT là bảng kiểm gồm 23 câu hỏi dành cho cha mẹ nhằm sàng lọc trẻ từ 18–30 tháng tuổi có nguy cơ cao mắc tự kỷ.',
        'anchor': 'Modified Checklist for Autism in Toddlers (M-CHAT) to screen children with high risk of ASD.',
    },
    {
        'code': 'A42E36C02C',
        'grade': 3,
        'rationale': 'Tổng hợp kết quả so sánh độ chính xác của M-CHAT-R/F với các công cụ sàng lọc nổi bật khác về độ nhạy, độ đặc hiệu và giá trị tiên đoán.',
        'anchor': 'comparative analysis of the M-CHAT-R/F against other prominent screening tools',
    },
    {
        'code': '16B5D90BFD',
        'grade': 3,
        'rationale': 'Kết luận của bài tổng quan hệ thống chỉ rõ M-CHAT-R/F không thể hiện tính hữu ích phổ quát và nhất quán như một công cụ sàng lọc ban đầu độc lập do PPV thấp.',
        'anchor': 'This systematic review concluded that the M-CHAT-R/F did not demonstrate consistent, universal utili',
    },
    {
        'code': '5C80771546',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả phương pháp phân tích độ chính xác sàng lọc của M-CHAT-R/F khi đối chiếu với các công cụ thay thế.',
        'anchor': 'comparative screening accuracy of the M-CHAT-R/F',
    },
    {
        'code': '5080D46133',
        'grade': 2,
        'rationale': 'Đoạn văn phân tích sự biến thiên đáng kể về hiệu suất sàng lọc của M-CHAT-R/F giữa bối cảnh cộng đồng và cơ sở lâm sàng.',
        'anchor': 'Current research shows a considerable variation in outcomes',
    },
    {
        'code': 'F44C10F5AD',
        'grade': 1,
        'rationale': 'Tiêu chí lựa chọn nghiên cứu so sánh các chỉ số độ chính xác của M-CHAT-R/F với các công cụ sàng lọc khác.',
        'anchor': 'compared the accuracy metrics of the M-CHAT-R/F with alternative screening tools',
    },
    {
        'code': 'D66041F695',
        'grade': 3,
        'rationale': 'Đoạn văn định nghĩa M-CHAT-R/F là công cụ sàng lọc được áp dụng rộng rãi trên toàn cầu, đồng thời chỉ ra các nghiên cứu gần đây đặt dấu hỏi về độ nhạy và độ đặc hiệu tối ưu.',
        'anchor': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) a widely adopted tool globally',
    },
    {
        'code': '7C87F80894',
        'grade': 3,
        'rationale': 'Kết quả tổng quan xác định hồ sơ hiệu suất phức tạp của M-CHAT-R/F: độ nhạy phát hiện ca bệnh cao nhưng độ đặc hiệu thấp dẫn đến nhiều ca dương tính giả.',
        'anchor': 'From 172 identified articles, six high-quality studies encompassing',
    },
    {
        'code': '7967005F30',
        'grade': 0,
        'rationale': 'Bảng chú giải các từ viết tắt tên công cụ, không chứa dữ liệu độ chính xác.',
        'anchor': '',
    },
    {
        'code': 'D8C5675D52',
        'grade': 1,
        'rationale': 'Mô tả kết quả tìm kiếm xác định 6 nghiên cứu so sánh trực tiếp giữa M-CHAT-R/F và công cụ khác.',
        'anchor': 'direct comparison between the M-CHAT-R/F and an alternative screening tool',
    },
    {
        'code': '54625D7900',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả quan sát hành vi BOSA, không liên quan đến M-CHAT-R/F.',
        'anchor': '',
    },
    {
        'code': '626A5794AC',
        'grade': 3,
        'rationale': 'Tóm tắt phát hiện nghiên cứu chỉ ra M-CHAT-R/F có độ nhạy biến thiên, giá trị dự đoán dương tính (PPV) thấp dai dẳng và dễ dẫn đến chẩn đoán sót ở mức độ nhẹ.',
        'anchor': 'M-CHAT-R/F exhibits variable sensitivity, a persistently low positive predictive value',
    },
    {
        'code': '4C01A2AC56',
        'grade': 2,
        'rationale': 'Phương pháp tổng hợp dữ liệu chiết xuất độ nhạy, độ đặc hiệu, PPV và NPV cho M-CHAT-R/F và các công cụ so sánh.',
        'anchor': 'sensitivity, specificity, PPV and NPV for both the M-CHAT-R/F and its comparator tools',
    },
    {
        'code': 'DE580D95CB',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích nguồn gốc của M-CHAT là phiên bản sửa đổi được phát triển nhằm nâng cao độ chính xác sàng lọc của bảng kiểm CHAT ban đầu.',
        'anchor': 'The M-CHAT was later shortened to ten questions in order to make it more convenient',
    },
    {
        'code': 'EBAE3184C8',
        'grade': 2,
        'rationale': 'Đoạn thảo luận ghi nhận M-CHAT là phương pháp sàng lọc được sử dụng phổ biến nhất để phát hiện tự kỷ với các nghiên cứu đánh giá độ nhạy và đặc hiệu.',
        'anchor': 'The M-CHAT, AQ, and CBSL are the screening methods most commonly used',
    },
    {
        'code': 'FF6B46CD06',
        'grade': 3,
        'rationale': 'Bảng so sánh cụ thể cho thấy M-CHAT-R/F có độ nhạy và giá trị dự đoán dương tính (PPV) thấp hơn đáng kể so với công cụ kỹ thuật số Q-CHAT-10.',
        'anchor': 'M-CHAT-R/F performed poorly, with low sensitivity and PPV',
    },
    {
        'code': 'AFDD171B87',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về sự cần thiết của phỏng vấn theo dõi (Follow-up) trong M-CHAT để nâng cao PPV và giảm thiểu tỷ lệ dương tính giả.',
        'anchor': 'follow-up interviews to improve the PPV and minimize the false-positiv',
    },
    {
        'code': '2A0BB83C4F',
        'grade': 2,
        'rationale': 'Đoạn văn lưu ý những hạn chế về độ chính xác của M-CHAT khi áp dụng trên quần thể trẻ sinh non (ex-preterm).',
        'anchor': 'Modified Checklist for Autism in Toddlers (M-CHAT), while widely used, shows limitations in the ex-preterm population',
    },
    {
        'code': '8F620C1C02',
        'grade': 1,
        'rationale': 'Chiến lược tìm kiếm tài liệu về độ chính xác sàng lọc của M-CHAT trên các cơ sở dữ liệu y khoa.',
        'anchor': 'A systematic literature search was conducted across four databases',
    },
    {
        'code': '740D779A5E',
        'grade': 1,
        'rationale': 'Đoạn văn nhận định các công cụ sàng lọc như M-CHAT vẫn cần thêm nghiên cứu thực nghiệm trên các bộ dữ liệu đa dạng.',
        'anchor': 'The tools such as M-CHAT, FYI, GADS, and ASAS',
    },
    {
        'code': '26322AAE81',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ lý do lựa chọn M-CHAT để sàng lọc tự kỷ ở trẻ em do công cụ này đã được sử dụng rộng rãi và chuẩn hóa tại Việt Nam.',
        'anchor': 'In this study, we used M-CHAT for screening ASD among the studied children as it has been widely use',
    },
    {
        'code': 'FC788C4617',
        'grade': 0,
        'rationale': 'Chú thích bảng thống kê không chứa dữ liệu độ chính xác.',
        'anchor': '',
    },
    {
        'code': 'F47CAAD305',
        'grade': 1,
        'rationale': 'Mô tả phương pháp so sánh độ chính xác của M-CHAT-R/F với các công cụ sàng lọc nâng cao kỹ thuật số mới.',
        'anchor': 'how the M-CHAT-R/F compares with newly developed and digitally enhanced screening tools',
    },
    {
        'code': '5C7A1F5907',
        'grade': 2,
        'rationale': 'Đoạn phương pháp mô tả quy trình áp dụng bảng kiểm M-CHAT trong giai đoạn sàng lọc tại cộng đồng ở Việt Nam.',
        'anchor': 'Modified Checklist for Autism in Toddlers (M-CHAT) was utilized for the screening phase of our study.',
    },
    {
        'code': '836DAB3FE9',
        'grade': 2,
        'rationale': 'Đoạn thảo luận nhận định ưu thế dự đoán của M-CHAT-R/F đang dần bị thách thức bởi sự xuất hiện của các công cụ sàng lọc kỹ thuật số mới.',
        'anchor': 'comparative advantage of the M-CHAT-R/F’s predictive value is increasingly challenged',
    },
    {
        'code': 'C0DF942964',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu nghiên cứu chuẩn hóa gốc của M-CHAT-R/F trên mẫu 16.071 trẻ: thời gian thực hiện 10 phút, độ nhạy đạt 0,91 và độ đặc hiệu đạt 0,95.',
        'anchor': 'The M-CHAT-R/F takes about 10 min to complete.',
    },
    {
        'code': 'C0EAB0686F',
        'grade': 1,
        'rationale': 'Tiêu chí thu nạp nghiên cứu so sánh độ chính xác sàng lọc của M-CHAT-R/F với các công cụ khác.',
        'anchor': 'screening accuracy of the M-CHAT-R/F to that of other screening tools',
    },
    {
        'code': 'FDEEFB0261',
        'grade': 3,
        'rationale': 'Đoạn văn giới thiệu định nghĩa hoàn chỉnh của M-CHAT-R/F: bảng kiểm sửa đổi có phỏng vấn theo dõi, gồm hai giai đoạn do cha mẹ trả lời để sàng lọc trẻ 16–30 tháng tuổi.',
        'anchor': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) has become a prominent two-stage, parent-dependent screening tool',
    },
    {
        'code': '0962FBC376',
        'grade': 1,
        'rationale': 'Đoạn văn đánh giá chất lượng phương pháp luận cao và nguy cơ sai lệch thấp của 6 nghiên cứu về độ chính xác M-CHAT-R/F.',
        'anchor': 'All six included studies demonstrated high methodological quality',
    },
    {
        'code': '1CD05755ED',
        'grade': 2,
        'rationale': 'Tổng quan kiến thức hiện có khẳng định M-CHAT-R/F duy trì độ chính xác chẩn đoán đáng tin cậy so với các công cụ sàng lọc truyền thống.',
        'anchor': 'Modified Checklist for Autism in Toddlers, Revised with Follow-Up (M-CHAT-R/F) maintain reliable diagnostic accuracy',
    },
    {
        'code': '05261F4569',
        'grade': 3,
        'rationale': 'Đoạn thảo luận phân tích sâu: M-CHAT-R/F hoạt động như một công cụ sàng lọc có độ nhạy cao nhưng độ đặc hiệu thấp, dẫn đến số lượng lớn trường hợp dương tính giả cần chuyển tuyến chuyên sâu.',
        'anchor': 'the M-CHAT-R/F functions as a highly sensitive, yet low specificity, screening tool',
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

