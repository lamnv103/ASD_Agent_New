import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_16'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q042.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q042':
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
        'code': 'B753B846F9',
        'grade': 3,
        'rationale': 'Đoạn văn phân biệt trực tiếp giữa ASI và các can thiệp dựa trên cảm giác (SBIs): SBIs thường mang tính thụ động do người lớn áp đặt kích thích cảm giác, trái ngược với các nguyên tắc cốt lõi của ASI.',
        'anchor': 'Sensory‐based interventions stand in contrast to ASI in that their application often contradicts many of the core principles of ASI.',
    },
    {
        'code': '5341412B51',
        'grade': 0,
        'rationale': 'Danh mục tài liệu hỗ trợ bổ sung, không có nội dung phân tích so sánh ASI và các can thiệp khác.',
        'anchor': '',
    },
    {
        'code': '6C82E2DDD8',
        'grade': 2,
        'rationale': 'Đoạn thảo luận nhấn mạnh sự cần thiết phải phân biệt rõ ràng và loại trừ các nghiên cứu can thiệp cảm giác không tuân thủ nguyên tắc ASI khỏi các tổng quan bằng chứng.',
        'anchor': 'studies such as these should be excluded from evidence‐based reviews of ASI',
    },
    {
        'code': 'B303A2D698',
        'grade': 0,
        'rationale': 'Bảng tiêu chí đánh giá chất lượng CEC đối với các nghiên cứu được tổng quan, không có văn bản giải thích sự khác biệt.',
        'anchor': '',
    },
    {
        'code': '273AD0AE2B',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về tính kén ăn và các bệnh lý tiêu hóa ở trẻ tự kỷ, không phân biệt ASI với các can thiệp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'ABCA692D0A',
        'grade': 1,
        'rationale': 'Đoạn mô tả thiết kế thử nghiệm SenITA sử dụng liệu pháp Điều hòa Cảm giác Ayres (ASI) cho trẻ tự kỷ.',
        'anchor': 'The intervention comprised Ayres Sensory Integration ® therapy delivered',
    },
    {
        'code': '8E0ECAE98E',
        'grade': 2,
        'rationale': 'Đoạn thảo luận giải thích lý do kết quả tổng quan này khác biệt so với các tổng quan trước đó là do các nghiên cứu trước đã gộp chung các can thiệp cảm giác không phải ASI.',
        'anchor': 'The findings from this review diverge from those of earlier reviews',
    },
    {
        'code': 'B638B4E6D5',
        'grade': 0,
        'rationale': 'Mô tả quy trình sàng lọc cơ sở dữ liệu ở giai đoạn 1, không có nội dung so sánh ASI và các can thiệp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'DD0E1D7D75',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu về liệu pháp điều hòa cảm giác do Jean Ayres sáng lập và khuyến nghị nghiên cứu của NICE.',
        'anchor': 'The primary goal of OT intervention is to enable participation in activities of everyday life',
    },
    {
        'code': 'F916609B2D',
        'grade': 1,
        'rationale': 'Mô tả nghiên cứu của Iwanaga et al. so sánh kết quả của trẻ tự kỷ nhận can thiệp ASI trong 9 tháng với các phương pháp khác.',
        'anchor': 'Iwanaga et al. [2014] is a nonrandomized study that compares outcomes data from children with ASD who received 9 months ASI intervention',
    },
    {
        'code': '3CC6275DDE',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ tiêu chí sàng lọc giai đoạn hai nhằm xác định các nghiên cứu tuân thủ nghiêm ngặt nguyên lý can thiệp của Ayres Sensory Integration (ASI).',
        'anchor': 'In Stage Two, the 19 studies were further examined to determine if they met the following criteria',
    },
    {
        'code': 'F755605EF7',
        'grade': 2,
        'rationale': 'Phần kết luận tổng quan khẳng định can thiệp ASI đáp ứng tiêu chuẩn thực hành dựa trên bằng chứng cho trẻ tự kỷ từ 4–12 tuổi khi áp dụng đúng nguyên lý.',
        'anchor': 'Ayres Sensory Integration intervention is frequently requested by parents and is often utilized by occupational therapists',
    },
    {
        'code': 'B5E06C9C99',
        'grade': 0,
        'rationale': 'Mục lục các tệp hỗ trợ trực tuyến, không có nội dung phân biệt ASI.',
        'anchor': '',
    },
    {
        'code': '34E03728B1',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về sự không đồng nhất của các biến số kết quả đo lường trong các nghiên cứu đánh giá can thiệp ASI.',
        'anchor': 'outcomes measured in existing studies vary widely and may not be sensitive to the changes expected following ASI intervention',
    },
    {
        'code': 'DF8A2F72E8',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu về vị trí của liệu pháp hoạt động sử dụng nguyên lý ASI trong giáo dục đặc biệt cho trẻ tự kỷ.',
        'anchor': 'Occupational therapy using the principles of Ayres Sensory Integration® (ASI) intervention is among the most req',
    },
    {
        'code': '8339FB9707',
        'grade': 1,
        'rationale': 'Đoạn phân tích các yếu tố gây nhiễu trong các tổng quan trước đây về ASI, cụ thể là việc thiếu mô tả đặc điểm kiểu hình cảm giác của người tham gia.',
        'anchor': 'confounding interpretation of the evidence on ASI intervention is that past reviews and meta‐analyses include studies that failed to provide an adequate description',
    },
    {
        'code': '92660C11F2',
        'grade': 0,
        'rationale': 'Bảng chú giải viết tắt trong tài liệu tổng quan, không có nội dung phân tích so sánh.',
        'anchor': '',
    },
    {
        'code': '9343C68FAA',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu bị loại trừ khỏi phân tích chất lượng CEC, không phân tích sự khác biệt của ASI.',
        'anchor': '',
    },
    {
        'code': '085651F03E',
        'grade': 0,
        'rationale': 'Tuyên bố tuân thủ chuẩn mực đạo đức nghiên cứu và xung đột lợi ích, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '84B8D028AA',
        'grade': 2,
        'rationale': 'Đoạn thảo luận khẳng định ASI là thực hành dựa trên bằng chứng khi đảm bảo tính chuẩn mực về đo lường độ trung thực (fidelity measure).',
        'anchor': 'Our study indicates that ASI intervention meets criteria for an evidence‐based practice',
    },
    {
        'code': '176141A06F',
        'grade': 0,
        'rationale': 'Bảng đánh giá các tiêu chí chỉ báo chất lượng CEC, không chứa văn bản so sánh phương pháp.',
        'anchor': '',
    },
    {
        'code': '3145B16616',
        'grade': 2,
        'rationale': 'Tóm tắt bài viết chỉ ra sự thiếu rõ ràng trong y văn giữa điều hòa cảm giác Ayres (ASI) và các can thiệp cảm giác khác, và đặt ra mục tiêu làm rõ.',
        'anchor': 'Sensory integration is one of the most highly utilized interventions in autism',
    },
    {
        'code': 'E344862663',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa về tích hợp đa cảm giác và cách não bộ diễn giải các luồng thông tin cảm giác đầu vào.',
        'anchor': 'Multisensory integration is defined as the study of how the brain integrates and interprets input fr',
    },
    {
        'code': '6AEB9CDF25',
        'grade': 0,
        'rationale': 'Mô tả chi tiết chiến lược tìm kiếm tài liệu trên cơ sở dữ liệu, không có nội dung so sánh.',
        'anchor': '',
    },
    {
        'code': '031CD1F188',
        'grade': 0,
        'rationale': 'Bảng ma trận đánh giá chất lượng chỉ báo CEC, không có nội dung so sánh.',
        'anchor': '',
    },
    {
        'code': '1E1455F43A',
        'grade': 0,
        'rationale': 'Mô tả tiêu chí loại trừ giai đoạn 1 của quy trình tổng quan hệ thống, không so sánh ASI.',
        'anchor': '',
    },
    {
        'code': '2BDD94BC08',
        'grade': 2,
        'rationale': 'Đoạn văn tóm lược nguồn gốc lý thuyết của Jean Ayres về rối loạn chức năng điều hòa cảm giác là vấn đề tổ chức thông tin cảm giác để sử dụng.',
        'anchor': 'Ayres (1972, p. 4) described sensory integration dysfunction as a problem in the ability to “organize sensory information for use”',
    },
    {
        'code': 'CEBA798D0A',
        'grade': 2,
        'rationale': 'Đoạn văn phân biệt SIT/ASI (liệu pháp chuyên sâu tuân thủ chuẩn mực) với các can thiệp dựa trên cảm giác thông thường và chiến lược điều chỉnh môi trường.',
        'anchor': 'However, sensory-based interventions, as well as sensory strategies and environmental adaptations, are currently reported by many professionals',
    },
    {
        'code': '5818E33BAF',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu về tỷ lệ trẻ em gặp khó khăn về tích hợp và xử lý cảm giác trong các nhóm trẻ phát triển và tự kỷ.',
        'anchor': 'Sensory integration and processing (SI/SP) differences are estimated to affect 5%–25% of children',
    },
    {
        'code': '463BC15E4B',
        'grade': 3,
        'rationale': 'Đoạn văn giải thích trực tiếp: các can thiệp cảm giác khác thiếu các thành phần cốt lõi của ASI như cá nhân hóa can thiệp, sự tham gia chủ động của trẻ, thiết lập liên minh trị liệu, và đặt ra thử thách vừa sức trong bối cảnh chơi đùa.',
        'anchor': 'They lack many of the key ingredients of the ASI such as individual‐tailoring, active engagement of the child',
    },
    {
        'code': '42DA2AA3C6',
        'grade': 1,
        'rationale': 'Mô tả nghiên cứu thử nghiệm RCT của Pfeiffer et al. so sánh hai can thiệp hoạt động trị liệu (ASI so với can thiệp vận động tinh).',
        'anchor': 'Pfeiffer et al. [2011] is a randomized controlled trial comparing two occupational therapy intervent',
    },
    {
        'code': 'ED2A2CB334',
        'grade': 3,
        'rationale': 'Đoạn văn nêu rõ định nghĩa: để phân biệt liệu pháp điều hòa cảm giác (SIT) với các can thiệp dựa trên cảm giác khác, bộ nguyên tắc đo lường độ trung thực (fidelity principles) đã được phát triển và đăng ký nhãn hiệu là ASI.',
        'anchor': 'To distinguish SIT from other sensory-based interventions, a set of fidelity principles to guide delivery was developed and registered as ASI.',
    },
    {
        'code': '29059574FD',
        'grade': 1,
        'rationale': 'Mô tả thử nghiệm RCT của Schaaf et al. (2014) đánh giá hiệu quả can thiệp ASI đối với các mục tiêu cá nhân ở trẻ tự kỷ.',
        'anchor': 'Schaaf et al. [2014] is a randomized controlled trial of 32 children with ASD, 6–9 years old, who re',
    },
    {
        'code': '1D9FA51E84',
        'grade': 0,
        'rationale': 'Bảng thống kê phụ lục tài liệu bổ sung, không có nội dung phân tích so sánh.',
        'anchor': '',
    },
    {
        'code': '5B0BC275DE',
        'grade': 0,
        'rationale': 'Bảng đánh giá chỉ báo chất lượng CEC của các nghiên cứu can thiệp, không chứa văn bản so sánh.',
        'anchor': '',
    },
    {
        'code': 'D4B5E3C78B',
        'grade': 1,
        'rationale': 'Mô tả chiến lược tìm kiếm các nghiên cứu về tự kỷ và điều hòa cảm giác Ayres trên 7 cơ sở dữ liệu quốc tế.',
        'anchor': 'In Stage One, searches were conducted in CINAHL, Cochrane Reviews, Cochrane Trials, Embase, ERIC, Medline',
    },
    {
        'code': '3A0D46CD87',
        'grade': 0,
        'rationale': 'Bảng đánh giá tiêu chí CEC, không có nội dung văn bản so sánh ASI với can thiệp khác.',
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

