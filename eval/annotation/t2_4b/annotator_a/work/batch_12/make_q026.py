import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_12.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_12/q026.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q026':
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
        'code': '4C1A9BD7DB',
        'grade': 1,
        'rationale': 'Đoạn văn báo cáo kết quả cuộc điều tra sàng lọc ASD bằng công cụ M-CHAT ở trẻ 18 và 30 tháng tuổi tại Việt Nam.',
        'anchor': 'The overall prevalence of ASDs among children aged 18 and 30 months in 7 cities/provinces was 0.758%',
    },
    {
        'code': '2DEBE0482B',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu công cụ sàng lọc ESAT được thiết kế cho trẻ sơ sinh và trẻ nhỏ từ 0 đến 36 tháng tuổi.',
        'anchor': 'The ESAT’s design is based on the symptoms of ASD and seeks to differentiate infants aged 0–36 months',
    },
    {
        'code': 'D8005F759C',
        'grade': 0,
        'rationale': 'Bảng nghiên cứu về giấc ngủ và hành vi thách thức ở trẻ tự kỷ, không liên quan đến độ tuổi sàng lọc tự kỷ.',
        'anchor': '',
    },
    {
        'code': '9746ACFC54',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả công cụ sàng lọc mức độ 2 STAT được thiết kế để sử dụng cho trẻ nhỏ từ 24 đến 36 tháng tuổi.',
        'anchor': 'The Screening Tool for Autism in Toddlers (STAT; Stone et al., 2004) is a Level 2 screening measure administered by a trained professional.',
    },
    {
        'code': '25D3DA7E2D',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả công cụ sàng lọc RAADS-R được thiết kế cho người trưởng thành trên 18 tuổi, không liên quan đến sàng lọc ở trẻ em.',
        'anchor': '',
    },
    {
        'code': '4F1D529BD3',
        'grade': 1,
        'rationale': 'Đoạn văn tổng quan về xu hướng nghiên cứu và các công cụ sàng lọc tự kỷ trong 3 thập kỷ qua.',
        'anchor': 'There is an increasing trend in studies related to autism symptoms and screening over the last three decades.',
    },
    {
        'code': 'AA681CD1D8',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các phương pháp sàng lọc tự kỷ dạng kết hợp (hybrid methods), cung cấp thông tin kỹ thuật về các công cụ.',
        'anchor': 'Summary of the hybrid Autism spectrum disorder (ASD) screening methods.',
    },
    {
        'code': '7CDB06F8C5',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả bảng hỏi sàng lọc CAST được thiết kế cho trẻ em trong độ tuổi từ 4 đến 11 tuổi.',
        'anchor': 'The CAST is another parental or self-completion questionnaire-based autism screening tool that was developed by [22] at the Autism Research Centre',
    },
    {
        'code': '236F26F030',
        'grade': 3,
        'rationale': 'Viện Hàn lâm Nhi khoa Hoa Kỳ (AAP) khuyến nghị chính thức: sàng lọc phát triển chung ở các mốc 9, 18, 30 tháng và sàng lọc chuyên biệt tự kỷ ở mốc 18 và 24 tháng.',
        'anchor': 'recommends that children be screened for general development using standardized, validated tools at 9, 18, or 30 months and for autism at 18 and 24 months',
    },
    {
        'code': '426A3ECCD0',
        'grade': 0,
        'rationale': 'Đoạn văn về đáp ứng miễn dịch và tự miễn ở trẻ tự kỷ, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': 'ED230694C4',
        'grade': 1,
        'rationale': 'Đoạn văn so sánh độ đặc hiệu của các công cụ sàng lọc tự kỷ khác nhau, cung cấp bối cảnh đo lường.',
        'anchor': 'Similarly, RAADS-R has shown the highest specificity of 100% and DBD-ES has displayed the lowest recorded specificity at 48%.',
    },
    {
        'code': '4989BF9A75',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về triệu chứng tiêu hóa và hệ vi sinh đường ruột ở trẻ tự kỷ, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': 'D4B7E95901',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về thời gian thực hiện các bài tập và bảng hỏi của công cụ sàng lọc tự kỷ.',
        'anchor': 'making it more time consuming than the other available tools.',
    },
    {
        'code': '582A20622B',
        'grade': 3,
        'rationale': 'Đoạn văn nêu rõ các triệu chứng tự kỷ thường bắt đầu xuất hiện từ 12 đến 18 tháng tuổi và khuyến nghị sàng lọc ở các mốc 18 và 24 tháng.',
        'anchor': 'Research has shown that symptoms of autism typically begin to emerge between 12 and 18 months of age',
    },
    {
        'code': '58D58CDBEC',
        'grade': 0,
        'rationale': 'Đoạn văn về chức năng thích ứng ở trẻ tự kỷ kèm ADHD, không liên quan đến sàng lọc tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'D4F2F87B2C',
        'grade': 0,
        'rationale': 'Tài liệu liệt kê các ví dụ về khó khăn giao tiếp xã hội ở người tự kỷ, không đề cập đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': 'DE071711E4',
        'grade': 1,
        'rationale': 'Đoạn mô tả quy trình mời các trẻ có kết quả sàng lọc dương tính đến khám chẩn đoán khẳng định trong một nghiên cứu.',
        'anchor': 'All children of screen-positive group and 2% children of screen-negative group were invited to diagnostic confirmation assessment.',
    },
    {
        'code': '87D040B1A0',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về nhận thức ngày càng tăng về tự kỷ và sự sẵn có của các công cụ sàng lọc giúp phát hiện sớm.',
        'anchor': 'Autism is no longer a dilemma for ordinary people due to the rapidly increasing awareness of the ASD spectrum',
    },
    {
        'code': '837611E63F',
        'grade': 0,
        'rationale': 'Đoạn văn về tình trạng béo phì của người mẹ liên quan đến nguy cơ có kết quả sàng lọc tự kỷ dương tính, không nêu mốc tuổi sàng lọc.',
        'anchor': '',
    },
    {
        'code': '16969DE047',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả công cụ sàng lọc ITC (thuộc CSBS-DP) được sử dụng để sàng lọc sớm các khó khăn giao tiếp và tự kỷ ở trẻ từ 6 đến 24 tháng tuổi.',
        'anchor': 'The ICT is one component of the Communication and Symbolic Behaviour Scale—Developmental Profile (CSBS-DP) established by [49]',
    },
    {
        'code': 'A635EBAB82',
        'grade': 3,
        'rationale': 'Viện Hàn lâm Nhi khoa Hoa Kỳ (AAP) khuyến nghị sàng lọc phổ quát tự kỷ cho tất cả trẻ em tại các lần khám sức khỏe định kỳ lúc 18 và 24 tháng tuổi.',
        'anchor': 'The American Academy of Pediatrics recommends that all children be screened for autism at 18 and 24 months',
    },
    {
        'code': 'FB8FD325AD',
        'grade': 3,
        'rationale': 'Hướng dẫn y tế công cộng nêu rõ khuyến nghị sàng lọc tự kỷ rộng rãi ở mốc 18 và 24 tháng tuổi để can thiệp kịp thời.',
        'anchor': 'Effective public health practice necessitates the adoption of structured, evidence-based guidelines for autism screening.',
    },
    {
        'code': 'E212CFB2F8',
        'grade': 0,
        'rationale': 'Đoạn văn về các yếu tố môi trường liên quan đến tự kỷ như valproate hoặc sinh non, không đề cập đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': '986A6E53C1',
        'grade': 0,
        'rationale': 'Đoạn văn về hành vi đi lang thang (elopement) ở trẻ khuyết tật phát triển, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': '40DA12B01D',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả công cụ sàng lọc CSBS-DP dùng để phát hiện sớm nguy cơ khuyết tật giao tiếp ở trẻ nhỏ từ 6 đến 24 tháng tuổi.',
        'anchor': 'identify the risk of communication and symbolic functioning disabilities in infants aged from 6 to 24 months',
    },
    {
        'code': '39209A5006',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả công cụ M-CHAT dùng để sàng lọc tự kỷ cho trẻ em ở độ tuổi biết đi từ 16 đến 30 tháng tuổi.',
        'anchor': 'Modified Checklist for Autism in Toddlers (M-CHAT) was utilized for the screening phase of our study.',
    },
    {
        'code': 'E63C96F710',
        'grade': 1,
        'rationale': 'Đoạn văn bàn về sự tiện lợi của các công cụ sàng lọc tự kỷ trực tuyến và ứng dụng điện thoại.',
        'anchor': 'Some of the discussed ASD screening tools are available on the internet, either as web-based online tests or smartphone applications.',
    },
    {
        'code': '2C0644D13C',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu công cụ sàng lọc tương tác STAT dùng để phân biệt trẻ tự kỷ với các rối loạn phát triển khác ở lứa tuổi chập chững biết đi.',
        'anchor': 'The STAT is another interactive screening tool for differentiating children with autism from those with other developmental disorders.',
    },
    {
        'code': '0544D3C3F0',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ công cụ bảng kiểm M-CHAT được xác thực để sàng lọc nguy cơ tự kỷ cho trẻ từ 16 đến 30 tháng tuổi.',
        'anchor': 'We used the 23 item Modified Checklist for Autism in Toddlers (M-CHAT) to screen children with high risk of ASD.',
    },
    {
        'code': 'D5FF4E946D',
        'grade': 3,
        'rationale': 'Tài liệu hướng dẫn của CDC chỉ rõ các mốc tuổi khám sàng lọc phát triển định kỳ: 9 tháng, 18 tháng, và 30 tháng, cùng với sàng lọc chuyên biệt tự kỷ lúc 18 và 24 tháng.',
        'anchor': 'The American Academy of Pediatrics (AAP) recommends developmental and behavioral screening for all children during regular well-child visits',
    },
    {
        'code': '3AF957284D',
        'grade': 3,
        'rationale': 'Tài liệu CDC khẳng định tự kỷ có thể được phát hiện lúc 18 tháng tuổi hoặc sớm hơn, và khuyến nghị trẻ cần được sàng lọc phát triển định kỳ lúc 9, 18, 24 hoặc 30 tháng.',
        'anchor': 'ASD can sometimes be detected at 18 months of age or younger. By age 2, a diagnosis by an experienced professional can be considered reliable.',
    },
    {
        'code': 'E73799F4D6',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả dữ liệu điều tra dịch tễ học tự kỷ ở trẻ từ 18 đến 30 tháng tuổi tại Việt Nam.',
        'anchor': 'autism spectrum disorder (ASD) amongst children aged 18 to 30 months in Vietnam.',
    },
    {
        'code': 'C19CECB3B5',
        'grade': 3,
        'rationale': 'Hướng dẫn chi tiết của CDC và AAP nêu rõ các mốc sàng lọc phát triển chung (9, 18, 30 tháng) và bắt buộc sàng lọc tự kỷ lúc 18 và 24 tháng tuổi.',
        'anchor': 'The American Academy of Pediatrics recommends that all children receive screening for developmental delays at their 9-, 18-, and 24- or 30-month well-child visits, with specific autism screenings at the 18- and 24-month well-child visits.',
    },
    {
        'code': '5AC6C422F7',
        'grade': 1,
        'rationale': 'Đoạn văn giải thích quy trình thực hiện bảng hỏi hoặc phỏng vấn của các công cụ sàng lọc ASD.',
        'anchor': 'Administration refers to undertaking the questionnaires or interviews provided by the ASD screening tools',
    },
    {
        'code': 'CC6D1EE4FA',
        'grade': 1,
        'rationale': 'Đoạn tổng quan nhấn mạnh tầm quan trọng của phát hiện sớm ASD và sự phát triển của các công cụ sàng lọc chính xác.',
        'anchor': 'The importance of early detection of ASD and subsequent early intervention is well documented.',
    },
    {
        'code': '1018DD04C9',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả việc chẩn đoán tự kỷ dựa trên theo dõi hành vi và sự phát triển của trẻ.',
        'anchor': 'Doctors look at the child\'s behavior and development to make a diagnosis.',
    },
    {
        'code': '15F7C33240',
        'grade': 0,
        'rationale': 'Đoạn văn về tỷ lệ ADHD và lo âu đồng mắc trong tự kỷ, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': 'C95BCB04A8',
        'grade': 0,
        'rationale': 'Đoạn văn ghi nhận phân công công việc của nhóm tác giả nghiên cứu, không chứa nội dung khoa học.',
        'anchor': '',
    },
    {
        'code': 'C895CD3C49',
        'grade': 2,
        'rationale': 'Bảng 1 tổng hợp các phương pháp sàng lọc sẵn có cho trẻ sơ sinh và trẻ nhỏ, nêu rõ độ tuổi mục tiêu của từng công cụ (M-CHAT 16-30 tháng, CHAT 18 tháng, ESAT 0-36 tháng).',
        'anchor': 'Summary of screening methods available for infants and children.',
    },
    {
        'code': '33882AAFF3',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả công cụ Q-CHAT được áp dụng để sàng lọc tự kỷ cho trẻ chập chững biết đi ở độ tuổi 18 đến 24 tháng.',
        'anchor': 'The Q-CHAT, one of the oldest methods of screening for autism, was developed by [29]',
    },
    {
        'code': '0CF7BB2372',
        'grade': 0,
        'rationale': 'Đoạn văn về nghiên cứu ăn uống chọn lọc và thiếu hụt dinh dưỡng ở 22 trẻ tự kỷ, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': '1576A4B61C',
        'grade': 0,
        'rationale': 'Đoạn văn về gánh nặng của ASD trên toàn cầu, không đề cập đến độ tuổi sàng lọc.',
        'anchor': '',
    },
    {
        'code': '2F7066BB89',
        'grade': 3,
        'rationale': 'Tài liệu hướng dẫn nêu rõ ASD có thể được chẩn đoán đáng tin cậy lúc 2 tuổi và việc sàng lọc phát triển cần được thực hiện thường xuyên ở các mốc tuổi sớm.',
        'anchor': 'ASD can usually be reliably diagnosed by the age of 2.',
    },
    {
        'code': '7E74182F81',
        'grade': 1,
        'rationale': 'Đoạn văn nêu những phê bình về các công cụ chẩn đoán như ADI-R và ADOS tốn nhiều thời gian, đòi hỏi chuyên gia cấp phép.',
        'anchor': 'However, they have been criticised for being time consuming, having long questionnaires and scoring methods',
    },
    {
        'code': '7BDA621825',
        'grade': 0,
        'rationale': 'Bảng số liệu không liên quan đến độ tuổi sàng lọc tự kỷ.',
        'anchor': '',
    },
    {
        'code': '8D096B7095',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các phương pháp sàng lọc kết hợp cho trẻ em, cung cấp chi tiết kỹ thuật.',
        'anchor': 'Summary of the hybrid Autism spectrum disorder (ASD) screening methods.',
    },
    {
        'code': 'ABDBECDD96',
        'grade': 1,
        'rationale': 'Đoạn văn nêu rõ các triệu chứng của tự kỷ trở nên rõ ràng và dễ nhận biết hơn ở trẻ từ 2 đến 3 tuổi, thúc đẩy việc phát triển các phương pháp sàng lọc sớm.',
        'anchor': 'The symptoms of autism are more visible and easy to identify in children two to three years of age.',
    },
    {
        'code': '6461F0C092',
        'grade': 1,
        'rationale': 'Đoạn văn bàn về độ nhạy của các công cụ sàng lọc ở nhóm người lớn và trẻ mới biết đi.',
        'anchor': 'showed a reduction in sensitivity for adults and toddlers',
    },
    {
        'code': 'A263DA6709',
        'grade': 1,
        'rationale': 'Đoạn văn hướng dẫn cha mẹ liên hệ hệ thống trường công lập khi trẻ từ 3 tuổi trở lên có mối lo ngại về phát triển.',
        'anchor': 'If your child is 3 years old or older, contact your local public school system.',
    },
    {
        'code': '3F5B7E81FA',
        'grade': 0,
        'rationale': 'Bảng nhân khẩu học của nhóm 24 người tham gia nghiên cứu giáo dục, không liên quan đến sàng lọc.',
        'anchor': '',
    },
    {
        'code': 'D23B635010',
        'grade': 1,
        'rationale': 'Đoạn văn nêu định nghĩa ASD và giới thiệu cuộc nghiên cứu dịch tễ học ở trẻ 18-30 tháng tuổi tại miền Bắc Việt Nam.',
        'anchor': 'investigated the prevalence of autism spectrum disorders and examined their relation to selected socio-demographic factors among children aged 18–30 months',
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
