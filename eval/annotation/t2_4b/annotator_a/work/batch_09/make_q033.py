import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_09.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_09/q033.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q033':
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
        'code': '811A8CA5CF',
        'grade': 1,
        'rationale': 'Bảng thống kê các can thiệp của cha mẹ nhằm thúc đẩy phát triển trẻ sớm trong 3 năm đầu đời, cung cấp bối cảnh về các nghiên cứu can thiệp.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': 'A67429EC89',
        'grade': 2,
        'rationale': 'Bảng đặc điểm các nghiên cứu can thiệp do cha mẹ thực hiện, tổng hợp các kết quả cải thiện kỹ năng giao tiếp và tương tác xã hội của trẻ tự kỷ.',
        'anchor': 'Study characteristics.',
    },
    {
        'code': 'B92B0B151B',
        'grade': 2,
        'rationale': 'Bảng tổng hợp 54 nghiên cứu với 51 kích thước hiệu ứng về can thiệp do cha mẹ thực hiện (PII) ở trẻ tự kỷ, cung cấp bằng chứng định lượng về hiệu quả.',
        'anchor': 'Overview of 54 studies yielding 51 independent effect sizes',
    },
    {
        'code': '1E8EE404DE',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các tổng quan hệ thống trước đó về can thiệp qua cha mẹ cho trẻ tự kỷ, ghi nhận các bằng chứng về tính hiệu quả.',
        'anchor': 'Summaries of included reviews',
    },
    {
        'code': '5641153CE4',
        'grade': 1,
        'rationale': 'Bảng nghiên cứu về các chương trình can thiệp nuôi dạy con nhằm cải thiện các khía cạnh phát triển ở trẻ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '2FF660C38E',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về sự phát triển của can thiệp do cha mẹ thực hiện (PMI) cho trẻ nhỏ tự kỷ và những kết quả tích cực được ghi nhận ở trẻ và cha mẹ.',
        'anchor': 'PMI has been actively pursued as a means of providing interventions to young children with autism',
    },
    {
        'code': '22E21579AA',
        'grade': 1,
        'rationale': 'Đoạn văn nêu câu hỏi nghiên cứu về hiệu quả của các can thiệp chăm sóc nuôi dưỡng đối với sự phát triển cảm xúc xã hội ở trẻ dưới 3 tuổi.',
        'anchor': 'What is the effectiveness of caregiving interventions to support socioemotional and behavioural development',
    },
    {
        'code': 'FF0F006202',
        'grade': 2,
        'rationale': 'Đoạn văn cung cấp bằng chứng cho thấy tập huấn can thiệp do cha mẹ thực hiện cho các gia đình ở nông thôn giúp cải thiện hành vi xã hội và kỹ năng giao tiếp của trẻ tự kỷ.',
        'anchor': 'Findings of this systematic review provide preliminary evidence that parent-mediated intervention training for families living in nonurban areas can assist in improving social behavior and communication skills of children with ASD.',
    },
    {
        'code': 'A657A1AF6E',
        'grade': 2,
        'rationale': 'Đoạn văn tổng quan về các can thiệp hành vi và giáo dục trong tự kỷ, ghi nhận can thiệp do cha mẹ thực hiện là phương pháp tiếp cận phổ biến và có bằng chứng hỗ trợ.',
        'anchor': 'We conducted a comprehensive review of behavioral and educational interventions for individuals with autism spectrum disorder (ASD).',
    },
    {
        'code': '1B935BFED0',
        'grade': 1,
        'rationale': 'Đoạn văn giải thích các giới hạn dữ liệu về sức khỏe thể chất của trẻ trong các nghiên cứu can thiệp của cha mẹ.',
        'anchor': 'Child health outcomes were not commonly or consistently measured across studies;',
    },
    {
        'code': 'D719DF46C9',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về hiệu quả của các nhóm tập huấn kỹ năng xã hội cho thanh thiếu niên tự kỷ, liên quan gián tiếp đến vai trò hỗ trợ của phụ huynh.',
        'anchor': 'This study adds to the still limited evidence for the efficacy of the culturally adapted SSTs for adolescents on the autism spectrum.',
    },
    {
        'code': '581C637FE3',
        'grade': 3,
        'rationale': 'Phân tích tổng hợp khẳng định trẻ tự kỷ được hưởng lợi rõ rệt từ các can thiệp do cha mẹ thực hiện (PII), cung cấp bằng chứng trực tiếp và toàn diện trả lời câu hỏi.',
        'anchor': 'Children with autism spectrum disorder (ASD) have been shown to benefit from parent-implemented interventions (PIIs).',
    },
    {
        'code': 'C84AD7CED2',
        'grade': 0,
        'rationale': 'Đoạn văn là hướng dẫn làm bài kiểm tra trong tài liệu tập huấn CST, không chứa thông tin đánh giá hiệu quả can thiệp.',
        'anchor': '',
    },
    {
        'code': '2D9270C877',
        'grade': 0,
        'rationale': 'Bảng đánh giá các tiêu chí chỉ số chất lượng CEC cho các nghiên cứu được tổng quan, không có số liệu hiệu quả.',
        'anchor': '',
    },
    {
        'code': 'DB39A459B9',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về can thiệp dựa trên cảm giác (SBIs) có thể do người chăm sóc thực hiện, liên quan gián tiếp đến câu hỏi.',
        'anchor': 'SBIs may be implemented by caregivers and other team members or accessed independently by the child',
    },
    {
        'code': 'EAB57146D9',
        'grade': 0,
        'rationale': 'Đoạn văn giải thích đáp án trắc nghiệm bài tập tình huống trong chương trình tập huấn CST, không đánh giá hiệu quả can thiệp.',
        'anchor': '',
    },
    {
        'code': '910C30E758',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu các triệu chứng cốt lõi của ASD và sự cần thiết của các can thiệp hành vi nhằm cải thiện chất lượng cuộc sống.',
        'anchor': 'Autisms Spectrum Disorders (ASD) are characterized by core symptoms',
    },
    {
        'code': 'EC98F04AAF',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp bằng chứng định lượng phân tích tổng hợp chứng minh can thiệp do cha mẹ thực hiện có hiệu quả tích cực gộp trên nhiều lĩnh vực ở trẻ tự kỷ.',
        'anchor': 'Across all 51 effect sizes, the random effects weighted average was',
    },
    {
        'code': 'C5A8353918',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả nội dung các buổi tập huấn kỹ năng người chăm sóc (CST) của WHO, liên quan đến cấu trúc can thiệp.',
        'anchor': 'Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging behaviours.',
    },
    {
        'code': '9BD6D901C8',
        'grade': 1,
        'rationale': 'Đoạn văn giải thích phương pháp tính toán kích thước hiệu ứng (Tau-U) cho các kết quả ngôn ngữ trong các nghiên cứu ca đơn lẻ.',
        'anchor': 'Effect sizes were calculated for every language outcome measure in each included study.',
    },
    {
        'code': 'EB7CCEBF3E',
        'grade': 3,
        'rationale': 'Phân tích tổng hợp từ 8 nghiên cứu báo cáo tác động của can thiệp do cha mẹ thực hiện (PMI) lên chức năng thích ứng do cha mẹ đánh giá ở trẻ tự kỷ.',
        'anchor': 'With respect to the primary outcome defined in this review and meta-analysis eight studies reported the effects of PMIs on parent-reported adaptive functioning',
    },
    {
        'code': '15E0F666F5',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích cơ chế hiệu quả của các tiếp cận qua cha mẹ (như FPI): sự cải thiện mức độ đáp ứng của người chăm sóc làm trung gian thúc đẩy phát triển ngôn ngữ của trẻ.',
        'anchor': 'Parent-mediated approaches, such as FPI, add to this picture by showing that improvements in caregiver responsivity mediate children’s language outcomes',
    },
    {
        'code': 'DF1B8C0CEE',
        'grade': 1,
        'rationale': 'Đoạn văn nêu tổng quan về trị liệu ngôn ngữ và các can thiệp hành vi phát triển tự nhiên (NDBI) trong điều trị tự kỷ.',
        'anchor': 'Speech–language therapy remains central to ASD intervention. Evidence-based approaches include naturalistic developmental behavioral interventions',
    },
    {
        'code': '135F3D813C',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả phương pháp tổng hợp và thẩm định bằng chứng của nhóm hướng dẫn WHO.',
        'anchor': 'The systematic reviews based on the review questions were used to summarize and appraise the evidence.',
    },
    {
        'code': 'BC272C8842',
        'grade': 1,
        'rationale': 'Bảng nghiên cứu về các chương trình can thiệp nuôi dạy con và tác động đến sự phát triển của trẻ nhỏ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '1EE5787F2B',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu can thiệp của cha mẹ nhằm hỗ trợ các kỹ năng nhận thức và ngôn ngữ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '10CAE5BDE8',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu can thiệp chăm sóc nuôi dạy trẻ sớm.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '463D3B95C9',
        'grade': 1,
        'rationale': 'Bảng thống kê các can thiệp nuôi dạy con trong 3 năm đầu đời.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '4D6B39D630',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả các phép chuyển đổi thống kê dùng trong phân tích tổng hợp, không chứa kết quả về hiệu quả can thiệp.',
        'anchor': '',
    },
    {
        'code': 'A04C1C0EC3',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các hạn chế phương pháp luận trong các nghiên cứu phân tích tổng hợp về can thiệp.',
        'anchor': 'Results of this meta-analysis should be interpreted in the context of several limitations.',
    },
    {
        'code': '715CDBB8E6',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả việc tạo biểu đồ phễu (funnel plots) để đánh giá nguy cơ thiên lệch xuất bản trong các nghiên cứu NDBI.',
        'anchor': 'Funnel plots were created using R (R Core Team, 2023) to assess risk of publication bias',
    },
    {
        'code': '10AA7054E2',
        'grade': 1,
        'rationale': 'Đoạn văn bàn về việc cha mẹ kết hợp giáo dục giấc ngủ với các can thiệp hành vi từng bước cho trẻ tự kỷ.',
        'anchor': 'Therefore, it is often easier and more acceptable for parents to associate sleep education with behavioral gradual interventions',
    },
    {
        'code': '938C99A891',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả phản ứng thử vị thức ăn của trẻ trong một thử nghiệm nhỏ về ăn uống, không chứa đánh giá tổng thể về can thiệp cha mẹ.',
        'anchor': '',
    },
    {
        'code': 'CD5914B6E0',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về hiệu quả của các nhóm tập huấn kỹ năng xã hội (SSGPs) trong việc tăng kiến thức và tương tác xã hội của trẻ tự kỷ.',
        'anchor': 'efficacy of SSGPs in increasing the social knowledge and social skills of autistic youth',
    },
    {
        'code': '3B0FD49FFD',
        'grade': 2,
        'rationale': 'Đoạn văn nêu mục tiêu của các nghiên cứu can thiệp qua cha mẹ là cải thiện hành vi xã hội và giao tiếp của trẻ tự kỷ thông qua việc nâng cao kỹ năng và kiến thức của cha mẹ.',
        'anchor': 'The aim of all of the studies was to improve social behavior and communication skills of children with ASD through increasing the knowledge of parents',
    },
    {
        'code': 'CE59853BA6',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu về các chương trình can thiệp nuôi dạy con giai đoạn sớm.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '8C8B32BE53',
        'grade': 2,
        'rationale': 'Đoạn văn nhấn mạnh tầm quan trọng của việc cha mẹ đóng vai trò chủ động trong trị liệu, khẳng định việc trị liệu sẽ hiệu quả hơn khi cha mẹ tham gia vào quá trình can thiệp.',
        'anchor': 'Therapy for children and teens requires parents to play an active role.',
    },
    {
        'code': 'B8318167E8',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về bằng chứng sơ bộ và nhu cầu nghiên cứu thêm về tính khả thi, hiệu quả của can thiệp do cha mẹ thực hiện từ xa.',
        'anchor': 'This systematic review provides preliminary evidence on the effectiveness of remotely delivered parent-mediated intervention training.',
    },
    {
        'code': '2A268FF039',
        'grade': 3,
        'rationale': 'Tổng quan hệ thống từ 30 thử nghiệm ngẫu nhiên có đối chứng (RCT) chứng minh can thiệp do cha mẹ thực hiện (PMI) đem lại hiệu quả lâm sàng rõ rệt cho trẻ và thanh thiếu niên tự kỷ.',
        'anchor': 'The current systematic review identified 30 RCTs of PMIs for children and adolescents with ASD.',
    },
    {
        'code': 'A11FCF75F2',
        'grade': 2,
        'rationale': 'Đoạn văn khẳng định các can thiệp nuôi dạy con trong 3 năm đầu đời có hiệu quả trong việc cải thiện sự phát triển trẻ thơ và kỹ năng chăm sóc.',
        'anchor': 'Parenting interventions during the first 3 years of childhood are effective for improving ECD and caregiving.',
    },
    {
        'code': 'F23E9BE704',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các tổng quan hệ thống trước đây về các biện pháp can thiệp cho trẻ tự kỷ.',
        'anchor': 'Summaries of included reviews',
    },
    {
        'code': '155AB87361',
        'grade': 1,
        'rationale': 'Trích dẫn định tính ghi nhận phản hồi tích cực của cha mẹ về việc tiếp cận các kỹ năng hỗ trợ con.',
        'anchor': 'And the number of parents that say oh if only we had known this.',
    },
    {
        'code': 'F1E291C1AC',
        'grade': 1,
        'rationale': 'Đoạn trích kết quả từ một nghiên cứu đánh giá chức năng thích ứng sau 6 tháng theo dõi.',
        'anchor': 'A single study (44) reported on parent-rated adaptive functioning after 6 months of follow-up on Vineland Adaptive Behavior Scales Daily Living',
    },
    {
        'code': 'A401D83BE0',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về sự tham gia của cha mẹ và các bằng chứng về sự gắn kết, hiệu quả can thiệp sớm.',
        'anchor': 'our review suggests that parental engagement and support programs may indeed have universal',
    },
    {
        'code': '5940C17B2A',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu các can thiệp NDBI do phụ huynh thực hiện đang là phương pháp được nghiên cứu nhiều nhất với bằng chứng hiệu quả ngày càng gia tăng.',
        'anchor': 'NDBIs are now the most frequently studied intervention approach for this population.',
    },
    {
        'code': '86CFD36472',
        'grade': 1,
        'rationale': 'Mô tả biểu đồ Forest plot thể hiện kích thước hiệu ứng khác biệt trung bình chuẩn hóa (SMD) của các nghiên cứu can thiệp.',
        'anchor': 'Blue squares represent the SMD for each study, with the size of the square being proportional to the study weight.',
    },
    {
        'code': '70EADC6977',
        'grade': 0,
        'rationale': 'Đoạn văn hướng dẫn tự kiểm tra kiến thức sau buổi học trong tài liệu tập huấn CST, không đánh giá hiệu quả can thiệp.',
        'anchor': '',
    },
    {
        'code': '0FDD4F794A',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu về can thiệp nuôi dạy con giai đoạn sớm.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': '58C6B2DE6E',
        'grade': 1,
        'rationale': 'Đoạn mở đầu giới thiệu về ASD và cơ sở lý luận của các can thiệp do cha mẹ thực hiện trong môi trường tự nhiên.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurodevelopmental disorder characterized by early-onset difficulties in social interaction',
    },
    {
        'code': 'BEB75F08F5',
        'grade': 3,
        'rationale': 'Phân tích tổng hợp khẳng định các can thiệp do cha mẹ thực hiện (PMI) có hiệu quả cải thiện tương tác phụ huynh - trẻ, giao tiếp và kỹ năng xã hội của trẻ tự kỷ.',
        'anchor': 'There has been increasing interest in parent-mediated interventions (PMIs) for children with autism spectrum disorders (ASDs).',
    },
    {
        'code': 'B0A0C63525',
        'grade': 0,
        'rationale': 'Bảng định nghĩa các chỉ số đo lường kích thước hiệu ứng và chất lượng nghiên cứu, không chứa số liệu đánh giá can thiệp.',
        'anchor': '',
    },
    {
        'code': '64F7A8FC36',
        'grade': 1,
        'rationale': 'Mô tả hình ảnh biểu đồ Forest plot trình bày kết quả gộp của các nghiên cứu can thiệp.',
        'anchor': 'Blue squares represent the SMD for each study, with the size of the square being proportional to the study weight.',
    },
    {
        'code': 'DD8FA88522',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả quy trình mã hóa dữ liệu nghiên cứu NDBI theo chuẩn phương pháp luận, không chứa kết quả can thiệp.',
        'anchor': '',
    },
    {
        'code': 'A2B9460D08',
        'grade': 1,
        'rationale': 'Đoạn trích ý kiến nhà trị liệu về sự phụ thuộc của kết quả can thiệp vào mức độ gắn kết và nỗ lực của người chăm sóc.',
        'anchor': 'It did work . . . But it ’s an awful lot of input to give, to get to that.',
    },
    {
        'code': 'BD7C73D710',
        'grade': 1,
        'rationale': 'Bảng dữ liệu các nghiên cứu can thiệp nuôi dạy con hỗ trợ phát triển sớm.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'code': 'D33CF9C0BE',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các hạn chế trong việc so sánh các phương thức triển khai can thiệp qua phụ huynh.',
        'anchor': 'Identifying the superior delivery method of intervention for this population is limited by a lack of between-group comparisons',
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
