# Hướng dẫn gán nhãn — Retrieval Evaluation Dataset v1

Áp dụng cho `retrieval_eval_v1.jsonl`. Schema: `retrieval_eval_v1_schema.json`. Validator: `scripts/validate_retrieval_eval.py`.

## 1. Đơn vị gán nhãn
- Mỗi nhãn là một cặp **(câu hỏi, chunk)**.
- Chunk phải thuộc tập đã embed: `eval/reports/embedding_manifest.csv`, gồm 2.338 chunk `section_v2_1`, manifest SHA-256 `542cce21…`.
- Mỗi nhãn lưu kèm `content_sha256`. Nếu nội dung chunk đổi, validator báo "hash drift" và nhãn đó phải gán lại.
- Chunk bị loại khỏi embedding không được gán nhãn. Nếu bằng chứng chỉ nằm ở chunk bị loại, ghi vào `annotation_notes` với mã `evidence_excluded`.

## 2. Thang điểm
| Grade | Khi nào dùng | Ví dụ |
|---:|---|---|
| 3 | Chunk **trực tiếp** cung cấp bằng chứng chính để trả lời | "Dấu hiệu sớm 18 tháng?" → danh sách dấu hiệu theo mốc tuổi của CDC |
| 2 | Đóng góp **đáng kể**, nhưng chưa đủ một mình | Bảng tiêu chí DSM-5 cho câu "hành vi lặp lại gồm gì?" |
| 1 | Chỉ hỗ trợ một phần, hoặc cung cấp ngữ cảnh | Câu "nam gấp 3 lần nữ" cho câu hỏi về tỉ lệ mắc |
| 0 | **Không** đóng góp, kể cả khi trùng từ khóa (đã đọc và xác nhận là âm tính) | "MMRM" (phương pháp thống kê) khi câu hỏi về vắc-xin MMR; chunk danh mục tham khảo |
| -1 | Chunk **liên quan** nhưng mâu thuẫn với bằng chứng khác (grade ≥ 2) của cùng câu hỏi, hoặc cần đối chiếu khác biệt ngữ cảnh (nhóm con, định nghĩa kết quả) | Tổng quan ASI "đạt tiêu chí EBP" so với RCT SenITA "không hiệu quả" |

Quy tắc bắt buộc:
- **Phải đọc nội dung chunk.** Không chấm điểm dựa trên tiêu đề tài liệu, heading, độ tương đồng hay số lần khớp từ khóa.
- Không đánh đồng "tài liệu nói về ASD" với "chunk trả lời câu hỏi".
- Hai chunk khác độ tuổi (mốc 18 tháng và 24 tháng) không thay thế được cho nhau. Chunk sai độ tuổi được gán 0 với `aspect = hard_negative_wrong_age`.
- Grade -1 chỉ dùng khi đã đọc đủ cả hai phía. Một câu "nghiên cứu đơn ca cho thấy hiệu quả, nhưng tổng quan nói chưa đủ bằng chứng" nằm trong **cùng một** chunk thì **không** phải -1, vì bản thân chunk đã cân bằng hai phía.
- Ghi `rationale_vi` (một câu) cho mọi nhãn, kể cả nhãn 0.

## 3. Lớp bằng chứng và mức độ tin cậy
| Khái niệm | Trong dataset |
|---|---|
| Relevant (đưa vào phép tính nhị phân) | grade ≥ 2 → `relevant_chunk_ids` |
| Partial | grade 1 (chỉ dùng cho nDCG) |
| Negative (đã xác minh) | grade 0 |
| Conflicting | grade -1 (gain = 2 trong nDCG; báo cáo riêng; được tính là bằng chứng bắt buộc cho khía cạnh "mâu thuẫn") |
| Candidate (đã pool nhưng chưa chấm) | `candidate_chunk_ids`. **Không bao giờ** đưa vào gold |
| Unanswerable | `answerability = unanswerable`, không có `relevant_chunk_ids` |

Mức độ tin cậy của cả bản ghi (`label_tier`):
- `candidate`: chưa gán nhãn.
- `silver_single_annotator`: một người hoặc mô hình gán, đã đọc nội dung. **Đây là mức hiện tại của v1.**
- `gold_human_verified`: phải có ít nhất 1 người đánh giá là con người. Nếu có 2 người thì phải qua bước adjudication.

## 4. Trạng thái
`annotation_status` nhận một trong các giá trị:
- `pending_annotation`;
- `annotated_single`;
- `adjudicated`;
- `verified_unanswerable`;
- `not_applicable` (câu ngoài luồng `expert_qa`).

`annotation_completeness` nhận một trong các giá trị:
- `complete_for_judged_pool`: mọi ứng viên trong pool đã được chấm. Recall so với các chunk chưa vào pool **vẫn chưa biết**.
- `partial`: pool còn thiếu đã biết. Không dùng cho metric recall.

## 5. Quy trình
1. **Pooling.**
   - v1 dùng: tìm kiếm từ khóa nhiều mẫu (tiếng Anh, có từ đồng nghĩa), cộng với **duyệt toàn bộ chunk** của các nguồn có khả năng liên quan. Ghi vào `search_log`.
   - Từ T2: thêm hợp top-20 của các cấu hình A, B, C (dense, FTS, hybrid). Chunk mới đưa vào `candidate_chunk_ids` cho tới khi được chấm.
2. **Đọc và chấm** theo mục 2. Với chunk dài, đọc đủ phần liên quan, không dựa trên đoạn trích ngắn.
3. **Âm tính có chủ đích:** mỗi câu nên có ít nhất 1 grade 0 lấy từ các chunk khớp từ khóa nhưng không trả lời (hard negative).
4. **Câu nhiều khía cạnh:** đặt `aspect = aspect_<tên>` và bảo đảm mỗi khía cạnh trong `evidence_requirements` có ít nhất một chunk grade ≥ 2, hoặc ghi rõ khía cạnh nào thiếu.
5. **Câu blocked hoặc unanswerable:** vẫn chấm các chunk dễ gây dương tính giả (grade 0) để đo hành vi của evidence gate.
6. **Hai người đánh giá (khi có):**
   - Mỗi người chấm độc lập; không xem nhãn của người kia.
   - Tính tỉ lệ đồng thuận và weighted Cohen's κ (trọng số tuyến tính, thang -1…3; -1 tính riêng).
   - Ghi các trường hợp bất đồng vào `phase_6_2_t1_unresolved_annotations_*.md`.
   - Người thứ ba hoặc chuyên gia quyết định cuối; khi đó `annotation_status = adjudicated`.
   - **Không** tự tạo số liệu đồng thuận khi chưa có hai lần chấm độc lập.
7. **Câu y khoa có xung đột hoặc liên quan thuốc:** cần chuyên gia ASD duyệt trước khi nâng lên gold.

## 6. Không được làm
- Bịa `chunk_id`. Validator đối chiếu với manifest và hash nội dung.
- Đưa chunk chưa chấm vào `relevant_chunk_ids`.
- Đánh dấu `gold_human_verified` khi không có người đánh giá là con người.
- Ghi câu hỏi thật của người dùng, thông tin cá nhân hoặc secret vào dataset (validator quét email, số điện thoại, chuỗi giống key).
- Thêm câu hỏi chỉ để làm đẹp metric (câu quá dễ, câu trùng lặp).
