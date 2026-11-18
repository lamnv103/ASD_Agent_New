# Phase 6.2 – T2.4: Sparse / FTS Retrieval Baseline — 2026-11-15

**Kết luận: READY WITH CONDITIONS.** Không tự chuyển sang T2.5.

FTS baseline đã chạy ổn định:
- 3 cấu hình; xếp hạng khớp truy vấn SQL độc lập ở 198/198 lượt (66 câu × 3 cấu hình);
- 0 vi phạm authorization; tái lập được (`--check`);
- 0 lệnh gọi API; DB không thay đổi.

Pool ứng viên chung (Dense ∪ FTS) đã tạo ở dạng mù, nhưng **PENDING ANNOTATION**: chưa có người chấm mù. Vì vậy mọi metric so sánh chỉ là **exploratory**.

## 1. Phạm vi và đầu vào
- **Mục tiêu:**
  - FTS (PostgreSQL full-text search) độc lập với dense;
  - kiểm định FTS-A/B/C;
  - tạo pool công bằng Dense ∪ FTS;
  - chạy các ca kiểm thử bắt buộc;
  - đánh giá exploratory trên cohort cố định của T2.3.1.
- **Không làm:** hybrid/RRF, reranker, evidence gate; sửa dense; gọi embedding hay API; ghi DB; đổi schema/quyền/authorization; sửa dataset.

| Đầu vào | SHA-256 |
|---|---|
| `retrieval_eval_v1.jsonl` / `…_merged_2026-11-14.jsonl` | `7704bb51…` / `6bd3ad78…` (không đổi) |
| Manifest cohort `dense_eval_frozen_cohort_manifest_2026-11-15.csv` | `0d88846e…` |
| `config/query_glossary_vi_en_v1.json` | `aad39e34…` |
| `config/fts_profiles.json` | `8ace29e3…` |
| `app/retrieval/fts.py` / `scripts/fts_eval_t2_4.py` | `d2100ebf…` / `f033ccb6…` |
| `dense.py` / `research_reader.py` / `retrieval_profiles.json` (không sửa) | `46561e4b…` / `3bf30477…` / `17595edc…` |
| Allowlist authorization 2 / danh sách loại D-1 | `59c3d6cf…` / `d3bb36fc…` |

Báo cáo đi kèm:
- `fts_architecture_audit_2026-11-15.md`
- `fts_retrieval_design_2026-11-15.md`
- `fts_query_glossary_2026-11-15.json` (glossary, kết quả kiểm tra corpus, bản mở rộng của 66 câu)
- `fts_candidate_pool_2026-11-15.jsonl` (file **mù**)
- `fts_candidate_pool_key_2026-11-15.jsonl` (khoá **niêm phong**)
- `fts_candidate_pool_manifest_2026-11-15.csv`
- `fts_candidate_overlap_2026-11-15.csv`
- `fts_retrieval_metrics_2026-11-15.json` (exploratory)
- `fts_error_analysis_2026-11-15.md`
- `fts_run_record_2026-11-15.json` (tsquery, bản mở rộng, danh sách xếp hạng, fingerprint)

## 2. Audit FTS (tóm tắt)
- Cấu hình hiện có:
  - `content_tsv` dùng config `english` (heading B, nội dung A), có GIN index;
  - view `security_barrier` khiến index không được dùng (khoảng 0,1 s/truy vấn, chấp nhận được);
  - không có `unaccent` hay `pg_trgm` (có sẵn nhưng chưa cài; cài phải qua migration).
- **Tiếng Việt:** config `english` để nguyên âm tiết có dấu. `plainto_tsquery` AND mọi âm tiết, nên **cả 6 câu Việt thử nghiệm đều ra 0 kết quả**. Âm tiết Việt gần như không có trong corpus (ví dụ `trẻ` 0, `tự` 2).
- **Biến thể chính tả:**
  - `behaviour` (196) và `behavior` (680) là hai lexeme khác nhau; tương tự `paediatric/pediatric`.
  - `ADOS` thành `ado`; `DSM-5` thành `dsm` & `-5`.
  - **`WHO` là từ dừng**, nên tsquery rỗng.
- **AND làm mất kết quả:**
  - "restricted interests" (cụm) chỉ có 7 chunk, so với 26 của "restricted, repetitive".
  - Câu tiếng Anh dài theo AND có thể ra 0 kết quả.
- **Hàm xếp hạng là `ts_rank_cd`, không phải BM25.**

## 3. Cấu hình đã triển khai
| Mã | Truy vấn | Giả thuyết | Kết quả thực tế (66 câu, top-20) |
|---|---|---|---|
| **FTS-A** `fts_a_baseline_v1` | `plainto_tsquery('english', câu VI)` | Câu Việt thô vô dụng với corpus tiếng Anh | **0 kết quả ở 66/66 câu.** Xác nhận audit |
| **FTS-B** `fts_b_glossary_and_v1` | VI ∨ (∧ khái niệm, ∨ biến thể), glossary v1 | Glossary + AND bù lệch ngôn ngữ cho câu đặc hiệu | Có kết quả ở 55 câu; **0 kết quả ở 11 câu**; dưới 20 kết quả ở 38 câu |
| **FTS-C** `fts_c_glossary_or_v1` | VI ∨ (∨ khái niệm) | OR tránh mất kết quả của AND | Có kết quả ở 65 câu (q062 ra 0); bị khái niệm chung lấn át |

Chi tiết thiết kế, ưu/nhược và rủi ro false positive: `fts_retrieval_design_2026-11-15.md`.

## 4. Pool ứng viên công bằng
- **Dense:** chạy lại đúng cấu hình T2.3.1 (cache, 0 API), **66/66 danh sách giống hệt T2.3.3**.
- **FTS:** top-20 của A, B, C.
- **Thống kê:**

| | Cặp (câu, chunk) | Chunk duy nhất |
|---|---|---|
| **Pool Dense ∪ FTS** | **2.791** (trung bình 42,3/câu, tối đa 58) | **1.218** |
| Chỉ dense | 997 | 424 |
| Chỉ FTS (B và/hoặc C; A không đóng góp) | 1.471 | 409 |
| Cả hai | 323 | 385 |
| Theo nguồn gốc | dense 997 · fts_c 961 · fts_b 350 · fts_b+fts_c 160 · dense+fts_b 159 · dense+fts_b+fts_c 89 · dense+fts_c 75 | |

- **Đã có nhãn trong pool:** 270 cặp (nhãn gốc) / 573 cặp (nhãn merge). **Chưa có nhãn ở cả hai bộ: 2.218 cặp (79%).**
- **Overlap top-20 dense–FTS-B:** Jaccard trung bình 0,131; trung bình 3,8 chunk chung; **20/66 câu không có chunk chung**. Dense–FTS-C: Jaccard 0,073. Xem `fts_candidate_overlap_2026-11-15.csv`.
- **Tính mù:**
  - file chấm không có hệ thống, rank, điểm hay nhãn cũ;
  - thứ tự theo `item_id` băm;
  - khoá nguồn gốc tách riêng.
  - Có test tự động: `test_blind_export_hides_system_rank_score_and_prior_labels`, `test_pool_is_the_deduplicated_union_of_every_system_top20`.
- **Trạng thái: PENDING ANNOTATION.**
  - Chưa có người chấm. **Không dùng nhãn AI** để thay thế chấm mù.
  - Khi có người chấm: chấm toàn bộ 2.791 cặp theo thang 3/2/1/0/−1, kể cả cặp đã có nhãn silver, để mọi hệ thống được chấm cùng điều kiện.
  - Nếu có 2 người: lưu riêng và tính weighted kappa. Nếu chỉ 1 người: ghi rõ là single-annotator.

## 5. Kết quả EXPLORATORY (không phải so sánh công bằng)
- **Phạm vi:** 55 câu nhóm `answerable` cố định theo T2.3.1. Nhãn gốc và nhãn merge báo cáo **riêng**.
- **Định nghĩa metric giống T2.3.3:**
  - R = chunk đã chấm grade ≥ 2 và truy xuất được;
  - chunk unjudged không bao giờ tính là 0;
  - nDCG gain 3→7, 2→3, 1→1, 0→0, −1 không có gain;
  - source recall đếm mỗi nguồn một lần;
  - trung bình macro theo câu.

| Metric | Dense (gốc) | FTS-B (gốc) | FTS-C (gốc) | Dense (merge) | FTS-B (merge) | FTS-C (merge) |
|---|---|---|---|---|---|---|
| Recall@10 | 0,491 | 0,220 | 0,155 | 0,607 | 0,246 | 0,159 |
| Recall@20 | 0,646 | 0,303 | 0,175 | 0,716 | 0,328 | 0,196 |
| Hit@10 | 0,909 | 0,509 | 0,364 | 0,964 | 0,655 | 0,455 |
| MRR (cận dưới) | 0,585 | 0,288 | 0,195 | 0,782 | 0,388 | 0,241 |
| MRR cận trên | 0,952 | 0,882 | 0,991 | 0,801 | 0,873 | 0,982 |
| nDCG@10 | 0,440 | 0,205 | 0,135 | 0,608 | 0,240 | 0,145 |
| Judged-only precision@10 | 0,846 | 0,818 | 0,765 | 0,598 | 0,767 | 0,742 |
| Source recall@10 | 0,737 | 0,510 | 0,406 | 0,761 | 0,519 | 0,429 |
| **Judged coverage@5 / @10 / @20 (micro)** | 0,36 / 0,27 / 0,19 | 0,24 / 0,18 / 0,14 | 0,12 / 0,10 / 0,06 | 0,99 / 0,64 / 0,37 | 0,34 / 0,27 / 0,21 | 0,16 / 0,14 / 0,09 |
| Số chunk truy xuất @20 (55 câu) | 1.100 | 687 | 1.085 | 1.100 | 687 | 1.085 |

FTS-A: 0 kết quả nên mọi metric bằng 0 hoặc không xác định.

**Vì sao chưa được kết luận hệ thống nào tốt hơn:**
1. **Nhãn thiên lệch.**
   - Nhãn gốc đến từ quá trình tìm kiếm của T1.
   - Nhãn merge thêm 95 nhãn relevant chỉ từ top-20 dense.
   - Coverage của FTS chỉ 6–34%, so với 19–99% của dense.
   - Recall/hit/MRR (cận dưới) của FTS bị **đánh giá thấp có hệ thống**. MRR cận trên của FTS-C (0,98–0,99) cho thấy khoảng bất định rất lớn.
2. **FTS-B trả ít kết quả hơn K** ở 38/66 câu (tổng 687/1.100 lượt @20 trên 55 câu). Nhờ vậy precision không bị phạt, nhưng recall ở các câu đó thấp.
3. **Glossary viết từ chính bộ câu eval** (dev = test), nên kết quả B/C lạc quan về khả năng khái quát.

**Metric đủ điều kiện báo cáo ngay:**
- thống kê truy xuất và pool;
- overlap;
- judged coverage;
- tính đúng của retriever (khớp SQL độc lập);
- an toàn và authorization.

**Metric chỉ exploratory:** recall, precision, MRR, nDCG, hit, source recall khi so FTS với dense.

## 6. Ca kiểm thử bắt buộc
Chi tiết: `fts_error_analysis_2026-11-15.md`.

| Câu | Dense | FTS-B | Cải thiện? |
|---|---|---|---|
| q066 động kinh | 0 relevant trong top-20 | Relevant ở **rank 1, 2, 3** và 10; recall@10 = 1,0 | **Có** (trên nhãn hiện có); phụ thuộc glossary "động kinh" → epilepsy |
| q033 can thiệp do cha mẹ thực hiện | ADHD ở rank 1; relevant (merge) ở rank 10 | Không có ADHD; relevant đã chấm ở rank 5; rank 1–2 là tổng quan can thiệp do cha mẹ thực hiện (CSV-089), **chưa chấm** | **Có dấu hiệu**, cần chấm mù |
| q063 nhại lời | Reprints ở rank 1 và 3; relevant ở rank 5 | 6/6 chunk "echolalia", relevant ở **rank 1** (5 relevant + 1 grade 1), không boilerplate | **Có**; phụ thuộc glossary |
| q054 tại nhà vs tại trường | Quiz WHO-CST; relevant ở rank 17 | Trích đoạn phỏng vấn SENITA; không có relevant đã chấm | **Không** (corpus không có so sánh trực tiếp) |

Ngược lại, FTS **kém hơn** dense ở q011, q050, q051, q056 (0–1 kết quả, hoặc không có relevant đã chấm). Vẫn không coi các câu này là lỗ hổng truy xuất của dense, theo đính chính ở T2.3.3. q057 và q016 tiếp tục chờ phân xử, không sửa nhãn.

## 7. Bảo mật và bất biến (đã chạy)
| Kiểm tra | Kết quả |
|---|---|
| Role | Chỉ `asd_rag_v2_research_reader`, `read_only`. Profile khác role reader bị từ chối (unit test). Kết nối sai role thì lỗi `wrong_role` |
| Authorization | 0 chunk ngoài allowlist authorization 2; 0 chunk D-1; `authorization_version` = 2 cho mọi kết quả (198 lượt + integration test) |
| SQL injection | Text độc hại chỉ đi qua tham số `plainto/phraseto`. SQL cố định. Integration test với `x'); DROP TABLE …; -- & !a ∣ b:*` chạy bình thường và view vẫn nguyên |
| Đúng thứ tự | Xếp hạng của retriever = truy vấn SQL độc lập (không dùng ORDER BY/LIMIT trong SQL, sắp xếp bằng Python) ở 198/198 lượt |
| Tái lập | `fts_eval_t2_4.py --check`: mọi file giống hệt (trừ timestamp/latency) |
| API | 0 lệnh gọi (dense dùng cache 66/66; FTS chỉ dùng PostgreSQL) |
| DB fingerprint (reader): nội dung + vector của view, ma trận quyền 4 role × 22 relation, thuộc tính role, bộ đếm ghi | **Trước = sau** |
| Query cache / dataset gốc / dataset merge | Không đổi |
| Test | `ruff` đạt; `pytest` unit **222 passed** (48 test mới); integration FTS **8 passed** (`-m integration tests/integration/test_fts_retrieval_db.py`) |
| File ghi ra | Chỉ file: code/config/test mới, báo cáo `eval/reports/fts_*_2026-11-15.*`, log `logs/retrieval/t2_4_*.jsonl`. Không có migration hay thay đổi schema |

## 8. Điều kiện trước T2.5
| # | Điều kiện |
|---|---|
| C1 | **Chấm mù toàn bộ pool** (2.791 cặp; tối thiểu là 2.218 cặp chưa có nhãn) bằng người chấm. Lý tưởng là 2 người để tính weighted kappa. Trước khi xong, không so sánh dense với FTS và không tối ưu fusion |
| C2 | Phân xử q057 (nhãn câu) và q016 (2 chunk), kế thừa từ T2.3.3 |
| C3 | Glossary v2: bỏ hoặc sửa 9 thuật ngữ có 0 chunk (`WHO` thành "World Health Organization"; giữ `stem cell` làm dấu hiệu vắng) để đạt tiêu chí T0 C4. Đánh giá trên **bộ câu hold-out** không dùng để viết glossary |
| C4 | Ghi nhận giới hạn của FTS-B: AND mất kết quả ở 11 câu. FTS-C bị khái niệm chung lấn át. Mọi biến thể mới (ví dụ AND có ngưỡng tối thiểu, trọng số theo IDF khái niệm) phải là thí nghiệm riêng, có giả thuyết, **sau** khi có nhãn mù |
| C5 (đề xuất, không tự làm) | Nếu cần `unaccent`, đổi trọng số heading, hoặc index dùng được qua view: lập đề xuất migration riêng, kèm lý do, ảnh hưởng, backup và rollback |

## 9. Trả lời các câu hỏi bắt buộc
1. **Cấu hình đã triển khai:** FTS-A (`fts_a_baseline_v1`), FTS-B (`fts_b_glossary_and_v1`), FTS-C (`fts_c_glossary_or_v1`). Cả ba dùng config `english`, ranker `ts_rank_cd` (không phải BM25), role reader và view nghiên cứu.
2. **Vấn đề của config hiện tại với tiếng Việt:**
   - không có config tiếng Việt;
   - âm tiết có dấu được giữ nguyên và AND với nhau, nên câu Việt cho **0 kết quả**;
   - không có `unaccent`;
   - corpus tiếng Anh gần như không chứa âm tiết Việt.
   Ngoài ra, ở phía tiếng Anh: Anh/Mỹ khác lexeme, `WHO` là từ dừng, `ADOS` thành `ado`.
3. **Glossary giúp truy vấn nào:**
   - rõ nhất ở q066 (động kinh → epilepsy, rank 1) và q063 (nhại lời → echolalia, rank 1);
   - q016 (joint attention, rank 2);
   - q033 (can thiệp do cha mẹ thực hiện: ADHD biến mất, tổng quan liên quan lên top, nhưng chưa chấm).
   Glossary **không** giúp: q054, các câu có cụm tuổi (q050, q051), và câu nhiều khái niệm (q052).
4. **Chunk duy nhất trong pool Dense ∪ FTS:** **1.218** (2.791 cặp câu–chunk).
5. **Chỉ dense tìm được:** **424 chunk duy nhất** (997 cặp).
6. **Chỉ FTS tìm được:** **409 chunk duy nhất** (1.471 cặp).
7. **q066, q033, q063, q054:**
   - q066 và q063: **có cải thiện** trên nhãn hiện có;
   - q033: có dấu hiệu, chờ chấm;
   - q054: **không cải thiện**.
8. **Chấm mù pool:** **chưa**. Trạng thái PENDING ANNOTATION; không dùng AI để thay thế.
9. **Metric đủ điều kiện báo cáo:** thống kê pool và overlap, judged coverage, tính đúng của retriever, an toàn. **Chỉ exploratory:** recall/precision/MRR/nDCG/hit/source recall khi so sánh hệ thống.
10. **API call / thay đổi DB:** **không**. 0 API; fingerprint DB trước = sau; chỉ đọc bằng role reader.
11. **Đủ điều kiện sang T2.5:** **READY WITH CONDITIONS**. Điều kiện chính là C1 (chấm mù pool) và C2 (phân xử). Không tự chuyển sang T2.5.
