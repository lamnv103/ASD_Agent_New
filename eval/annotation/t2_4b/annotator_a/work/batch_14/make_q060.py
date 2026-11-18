import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_14'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q060.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q060':
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
        'code': '9F26C39B84',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu về triệu chứng tiêu hóa, không thảo luận chế độ ăn không gluten/casein.',
        'anchor': '',
    },
    {
        'code': 'EDF425DBF9',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận khoảng trống nghiên cứu về tự kỷ tại Việt Nam, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '84C59C931C',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu các nghiên cứu cải thiện giao tiếp và các viện NIH tài trợ, không đề cập đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': 'B304E1BF52',
        'grade': 2,
        'rationale': 'Đoạn văn báo cáo thử nghiệm RCT của Ghalichi et al. đánh giá chế độ ăn không gluten trong 6 tuần ở trẻ tự kỷ, cho thấy giảm triệu chứng tiêu hóa và rối loạn hành vi.',
        'anchor': 'Ghalichi et al. [32] conducted a small RCT that investigated the effect of a six-week gluten-free diet on GIS and behavioral indices in children with ASD',
    },
    {
        'code': 'C983E9B423',
        'grade': 0,
        'rationale': 'Bài viết về quản lý rối loạn giấc ngủ ở trẻ tự kỷ bằng các biện pháp không dùng thuốc, không liên quan đến chế độ ăn GFCF.',
        'anchor': '',
    },
    {
        'code': '52FB6B00EA',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh mức độ lo âu giữa các nhóm trẻ tự kỷ và ADHD, không nhắc đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '793D7B696B',
        'grade': 2,
        'rationale': 'Đoạn thảo luận chỉ ra dữ liệu về không dung nạp gluten ở người tự kỷ còn gây tranh cãi và có rất ít bằng chứng về hiệu quả của các liệu pháp ăn kiêng trong điều trị tự kỷ.',
        'anchor': 'some studies have found little evidence of the efficacy of nutritional supplements and dietary therapies',
    },
    {
        'code': 'D1D1A061C7',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về tỷ lệ đi lang thang ở trẻ khuyết tật phát triển tại Mỹ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '20770E4247',
        'grade': 1,
        'rationale': 'Đoạn văn ghi nhận thực tế nhiều trẻ tự kỷ áp dụng chế độ ăn hạn chế gluten và sữa liên quan đến chứng kén ăn.',
        'anchor': 'subjects followed a diet, mostly based on gluten and milk restriction, including individuals exhibiting food selectivity.',
    },
    {
        'code': 'E867E7A7C6',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về bối cảnh văn hóa và kỳ thị liên quan đến tự kỷ tại Việt Nam, không đề cập đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '894DBB0D76',
        'grade': 0,
        'rationale': 'Đoạn tổng quan về các công cụ sàng lọc và chẩn đoán tự kỷ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '17C3E5C889',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các vấn đề tâm thần và lo âu đồng mắc ở trẻ tự kỷ và ADHD, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '9112EEB916',
        'grade': 0,
        'rationale': 'Đoạn văn nói về carnosine đối với giấc ngủ ở trẻ tự kỷ, không đề cập đến chế độ ăn không gluten/casein.',
        'anchor': '',
    },
    {
        'code': 'E527C449CC',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu tiêu hóa trong tự kỷ, không có nội dung về chế độ ăn gluten/casein.',
        'anchor': '',
    },
    {
        'code': 'CC23FE6162',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD đồng mắc ở trẻ tự kỷ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': '98BC9B2B51',
        'grade': 1,
        'rationale': 'Đoạn văn nêu một số nghiên cứu gợi ý trẻ tự kỷ có thể có nguy cơ cao hơn về nhạy cảm với gluten, nhưng chưa xác định được bệnh sinh tiêu hóa đặc thù.',
        'anchor': 'Though some studies suggest that autistic children may be at higher risk for gluten sensitivity, lactase deficiencies, and even intestinal inflammation',
    },
    {
        'code': 'F57EEB305B',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về bổ sung men vi sinh và hệ vi sinh đường ruột ở trẻ tự kỷ, không thảo luận chế độ ăn GFCF.',
        'anchor': '',
    },
    {
        'code': 'B0D24992E5',
        'grade': 0,
        'rationale': 'Hướng dẫn đánh giá chỉ số khối cơ thể và thói quen ăn uống trước can thiệp giáo dục, không đánh giá hiệu quả chế độ ăn GFCF.',
        'anchor': '',
    },
    {
        'code': 'FDB7BD0159',
        'grade': 0,
        'rationale': 'Tổng quan về các công cụ đánh giá và chẩn đoán tự kỷ theo DSM-5-TR, không liên quan đến dinh dưỡng.',
        'anchor': '',
    },
    {
        'code': 'DF3DC8CFAF',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu tiêu hóa trong tự kỷ, không đề cập đến chế độ ăn không gluten/casein.',
        'anchor': '',
    },
    {
        'code': 'F721BC12C7',
        'grade': 1,
        'rationale': 'Đoạn văn đề cập đến sự phổ biến của các khuyến nghị ăn kiêng trong cộng đồng tự kỷ và khẳng định cần nghiên cứu thêm để xác thực.',
        'anchor': 'Given the popularity of many of these dietary recommendations among the autism community at large, further investigation is warranted to better validate their use.',
    },
    {
        'code': '9AEEDA1523',
        'grade': 0,
        'rationale': 'Đoạn văn nhấn mạnh tính chặt chẽ về phương pháp khi đánh giá các triệu chứng tiêu hóa, không đánh giá chế độ ăn GFCF.',
        'anchor': '',
    },
    {
        'code': 'A3CC929567',
        'grade': 2,
        'rationale': 'Đoạn văn báo cáo nghiên cứu của Grimaldi et al. gợi ý hiệu quả hiệp đồng đối với hành vi khi kết hợp prebiotic và chế độ ăn loại trừ gluten/casein.',
        'anchor': 'synergistic effect on behavior resulted from the combination of prebiotic and casein/gluten-free exclusion diet.',
    },
    {
        'code': '05765581B4',
        'grade': 3,
        'rationale': 'Đoạn văn trả lời trực tiếp câu hỏi: trích dẫn tổng quan hệ thống của Mulloy et al. kết luận các nghiên cứu hiện có không ủng hộ việc sử dụng chế độ ăn GFCF để điều trị tự kỷ và cảnh báo nguy cơ giảm mật độ xương.',
        'anchor': 'Mulloy et al. [80] conducted a systematic review of GFCF diets when implemented in the treatment of ASD, concluding that the published studies they identified do not support the use of these diets in the treatment of ASD.',
    },
    {
        'code': 'C1DD040DEF',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến dinh dưỡng.',
        'anchor': '',
    },
    {
        'code': '365B85DC1C',
        'grade': 0,
        'rationale': 'Tiêu chuẩn chẩn đoán tự kỷ theo DSM, không chứa nội dung về chế độ ăn uống.',
        'anchor': '',
    },
    {
        'code': '9BF6741056',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích tỷ lệ lo âu và ADHD ở người tự kỷ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': 'D8E99B679D',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về tình trạng thiếu hụt dinh dưỡng và tính kén ăn ở trẻ tự kỷ, không đánh giá chế độ ăn GFCF chữa tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'DC453289E2',
        'grade': 2,
        'rationale': 'Bảng tổng hợp chi tiết nghiên cứu RCT của Ghalichi et al. về tác động của chế độ ăn không gluten lên triệu chứng tiêu hóa và hành vi ở trẻ tự kỷ.',
        'anchor': 'Investigated the effect of a gluten-free diet on GIS and behavior in ASD children.',
    },
    {
        'code': '8FB795231E',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu tiêu hóa trong tự kỷ, không chứa nội dung về chế độ ăn không gluten/casein.',
        'anchor': '',
    },
    {
        'code': '8908DB871E',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': 'E3F7716AAC',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về tỷ lệ hiện mắc và gánh nặng của bệnh tự kỷ tại Việt Nam và thế giới, không đề cập đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': 'CA949BB29E',
        'grade': 0,
        'rationale': 'Đoạn tóm tắt nghiên cứu về triệu chứng ADHD và lo âu ở người tự kỷ, không liên quan đến chế độ ăn.',
        'anchor': '',
    },
    {
        'code': 'A9CABD4888',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu tiêu hóa trong tự kỷ, không có nội dung về chế độ ăn gluten/casein.',
        'anchor': '',
    },
    {
        'code': '2E090CA8B1',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bệnh tự miễn và bất thường miễn dịch ở người tự kỷ, không đề cập đến chế độ ăn GFCF.',
        'anchor': '',
    },
    {
        'code': '04B448BCBD',
        'grade': 0,
        'rationale': 'Đoạn văn nói về táo bón và tính kén ăn ở trẻ tự kỷ do thiếu chất xơ, không liên quan đến việc ăn kiêng GFCF để chữa tự kỷ.',
        'anchor': '',
    },
    {
        'code': '024BF988D5',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng tiêu hóa thường gặp ở trẻ tự kỷ, không đề cập đến chế độ ăn không gluten hay casein.',
        'anchor': '',
    },
    {
        'code': '8075A428CA',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về động kinh và các cơ chế sinh học phân tử đồng mắc ở trẻ tự kỷ, không liên quan đến chế độ ăn.',
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

