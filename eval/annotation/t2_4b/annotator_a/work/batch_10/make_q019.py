import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_10.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_10/q019.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q019':
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
        'code': '400EFC81A2',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về triệu chứng ADHD và lo âu đồng mắc trong ASD, không đề cập đến các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '27C95B519D',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích về lo âu và thiếu hụt giao tiếp xã hội ở người tự kỷ và ADHD, không mô tả các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': 'EC17A99975',
        'grade': 0,
        'rationale': 'Đoạn văn nói về vai trò của công cụ giao tiếp tăng cường (AAC) trong thăm khám y tế, không liên quan đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '4AFF1ECDFC',
        'grade': 0,
        'rationale': 'Đoạn văn tổng quan về bối cảnh nghiên cứu tự kỷ tại Việt Nam, không đề cập đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '791E94F30F',
        'grade': 1,
        'rationale': 'Đoạn định nghĩa chung về ASD nhắc đến các hành vi lặp lại và sở thích thu hẹp như một tiêu chuẩn chẩn đoán cốt lõi, cung cấp bối cảnh phân loại.',
        'anchor': 'presence of restricted interests and repetitive behaviors',
    },
    {
        'code': '33C5D117ED',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về chức năng tự điều chỉnh hoặc tìm kiếm cảm giác thỏa mãn thông qua các hành vi rập khuôn vận động và phát âm ở trẻ tự kỷ.',
        'anchor': 'motor and vocal stereotypy may sometimes reflect a search for positive and pleasurable sensory stimulation',
    },
    {
        'code': '4540AED167',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu về các yếu tố dự báo sớm ở trẻ em, không mô tả các dạng hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '718147AA55',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả các khiếm khuyết ngôn ngữ ở trẻ tự kỷ và có đề cập đến chứng nhại lời (echolalia) - một dạng hành vi lặp lại bằng lời nói.',
        'anchor': 'Speech and language impairments are among the most recognizable features of ASD.',
    },
    {
        'code': '8985F761C0',
        'grade': 1,
        'rationale': 'Đoạn văn trích Tiêu chuẩn A của DSM-5 về khiếm khuyết giao tiếp và tương tác xã hội, cung cấp bối cảnh tiêu chuẩn chẩn đoán nhưng không đi sâu vào Tiêu chuẩn B (hành vi lặp lại).',
        'anchor': 'Deficits in social-emotional reciprocity, ranging, for example, from abnormal social approach',
    },
    {
        'code': '073DDB0223',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả thử nghiệm về nhận thức thị giác và chứng sợ thức ăn mới ở trẻ tự kỷ, không đề cập đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '3F86AD10A4',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu các triệu chứng cốt lõi của ASD bao gồm giao tiếp xã hội và các hành vi hạn hẹp lặp lại.',
        'anchor': 'Autisms Spectrum Disorders (ASD) are characterized by core symptoms (social communication and restricted and repetitive behaviors)',
    },
    {
        'code': '4980082CFB',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu về mối liên hệ giữa giấc ngủ và hành vi thách thức ở trẻ tự kỷ, không mô tả chi tiết các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '2C0B11A193',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích định nghĩa lâm sàng của các hành vi vận động lặp lại (motor stereotypies, vocal stereotypy) và sự khăng khăng giữ nguyên nếp (insistence on sameness) ở người tự kỷ.',
        'anchor': 'Atypical sensory processing, including hyper‐responsiveness to sounds and visual objects and scenes, is predictive of repetitive motor behavior in autistic people',
    },
    {
        'code': '45C21D2964',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa ASD bao gồm khiếm khuyết giao tiếp xã hội và các hành vi hạn hẹp, lặp lại.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors',
    },
    {
        'code': '004190D694',
        'grade': 0,
        'rationale': 'Đoạn văn về tỷ lệ ADHD và triệu chứng lo âu ở người tự kỷ, không đề cập chi tiết đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '3096828837',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về tỷ lệ hiện mắc trong phân tích tổng hợp, không liên quan đến các dạng hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': 'AF1C1C175B',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu định nghĩa ASD bao gồm các kiểu hành vi hoặc sở thích lặp lại và hạn hẹp.',
        'anchor': 'limited and repetitive behavioural patterns',
    },
    {
        'code': 'D8C2324FEE',
        'grade': 3,
        'rationale': 'Đoạn văn của CDC liệt kê danh sách cụ thể các hành vi hạn chế và lặp lại phổ biến ở người tự kỷ, trả lời trực tiếp câu hỏi.',
        'anchor': 'The list below gives some examples of different types of behaviors that are common among people diagnosed with ASD.',
    },
    {
        'code': 'A185974BCB',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả các rối loạn vận động, tật giật cơ (tics) và các hành vi rập khuôn vận động (motor stereotypies) thường gặp ở trẻ tự kỷ.',
        'anchor': 'Movement disorders, Tics, Tourette Syndrome: Tic disorders, such as Tourette Syndrome (TS), are more common in autistic individuals',
    },
    {
        'code': '86ED72C5A2',
        'grade': 1,
        'rationale': 'Bảng điểm các phân nhóm của ADOS và ADI-R, bao gồm thang đo hành vi lặp lại hạn hẹp (RRB) trong đánh giá chẩn đoán.',
        'anchor': 'Mean scores and standard deviation of ADOS and ADI-R subdomains',
    },
    {
        'code': '6902A7E4B0',
        'grade': 0,
        'rationale': 'Đoạn thảo luận về sự khác biệt giữa lo âu và bệnh đồng mắc tâm thần ở trẻ tự kỷ và ADHD, không mô tả các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '4056B65529',
        'grade': 0,
        'rationale': 'Bảng số liệu điểm trung bình về hành vi bỏ trốn (elopement) ở các nhóm trẻ, không nói về các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '738EA13AE2',
        'grade': 3,
        'rationale': 'Tài liệu CDC nêu rõ các biểu hiện cụ thể của hành vi lặp lại: lặp lại từ ngữ, sắp xếp đồ vật theo hàng, chơi đồ chơi cùng một cách, khăng khăng theo lịch trình rập khuôn.',
        'anchor': 'People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests.',
    },
    {
        'code': '223211B891',
        'grade': 1,
        'rationale': 'Đoạn hướng dẫn người chăm sóc kỹ thuật bắt chước hành vi phù hợp của trẻ trong giờ chơi, gián tiếp liên quan đến quản lý hành vi.',
        'anchor': 'By imitating, you are rewarding your child’s play ideas.',
    },
    {
        'code': '1093C91EEF',
        'grade': 0,
        'rationale': 'Đoạn văn về phản ứng miễn dịch bất thường và cytokine ở người tự kỷ, không liên quan đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '4FAD653E98',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả công cụ sàng lọc CBCL (Child Behaviour Checklist), không phân tích chi tiết các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '8BFE5845E7',
        'grade': 1,
        'rationale': 'Đoạn tổng quan nêu định nghĩa tự kỷ với khiếm khuyết xã hội, hành vi lặp lại và giao tiếp hạn chế.',
        'anchor': 'Autism spectrum disorder (ASD), a key topic in today’s clinical industry throughout the globe, refers to a pervasive developmental disorder that hinders an individual’s skills in socialisation, creates repetitive behaviours',
    },
    {
        'code': 'A29B10175E',
        'grade': 0,
        'rationale': 'Đoạn văn là phần ghi chú mã hóa tiêu chuẩn DSM-IV và DSM-5, không liệt kê các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '41F055D980',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về tỷ lệ hiện mắc các hành vi thách thức ở trẻ tự kỷ, bao gồm các hành vi tự gây thương tích và hung tính.',
        'anchor': 'Challenging behavior can be prevalent in children with ASD.',
    },
    {
        'code': 'D7C8E4E5F0',
        'grade': 0,
        'rationale': 'Đoạn văn bàn về phát hiện sớm chậm phát triển vận động ở trẻ nhỏ, không đề cập đến hành vi lặp lại ở trẻ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'CC1F148200',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu ASD với đặc trưng khiếm khuyết tương tác xã hội và sự xuất hiện của các hành vi rập khuôn, lặp lại.',
        'anchor': 'It is characterized by two core domains: persistent social communication differences and restricted',
    },
    {
        'code': 'EDDE0C9121',
        'grade': 0,
        'rationale': 'Bảng mô tả các hành vi thực hành cho ăn của người chăm sóc, không mô tả các hành vi lặp lại của trẻ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'BE3CDE67E0',
        'grade': 1,
        'rationale': 'Đoạn văn định nghĩa các đặc điểm cốt lõi của tự kỷ bao gồm sở thích tập trung và các hành vi lặp lại.',
        'anchor': 'Autism is a neurodevelopmental disability (NDD) characterized by core features such as social communication challenges, focused interests, and repetitive behaviors',
    },
    {
        'code': '38F5439A50',
        'grade': 0,
        'rationale': 'Đoạn văn về sự tham gia của cộng đồng tự kỷ trong nghiên cứu khoa học tại Việt Nam, không liên quan đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '99A27CBE96',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về định hướng nghiên cứu đặc điểm thính giác ở người tự kỷ, không đề cập đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '9195EC6F43',
        'grade': 1,
        'rationale': 'Tài liệu tóm tắt các điểm cơ bản về tự kỷ, nêu việc trẻ gặp khó khăn trong giao tiếp và có các hành vi hoặc sở thích lặp lại, thu hẹp.',
        'anchor': 'People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests.',
    },
    {
        'code': 'A1A30157C6',
        'grade': 0,
        'rationale': 'Đoạn thông tin bản quyền và lưu hành tài liệu, hoàn toàn không liên quan đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '46C46AABC4',
        'grade': 0,
        'rationale': 'Đoạn văn về Đạo luật Autism CARES của Hoa Kỳ hỗ trợ tài trợ nghiên cứu, không liên quan đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '5CF809E946',
        'grade': 0,
        'rationale': 'Đoạn văn về nguy cơ đi lang thang (elopement) ở trẻ khuyết tật phát triển, không mô tả các dạng hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': 'D06307E2D3',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả công cụ phỏng vấn chẩn đoán ADI-R, có chứa lĩnh vực đánh giá hành vi lặp lại và rập khuôn.',
        'anchor': 'A semi-structured interview administered to parents, designed to make a diagnosis of autism according to DSM-IV criteria.',
    },
    {
        'code': 'BD99324AD0',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ tiêu chuẩn chẩn đoán ASD theo hai lĩnh vực, trong đó có mẫu hình hành vi, sở thích hoặc hoạt động hạn hẹp, lặp lại.',
        'anchor': 'restricted, repetitive patterns of behavior, interests, or activities (RRBs)',
    },
    {
        'code': 'C6E18A5052',
        'grade': 1,
        'rationale': 'Đoạn nghiên cứu về mối tương quan giữa vi khuẩn đường ruột với mức độ hành vi rập khuôn lặp lại đo theo thang ADI.',
        'anchor': 'strong association of the amount of Desulfovibrio spp. with the severity of ASD according to the Autism Diagnostic Interview (ADI) restricted/repetitive behavior subscale score',
    },
    {
        'code': '1E0CBB4479',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả khó khăn trong việc hiểu ngôn ngữ cơ thể và ngữ điệu giọng nói, không đề cập đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '83A6159C48',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu xu hướng tham gia vào các hành vi lặp lại hạn hẹp (RRBs) và mối liên quan với xử lý cảm giác bất thường ở trẻ tự kỷ.',
        'anchor': 'restricted and repetitive behaviors including commonly associat',
    },
    {
        'code': 'A74E2D0492',
        'grade': 0,
        'rationale': 'Đoạn văn về hiện tượng giảm đáp ứng và thích nghi thính giác ở người tự kỷ, không liên quan đến các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '3645EB43E9',
        'grade': 0,
        'rationale': 'Đoạn văn về bệnh não động kinh và co giật ở trẻ tự kỷ, không mô tả các hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '86B65E3AD0',
        'grade': 3,
        'rationale': 'Tài liệu CDC liệt kê đầy đủ các ví dụ cụ thể về hành vi lặp lại ở trẻ tự kỷ: xếp đồ chơi thành hàng, lặp lại lời nói, chơi đồ chơi cố định một kiểu, vỗ tay, đung đưa người.',
        'anchor': 'Lines up toys or other objects and gets upset when order is changed',
    },
    {
        'code': '4AA90B323B',
        'grade': 2,
        'rationale': 'Tài liệu hướng dẫn nêu các ví dụ về hành vi lặp lại tìm kiếm cảm giác: sờ quần áo người lạ, ngửi đồ vật, nhìn chăm chú vào đồ vật quay tròn.',
        'anchor': 'Challenging behaviour to get access to a sensation Behaviour can help a child get sensation (a feeling)',
    },
    {
        'code': '6D29A2A1F6',
        'grade': 1,
        'rationale': 'Đoạn văn bàn về ảnh hưởng của xử lý thính giác đối với các hành vi hạn chế và lặp lại ở người tự kỷ.',
        'anchor': 'recent evidence suggests that the autistic auditory profile may also impact the non‐social domains of autistic behavior, specifically around “restrictive and repetitive behaviors”',
    },
    {
        'code': 'BB46B2D9FA',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về sự khác biệt triệu chứng lo âu theo độ tuổi và giới tính ở người tự kỷ, không mô tả hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': '47E22F94B0',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu thang đo quan sát chẩn đoán ADOS đánh giá các hành vi lặp lại và hạn hẹp.',
        'anchor': 'The Autism Diagnostic Observation Schedule (ADOS',
    },
    {
        'code': '16242627FF',
        'grade': 3,
        'rationale': 'Đoạn văn trích dẫn đầy đủ Tiêu chuẩn B của DSM-5 về các dạng hành vi lặp lại: vận động rập khuôn, sử dụng đồ vật hoặc lời nói rập khuôn, khăng khăng giữ nếp sinh hoạt, sở thích hạn hẹp, bất thường cảm giác.',
        'anchor': 'Stereotyped or repetitive motor movements, use of objects, or speech (e.g., simple motor stereotypes, lining up toys or flipping objects, echolalia, idiosyncratic phrases).',
    },
    {
        'code': '4E92DBEA7D',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh chức năng thích ứng ở trẻ tự kỷ có và không có ADHD, không đề cập đến hành vi lặp lại.',
        'anchor': '',
    },
    {
        'code': 'ADC26D8FDA',
        'grade': 3,
        'rationale': 'Bảng tiêu chuẩn chẩn đoán DSM-5 liệt kê cụ thể các nhóm hành vi lặp lại và hạn hẹp: cử động rập khuôn, thói quen cứng nhắc, sở thích cố định hạn hẹp và phản ứng cảm giác bất thường.',
        'anchor': '| 1. Stereotyped or repetitive motor movements, use of objects, or speech |',
    },
    {
        'code': 'ED01A4D7F4',
        'grade': 0,
        'rationale': 'Đoạn văn nói về sự kỳ thị và cảm xúc gia đình khi nhận chẩn đoán tự kỷ tại Việt Nam, không liên quan đến hành vi lặp lại.',
        'anchor': '',
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
