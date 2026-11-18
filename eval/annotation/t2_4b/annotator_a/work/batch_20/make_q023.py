import json
import os

batch_file = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl'
returned_dir = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/returned/batch_20'
os.makedirs(returned_dir, exist_ok=True)
out_file = os.path.join(returned_dir, 'q023.jsonl')

with open(batch_file, 'r', encoding='utf-8') as f:
    items = [json.loads(line) for line in f if json.loads(line)['question_id'] == 'q023']

annotations = {
    "E3D107BDAB": (1, "Đoạn văn thảo luận về sự tập trung/cố định vào các âm thanh không liên quan đến xã hội ảnh hưởng đến khả năng giao tiếp và tham gia xã hội của trẻ tự kỷ.", "Together, enhanced sensitivity or fixation on socially irrelevant sounds, and a reduced tendency to attend to socially important ones such as speech, likely influence communication abilities and social participation"),
    "19666697F8": (0, "Mẹo chăm sóc trẻ sơ sinh 2 tháng tuổi, không liên quan đến tự kỷ hay sở thích hạn hẹp.", ""),
    "6A3C88BDFB": (0, "Hướng dẫn của WHO về nuôi con bằng sữa mẹ, không liên quan đến tự kỷ.", ""),
    "83AD3C9E20": (0, "Đoạn văn nói về điều trị bằng thuốc và rối loạn học tập nói chung, không bàn về sở thích hạn hẹp.", ""),
    "15110482F8": (0, "Bảng mô tả các chương trình nhóm kỹ năng xã hội cho trẻ vị thành niên tự kỷ, không bàn về sở thích hạn hẹp ảnh hưởng học tập.", ""),
    "CF2287B5D0": (2, "Đoạn văn minh họa việc tận dụng sự chú ý của trẻ vào một sở thích cụ thể (con voi trong sách) để thu hút trẻ tham gia hoạt động học tập chung và tương tác.", "Laila’s mother tries again. She notices Laila looking at an elephant in the book. Laila’s mother shows Laila the elephant and says, “We have an elephant!” Laila watches this time."),
    "5B935E8E9A": (0, "Khuyến nghị của WHO về can thiệp phát triển trẻ thơ, không nói về sở thích hạn hẹp.", ""),
    "2855D78B14": (0, "Lịch sử phát triển các can thiệp hành vi tự nhiên (NDBI) trong tự kỷ, không bàn về tác động của sở thích hạn hẹp đến học tập.", ""),
    "CD457E9E20": (0, "Nghiên cứu về giao tiếp xã hội của trẻ tự kỷ trong môi trường mầm non hòa nhập, không đề cập đến sở thích hạn hẹp.", ""),
    "931C188C85": (0, "Yếu tố dịch tễ học và vệ sinh môi trường liên quan đến nguy cơ tự kỷ, không liên quan đến học tập.", ""),
    "A750D53002": (0, "Khó khăn trong chẩn đoán tự kỷ ở người trưởng thành, không bàn về việc học tập.", ""),
    "2A485C3BA5": (0, "Quan sát kỹ năng xã hội ở trường mầm non, không đề cập sở thích hạn hẹp.", ""),
    "FFD4823C06": (0, "Mẹo phát triển cho trẻ 6 tháng tuổi, không liên quan đến tự kỷ.", ""),
    "47690261F2": (0, "Hướng dẫn chia nhỏ bước khi dạy trẻ trong sinh hoạt gia đình, không đề cập đến sở thích hạn hẹp.", ""),
    "EB75D80BDF": (0, "Lịch trình các buổi tập huấn cho người chăm sóc, không có nội dung học thuật.", ""),
    "B10DFD8AD9": (0, "Thông tin liên hệ và tài nguyên sức khỏe tâm thần, không liên quan.", ""),
    "7DBDFEF770": (0, "Phương pháp phân tích gộp về can thiệp tự kỷ, không liên quan.", ""),
    "EA446E2C37": (0, "Tóm tắt các buổi tập huấn kỹ năng cho người chăm sóc, không bàn về sở thích hạn hẹp.", ""),
    "2E9513B127": (0, "Mẹo phát triển cho trẻ 4 tháng tuổi, không liên quan đến tự kỷ.", ""),
    "56AC7222E4": (0, "Đoạn văn thảo luận về giao tiếp tăng cường và thay thế (AAC), không bàn về sở thích hạn hẹp.", ""),
    "0FE9ACEBD8": (0, "Hạn chế nghiên cứu về dạy bơi cho trẻ tự kỷ, không liên quan đến việc học.", ""),
    "2A466386A7": (0, "Thông tin giới thiệu người điều phối chương trình tập huấn, không có nội dung.", ""),
    "C454F60111": (0, "Kết quả phân tích hồi quy trong phân tích gộp về can thiệp tự kỷ, không liên quan.", ""),
    "84FC8ABB1D": (1, "Đoạn văn mô tả tiêu chuẩn DSM-5 về các sở thích bị thu hẹp, cố định bất thường về cường độ hoặc sự tập trung.", "3. Highly restricted, fixated interests that are abnormal in intensity or focus (e.g., strong attachment to or preoccupation with unusual objects, excessively circumscribed or perseverative interests)."),
    "BDE001CCF4": (0, "Biểu đồ nhiệt kế hành vi giúp trẻ bình tĩnh và sẵn sàng học hỏi, không nói về sở thích hạn hẹp.", ""),
    "E444C3A3FC": (0, "Địa điểm nghiên cứu tự kỷ tại trường học ở Việt Nam, không bàn về cơ chế sở thích hạn hẹp.", ""),
    "350EF62905": (0, "Khó khăn của người tự kỷ trong môi trường âm thanh ồn ào, không nói về sở thích hạn hẹp.", ""),
    "BD484F11D2": (1, "Đoạn văn giới thiệu tự kỷ là rối loạn phát triển ảnh hưởng đến cách con người tương tác, giao tiếp, học tập và hành vi.", "Autism spectrum disorder (ASD) is a neurological and developmental disorder that affects how people interact with others, communicate, learn, and behave."),
    "A009F8D9A3": (2, "Đoạn văn nêu rõ biểu hiện sở thích sâu sắc kéo dài vào các chủ đề cụ thể (như con số, chi tiết, sự kiện) và chỉ ra các thế mạnh học tập chi tiết, ghi nhớ lâu, xuất sắc trong toán, khoa học, nghệ thuật.", "Having a lasting intense interest in specific topics, such as numbers, details, or facts"),
    "CDDF119B47": (1, "Đoạn văn mô tả các ví dụ về sở thích ám ảnh và hành vi hạn chế lặp lại ở trẻ tự kỷ.", "* Has obsessive interests"),
    "399BBC4ED8": (0, "Mẹo khen ngợi và sử dụng phần thưởng khi dạy trẻ kỹ năng mới, không bàn về sở thích hạn hẹp.", ""),
    "D8A7F554B5": (0, "Xử lý thính giác trong tương tác xã hội ở người tự kỷ, không liên quan đến sở thích hạn hẹp.", ""),
    "C8B84F7E6F": (0, "Nguyên tắc thiết kế công cụ sàng lọc tự kỷ, không liên quan.", ""),
    "1A9BA86026": (0, "Thách thức về xử lý thính giác ở người tự kỷ, không liên quan.", ""),
    "48B71866CB": (0, "Câu hỏi kiểm tra kiến thức cuối buổi tập huấn phụ huynh, không liên quan.", ""),
    "F15FEDD056": (0, "Cảm nhận âm nhạc và thách thức cảm giác ở người tự kỷ, không liên quan.", ""),
    "6F8BC92317": (2, "Đoạn văn chỉ ra người tự kỷ có sở thích hạn hẹp hoặc hành vi lặp lại, đồng thời có những cách thức học tập, vận động hoặc chú ý khác biệt.", "People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests. People with ASD may also have different ways of learning, moving, or paying attention."),
    "661E1BC6E9": (0, "Báo cáo biến cố bất lợi trong nghiên cứu can thiệp, không liên quan.", ""),
    "4B293009E5": (0, "Kể chuyện phụ huynh thực hành kỹ năng tại nhà, không liên quan.", ""),
    "2526443327": (2, "Đoạn văn nêu bật người tự kỷ có hành vi hoặc sở thích hạn hẹp, lặp lại và có những cách học tập, tập trung chú ý khác biệt.", "* People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests."),
    "00971DB013": (0, "Phân loại các nhóm học sinh tự kỷ theo hành vi trong bữa ăn, không liên quan đến việc học tập.", ""),
    "BD341B7D8A": (3, "Đoạn văn giải thích thuyết Đơn tiêu (Monotropism) cho thấy sự tập trung sâu, bền bỉ vào các lĩnh vực hạn hẹp giải thích cả sở thích hạn hẹp lẫn các kỹ năng xuất sắc và khả năng đạt thành tựu trong các ngành STEM.", "Monotropism theory suggests deep, sustained focus on restricted domains, explaining both restricted interests and exceptional skills [50]. Systemizing theory highlights strengths in rule-based reasoning and pattern detection")
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

