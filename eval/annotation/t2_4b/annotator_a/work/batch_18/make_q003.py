import json
import os

batch_path = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_18.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_18'
os.makedirs(returned_dir, exist_ok=True)
returned_path = os.path.join(returned_dir, 'q003.jsonl')

content_map = {}
with open(batch_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line.strip())
        if obj.get('question_id') == 'q003':
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
        'code': '46AFD0C279',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các yếu tố nguy cơ làm tăng khả năng mắc động kinh ở trẻ tự kỷ, không nói về yếu tố gây ra bệnh tự kỷ.',
        'anchor': '',
    },
    {
        'code': '5D4403E721',
        'grade': 0,
        'rationale': 'Đoạn văn nghiên cứu về triệu chứng tiêu hóa và hệ vi sinh đường ruột ở trẻ tự kỷ, không thảo luận về yếu tố nguy cơ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'ABD1FF15FF',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các bệnh tâm thần đồng mắc và lo âu ở thanh thiếu niên tự kỷ, không nói về nguyên nhân gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '4937F3E77B',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về điểm cắt thuật toán phát hiện nguy cơ tự kỷ trong đánh giá tâm lý, không phân tích nguyên nhân hay yếu tố nguy cơ sinh học/môi trường.',
        'anchor': '',
    },
    {
        'code': '463472DCAA',
        'grade': 0,
        'rationale': 'Đoạn văn giới thiệu về các công cụ sàng lọc và chẩn đoán tự kỷ, không đề cập đến yếu tố nguy cơ.',
        'anchor': '',
    },
    {
        'code': '16A12AAFBA',
        'grade': 0,
        'rationale': 'Đoạn văn mô tả tiêu chí điểm số AOSI xác định hành vi nguy cơ tự kỷ ở trẻ 12 tháng tuổi trong thử nghiệm can thiệp sớm, không thảo luận yếu tố nguyên nhân.',
        'anchor': '',
    },
    {
        'code': '76843C83AB',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về các triệu chứng lo âu và ADHD đồng mắc ở trẻ tự kỷ, không đề cập đến yếu tố nguy cơ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '5C74EC53D0',
        'grade': 0,
        'rationale': 'Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '77270F6107',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích nguy cơ mắc bệnh chuyển hóa tim mạch ở người tự kỷ, không thảo luận về yếu tố gây ra tự kỷ.',
        'anchor': '',
    },
    {
        'code': '194EA8D361',
        'grade': 2,
        'rationale': 'Đoạn văn tổng quan các nghiên cứu tại Việt Nam xác định nguyên nhân tự kỷ, nhấn mạnh mối liên hệ giữa phơi nhiễm dioxin chu sinh và các hành vi tự kỷ.',
        'anchor': 'A recurrent theme and narrative in the review was identifying causes of (and factors associated with) autism',
    },
    {
        'code': '93F5871761',
        'grade': 3,
        'rationale': 'Tài liệu giải thích trực tiếp các yếu tố làm tăng nguy cơ phát triển tự kỷ bao gồm: có anh chị em mắc ASD, cha mẹ lớn tuổi, các tình trạng di truyền (Down, Fragile X), cân nặng khi sinh rất thấp.',
        'anchor': 'Researchers do not know the primary causes of ASD, but studies suggest that a person’s genes and asp',
    },
    {
        'code': '6E2D8FCA3E',
        'grade': 2,
        'rationale': 'Đoạn văn trình bày các phát hiện di truyền từ nghiên cứu GWAS xác định hàng chục biến thể phổ biến liên quan đến nguy cơ tự kỷ và chức năng synap.',
        'anchor': 'Genome-wide association studies (GWASs) have identified dozens of common variants associated with au',
    },
    {
        'code': '57507B9DC2',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về nguy cơ chấn thương do hành vi đi lang thang ở trẻ khuyết tật phát triển, không liên quan đến yếu tố nguy cơ tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'E345C8C3D3',
        'grade': 0,
        'rationale': 'Đoạn văn so sánh mức độ lo âu giữa các nhóm trẻ tự kỷ và ADHD, không đề cập đến nguy cơ gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '078B4A1002',
        'grade': 0,
        'rationale': 'Đoạn văn giải thích các yếu tố nguy cơ của rối loạn tăng động giảm chú ý (ADHD), không phải của rối loạn phổ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '255F3A5C5F',
        'grade': 3,
        'rationale': 'Tài liệu của CDC nêu rõ các yếu tố làm tăng nguy cơ phát triển tự kỷ: có anh chị em ruột mắc ASD, một số tình trạng di truyền hoặc nhiễm sắc thể (Fragile X, xơ cứng củ), biến chứng khi sinh và sinh ra từ cha mẹ lớn tuổi.',
        'anchor': 'There is not just one cause of ASD. Many different factors have been identified that may make a child more likely to have ASD',
    },
    {
        'code': 'F6DAE16231',
        'grade': 2,
        'rationale': 'Đoạn thảo luận phân tích bối cảnh lịch sử tại Việt Nam về nghiên cứu nguyên nhân tự kỷ, đặc biệt là phơi nhiễm chất độc da cam/dioxin (TCDD) gây độc phát triển.',
        'anchor': 'The historical context of Viet Nam provides a unique focus on the causes of autism, notably dioxin exposure',
    },
    {
        'code': '1731A1F532',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về các yếu tố căn nguyên chung trước và sau sinh cũng như nguy cơ di truyền đa hiệu giữa tự kỷ và các bệnh đồng mắc.',
        'anchor': 'Shared genetic risk between autism and phenotypes are seen with DDX3X-related neurodevelopmental disorder',
    },
    {
        'code': '8892EDE8DF',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về các giả thuyết vệ sinh, phơi nhiễm vi sinh vật trong thai kỳ và ảnh hưởng của hormone giới tính lên nguy cơ tự kỷ.',
        'anchor': 'Hygiene practices commonly in urban areas lowered microbial exposure in pregnancy',
    },
    {
        'code': '8B2BF9CB31',
        'grade': 0,
        'rationale': 'Tổng quan về chẩn đoán và sàng lọc tự kỷ theo DSM-5-TR, không chứa thông tin yếu tố nguy cơ.',
        'anchor': '',
    },
    {
        'code': 'C818B0CBC5',
        'grade': 1,
        'rationale': 'Đoạn văn thảo luận về căn nguyên di truyền chung giữa hội chứng Tourette và tự kỷ thông qua các gen chức năng synap (NRXN1, CNTNAP2).',
        'anchor': 'common genetic etiology between both conditions. The genes NRXN1, CNTNAP2 and SLITRK5',
    },
    {
        'code': '25AA0EAAEC',
        'grade': 1,
        'rationale': 'Đoạn văn đề cập đến nhóm trẻ có nguy cơ cao phát triển tự kỷ (chẳng hạn như em ruột của trẻ đã được chẩn đoán mắc ASD).',
        'anchor': 'high-risk children (for example, younger siblings of children with ASD)',
    },
    {
        'code': '7F9569169A',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về gánh nặng và tỷ lệ hiện mắc tự kỷ tại Việt Nam và các nước, không phân tích yếu tố nguy cơ.',
        'anchor': '',
    },
    {
        'code': '2F8596E024',
        'grade': 3,
        'rationale': 'Đoạn văn xác định hoạt hóa miễn dịch của mẹ (MIA) trong thai kỳ do nhiễm virus/vi khuẩn là một trong những yếu tố nguy cơ miễn dịch được thiết lập rõ ràng nhất đối với ASD.',
        'anchor': 'Maternal immune activation during pregnancy is one of the best-established immunological risk factor',
    },
    {
        'code': '9A8D172E60',
        'grade': 1,
        'rationale': 'Bảng tóm tắt nghiên cứu theo dõi trẻ có nguy cơ gia đình cao và thấp đối với tự kỷ để đánh giá các yếu tố dự đoán sớm.',
        'anchor': 'Evaluate early-life predictors of mid-childhood ASD and anxiety sympto',
    },
    {
        'code': '89C0C57BC8',
        'grade': 0,
        'rationale': 'Đoạn tóm tắt nghiên cứu về triệu chứng ADHD và lo âu ở người tự kỷ, không liên quan đến nguy cơ gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '5928DC5B21',
        'grade': 0,
        'rationale': 'Đoạn thảo luận về điểm cắt thuật toán phát hiện nguy cơ tự kỷ trong đánh giá tâm lý, không phân tích yếu tố nguy cơ sinh học hay môi trường.',
        'anchor': '',
    },
    {
        'code': '6A6187E5D1',
        'grade': 0,
        'rationale': 'Đoạn văn nói về bệnh celiac và chế độ ăn không gluten ở trẻ tự kỷ, không thảo luận về yếu tố nguy cơ tự kỷ.',
        'anchor': '',
    },
    {
        'code': '8E56F84214',
        'grade': 0,
        'rationale': 'Mô tả bài kiểm tra đánh giá tâm lý TAP xác định nguy cơ tự kỷ, không chứa thông tin yếu tố nguy cơ bệnh sinh.',
        'anchor': '',
    },
    {
        'code': '47F677CF80',
        'grade': 2,
        'rationale': 'Phân tích tổng hợp chỉ ra trẻ sinh ra từ các gia đình có tiền sử bệnh tự miễn (viêm khớp dạng thấp, rối loạn tuyến giáp, vảy nến) có nguy cơ mắc tự kỷ cao hơn 28%.',
        'anchor': 'Another association between autoimmunity and autism has been found with regard to the risk of autism in children from families with a history of autoimmunity.',
    },
    {
        'code': '64156F07F2',
        'grade': 2,
        'rationale': 'Đoạn văn phân tích vai trò của nhiễm trùng chu sinh, bệnh tự miễn của mẹ và phơi nhiễm môi trường làm gia tăng nồng độ cytokine tiền viêm dẫn đến tăng nguy cơ tự kỷ ở con.',
        'anchor': 'While epidemiological and animal data remain promising, prenatal infection, autoimmune disease',
    },
    {
        'code': 'AA11AF9D17',
        'grade': 2,
        'rationale': 'Đoạn văn khẳng định các yếu tố trong thời kỳ thai nghén đóng vai trò quyết định định hình nguy cơ ASD, đặc biệt là hoạt hóa miễn dịch của người mẹ (MIA).',
        'anchor': 'Gestational factors play a critical role in shaping ASD risk. Maternal immune activation (MIA) has b',
    },
    {
        'code': '6206BBBD3D',
        'grade': 1,
        'rationale': 'Đoạn văn phân tích cơ chế miễn dịch dị ứng và các rối loạn liên quan ở trẻ tự kỷ, cung cấp bối cảnh về tương tác miễn dịch.',
        'anchor': 'Allergic disorders are caused by dysregulated responses of the immune system to allergens in the env',
    },
    {
        'code': '355083BAD1',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các đặc điểm di truyền nêu rõ có hơn 200 gen nguy cơ tự kỷ, bao gồm các biến thể đa gen phổ biến và biến thể mới phát sinh (de novo).',
        'anchor': '>200 ASD risk genes; both common polygenic and rare de novo variants implicated',
    },
    {
        'code': '59B7914590',
        'grade': 2,
        'rationale': 'Đoạn tổng quan khẳng định tự kỷ có tính di truyền cao với ước tính 60–90%, cả biến thể di truyền từ cha mẹ và biến thể de novo đều đóng góp vào nguy cơ ASD.',
        'anchor': 'ASD is among the most heritable neurodevelopmental conditions, with twin and family studies estimati',
    },
    {
        'code': '25C63E5DCB',
        'grade': 2,
        'rationale': 'Nghiên cứu tại Việt Nam cho thấy tỷ lệ mắc ASD cao hơn ở trẻ có mẹ làm nghề nông, gợi ý mối liên hệ giữa nguy cơ tự kỷ và phơi nhiễm hóa chất trừ sâu.',
        'anchor': 'This finding suggests a possible relationship between ASD and farming practice, especially the common use of pesticides in Vietnam.',
    },
    {
        'code': 'E8B251D532',
        'grade': 0,
        'rationale': 'Đoạn văn hướng dẫn quy trình chuyển tuyến khi trẻ có nguy cơ tự kỷ trên sàng lọc, không chứa thông tin yếu tố nguy cơ bệnh sinh.',
        'anchor': '',
    },
    {
        'code': '634D553D17',
        'grade': 0,
        'rationale': 'Sơ đồ dòng CONSORT phân loại trẻ có nguy cơ tự kỷ theo điểm số AOSI, không nói về nguyên nhân gây bệnh.',
        'anchor': '',
    },
    {
        'code': 'C3B6B82A4E',
        'grade': 0,
        'rationale': 'Bảng thống kê tỷ lệ hiện mắc tự kỷ theo tuổi và giới tính tại miền Bắc Việt Nam, không phân tích yếu tố nguy cơ.',
        'anchor': '',
    },
    {
        'code': '8EFB887A97',
        'grade': 0,
        'rationale': 'Đoạn văn phân tích nguy cơ mắc các bệnh tâm thần đồng mắc ở người tự kỷ, không thảo luận yếu tố nguy cơ gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '1EEAEE6D73',
        'grade': 0,
        'rationale': 'Đoạn văn nói về các vấn đề ăn uống và nguy cơ rối loạn tiêu hóa ở trẻ tự kỷ, không đề cập đến nguyên nhân gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '2741BAE743',
        'grade': 3,
        'rationale': 'Đoạn văn liệt kê chi tiết các yếu tố môi trường và chu sinh làm tăng nguy cơ tự kỷ: phơi nhiễm valproate, rượu thai kỳ, sinh non, nhiễm trùng âm đạo-cổ tử cung của mẹ, ngạt sơ sinh, chấn thương sản khoa, cân nặng khi sinh thấp và béo phì ở mẹ.',
        'anchor': 'Autism can be associated with known environmental factors that can include exposures such as valproate, intrauterine alcohol exposure, prematurity, etc.',
    },
    {
        'code': 'F3FD69E5A9',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến yếu tố nguy cơ gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': '0C74714DCD',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các triệu chứng lo âu và ADHD ở trẻ tự kỷ, không liên quan đến câu hỏi.',
        'anchor': '',
    },
    {
        'code': '680E48071A',
        'grade': 0,
        'rationale': 'Đoạn văn thảo luận về nguy cơ béo phì và tiểu đường do dùng thuốc chống loạn thần ở người tự kỷ, không nói về yếu tố gây tự kỷ.',
        'anchor': '',
    },
    {
        'code': 'BB91336BD5',
        'grade': 2,
        'rationale': 'Đoạn văn phân tích các biến thể di truyền hiếm gặp (CNVs và SNVs de novo) tạo nên nhóm nguy cơ di truyền lớn đối với tự kỷ.',
        'anchor': 'Rare genetic variants—including copy number variants (CNVs) and de novo single-nucleotide variants—c',
    },
    {
        'code': '7D0D49DE57',
        'grade': 3,
        'rationale': 'Đoạn văn giải thích tương tác gen - môi trường đóng góp vào nguy cơ tự kỷ: hoạt hóa miễn dịch của mẹ, phơi nhiễm trước sinh với ô nhiễm không khí, thuốc trừ sâu, axit valproic và các tình trạng chuyển hóa của mẹ (béo phì, tiểu đường).',
        'anchor': 'While genetics play a dominant role, gene–environment interactions contribute to ASD risk. Recent st',
    },
    {
        'code': 'F2DA1BA748',
        'grade': 1,
        'rationale': 'Đoạn văn nêu nhận thức chung rằng nguyên nhân tự kỷ là phức tạp gồm tương tác di truyền và các yếu tố môi trường.',
        'anchor': 'global understandings of autism recognise the aetiology of autism to be complex, with interactive genetic and environmental factors',
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

