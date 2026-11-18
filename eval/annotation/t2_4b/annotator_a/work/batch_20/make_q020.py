import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_20'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q020.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q020']

annotations = {
    "85543642DE": (2, "Đoạn văn giới thiệu về vấn đề kén ăn ở trẻ tự kỷ, bao gồm các đặc điểm y khoa, cảm giác và hành vi ảnh hưởng đến sự từ chối thức ăn.", "Exploring feeding issues in ASD, we can observe either medical or sensorial/behavioral characteristics which influence food refusal or restricted food preferences of autistic children during mealtimes."),
    "451A48AF6C": (2, "Đoạn văn thảo luận về việc phân nhóm trẻ kén ăn nguy cơ cao và tầm quan trọng của việc đánh giá toàn diện các yếu tố dinh dưỡng, y tế, cảm giác, hành vi để can thiệp cá nhân hóa.", "these clusters examined by authors permit clinicians to immediately detect the core symptom of a child along with the correlated variables (nutritional, medical, sensorial, behavioral, and environmental)."),
    "FD9ECCFAD5": (2, "Đoạn văn mô tả các can thiệp xử lý cảm giác đối với chứng kén ăn, như biến đổi hình thức cảm giác của rau củ thành đồ ăn nhẹ và làm quen khứu giác để tăng khả năng chấp nhận thức ăn.", "physical changes in foods can contribute to improving sensory processing and the consequent intake of foods otherwise rejected."),
    "922CB24819": (0, "Đoạn văn bàn về đồng mắc ADHD và lo âu ở người tự kỷ, không liên quan đến kén ăn hay đánh giá can thiệp ăn uống.", ""),
    "D120F43B7D": (3, "Đoạn văn giới thiệu chi tiết thang đo chuẩn hóa BPFAS gồm 35 mục dùng để đánh giá hành vi ăn súc tích của trẻ và hành vi của cha mẹ trong bữa ăn.", "The Behavior Pediatric Feeding Assessment Scale (BPFAS), the original instrument made up of 35 items, allows the calculation of four scores, relating to the four subscales of which it is composed"),
    "F74038E5F2": (0, "Đoạn văn phân tích phương pháp nghiên cứu thử nghiệm lâm sàng và biến cố bất lợi trong can thiệp tự kỷ nói chung, không nói về kén ăn.", ""),
    "A27DA5FA72": (0, "Đoạn văn tổng quan về chẩn đoán và đánh giá tự kỷ theo DSM-5-TR, không đề cập đến ăn uống.", ""),
    "089400003D": (3, "Đoạn văn hướng dẫn quy trình đánh giá kén ăn trước can thiệp: kiểm tra bệnh đường tiêu hóa (GID), nhật ký ăn uống, đường cong tăng trưởng/BMI và bảng hỏi tần suất thực phẩm FFQ.", "Firstly, before implementing an educational intervention, the following intersected aspects such as GID, assumed foods (food diary), and growth curves as suggested by Badalyan and Schwartz [59], should be addressed."),
    "F66267648E": (0, "Bảng tóm tắt kết quả nghiên cứu can thiệp từ xa do cha mẹ thực hiện về giao tiếp xã hội, không liên quan đến vấn đề ăn uống.", ""),
    "B0C8BF9CA0": (3, "Đoạn văn trình bày các kỹ thuật can thiệp hành vi cụ thể đối với chứng kén ăn: củng cố cá nhân hóa, tiếp xúc phân cấp, làm mẫu qua video và quy trình không rút thìa (non-removal of spoon).", "using individualized reinforcement and hierarchical exposure can increase flexibility in food intake in children with ASD."),
    "65099E3990": (0, "Đoạn văn khuyến nghị nghiên cứu can thiệp qua phụ huynh từ xa trong kỹ năng xã hội, không đề cập đến kén ăn.", ""),
    "F1A8CED362": (2, "Đoạn văn phân tích cơ chế hành vi khiến trẻ duy trì việc từ chối thức ăn và áp lực của cha mẹ trong bữa ăn, làm cơ sở cho can thiệp hành vi.", "the child learns to avoid undesirable foods by emitting challenging behaviors, as well as the parents involuntarily maintaining such behaviors by presenting only the preferred food at mealtime"),
    "A6DB37EB0B": (3, "Đoạn văn mô tả chi tiết quy trình định hình hành vi (shaping) và củng cố vi sai từng bước để tăng cường việc chấp nhận và ăn các món ăn mới ở trẻ tự kỷ.", "When applied to the feeding behaviors, during the shaping procedure the tutor should gradually reinforce the successive approximations of the target feeding behavior, such as: placing food in the spoon, food near the lips"),
    "BCBFA06D83": (2, "Đoạn văn phân tích các nguyên nhân đa chiều gây kén ăn ở trẻ tự kỷ, bao gồm rối loạn tiêu hóa (GID), chứng ác cảm cảm giác và loạn khuẩn đường ruột.", "Concerning the causes of food selectivity in children with ASD, scientists have examined diverse dimensions of altering feeding behaviors. As mentioned above, the importance of motor conditions and/or gastrointestinal complications should be addressed"),
    "8A3011617F": (3, "Đoạn văn giới thiệu chi tiết thang đo BAMBI (18 mục) để đánh giá hành vi ăn uống của trẻ tự kỷ qua 3 yếu tố: giới hạn đa dạng món, từ chối thức ăn và đặc điểm tự kỷ.", "The Brief Autism Mealtime Behavior Inventory (BAMBI) is a tool composed of 18 items to identify the presence of aggressive and destructive behaviors during meals"),
    "2AD2A8CD92": (0, "Đoạn văn bàn về can thiệp sớm iBASIS-VIPP cho trẻ có dấu hiệu sớm của tự kỷ, không liên quan đến can thiệp kén ăn.", ""),
    "62369EB295": (2, "Đoạn văn nhấn mạnh việc phân loại nhóm triệu chứng giúp nhân viên lâm sàng đánh giá hiệu quả can thiệp phù hợp với hồ sơ ban đầu của từng trẻ.", "classification in subgroups could permit clinical staff to assess the efficacy of treatment with respect to the children’s profile in the baseline (tailored treatment)."),
    "A713CCA32E": (0, "Đoạn văn nói về can thiệp do cha mẹ làm trung gian qua mạng đối với kỹ năng xã hội, không bàn về kén ăn.", ""),
    "69DBC29612": (0, "Đoạn văn mô tả quy trình chuyển gửi đánh giá toàn diện sau khi sàng lọc tự kỷ, không liên quan đến ăn uống.", ""),
    "1278CD36D7": (0, "Đoạn văn thảo luận về chức năng thích ứng và triệu chứng lo âu ở trẻ tự kỷ và ADHD, không liên quan đến kén ăn.", ""),
    "E03CD339B4": (1, "Đoạn văn mô tả trải nghiệm căng thẳng của các bà mẹ khi xử lý các khó khăn về ăn uống của trẻ tự kỷ trong bữa ăn gia đình.", "Additionally, the need to negotiate a child’s feeding challenge was reported by many mothers as one of the reasons influencing family well-being"),
    "49C69129B2": (2, "Đoạn văn mô tả thử nghiệm đánh giá phản ứng nếm thức ăn và can thiệp hành vi để vượt qua việc từ chối ăn ở trẻ.", "all children consistently refused bites and engaged in feeding in"),
    "A8171FD588": (0, "Đoạn văn tổng quan về sàng lọc và chẩn đoán tự kỷ theo DSM-IV/5, không đề cập đến kén ăn.", ""),
    "D18D503B44": (0, "Đoạn văn bàn về đáp ứng miễn dịch và bệnh tự miễn ở người tự kỷ, không liên quan đến can thiệp kén ăn.", ""),
    "58EB694D1D": (2, "Đoạn văn trình bày phương pháp đánh giá trực tiếp hành vi của trẻ trong bữa ăn qua quan sát tự nhiên hoặc phân tích chức năng.", "Direct measurement regards the behavior exhibited by children during mealtimes."),
    "A184E2E3BC": (2, "Đoạn văn kết luận sự cần thiết phải phối hợp giữa gia đình và nhân viên lâm sàng để đánh giá đúng nguyên nhân gây kén ăn ở trẻ tự kỷ.", "Concluding, food selectivity is a problem common in many children, in particular those with autism symptoms. Therefore, families along with clinical staff should establish concurrent causes of feeding issues in their child through a correct assessmen"),
    "0C1F022282": (0, "Đoạn văn bàn về giả thuyết nghiên cứu lo âu và ADHD ở người tự kỷ, không liên quan đến ăn uống.", ""),
    "FDE1B38BC1": (3, "Đoạn văn tóm tắt các kỹ thuật can thiệp hành vi hiệu quả dựa trên nguyên lý ABA đối với kén ăn: tăng cường củng cố, định hình, làm mờ kích thích và dập tắt hành vi trốn tránh.", "In the section concerning behavioral interventions, we have listed diverse, effective techniques based on ABA principles displaying some examples of their implementation"),
    "F681DFCE9B": (2, "Đoạn văn chỉ ra thông tin đánh giá giúp xác định hành vi mục tiêu can thiệp và các yếu tố bối cảnh, rào cản đối với việc ăn uống đầy đủ.", "This information could help clinicians to identify the target behaviors of the intervention, along with the contextual factors that might constitute specific advantages and possible barriers to adequate food intake."),
    "1D67FB6B70": (2, "Đoạn văn hướng dẫn thu thập bệnh sử qua phỏng vấn gia đình kết hợp các công cụ thang đo chuẩn hóa để lên kế hoạch can thiệp giáo dục phù hợp.", "Starting with interviews of families, the clinicians could enrich their anamnesis of children using well-structured instruments such as questionnaires and measure scales."),
    "BD8FBA235E": (1, "Đoạn văn nhắc đến tiêu chuẩn DSM-5 đối với rối loạn ăn uống trẻ em (như ARFID - rối loạn né tránh/hạn chế tiếp nhận thức ăn) liên quan đến kén ăn.", "In the new edition of DSM-5 (https://www.ncbi.nlm.nih.gov/books/NBK519712/table/ch3.t18/, accessed on 9 February 2023), nutrition and eating disorders during childhood include pica, avoidant/restrictive disorder of food intake"),
    "C14E67B5A5": (2, "Đoạn văn phân tích nguy cơ thiếu hụt dinh dưỡng (vitamin D, chất xơ, vitamin E, canxi) ở trẻ kén ăn, đòi hỏi phải đánh giá dinh dưỡng cẩn trọng.", "Seventy-eight percent consumed a diet at risk of five or more inadequacies. Risk for specific inadequacies included vitamin D (97% of the sample), fiber (91%), vitamin E (83%), and calcium (71%)."),
    "82DEF08DC1": (2, "Đoạn văn hướng dẫn đánh giá dinh dưỡng ở trẻ tự kỷ nhằm phát hiện tình trạng thiếu hụt vi chất do chế độ ăn hạn hẹp.", "Concerning the nutritional assessment for children with ASD, clinicians should detect the causal nutritional inadequacies connected to the restricted intake"),
    "25B8597E69": (2, "Đoạn văn khẳng định can thiệp huấn luyện phụ huynh (trực tiếp hoặc qua từ xa) mang lại hiệu quả cải thiện các vấn đề ăn uống ở trẻ tự kỷ.", "The clinical interventions for children, adolescents, and young adults with autism have demonstrated gains in different developmental domains where parent inclusion and related training have been largely suggested and recommended"),
    "FB71AF5140": (2, "Đoạn văn nhấn mạnh điều trị rối loạn ăn uống ở trẻ em là phức tạp và bắt buộc phải tiếp cận đa ngành.", "The treatment of eating disorders in children is complex and necessarily multidisciplinary."),
    "2845638432": (1, "Đoạn văn đề cập đến tỷ lệ dị ứng thức ăn gia tăng ở trẻ tự kỷ cần được kiểm tra khi đánh giá vấn đề ăn uống.", "Parent-reported food allergies were nearly 2.5 times more common in children with ASD"),
    "5A07DD3133": (1, "Đoạn văn lưu ý vai trò của gia đình trong việc giảm thiểu vấn đề ăn uống của trẻ bằng cách tăng tiêu thụ thức ăn lành mạnh.", "families can reduce the feeding issues of children (overweight, intake of junk food, and other eating disorders) increasing the consumption of healthy foods."),
    "180A3D6142": (2, "Đoạn văn lưu ý cần phân biệt rõ triệu chứng từ chối thức ăn có nguồn gốc thực thể (y khoa) hay có chức năng hành vi (nhằm thu hút sự chú ý hoặc trốn tránh).", "Conversely, a severe symptom of food refusal could be characterized by dysfunctional behaviors that have the function to obtain social attention or escape [14]."),
    "0698F0B688": (2, "Bảng tóm tắt các bảng hỏi chuẩn hóa chính dùng để đánh giá hành vi ăn uống ở trẻ em (BAMBI-C, STEPS,...).", "ijerph-20-05092-t001_Table 1Table 1\nDescriptions of some main questionnaires regarding feeding behaviors."),
    "38208CBA60": (2, "Đoạn văn nghiên cứu so sánh về tần suất ăn uống chọn lọc và nguy cơ thiếu hụt dinh dưỡng ở trẻ tự kỷ so với trẻ phát triển bình thường.", "Firstly, the frequency of selective eating and nutritional deficiency was studied among 22 children with autism and an age-matched TDC group. Children with autism ate fewer foods on average than TDC."),
    "DFE346D5D3": (2, "Đoạn văn nhấn mạnh chế độ ăn hạn chế ảnh hưởng đến dinh dưỡng của trẻ và tạo gánh nặng lớn cho gia đình, cần can thiệp hỗ trợ phụ huynh.", "Since a restricted diet can influence the nutritional intake of children, causing significant stress to the families [32,51], feeding problems should be considered as a severe burden for families and therapists"),
    "B53DD3B76D": (3, "Đoạn văn tổng quan giới thiệu mục tiêu cung cấp hướng dẫn toàn diện về quy trình đánh giá và các phương pháp can thiệp đối với chứng kén ăn ở trẻ tự kỷ.", "Autisms Spectrum Disorders (ASD) are characterized by core symptoms (social communication and restricted and repetitive behaviors) and related comorbidities, including sensory anomalies, feeding issues, and challenging behaviors."),
    "75C22FFE9E": (2, "Đoạn văn thảo luận về sự tham gia của cha mẹ và các chuyên gia đa ngành (nhà trị liệu hoạt động, tâm lý, ngôn ngữ) trong các phương pháp can thiệp ăn uống dựa trên hành vi hoặc cảm giác.", "Generally, parental involvement can change depending on familiar resources and the type of the intervention (e.g., behavior-based or sensory-based approaches) and providers (e.g., occupational therapists, psychologists, or speech therapists)."),
    "5AA491A7CB": (3, "Đoạn văn nêu rõ mục đích bài tổng quan là làm sáng tỏ cách đánh giá chứng kén ăn ở trẻ tự kỷ và cách lập kế hoạch can thiệp lâm sàng cá nhân hóa, hiệu quả.", "The current narrative review sheds light on how to assess food selectivity in children with ASD and how to plan effective and individualized interventions."),
    "3BAC728961": (2, "Bảng liệt kê các thực hành cho ăn mang tính giáo dục của người chăm sóc để can thiệp hành vi ăn uống.", "ijerph-20-05092-t002_Table 2Table 2\nRepresentative items of the educational caregiver feeding practices."),
    "0840EF7619": (1, "Đoạn văn báo cáo kết quả theo dõi mối liên hệ bền vững giữa chứng kén ăn và tính quá mẫn cảm giác ở trẻ tự kỷ.", "Results comparing time one to time two indicated no change in food selectivity level and a stable, significant relationship between food selectivity and sensory over-responsivity."),
    "6405F5F0FA": (0, "Đoạn văn bàn về dấu ấn sinh học tiên lượng trong can thiệp giao tiếp cho trẻ ít lời, không nói về kén ăn.", ""),
    "208BD9A91C": (0, "Đoạn văn nói về các can thiệp phát triển hành vi tự nhiên (NDBIs) trong giai đoạn thơ ấu, không nói về ăn uống.", ""),
    "6EA4321137": (0, "Đoạn văn bàn về hành vi đi lạc/bỏ chạy ở trẻ khuyết tật phát triển, không liên quan đến kén ăn.", ""),
    "E7178429E2": (0, "Đoạn văn mã hóa phương pháp phân tích gộp về bối cảnh can thiệp tự kỷ nói chung, không nói về kén ăn.", "")
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
