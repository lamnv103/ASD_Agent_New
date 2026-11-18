# T2.3.3: q057 (vắc-xin) — trạng thái và phân tích độ nhạy — 2026-11-15

**Kết luận: CHƯA giải quyết, chờ phân xử.** Nhãn q057 được giữ nguyên: `unanswerable` / `insufficient`, nhóm T2.3.1 = `unanswerable`. Không có file dataset nào bị sửa. Giả định "answerable" bên dưới chỉ tồn tại trong bộ nhớ của script đánh giá.

## 1. Câu hỏi và bằng chứng đã đọc
- **Câu hỏi:** "Vắc-xin có gây tự kỷ không?"
- **Phạm vi trả lời T1:** "Corpus không có bằng chứng → insufficient, không suy diễn".
- **Kiểm tra từ khoá toàn corpus** (role `research_reader`, đọc qua view, regex `vaccin`): có **4 chunk**. Chỉ 1 chunk nói về quan hệ vắc-xin và tự kỷ:

| Chunk | Nội dung | Có trả lời câu hỏi? |
|---|---|---|
| ASD-OA-PMC12620806#0021 (rank 4 trong top-20 dense) | "…the firestorm of controversy surrounding the alleged role of routine childhood vaccinations in autism and GI tract dysfunction, infamously suggested in a now retracted study…" | **Một phần.** Nói giả thuyết đến từ một nghiên cứu *đã bị rút*. Không nêu kết luận dịch tễ (ví dụ "không có liên quan nhân quả") và không dẫn nghiên cứu phủ định |
| ASD-OA-PMC12620806#0034 | Tỷ lệ tiêm phế cầu/cúm thấp ở người tự kỷ | Không |
| ASD-OA-PMC13393316#0001 | Thanh thiếu niên tự kỷ ít được tiêm cúm hằng năm | Không |
| WHO-ECD-GUIDELINE-2020#0023 | Tên phòng ban "Immunization, Vaccines and Biologicals" | Không |

**Hai cách đọc chunk #0021, cả hai đều có lý:**
- (a) Đủ để trả lời có kiểm soát: "giả thuyết xuất phát từ một nghiên cứu đã bị rút". Khi đó q057 thành `partially_answerable`.
- (b) Không đủ: chunk không khẳng định vắc-xin không gây tự kỷ, nên trả lời từ chunk này dễ thành suy diễn. Khi đó giữ `unanswerable`.

Đây là quyết định về chính sách câu trả lời y khoa, thuộc về chủ dự án hoặc chuyên gia lâm sàng, không phải người đánh giá retrieval. Mục q057 trong `phase_6_2_t2_3_2_unresolved_adjudications_2026-11-14.csv` vẫn mở.

## 2. Kết quả dense cho q057 (nhãn hiện hành)
- Top-1 cosine similarity là **0,3585**. Giá trị này nằm trong khoảng của câu answerable (T2.3.1: trung vị 0,464, khoảng 0,280–0,592), nên **điểm dense không tách được câu không trả lời được**.
- Top-10 gồm:
  - 9 chunk grade 0: bối cảnh Việt Nam, dioxin, tic, tự miễn, bảng;
  - chunk #0021 ở **rank 4**, trạng thái `needs_adjudication`.
- Không có nhãn relevant ở cả A và B, nên q057 không đóng góp vào recall/MRR.

## 3. Độ nhạy: hai giả định
Script `scripts/dense_eval_t2_3_3.py` tính lại nhóm chính (answerable). Giả định answerable dùng chunk #0021 với grade giả định 2.

| Giả định | Run | Số câu | Recall@5 | Recall@10 | Recall@20 | Hit@5 | Hit@10 | MRR | nDCG@10 | Cov@10 |
|---|---|---|---|---|---|---|---|---|---|---|
| q057 unanswerable (nhãn hiện hành) | A original | 55 | 0,348 | 0,491 | 0,646 | 0,836 | 0,909 | 0,585 | 0,440 | 0,271 |
| q057 answerable (giả định) | A original | 56 | 0,359 | 0,500 | 0,652 | 0,839 | 0,911 | 0,579 | 0,440 | 0,284 |
| q057 unanswerable (nhãn hiện hành) | B merged | 55 | 0,473 | 0,607 | 0,716 | 0,964 | 0,964 | 0,782 | 0,608 | 0,642 |
| q057 answerable (giả định) | B merged | 56 | 0,482 | 0,614 | 0,721 | 0,964 | 0,964 | 0,772 | 0,605 | 0,648 |

Với q057 được giả định là answerable:
- Recall@5/10 = 1,0, vì chỉ có 1 chunk relevant và nó nằm ở rank 4.
- MRR = 0,25.

**Ảnh hưởng tới số liệu tổng là nhỏ:** |Δ| ≤ 0,012 cho recall, ≤ 0,010 cho MRR, ≤ 0,003 cho nDCG@10. Tất cả nằm trong khoảng CI95 bootstrap của nhóm chính. Không kết luận nào của T2.3.3 thay đổi theo giả định này.

## 4. Việc cần làm
- Chủ dự án hoặc chuyên gia quyết định (a) hay (b).
  - Nếu (a): tạo **phiên bản dataset mới** (không sửa `retrieval_eval_v1.jsonl` hay file merge). Đổi answerability của q057 và ghi chunk #0021 là judged.
  - Ở T2.4, nhóm unanswerable chỉ còn q059. Với q059, kiểm tra từ khoá cho 0 chunk về tế bào gốc, nên đây là khoảng trống corpus thật.
- Bất kể quyết định nào, q057 là ca kiểm thử tốt cho evidence gate sau này. Điểm dense không phân biệt được "có nhắc tới" với "có bằng chứng trả lời".
