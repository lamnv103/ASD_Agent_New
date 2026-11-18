# T2.4-B — Hồ sơ phân xử q057 và q016 (cho người có thẩm quyền) — 2026-11-15

**Trạng thái: CHỜ QUYẾT ĐỊNH.** Hồ sơ này không đưa ra quyết định thay người có thẩm quyền và không sửa nhãn nào.

Hồ sơ **cố ý không nêu ảnh hưởng của quyết định lên metric** (Hit@k, recall…). Quyết định phải dựa trên nội dung, không dựa trên việc metric tăng hay giảm. Nội dung chunk dưới đây là nguyên văn, đọc qua view nghiên cứu bằng role reader.

Ghi quyết định vào `eval/annotation/t2_4b/coordinator/special_case_decisions_template_2026-11-15.json`. Hãy lưu thành file mới; mọi trường đều bắt buộc.

---

## q057 — "Vắc-xin có gây tự kỷ không?"
- **Nhãn hiện tại (T1, silver):** `unanswerable` / `insufficient`. Phạm vi T1: "Corpus không có bằng chứng → insufficient, không suy diễn".
- **Kiểm tra từ khoá toàn corpus** (T2.3.3, regex `vaccin` trên 2.291 chunk được phép truy xuất): 4 chunk. Chỉ 1 chunk nói về quan hệ vắc-xin và tự kỷ:
  - ASD-OA-PMC12620806#0021: chunk dưới đây.
  - PMC12620806#0034 và PMC13393316#0001: tỷ lệ *tiêm chủng* thấp ở người tự kỷ. Không nói về nguyên nhân.
  - WHO-ECD-GUIDELINE-2020#0023: tên một phòng ban.

**Chunk ASD-OA-PMC12620806#0021**
- Nguồn: *Parallel paths: A narrative review exploring autism and its co-occurring conditions* (PMC12620806).
- Mục: "AUTISM PRESENTATION… > GI CCs"; ký tự 52757–55132.

> "It would be remiss of us to ignore the firestorm of controversy surrounding the alleged role of routine childhood vaccinations in autism and GI tract dysfunction, infamously suggested in a now retracted study. It is not unreasonable to presume that this cause célèbre deterred clinicians and investigators from investing resources into examining GI health in autistic patients…"

Phần còn lại của chunk nói về triệu chứng tiêu hoá, không nói thêm về vắc-xin.

**Bốn điều phải phân biệt (R7):**

| | Corpus nói gì | Corpus **không** nói gì |
|---|---|---|
| Nghiên cứu lịch sử từng được công bố | Có một nghiên cứu từng gợi ý vắc-xin có vai trò ("alleged role… infamously suggested") | Tên, năm, thiết kế của nghiên cứu đó |
| Nghiên cứu đã bị rút | Nghiên cứu đó "now retracted" (đã bị rút) | Lý do bị rút |
| Bằng chứng khoa học hiện tại | — | **Không có** chunk nào trình bày nghiên cứu dịch tễ đánh giá vắc-xin và tự kỷ, hay kết luận "không có liên quan" |
| Khẳng định nhân quả | Chunk gọi đó là vai trò "bị cáo buộc" (alleged); **không** khẳng định nhân quả | Không khẳng định vắc-xin gây tự kỷ, cũng không khẳng định vắc-xin không gây tự kỷ |

**Không được suy ra** "vắc-xin gây tự kỷ" từ việc corpus nhắc đến một nghiên cứu đã bị rút.

**Các lựa chọn để người có thẩm quyền quyết định:**
- **(a) `partially_answerable`.** Corpus cho phép một câu trả lời giới hạn: "Corpus chỉ ghi nhận giả thuyết này đến từ một nghiên cứu đã bị rút; corpus không chứa nghiên cứu đánh giá trực tiếp." Chunk #0021 sẽ có grade 1–2 (người quyết định chọn) và `expected_evidence_status` = `partial`.
- **(b) Giữ `unanswerable`.** Một câu nhắc trong bài tổng quan về tiêu hoá không đủ làm bằng chứng cho câu hỏi nhân quả. Câu trả lời nên báo thiếu bằng chứng và hướng người hỏi tới nguồn y tế chính thức. Chunk #0021 sẽ có grade 0–1.
- **(c) Khác:** ghi rõ.

**Người quyết định cần:** chủ dự án, cùng chuyên gia lâm sàng hoặc y tế công cộng nếu có. Nếu chọn (a), nhãn mới phải vào **phiên bản dataset mới**, không sửa `retrieval_eval_v1.jsonl` hay file merge.

---

## q016 — "\"Chú ý chung\" (joint attention) là gì và tập thế nào?"
- **Nhãn hiện tại (T1, silver):** `partially_answerable` / `partial`. Phạm vi T1: "Khái niệm chú ý chung và can thiệp (JASPER, tiếp cận phát triển)".
- **Chờ phân xử từ T2.3.2:** 2 chunk WHO-CST-PARTICIPANTS-2022, grade tạm 2 do annotator AI gán. **Grade tạm này không phải nhãn** và không dùng làm gợi ý.

**Chunk WHO-CST-PARTICIPANTS-2022#0023** (Caregiver skills training… participants' guide; Session 2: Keeping children engaged; trang 52)

> "Level of engagement: shared engagement — These children are sharing engagement with someone (noticing a person and doing a shared activity at the same time). Shared engagement is best for learning… our goal is to help them spend more time sharing engagement… [Laila's story: her mother looks and listens to notice what Laila is interested in, moves in front of Laila, gets down to her level, puts the activity between them…]"

**Chunk WHO-CST-PARTICIPANTS-2022#0024** (cùng nguồn, trang 57)

> "…This is shared engagement: Laila and her mother are doing an activity together and Laila is noticing her mother and the activity at the same time!… Shared engagement means that the child is paying attention to two things at the same time: 1. you, and 2. the activity you and your child are doing together. Other times children may be: not engaged…; object-engaged… [Key messages; tips: look and listen, give 2 or 3 options, respond to the child's choice]"

**Câu hỏi cần quyết định:**
1. **Khái niệm.** "Shared engagement" theo định nghĩa của WHO-CST ("chú ý đồng thời tới người lớn và hoạt động chung") có được coi là định nghĩa, hoặc một dạng, của *joint attention* không?
   - Trong tài liệu chuyên môn, joint attention thường được mô tả bằng việc phối hợp ánh nhìn, chỉ tay hay khởi xướng/đáp ứng.
   - **Hai chunk không dùng từ "joint attention".**
2. **Mức hỗ trợ.** Nếu chấp nhận câu 1: #0024 có định nghĩa và mẹo luyện tập (phần "tập thế nào"); #0023 có các mức tương tác và ví dụ. Mức hỗ trợ là 3, 2 hay 1?
3. Nếu không chấp nhận câu 1: grade 1 (bối cảnh liên quan) hay 0?

**Các lựa chọn cho mỗi chunk:** 3 / 2 / 1 / 0, kèm lý do. Lý do phải dựa trên nội dung, không dựa trên ảnh hưởng tới metric.

**Người quyết định cần:** chuyên gia ngôn ngữ trị liệu hoặc can thiệp sớm, hoặc chủ dự án nếu chưa có chuyên gia.

Hai chunk này cũng có trong pool T2.4-B và sẽ được người chấm A và B chấm mù như mọi cặp khác. Quyết định ở đây tách biệt với nhãn A/B. Nếu có khác biệt giữa hai bên, ghi lại cả hai.

---

## Còn tồn đọng từ T2.3.2 (không thuộc yêu cầu R7, ghi để không bị bỏ sót)
- **q041 NIHR-SENITA-2022#0309**
  - Grade tạm −1: lợi ích do người chăm sóc cảm nhận (định tính), trái với kết quả RCT không có hiệu quả.
  - Đề xuất: người thứ hai (human) xác nhận có giữ −1 hay không.
