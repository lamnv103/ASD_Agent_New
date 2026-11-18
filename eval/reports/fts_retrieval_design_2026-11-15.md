# T2.4 — FTS Retrieval Design — 2026-11-15

## 1. Thành phần
| File | Vai trò |
|---|---|
| `app/retrieval/fts.py` (mới) | Glossary + mở rộng truy vấn, ghép tsquery, `FtsReader` (SQL cố định), `FtsRetriever` (kiểm tra đầu vào, provenance, log) |
| `config/fts_profiles.json` (mới) | 3 profile: `fts_a_baseline_v1`, `fts_b_glossary_and_v1`, `fts_c_glossary_or_v1` |
| `config/query_glossary_vi_en_v1.json` (mới) | Glossary VI→EN v1 (theo quyết định T0 C4): 94 mục, quy tắc tuổi, danh sách từ chung không mở rộng. SHA `aad39e34…` |
| `scripts/fts_eval_t2_4.py` (mới) | Chạy thử nghiệm, tạo pool công bằng, tính overlap, metric exploratory, kiểm chứng độc lập; có chế độ `--check` |
| `tests/unit/test_fts.py`, `tests/integration/test_fts_retrieval_db.py` (mới) | 48 test unit + 8 test integration |

Retriever dense (`dense.py`, `research_reader.py`, `retrieval_profiles.json`) **không bị sửa**. SHA trước và sau đều là `46561e4b…`, `3bf30477…`, `17595edc…`.

## 2. An toàn và provenance
- **Kết nối:**
  - Chỉ dùng role `research_reader`. Profile nào khai báo role khác bị từ chối khi nạp.
  - `current_user` phải bằng `asd_rag_v2_research_reader`, nếu không thì lỗi `wrong_role`.
  - Session `read_only`, chịu `statement_timeout` 60 s của role.
- **SQL cố định**, chỉ đọc view `asd_rag.v_research_retrieval_chunks` (đã áp authorization và C5), lọc `profile_code`, `LIMIT k` (k ∈ [1, 50]). Không đọc cột vector.
- **Chống injection:**
  - Text người dùng chỉ đi qua `plainto_tsquery` / `phraseto_tsquery`, dưới dạng tham số. Hai hàm này bỏ qua toán tử.
  - tsquery cuối cùng được ghép từ chuỗi tsquery do chính PostgreSQL trả về (lexeme đã được PG trích dẫn). Python chỉ thêm `( ) & |`.
  - Không có `to_tsquery` nào nhận text thô.
- **Fail-closed** khi gặp một trong các lỗi:
  - thiếu trường provenance; thiếu cả trang lẫn khoảng ký tự;
  - hash nội dung sai;
  - `profile_code` sai;
  - điểm không hợp lệ;
  - chunk trùng;
  - sai thứ tự `(score desc, chunk_id asc)`;
  - trả nhiều hơn k hàng;
  - hơn một authorization.
- **Mỗi lần truy xuất ghi lại:**
  - hash câu gốc; câu đã chuẩn hoá;
  - khái niệm, trigger và thuật ngữ EN;
  - từ không ánh xạ được;
  - phiên bản và SHA của glossary;
  - config `english`; tsquery; ranker; điểm; provenance của chunk và nguồn; authorization.

  Log JSONL chỉ chứa hash câu gốc, giống dense. Câu gốc của bộ eval nằm trong `fts_run_record_2026-11-15.json`.
- **Ý nghĩa điểm:** `ts_rank_cd` chỉ dùng để xếp thứ tự. **Không phải BM25**, không phải xác suất đúng, không phải bằng chứng y khoa.

## 3. Glossary v1 (quy tắc)
- Một mục chỉ kích hoạt khi trigger tiếng Việt có trong câu: khớp theo ranh giới từ, trigger dài nhất trước, phần đã khớp bị tiêu thụ.
- Thuật ngữ EN chỉ là bản dịch hoặc biến thể chính tả/viết tắt của trigger. Không thêm triệu chứng, chẩn đoán hay ý định.
- **Dấu:**
  - Câu có dấu thì khớp nguyên dạng (NFC, chữ thường).
  - Câu **không có dấu nào** mới khớp với trigger đã bỏ dấu, để tránh nhầm như "đồng kính" thành "động kinh".
- **Tuổi:** "N tháng" thành `N months` / `N-month-old`; "N tuổi" thành `N years` / `N-year-old`.
- **Từ viết tắt viết hoa** (ADHD, AAC, DSM-5, ADOS-2, M-CHAT-R/F…) được giữ làm thuật ngữ EN; nếu có mục glossary thì lấy kèm biến thể.
- **Kiểm tra corpus** (tiêu chí T0 C4: mỗi thuật ngữ EN xuất hiện ít nhất 1 lần):
  - 263 thuật ngữ được kiểm (mọi thuật ngữ EN của 94 mục, cộng thuật ngữ tuổi sinh ra cho 66 câu); **9 thuật ngữ có 0 chunk**: `WHO` (từ dừng), `auditory sensitivity`, `curable`, `delayed development`, `delayed speech`, `loss of skills`, `sensitivity to noise`, `stem cell`, `stem cells`.
  - Các thuật ngữ này không ảnh hưởng xếp hạng (không khớp gì). Nhưng **tiêu chí T0 chưa đạt**, phải xử lý ở v2:
    - bỏ các thuật ngữ đó;
    - riêng `stem cell` giữ làm dấu hiệu "không có trong corpus" cho q059;
    - thay `WHO` bằng "World Health Organization".
- **Giới hạn quan trọng:** glossary được viết từ vốn từ của chính 66 câu eval (dev = test), nên kết quả B và C trên bộ này **lạc quan**. Cần bộ câu hold-out trước khi nói đến khả năng khái quát.

## 4. Ba cấu hình
| | **FTS-A** `fts_a_baseline_v1` | **FTS-B** `fts_b_glossary_and_v1` | **FTS-C** `fts_c_glossary_or_v1` |
|---|---|---|---|
| Phiên bản | 1 | 1 (glossary v1) | 1 (glossary v1) |
| Xử lý truy vấn | NFC + gộp khoảng trắng; câu Việt nguyên văn | Như A, cộng mở rộng glossary | Như B |
| tsquery | `plainto_tsquery('english', câu)`: AND mọi từ | `(câu VI)` OR (**AND** giữa các khái niệm; trong mỗi khái niệm OR các biến thể) | `(câu VI)` OR (**OR** giữa các khái niệm) |
| Config / ranker | `english` / `ts_rank_cd` (normalization 0), hoà điểm thì xếp theo chunk_id | Như A | Như A |
| Ưu điểm | Cấu hình có sẵn, không giả định gì | Chính xác khi câu có 2–3 khái niệm đặc hiệu (q066: tự kỷ ∧ động kinh) | Không mất kết quả khi một khái niệm hiếm hoặc vắng |
| Nhược điểm | Câu Việt cho 0 kết quả (audit §2) | Mất kết quả khi có khái niệm hiếm hoặc vắng (`cure` 3 chunk, `stem cell` 0) hoặc câu nhiều khái niệm (q052: 6 khái niệm AND) | Khái niệm chung ("autism" 719 chunk) lấn át; `ts_rank_cd` thưởng mật độ từ chung |
| Dự kiến cải thiện | Không có | Câu có thuật ngữ đặc hiệu mà dense bỏ sót: q066, q063, q033 | Câu mà B trả 0 |
| Dự kiến false positive | — | Cụm bị stem/từ dừng: `lining up` thành `line`; `point`; trích đoạn phỏng vấn chứa đủ "parent/home/school/intervention" | Chunk chỉ chứa khái niệm chung |
| Giả thuyết kiểm định | Xác nhận audit (câu Việt thô vô dụng) | Glossary + AND bù được lệch ngôn ngữ cho câu đặc hiệu | AND làm mất kết quả; OR thì ra sao |

Không có LLM, không gọi API dịch, không có reranker, hybrid hay evidence gate.

## 5. Pool ứng viên công bằng (R4)
1. Dense top-20 chạy lại đúng cấu hình T2.3.1 (cache, không API): **66/66 danh sách giống hệt T2.3.3**.
2. FTS-A/B/C top-20 cho 66 câu.
3. Hợp theo từng câu, khử trùng theo `chunk_id`.
4. **File mù** `fts_candidate_pool_2026-11-15.jsonl`:
   - mỗi dòng gồm `item_id`, câu hỏi, phạm vi trả lời, `chunk_id`/nguồn/tài liệu/tiêu đề/mục/trang/khoảng ký tự, nội dung + SHA, và các ô `grade`/`rationale_vi`/`annotator_id`/`annotated_at` để trống;
   - **không** có hệ thống, rank, điểm hay nhãn cũ;
   - thứ tự hiển thị theo `item_id` = sha256(salt | câu | chunk), độc lập với rank và hệ thống.
5. **File khoá niêm phong** `fts_candidate_pool_key_2026-11-15.jsonl`: nguồn gốc (`in_dense`/`in_fts_a`/`in_fts_b`/`in_fts_c`), rank, điểm, nhãn gốc/merge, trạng thái T2.3.2. **Không giao cho người chấm.**
6. Thang chấm như T2.3.2 (3/2/1/0/−1). Chunk chưa chấm không bao giờ tính là 0. Nếu có hai người chấm: lưu riêng và tính weighted kappa.
