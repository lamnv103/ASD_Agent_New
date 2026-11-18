import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_19.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_19'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q027.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q027']

annotations = {
    "E15F37AD7A": (2, "Đoạn văn nêu rõ tiêu chuẩn chẩn đoán DSM-5 yêu cầu bao quát nhóm A (tương tác và giao tiếp xã hội) và ít nhất hai tiêu chuẩn từ nhóm B (hành vi hạn chế và lặp lại).", "items in the existing screening methods should cover social interaction and social communication (Category A) in the DSM-5 manual and at least two criteria from Category B (Restricted and Reparative Behaviour)."),
    "7DD437F629": (0, "Đoạn văn nói về sự kỳ thị và bối cảnh chẩn đoán tự kỷ tại Việt Nam, không liên quan đến tiêu chuẩn chẩn đoán DSM-5.", ""),
    "8C7B389E73": (2, "Đoạn văn tóm tắt tiêu chuẩn chẩn đoán DSM-5 gồm khó khăn dai dẳng về giao tiếp xã hội và các biểu hiện hành vi, sở thích lặp lại hạn chế.", "According to the DSM-5 (APA, 2013), to meet the diagnostic criteria, an individual must exhibit persistent challenges in social communication and interaction across multiple settings and also demonstrate symptoms in the restricted, repetitive patterns"),
    "636B19CCDC": (1, "Đoạn văn nhắc đến một số tiêu chuẩn cụ thể của DSM-5 (A1, B1, B4) trong phân tích kết quả thử nghiệm can thiệp sớm.", "the 7 criteria for ASD (Table 3). A logistic regression analysis incorporating covariates identified reduced odds of meeting DSM-5 criteria A1 among the iBASIS-VIPP group (deficits in social-emotional reciprocity"),
    "6120526FFF": (0, "Đoạn văn bàn về đồng mắc lo âu và ADHD ở trẻ tự kỷ, không nêu tiêu chuẩn chẩn đoán DSM-5.", ""),
    "4BC0244DB3": (1, "Đoạn văn định nghĩa ASD theo thiếu hụt giao tiếp xã hội và hành vi lặp lại, đồng thời nhắc đến việc DSM-5 chính thức cho phép chẩn đoán đồng thời ASD và ADHD.", "Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors"),
    "6932932EEF": (0, "Đoạn văn thảo luận về các mức độ lo âu và bệnh lý tâm thần đi kèm ở trẻ tự kỷ và ADHD, không nêu tiêu chuẩn chẩn đoán DSM-5.", ""),
    "8FA463304E": (0, "Đoạn văn nói về triệu chứng tiêu hóa và hệ vi sinh vật đường ruột ở trẻ tự kỷ, không liên quan đến tiêu chuẩn DSM-5.", ""),
    "1B85BCF617": (0, "Đoạn văn nghiên cứu về tỷ lệ đồng mắc ADHD và lo âu ở trẻ tự kỷ, không trình bày tiêu chuẩn DSM-5.", ""),
    "98EF6A3F2A": (-1, "Đoạn văn là thông báo bản quyền và xuất bản của NIMH, không chứa nội dung khoa học.", "The information in this publication is in the public domain and may be reused or copied without permission."),
    "732C62F9D9": (1, "Đoạn văn nhận xét về tầm quan trọng của tiêu chuẩn DSM-5 đối với việc đánh giá độ tin cậy của các công cụ sàng lọc tự kỷ.", "none of the reviews emphasise the importance of the DSM-5 criteria for evaluating the reliability of ASD screening."),
    "F0F50C4368": (1, "Đoạn văn lưu ý sự cần thiết của các công cụ sàng lọc mới phải tuân theo các tiêu chuẩn chẩn đoán của DSM-5.", "the majority of these screening tools do not fully align with the new criteria for ASD developed under the DSM-5. Therefore, the need for revised methods that adhere to the standards of the DSM-5 have arisen."),
    "D131F504D5": (0, "Bảng đếm số lượng các công cụ/tiêu chuẩn (CARS, DSM-4, DSM-5,...) trong tài liệu bổ sung, không mô tả tiêu chuẩn.", ""),
    "41C5A70D36": (0, "Đoạn văn bàn về đáp ứng miễn dịch bất thường và bệnh tự miễn ở người tự kỷ, không liên quan đến tiêu chuẩn DSM-5.", ""),
    "C1FF04F071": (1, "Đoạn văn đề cập DSM-5 của Hiệp hội Tâm thần học Hoa Kỳ cung cấp các tiêu chuẩn chuẩn hóa để chẩn đoán ASD.", "the American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD."),
    "D7BD0DA199": (0, "Đoạn văn nói về các can thiệp hành vi và hội chứng căng trương lực (catatonia) ở trẻ tự kỷ, không trình bày tiêu chuẩn cốt lõi của ASD trong DSM-5.", ""),
    "97589F5090": (3, "Đoạn văn liệt kê đầy đủ cả 7 tiêu chuẩn chẩn đoán ASD theo DSM-5: A1, A2, A3 (giao tiếp xã hội) và B1, B2, B3, B4 (hành vi lặp lại hạn chế).", "these criteria were A1 (deficits in social-emotional reciprocity), A2 (deficits in nonverbal communicative behaviors used for social interaction), A3 (deficits in developing, maintaining, and understanding relationships)"),
    "64CF120CE2": (3, "Đoạn văn trình bày chi tiết Tiêu chuẩn A của DSM-5 (gồm 3 tiêu chí: tương hỗ xã hội-cảm xúc, giao tiếp phi ngôn ngữ, phát triển mối quan hệ) và các mức độ nghiêm trọng (Level 1-3).", "1. Deficits in social-emotional reciprocity, ranging, for example, from abnormal social approach and failure of normal back-and-forth conversation; to reduced sharing of interests, emotions, or affect; to failure to initiate or respond to social"),
    "174C35B22F": (2, "Đoạn văn tóm tắt định nghĩa tự kỷ theo DSM-5-TR gồm thách thức trong tương tác xã hội và giao tiếp cùng với sự hiện diện của sở thích hạn chế và hành vi lặp lại.", "Autism Spectrum Disorder (ASD) is a neurodevelopmental condition characterized by challenges in social interaction and communication, and the presence of restricted interests and repetitive behaviors (Diagnostic and Statistical Manual"),
    "9E8FD1CFDE": (1, "Đoạn văn giải thích sự thay đổi giữa DSM-IV và DSM-5, gộp 5 rối loạn phát triển lan tỏa thành ASD.", "The most recent version of the DSM (DSM-5) groups the five PDDs, consisting of Asperger syndrome (AS), pervasive development disorder–not otherwise specified (PDD-NOS), Rett syndrome (RS), and childhood disintegrative disorder (CDD), into ASD"),
    "E13F6956C2": (1, "Đoạn văn tóm lược điểm chính về nguồn thông tin chẩn đoán và vai trò của cẩm nang DSM-5 trong việc cung cấp tiêu chuẩn chẩn đoán.", "The American Psychiatric Association's Diagnostic and Statistical Manual, Fifth Edition (DSM-5) provides standardized criteria to help diagnose ASD."),
    "4CF50E1153": (3, "Bảng 1 trình bày chi tiết và toàn diện toàn bộ tiêu chuẩn chẩn đoán DSM-5 cho tự kỷ: Nhóm A (A1, A2, A3) và Nhóm B (B1, B2, B3, B4).", "Table 1.\nDiagnostic Criteria of Autism Spectrum Disorder in the DSM-5\n| A. Social communication and interaction challenges: |\n| 1. Deficits in social-emotional reciprocity |\n| 2. Deficits in nonverbal communicative behaviors used for social interaction"),
    "2E6A75C631": (0, "Đoạn văn mô tả tiêu chí lựa chọn nghiên cứu cho can thiệp nhóm kỹ năng xã hội ở trẻ vị thành niên, không giải thích tiêu chuẩn DSM-5.", ""),
    "BD2403ADC8": (3, "Đoạn văn giải thích cấu trúc và các thay đổi cốt lõi của tiêu chuẩn DSM-5/DSM-5-TR: sáp nhập 2 lĩnh vực (giao tiếp xã hội và hành vi lặp lại hạn chế), bổ sung triệu chứng cảm giác, thang độ nặng 1-3 và yêu cầu đủ 3 tiêu chí nhóm A.", "the three symptom categories of social impairment, language/communication impairment, and repetitive/restricted behaviors were merged into two symptom domains: persistent deficits in social communication and interaction and restricted"),
    "8488D91E82": (0, "Đoạn văn bàn về kết quả thử nghiệm lâm sàng can thiệp sớm iBASIS-VIPP, không trình bày tiêu chuẩn DSM-5.", ""),
    "345292C1A4": (1, "Đoạn văn nêu tổng quan nghiên cứu đánh giá các công cụ sàng lọc tự kỷ dựa trên việc đáp ứng các thông số của DSM-5.", "the fulfilment of Diagnostic and Statistical Manual of Mental Disorders (DSM-5) specifications"),
    "D5472BF1A3": (0, "Danh sách từ viết tắt trong bài báo, không chứa nội dung giải thích tiêu chuẩn.", ""),
    "925B934DDF": (2, "Đoạn văn trình bày các chỉ dẫn chẩn đoán và đặc tả đi kèm của tiêu chuẩn DSM-5 (về khuyết tật trí tuệ, suy giảm ngôn ngữ, tình trạng bệnh lý).", "Individuals with a well-established DSM-IV diagnosis of autistic disorder, Asperger's disorder, or pervasive developmental disorder not otherwise specified should be given the diagnosis of autism spectrum disorder."),
    "8F03594A70": (0, "Đoạn văn trình bày các mục tiêu nghiên cứu về ADHD và lo âu đồng mắc trong ASD, không nêu tiêu chuẩn DSM-5.", ""),
    "AB14022D41": (0, "Đoạn văn nói về sự tham gia của cộng đồng tự kỷ trong nghiên cứu tại Việt Nam, không liên quan đến tiêu chuẩn DSM-5.", ""),
    "6586637843": (1, "Đoạn văn bàn về mức độ tuân thủ tiêu chuẩn ASD của DSM-5 ở các công cụ sàng lọc hiện có.", "Many of the available screening tools, especially the short versions, comply only partly with the ASD criteria of the DSM-5 introduced in 2013."),
    "7508E32FBA": (0, "Đoạn văn bàn về hành vi đi lạc/bỏ chạy ở trẻ khuyết tật phát triển tại Mỹ, không liên quan đến tiêu chuẩn DSM-5.", ""),
    "67E499A230": (0, "Đoạn văn trình bày tiêu chuẩn DSM-5 đối với rối loạn ăn uống (như ARFID), không phải tiêu chuẩn chẩn đoán tự kỷ.", ""),
    "C082447E90": (0, "Đoạn văn mô tả phương pháp và người tham gia trong nghiên cứu về ADHD và lo âu đồng mắc ở ASD, không trình bày tiêu chuẩn.", ""),
    "F125B9B37A": (2, "Đoạn văn tóm tắt các đặc điểm cốt lõi của tự kỷ theo DSM-5 từ nguồn Viện Sức khỏe Tâm thần Quốc gia Hoa Kỳ (NIMH).", "According to the *Diagnostic and Statistical Manual of Mental Disorders (DSM-5)*, a guide created by the American Psychiatric Association that health care providers use to diagnose mental disorders and developmental disorders, people with ASD often have:"),
    "EA3CE1631E": (0, "Đoạn văn nói về mối liên hệ sinh học giữa động kinh và tự kỷ, không liên quan đến tiêu chuẩn DSM-5.", ""),
    "A2A22E1557": (0, "Đoạn văn mô tả việc sử dụng công cụ KID-SCID để đánh giá các rối loạn theo DSM-IV, không phải tiêu chuẩn tự kỷ DSM-5.", ""),
    "60398D00B7": (3, "Đoạn văn trình bày chi tiết Tiêu chuẩn B của DSM-5 (gồm 4 nhóm hành vi lặp lại hạn chế: vận động lặp lại, sự đồng nhất/thói quen, sở thích cố định, phản ứng cảm giác) và 3 mức độ nghiêm trọng.", "1. Stereotyped or repetitive motor movements, use of objects, or speech (e.g., simple motor stereotypes, lining up toys or flipping objects, echolalia, idiosyncratic phrases)."),
    "4ED216920C": (0, "Đoạn văn mô tả phương pháp trích xuất dữ liệu của một phân tích tổng hợp về bệnh đồng mắc, không nêu tiêu chuẩn tự kỷ.", ""),
    "192344232C": (0, "Đoạn văn thảo luận về sự giao thoa giữa lo âu và thiếu hụt giao tiếp xã hội trong ASD và ADHD, không nêu tiêu chuẩn DSM-5.", ""),
    "79F26D1C52": (1, "Đoạn văn giới thiệu về quá trình chuyển đổi từ DSM-IV sang DSM-5 năm 2013 ảnh hưởng đến chẩn đoán tự kỷ.", "In 2013, the DSM-IV was revised, which posed a significant challenge to the way individuals are assessed as being on the ASD spectrum and necessitated refinements of existing diagnosis as well as screening techniques."),
    "F8BD5B9A56": (1, "Đoạn văn so sánh tỷ lệ phát hiện đồng mắc ADHD ở người tự kỷ theo DSM-IV so với tiêu chuẩn DSM-5.", "Studies using DSM-IV reported lower rates of ADHD in contrast to ones using DSM-5 criteria."),
    "02325880DC": (0, "Bảng đếm tiêu chí đánh giá chất lượng phương pháp MMAT, hoàn toàn không liên quan.", ""),
    "5DF1AA9340": (3, "Đoạn văn tóm tắt cấu trúc bắt buộc của tiêu chuẩn chẩn đoán DSM-5: phải có đủ 3 biểu hiện trong nhóm giao tiếp xã hội (A1-A3) và ít nhất 2 trong 4 dạng hành vi lặp lại hạn chế (B1-B4).", "To meet diagnostic criteria for ASD according to DSM-5, a child must have persistent deficits in each of three areas of social communication and interaction (see A.1. through A.3. below) plus at least two of four types of restricted, repetitive behaviors"),
    "33B362108E": (0, "Đoạn văn mô tả tiêu chí lựa chọn bài báo trong một phân tích gộp về bệnh lý tâm thần đi kèm, không trình bày tiêu chuẩn tự kỷ.", "")
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
            # Let's truncate span cleanly if > 250
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

