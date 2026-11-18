# Phase 6.2 – T2.3.2: Annotation Quality Report — 2026-11-14 (chạy 14–15/11/2026)

## 1. Người chấm và giới hạn
- **Một annotator duy nhất: A1, mô hình AI (`claude-opus-5-5`)**, cùng annotator đã gán nhãn T1. **Không có người chấm.** Vì vậy không tính được kappa hay độ đồng thuận giữa người chấm.
- Mọi nhãn mới là **silver**, không có nhãn gold. Grade 2–3 nghĩa là "relevant theo A1", chưa phải gold đã xác minh.
- Rủi ro thiên lệch xác nhận: A1 vừa viết câu hỏi và phạm vi trả lời (T1), vừa chấm. Một số ca biên đã được đưa vào `needs_adjudication` thay vì quyết định một mình.

## 2. Quy trình chấm
- **Đơn vị chấm** là cặp (câu hỏi, chunk). Một chunk được chấm lại độc lập cho từng câu hỏi; nhãn của câu khác không được dùng lại.
- **Đọc toàn văn.** Snapshot 696 chunk lấy qua `v_research_retrieval_chunks` bằng role `research_reader`. Mỗi chunk được kiểm hash với manifest (0 lệch).
- **Chấm mù rank và điểm.** Trình xem `judge_view.py` ẩn rank và cosine, sắp chunk theo `chunk_id`.
  - Giới hạn: lô ưu tiên `high` tương ứng rank ≤ 5 (hoặc ≤ 10 với câu unanswerable/refusal), nên A1 biết mọi chunk trong lô nằm ở top đầu, dù không biết thứ tự.
  - Rank chỉ được ghi vào `origin` sau khi chấm, để truy vết.
- **Không chấm theo tiêu đề, không suy diễn y khoa ngoài văn bản.** Rationale tiếng Việt ngắn, kiểm chứng được bằng cách đọc lại chunk.
- **Thứ tự chấm theo yêu cầu:**
  1. Toàn bộ 246 ứng viên `high`.
  2. Toàn bộ pool của q033 và q054.
  3. Các câu chủ đề yếu: ứng viên `medium` của q011, q015, q034, q041, q042, q056.
  4. Hai câu không tìm thấy bằng chứng mới ở lô high: ứng viên `medium` của q063, q066.

## 3. Quy tắc nhất quán đã áp dụng
| Tình huống | Grade | Ví dụ |
|---|---|---|
| Trả lời trực tiếp ý chính của câu hỏi | 3 | SENITA#0243 (xác suất chi phí–hiệu quả); SENITA#0045 (ASI khác can thiệp cảm giác khác) |
| Trả lời một khía cạnh trong phạm vi | 2 | CDC-MILESTONES-02#0009 (hành động sớm, sàng lọc) |
| Bối cảnh, gián tiếp, hoặc **dân số chung** (không riêng ASD) | 1 | NIMH-TEEN-BRAIN (teen nói chung); ASD-NEW-002 phần văn bản (can thiệp nuôi dạy cho dân số chung) |
| Sai bệnh, bảng mô tả, danh mục, phản biện, bản quyền, câu đố, mẹo không liên quan | 0 | NIMH-ADHD với câu hỏi về tự kỷ; bảng đặc điểm nghiên cứu ASD-NEW-002; đáp án quiz WHO-CST |
| Mâu thuẫn với chunk khác hoặc với kết luận chính | −1 (chỉ tạm, cần phân xử) | SENITA#0309 (lợi ích cảm nhận vs RCT không hiệu quả) |
| Câu hỏi ngoài phạm vi (q062) | — (`excluded`) | 5 ứng viên |

- **Câu unanswerable/refusal:** grade nói chunk có trả lời được câu hỏi hay không, không đánh giá chủ đề lân cận.
  - q058 (liều risperidone): 9 chunk về liều *thuốc khác* đều grade 0. Đây là hard negative quan trọng cho evidence gate sau này.
  - q059 (tế bào gốc): 0 chunk liên quan; một chunk bối cảnh grade 1 ("không có thuốc điều trị triệu chứng lõi").
- **Không đổi nhãn cũ.** Không có cặp nào trùng giữa pool và nhãn T1 (đã kiểm ở audit), nên không có xung đột cần hoà giải.

## 4. Phân bố nhãn mới (303 judged)
| Nhóm câu (T2.3.1) | 3 | 2 | 1 | 0 | Tổng |
|---|---|---|---|---|---|
| answerable | 29 | 53 | 64 | 58 | 204 |
| answerable_partial_pool | 1 | 4 | 2 | 2 | 9 |
| conflicting | 2 | 5 | 18 | 28 | 53 |
| unanswerable | 0 | 0 | 1 | 18 | 19 |
| refusal | 0 | 1 | 3 | 14 | 18 |
| **Tổng** | **32** | **63** | **88** | **120** | **303** |

Thêm 4 dòng `needs_adjudication` (tạm: 2, 2, −1, 1) và 5 dòng `excluded`.

**Theo ưu tiên:**

| Ưu tiên | 3 | 2 | 1 | 0 |
|---|---|---|---|---|
| high | 29 | 53 | 70 | 85 |
| medium | 3 | 9 | 9 | 25 |
| low | 0 | 1 | 9 | 10 |

Tỷ lệ relevant giảm rõ khi rank tăng: 95 nhãn mới grade ≥ 2 nằm ở rank 1–5 (81), 6–10 (13) và 11–20 (1).

## 5. Hard negative (120 nhãn grade 0)
| Loại | Ví dụ | Ý nghĩa cho T2.3.3 trở đi |
|---|---|---|
| Sai bệnh (ADHD) | NIH-NIMH-ADHD: 8 nhãn 0 ở 6 câu (q004, q006, q033, q038, q063, q066) | Dense nhầm ADHD với ASD; cần evidence gate hoặc lọc chủ đề |
| Dân số chung, dạng bảng | ASD-NEW-002: 12 bảng can thiệp nuôi dạy | Từ khoá "parenting intervention" kéo về tài liệu không phải ASD |
| Câu đố, mẫu dịch vụ, bản quyền, thư biên tập | WHO-CST-PARTICIPANTS (15 nhãn 0, phần lớn là quiz/đáp án), NIMH reprints, thư biên tập PLOS | Chunk ít thông tin nhưng điểm dense cao |
| Liều thuốc khác cho câu refusal | ASD-CSV-095, PMC7407189 (q058) | Rủi ro trả lời kê đơn sai thuốc nếu không có gate |
| Mốc phát triển sai độ tuổi hoặc lĩnh vực | CDC-MILESTONES-*: mẹo hoạt động | Câu hỏi theo tuổi bị kéo về trang mốc khác |

## 6. Kiểm soát chất lượng đã làm
- **Kiểm tra máy:** 14 kiểm tra trong validator; rationale có ở 312/312 dòng có quyết định.
- **Dùng lại quy tắc cũ:** cùng chunk ASD-NEW-002 dạng bảng thì cùng grade 0 cho q033 và q054; cùng loại văn bản ASD-NEW-002 thì grade 1, như quy tắc đã dùng ở q033 (b09).
- **Ca biên được tách ra, không ép grade:** 4 dòng trong `phase_6_2_t2_3_2_unresolved_adjudications_2026-11-14.csv`. Đặc biệt q057: chunk có thể làm đổi nhãn unanswerable của câu hỏi.

**Chưa làm:**
- Chấm lại mẫu bởi người.
- Chấm lại sau một khoảng thời gian (test–retest).

**Đề xuất:** người chấm thứ hai (human) chấm mù một mẫu phân tầng khoảng 60 nhãn: 20 grade 3–2, 20 grade 1, 20 grade 0. Ưu tiên các câu nhóm conflicting và refusal. Sau đó tính Cohen's kappa có trọng số trước khi coi bất kỳ nhãn nào là gold.

## 7. Giới hạn đã biết
1. Chỉ có một annotator AI. Không có kappa và không có gold.
2. **Thiên lệch pool:** mọi nhãn mới đến từ top-20 của dense. Nhãn mới làm lợi cho dense khi so với retriever khác (FTS/hybrid) nếu các retriever đó không được pool và chấm tương đương.
3. Còn 791 ứng viên `unjudged` (214 medium, 577 low). Recall trên các câu này vẫn là cận dưới, và chunk relevant ngoài pool chưa được biết.
4. Grade 1 cho tài liệu dân số chung là quy ước dự án, không phải chân lý lâm sàng. Chuyên gia có thể muốn grade 0 (không áp dụng cho ASD) hoặc grade 2 (bằng chứng gián tiếp hợp lệ).
5. Biết trước "lô high = top đầu" có thể khiến A1 nghiêng về chấm relevant. Phân bố ở mục 4 (85/237 grade 0 trong lô high) cho thấy không có xu hướng chấm dễ rõ rệt, nhưng chưa được kiểm chứng độc lập.
