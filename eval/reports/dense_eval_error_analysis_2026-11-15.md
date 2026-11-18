# T2.3.3: Dense Retrieval — Error Analysis — 2026-11-15

## Phương pháp
- Đọc trực tiếp nội dung top-10 (một số câu đến top-20) của từng câu mục tiêu. Nội dung lấy qua `asd_rag.v_research_retrieval_chunks` bằng role `research_reader`, chỉ đọc. Không suy luận từ ID hay tiêu đề.
- Mỗi chunk được đối chiếu với nhãn A (gốc) và B (merge), hoặc trạng thái unjudged/needs_adjudication.
- Để tách **lỗi truy xuất** khỏi **khoảng trống corpus**, chạy một **kiểm tra từ khoá toàn corpus** (regex trên cột `content` của view, chỉ đọc).
  - Đây là công cụ kiểm toán, **không phải retriever**: không thêm FTS hay hybrid, không đổi kết quả dense.
  - Kiểm tra từ khoá chỉ cho biết chủ đề **có mặt**. Mức relevant của các chunk tìm được *chưa được chấm*, trừ khi ghi rõ.
- Script tạm: `t233_audit.py` (scratchpad). Kết quả trích dẫn bên dưới.

## Phân loại lỗi
| Mã | Loại |
|---|---|
| RF | Retrieval failure: corpus có bằng chứng đã chấm relevant, nhưng dense không đưa vào top-k |
| CG | Corpus coverage gap: không có nội dung trong corpus |
| AI | Annotation incompleteness: chunk có thể relevant nằm trong top-k nhưng chưa được chấm |
| QL | Query-language mismatch: giả thuyết câu hỏi tiếng Việt khớp kém với văn bản tiếng Anh. **Không kiểm chứng được trong T2.3.3**, vì việc này cần embed truy vấn tiếng Anh, tức là gọi API (bị cấm) |
| BN | Boilerplate/noise |
| CE | Conflicting evidence |
| ND | Chưa đủ dữ liệu để kết luận |

## 1. Tổng hợp theo câu
| Câu | Quan sát (nội dung đã đọc) | Kiểm tra từ khoá corpus | Phân loại |
|---|---|---|---|
| **q033** can thiệp do cha mẹ thực hiện | **Rank 1 là NIMH-ADHD#0008** ("Therapy for children and teens requires parents to play an active role", điều trị ADHD). Rank 2, 4, 9 là bảng can thiệp nuôi dạy **dân số chung** (ASD-NEW-002). Rank 6–8 là quiz WHO-CST. Chunk relevant đầu tiên là CSV-018#0018 (bảng effect size) ở **rank 10**. Năm chunk relevant cốt lõi (CSV-018#0024/#0026 g=0,60/0,52; CSV-011#0017; CSV-089#0030; PMC10774556#0013) **không có trong top-20** | "parent-mediated/-implemented": **36 chunk, 12 nguồn**, chỉ 3 chunk xuất hiện trong bất kỳ top-20 nào. Các abstract CSV-011#0000, CSV-018#0000, CSV-089#0004 đều ngoài top-20 | **RF** (chính), **BN**, QL (giả thuyết: "cha mẹ thực hiện" so với "parent-mediated") |
| **q054** tại nhà vs tại trường | Top-10 có 8 chunk WHO-CST (quiz, đáp án, mẹo tại nhà) và 2 chunk ASD-NEW-002. Relevant đầu tiên ở **rank 17**. Không chunk nào so sánh trực tiếp hai hình thức | Không có so sánh trực tiếp. Bằng chứng riêng cho từng hình thức có: PMI (xem q033) và can thiệp tại trường (CSV-019#0000/#0033, ngoài top-20) | **BN** + **RF** (bằng chứng riêng lẻ không lên top); **CG** cho phần "so sánh trực tiếp" (nhãn partially answerable đúng) |
| **q011** tuổi dậy thì | Top-3 là relevant (PMC12593641#0002; PMC12468522#0020, #0005: camouflaging ở vị thành niên gắn với lo âu, trầm cảm, burnout). PMC12468522#0093 ("pubertal surges in sex steroids can exacerbate ASD symptoms…") ở **rank 11, unjudged** | "pubert": 8 chunk, 3 nguồn; có nội dung riêng ASD (#0093, #0096) | Retrieval **tốt**; **AI** (#0093 chưa chấm). Thiếu nội dung về giới tính và vệ sinh tuổi dậy thì: **ND** (từ khoá không thấy, nhưng chưa tìm hết) |
| **q056** tâm lý tuổi teen | Rank 1–4 là NIMH-TEEN-BRAIN (teen nói chung, grade 1). Chunk riêng ASD ở rank 5–8 (PMC12593641#0002, PMC12620806#0031, PMC12468522#0005, #0020: grade 2–3, **có camouflaging/masking**). #0093 ở rank 11, unjudged | "masking/camouflag": 19 chunk, 7 nguồn (một phần là "masking" theo nghĩa làm mù trong RCT, không liên quan) | **BN nhẹ** (nguồn chung đứng trên nguồn riêng ASD); **AI**. **Đính chính T2.3.2:** báo cáo coverage T2.3.2 (mục 6) ghi "masking" là phần còn thiếu của q056. Điều đó **không đúng**: PMC12468522#0005 (grade 3, nhãn T1) có nói camouflaging ở vị thành niên |
| **q050** 15 tháng chưa nói | Rank 2 = MILESTONES-15#0009 (g2), rank 3 = #0006 (**mốc ngôn ngữ 15 tháng**, g3), rank 10 = CDC-CONCERNED#0001 (g2) | — | Retrieval **tốt**. Nhận định "thiếu" ở T2.3.2 chỉ có nghĩa là pool không thêm nhãn mới, không phải dense trả kết quả kém |
| **q051** chậm phát triển ở 4 tháng | Rank 1, 2, 4, 5 là mốc 4 tháng (g2–3). Rank 6–10 unjudged (giới thiệu trang, mẹo, CDC-ASD-ABOUT) | — | Retrieval **tốt**; **AI** (5 chunk unjudged trong top-10, không có trong pool high) |
| **q063** nhại lời (echolalia) | **Rank 1 và 3 là trang bản quyền "Reprints"** (NIMH-ADHD#0018, TEEN-BRAIN#0008, sim 0,28 và 0,26). Rank 2, 4, 6, 7 là mốc ngôn ngữ hoặc mẹo. Relevant duy nhất trong top-10 là CDC-ASD-SIGNS#0002 ở **rank 5** ("Repeats words or phrases over and over (called echolalia)"). Định nghĩa và chức năng nằm ở NIDCD#0004 (immediate/delayed echolalia, g3) và PMC12468522#0042 (chức năng giao tiếp và tự điều hoà, g3), cả hai **ngoài top-20** | "echolal": 6 chunk, 6 nguồn, đều đã có nhãn relevant | **RF** + **BN** (boilerplate lên rank 1). Top-1 sim 0,28 là thấp nhất trong nhóm answerable. Từ "nhại lời" có thể khớp kém với "echolalia": **QL** (giả thuyết) |
| **q066** động kinh | Top-10 đều grade 0: bệnh đồng mắc **tâm thần** (CSV-088 ×5, CSV-078 ×2), tic và vận động (PMC12620806#0011/#0012), triệu chứng ADHD. **Không có relevant trong top-20 ở cả A và B** | "epilep/seizure": **27 chunk, 15 nguồn**. Các chunk đã chấm relevant: PMC12620806#0008 (g2), #0010 (g3: động kinh kèm triệu chứng lõi nặng hơn), #0009, CDC-ASD-SIGNS#0003 (g2) đều ngoài top-20 | **RF** (nghiêm trọng): embedding gom "bệnh đi kèm" về tâm thần thay vì thần kinh; **QL** (giả thuyết: "động kinh") |
| **q016** joint attention | Rank 1–2 là WHO-CST#0024/#0023 (shared engagement, **needs_adjudication**). Không có relevant đã chấm trong top-20 ở A và B | — | **CE/ND**: nếu chuyên gia xác nhận "shared engagement" ≈ joint attention thì hit@1 = 1. Kết quả của q016 phụ thuộc phân xử |
| **q057** vắc-xin | Xem `dense_eval_q057_sensitivity_2026-11-15.md`. Chunk #0021 ở rank 4 | "vaccin": 4 chunk; chỉ #0021 nói về quan hệ nhân quả (nghiên cứu đã bị rút) | **ND** (chờ phân xử); CG một phần (không có bằng chứng phủ định trực tiếp) |
| q059 tế bào gốc | Top-10 đều grade 0 | "stem cell": **0 chunk** | **CG** thật (nhãn unanswerable đúng) |

## 2. Placeholder hình ảnh (`Image:` / `[Original asset:`)
- **Trong corpus truy xuất được:** 102/2.291 chunk (4,5%) có placeholder. Chỉ **3** chunk gần như chỉ còn placeholder (< 80 ký tự nội dung khác). Nguồn nhiều nhất: ASD-NEW-002 (15), PMC10981608 (7), CSV-011 (7), CSV-020 (6), PMC7726187 (6).
- **Trong kết quả dense (66 câu, nhãn B):**

| Top-K | Lượt có placeholder | Grade 3 / 2 / 1 / 0 / unjudged |
|---|---|---|
| 5 | 23/330 (7,0%) | 3 / 5 / 10 / 5 / 0 |
| 10 | 39/660 (5,9%) | 4 / 8 / 10 / 5 / 12 |
| 20 | 68/1.320 (5,2%) | 4 / 8 / 13 / 5 / 38 |

- **Nhận định:** placeholder **không** phải nguồn nhiễu chính. Phần lớn chunk có placeholder vẫn có nội dung (ví dụ trang CDC "Image: … As your child's first teacher…"). Chỉ 5 lượt grade 0 trong top-10.
  - Rủi ro thật: chunk mô tả hình hoặc biểu đồ mà nội dung số liệu nằm trong hình (ví dụ CSV-018#0023 "Fig. 3 Galbraith Plot… [Original asset…]"). Chunk như vậy được truy xuất nhưng không đủ để trả lời.
  - Theo phạm vi T2.3.3, **không loại bỏ** placeholder. Chỉ báo cáo.

## 3. Nhiễu (grade 0) trong top-10, 66 câu, nhãn B
Có 125 lượt grade 0 trong 660 lượt top-10. Phân nhóm theo `aspect` của nhãn:

| Nhóm | Lượt | Câu bị ảnh hưởng |
|---|---|---|
| Sai chủ đề, sai tuổi, mẹo không liên quan | 85 | 34 câu |
| Bảng, phương pháp, mảnh văn bản | 17 | q011, q015, q041, q042, q044, q054, q057–q060, q066 |
| Sai bệnh (ADHD) | 7 | q004, q006, q033, q038, q066 |
| Quiz/đáp án WHO-CST | 7 | q033, q054 |
| Boilerplate (bản quyền, thư biên tập) | 5 | q021, q063 |
| Dân số chung (bảng can thiệp nuôi dạy) | 4 | q033, q054 |

## 4. Kết luận error analysis
1. **Lỗi truy xuất nghiêm trọng** (corpus có bằng chứng, dense không tìm ra):
   - q066 (động kinh): 0 relevant trong top-20.
   - q033 (PMI): relevant đầu tiên ở rank 10, 5 chunk cốt lõi ngoài top-20.
   - q063 (nhại lời): định nghĩa và chức năng ngoài top-20.
   - q054: rank 17.
2. **Khoảng trống corpus thật:** q059 (tế bào gốc), và phần "so sánh trực tiếp tại nhà vs tại trường" của q054. Không kết luận khoảng trống cho các chủ đề khác chỉ vì dense không tìm thấy: kiểm tra từ khoá cho thấy động kinh, PMI, dậy thì, camouflaging và echolalia **đều có trong corpus**.
3. **Annotation chưa đủ:** nhiều chunk có thể relevant ở rank 6–20 vẫn unjudged, ví dụ PMC12468522#0093 cho q011 và q056.
4. **Nhiễu:** boilerplate và quiz có điểm dense cao với câu hỏi ngắn hoặc mơ hồ (q063, q033, q054).
5. **Query-language mismatch** là giả thuyết hợp lý cho q033, q063, q066 nhưng **chưa kiểm chứng được** trong T2.3.3, vì việc này cần embed truy vấn tiếng Anh, tức là gọi API (bị cấm). Đây là đầu vào cho T2.4: thử nghiệm glossary/FTS theo quyết định C4.
