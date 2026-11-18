import json

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_08.jsonl'
returned_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_08/q048.jsonl'

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q048':
            content_map[obj['annotation_code']] = obj['content']

def extract_span(code, anchor, max_len=200):
    c = content_map[code]
    idx = c.find(anchor)
    if idx == -1:
        raise ValueError(f"Anchor '{anchor}' not found in {code}")
    # slice up to max_len chars
    sub = c[idx:idx+max_len]
    # prefer stopping at newline or period if possible
    if '\n' in sub:
        sub = sub.split('\n')[0].strip()
    return sub

raw_annotations = [
    {
        'annotation_code': 'F7FF3670F0',
        'grade': 0,
        'rationale': 'Đoạn văn hướng dẫn liên hệ trường học khi trẻ từ 3 tuổi trở lên, không nói về các biện pháp cha mẹ có thể làm trong 3 năm đầu đời.',
        'anchor': '',
    },
    {
        'annotation_code': '002801D87E',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả phương pháp tìm kiếm tài liệu của bài tổng quan về các can thiệp nuôi dạy trẻ trong 3 năm đầu đời, cung cấp bối cảnh phương pháp luận.',
        'anchor': 'We included randomized controlled trials',
    },
    {
        'annotation_code': '334094E361',
        'grade': 1,
        'rationale': 'Bảng chi tiết các nghiên cứu can thiệp của cha mẹ (chăm sóc đáp ứng) đối với trẻ sơ sinh và trẻ nhỏ, mang tính bối cảnh nghiên cứu cụ thể.',
        'anchor': 'An intervention targeting preterm, low birth weight infants',
    },
    {
        'annotation_code': '91F3941D02',
        'grade': 3,
        'rationale': 'Đoạn văn hướng dẫn cụ thể cách cha mẹ trao quyền lựa chọn cho trẻ trong các sinh hoạt hàng ngày nhằm tạo động lực và thúc đẩy trẻ tham gia tích cực.',
        'anchor': 'Good choices are tasks that can be done',
    },
    {
        'annotation_code': 'B86D0C8569',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp các hành động cụ thể, thiết thực cha mẹ có thể làm để phát triển ngôn ngữ và nhận thức: đọc sách, chơi đếm số, nói câu dài hơn và cho trẻ giúp việc nhà.',
        'anchor': 'Read with your child.',
    },
    {
        'annotation_code': '0390C89F9F',
        'grade': 3,
        'rationale': 'Đoạn văn hướng dẫn cha mẹ với vai trò người thầy đầu tiên thực hiện các tương tác tích cực để giúp bé phát triển trí não và học tập.',
        'anchor': 'As your baby\'s first teacher, you can help his or her learning and brain development.',
    },
    {
        'annotation_code': '5C066C9D56',
        'grade': 2,
        'rationale': 'Đoạn văn hướng dẫn hành động rõ ràng cho cha mẹ khi trẻ dưới 3 tuổi có nguy cơ hoặc dấu hiệu chậm phát triển: liên hệ hệ thống can thiệp sớm.',
        'anchor': 'If your child is younger than 3 years old, contact your local early intervention system',
    },
    {
        'annotation_code': 'FA7E52B7CA',
        'grade': 3,
        'rationale': 'Khuyến nghị chính thức của WHO nêu rõ tất cả trẻ em cần được chăm sóc đáp ứng (responsive care) trong 3 năm đầu đời và cha mẹ cần được hỗ trợ để thực hiện điều này.',
        'anchor': 'All infants and children should receive responsive care during the first 3 years of life',
    },
    {
        'annotation_code': 'A406CC5EFF',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các nghiên cứu về chương trình can thiệp nuôi dạy con trong những năm đầu đời, cung cấp dữ liệu nghiên cứu chi tiết.',
        'anchor': 'rural China',
    },
    {
        'annotation_code': 'A77C5AB7E9',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về tác động của các can thiệp nuôi dạy con đối với kỹ năng của cha mẹ và nhấn mạnh tầm quan trọng của sự tham gia của người cha trong sự phát triển sớm của trẻ.',
        'anchor': 'fathers are critically important for ECD',
    },
    {
        'annotation_code': 'E59FA8F9D6',
        'grade': 3,
        'rationale': 'Đoạn văn phân tích hiệu quả của việc chăm sóc đáp ứng (responsive caregiving), chỉ ra rằng việc cha mẹ nhận biết, thấu hiểu và đáp ứng kịp thời các tín hiệu của trẻ mang lại hiệu quả phát triển vượt trội.',
        'anchor': 'Regarding intervention content, we found that those with responsive caregiving components',
    },
    {
        'annotation_code': 'B2BAC52371',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích tầm quan trọng của các biện pháp thúc đẩy trong 3 năm đầu đời và cách thức các can thiệp hỗ trợ cha mẹ cung cấp sự chăm sóc nuôi dưỡng (nurturing care).',
        'anchor': 'Promotive interventions are particularly important in the first 3 years of life',
    },
    {
        'annotation_code': '33938A1826',
        'grade': 1,
        'rationale': 'Đoạn văn liệt kê 6 lĩnh vực phát triển đầu đời (nhận thức, ngôn ngữ, vận động, cảm xúc-xã hội, hành vi, gắn bó) được đánh giá trong các can thiệp của cha mẹ.',
        'anchor': 'The primary outcomes were 6 domains of ECD',
    },
    {
        'annotation_code': '0C7F1B7564',
        'grade': 1,
        'rationale': 'Bảng thống kê các nghiên cứu can thiệp nuôi dạy con ở độ tuổi nhỏ nhằm cải thiện nhận thức và ngôn ngữ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'annotation_code': 'CB3AE1F129',
        'grade': 3,
        'rationale': 'Đoạn văn tổng kết các loại hình can thiệp cha mẹ mang lại lợi ích lớn trong những năm đầu đời, cụ thể là chăm sóc đáp ứng, đọc sách cùng con, chơi đùa và tương tác tích cực.',
        'anchor': 'These different types of parenting interventions have consistently shown benefits across a wide age range of children, and especially during early childhood',
    },
    {
        'annotation_code': '386CC13598',
        'grade': 1,
        'rationale': 'Đoạn văn giới thiệu về các can thiệp do cha mẹ làm trung gian cho trẻ tự kỷ trong giai đoạn sớm nhằm cải thiện kỹ năng giao tiếp và xã hội.',
        'anchor': 'Autism spectrum disorder (ASD) is a neurodevelopmental disorder characterized by early-onset difficulties in social interaction',
    },
    {
        'annotation_code': 'F6FDA54FC5',
        'grade': 0,
        'rationale': 'Đoạn văn về rủi ro đuối nước và sự chuẩn bị của cha mẹ khi tham gia các hoạt động dưới nước, không liên quan đến thúc đẩy phát triển nói chung trong 3 năm đầu.',
        'anchor': '',
    },
    {
        'annotation_code': '655208BAB5',
        'grade': 1,
        'rationale': 'Đoạn văn nêu câu hỏi nghiên cứu của nhóm chuyên gia về hiệu quả của việc kết hợp chăm sóc và dinh dưỡng trong 3 năm đầu đời.',
        'anchor': 'What is the effectiveness of integrated caregiving and nutrition interventions in the first 3 years of life',
    },
    {
        'annotation_code': '6199937290',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu can thiệp cha mẹ thúc đẩy phát triển trẻ em thông qua giáo dục và hướng dẫn thực hành.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'annotation_code': '590FFA4C72',
        'grade': 1,
        'rationale': 'Bảng thống kê các can thiệp nuôi dạy con giai đoạn sớm hỗ trợ tương tác và kỹ năng nhận thức ở trẻ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'annotation_code': 'AEC5B23821',
        'grade': 3,
        'rationale': 'Đoạn văn khẳng định các can thiệp nuôi dạy con trong 3 năm đầu đời có hiệu quả cao, đồng thời nêu rõ chăm sóc đáp ứng và tạo cơ hội học tập sớm thúc đẩy sự phát triển trí não.',
        'anchor': 'Parenting interventions during the first 3 years of childhood are effective for improving ECD and caregiving.',
    },
    {
        'annotation_code': 'D3EBB4646D',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp bằng chứng cho thấy các chương trình kết hợp chăm sóc đáp ứng với học tập sớm trong 3 năm đầu đời đem lại lợi ích lớn nhất cho nhận thức, ngôn ngữ và vận động của trẻ.',
        'anchor': 'Parenting interventions for children during the first 3 years of life are effective for improving ECD outcomes',
    },
    {
        'annotation_code': '4AD9D46708',
        'grade': 1,
        'rationale': 'Bảng thống kê các nghiên cứu can thiệp cha mẹ nhằm nâng cao sự gắn bó và kích thích tương tác mẹ-con.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'annotation_code': 'C003812206',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận tổng hợp từ 102 thử nghiệm can thiệp của cha mẹ trong 3 năm đầu, chỉ ra các yếu tố giúp nâng cao hiệu quả nuôi dạy và phát triển trẻ.',
        'anchor': 'largest and most comprehensive systematic review and meta-analysis that synthesized 102 parenting interventions',
    },
    {
        'annotation_code': '27BFB351DE',
        'grade': 3,
        'rationale': 'Đoạn văn đưa ra chỉ dẫn cụ thể cho cha mẹ về cách xây dựng các hoạt động chơi phù hợp trình độ của trẻ, chia nhỏ các bước và đi theo sự dẫn dắt của trẻ để thúc đẩy phát triển.',
        'anchor': 'Begin with play routines at the right level for your child.',
    },
    {
        'annotation_code': '9D332937F3',
        'grade': 1,
        'rationale': 'Đoạn văn liệt kê các mốc phát triển vận động tinh và tự phục vụ ở mốc 3 tuổi, mang tính tham khảo để theo dõi hơn là hành động của cha mẹ.',
        'anchor': 'Strings items together, like large beads or macaroni',
    },
    {
        'annotation_code': '2C50B771D1',
        'grade': 2,
        'rationale': 'Đoạn văn giới thiệu chương trình tập huấn kỹ năng cho người chăm sóc (CST của WHO) hướng dẫn cha mẹ cách tương tác, chơi và giao tiếp với trẻ chậm phát triển.',
        'anchor': 'Caregiver skills training for families of children with developmental delays or disabilities (CST) package was developed',
    },
    {
        'annotation_code': 'DFC5BAE2A7',
        'grade': 2,
        'rationale': 'Đoạn văn định nghĩa rõ ràng các khái niệm then chốt như sự gắn bó (attachment) giữa trẻ sơ sinh và người lớn, một nền tảng cảm xúc xã hội quan trọng trong giai đoạn đầu đời.',
        'anchor': 'Attachment An emotional bond between an infant and one or more adults.',
    },
    {
        'annotation_code': 'B0A971270E',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các quyết định thiết kế chương trình nuôi dạy trẻ (thời lượng, hình thức, bối cảnh) cho các nhà hoạch định chính sách.',
        'anchor': 'Decisions regarding program duration, delivery modality, and setting',
    },
    {
        'annotation_code': '09D23E928C',
        'grade': 2,
        'rationale': 'Đoạn văn giải thích lợi ích của việc đào tạo cha mẹ thành người đồng trị liệu để thực hiện các can thiệp tự nhiên tại nhà giúp trẻ tiến bộ trong nhiều lĩnh vực.',
        'anchor': 'clinical interventions for children, adolescents, and young adults with autism have demonstrated gains in different developmental domains where parent inclusion',
    },
    {
        'annotation_code': '05BB35FD8F',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp lời khuyên cụ thể cho cha mẹ về cách thúc đẩy học tập và phát triển trí não cho bé thông qua các hoạt động an toàn hàng ngày.',
        'anchor': 'As your baby\'s first teacher, you can help his or her learning and brain development.',
    },
    {
        'annotation_code': 'DAC110BDDA',
        'grade': 3,
        'rationale': 'Tóm tắt kết quả phân tích tổng hợp 102 thử nghiệm cho thấy các can thiệp của cha mẹ trong 3 năm đầu đời cải thiện nhận thức, ngôn ngữ, vận động và cảm xúc-xã hội, đặc biệt khi kết hợp chăm sóc đáp ứng và học tập sớm.',
        'anchor': 'parenting interventions for children during the first 3 years of life that were implemented across a total of 33 countries.',
    },
    {
        'annotation_code': '7CE5209A6C',
        'grade': 2,
        'rationale': 'Đoạn văn nêu kết luận về hiệu quả bao quát của các can thiệp nuôi dạy con trong 3 năm đầu đời và kêu gọi mở rộng quy mô các chương trình này toàn cầu.',
        'anchor': 'largest and most comprehensive global systematic review and meta-analysis that demonstrates the effectiveness of parenting interventions during the first 3 years of life',
    },
    {
        'annotation_code': 'CE1C85951E',
        'grade': 1,
        'rationale': 'Đoạn văn cung cấp bằng chứng sơ bộ về việc tập huấn cho cha mẹ ở vùng nông thôn để hỗ trợ phát triển hành vi xã hội và giao tiếp của trẻ tự kỷ.',
        'anchor': 'parent-mediated intervention training for families living in nonurban areas can assist in improving social behavior',
    },
    {
        'annotation_code': '62589DB766',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu can thiệp đọc sách đối thoại giữa cha mẹ và con để thúc đẩy phát triển ngôn ngữ.',
        'anchor': 'A parent–child dialogic reading program',
    },
    {
        'annotation_code': 'E6D842EBF2',
        'grade': 1,
        'rationale': 'Đoạn văn nêu câu hỏi nghiên cứu về hiệu quả của các can thiệp chăm sóc thúc đẩy học tập sớm trong 3 năm đầu đời.',
        'anchor': 'What is the effectiveness of caregiving interventions that promote early learning in the first 3 years of life on ECD?',
    },
    {
        'annotation_code': '5BF854FC54',
        'grade': 3,
        'rationale': 'Đoạn văn hướng dẫn thực tế cho cha mẹ các hoạt động thúc đẩy phát triển như khuyến khích chơi tự do, trò chuyện và cùng giải quyết vấn đề.',
        'anchor': 'As your child\'s first teacher, you can help his or her learning and brain development.',
    },
    {
        'annotation_code': 'EE2D02C4A1',
        'grade': 1,
        'rationale': 'Đoạn văn tóm tắt ngắn về việc tìm hiểu mốc phát triển và các gợi ý hoạt động cho trẻ 3 tuổi, mang tính định hướng ban đầu.',
        'anchor': 'Find tips and activities you can do for your 3-year-old.',
    },
    {
        'annotation_code': 'BDAEFBB18F',
        'grade': 3,
        'rationale': 'Đoạn văn hướng dẫn cụ thể cách cha mẹ hỗ trợ trẻ phát triển kỹ năng giải quyết vấn đề, tương tác xã hội và học hỏi từ những năm đầu.',
        'anchor': 'As your child\'s first teacher, you can help his or her learning and brain development.',
    },
    {
        'annotation_code': '73904A68D7',
        'grade': 1,
        'rationale': 'Đoạn văn nêu các câu hỏi nghiên cứu định hướng chính sách của WHO liên quan đến can thiệp chăm sóc đáp ứng trong những năm đầu đời.',
        'anchor': 'What is the effectiveness of responsive caregiving interventions in the first 3 years of life',
    },
    {
        'annotation_code': '5DF94943C8',
        'grade': 1,
        'rationale': 'Bảng thống kê nghiên cứu can thiệp thăm khám tại nhà nhằm cung cấp hướng dẫn và hỗ trợ cha mẹ nuôi dạy trẻ.',
        'anchor': '| Author, Year Country | Intervention Description | Intervention Includes Responsive Caregiving',
    },
    {
        'annotation_code': '16A388D235',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bài học bơi cho trẻ tự kỷ và cách thích ứng với thách thức giao tiếp, không liên quan trực tiếp đến thúc đẩy phát triển toàn diện trong 3 năm đầu.',
        'anchor': '',
    },
    {
        'annotation_code': 'B510DF9E51',
        'grade': 3,
        'rationale': 'Đoạn văn hướng dẫn thực tế cha mẹ các hoạt động tương tác ngôn ngữ và chơi đùa hàng ngày để giúp phát triển trí não cho trẻ.',
        'anchor': 'As your child\'s first teacher, you can help his or her learning and brain development.',
    },
    {
        'annotation_code': 'E6264105E3',
        'grade': 1,
        'rationale': 'Đoạn văn liệt kê các mốc phát triển ngôn ngữ ở trẻ 3 tuổi, mang tính chất chỉ dấu theo dõi hơn là hành động can thiệp của cha mẹ.',
        'anchor': 'Talks with you in conversation using at least two back-and-forth exchanges',
    },
    {
        'annotation_code': '88371F5229',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về nghiên cứu tập huấn can thiệp từ xa do cha mẹ thực hiện cho trẻ em khuyết tật phát triển.',
        'anchor': 'This systematic review provides preliminary evidence on the effectiveness of remotely delivered parent-mediated intervention training.',
    }
]

annotations = []
errors = []

for r in raw_annotations:
    code = r['annotation_code']
    grade = r['grade']
    rat = r['rationale']
    anchor = r['anchor']
    
    if grade == 0:
        span = ''
    else:
        try:
            span = extract_span(code, anchor)
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
