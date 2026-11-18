import json
import sys

sys.path.insert(0, 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_20')
from verify_question import get_question_passages
passages = get_question_passages('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_20.jsonl', 'q047')

# Q047: Mốc phát triển của trẻ 9 tháng là gì?
# 38 candidates

annotations_q047_raw = [
    # 1. 3159083451 - Preemptive intervention clinical trial: infants between 9 and 15 months, SACS-R checklist
    {
        'annotation_code': '3159083451',
        'grade': 1,
        'rationale': 'Đoạn mô tả thử nghiệm lâm sàng cho trẻ từ 9 đến dưới 15 tháng có dấu hiệu tự kỷ sớm theo bảng kiểm SACS-R, chỉ liên quan gián tiếp đến phát triển ở mốc 9 tháng.',
        'target_span': 'the infant was between age 9 months and less than 15 months (corrected for prematurity) at eligibility screening',
        'confidence': 'high'
    },
    # 2. 5A82961F14 - Milestones by 6 Months: physical development
    {
        'annotation_code': '5A82961F14',
        'grade': 0,
        'rationale': 'Đoạn mô tả mốc phát triển vận động của trẻ 6 tháng tuổi, không phải mốc phát triển của trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 3. 01269360CE - Tips and activities for 9-month-old: crawl, scoot, roll, wave bye-bye, shake head no
    {
        'annotation_code': '01269360CE',
        'grade': 2,
        'rationale': 'Đoạn gợi ý các hoạt động hỗ trợ trẻ 9 tháng phát triển như khuyến khích bò, vẫy tay chào, lắc đầu; phản ánh các kỹ năng phát triển đặc trưng của mốc 9 tháng.',
        'target_span': 'Place toys on the ground or on a play mat a little out of reach and encourage your baby to crawl, scoot, or roll to get them.',
        'confidence': 'high'
    },
    # 4. F7118F7954 - Milestones by 30 Months: physical development
    {
        'annotation_code': 'F7118F7954',
        'grade': 0,
        'rationale': 'Đoạn mô tả mốc vận động của trẻ 30 tháng tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 5. 1782493E27 - Milestones by 3 Years: physical development
    {
        'annotation_code': '1782493E27',
        'grade': 0,
        'rationale': 'Đoạn mô tả mốc vận động của trẻ 3 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 6. 5889122F0F - Milestones by 30 Months: checklists
    {
        'annotation_code': '5889122F0F',
        'grade': 0,
        'rationale': 'Đoạn hướng dẫn kiểm tra mốc phát triển của trẻ 30 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 7. 688B5F8969 - Milestones by 2 Months: checklists
    {
        'annotation_code': '688B5F8969',
        'grade': 0,
        'rationale': 'Đoạn hướng dẫn kiểm tra mốc phát triển của trẻ 2 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 8. 6C17D99419 - Ayres sensory integration review for preschool children
    {
        'annotation_code': '6C17D99419',
        'grade': 0,
        'rationale': 'Đoạn báo cáo nghiên cứu về can thiệp tích hợp cảm giác ở trẻ mẫu giáo, không liên quan đến mốc phát triển trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 9. 0C92E51B2A - CDC Learn the Signs. Act Early. program overview
    {
        'annotation_code': '0C92E51B2A',
        'grade': 1,
        'rationale': 'Đoạn giới thiệu chương trình theo dõi mốc phát triển chung của CDC, cung cấp bối cảnh về công cụ theo dõi mốc phát triển.',
        'target_span': 'CDC\'s "Learn the Signs. Act Early." program aims to improve early identification of developmental delays and disabilities, such as ASD, by promoting early childhood developmental monitoring',
        'confidence': 'high'
    },
    # 10. 372562D51E - Developmental monitoring: information for families
    {
        'annotation_code': '372562D51E',
        'grade': 1,
        'rationale': 'Đoạn hướng dẫn cha mẹ theo dõi mốc phát triển và trao đổi với bác sĩ trong các buổi khám sức khỏe định kỳ.',
        'target_span': 'Explore CDC\'s Milestone Tracker app, milestone checklists, and other materials. Access these free tools and more to help you track your child\'s milestones.',
        'confidence': 'high'
    },
    # 11. E29161DD00 - Developmental monitoring definition
    {
        'annotation_code': 'E29161DD00',
        'grade': 1,
        'rationale': 'Đoạn định nghĩa mốc phát triển và quá trình theo dõi phát triển của trẻ em nói chung.',
        'target_span': 'Developmental monitoring involves observing how your child grows and whether your child meets the typical developmental milestones, or skills that most children reach by a certain age, in playing, learning, speaking, behaving, and moving.',
        'confidence': 'high'
    },
    # 12. 75BB3722AC - Resources for developmental monitoring and screening
    {
        'annotation_code': '75BB3722AC',
        'grade': 1,
        'rationale': 'Đoạn liệt kê các tài liệu và ứng dụng của CDC về mốc phát triển của trẻ em, là thông tin tài nguyên bối cảnh.',
        'target_span': '* CDC\'s Developmental Milestones',
        'confidence': 'high'
    },
    # 13. 95D3A77A4D - Milestones by 2 Years: checklists
    {
        'annotation_code': '95D3A77A4D',
        'grade': 0,
        'rationale': 'Đoạn hướng dẫn kiểm tra mốc phát triển cho trẻ 2 tuổi, không liên quan đến mốc phát triển trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 14. 6FACEC4CA3 - Milestones by 6 Months: checklists
    {
        'annotation_code': '6FACEC4CA3',
        'grade': 0,
        'rationale': 'Đoạn hướng dẫn kiểm tra mốc phát triển cho trẻ 6 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 15. 98439ADA04 - Milestones by 4 Months: checklists
    {
        'annotation_code': '98439ADA04',
        'grade': 0,
        'rationale': 'Đoạn hướng dẫn kiểm tra mốc phát triển cho trẻ 4 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 16. BFEB5081A5 - Tips and activities: baby-proof home for 9 months
    {
        'annotation_code': 'BFEB5081A5',
        'grade': 1,
        'rationale': 'Đoạn hướng dẫn phụ huynh giữ an toàn cho trẻ 9 tháng tuổi khi trẻ bắt đầu bám đứng, liên quan gián tiếp đến giai đoạn phát triển 9 tháng.',
        'target_span': 'Put your baby close to things that she can pull up on safely.',
        'confidence': 'high'
    },
    # 17. FD00C4FFCE - Concerned About Your Child\'s Development: milestone checklists
    {
        'annotation_code': 'FD00C4FFCE',
        'grade': 1,
        'rationale': 'Đoạn hướng dẫn sử dụng bảng kiểm mốc phát triển chung khi có lo ngại về phát triển của trẻ.',
        'target_span': 'Use CDC\'s Milestone Tracker app or fill out a milestone checklist to track your child\'s development.',
        'confidence': 'high'
    },
    # 18. BE9D6FD832 - Milestones by 3 Years: checklists
    {
        'annotation_code': 'BE9D6FD832',
        'grade': 0,
        'rationale': 'Đoạn về bảng kiểm mốc phát triển cho trẻ 3 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 19. 0E31BE6330 - More parenting tips and activities for 9-month-old (peek-a-boo, look for hidden toys)
    {
        'annotation_code': '0E31BE6330',
        'grade': 2,
        'rationale': 'Đoạn gợi ý các trò chơi và hoạt động phù hợp cho trẻ 9 tháng như chơi ú òa, tìm đồ vật bị giấu dưới chăn; phản ánh sự phát triển nhận thức và tương tác ở lứa tuổi này.',
        'target_span': 'Play a game that teaches your baby to look for things she sees you hide, such as a toy under a blanket.',
        'confidence': 'high'
    },
    # 20. 3B8B2AB17C - Definition of developmental milestones
    {
        'annotation_code': '3B8B2AB17C',
        'grade': 1,
        'rationale': 'Đoạn đưa ra định nghĩa chuẩn về mốc phát triển ở trẻ em (những điều mà 75% trẻ trở lên làm được ở độ tuổi nhất định).',
        'target_span': 'Developmental milestones are things most children (75% or more) can do by a certain age.',
        'confidence': 'high'
    },
    # 21. 6B02C76670 - Milestones by 15 Months: checklists
    {
        'annotation_code': '6B02C76670',
        'grade': 0,
        'rationale': 'Đoạn về bảng kiểm mốc phát triển cho trẻ 15 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 22. 6FC7A2CFE8 - Milestones by 1 Year: checklists
    {
        'annotation_code': '6FC7A2CFE8',
        'grade': 0,
        'rationale': 'Đoạn về bảng kiểm mốc phát triển cho trẻ 1 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 23. AA47BBC71A - Milestones by 3 Years: Language/Communication
    {
        'annotation_code': 'AA47BBC71A',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc ngôn ngữ và giao tiếp của trẻ 3 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 24. 8659A3F8E6 - Milestones by 2 Years: Movement/Physical Development
    {
        'annotation_code': '8659A3F8E6',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc vận động của trẻ 2 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 25. 481290A9E1 - Milestones by 9 Months: Social/Emotional
    {
        'annotation_code': '481290A9E1',
        'grade': 3,
        'rationale': 'Đoạn liệt kê trực tiếp và đầy đủ các mốc phát triển cảm xúc - xã hội mà hầu hết trẻ 9 tháng tuổi đạt được theo CDC.',
        'target_span': '* Is shy, clingy, or fearful around strangers\n\n* Shows several facial expressions, like happy, sad, angry, and surprised\n\n* Looks when you call her name',
        'confidence': 'high'
    },
    # 26. E99B68EEEC - Milestones by 9 Months: Movement/Physical Development
    {
        'annotation_code': 'E99B68EEEC',
        'grade': 3,
        'rationale': 'Đoạn liệt kê trực tiếp các mốc phát triển vận động thể chất chuẩn của trẻ 9 tháng tuổi (tự ngồi dậy, chuyển đồ chơi giữa 2 tay, cào thức ăn, ngồi vững).',
        'target_span': '* Gets to a sitting position by herself\n\n* Moves things from one hand to her other hand\n\n* Uses fingers to “rake” food towards himself\n\n* Sits without support',
        'confidence': 'high'
    },
    # 27. EAAC49B869 - Milestones by 3 Years: Cognitive
    {
        'annotation_code': 'EAAC49B869',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc nhận thức của trẻ 3 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 28. 62D58DCB4B - Milestones by 9 Months: What to know
    {
        'annotation_code': '62D58DCB4B',
        'grade': 2,
        'rationale': 'Đoạn giới thiệu về các mốc phát triển mà hầu hết trẻ đạt được khi 9 tháng tuổi và hướng dẫn theo dõi.',
        'target_span': 'Learn about the developmental milestones that most babies do by 9 months of age.',
        'confidence': 'high'
    },
    # 29. 20FBC4A5AB - Milestones by 4 Months: Movement
    {
        'annotation_code': '20FBC4A5AB',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc vận động của trẻ 4 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 30. 2702B08635 - Milestones by 2 Months: parenting tips
    {
        'annotation_code': '2702B08635',
        'grade': 0,
        'rationale': 'Đoạn gợi ý hoạt động cho trẻ 2 tháng tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 31. C0EB75EFCE - Milestones by 18 Months: checklists
    {
        'annotation_code': 'C0EB75EFCE',
        'grade': 0,
        'rationale': 'Đoạn về bảng kiểm mốc phát triển cho trẻ 18 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 32. 8009B99181 - Milestones by 1 Year: Movement
    {
        'annotation_code': '8009B99181',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc vận động của trẻ 1 tuổi, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 33. 83A56183AC - AAP recommends developmental screening at 9, 18, 30 months
    {
        'annotation_code': '83A56183AC',
        'grade': 2,
        'rationale': 'Đoạn nêu khuyến nghị của Viện Hàn lâm Nhi khoa Hoa Kỳ (AAP) về việc sàng lọc phát triển tổng quát cho trẻ tại mốc 9 tháng tuổi.',
        'target_span': 'The American Academy of Pediatrics recommends that children be screened for general development using standardized, validated tools at 9, 18, or 30 months',
        'confidence': 'high'
    },
    # 34. 286DBBD938 - Milestones by 9 Months: Language/Communication
    {
        'annotation_code': '286DBBD938',
        'grade': 3,
        'rationale': 'Đoạn liệt kê trực tiếp các mốc phát triển ngôn ngữ và giao tiếp của trẻ 9 tháng tuổi (phát ra nhiều âm thanh khác nhau như mamamama, giơ tay đòi bế).',
        'target_span': '* Makes a lot of different sounds like “mamamama” and “bababababa”\n\n* Lifts arms up to be picked up',
        'confidence': 'high'
    },
    # 35. 7D65B2F328 - Signs and symptoms of ASD: 9-month milestones mentioned
    {
        'annotation_code': '7D65B2F328',
        'grade': 2,
        'rationale': 'Đoạn nêu các dấu hiệu cảnh báo tự kỷ tại mốc 9 tháng (không phản ứng với tên gọi, không biểu lộ nét mặt), gián tiếp chỉ ra các mốc phát triển bình thường cần đạt ở 9 tháng.',
        'target_span': '* Does not respond to name by 9 months of age\n\n* Does not show facial expressions such as happy, sad, angry, and surprised by 9 months of age',
        'confidence': 'high'
    },
    # 36. 4C460A8628 - Milestones by 9 Months: checklists
    {
        'annotation_code': '4C460A8628',
        'grade': 2,
        'rationale': 'Đoạn hướng dẫn kiểm tra các mốc phát triển mà trẻ đạt được khi 9 tháng tuổi thông qua bảng kiểm của CDC.',
        'target_span': 'Check the milestones your baby has reached by 9 months by completing a checklist',
        'confidence': 'high'
    },
    # 37. E64E48BA55 - Milestones by 18 Months: Movement
    {
        'annotation_code': 'E64E48BA55',
        'grade': 0,
        'rationale': 'Đoạn liệt kê mốc vận động của trẻ 18 tháng, không liên quan đến trẻ 9 tháng.',
        'target_span': '',
        'confidence': 'high'
    },
    # 38. F823E4B63B - Milestones by 9 Months: Cognitive Milestones
    {
        'annotation_code': 'F823E4B63B',
        'grade': 3,
        'rationale': 'Đoạn liệt kê trực tiếp các mốc phát triển nhận thức của trẻ 9 tháng tuổi (tìm đồ vật bị rơi khỏi tầm mắt, đập hai vật vào nhau).',
        'target_span': '* Looks for objects when dropped out of sight (like his spoon or toy)\n\n* Bangs two things together',
        'confidence': 'high'
    },
]

# Check target_spans
errors = 0
annotations_q047 = []
for item in annotations_q047_raw:
    code = item['annotation_code']
    grade = item['grade']
    target_span = item['target_span']
    
    if grade != 0:
        if target_span not in passages[code]:
            print(f"ERROR: target span not in passage for {code}!")
            print(repr(target_span))
            errors += 1
    else:
        target_span = ""
        
    ann = {
        'annotation_code': code,
        'grade': grade,
        'rationale': item['rationale'],
        'evidence_span': target_span,
        'confidence': item['confidence'],
        'needs_review': False,
        'review_note': '',
        'annotation_type': 'ai_generated',
        'model': 'claude-sonnet-4-6',
        'prompt_version': 't2_4b_ai_v1'
    }
    annotations_q047.append(ann)

if errors == 0:
    outpath = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_20/q047.jsonl'
    with open(outpath, 'w', encoding='utf-8') as f:
        for ann in annotations_q047:
            f.write(json.dumps(ann, ensure_ascii=False) + '\n')
    print(f'Successfully wrote {len(annotations_q047)} annotations to q047.jsonl')
else:
    print(f'Cannot write: {errors} span errors.')
