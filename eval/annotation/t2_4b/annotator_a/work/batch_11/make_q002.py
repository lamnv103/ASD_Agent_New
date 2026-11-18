import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_11.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_11/q002.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q002':
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
        'code': '202A4E9806',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu thống kê trực tiếp của CDC về tỷ lệ mắc tự kỷ ở trẻ em (khoảng 1 trên 54 trẻ tại Mỹ) và tỷ lệ phổ biến theo giới tính (trẻ trai gấp 4 lần trẻ gái).',
        'anchor': 'The Centers for Disease Control and Prevention (CDC) estimates that about 1 in every 54 children in the U.S. has been identified as having ASD.',
    },
    {
        'code': 'EDBEA411E9',
        'grade': 1,
        'rationale': 'Đoạn mở đầu định nghĩa rối loạn phổ tự kỷ và các vấn đề tâm thần đồng mắc ở trẻ em, cung cấp bối cảnh lâm sàng.',
        'anchor': 'Autism Spectrum Disorder (ASD) is a neurodevelopmental disorder characterized by persistent deficits in social communication',
    },
    {
        'code': 'C045C09F16',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về triệu chứng lo âu và ADHD đồng mắc ở trẻ tự kỷ, không đề cập đến tỷ lệ phổ biến của tự kỷ trong dân số.',
        'anchor': '',
    },
    {
        'code': '8443897843',
        'grade': 0,
        'rationale': 'Bảng số liệu phân loại không rõ bối cảnh, không liên quan đến tỷ lệ tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': 'ECF77FC0E7',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về cuộc điều tra dịch tễ học đại diện quốc gia đầu tiên về tỷ lệ tự kỷ tại Việt Nam và sự cần thiết của dữ liệu dịch tễ học.',
        'anchor': 'To the best of our knowledge, this is the first epidemiological, nationally representative, population-based survey on autism spectrum disorders (ASDs) in Vietnam.',
    },
    {
        'code': 'BA814F08B0',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp ước tính tỷ lệ mắc tự kỷ trên toàn thế giới là 62 trên 10.000 trẻ em (khoảng 0,62%).',
        'anchor': 'with an estimated prevalence of 62/10,000 children worldwide.',
    },
    {
        'code': '37F098141B',
        'grade': 3,
        'rationale': 'Nghiên cứu dịch tễ tại Việt Nam cung cấp số liệu trực tiếp: tỷ lệ hiện mắc ASD ở trẻ 18-30 tháng tuổi tại 3 tỉnh phía Bắc là 0,752%.',
        'anchor': 'The overall prevalence of ASD among children aged 18 and 30 months in the three cities/provinces was 0.752%',
    },
    {
        'code': '3492D9E99E',
        'grade': 0,
        'rationale': 'Đoạn văn nói về tỷ lệ dị ứng thức ăn ở trẻ tự kỷ so với trẻ không tự kỷ, không nêu tỷ lệ mắc tự kỷ trong cộng đồng.',
        'anchor': '',
    },
    {
        'code': 'BFEC8D15A7',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu ước tính tỷ lệ tự kỷ ở trẻ em là 1 trên 68 trẻ.',
        'anchor': 'According to [2], one out of every 68 children has autism.',
    },
    {
        'code': '46D69F8400',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa các đặc điểm cốt lõi của tự kỷ, cung cấp bối cảnh chung nhưng không chứa số liệu tỷ lệ phổ biến.',
        'anchor': 'Autism is a neurodevelopmental disability (NDD) characterized by core features such as social communication challenges',
    },
    {
        'code': '522236ED9A',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các bệnh đồng mắc ở các giai đoạn cuộc sống khác nhau của người tự kỷ.',
        'anchor': 'findings regarding comorbidity are not representative for the different stages of a life with ASD.',
    },
    {
        'code': '729A2D9DDD',
        'grade': 0,
        'rationale': 'Đoạn văn về tỷ lệ các triệu chứng ADHD và lo âu đồng mắc trong ASD, không nói về độ phổ biến của ASD.',
        'anchor': '',
    },
    {
        'code': '46EC777A4B',
        'grade': 3,
        'rationale': 'Đoạn thảo luận phân tích số liệu tỷ lệ hiện mắc ASD ở trẻ nhỏ tại Việt Nam (0,752%) và so sánh với các nghiên cứu trước đây.',
        'anchor': 'This study found a prevalence of ASD among very young children that is higher than reported from previous studies in Vietnam',
    },
    {
        'code': '29DDB4081A',
        'grade': 1,
        'rationale': 'Đoạn trích nhắc đến sự gia tăng tỷ lệ tự kỷ ở trẻ em có bệnh viêm da dị ứng từ cuộc Điều tra Sức khỏe Trẻ em Quốc gia 2007.',
        'anchor': 'prevalence of autism was significantly increased in children with AD (2.19 vs 0.89%',
    },
    {
        'code': 'D3894B9801',
        'grade': 0,
        'rationale': 'Đoạn văn về chức năng thích ứng ở trẻ tự kỷ kèm ADHD, không liên quan đến tỷ lệ tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': '7849F529E5',
        'grade': 0,
        'rationale': 'Đoạn văn về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không có số liệu tỷ lệ mắc.',
        'anchor': '',
    },
    {
        'code': '450158578A',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa rối loạn phổ tự kỷ và các biến thiên lâm sàng, không có số liệu tỷ lệ phổ biến.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits',
    },
    {
        'code': 'B0390480D0',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về triệu chứng tiêu hóa và hệ vi sinh đường ruột ở trẻ tự kỷ, không liên quan đến tỷ lệ phổ biến của bệnh.',
        'anchor': '',
    },
    {
        'code': 'B4CD710737',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả cỡ mẫu tham gia cuộc điều tra sàng lọc dịch tễ tự kỷ tại miền Bắc Việt Nam (40.243 trẻ).',
        'anchor': 'A total of 40,243 children (94.5% of those approached) agreed to participate in the study and completed the face-to-face interviews',
    },
    {
        'code': 'BCEAF5CA37',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp ước tính hiện tại về tỷ lệ tự kỷ chiếm khoảng 1-4% dân số.',
        'anchor': 'Autism is a relatively common diagnosis, with current estimates suggesting approximately 1-4% of the population is affected.',
    },
    {
        'code': '6573C700E3',
        'grade': 0,
        'rationale': 'Đoạn văn về tính chọn lọc thức ăn và rối loạn tiêu hóa ở trẻ em, không liên quan đến tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '8AC671C65F',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu can thiệp, không chứa số liệu tỷ lệ tự kỷ trong dân số.',
        'anchor': '',
    },
    {
        'code': '1A4C03966D',
        'grade': 0,
        'rationale': 'Bảng tần suất các rối loạn tâm thần đồng mắc ở trẻ tự kỷ và trẻ ADHD, không nói về tỷ lệ tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': 'D8212E1206',
        'grade': 0,
        'rationale': 'Đoạn văn về miễn dịch và bệnh tự miễn trong tự kỷ, không liên quan đến tỷ lệ mắc tự kỷ.',
        'anchor': '',
    },
    {
        'code': '4E42B01257',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu chung về rối loạn phổ tự kỷ và các thách thức về giao tiếp, xã hội ở trẻ em.',
        'anchor': 'Autism spectrum disorder (ASD) is a developmental disability that can cause significant social, communication, and behavioral challenges.',
    },
    {
        'code': '058BE93ECD',
        'grade': 0,
        'rationale': 'Đoạn văn về các tình trạng thần kinh đồng mắc ở người tự kỷ, không chứa số liệu tỷ lệ mắc tự kỷ.',
        'anchor': '',
    },
    {
        'code': '1BE0FA8701',
        'grade': 0,
        'rationale': 'Đoạn văn ghi nhận đóng góp của các tác giả trong một nghiên cứu, không chứa thông tin nội dung về tự kỷ.',
        'anchor': '',
    },
    {
        'code': '1C74C78050',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về sự chênh lệch trong sàng lọc và độ tuổi chẩn đoán tự kỷ ở trẻ nhỏ.',
        'anchor': 'Although young children can be reliably diagnosed at age 2',
    },
    {
        'code': 'C5C2831F5A',
        'grade': 3,
        'rationale': 'Đoạn văn nêu kết quả điều tra dân số tại Việt Nam cho thấy tỷ lệ hiện mắc ASD ở trẻ 18-30 tháng tại miền Bắc là 0,752%.',
        'anchor': 'Our findings show that the prevalence of ASD among children aged 18–30 months in northern Vietnam was 0.752%',
    },
    {
        'code': '39194C18C0',
        'grade': 3,
        'rationale': 'Đoạn văn nêu rõ số liệu tỷ lệ mắc tự kỷ: 1 trên 44 trẻ em tại Hoa Kỳ và 1 trên 160 trẻ em trên toàn cầu.',
        'anchor': 'Recent data indicate that one in 44 children in the United States (Maenner et al., 2021) and one in 160 children internationally',
    },
    {
        'code': '5600ABD5BC',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả công cụ phỏng vấn KID-SCID dùng để đánh giá bệnh tâm thần đồng mắc, không nêu tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'DA788B8957',
        'grade': 0,
        'rationale': 'Đoạn văn về tỷ lệ đi lang thang (elopement) ở trẻ khuyết tật phát triển, không liên quan đến tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '71389341F5',
        'grade': 2,
        'rationale': 'Đoạn văn ghi nhận tỷ lệ hiện mắc ngày càng tăng của ASD đặt ra áp lực lớn cho các dịch vụ can thiệp sớm và giáo dục.',
        'anchor': 'The increasing prevalence of ASD exerts major demands on early intervention services and education',
    },
    {
        'code': '4701C26B7D',
        'grade': 3,
        'rationale': 'Tổng quan dịch tễ học chi tiết về tỷ lệ mắc ASD trên thế giới (0,5-1%), Châu Âu (0,019-7,2%), Mỹ (1,13%), Nam Á, Trung Quốc, Hàn Quốc và Việt Nam (0,415% - 0,52%).',
        'anchor': 'Autism spectrum disorders prevalence appears to be increasing worldwide, with reported prevalence of about 0.5–1%',
    },
    {
        'code': '8FA1F14701',
        'grade': 0,
        'rationale': 'Đoạn văn báo cáo độ tin cậy giữa những người đánh giá trong nghiên cứu tâm thần, không chứa thông tin về tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '54E3782DFB',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về tầm quan trọng của các ước tính dịch tễ học dựa trên dân số đối với các bệnh đồng mắc.',
        'anchor': 'Knowledge gained in population based estimates of comorbidity is therefore not only practically important',
    },
    {
        'code': '1664DFAD67',
        'grade': 1,
        'rationale': 'Đoạn văn khuyến nghị về việc áp dụng các hướng dẫn sàng lọc tự kỷ dựa trên bằng chứng trong y tế công cộng.',
        'anchor': 'Effective public health practice necessitates the adoption of structured, evidence-based guidelines for autism screening.',
    },
    {
        'code': 'BFABED771B',
        'grade': 1,
        'rationale': 'Đoạn mở đầu định nghĩa tự kỷ với các đặc điểm khó khăn giao tiếp xã hội và hành vi lặp lại, không có số liệu tỷ lệ mắc.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurodevelopmental disorder characterised by ongoing difficulties in social interactions and communication',
    },
    {
        'code': 'BBCBFB14D9',
        'grade': 0,
        'rationale': 'Đoạn văn báo cáo tỷ lệ căng trương lực (catatonia 1,8%) ở người tự kỷ trong phân tích tổng hợp, không phải tỷ lệ mắc tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': '58BB614F87',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về mức độ lo âu và bệnh đồng mắc tâm thần ở trẻ tự kỷ và ADHD, không liên quan đến tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '76B3005D45',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả định nghĩa ca bệnh của các rối loạn đồng mắc theo DSM/ICD, không có thông tin tỷ lệ mắc tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'B2D441016A',
        'grade': 0,
        'rationale': 'Đoạn văn về bệnh động kinh đồng mắc trong tự kỷ, không nói về tỷ lệ phổ biến của tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': 'F48F71175C',
        'grade': 0,
        'rationale': 'Đoạn văn về các vấn đề tiêu hóa thường gặp ở trẻ tự kỷ, không liên quan đến tỷ lệ tự kỷ trong dân số.',
        'anchor': '',
    },
    {
        'code': 'AA11375D32',
        'grade': 0,
        'rationale': 'Đoạn văn khuyến nghị hạ ngưỡng chuyển tuyến khám tiêu hóa ở trẻ tự kỷ, không liên quan đến độ phổ biến của tự kỷ.',
        'anchor': '',
    },
    {
        'code': '63A62ABAA5',
        'grade': 0,
        'rationale': 'Đoạn văn về sự căng thẳng và lo âu liên quan đến tương tác xã hội ở người tự kỷ, không đề cập đến tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'CB2A325EED',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả phân tích thống kê ngẫu nhiên cho các bệnh đồng mắc tâm thần ở trẻ em, không nêu tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '15CC786F4F',
        'grade': 0,
        'rationale': 'Đoạn văn về sự kỳ thị và quan niệm văn hóa về tự kỷ tại Việt Nam, không có số liệu tỷ lệ phổ biến.',
        'anchor': '',
    },
    {
        'code': 'A29DA3FF9A',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu trực tiếp về tỷ lệ tự kỷ ở trẻ tiểu học tại Vương quốc Anh là khoảng 1-2%.',
        'anchor': 'The prevalence of autism in UK primary school-aged children is approximately 1 –2%1',
    },
    {
        'code': '5179796AD9',
        'grade': 0,
        'rationale': 'Đoạn văn về tiêu chuẩn phân loại bệnh đồng mắc theo công cụ KID-SCID ở trẻ tự kỷ, không chứa số liệu tỷ lệ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'DB6DE736A2',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các bệnh lý tâm thần đồng mắc trong ASD, không nói về tỷ lệ phổ biến của tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': '1A70A49601',
        'grade': 0,
        'rationale': 'Đoạn văn tổng kết tỷ lệ các rối loạn tâm thần đồng mắc trong tự kỷ, không nêu tỷ lệ tự kỷ ở trẻ em.',
        'anchor': '',
    },
    {
        'code': '4EAD2A3D47',
        'grade': 1,
        'rationale': 'Đoạn tóm tắt tổng quan nghiên cứu tự kỷ tại Việt Nam, cung cấp bối cảnh về sự thiếu hụt nghiên cứu dịch tễ trong nước.',
        'anchor': 'Autism research has mostly focused on Western contexts, with few studies in Vietnamese cultural contexts.',
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
