import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_19'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q030.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q030']

annotations = {
    "D9C4BB20B8": (2, "Bảng tóm tắt các nghiên cứu báo cáo tỷ lệ xuất hiện triệu chứng tiêu hóa nặng ở trẻ tự kỷ lên tới 40.5% và mối liên quan với vấn đề hành vi.", "At least one severe GI symptom or FS in 40.5% of participants."),
    "2D24400159": (1, "Đoạn văn đề cập đến sự liên hệ giữa táo bón, rối loạn tiêu hóa và rối loạn giấc ngủ ở trẻ tự kỷ.", "Neumeyer et al. [47] found that constipation correlated with sleep disorders in younger children"),
    "A10A2D7722": (0, "Đoạn văn thảo luận về lo âu, thiếu hụt giao tiếp và kỹ năng vận động ở trẻ tự kỷ, không đề cập đến vấn đề tiêu hóa.", ""),
    "F862F73D3C": (2, "Đoạn văn báo cáo tỷ lệ mắc triệu chứng tiêu hóa rất cao ở trẻ tự kỷ (87.6% - 97.1%) và sự kéo dài của các triệu chứng này theo thời gian.", "Babinska et al. [24] found GIS more common in girls with ASD than in boys (97.1% to 87.6% 2 = 13.57, p = 0.009), and 70.6% of girls and 44.5% of boys experienced GIS several times weekly or every day."),
    "661C284A98": (2, "Đoạn văn giải thích tỷ lệ táo bón gia tăng ở trẻ tự kỷ liên quan đến chứng chọn lọc thức ăn và chế độ ăn thiếu chất xơ.", "Increased rates of constipation are also likely affected by food selectivity in this population, as dietary patterns in autism are frequently characterized by minimal intake of fiber-containing foods"),
    "12781F13D2": (1, "Bảng tổng hợp nghiên cứu ghi nhận nhóm trẻ tự kỷ có triệu chứng tiêu hóa thường có triệu chứng tự kỷ cốt lõi nặng hơn.", "ASD + GIS associated with more severe ASD core symptoms than those without GIS."),
    "8432E3AAC9": (1, "Bảng tổng hợp nghiên cứu ghi nhận trẻ tự kỷ có vấn đề tiêu hóa có tỷ lệ rối loạn giấc ngủ cao hơn đáng kể (64.1% so với 50.8%).", "Sign more sleep disorder s/s for children with GI problems (64.1%; 150/234) than for those without GI problems (50.8%; 156/307)."),
    "3853A5AC6A": (0, "Đoạn văn bàn về định nghĩa tự kỷ và bệnh đồng mắc ADHD, không liên quan đến vấn đề tiêu hóa.", "Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors"),
    "5880ACC3B2": (1, "Bảng tổng kết nghiên cứu ghi nhận bất thường tiêu hóa xuất hiện ở 53.9% trẻ tự kỷ trong một thử nghiệm chế độ ăn.", "GI abnormalities in 53.9%. In the gluten-free diet group, the prevalence of GIS decreased significantly to 17.10%."),
    "0FF9B42FD6": (1, "Bảng tóm tắt thử nghiệm can thiệp vi sinh đường ruột cải thiện đáng kể táo bón, tiêu chảy, khó tiêu và đau bụng ở trẻ tự kỷ.", "Significant improvements in constipation, diarrhea, indigestion, and abdominal pain."),
    "BD8953E75C": (0, "Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không đề cập đến tiêu hóa.", ""),
    "0D00A7252C": (1, "Đoạn văn liên hệ triệu chứng tiêu hóa với hành vi thách thức và rối loạn cảm xúc/hành vi ở trẻ mầm non tự kỷ.", "Preschool children with ASD with GIS were found to have substantially more internalizing and externalizing symptoms, significantly different emotional/behavioral problems, and restrictive/repetitive behaviors than those without GIS"),
    "6192667D7F": (3, "Đoạn văn khẳng định trẻ tự kỷ có nguy cơ cao gặp triệu chứng tiêu hóa (9% đến 91%), phổ biến nhất là táo bón, tiêu chảy và đau bụng gây suy giảm chất lượng sống.", "GIS are experienced by between 9 and 91% of children with ASD, and individuals with GIS have a lower quality of life compared to that of those with no GIS"),
    "FE6589E61A": (0, "Đoạn văn tổng quan về đánh giá và chẩn đoán tự kỷ, không đề cập vấn đề tiêu hóa.", ""),
    "221868F75F": (1, "Đoạn văn phân tích mối liên quan giữa triệu chứng tiêu hóa và hành vi thách thức ở 40-65% trẻ tự kỷ có vấn đề tiêu hóa.", "Challenging behaviors are common, and they occur in between 40% and 65% of children with ASD who have at least one GIS"),
    "8272CD28A0": (3, "Đoạn văn khẳng định các vấn đề tiêu hóa thường xuyên được báo cáo ở trẻ tự kỷ, làm tăng đáng kể gánh nặng bệnh tật dù tỷ lệ ước tính dao động do phương pháp đo lường.", "GI problems are frequently reported among autistic children. These conditions contribute significantly to the disease burden associated with autism, though estimates of their prevalence vary substantially due to differences in sampling and measurement"),
    "434A3E2846": (1, "Đoạn văn thảo luận mối quan hệ giữa rối loạn tiêu hóa và rối loạn giấc ngủ ở trẻ tự kỷ.", "The research reviewed on GIS and sleep problems concurs with previous work that sleep problems are common and are associated with GIS"),
    "A85CA5F1B9": (1, "Đoạn văn bàn về can thiệp chế độ ăn không gluten/casein ở trẻ tự kỷ có biểu hiện triệu chứng tiêu hóa (táo bón, tiêu chảy).", "the diet was effective in improving the behaviors of children with ASD showing gastrointestinal symptoms (in particular, constipation and diarrhea)"),
    "C6A7F95D29": (0, "Đoạn văn nói về kỳ thị xã hội và nhận thức về tự kỷ tại Việt Nam, không liên quan đến tiêu hóa.", ""),
    "7E338C45C8": (1, "Đoạn văn trình bày phân tích hệ vi sinh vật và chuyển hóa đường ruột liên quan đến triệu chứng tiêu hóa ở trẻ tự kỷ.", "Integrated microbiome–metabolome analyses (fecal SCFAs, bile acids, aromatic amino acid catabolites) reveal distinct clusters in ASD that associate with GI symptoms and adaptive behavior"),
    "DF77CECB38": (3, "Đoạn văn cung cấp số liệu dịch tễ cụ thể cho thấy trẻ tự kỷ có nguy cơ mắc triệu chứng tiêu hóa (táo bón, tiêu chảy, dị ứng thức ăn) cao hơn từ 2 đến 3 lần so với trẻ phát triển bình thường.", "Studies vary regarding the proportion of children with ASD in samples reported to experience at least one GIS. The prevalence of GIS in autistic samples has been reported to be 30–37.4% [30,59] and 82.4% in the previous three months"),
    "B4E1695AFB": (0, "Đoạn văn nói về đồng mắc ADHD và lo âu ở người tự kỷ, không đề cập đến tiêu hóa.", ""),
    "A87A62B77A": (2, "Bảng tóm tắt các nghiên cứu báo cáo tỷ lệ mắc triệu chứng tiêu hóa cao ở trẻ tự kỷ và nguy cơ táo bón, tiêu chảy tăng cao trong 3 năm đầu đời.", "Higher prevalence GIS in autistic girls than boys. High rates food selectivity 69.1% and mealtime difficulties 64.3%."),
    "CD9ABCBC0D": (1, "Bảng tóm tắt các nghiên cứu kiểm tra cytokine niêm mạc ruột và vi sinh đường ruột ở trẻ tự kỷ có vấn đề tiêu hóa.", "The ASD GI group produced increased mucosa-relevant cytokines compared to ASD no GI group."),
    "F5C448B082": (2, "Đoạn văn tổng quan y văn cho thấy trẻ tự kỷ có nguy cơ cao gặp các lo ngại về tiêu hóa như đau bụng, tiêu chảy và táo bón.", "Review of the scientific literature does indicate that a greater risk for GI concerns (e.g., abdominal pain, diarrhea, constipation) exists in these patients, though the etiology of these observations remains unclear."),
    "926C3C2DAE": (1, "Đoạn văn phân tích hành vi thách thức (gây hấn, lo âu, thu mình) như một cách biểu hiện của khó chịu tiêu hóa ở trẻ tự kỷ.", "The presence of challenging behaviors may reflect the expression of abdominal discomfort in preschool children with ASD"),
    "206C64A381": (1, "Đoạn văn thảo luận mối quan hệ trục ruột-não-miễn dịch và khác biệt thành phần vi sinh vật đường ruột ở trẻ tự kỷ có vấn đề tiêu hóa.", "The results showed the microbiota composition of the children with GIS differed from that of those without GIS and they produced increased levels of mucosa-relevant cytokines."),
    "423E027FDA": (0, "Đoạn văn thảo luận về các mức độ lo âu và bệnh đồng mắc tâm thần ở trẻ tự kỷ và ADHD, không đề cập đến tiêu hóa.", ""),
    "AF674C6466": (0, "Đoạn văn bàn về suy giảm chức năng thích ứng và triệu chứng lo âu ở trẻ tự kỷ và ADHD, không liên quan đến tiêu hóa.", ""),
    "91297D9B52": (1, "Đoạn văn nói về từ chối thức ăn, chọn lọc thức ăn liên quan đến vấn đề tiêu hóa và quá mẫn cảm giác ở trẻ tự kỷ.", "food refusal was associated with lower BMI, sensory issues, and dysfunctional behavior. They concluded that food selectivity involves GIS, individual hypersensitivity, parental behavior, and environmental factors."),
    "CD3D8A3776": (2, "Bảng liệt kê các yếu tố có mối liên hệ tích cực với triệu chứng tiêu hóa, bao gồm sự hiện diện của tự kỷ và mức độ nghiêm trọng của tự kỷ.", "Key factors and their association to GIS.\n| Relationship | Factor |\n|---|---|\n| No Association | Age [8,14,24] |\n| Contradictory Evidence | Positive Association [47] | Language and Communication Ability |\n| No Association [49] |\n| Positive Association [36,40,44,50] | ASD Severity"),
    "EE6188D2E1": (2, "Đoạn văn tổng quan 28 nghiên cứu về tỷ lệ phổ biến của triệu chứng tiêu hóa ở trẻ tự kỷ và mối liên quan với thoái lùi phát triển và mức độ tự kỷ.", "However, the etiology of GIS in ASD remains poorly understood [14]. A detailed understanding of the nature of GIS and how they are associated with co-occurring conditions is required to facilitate the diagnosis of ASD and the treatment of GIS"),
    "6DE642F3A5": (1, "Đoạn văn liên hệ hành vi ăn uống không điển hình và chọn lọc thức ăn với sự hiện diện của ít nhất một triệu chứng tiêu hóa ở trẻ tự kỷ.", "Food selectivity has been associated with the presence of at least one GIS, higher levels of SIB, and anxiety problems"),
    "AB7EB0D26C": (1, "Đoạn văn lưu ý sự cần thiết phải chuẩn hóa định nghĩa và đánh giá triệu chứng tiêu hóa ở người tự kỷ.", "We note a significant need for increased methodological rigor when defining and assessing GI symptoms in autistic patients."),
    "45B886E05B": (3, "Đoạn văn khẳng định các vấn đề tiêu hóa phổ biến nhất ở người tự kỷ gồm táo bón, tiêu chảy và đau bụng, tất cả đều gặp nhiều hơn ở trẻ tự kỷ so với bạn cùng lứa.", "The most common GI concerns among autistic individuals include constipation, diarrhea, and abdominal pain, all of which have been found to be more common among autistic children compared to neurotypical peers"),
    "AE4DB20CAF": (1, "Bảng tóm tắt nghiên cứu ghi nhận trẻ tự kỷ có vấn đề tiêu hóa có nhiều vấn đề lo âu và triệu chứng thể chất hơn.", "ASD children with GIS had more anxiety problems, somatic complaints, externalizing, and total problems than those without GIS."),
    "5A07ACB701": (3, "Đoạn văn thống kê chi tiết tỷ lệ các triệu chứng tiêu hóa cụ thể ở trẻ tự kỷ: trào ngược (5.5%), buồn nôn (23.2-27.9%), nôn (4.2-11.4%), táo bón (22.1-65%), tiêu chảy (10.6-64.7%) và đau bụng (22.9-53.7%).", "Symptoms affecting the lower GI tract include constipation, diarrhea, and pain on stooling. Constipation occurred in 22.1–24.1% of children with ASD in some samples [46,48] and 47.1–65% in other samples"),
    "1579AFEA58": (0, "Đoạn văn nói về phản ứng miễn dịch bất thường và bệnh tự miễn, không bàn về vấn đề tiêu hóa ở trẻ tự kỷ.", ""),
    "F300FFC008": (0, "Đoạn văn bàn về hành vi đi lạc/bỏ chạy ở trẻ khuyết tật phát triển, không liên quan đến tiêu hóa.", "")
}

item_map = {it['annotation_code']: it['content'] for it in items}
results = []

for it in items:
    code = it['annotation_code']
    if code not in annotations:
        raise ValueError(f"Missing annotation for {code}")
    grade, rationale, span = annotations[code]
    content = it['content']
    if grade != 0:
        if not span:
            raise ValueError(f"Span empty for non-zero grade in {code}")
        if span not in content:
            raise ValueError(f"Span not found in content for {code}: {span}")
        if len(span) > 250:
            span_sub = span[:245]
            if span_sub not in content:
                raise ValueError(f"Truncated span not found: {span_sub}")
            span = span_sub
    else:
        span = ""
    
    obj = {
        "annotation_code": code,
        "grade": grade,
        "rationale": rationale,
        "evidence_span": span,
        "confidence": "high",
        "needs_review": False,
        "review_note": "",
        "annotation_type": "ai_generated",
        "model": "claude-sonnet-4-6",
        "prompt_version": "t2_4b_ai_v1"
    }
    results.append(obj)

with open(out_file, 'w', encoding='utf-8') as f:
    for obj in results:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')

print(f"Total entries: {len(results)}")
print(f"Successfully generated and verified {out_file} with {len(results)} annotations.")
