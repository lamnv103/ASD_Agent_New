# Phase 6.2 – T0: Technical Decisions (C1–C5) — 2026-11-14

**Trạng thái T0: COMPLETED.** C1–C5 được ghi thành quyết định chính thức, kèm lý do, phạm vi, non-goals, acceptance criteria và dependency map.

Không có thay đổi code runtime, DB, vector hay quyền. Phần **triển khai** C1 (migration 007) và C5 (filter trong retriever) thuộc các task sau.

Căn cứ:
- [retrieval_architecture_audit_2026-11-14.md](retrieval_architecture_audit_2026-11-14.md)
- Prompt Phase 6.2
- Các phép đo chỉ đọc trong phiên này (mục 6)

---

## C1 — Research retrieval access: Phương án A (migration 007, role chỉ đọc + view)

**Quyết định:** Retrieval và evaluation nghiên cứu **không** dùng role `ingest`. Tạo role chuyên biệt (tên đề xuất `asd_rag_v2_research_reader`). Role này chỉ có `SELECT` trên một view truy xuất nghiên cứu.

**Lý do (VERIFIED trong audit 6.1, §4):**
- Ngoài owner, chỉ `ingest` đọc được vector nghiên cứu.
- `ingest` có quyền `DELETE` trên `chunks` và `chunk_embeddings`, nên dùng nó cho retrieval là thừa quyền.
- Role `app` đúng là không đọc được dữ liệu nghiên cứu, và phải giữ nguyên như vậy.

**Phạm vi (task database/access riêng, trước T2):**
1. Một view (đề xuất `v_research_retrieval_chunks`) gồm: vector + nội dung chunk + provenance (`source_id`, `document_id`, `chunk_id`, title, URL, section, page / char range, `content_sha256`, `chunking_profile`, `model_id`, `vector_dimension`, `authorization_id`). View đã áp toàn bộ filter của C5.
2. Role `NOLOGIN` hoặc `LOGIN` (tuỳ cách chạy), `NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS`, chỉ có `USAGE` trên schema và `SELECT` trên view đó.
   - Không cấp trên bảng gốc nếu view chạy bằng quyền owner (mặc định của PostgreSQL).
   - Nếu dùng `security_invoker`, phải trình bày lại phạm vi grant.
3. Rollback script, backup trước khi áp dụng, thử trên container cô lập (apply → probe → rollback → re-apply), bổ sung probe vào `db_check.py`.

**Non-goals:**
- Không đổi quyền của `app`, `ingest` hay `owner`.
- Không mở production retrieval.
- Không dùng `SECURITY DEFINER`.
- Không cấp quyền trên toàn schema.

**Acceptance criteria:**
| # | Tiêu chí | Cách kiểm |
|---|---|---|
| C1-1 | Role mới đọc được view nghiên cứu | probe `SELECT … LIMIT 1` bằng chính role mới |
| C1-2 | Role mới **không** đọc được: `chunks`, `chunk_embeddings`, `research_chunk_embeddings`, `source_rights`, `rights_assessments`, các bảng authorization, `retrieval_logs`, `v_retrieval_ready_chunks` | probe phải bị từ chối (InsufficientPrivilege) |
| C1-3 | Role mới không INSERT/UPDATE/DELETE/TRUNCATE/DDL được ở bất kỳ đâu | probe `… WHERE false` hoặc `CREATE TABLE` phải bị từ chối |
| C1-4 | Quyền của `app`/`ingest`/`owner` không đổi | so sánh fingerprint ACL (bảng + cột) trước/sau = chỉ khác ở đối tượng mới |
| C1-5 | View không trả chunk ngoài C5 | integration test âm tính (mục C5) |
| C1-6 | Có backup, rollback, thử trên container cô lập, `db_check` pass | báo cáo migration |

**Dừng migration nếu:** role mới truy cập được bất kỳ đối tượng nào ngoài view; view lộ chunk ngoài allowlist; có function `SECURITY DEFINER` lọt vào đường truy cập.

---

## C2 — Retrieval Evaluation Dataset v1 (ưu tiên cao nhất)

**Quyết định:** Mọi so sánh retriever, Top-K, fusion hay reranker chỉ được thực hiện trên dataset có nhãn đã đọc nội dung. Nhãn có tiêu chuẩn tin cậy rõ ràng (silver / gold).

**Lý do:** audit 6.1 (R2) cho thấy chưa có nhãn, nên mọi lựa chọn K hay fusion hiện tại là tuỳ ý.

**Phạm vi (T1, hoàn thành trong phiên này):** dataset, schema, guidelines, status, validator, báo cáo. Xem [phase_6_2_t1_evaluation_dataset_report_2026-11-14.md](phase_6_2_t1_evaluation_dataset_report_2026-11-14.md).

**Non-goals:**
- Không chạy retriever.
- Không tính metric.
- Không gọi API.
- Không tuyên bố inter-annotator agreement khi chỉ có một người gán.

**Acceptance criteria:** validator pass; không có chunk ID bịa; trạng thái pending/partial được thống kê; nhãn silver được phân biệt rõ với gold. Kết quả: **đạt** (xem T1). Điều kiện còn lại là **human verification** trước khi gọi là gold (mục 5).

---

## C3 — Reranker: tạm bỏ trong baseline

**Quyết định:**
- Baseline gồm A (dense), A′ (dense trên câu tham chiếu tiếng Anh, chỉ để đo khoảng cách ngôn ngữ), B (FTS), C (hybrid).
- **Không** có D (rerank).
- Không gọi Cohere Rerank, không gửi chunk ra ngoài, không cài hay tải model rerank.

**Lý do:**
- Chưa có nhãn.
- Chưa chứng minh được lợi ích.
- Rerank qua API gửi lại nội dung chunk, vượt phạm vi ủy quyền nghiên cứu hiện tại (chỉ embedding).

**Điều kiện để mở lại:** baseline A/B/C đã có kết quả với khoảng tin cậy, và có phân tích lỗi cho thấy thứ hạng (không phải độ phủ) là điểm nghẽn. Khi đó đề xuất một thí nghiệm riêng, ghi rõ chi phí, dữ liệu đi ra ngoài và ủy quyền.

**Acceptance criteria:**
- Không có code hay dependency rerank trong T2–T5.
- `retrieval_results.rerank_score` để NULL.

---

## C4 — Bilingual query: glossary + English expansion có kiểm soát, không LLM

**Quyết định:**
- Giữ nguyên câu hỏi tiếng Việt cho nhánh dense.
- Sinh thêm **một** truy vấn tiếng Anh từ glossary có phiên bản. Không dịch từng từ, không thêm triệu chứng hay chẩn đoán mà người dùng không nói.
- Ghi lại cả câu gốc (dưới dạng hash theo chính sách log) lẫn bản mở rộng.
- Đánh giá từng nhánh riêng: A (VI dense), A-EN (dense trên bản mở rộng), B (FTS trên bản mở rộng).

**Bằng chứng mới từ corpus** (đếm trên 2.338 chunk đã embed, chỉ đọc):
| Thuật ngữ khởi đầu | Chunk chứa | Hệ quả cho glossary |
|---|---:|---|
| autism / ASD | 942 / 702 | dùng cả hai dạng; "ASD" là từ viết tắt rất phổ biến |
| social communication / social interaction | 143 / 110 | giữ |
| repetitive behaviors (US) / behaviours (UK) | 65 / 8 | **phải có cả hai cách viết**: FTS `english` stem `behavior` và `behaviour` thành 2 lexeme khác nhau (tương tự "challenging behaviour", 101 chunk) |
| restricted interests | **7** | thêm "restricted, repetitive" (35), "circumscribed interests" |
| sensory sensitivity | **14** | thêm "sensory processing" (99), "over-responsivity / hyper-reactivity" (107), "sensory integration" (96) |
| early intervention | 53 | giữ |
| augmentative and alternative communication / AAC | 33 / 98 | thêm "AAC" |
| developmental milestones / milestones | 29 / 96 | thêm "milestones" |
| neurodevelopmental disorder/condition | 43 | thêm "condition" |
| echolalia, joint attention, food selectivity, elopement/wandering | 6, 50, 48, 141 | thêm (có trong bộ eval) |

**Phạm vi:**
- File glossary có phiên bản: đề xuất `config/query_glossary_vi_en_v1.json`, tạo ở T3, không tạo trong T0.
- Mỗi mục gồm: thuật ngữ VI, danh sách EN ưu tiên, biến thể chính tả, ghi chú; có hash phiên bản.
- Kèm unit test cho các quy tắc: không thêm khái niệm ngoài câu hỏi; giữ nguyên từ viết tắt.

**Non-goals:** không dùng LLM; không gọi API dịch; không đổi câu gốc.

**Acceptance criteria:**
- Glossary có phiên bản và hash.
- Mỗi thuật ngữ EN trong glossary xuất hiện ít nhất 1 lần trong corpus (kiểm tự động).
- Bản mở rộng tất định (cùng input cho cùng output).
- Log có đủ phiên bản glossary và bản mở rộng.
- Đo được A vs A-EN vs B trên dataset v1.

---

## C5 — Filtering bắt buộc ở tầng DB query

**Quyết định:** mọi truy vấn retrieval nghiên cứu lọc **trong SQL, trước** `ORDER BY … LIMIT`. Không lấy Top-K rồi mới lọc.

| # | Điều kiện | Ánh xạ cụ thể (cột/đối tượng hiện có) |
|---|---|---|
| 1 | Authorization còn hiệu lực | `research_embedding_authorizations.revoked_at IS NULL` |
| 2 | Chunk thuộc phạm vi authorization | JOIN `research_embedding_authorization_chunks (authorization_id, chunk_id, content_sha256)` |
| 3 | Embedding profile đúng | `research_chunk_embeddings.profile_id` = profile được chọn |
| 4 | Model đúng | `research_chunk_embeddings.model_id = embedding_profiles.model_id` |
| 5 | Dimension đúng | `vector_dimension = 1536` và `vector_dims(embedding) = 1536` |
| 6 | Document hiện hành | `documents.is_current` |
| 7 | Corpus version được chọn | `chunks.chunking_profile = authorizations.chunking_profile` (`section_v2_1`) + `content_sha256` khớp allowlist |
| 8 | Không quarantine | `documents.content_review_status <> 'quarantined'` |
| 9 | Không excluded | chunk có trong allowlist; `retrieval_eligible`; `completeness_status` thuộc nhóm đã kiểm chứng |
| 10 | Quan hệ source/document/chunk hợp lệ | JOIN `chunks → documents → sources` theo khóa ngoại; `documents.source_id` = `authorization_sources.source_id` |

Các điều kiện 1, 2, 6, 7, 8, 9, 10 đã có trong `v_research_embedding_candidates` (migration 006). View của C1 sẽ dùng lại chúng và thêm 3, 4, 5.

**Kiểm thử bắt buộc (positive + negative):** dùng fixture trên container cô lập, không trên DB thật.
- Authorization bị revoke → 0 kết quả.
- Chunk ngoài allowlist có vector → không trả về.
- Content hash lệch → không trả về.
- Profile/model khác → không trả về.
- Document `is_current = false` hoặc quarantined → không trả về.
- Chunk `text_encoding_lost` → không trả về.
- Truy vấn có `LIMIT k` vẫn trả đủ k kết quả hợp lệ khi chunk xếp đầu bị lọc (chứng minh lọc diễn ra trước `LIMIT`).

**Non-goals:** không đưa vector nghiên cứu vào `v_retrieval_ready_chunks` hay `chunk_embeddings`; không mở cho role `app`.

**Quyết định mở cần chủ dự án duyệt (phát sinh trong T1):**
- 47 chunk **danh mục tài liệu tham khảo** (ASD-CSV-017: 27, ASD-CSV-018: 20, heading "*Indicates studies included…") nằm trong allowlist và đã có vector. Đây là nguồn dương tính giả (xem T1).
- Cách xử lý không phá huỷ: tạo **authorization mới** với manifest loại các chunk này, rồi revoke authorization 1. Không xoá vector, không re-chunk.
- Cần trình bày phạm vi trước khi làm.

---

## Dependency map

```
T0 (quyết định) ──► T1 dataset v1 (silver) ──► [H] human verification mẫu ưu tiên cao ──┐
        │                                                                                    │
        ├─► DB-ACCESS: migration 007 (C1 + view C5) ──► T2 dense retriever (A, A-EN) ──┐     │
        │                                                                              ├─► T5 eval harness ─► T8 Top-K
        └─► T3 glossary (C4) + lexical FTS (B) ────────────────────────────────────────┤      (dev/test split)
                                                    T4 fusion RRF + dedupe/diversity (C)┘
   Song song: D-1 quyết định 47 chunk danh mục tham khảo (authorization mới) — trước T5
   Sau T8: (tuỳ chọn) đề xuất thí nghiệm rerank riêng (C3) · evidence gate (T9)
```

| Task | Phụ thuộc | Đầu ra |
|---|---|---|
| DB-ACCESS (migration 007) | T0 C1/C5 | role + view nghiên cứu, probe, rollback |
| T2 Dense | DB-ACCESS | kết quả A/A-EN kèm provenance |
| T3 Glossary + FTS | T0 C4 | glossary v1, kết quả B |
| T4 Fusion | T2, T3 | C (RRF k=60), dedupe, giới hạn số chunk mỗi tài liệu |
| T5 Eval harness | T1, T2–T4 | metric + CI; pool mở rộng từ top-20 → bổ sung nhãn |
| H Human verification | T1 | nâng mẫu ưu tiên cao lên gold |

## 6. Kiểm tra đã chạy cho T0
Truy vấn chỉ đọc trên snapshot của 2.338 chunk đã embed (bảng thuật ngữ ở C4) và trên DB (fingerprint ở báo cáo T1, mục Regression). Không gọi API, không ghi DB.
