import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_17.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_17'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q059.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q059':
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
        'code': 'F9EAEFC5F4',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bệnh tâm thần đồng mắc và lo âu ở thanh thiếu niên tự kỷ, không liên quan đến tế bào gốc hay điều trị tự kỷ.',
        'anchor': '',
    },
    {
        'code': '4A2BAEAA77',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu triệu chứng tiêu hóa ở trẻ tự kỷ, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '4EB4D48765',
        'grade': 0,
        'rationale': 'Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '8CE617814A',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về rối loạn tic và hội chứng Tourette ở người tự kỷ, không nhắc đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '796CE27890',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về hệ vi sinh đường ruột và các triệu chứng tiêu hóa ở trẻ tự kỷ, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '92111DF175',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh mức độ lo âu giữa các nhóm trẻ tự kỷ và ADHD, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'CAEF8BFA7C',
        'grade': 0,
        'rationale': 'Bảng phụ lục thống kê cỡ mẫu nghiên cứu tại Việt Nam, không có thông tin về tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'A77F56C96E',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận khoảng trống nghiên cứu tự kỷ tại Việt Nam, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'EA5B8AFCE5',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các thử nghiệm liệu pháp gen và điều trị nhắm trúng đích đảo ngược biến đổi sinh học thần kinh ở các hội chứng di truyền liên quan tự kỷ.',
        'anchor': 'many conditions have targeted treatments that can help to reverse the neurobiological changes in the brain',
    },
    {
        'code': '38FD9C473C',
        'grade': 0,
        'rationale': 'Bảng viết tắt các công cụ giao tiếp tăng cường (AAC), không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'D3DBD871B3',
        'grade': 0,
        'rationale': 'Tổng quan về chẩn đoán và sàng lọc tự kỷ theo DSM-5-TR, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'D72DDD136B',
        'grade': 1,
        'rationale': 'Đoạn văn cung cấp thông tin y tế về việc dùng thuốc điều trị các triệu chứng cụ thể đi kèm ở người tự kỷ, cung cấp bối cảnh điều trị.',
        'anchor': 'A health care provider may prescribe medication to treat specific symptoms',
    },
    {
        'code': '6573FE0FDC',
        'grade': 0,
        'rationale': 'Mô tả thử nghiệm sử dụng chế phẩm sinh học probiotic ở trẻ tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '136AC31223',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về khó khăn cảm xúc và lo âu ở thanh thiếu niên tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '8801116DA4',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về Đạo luật Autism CARES và các viện tài trợ nghiên cứu của NIH, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '7E4853AA6E',
        'grade': 0,
        'rationale': 'Đoạn tóm tắt nghiên cứu về triệu chứng ADHD và lo âu ở người tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'A20C8D7DFB',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về tỷ lệ hiện mắc và gánh nặng của bệnh tự kỷ tại Việt Nam và thế giới, không chứa thông tin về tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'A3822A7942',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu kỹ thuật kích thích não không xâm lấn (tDCS) như liệu pháp sinh học thử nghiệm ở trẻ em tự kỷ.',
        'anchor': 'NIBS techniques, such as tDCS, have been recently proposed in pediatric populations to explore its effect on brain plasticity',
    },
    {
        'code': '997C11EA71',
        'grade': 0,
        'rationale': 'Bảng thống kê tỷ lệ tham gia trong nghiên cứu melatonin cho giấc ngủ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '58406A7911',
        'grade': 0,
        'rationale': 'Đoạn thảo luận về nghiên cứu tự kỷ tại Việt Nam và phơi nhiễm dioxin, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '119D1995F6',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các bệnh lý tâm thần đồng mắc ở người tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '633712CDB8',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu về hoạt chất carnosine như một chất chống oxy hóa được thử nghiệm hỗ trợ trẻ tự kỷ, cung cấp bối cảnh bổ sung sinh học.',
        'anchor': 'Carnosine or L-carnosine is a dipeptide composed by alanine and histidine, which acts as an antitoxi',
    },
    {
        'code': '69EC4342E9',
        'grade': 0,
        'rationale': 'Đoạn phân tích mối liên hệ bệnh sinh giữa bệnh động kinh và tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'D5600905E9',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về liệu pháp massage như một can thiệp không dùng thuốc hỗ trợ trẻ tự kỷ, cung cấp bối cảnh trị liệu.',
        'anchor': 'The use of massage in autistic children with sleep problems is based on theoretical grounds',
    },
    {
        'code': '025400E6C0',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'AEE1BD62C8',
        'grade': 0,
        'rationale': 'Bảng tóm tắt kết quả phân tích tổng hợp các can thiệp sớm cho tự kỷ, không đề cập đến liệu pháp tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '69704EF5B7',
        'grade': 0,
        'rationale': 'Thông tin liên hệ tham khảo MedlinePlus, không chứa thông tin về tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'D8F6B94C74',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về kỳ thị văn hóa liên quan đến chẩn đoán tự kỷ tại Việt Nam, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '33119CF583',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về dị ứng thực phẩm và triệu chứng tiêu hóa ở trẻ tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'A81997F371',
        'grade': 0,
        'rationale': 'Tiêu chuẩn chẩn đoán tự kỷ theo DSM, không có nội dung về tế bào gốc hay chữa bệnh.',
        'anchor': '',
    },
    {
        'code': 'A839CC3F4A',
        'grade': 1,
        'rationale': 'Tài liệu của CDC về các liệu pháp tâm lý hỗ trợ người tự kỷ kiểm soát lo âu, trầm cảm, cung cấp bối cảnh can thiệp toàn diện.',
        'anchor': 'Psychological approaches can help people with ASD cope with anxiety, depression, and other mental he',
    },
    {
        'code': 'A131E3A552',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '6B01D08DCA',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về đáp ứng miễn dịch bất thường và cytokine tiền viêm ở người tự kỷ, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'CB4631D590',
        'grade': 1,
        'rationale': 'Tài liệu chính thức của CDC khẳng định hiện không có thuốc hay phương pháp nào chữa khỏi các triệu chứng cốt lõi của tự kỷ, cung cấp bối cảnh quan trọng về việc chưa có cách chữa khỏi tự kỷ.',
        'anchor': 'There are no medications that treat the core symptoms of ASD.',
    },
    {
        'code': 'AEFEF75B95',
        'grade': 0,
        'rationale': 'Bảng chú giải viết tắt trong bài báo tổng quan, không có nội dung về tế bào gốc.',
        'anchor': '',
    },
    {
        'code': 'F2E08850CC',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về tỷ lệ đi lang thang ở trẻ khuyết tật phát triển tại Mỹ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '7462ECC60A',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu về các công cụ sàng lọc và chẩn đoán tự kỷ, không liên quan đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '24711192F9',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích các đột biến gen đơn nucleotide phát hiện qua giải trình tự WES và WGS, không đề cập đến tế bào gốc.',
        'anchor': '',
    },
    {
        'code': '872BF71B8D',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các triệu chứng ADHD và lo âu ở trẻ tự kỷ, không liên quan đến tế bào gốc.',
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

