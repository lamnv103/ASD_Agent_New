import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_16'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q049.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q049':
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
        'code': 'FD25F8AA2C',
        'grade': 3,
        'rationale': 'Đoạn văn trích Khuyến nghị 4 của WHO: các can thiệp hỗ trợ sức khỏe tinh thần bà mẹ cần được lồng ghép vào các dịch vụ phát triển và sức khỏe trẻ em.',
        'anchor': 'Based on the review, the findings for maternal outcomes',
    },
    {
        'code': 'DCF6057E3D',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả các cân nhắc can thiệp của WHO đối với các quần thể nguy cơ cao dựa trên các hướng dẫn có sẵn.',
        'anchor': 'based on other WHO guidelines and statements',
    },
    {
        'code': 'E749CFCA70',
        'grade': 3,
        'rationale': 'Đoạn văn liệt kê 5 lĩnh vực then chốt để xây dựng khuyến nghị của WHO nhằm cải thiện phát triển trẻ thơ: 1. chăm sóc đáp ứng; 2. học tập sớm; 3. lồng ghép can thiệp; 4. sức khỏe tinh thần bà mẹ; 5. hỗ trợ người chăm sóc.',
        'anchor': 'five areas for development of recommendations to improve ECD outcomes:',
    },
    {
        'code': '1984C117D6',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu phần bằng chứng và các khuyến nghị cốt lõi của WHO về can thiệp phát triển trẻ thơ.',
        'anchor': 'Evidence and recommendations',
    },
    {
        'code': '361CC4B3C8',
        'grade': 1,
        'rationale': 'Danh sách các câu hỏi lâm sàng then chốt theo định dạng PICO định hướng cho các khuyến nghị của WHO về phát triển trẻ thơ.',
        'anchor': 'Key questions',
    },
    {
        'code': 'D1FE538624',
        'grade': 0,
        'rationale': 'Bảng danh mục các chữ viết tắt trong hướng dẫn của WHO, không chứa nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': '6C114887B7',
        'grade': 0,
        'rationale': 'Đoạn mở đầu phân tích tổng hợp can thiệp tự kỷ sớm (Project AIM), không chứa khuyến nghị của WHO.',
        'anchor': '',
    },
    {
        'code': 'E885B1B867',
        'grade': 0,
        'rationale': 'Danh sách các khoảng trống nghiên cứu cần ưu tiên trong tương lai, không phải khuyến nghị thực hành của WHO.',
        'anchor': '',
    },
    {
        'code': 'DE34817F15',
        'grade': 0,
        'rationale': 'Mô tả cấu trúc PICO trong việc xây dựng câu hỏi hướng dẫn, không chứa nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': '83348B1289',
        'grade': 0,
        'rationale': 'Danh sách tên và địa chỉ cơ quan của các chuyên gia tham gia nhóm soạn thảo hướng dẫn WHO, không có nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': '3EF7AA5FA3',
        'grade': 1,
        'rationale': 'Danh mục các báo cáo tổng quan hệ thống nền tảng phục vụ xây dựng hướng dẫn can thiệp chăm sóc của WHO.',
        'anchor': 'Caregiving interventions to support early child development in the first three years of life',
    },
    {
        'code': '562D186B27',
        'grade': 1,
        'rationale': 'Đoạn hướng dẫn về việc thích ứng và triển khai các khuyến nghị của WHO tại cấp quốc gia và địa phương.',
        'anchor': 'likely to be affected by the recommendations will be specifically reviewed',
    },
    {
        'code': '1C8375B813',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ mục đích của tài liệu hướng dẫn WHO là cung cấp các khuyến nghị toàn cầu dựa trên bằng chứng nhằm cải thiện phát triển trẻ thơ.',
        'anchor': 'This guideline provides global, evidence-informed recommendations on improving ECD.',
    },
    {
        'code': 'D4EC3BF01D',
        'grade': 3,
        'rationale': 'Cơ sở lý giải cho Khuyến nghị 1 của WHO: bằng chứng khẳng định tính hiệu quả của các can thiệp hỗ trợ chăm sóc đáp ứng trong 3 năm đầu đời của trẻ.',
        'anchor': 'The recommendation reflects the evidence demonstrating the efficacy of int',
    },
    {
        'code': 'AE7A946933',
        'grade': 1,
        'rationale': 'Phụ lục tổng hợp các hướng dẫn liên quan khác của WHO cho quần thể trẻ em nguy cơ cao tại các nước có thu nhập thấp và trung bình.',
        'anchor': 'This guideline contains recommendations for a specific high-risk population',
    },
    {
        'code': '5589C37261',
        'grade': 1,
        'rationale': 'Phụ lục liệt kê các công cụ và hướng dẫn có sẵn của WHO về chăm sóc sức khỏe và dinh dưỡng bà mẹ, trẻ em.',
        'anchor': 'WHO recommendations for improving infant and child health are included in',
    },
    {
        'code': '17EDB88FFE',
        'grade': 2,
        'rationale': 'Tóm tắt các cân nhắc của Nhóm Xây dựng Hướng dẫn (GDG) của WHO về hướng đi và độ mạnh của khuyến nghị hỗ trợ sức khỏe tinh thần bà mẹ.',
        'anchor': 'Summary of the considerations of the members of the GDG for determining the direction and strength',
    },
    {
        'code': '41BF54556C',
        'grade': 1,
        'rationale': 'Phụ lục danh mục các khuyến nghị của WHO về chăm sóc trẻ sơ sinh và trẻ nhỏ.',
        'anchor': 'WHO recommendations for improving infant and child health are included in',
    },
    {
        'code': '714C3F1BFF',
        'grade': 2,
        'rationale': 'Mô tả đối tượng đích của hướng dẫn WHO: trực tiếp ảnh hưởng đến tất cả cha mẹ, người chăm sóc chính và cán bộ y tế cơ sở.',
        'anchor': 'This guideline directly affects all parents and primary caregivers',
    },
    {
        'code': 'FEF56568A5',
        'grade': 1,
        'rationale': 'Cấu trúc trình bày các khuyến nghị và tổng hợp bằng chứng từ các tổng quan hệ thống của WHO.',
        'anchor': 'The discussion points around each of the key questions are presented',
    },
    {
        'code': 'BE9B0C2F91',
        'grade': 2,
        'rationale': 'Đoạn văn nêu phạm vi hướng dẫn: giải quyết khoảng trống chính sách khi trước đây chưa có khuyến nghị cụ thể của WHO dành riêng cho can thiệp phát triển trẻ thơ (ECD).',
        'anchor': 'there are presently no WHO recommendations focussed on ECD-specific interventions',
    },
    {
        'code': 'D0E0652381',
        'grade': 2,
        'rationale': 'Tài liệu hướng dẫn "Chăm sóc vì sự phát triển trẻ em" của WHO khuyến nghị các hoạt động chơi đùa và giao tiếp để gia đình kích thích học tập sớm ở trẻ.',
        'anchor': '“Care for child development” recommends play and communication activities for families to stimulate',
    },
    {
        'code': '9720A33285',
        'grade': 0,
        'rationale': 'Kế hoạch cập nhật định kỳ hướng dẫn của WHO khi có bằng chứng mới, không chứa nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': 'D8486E48B2',
        'grade': 2,
        'rationale': 'Tài liệu của WHO khuyến nghị điều dưỡng làm việc phối hợp với gia đình, hướng dẫn người chăm sóc nhận biết và đáp ứng nhạy cảm với các tín hiệu của trẻ.',
        'anchor': 'This publication recommends that nurses work in partnership with families, teach caregi',
    },
    {
        'code': '64D6F22795',
        'grade': 0,
        'rationale': 'Danh sách thành viên ban soạn thảo Hướng dẫn WHO, không có nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': '03FC082C1C',
        'grade': 3,
        'rationale': 'Đoạn văn trích xuất nguyên văn khuyến nghị cốt lõi của WHO: mọi trẻ nhũ nhi và trẻ nhỏ cần nhận được chăm sóc đáp ứng trong 3 năm đầu đời; cha mẹ và người chăm sóc cần được hỗ trợ để cung cấp chăm sóc đáp ứng và học tập sớm.',
        'anchor': 'In order to improve early childhood development, WHO recommends: All infants and children should receive responsive care',
    },
    {
        'code': '1D823B0DC1',
        'grade': 2,
        'rationale': 'Phần bối cảnh khẳng định tài liệu cung cấp các khuyến nghị toàn cầu dựa trên bằng chứng về các phương pháp tiếp cận cải thiện phát triển trẻ thơ.',
        'anchor': 'provides global, evidenceinformed recommendations on approaches to improve ECD',
    },
    {
        'code': '399C8682E3',
        'grade': 0,
        'rationale': 'Bảng hồ sơ bằng chứng GRADE đánh giá chất lượng chứng cứ lâm sàng, không có nội dung khuyến nghị.',
        'anchor': '',
    },
    {
        'code': '41B41C1F77',
        'grade': 1,
        'rationale': 'Hướng dẫn của WHO về thời gian, số lần và địa điểm tiếp xúc sau sinh tại các môi trường nghèo tài nguyên.',
        'anchor': 'Recommendations address timing, number and place of postnatal contacts',
    },
    {
        'code': '658D04AABA',
        'grade': 1,
        'rationale': 'Tổng quan toàn cầu về hiệu quả của các can thiệp nuôi dạy con trong giai đoạn thơ ấu nhằm hỗ trợ mục tiêu phát triển trẻ thơ của Liên Hợp Quốc.',
        'anchor': 'provide a comprehensive global review of the effectiveness of parenting interventions',
    },
    {
        'code': '295BC64679',
        'grade': 3,
        'rationale': 'Khuyến nghị 3 của WHO: hỗ trợ chăm sóc đáp ứng và học tập sớm cần được lồng ghép vào các can thiệp nhằm cải thiện phát triển trẻ thơ.',
        'anchor': 'Feasibility The group concluded that it was probably feasible to implement the interventions.',
    },
    {
        'code': 'D39D6156DF',
        'grade': 1,
        'rationale': 'Đoạn thảo luận phân tích sự cần thiết của việc xây dựng các gói can thiệp kết hợp nuôi dạy con theo khuyến nghị y văn.',
        'anchor': 'intervention packages is recommended in the literature',
    },
    {
        'code': '1BCE9C1A5F',
        'grade': 3,
        'rationale': 'Khuyến nghị 2 của WHO: cơ sở khoa học khẳng định hiệu quả của các can thiệp hỗ trợ cơ hội học tập sớm cho trẻ trong 3 năm đầu đời.',
        'anchor': 'The recommendation reflects the evidence which demonstrates the efficacy o',
    },
    {
        'code': 'ADBF2CCDE9',
        'grade': 0,
        'rationale': 'Bảng hồ sơ bằng chứng GRADE đánh giá can thiệp phát triển nhận thức, không chứa văn bản khuyến nghị.',
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

