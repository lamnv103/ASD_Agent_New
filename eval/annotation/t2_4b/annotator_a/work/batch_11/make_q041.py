import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_11.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_11/q041.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q041':
            content_map[obj['annotation_code']] = obj['content']

def get_span(code, anchor, max_len=200):
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
        'code': '456CEF59D7',
        'grade': 3,
        'rationale': 'Kết quả thử nghiệm ngẫu nhiên có đối chứng SenITA RCT chỉ ra rằng liệu pháp điều hòa cảm giác (SIT) không mang lại hiệu quả có ý nghĩa thống kê về mặt lâm sàng trên kết quả chính sau 6 và 12 tháng.',
        'anchor': 'No evidence of meaningful intervention effects was found at 6 or 12 months across behavioural, adaptive functioning, socialisation, carer stress, health utility or quality-of-life measures.',
    },
    {
        'code': '9EA6087D07',
        'grade': 2,
        'rationale': 'Trích dẫn định tính từ phụ huynh ghi nhận sự cải thiện ở trẻ trong việc tham gia các hoạt động thể chất và tương tác sau khi can thiệp điều hòa cảm giác.',
        'anchor': 'he was able to participate in playground football, having done this intervention',
    },
    {
        'code': 'A40F9B59AE',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về rối loạn trầm cảm chủ yếu (MDD) và triệu chứng cơ thể, không đề cập đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '1FBB3E7DF8',
        'grade': 0,
        'rationale': 'Đoạn văn về tác dụng phụ của cây nữ lang (valerian) đối với tiêu hóa, không liên quan đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '33966408E2',
        'grade': 0,
        'rationale': 'Đoạn văn nêu câu hỏi nghiên cứu về can thiệp nuôi dưỡng trong 3 năm đầu đời, không đề cập đến liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'A83F128508',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về việc liệu pháp điều hòa cảm giác còn có quá ít nghiên cứu chất lượng cao để ước tính kích thước hiệu ứng tổng hợp trong phân tích tổng hợp.',
        'anchor': 'Categories of intervention approaches that were too sparsely represented',
    },
    {
        'code': 'EFD1E07EEF',
        'grade': 0,
        'rationale': 'Bảng từ khóa tìm kiếm cơ sở dữ liệu y khoa, không chứa thông tin đánh giá hiệu quả can thiệp.',
        'anchor': '',
    },
    {
        'code': '75423EF0A2',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả cách tính chỉ số Tau-U cho kết quả ngôn ngữ trong thiết kế ca đơn lẻ, không liên quan đến liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'A9FDD450EB',
        'grade': 1,
        'rationale': 'Đoạn văn báo cáo kích thước hiệu ứng trung bình (eta squared = 0.23) của một phân tích can thiệp, cung cấp bối cảnh thống kê.',
        'anchor': 'The average effect size that was calculated using eta squared is 0.23',
    },
    {
        'code': '9E485C1752',
        'grade': 3,
        'rationale': 'Đoạn văn phân tích rằng dù liệu pháp can thiệp cảm giác (SI/SP) được áp dụng rộng rãi, bằng chứng khoa học mạnh mẽ trong y văn vẫn còn hạn chế và cần được thẩm định khắt khe.',
        'anchor': 'Given the widespread delivery of SI/SP based assessment and treatment, one would expect an extensive strong evidence base in the literature.',
    },
    {
        'code': '45F7839FC3',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả nguồn gốc lý thuyết của liệu pháp điều hòa cảm giác Ayres (ASI) và việc phát triển các công cụ đánh giá chức năng xử lý cảm giác.',
        'anchor': 'Ayres (1972, p. 4) described sensory integration dysfunction as a problem in the ability to “organize sensory information for use”',
    },
    {
        'code': 'AF1038CB1B',
        'grade': 3,
        'rationale': 'Tổng quan hệ thống kết luận rằng liệu pháp can thiệp cảm giác (SI/SP-T) đang có bằng chứng mới nổi nhưng vẫn còn hạn chế về hiệu quả lâm sàng.',
        'anchor': 'SI/SP-T is a widely-used approach for treating individuals',
    },
    {
        'code': 'CB5811C117',
        'grade': 3,
        'rationale': 'Nghiên cứu kết luận liệu pháp điều hòa cảm giác Ayres (ASI) đáp ứng tiêu chuẩn là một thực hành dựa trên bằng chứng (evidence-based practice) cho trẻ tự kỷ 4-12 tuổi theo tiêu chuẩn CEC.',
        'anchor': 'Our study indicates that ASI intervention meets criteria for an evidence‐based practice',
    },
    {
        'code': '64F6438141',
        'grade': 2,
        'rationale': 'Bảng bằng chứng tổng hợp các nghiên cứu đánh giá hiệu quả của các can thiệp xử lý cảm giác ở trẻ em.',
        'anchor': '| Author/Year | Level of Evidence Study Design Risk of Bias | Participants Inclusion Criteria Study Setting | Intervention and Control Group',
    },
    {
        'code': '429FC5823A',
        'grade': 1,
        'rationale': 'Bảng lý do loại trừ các nghiên cứu khỏi phân tích tiêu chuẩn CEC (ví dụ không đúng chuẩn can thiệp ASI), cung cấp bối cảnh phương pháp luận.',
        'anchor': 'Studies Excluded from CEC Analysis',
    },
    {
        'code': '0B5232322A',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các can thiệp đào tạo từ xa cho phụ huynh, không liên quan đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '1C0C453F38',
        'grade': 2,
        'rationale': 'Đoạn văn ghi nhận phản hồi tích cực và mức độ hài lòng cao từ người chăm sóc đối với liệu pháp điều hòa cảm giác giúp cải thiện hành vi của trẻ.',
        'anchor': 'All carers would‘definitely’ recommend the intervention to others because it had helped their child',
    },
    {
        'code': '06EA013F07',
        'grade': 1,
        'rationale': 'Đoạn văn tổng quan về các phương pháp can thiệp cho trẻ tự kỷ, có nhắc đến việc giải quyết các vấn đề giác quan.',
        'anchor': 'treatment in autistic children and teenagers typically involves behavioral interventions',
    },
    {
        'code': '29AB7C4B74',
        'grade': 2,
        'rationale': 'Đoạn văn phân biệt sự khác nhau giữa can thiệp dựa trên cảm giác (SBIs) và điều hòa cảm giác Ayres (ASI) về mặt nguyên lý thực hành và bằng chứng.',
        'anchor': 'Sensory‐based interventions stand in contrast to ASI in that their application often contradicts many of the core principles of ASI.',
    },
    {
        'code': '52BCEEA35B',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu các can thiệp hành vi phát triển tự nhiên (NDBI), không nói về liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '4BFE93E5AB',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả cách mã hóa cường độ và phương thức triển khai của các can thiệp trong tổng quan.',
        'anchor': 'Interventions were coded for type, setting, implementer, and cumulative intensity',
    },
    {
        'code': '254B978972',
        'grade': 0,
        'rationale': 'Bảng định nghĩa các chỉ số đo lường hiệu ứng PND và IRD, không chứa số liệu liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'DB2202FC32',
        'grade': 3,
        'rationale': 'Tổng quan ghi nhận 4 nghiên cứu cho thấy sự cải thiện về mức độ căng thẳng của phụ huynh và hành vi của trẻ, nhưng nhấn mạnh sự thiếu hụt bằng chứng về tính chuẩn mực (fidelity) của liệu pháp.',
        'anchor': 'The review included four studies that demonstrated improvements in parental stress or child performance/behaviors',
    },
    {
        'code': '21D5E6AA5B',
        'grade': 0,
        'rationale': 'Đoạn văn tổng quan về các can thiệp hành vi và giáo dục nói chung trong tự kỷ, không phân tích liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '16B43ECEAF',
        'grade': 2,
        'rationale': 'Đoạn giới thiệu bối cảnh thử nghiệm SenITA RCT về liệu pháp điều hòa cảm giác cho trẻ tự kỷ có khó khăn xử lý cảm giác tại Vương quốc Anh.',
        'anchor': 'Background Approximately 1–2% of children have a diagnosis of autism in the UK',
    },
    {
        'code': 'D26A9AD66E',
        'grade': 2,
        'rationale': 'Đoạn văn phân tích một thử nghiệm ngẫu nhiên có đối chứng về can thiệp ASI ở trẻ tự kỷ và đánh giá sự tuân thủ các nguyên tắc can thiệp.',
        'anchor': 'this was a randomized controlled trial of children with autism who received intervention consistent with the principles of ASI',
    },
    {
        'code': '7F5393DFAC',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả ước tính hiệu quả cho can thiệp hành vi, NDBI và công nghệ, không nhắc đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': 'DC52364D2A',
        'grade': 0,
        'rationale': 'Đoạn văn về liệu pháp xoa bóp và chăn trọng lượng cho giấc ngủ ở trẻ tự kỷ, không phân tích liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': 'D222876257',
        'grade': 3,
        'rationale': 'Kết luận của thử nghiệm SenITA nêu rõ liệu pháp điều hòa cảm giác không đem lại hiệu quả lâm sàng rõ rệt trên các thang đo hành vi và không đạt hiệu quả chi phí.',
        'anchor': 'Health economic evaluation suggests that sensory integration therapy is not cost-effective compared with usual care alone.',
    },
    {
        'code': 'B0E860C11D',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả phương pháp tổng hợp bằng chứng của WHO, không liên quan đến liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': '440B3429A0',
        'grade': 2,
        'rationale': 'Bảng bằng chứng tổng hợp các nghiên cứu về can thiệp cảm giác ở trẻ em và đánh giá nguy cơ sai lệch.',
        'anchor': '| Author/Year | Level of Evidence Study Design Risk of Bias | Participants Inclusion Criteria Study Setting | Intervention and Control Group',
    },
    {
        'code': '19B2B70BF8',
        'grade': 1,
        'rationale': 'Bảng đặc điểm nghiên cứu tổng quan về các can thiệp hỗ trợ trẻ tự kỷ.',
        'anchor': 'Study characteristics.',
    },
    {
        'code': 'F7442C2785',
        'grade': 2,
        'rationale': 'Bảng bằng chứng lâm sàng về các can thiệp xử lý cảm giác cho trẻ em.',
        'anchor': '| Author/Year | Level of Evidence Study Design Risk of Bias | Participants Inclusion Criteria Study Setting | Intervention and Control Group',
    },
    {
        'code': 'F8A25DF916',
        'grade': 2,
        'rationale': 'Hướng dẫn của viện NICE khuyến nghị cần thêm nghiên cứu để xác định xem liệu pháp điều hòa cảm giác (SIT) có thực sự cải thiện các khó khăn cảm giác và hành vi hay không.',
        'anchor': 'The NICE Guideline Development Group recommended further research to establish whether or not sensory integration therapy (SIT) improves',
    },
    {
        'code': '603A140B66',
        'grade': 3,
        'rationale': 'Đoạn văn tổng quan về lịch sử 50 năm của khung lý thuyết Điều hòa Cảm giác và các tranh luận khoa học về hiệu quả lâm sàng của liệu pháp này.',
        'anchor': 'For more than 50 years, “Sensory Integration” has been a theoretical framework',
    },
    {
        'code': '7CC36757BC',
        'grade': 1,
        'rationale': 'Đoạn văn thống kê tỷ lệ các phương pháp can thiệp khác nhau được đưa vào nghiên cứu tổng quan.',
        'anchor': 'Other approaches included neurodevelopmental ( n = 47, 59.5%), applied behavioural analysis',
    },
    {
        'code': 'AF02CF0B5F',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả biểu đồ PRISMA chi tiết quá trình tìm kiếm tài liệu, không chứa kết quả can thiệp.',
        'anchor': '',
    },
    {
        'code': '5B9D71E2E3',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả các thang đo kết quả và đánh giá hiệu quả chi phí trong thử nghiệm liệu pháp điều hòa cảm giác SenITA.',
        'anchor': 'cost-effectiveness (assessed using the Client Service Receipt Inventory).',
    },
    {
        'code': '97800C5110',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu phương pháp phân tích chủ đề định tính từ lời kể của phụ huynh và nhà trị liệu tham gia can thiệp SIT.',
        'anchor': 'Each theme is discussed below and is supported by participant quotes.',
    },
    {
        'code': 'E29A56872D',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về các can thiệp dựa trên cảm giác (SBIs) và các tranh luận về tính hiệu quả của chúng trong hoạt động trị liệu.',
        'anchor': 'SBIs may be implemented by caregivers and other team members or accessed independently by the child as part of an occupational therapy intervention plan',
    },
    {
        'code': 'E37A2A8519',
        'grade': 1,
        'rationale': 'Bảng giả thuyết về các tác động xã hội và hành vi của rối loạn xử lý cảm giác.',
        'anchor': 'Hypothesized social and behavioral effects of sensory disruptions.',
    },
    {
        'code': 'D5EB4B46D7',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về việc liệu pháp SIT có duy trì được hiệu quả điều trị lâu dài sau khi kết thúc can thiệp hay không.',
        'anchor': 'Post-intervention treatment effects may be less specific, and we do not yet know whether or not SIT demonstrates sustained effects.',
    },
    {
        'code': '8499531867',
        'grade': 0,
        'rationale': 'Đoạn văn tổng quan về 30 thử nghiệm RCT can thiệp do cha mẹ làm trung gian (PMI), không liên quan đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '06988B1093',
        'grade': 1,
        'rationale': 'Đoạn văn bàn về các tiêu chuẩn đánh giá hiệu quả điều trị trong y học và tâm lý học hành vi.',
        'anchor': 'There have long been universal protocols for evaluating treatment efficacy and effectiveness in medicine and in behavioral interventions',
    },
    {
        'code': 'C763E8BF48',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả phương pháp thống kê quy đổi số liệu trong phân tích tổng hợp, không có thông tin liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': '6701FA5921',
        'grade': 0,
        'rationale': 'Đoạn văn bàn về hạn chế đo lường kết quả sức khỏe thể chất trong nghiên cứu trẻ em.',
        'anchor': '',
    },
    {
        'code': '17717A1959',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả thủ tục mã hóa nghiên cứu NDBI, không liên quan đến liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': 'D5166C8FFB',
        'grade': 0,
        'rationale': 'Đoạn văn trích kết quả theo dõi chức năng thích ứng sau 6 tháng trong một nghiên cứu, không liên quan đến liệu pháp cảm giác.',
        'anchor': '',
    },
    {
        'code': '1C101C8B80',
        'grade': 1,
        'rationale': 'Mô tả hình ảnh kích thước hiệu ứng từ các thử nghiệm ngẫu nhiên có đối chứng của các nhóm can thiệp tự kỷ.',
        'anchor': 'Figure 3 reflects summary effect sizes derived from outcomes extracted only from randomized controlled trials',
    },
    {
        'code': '77C0ADF29D',
        'grade': 0,
        'rationale': 'Mô tả tỷ lệ phần trăm nguy cơ sai lệch trong các nghiên cứu tổng quan, không chứa kết quả can thiệp.',
        'anchor': '',
    },
    {
        'code': 'CA29BBEA5B',
        'grade': 0,
        'rationale': 'Đoạn văn về các bài thuốc thảo dược cho rối loạn giấc ngủ, không liên quan đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '0FBE8E6C0E',
        'grade': 2,
        'rationale': 'Bảng bằng chứng tổng hợp các nghiên cứu về can thiệp cảm giác ở trẻ em và đánh giá nguy cơ sai lệch.',
        'anchor': '| Author/Year | Level of Evidence Study Design Risk of Bias | Participants Inclusion Criteria Study Setting | Intervention and Control Group',
    },
    {
        'code': 'A71A93ED34',
        'grade': 1,
        'rationale': 'Bảng thuật ngữ tìm kiếm liên quan đến rối loạn cảm giác và liệu pháp điều hòa cảm giác trong tổng quan y văn.',
        'anchor': 'Search terms.',
    },
    {
        'code': 'AD4C3BE1B4',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các tổng quan can thiệp giao tiếp và hành vi, không nhắc đến liệu pháp điều hòa cảm giác.',
        'anchor': '',
    },
    {
        'code': '2A6925193B',
        'grade': 2,
        'rationale': 'Bảng bằng chứng tổng hợp các nghiên cứu đánh giá hiệu quả của các can thiệp xử lý cảm giác ở trẻ em.',
        'anchor': '| Author/Year | Level of Evidence Study Design Risk of Bias | Participants Inclusion Criteria Study Setting | Intervention and Control Group',
    }
]

annotations = []
errors = []

for r in raw:
    code = r['code']
    grade = r['grade']
    rat = r['rationale']
    anchor = r['anchor']
    
    if grade == 0:
        span = ''
    else:
        try:
            span = get_span(code, anchor)
        except Exception as e:
            errors.append(str(e))
            span = ''
            
    ann = {
        'annotation_code': code,
        'grade': grade,
        'rationale': rat,
        'evidence_span': span,
        'confidence': 'high',
        'needs_review': False,
        'review_note': '',
        'annotation_type': 'ai_generated',
        'model': 'claude-sonnet-4-6',
        'prompt_version': 't2_4b_ai_v1'
    }
    annotations.append(ann)

print(f'Extraction errors: {len(errors)}')
for e in errors:
    print(e)

# Verify
verify_errors = []
for ann in annotations:
    code = ann['annotation_code']
    span = ann['evidence_span']
    grade = ann['grade']
    if grade != 0 and grade is not None:
        if not span:
            verify_errors.append(f'{code}: missing span')
        elif span not in content_map.get(code, ''):
            verify_errors.append(f'{code}: span not in content')

print(f'Verification errors: {len(verify_errors)}')
for e in verify_errors:
    print(e)

if not errors and not verify_errors:
    with open(returned_path, 'w', encoding='utf-8') as f:
        for ann in annotations:
            f.write(json.dumps(ann, ensure_ascii=False) + '\n')
    print(f'Successfully wrote {len(annotations)} annotations to {returned_path}')
