import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_14.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_14'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q054.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q054':
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
        'code': 'A567A7D80E',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về quy trình tiếp cận dịch vụ và tiêu chí chuyển tuyến điều trị điều hòa cảm giác, không đề cập đến ưu tiên can thiệp tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': 'F3E7C010A6',
        'grade': 1,
        'rationale': 'Đoạn văn khuyến nghị nghiên cứu thêm về tính khả thi và hiệu quả của các can thiệp do cha mẹ làm trung gian từ xa cho trẻ tự kỷ sống ngoài đô thị.',
        'anchor': 'Further research into the feasibility, efficacy, and appropriateness of the methods of delivery for',
    },
    {
        'code': '3EBE3911BC',
        'grade': 0,
        'rationale': 'Phụ lục tóm tắt các mẹo tương tác cụ thể của khóa tập huấn người chăm sóc, không đề cập đến việc so sánh can thiệp tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': 'CD96696424',
        'grade': 1,
        'rationale': 'Đoạn văn ghi nhận ý kiến phụ huynh về lợi ích của việc cung cấp kiến thức nền tảng cho cha mẹ để hỗ trợ can thiệp cho trẻ.',
        'anchor': 'And the number of parents that say oh if only we had known this.',
    },
    {
        'code': '3A3B0BF9FE',
        'grade': 0,
        'rationale': 'Đoạn văn là phần giải thích đáp án bài tập tình huống về hành vi thách thức trong tài liệu tập huấn cha mẹ, không so sánh can thiệp tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': '9BD9686709',
        'grade': 1,
        'rationale': 'Đoạn văn nêu rằng các can thiệp cảm giác có thể do người chăm sóc hoặc thành viên nhóm thực hiện trong các môi trường tự nhiên như gia đình, cộng đồng và trường học.',
        'anchor': 'SBIs may be implemented by caregivers and other team members or accessed independently by the child',
    },
    {
        'code': '1C142A6214',
        'grade': 1,
        'rationale': 'Đoạn kết luận tổng quan khẳng định các can thiệp nuôi dạy con trong 3 năm đầu đời có hiệu quả cải thiện sự phát triển của trẻ và kỹ năng chăm sóc.',
        'anchor': 'Parenting interventions during the first 3 years of childhood are effective for improving ECD and caregiving.',
    },
    {
        'code': '8DCD038506',
        'grade': 0,
        'rationale': 'Trang bài tập hướng dẫn nối hành vi và mục tiêu phản ứng trong tài liệu tập huấn kỹ năng người chăm sóc, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '296E96428A',
        'grade': 0,
        'rationale': 'Bảng thống kê đặc điểm các nghiên cứu can thiệp nuôi dạy con, không thảo luận việc lựa chọn ưu tiên môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': '65258C986B',
        'grade': 1,
        'rationale': 'Đoạn văn mô tả nhận xét của giáo viên và phụ huynh về sự cải thiện hành vi và khả năng thích nghi của trẻ trong lớp học sau can thiệp.',
        'anchor': 'For some children, teachers had also commented that their confidence, skills and general behaviour had improved.',
    },
    {
        'code': '938A9D4D00',
        'grade': 1,
        'rationale': 'Hướng dẫn của WHO về các nền tảng triển khai can thiệp phát triển trẻ thơ qua y tế cơ sở và thăm khám tại nhà.',
        'anchor': 'In LMICs, community health worker and primary health care facilities were the platforms for implementation.',
    },
    {
        'code': 'F847B74588',
        'grade': 1,
        'rationale': 'Tài liệu hướng dẫn của WHO về các can thiệp học tập sớm nhằm nâng cao kiến thức, thái độ và kỹ năng của người chăm sóc tại gia đình.',
        'anchor': 'Early learning and development Interventions that enhance caregivers’ access, knowledge, attitudes, practices or skills',
    },
    {
        'code': '5C063B1D3C',
        'grade': 1,
        'rationale': 'Đoạn phân tích tổng hợp chỉ ra các can thiệp qua cha mẹ giúp cải thiện kiến thức và hành vi thực hành của cha mẹ.',
        'anchor': 'Second, we analyzed the impact of parenting interventions on parents themselves',
    },
    {
        'code': '1BFD822DBC',
        'grade': 0,
        'rationale': 'Mô tả bài tập thực hành tương tác tại nhà trong khóa tập huấn kỹ năng người chăm sóc, không so sánh với trường học.',
        'anchor': '',
    },
    {
        'code': 'D69D4702A2',
        'grade': 2,
        'rationale': 'Đoạn văn tổng quan phân loại địa điểm triển khai can thiệp: phần lớn được thực hiện trực tiếp tại lớp học phổ thông, trong khi một số can thiệp diễn ra tại nhà hoặc cơ sở mầm non.',
        'anchor': 'Most of the described interventions were implemented directly in mainstream classroom settings',
    },
    {
        'code': '5EB92E9C78',
        'grade': 1,
        'rationale': 'Đoạn trích ý kiến nhà trị liệu nhấn mạnh tầm quan trọng của việc chuyển giao kỹ năng để phụ huynh tiếp tục duy trì can thiệp trong sinh hoạt hằng ngày.',
        'anchor': 'You can carry out 30-odd sessions, but once that intervention finished it ’s finished, unless the parent and the child',
    },
    {
        'code': 'E66AB0CE45',
        'grade': 0,
        'rationale': 'Khuyến nghị ngắn của WHO về hỗ trợ sức khỏe tâm thần của người chăm sóc, không đề cập đến ưu tiên nhà hay trường.',
        'anchor': '',
    },
    {
        'code': '2448787093',
        'grade': 1,
        'rationale': 'Tài liệu tập huấn kỹ năng người chăm sóc của WHO về thúc đẩy hành vi tích cực và giảm các hành vi thách thức.',
        'anchor': 'Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging behaviours.',
    },
    {
        'code': '97380982B8',
        'grade': 1,
        'rationale': 'Đoạn văn phân loại các can thiệp nuôi dạy con theo thành phần chăm sóc đáp ứng trong các nghiên cứu thử nghiệm lâm sàng.',
        'anchor': 'Out of the total 102 interventions, 70 (69%) had some degree of a responsive caregiving component',
    },
    {
        'code': '2AD51DAC20',
        'grade': 0,
        'rationale': 'Bài tập tình huống về tương tác giữa mẹ và con trong tài liệu tập huấn kỹ năng người chăm sóc, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '6270EBF763',
        'grade': 1,
        'rationale': 'Tổng quan có hệ thống và phân tích gộp về 102 thử nghiệm ngẫu nhiên có đối chứng về các can thiệp nuôi dạy con trong 3 năm đầu đời.',
        'anchor': '- We conducted a systematic review and meta-analysis of 102 randomized controlled trials of parenting interventions',
    },
    {
        'code': '35C44C9657',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích hiệu quả của kích thích xúc giác áp lực sâu đối với chức năng hành vi, không thảo luận việc lựa chọn giữa nhà và trường.',
        'anchor': '',
    },
    {
        'code': '25386C582F',
        'grade': 0,
        'rationale': 'Ý kiến bình duyệt của chuyên gia yêu cầu tác giả thảo luận thêm về bối cảnh chương trình, không cung cấp bằng chứng hay kết luận về ưu tiên can thiệp.',
        'anchor': '',
    },
    {
        'code': '106E53AF8F',
        'grade': 0,
        'rationale': 'Đoạn trích phỏng vấn về việc trị liệu tại phòng khám so với thực tế, không đề cập đến ưu tiên can thiệp tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': '28DDB9038A',
        'grade': 0,
        'rationale': 'Đoạn văn hướng dẫn can thiệp về tính kén ăn ở trẻ tự kỷ, không liên quan đến câu hỏi so sánh trường học và tại nhà.',
        'anchor': '',
    },
    {
        'code': 'D06392E3F5',
        'grade': 0,
        'rationale': 'Bảng thống kê kết quả đo lường sự tham gia của cha mẹ qua trang web, không so sánh môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': 'D52EA62D51',
        'grade': 0,
        'rationale': 'Bảng trích xuất đặc điểm các nghiên cứu can thiệp, không có nội dung thảo luận so sánh nhà và trường.',
        'anchor': '',
    },
    {
        'code': 'FBEF5560C7',
        'grade': 2,
        'rationale': 'Đoạn văn phân tích các lợi thế của can thiệp do cha mẹ làm trung gian (PMIs) khi đưa can thiệp vào môi trường tự nhiên tại nhà, giúp khái quát hóa kỹ năng vào đời sống thực tế.',
        'anchor': 'PMIs are advantageous because they reduce the demands on children with ASD compared to behavioral approaches and bring treatment into a home and community setting',
    },
    {
        'code': '4D4078C351',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về việc tối ưu hóa thiết kế chương trình nuôi dạy con và ghi nhận hiệu quả lớn hơn ở các nước LMICs.',
        'anchor': 'More research is needed to determine how to optimize the design and delivery of parenting programs',
    },
    {
        'code': 'A9BB62EE86',
        'grade': 0,
        'rationale': 'Trang hướng dẫn thực hành kỹ năng người chăm sóc trong các hoạt động sinh hoạt gia đình, không so sánh với trường học.',
        'anchor': '',
    },
    {
        'code': 'C483851B3E',
        'grade': 1,
        'rationale': 'Đoạn văn phân loại đặc điểm các can thiệp sớm ở trẻ tự kỷ, nêu rõ các can thiệp NDBI diễn ra trong môi trường tự nhiên như gia đình hoặc cộng đồng.',
        'anchor': 'NDBIs are naturalistic in that they take place in environments and within routines that are already likely to occur in the child’s life',
    },
    {
        'code': '1CE1E62BB9',
        'grade': 0,
        'rationale': 'Đoạn mô tả đánh giá can thiệp cảm giác thông thường trong thử nghiệm SenITA, không liên quan đến việc chọn ưu tiên nhà hay trường.',
        'anchor': '',
    },
    {
        'code': '9F70CC7CBE',
        'grade': 1,
        'rationale': 'Khuyến nghị của WHO nhấn mạnh tất cả trẻ em cần được nhận chăm sóc đáp ứng trong 3 năm đầu đời và người chăm sóc cần được hỗ trợ.',
        'anchor': 'All infants and children should receive responsive care during the first 3 years of life; parents and other caregivers should be supported to provide responsive care.',
    },
    {
        'code': '5E7C872323',
        'grade': 1,
        'rationale': 'Đoạn ghi nhận nhận xét của phụ huynh và nhà trị liệu về sự gia tăng tự tin và tính độc lập của trẻ sau can thiệp.',
        'anchor': 'Increased confidence and independence It was commonly identified by both carers and therapists that children',
    },
    {
        'code': '54E5196097',
        'grade': 0,
        'rationale': 'Bảng tóm tắt các nghiên cứu về can thiệp dựa trên cảm giác, không thảo luận việc ưu tiên môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': '84EBBE3EFF',
        'grade': 1,
        'rationale': 'Đoạn tổng quan cung cấp bằng chứng sơ bộ về hiệu quả của các khóa tập huấn can thiệp do cha mẹ thực hiện cho các gia đình ở nông thôn.',
        'anchor': 'Findings of this systematic review provide preliminary evidence that parent-mediated intervention training',
    },
    {
        'code': '1C863D8CB8',
        'grade': 0,
        'rationale': 'Đoạn mô tả các trang thiết bị cảm giác được cho mượn hoặc dùng trong phòng trị liệu, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '1A7B4345C4',
        'grade': 1,
        'rationale': 'Đoạn tổng quan khẳng định đây là nghiên cứu tổng hợp lớn nhất về can thiệp nuôi dạy con trong giai đoạn đầu đời của trẻ.',
        'anchor': 'To the best of our knowledge, this is the largest and most comprehensive systematic review and meta-analysis that synthesized 102 parenting interventions',
    },
    {
        'code': '2F443DD8EE',
        'grade': 0,
        'rationale': 'Đoạn văn ngắn về thông tin hỗ trợ người chăm sóc, không có nội dung so sánh môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': 'AB42AA8AB7',
        'grade': 0,
        'rationale': 'Bảng trích xuất đặc điểm các nghiên cứu can thiệp, không có phân tích ưu tiên nhà hay trường.',
        'anchor': '',
    },
    {
        'code': 'D292CDA6C1',
        'grade': 0,
        'rationale': 'Bảng thống kê các nghiên cứu về tự kỷ tại Việt Nam, không chứa nội dung phân tích so sánh can thiệp tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': 'BCD1FA3EC9',
        'grade': 0,
        'rationale': 'Bài tập tình huống về dạy trẻ kỹ năng tự mặc quần áo trong tài liệu người chăm sóc, không đề cập đến ưu tiên nhà hay trường.',
        'anchor': '',
    },
    {
        'code': '4CE0A3E61B',
        'grade': 0,
        'rationale': 'Hướng dẫn lập kế hoạch từng bước dạy kỹ năng mới tại nhà cho trẻ, không so sánh với can thiệp tại trường.',
        'anchor': '',
    },
    {
        'code': '643227B07C',
        'grade': 1,
        'rationale': 'Đoạn văn thống kê các cấp độ triển khai can thiệp tại trường học (cấp độ trẻ, bạn bè, nhân viên và môi trường vật lý) để thúc đẩy hòa nhập.',
        'anchor': 'Twelve (21%) studies applied the intervention at child level; nine (16%) at peer level; seven (13%) at staff level; and four (7%) at physical environment level.',
    },
    {
        'code': 'F66FA514D1',
        'grade': 0,
        'rationale': 'Bảng thống kê đặc điểm các nghiên cứu can thiệp qua phụ huynh từ xa, không phân tích so sánh với trường học.',
        'anchor': '',
    },
    {
        'code': 'CCF6B7138E',
        'grade': 1,
        'rationale': 'Đoạn tổng quan khẳng định việc đưa phụ huynh tham gia và tập huấn cha mẹ mang lại sự tiến bộ trong nhiều lĩnh vực phát triển của trẻ tự kỷ.',
        'anchor': 'The clinical interventions for children, adolescents, and young adults with autism have demonstrated gains in different developmental domains where parent inclusion',
    },
    {
        'code': '75180AAA4D',
        'grade': 1,
        'rationale': 'Đoạn tổng quan nhấn mạnh các chương trình gắn kết và hỗ trợ phụ huynh mang lại lợi ích phổ quát cho cả trẻ và cha mẹ bất kể độ tuổi.',
        'anchor': 'our review suggests that parental engagement and support programs may indeed have universal benefits on child and parent outcomes irrespective of child age or the timing of introduction.',
    },
    {
        'code': '0048364D9B',
        'grade': 0,
        'rationale': 'Bài tập tình huống về tương tác đồ chơi giữa người chăm sóc và trẻ trong tài liệu tập huấn, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '041F10B080',
        'grade': 0,
        'rationale': 'Đoạn văn chia sẻ cảm xúc cô đơn của phụ huynh và các rào cản khi tiếp cận hỗ trợ chuyên môn, không so sánh môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': '7CB1CEB254',
        'grade': 0,
        'rationale': 'Đoạn văn báo cáo quy trình thu thập số liệu và tỷ lệ bỏ cuộc trong thử nghiệm can thiệp Câu chuyện Xã hội tại trường học.',
        'anchor': '',
    },
    {
        'code': 'E1A83E8208',
        'grade': 2,
        'rationale': 'Đoạn văn mô tả cấu trúc chương trình CST của WHO kết hợp giữa 9 buổi nhóm (có thể tổ chức tại cơ sở y tế, trường học) và 3 buổi thăm tại nhà của gia đình để tối ưu hiệu quả.',
        'anchor': 'The course is designed to be delivered in nine core group sessions for caregivers and three home visits. The group sessions can be provided at a health facility, school or other community-based facility.',
    },
    {
        'code': '36365D57D7',
        'grade': 0,
        'rationale': 'Bảng tổng hợp đặc điểm các nghiên cứu can thiệp cha mẹ, không có văn bản thảo luận ưu tiên môi trường can thiệp.',
        'anchor': '',
    },
    {
        'code': 'D64B104004',
        'grade': 0,
        'rationale': 'Đoạn phỏng vấn chuyên viên hoạt động trị liệu về quy trình đánh giá lâm sàng, không thảo luận việc lựa chọn ưu tiên tại nhà hay tại trường.',
        'anchor': '',
    },
    {
        'code': '71CF4F51AF',
        'grade': 0,
        'rationale': 'Hướng dẫn các bước hỗ trợ trẻ học kỹ năng tự phục vụ tại gia đình, không so sánh hay thảo luận ưu tiên với trường học.',
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
