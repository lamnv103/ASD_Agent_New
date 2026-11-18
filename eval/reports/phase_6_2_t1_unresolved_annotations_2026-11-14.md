# Phase 6.2 – T1: Unresolved Annotations — 2026-11-14

Toàn bộ nhãn v1 là **single-annotator**: một lượt duy nhất, do mô hình AI (claude-opus-5-5) thực hiện sau khi đọc nội dung chunk. **Chưa có người đánh giá nào là con người**, nên không có inter-annotator agreement và không có nhãn gold. Chi tiết theo từng câu nằm trong [retrieval_eval_v1_annotation_status.csv](../datasets/retrieval_eval_v1_annotation_status.csv).

## 1. Cần adjudication (chuyên gia / chủ dự án) — 6 câu
| Câu | Vấn đề | Cần quyết định |
|---|---|---|
| q041 Liệu pháp điều hoà cảm giác có hiệu quả? | RCT SenITA (không hiệu quả có ý nghĩa, không chi phí–hiệu quả) và tổng quan AAP/SI-SP (bằng chứng hạn chế) **đối lập** với tổng quan ASI (đạt tiêu chí EBP) | Xác nhận nhãn -1 cho `ASD-SUP-PMC6590432#0033/#0035`. Câu trả lời mong đợi phải trình bày cả hai phía |
| q033 Can thiệp do cha mẹ thực hiện có hiệu quả? | ASD-CSV-011 (cải thiện nhỏ, không hiệu quả theo đánh giá lâm sàng) và ASD-CSV-018 (g ≈ 0,5–0,6) | Mức hiệu quả nào là kết luận chính; xác nhận nhãn -1 |
| q054 Nên ưu tiên tại nhà hay tại trường? | Không có so sánh trực tiếp; một chunk -1 | Giữ câu này, hay đổi thành `partially_answerable` thuần |
| q060 GFCF có chữa tự kỷ? | "Chưa được chứng minh" (PMC12620806) và "cải thiện hành vi ở nhóm con có GI" (NEW-003) | Xác nhận nhãn -1 và trạng thái `conflicting` |
| q058 Liều risperidone? | Gán `blocked` (kê đơn) | Chính sách: blocked hay insufficient + chuyển bác sĩ |
| q061 "Con tôi có bị tự kỷ không?" | Gán `blocked` (chẩn đoán cá nhân) kèm thông tin chung | Phạm vi được phép trả lời |

## 2. Pool chưa đầy đủ (`annotation_completeness = partial`) — 4 câu, không dùng cho recall
| Câu | Thiếu gì | Cách xử lý ở T2/T5 |
|---|---|---|
| q010 | Chưa đọc hết phần thân ASD-NEW-001 (mô tả dấu hiệu ở trẻ sơ sinh) | Pool từ top-20 của A/B/C rồi chấm bổ sung |
| q040 | Lợi ích học bơi mới xét ở mức tóm tắt | như trên |
| q057 Vắc-xin | Sự vắng mặt bằng chứng mới kiểm bằng từ khóa | Kiểm lại bằng pool dense; nếu vẫn không có thì giữ `unanswerable` |
| q059 Tế bào gốc | như q057 | như q057 |

## 3. Bằng chứng nằm ở chunk bị loại khỏi embedding
| Câu | Chunk bị loại | Ảnh hưởng |
|---|---|---|
| q021 hành vi thách thức | 14 chunk thân bài session 7 WHO-CST-PARTICIPANTS (`unclassified`) | Chỉ còn bản tóm tắt mẹo (`#0146`). Đề xuất duyệt thủ công 32 chunk `unclassified` |
| q011, q056 tuổi dậy thì | Phần thân ASD-OA-PMC12593641 (chỉ 6 chunk tóm tắt/kết luận trong tập embed) | Bằng chứng mỏng; cần kiểm tra lý do bị loại |

## 4. Bằng chứng mỏng hoặc gián tiếp (giữ trong dataset, đánh dấu partially_answerable)
- q006: chủ yếu 1 tổng quan và 1 bài đánh giá.
- q012: không có câu nói trực tiếp về thoái lui.
- q016: không có chunk định nghĩa joint attention.
- q023: không có bằng chứng về tác động lên việc học.
- q042: phải ghép từ nhiều chunk.
- q051: CDC không liệt kê "dấu hiệu chậm".
- q002: số liệu Mỹ là bản cũ (1/54, tài liệu NIDCD 2020). Câu trả lời phải nêu năm và nguồn.

## 5. Phát hiện chất lượng dữ liệu (ảnh hưởng T2, không sửa trong T1)
1. **47 chunk danh mục tài liệu tham khảo nằm trong tập embed**:
   - ASD-CSV-017: 27 chunk; ASD-CSV-018: 20 chunk.
   - Heading "*Indicates studies included in the systematic review", `section_type = body`.
   - Bộ phát hiện References của chunker đã bỏ sót chúng.
   - Chúng khớp từ khóa với nhiều câu hỏi (q016 joint attention, q023 "Special Interest Groups") và là nguồn dương tính giả. 4 chunk như vậy đã được gán grade 0 như hard negative.
   - Đề xuất: authorization mới loại các chunk này (xem T0, D-1). Không re-chunk.
2. **Chú thích hình/forest plot** (ASD-NEW-002 `#0068`, `#0073`) và **placeholder hình** là chunk ít giá trị, khớp từ khóa.
3. **Footer trang CDC** ("Updates may include minor edits…") và **câu tự kiểm tra** trong sổ tay WHO ("check your answers") đã được gán grade 0 ở các câu liên quan.
4. **Dương tính giả lexical:** "MMRM" khớp "MMR"; "Immunization" xuất hiện trong tên phòng ban WHO; bảng liều melatonin xuất hiện khi hỏi liều risperidone.

## 6. Độ phủ còn thiếu
- **11/71 nguồn chưa có chunk relevant nào:**
  - ASD-CSV-091;
  - ASD-OA-PMC4271434;
  - CDC-MILESTONES-06, -12, -18, -30, -36;
  - NIH-NIMH-ADHD, -MEDICATIONS, -TEEN-BRAIN, -TEEN-DEPRESSION.
  - Một số đã được chấm (chẳng hạn MILESTONES-18 làm hard negative sai tuổi; MEDICATIONS ở grade 1).
- Theo nhóm nguồn: A 60/71, B 13/13, C 13/18.
- **Nhóm câu hỏi mỏng:**
  - `aac_communication_support` có 2 câu, `multi_source` (chính) có 1 câu;
  - `query_style = synonym` có 4 câu, `long` 7, `age_specific` 7;
  - các mốc tuổi 6, 12, 18, 30, 36 tháng chưa có câu riêng.
- Lý do của các khoảng thiếu trên: chưa viết thêm câu hỏi, vì ưu tiên nhãn đúng hơn số lượng.

## 7. Hạn chế phương pháp
- **Thiên lệch pooling:** ứng viên được lấy bằng từ khóa tiếng Anh cộng duyệt nguồn, nên các chunk diễn đạt khác hẳn có thể bị sót. Nhãn hiện tại thiên về lexical, nên có thể ưu ái cấu hình B (FTS) khi so sánh. **Bắt buộc** mở rộng pool bằng top-20 của A, B, C ở T5 và chấm bổ sung trước khi so sánh cấu hình.
- **Một người gán, là AI:** cần người đánh giá kiểm lại ít nhất các câu ưu tiên `high` (12 câu) và một mẫu ngẫu nhiên của các câu `low`, rồi mới nâng lên gold.
