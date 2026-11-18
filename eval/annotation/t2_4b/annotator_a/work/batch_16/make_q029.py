import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_16.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_16'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q029.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q029':
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
        'code': 'BB2EEAD92D',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về sự phát triển các rối loạn đồng mắc ở trẻ tự kỷ và so sánh cho thấy trẻ tự kỷ có biểu hiện rối loạn lo âu nhiều hơn so với trẻ ADHD.',
        'anchor': 'In the present study it was found that children with ASD exhibit more anxiety disorders compared to children with ADHD.',
    },
    {
        'code': '7323AAAC58',
        'grade': 2,
        'rationale': 'Đoạn phân tích số liệu thống kê về tỷ lệ trẻ tự kỷ có ít nhất một rối loạn tâm thần đồng mắc (COMORBID).',
        'anchor': 'COMORBID having at least one comorbid disorder',
    },
    {
        'code': 'E24FCB36DE',
        'grade': 3,
        'rationale': 'Bảng số liệu thống kê chi tiết tần suất các rối loạn tâm thần đồng mắc (rối loạn lo âu và ADHD) ở trẻ tự kỷ so với nhóm ADHD.',
        'anchor': 'Frequency of comorbid psychiatric disorders in children with ASD and children with ADHD',
    },
    {
        'code': '4E91E07F05',
        'grade': 2,
        'rationale': 'Bảng tổng hợp y văn các nghiên cứu đánh giá yếu tố dự đoán sớm về triệu chứng tự kỷ và lo âu ở trẻ em.',
        'anchor': 'Evaluate early-life predictors of mid-childhood ASD and anxiety symptoms',
    },
    {
        'code': 'A203263CB7',
        'grade': 3,
        'rationale': 'Kết quả phân tích tổng hợp khẳng định thanh thiếu niên tự kỷ có tỷ lệ đồng mắc bệnh lý tâm thần cao hơn, bao gồm ADHD và lo âu.',
        'anchor': 'adolescents with ASD have higher comorbidity for psychopathology, including ADHD',
    },
    {
        'code': 'CF498B95AF',
        'grade': 2,
        'rationale': 'Tóm tắt mục tiêu nghiên cứu nhằm xác định các rối loạn tâm thần đồng mắc ở trẻ tự kỷ so với trẻ ADHD trong thực hành lâm sàng.',
        'anchor': 'identify comorbid psychiatric disorders in children with autism spectrum',
    },
    {
        'code': '41AF38EDB4',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả đối tượng mẫu nghiên cứu và quy trình tuyển chọn tại trung tâm sức khỏe tâm thần, không cung cấp dữ liệu tỷ lệ đồng mắc.',
        'anchor': '',
    },
    {
        'code': '2DD1AFFC0B',
        'grade': 0,
        'rationale': 'Mô tả công cụ phỏng vấn chẩn đoán KID-SCID và độ tin cậy giữa các đánh giá viên, không trả lời câu hỏi.',
        'anchor': '',
    },
    {
        'code': 'E482AF8BDE',
        'grade': 3,
        'rationale': 'Đoạn văn khẳng định ở các cá nhân có ASD, tần suất lo âu cao được phát hiện do sự căng thẳng gắn liền với tương tác xã hội và các khiếm khuyết giao tiếp.',
        'anchor': 'In individuals with ASD, a high frequency of anxiety is detected due to the stress and anxiety associated with social',
    },
    {
        'code': '742512AC30',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu dịch tễ học trực tiếp: trẻ em và thanh thiếu niên tự kỷ có tỷ lệ triệu chứng ADHD rất cao (16–85%) và có sự trùng lặp triệu chứng rõ rệt.',
        'anchor': 'Children and adolescents with ASD have shown high rates of ADHD symptoms (16–85%)',
    },
    {
        'code': '73478DD561',
        'grade': 3,
        'rationale': 'Đoạn văn báo cáo số liệu thực nghiệm: 57,5% trẻ tự kỷ có ít nhất một rối loạn đồng mắc, trong đó rối loạn lo âu chiếm 42,5% và ADHD chiếm 30%.',
        'anchor': 'In the ASD sample, twenty-three chi',
    },
    {
        'code': '2452FB4325',
        'grade': 3,
        'rationale': 'Đoạn văn nêu rõ trẻ tự kỷ thường trải qua lo âu chia ly, lo âu xã hội và các triệu chứng lo âu lan tỏa, đồng thời thảo luận về sự chồng chéo với ADHD.',
        'anchor': 'Youths with ASD often experience separation anxiety, social anxiety, and generalized anxiety symptom',
    },
    {
        'code': 'D982E5F83F',
        'grade': 2,
        'rationale': 'Đoạn phân tích về tỷ lệ đồng mắc của ADHD với các rối loạn tâm thần khác và sự xuất hiện đồng thời trong các rối loạn phát triển thần kinh.',
        'anchor': 'Research also shows a prevalence of ADHD in certain psychiatric comorbidities. It is especially high',
    },
    {
        'code': 'E774994E9E',
        'grade': 0,
        'rationale': 'Đoạn mô tả phương pháp tìm kiếm tài liệu trên các cơ sở dữ liệu PubMed, Scopus, không có số liệu tỷ lệ đồng mắc.',
        'anchor': '',
    },
    {
        'code': '2D0537309E',
        'grade': 2,
        'rationale': 'Đoạn giới thiệu nhấn mạnh tự kỷ là rối loạn phức tạp và thường đi kèm các bệnh lý tâm thần đồng mắc như ADHD và lo âu.',
        'anchor': 'Autism spectrum disorder (ASD) is a complex neurodevelopmental condition that manifests in early chi',
    },
    {
        'code': '584719F0CC',
        'grade': 2,
        'rationale': 'Đoạn thảo luận phân tích các phân nhóm tự kỷ có và không có đồng mắc ADHD và lo âu đối với chức năng thích ứng.',
        'anchor': 'When looking at ASD with and without specific comorbidities (ADHD and/or anxiety), the subgroup of A',
    },
    {
        'code': '048877205C',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu nghiên cứu cụ thể: tỷ lệ triệu chứng ADHD và lo âu ở mức độ lâm sàng ở trẻ tự kỷ lần lượt là 62,7% và 44,6%, cao hơn đáng kể so với nhóm trẻ bình thường.',
        'anchor': 'The rate of clinically elevated ADHD and anxiety symptoms in ASD was 62.7 and 44.6%',
    },
    {
        'code': 'BB9D0DD4B8',
        'grade': 2,
        'rationale': 'Đoạn phân tích so sánh mức độ lo âu ở trẻ em có chẩn đoán ADHD và tự kỷ trong các bối cảnh lâm sàng.',
        'anchor': 'This study is unique in that it aligns with our hypothesis that children with ADHD face higher level',
    },
    {
        'code': 'DA978FCF4B',
        'grade': 2,
        'rationale': 'Đoạn tổng quan khẳng định trẻ em mắc ADHD hoặc tự kỷ phải đối mặt với mức độ lo âu cao và các rối loạn tâm thần kèm theo.',
        'anchor': 'Children with attention deficit hyperactivity disorder (ADHD) or autism spectrum disorder (ASD) indi',
    },
    {
        'code': '3A5628FED7',
        'grade': 1,
        'rationale': 'Đoạn văn phân loại các rối loạn tâm thần ở trẻ em thành nhóm nội hóa và ngoại hóa, cung cấp bối cảnh phân loại bệnh đồng mắc.',
        'anchor': 'Child psychiatric disorders can be roughly divided into two main groups: internalizing and externali',
    },
    {
        'code': 'B8F3E76DCD',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ ADHD là một rối loạn đồng mắc thần kinh và phát triển phổ biến thường gặp ở trẻ tự kỷ.',
        'anchor': 'Attention deficit hyperactivity disorder (ADHD) is a common neurological, and developmental comorbid',
    },
    {
        'code': 'D6D9B5A19B',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả ngưỡng điểm T-score trong thang đo Conners và sự tương quan giữa các bảng hỏi của cha mẹ và giáo viên, không nêu tỷ lệ đồng mắc.',
        'anchor': '',
    },
    {
        'code': 'C9615A7C06',
        'grade': 3,
        'rationale': 'Đoạn văn khẳng định lo âu và ADHD là một trong những tình trạng tâm thần thường gặp nhất có tần suất gia tăng cao ở người tự kỷ.',
        'anchor': 'Among psychiatric conditions commonly noted to have elevated frequencies in persons with ASD are anx',
    },
    {
        'code': '7CE592312E',
        'grade': 2,
        'rationale': 'Đoạn văn nêu rõ mục tiêu và giả thuyết nghiên cứu rằng các triệu chứng ADHD và lo âu gia tăng trên lâm sàng thường xuyên xảy ra ở trẻ tự kỷ.',
        'anchor': 'evaluate the frequency of ADHD and anxiety symptoms in the participants diagnosed with ASD',
    },
    {
        'code': '6DD49FF898',
        'grade': 2,
        'rationale': 'Phần kết luận tổng quan khẳng định mối liên hệ mật thiết giữa lo âu và các rối loạn tâm thần đồng mắc ở người tự kỷ và ADHD.',
        'anchor': 'evaluate the possible linkage between anxiety and psychiatric comorbidities in individua',
    },
    {
        'code': 'BE196797A7',
        'grade': 1,
        'rationale': 'Bảng tương quan giữa tình trạng đồng mắc với độ tuổi và chỉ số IQ ở trẻ tự kỷ và ADHD.',
        'anchor': 'Correlations between comorbidity and age',
    },
    {
        'code': '78BACFAD43',
        'grade': 3,
        'rationale': 'Đoạn văn cung cấp số liệu trực tiếp: lo âu là một trong những vấn đề tâm thần phổ biến nhất ở tự kỷ, với tỷ lệ khó khăn lo âu từ 11–84% và tới 40% được chẩn đoán rối loạn lo âu.',
        'anchor': 'higher frequencies of anxiety difficulties (11–84%) have been reported in children with ASD',
    },
    {
        'code': 'D6CD7727A2',
        'grade': 2,
        'rationale': 'Đoạn thảo luận tổng quan tài liệu về mức độ lo âu và các bệnh tâm thần đồng mắc ở trẻ em mắc ADHD, ASD và cả hai bệnh.',
        'anchor': 'We conducted a literature review on the differing levels of anxiety and psychiatric comorbidities in children with ADHD, ASD',
    },
    {
        'code': '2C55E77A98',
        'grade': 2,
        'rationale': 'Đoạn phân tích tỷ lệ lo âu đồng mắc và chứng phiền muộn giới ở thanh thiếu niên có ASD và ADHD.',
        'anchor': 'Children with ADHD face higher levels of anxiety than others with estimated rates of co-occurring anxiety being between',
    },
    {
        'code': '26B1EBD4A3',
        'grade': 2,
        'rationale': 'Đoạn thảo luận lưu ý đây là nghiên cứu đầu tiên khảo sát tỷ lệ rối loạn tâm thần ở trẻ tự kỷ và so sánh với nhóm ADHD.',
        'anchor': 'first study to examine the rate of psychiatric disorders in children with ASD and',
    },
    {
        'code': 'EA2098FDDE',
        'grade': 2,
        'rationale': 'Đoạn thảo luận phân tích rằng trẻ em mắc tự kỷ và ADHD đều có tỷ lệ đồng mắc các rối loạn tâm thần rất cao tương đương nhau.',
        'anchor': 'children with ASD and ADHD do not differ with respect to their overall comorbidity rate',
    },
    {
        'code': '499BD59542',
        'grade': 2,
        'rationale': 'Đoạn văn thảo luận về ý nghĩa lâm sàng của việc chẩn đoán sớm các bệnh đồng mắc ADHD và lo âu ở trẻ tự kỷ để giảm thiểu tác động tiêu cực đến chức năng.',
        'anchor': 'ADHD and anxiety symptoms are related to poore',
    },
    {
        'code': '8DCDBA5677',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các nghiên cứu so sánh kỹ năng vận động và mức độ lo âu đồng mắc giữa các nhóm trẻ ADHD và tự kỷ.',
        'anchor': 'Compare movement and locomotor skills between those with ADHD and ASD',
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

