# Phase 6.2 – T1: Retrieval Evaluation Dataset v1 — 2026-11-14

**Trạng thái T1: COMPLETED (silver).**

| Hạng mục | Tình trạng |
|---|---|
| Dataset | Hợp lệ, có phiên bản và schema |
| Hướng dẫn gán nhãn, trạng thái nhãn | Có |
| Validator | Pass |
| Danh sách vấn đề chưa giải quyết | Có |
| Nhãn | **Single-annotator (AI), đã đọc nội dung, chưa có người xác minh** → silver, chưa phải gold |
| Kết luận cho T2 | **READY WITH CONDITIONS** (mục 8) |

## 1. Artifact
| File | Nội dung |
|---|---|
| [`eval/datasets/retrieval_eval_v1.jsonl`](../datasets/retrieval_eval_v1.jsonl) | 66 câu, 435 nhãn chunk (SHA-256 `7704bb51…`) |
| [`eval/datasets/retrieval_eval_v1_schema.json`](../datasets/retrieval_eval_v1_schema.json) | JSON Schema 2020-12, thang điểm, gain cho metric |
| [`eval/datasets/retrieval_eval_v1_annotation_guidelines.md`](../datasets/retrieval_eval_v1_annotation_guidelines.md) | Hướng dẫn gán nhãn |
| [`eval/datasets/retrieval_eval_v1_annotation_status.csv`](../datasets/retrieval_eval_v1_annotation_status.csv) | Trạng thái, vấn đề mở, ưu tiên duyệt cho từng câu |
| [`phase_6_2_t1_dataset_validation_2026-11-14.md`](phase_6_2_t1_dataset_validation_2026-11-14.md) + `.json` | Kết quả validator |
| [`phase_6_2_t1_unresolved_annotations_2026-11-14.md`](phase_6_2_t1_unresolved_annotations_2026-11-14.md) | Danh sách cần adjudication, pool thiếu, phát hiện dữ liệu |
| `scripts/validate_retrieval_eval.py`, `tests/unit/test_retrieval_eval_validator.py` | Validator (chỉ đọc file) và 19 unit test |

Tên file theo quy ước của dự án: `eval/datasets/<tên>_v<N>.jsonl`, báo cáo có hậu tố ngày. Trước khi tạo, `eval/datasets/` chỉ có `.gitkeep`, nên không có gì bị ghi đè.

## 2. Phương pháp
- **Tập hợp lệ:** 2.338 chunk đã embed (`section_v2_1`, `cohere_embed_v4_1536_v1`), pin bằng SHA-256 của manifest. Mỗi nhãn lưu kèm `content_sha256` của chunk.
- **Nguồn dữ liệu gán nhãn:** snapshot chỉ đọc lấy từ DB (`research_chunk_embeddings ⋈ chunks`). Không gọi API, không chạy retriever.
- **Pooling:**
  - Regex nhiều nhóm khái niệm (tiếng Anh, có đồng nghĩa) cộng với **duyệt toàn bộ chunk** của các nguồn có khả năng liên quan.
  - Các lệnh tìm kiếm được ghi lại trong `search_log` của từng câu.
- **Chấm điểm:**
  - Đọc nội dung chunk (đoạn liên quan hoặc toàn văn chunk). Thang 3/2/1/0/-1 theo guidelines.
  - Ghi lý do cho mọi nhãn, kể cả nhãn 0.
  - Tiêu đề tài liệu không bao giờ được dùng để khẳng định relevance.
- **Ví dụ kiểm tra lại trước khi chốt nhãn:**
  - Nhãn -1 dự kiến cho Social Stories (q017) đã được **hủy** sau khi đọc đủ chunk: bản thân chunk đã cân bằng hai phía.
  - Nghi ngờ mâu thuẫn ASI và SenITA (q041) chỉ được giữ sau khi đọc câu kết luận của cả hai.
- **Bổ sung 4 câu** (q063–q066) để phủ các kiểu truy vấn còn thiếu: ngôn ngữ đời thường hoặc từ đồng nghĩa (echolalia), rủi ro dương tính giả (chậm nói ≠ tự kỷ), thuật ngữ ngắn (ADOS-2), bệnh đi kèm (động kinh).

## 3. Kết quả số
| Chỉ số | Giá trị |
|---|---:|
| Số câu | **66** (62 từ Phụ lục B của 6.1 + 4 bổ sung) |
| Đã gán nhãn single-pass | 65 (61 hoàn chỉnh trong pool đã chấm + 4 pool chưa đủ) |
| Pending | **0** |
| Đã được con người xác minh (gold) | **0** |
| Relevant chunk đã xác minh nội dung (grade ≥ 2) | **300 nhãn / 238 chunk duy nhất** (grade 3: 114, grade 2: 186) |
| Partial (1) / negative (0) / conflicting (-1) | 66 / 64 / 5 |
| Hard negative có chủ đích (lexical, sai tuổi, danh mục tham khảo, boilerplate) | 13 |
| Câu cần nhiều chunk | **40** |
| Câu có bằng chứng từ ≥ 2 nguồn | 54 |
| Câu unanswerable | **2** (q057 vắc-xin, q059 tế bào gốc) |
| Câu blocked / out of scope | 2 / 1 |
| Câu partially answerable | 12 |
| Câu có bằng chứng mâu thuẫn | 4 (q033, q041, q054, q060) |
| Relevant chunk mỗi câu answerable | min 1 · median 5 · max 8 |

## 4. Độ phủ
| Nhóm | Câu | Answerable / partial / khác |
|---|---:|---|
| 1 Kiến thức cơ bản | 6 | 4 / 2 |
| 2 Dấu hiệu, biểu hiện | 7 | 4 / 3 |
| 3 Giao tiếp, tương tác xã hội | 5 | 4 / 1 |
| 4 Hành vi lặp lại, sở thích hạn hẹp | 5 | 4 / 1 |
| 5 Đánh giá, chẩn đoán (gồm bệnh đi kèm) | 9 | 9 / 0 |
| 6 Can thiệp, hỗ trợ | 10 | 9 / 1 |
| 7 Sensory | 5 | 4 / 1 |
| 8 Phát triển, milestones | 6 | 5 / 1 |
| 9 AAC, hỗ trợ giao tiếp | 2 | 2 / 0 |
| 10 Nhiều khía cạnh | 4 | 3 / 1 (mọi khía cạnh của q052, q053 đều có bằng chứng ≥ 2) |
| 11 Nhiều nguồn (nhóm chính) | 1 | 0 / 1 (thêm 54 câu có cờ `multi_source`) |
| 12 Thiếu bằng chứng / ngoài phạm vi | 6 | 2 unanswerable, 2 blocked, 1 out-of-scope, 1 conflicting |

Kiểu truy vấn (`query_style`):

| Kiểu | Số câu |
|---|---:|
| colloquial | 20 |
| short | 14 |
| technical | 13 |
| long | 7 |
| age_specific | 7 |
| false_positive_risk | 7 |
| synonym | 4 |
| conflicting | 4 |

Độ phức tạp: simple 19, moderate 38, complex 9.

Nguồn có ít nhất 1 chunk relevant: **60/71**. Theo nhóm: A 60/71, B (NC) 13/13, C (cơ quan) 13/18.

**Còn thiếu:**
- AAC và multi_source (nhóm chính) ít câu.
- Synonym ít câu.
- Mốc tuổi 6, 12, 18, 30, 36 tháng chưa có câu riêng.
- 11 nguồn chưa có nhãn relevant (danh sách trong báo cáo unresolved).

## 5. Phát hiện quan trọng cho T2
1. **47 chunk danh mục tài liệu tham khảo** (ASD-CSV-017, ASD-CSV-018) nằm trong index và gây dương tính giả cho truy vấn từ khóa. Cần quyết định D-1 (authorization mới loại chúng) trước T5.
2. **Chính tả Anh/Mỹ** ("behaviour"/"behavior") tạo hai lexeme khác nhau trong FTS `english`. Glossary C4 bắt buộc phải có cả hai.
3. Thuật ngữ trong prompt khởi đầu có tần suất thấp trong corpus: "restricted interests" 7 chunk, "sensory sensitivity" 14. Corpus dùng "restricted, repetitive" và "sensory processing / over-responsivity". Bảng đầy đủ ở T0, C4.
4. Bằng chứng của một số câu nằm ở chunk bị loại (session 7 WHO-CST, thân bài ASD-OA-PMC12593641). Đây là giới hạn của độ phủ, không phải lỗi của retriever.
5. **Dương tính giả lexical** có thật trong corpus ("MMRM" so với "MMR", bảng liều melatonin). Đây là test case tốt cho FTS và cho evidence gate.

## 6. Regression (đã chạy thực tế)
| Kiểm tra | Kết quả |
|---|---|
| Dataset validator | PASS, 0 lỗi, 0 cảnh báo |
| Unit test | **101 pass** (82 cũ + 19 mới) |
| Integration test (DB, chỉ đọc) | **11 pass** |
| `db_check` | ok, **34/34** probe phân quyền. Các probe chạy trong transaction luôn bị rollback |
| ruff | sạch |
| Code | So sánh hash 67 file: **chỉ có 2 file mới** (`scripts/validate_retrieval_eval.py`, `tests/unit/test_retrieval_eval_validator.py`), không file cũ nào đổi |
| Số lượng | research vectors 2.338 → 2.338; production vectors 0 → 0; chunks 5.470 → 5.470; ingestion_runs 17 → 17; authorizations 1 → 1; retrieval_logs 0 → 0; migrations 6 → 6 |
| Hash dữ liệu embedding | md5(chunk_id ‖ input_hash ‖ norm ‖ vector) của 2.338 vector **không đổi** (`3332a8be…`) |
| Nội dung chunk | md5(chunk_id ‖ content_sha256 ‖ eligibility ‖ status) **không đổi** (`e40dc061…`) |
| Schema / view | fingerprint cột và view **không đổi** |
| Quyền | fingerprint ACL bảng và ACL cột **không đổi**; role không đổi (app, ingest, owner) |
| API call | Không có. `ingestion_runs` không tăng; không chạy module nào gọi Cohere (validator chỉ đọc file; snapshot lấy bằng SELECT) |
| Raw | 199/199 file khớp baseline |

## 7. Vấn đề chưa giải quyết
Chi tiết trong [phase_6_2_t1_unresolved_annotations_2026-11-14.md](phase_6_2_t1_unresolved_annotations_2026-11-14.md):
- 6 câu cần adjudication;
- 4 câu pool chưa đủ;
- 3 câu có bằng chứng nằm ở chunk bị loại;
- 0 nhãn được con người xác minh;
- thiên lệch pooling lexical.

## 8. Khuyến nghị cho T2 và kết luận
**READY WITH CONDITIONS.** Dataset đủ để **chạy baseline thăm dò**: 61 câu có pool hoàn chỉnh, 300 nhãn relevant, có negative, conflicting, unanswerable và blocked. Dataset **chưa đủ** để đưa ra kết luận cuối cùng về cấu hình.

Điều kiện:
1. **DB-ACCESS (C1 + C5):** migration 007, gồm role chỉ đọc và view có filter, phải xong và qua probe **trước khi** retriever chạy. Không dùng role `ingest`.
2. **Mở rộng pool ở T5:** sau lần chạy A, A-EN, B, C đầu tiên, chấm bổ sung các chunk trong top-20 chưa được chấm (đưa vào `candidate_chunk_ids` trước). Chưa xong bước này thì chỉ báo metric kèm cảnh báo về thiên lệch lexical.
3. **Human verification** cho 12 câu ưu tiên `high` và một mẫu ngẫu nhiên khoảng 10 câu `low` trước khi gọi kết quả là gold. Nếu có người đánh giá thứ hai: tính weighted κ theo guidelines.
4. **Quyết định D-1** (47 chunk danh mục tham khảo) trước khi chốt metric. Nếu giữ nguyên, phải báo cáo riêng tỉ lệ các chunk này xuất hiện trong top-K.
5. **Báo cáo metric** loại các câu `partial`, `not_applicable` khỏi recall; tính riêng nhóm unanswerable và blocked (hành vi abstain). Chưa chọn K hay fusion trước khi chạy trên tách dev/test (§6 của audit 6.1).

Đề xuất thứ tự T2: (a) migration 007 + probe → (b) dense retriever A / A-EN với provenance đầy đủ, cache query embedding (66 câu × 2 ngôn ngữ ≈ 2 lời gọi API, chỉ gửi câu hỏi) → (c) chấm bổ sung pool → (d) T3 glossary + FTS.
