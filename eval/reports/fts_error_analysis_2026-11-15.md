# T2.4 — FTS Error Analysis — 2026-11-15

## Phương pháp
- Đọc trực tiếp nội dung top-10 qua view, bằng role reader, chỉ đọc. Danh sách xếp hạng lấy từ `fts_run_record_2026-11-15.json`.
- Mỗi chunk được đối chiếu với nhãn gốc (O) và nhãn merge (M). `O-/M-` = **chưa chấm**. Chunk chưa chấm **không** được kết luận là sai hay đúng.
- Rank relevant ghi bên dưới là rank của chunk **đã được chấm** grade ≥ 2. Nếu trước nó có chunk chưa chấm thì rank thật có thể còn tốt hơn.
- Vì nhãn thiên lệch về dense, mọi so sánh ở đây chỉ mang tính **mô tả từng ca**, không phải kết luận về hệ thống nào tốt hơn.

## 1. Bốn ca bắt buộc
| Câu | Dense (T2.3.1) | FTS-B (glossary, AND) | FTS-C (glossary, OR) | Phụ thuộc glossary | Đánh giá |
|---|---|---|---|---|---|
| **q066** động kinh | 0 relevant đã chấm trong top-20; top-10 là bệnh đồng mắc tâm thần, tic, ADHD | tsquery `(autism ∣ autist ∣ asd) & (epilepsi ∣ epilept ∣ seizur<->disord)`. **Rank 1–3** là PMC12620806#0009 (g2), #0010 (g3), #0008 (g2); rank 10 là CDC-ASD-SIGNS#0003 (g2). Rank 4–9 chưa chấm (PMC12620806#0003/#0004/#0014 có nhắc động kinh; PMC12468522#0053; bảng PMC4271434#0013; CSV-007#0005 là tiêu chí loại trừ có chữ "epilepsy"). 17 kết quả | Rank 1 và 3 relevant. Rank 2 là PMC4742252#0030 (đi lạc: false positive do "autism" OR); rank 4–5, 7, 9–10 là chunk chung về ASD hoặc ADHD (chưa chấm) | **Hoàn toàn:** "động kinh" → epilepsy. Không có glossary thì FTS-A ra 0 kết quả | **Cải thiện rõ trên nhãn hiện có**: recall@10 tăng 0 → 1,0 (B) |
| **q033** can thiệp do cha mẹ thực hiện | Rank 1 = NIMH-ADHD#0008 (g0); relevant gốc đầu tiên ngoài top-20; relevant merge đầu tiên ở rank 10 | tsquery cụm `parent-mediated/-implemented (intervention)` & `effective ∣ effectiveness ∣ efficacy`. **Không có chunk ADHD.** Rank 1–2 là CSV-089#0041/#0039 (tổng quan can thiệp do cha mẹ thực hiện qua từ xa: "preliminary evidence… can assist in improving social behavior and communication"), **chưa chấm**. Rank 5 là PMC10774556#0013 (g2). Rank 6 là CSV-018#0023 (omnibus Hedges' g, chưa chấm). False positive: WHO-CST-INTRO#0012, PMC9399988#0039 (SST tuổi teen), PMC7407189#0008 (giấc ngủ) | Có CSV-011#0022 ("30 RCTs of PMIs… clinically relevant effect", chưa chấm) ở rank 5. Top-3 là bảng effect size của AAC (CSV-017#0009, CSV-084#0039) và WHO-ECD: false positive từ "effect/efficacy" | **Hoàn toàn**: cụm "do cha mẹ thực hiện" | **Có dấu hiệu cải thiện** (ADHD biến mất, PMI lên top), nhưng **phần lớn chưa chấm**. Cần chấm mù trước khi kết luận |
| **q063** nhại lời | Rank 1 và 3 là trang "Reprints"; relevant đầu tiên ở rank 5; NIDCD#0004 và PMC12468522#0042 ngoài top-20 | Chỉ **6 kết quả**, đúng 6 chunk chứa "echolalia" trong corpus: rank 1 NIDCD#0004 (g3), 2 CDC-ASD-SIGNS#0002 (g3), 3 NIMH-ASD-2025#0001 (g2), 4 PMC10900867#0005 (g1), 5 PMC12468522#0042 (g3), 6 CDC-ASD-CLINICAL#0006 (g2). **Coverage 100%, không có boilerplate** | Giống B (chỉ một khái niệm) | **Hoàn toàn**: "nhại lại lời" → echolalia. Các biến thể "repeat(s/ing) words" không thêm kết quả nào | **Cải thiện rõ**: relevant ở rank 1, recall@10 tăng 0,2 → 1,0 |
| **q054** tại nhà vs tại trường | Top-10 là quiz WHO-CST; relevant merge đầu tiên ở rank 17 | 4 khái niệm AND (`intervention`, `home`, `parent`, `school`). Top-10 là **trích đoạn phỏng vấn SENITA** (×6), bảng NEW-002 (M0), bảng tổng quan. Không có relevant đã chấm. False positive do câu kể chuyện chứa đủ 4 từ | CSV-089 (can thiệp do cha mẹ thực hiện), CSV-020#0016 (can thiệp trong lớp học chính khoá, chưa chấm), NEW-003#0044 (M2, rank 7) | Có: các từ phổ biến "home/school/parent" | **Không cải thiện** với B. C đưa một số bằng chứng riêng lẻ lên. Corpus vẫn không có so sánh trực tiếp |

## 2. Các câu khác đáng chú ý
- **q016 (joint attention):** FTS-B/C có relevant đã chấm ở **rank 2**; dense không có trong top-20. Câu này vẫn chờ phân xử (2 chunk WHO-CST), **không sửa nhãn**.
- **q011, q050, q051, q056:** dense đã truy xuất tốt (theo đính chính T2.3.3). FTS **kém hơn** ở các câu này:
  - B trả 0 kết quả (q050, q051) hoặc 1 kết quả (q011);
  - C không có relevant đã chấm trong top-20.
  - Lý do: AND với cụm tuổi (`15 months`, `4 months`) và khái niệm chung. Đây không phải lỗi truy xuất của dense.
- **q057, q059 (unanswerable), q058 (refusal):**
  - B trả 2, 0, 0 kết quả. `stem cell` có 0 chunk trong corpus (khớp T2.3.3); `cure` chỉ 3 chunk.
  - C trả 20 kết quả nhưng chủ yếu do "autism".
  - Số kết quả rỗng hoặc ít của FTS-B có thể là tín hiệu "thiếu bằng chứng". Đây chỉ là giả thuyết cho evidence gate sau này, **chưa được kiểm định**.
- **FTS-B trả 0 kết quả** ở 11 câu: q004, q007, q034, q050, q051, q052, q058–q062. Nguyên nhân là AND với khái niệm hiếm hoặc vắng (`cure` 3, `early signs` 5, `caregiver skills training` 11, tuổi + "talk") hoặc câu nhiều khái niệm (q052 có 6). Riêng q034 còn vì `WHO` là từ dừng.

## 3. Nguồn false positive đã xác định (FTS)
| Nguyên nhân | Ví dụ |
|---|---|
| OR với khái niệm chung (C) | "autism" (719 chunk) lấn át: PMC4742252#0030 (đi lạc) ở rank 2 của q066 |
| Từ dừng hoặc stem làm cụm thành quá rộng | `lining up` thành `line` (60 chunk); `WHO` thành rỗng; `ADOS` thành `ado` |
| Từ phổ biến cùng xuất hiện trong văn kể chuyện | Trích đoạn phỏng vấn SENITA cho q054 (đủ parent/home/school/intervention) |
| Từ đa nghĩa | `point` (230 chunk: "at this point") cho q052; `effect/efficacy` kéo bảng effect size của chủ đề khác (q033, C) |
| Chunk tiêu chí loại trừ hoặc bảng | CSV-007#0005 ("…neurological disorders such as epilepsy… were excluded") ở rank 9 của q066 (B) |

## 4. Phân loại tổng hợp
| Câu | Dense | FTS-B | Ghi chú |
|---|---|---|---|
| q066 | Lỗi truy xuất | **Tìm được bằng chứng** (rank 1) | Phụ thuộc glossary |
| q063 | Lỗi truy xuất + boilerplate | **Tìm được bằng chứng** (rank 1, 6/6 chunk) | Phụ thuộc glossary |
| q033 | Lỗi truy xuất + nhiễu ADHD | Có dấu hiệu tìm được bằng chứng; phần lớn **chưa chấm** | Cần chấm mù |
| q054 | Nhiễu + khoảng trống corpus | Nhiễu (trích đoạn phỏng vấn) + khoảng trống corpus | Không cải thiện |
| q016 | Chờ phân xử | Relevant ở rank 2 | Chờ phân xử |
| q011, q050, q051, q056 | Tốt | **Kém** (0–1 kết quả hoặc không có relevant trong top-20) | AND với tuổi/khái niệm chung |

**Kết luận:** dense và FTS **bổ trợ nhau** theo từng câu: overlap top-20 thấp, Jaccard trung bình dense–FTS-B 0,13. Nhưng **không thể** kết luận hệ thống nào tốt hơn khi chưa chấm mù pool chung.
