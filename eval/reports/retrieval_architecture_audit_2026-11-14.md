# Retrieval Architecture Audit — Phase 6.1 (2026-11-14)

Phạm vi: chỉ đọc. Không sửa code, không migration, không gọi Cohere, không đổi vector/quyền/gate. Mọi truy vấn DB chạy trong transaction `read_only` (SELECT / EXPLAIN ANALYZE trên SELECT). Nhãn bằng chứng: **VERIFIED** (kiểm trực tiếp bằng code/SQL/test), **INFERRED** (suy từ thiết kế hoặc bằng chứng một phần), **UNKNOWN**.

---

## 1. Executive Summary

**Trạng thái hiện tại: chưa có Retrieval runtime.** Thứ duy nhất hệ thống có là *nền dữ liệu* cho retrieval, chưa có *pipeline* retrieval.

**Những gì đã có (VERIFIED):**
- 2.338 vector nghiên cứu (`research_chunk_embeddings`, `vector(1536)`, `embed-v4.0`).
- Cột `chunks.content_tsv` (FTS `english`) cùng GIN index.
- Schema log đã chừa cột cho hybrid: `retrieval_results.dense_rank/sparse_rank/fused_score/rerank_score`, `retrieval_logs.evidence_status`. Hiện chưa có dòng nào.
- Truy vấn vector duy nhất trong code là kiểm tra kỹ thuật `verify --query-check`: exact cosine, `LIMIT 3` viết cứng (`scripts/embed_research.py:365-369`).

**Những gì còn thiếu (VERIFIED):**
- Query processing, dense retriever dùng được, lexical retriever, fusion, dedupe/diversity, reranker, cấu hình Top-K, evidence gate, context builder.
- Bộ dữ liệu đánh giá retrieval.
- 7 thư mục `app/router`, `expert_qa`, `answer`, `safety`, `llm`, `greeting`, `info_lookup` chỉ chứa `.gitkeep`; `eval/datasets/` trống.

**Ba vấn đề quan trọng nhất:**
1. **Lệch ngôn ngữ truy vấn ↔ corpus.**
   - Chunk tiếng Anh: 3.740/3.740 (2.338/2.338 đã embed). Người dùng hỏi bằng tiếng Việt.
   - FTS cấu hình `english` trả **0 kết quả** cho "dấu hiệu sớm tự kỷ".
   - Vector cross-lingual chạy được nhưng cosine thấp hơn: 0,46–0,50 với câu tiếng Việt so với 0,53–0,66 với câu tiếng Anh. Đây là 5 câu thử, chưa đủ để kết luận.
   - Hybrid "đúng nghĩa" vì vậy phụ thuộc bước dịch hoặc mở rộng truy vấn sang tiếng Anh.
2. **Chưa có đường đọc research tối thiểu quyền.**
   - App không đọc được research vector. Đây là mục tiêu đã đạt, VERIFIED.
   - Role duy nhất đọc được (ngoài owner) là **ingest**, mà ingest có `DELETE` trên `chunks` và `chunk_embeddings`.
   - Chạy retrieval/eval bằng ingest là thừa quyền.
   - `retrieval_logs` không có cột phân biệt research/production; ingest cũng không có quyền ghi log.
3. **Chưa có bộ đánh giá có nhãn.** Không thể chọn Top-K, fusion hay reranker một cách khách quan. Mọi con số K hiện nay đều là giả định.

Thêm một điểm cần quyết định: thiết kế đã chốt trước đây ghi "Cohere Rerank" (`SKILL.md` §8). Rerank qua API **gửi lại văn bản chunk ra ngoài**, mà ủy quyền nghiên cứu hiện tại chỉ ghi phạm vi *embedding*.

**Sẵn sàng cho Phase 6.2: READY WITH CONDITIONS** (§9).

---

## 2. Current Architecture

### 2.1 Thực tế (implemented)

```
OFFLINE (implemented, VERIFIED)
data/raw ─build_corpus.py─► data/corpus ─import_sources.py─► sources/source_rights/documents
   └─chunk_pilot.py (section_v2_1)─► chunks (+ content_tsv GENERATED, GIN index)
   └─embedding_preflight.py ─► embedding_manifest.csv
   └─embed_research.py authorize (owner) ─► research_embedding_authorizations (+sources, +chunks allowlist)
   └─embed_research.py run (ingest) ─► Cohere /v2/embed (search_document) ─► research_chunk_embeddings
                                         [trigger research_embedding_guard]

ONLINE (implemented): KHÔNG CÓ.
Chỉ có kiểm tra kỹ thuật:
embed_research.py verify --query-check (ingest):
   5 câu cố định ─► Cohere (search_query) ─► SELECT … ORDER BY embedding <=> q LIMIT 3   (exact, không lọc)
```

### 2.2 Thiết kế (planned, chưa có code) — `README.md` "Luồng xử lý", `SKILL.md` §1

```
câu hỏi → safety → phân loại → greeting | info_lookup (SQL/FTS sources) | expert_qa: dense + FTS → fusion → rerank
         → evidence validation → LLM → answer validation
```

| Thành phần | Implemented | Planned | Bằng chứng |
|---|---|---|---|
| Embedding client (`CohereEmbedder`) | ✔ | | `app/retrieval/embeddings.py` |
| Research vector store + guard | ✔ | | migration 006, `db_check` 34/34 |
| FTS column + GIN | ✔ (chưa code nào dùng) | | `001_core_schema.sql:109-112`, `002_indexes.sql:12`; grep `tsquery|ts_rank` trong `app/ scripts/` = 0 |
| Dense retriever | ✘ (chỉ truy vấn kiểm tra) | ✔ | `scripts/embed_research.py:365-369` |
| Query processing / dịch | ✘ | ✔ ("giữ câu gốc") | `app/router`, `app/expert_qa` trống |
| Fusion / rerank / Top-K / evidence gate | ✘ | ✔ | grep `rerank|fusion|rrf|top_k` trong code = 0 |
| Retrieval logging | schema ✔, code ✘ | ✔ | `retrieval_logs` 0 dòng |
| Router / safety / answer / LLM | ✘ | ✔ | thư mục chỉ có `.gitkeep` |

---

## 3. Technical Audit Matrix

| Component | Current State | Evidence | Risk | Recommendation |
|---|---|---|---|---|
| **Vector Search** | Chỉ có truy vấn kiểm tra: `<=>` (cosine distance), score = `1 − distance`, `LIMIT 3`, **không lọc** profile / authorization / document. Query dùng `search_query`, document dùng `search_document`, cùng `embed-v4.0`/1536 (VERIFIED). Một vector đã lưu tự truy hồi chính nó ở hạng 1 (VERIFIED). | `embed_research.py:356-369`; `embeddings.py` `payload()` gửi `output_dimension=1536`, `validate_vector` kiểm 1536 + finite; `embedding_profiles` (1, `search_document`/`search_query`, cosine) | Nếu một authorization bị revoke, vector cũ vẫn bị truy xuất vì truy vấn không lọc. Nhiều profile sau này sẽ bị trộn. | Retriever chính thức phải JOIN điều kiện authorization active + `profile_id` + document current (qua một research retrieval view). |
| **pgvector Index** | Không có ANN index (cố ý). Plan: Seq Scan 2.338 dòng + top-N heapsort; 61,7 ms lạnh, 11,5–13,0 ms ấm (top-30). Exact search ⇒ recall 100%. | `002_indexes.sql:1-3`; EXPLAIN ANALYZE (§A2) | Không đáng kể ở quy mô hiện tại. | **Chưa** xây HNSW/IVFFlat. Xem lại khi > ~50k vector hoặc p95 > 100 ms. Nếu dùng HNSW thì opclass phải là `vector_cosine_ops` (khớp `<=>`), và filter + ANN cần kiểm recall (pgvector 0.8 iterative scan). |
| **Full-text Search** | Có cột + index, **chưa có code dùng**. `content_tsv = setweight(english(section_heading),'B') ‖ setweight(english(content),'A')`; tiêu đề tài liệu không có trong tsvector. `default_text_search_config = english`. `unaccent`/`pg_trgm` có sẵn nhưng **chưa cài**. Index phủ cả 3 profile (5.470 chunk). | `001_core_schema.sql:109-112`; `ts_debug`, thử nghiệm §A3 | Câu tiếng Việt → 0 kết quả. Ngữ nghĩa AND làm mất recall ("early signs autism toddler" → 2 kết quả). `DSM-5` tách thành `dsm` + `-5`; `M-CHAT-R/F` tách vụn. Nếu quên lọc theo profile sẽ trả chunk v1/v2. | Lexical retriever chạy trên **truy vấn tiếng Anh** (dịch / mở rộng), có chế độ OR, chỉ trên tập research. **Không gọi là BM25**: `ts_rank`/`ts_rank_cd` không có IDF/BM25 saturation. |
| **Hybrid Search** | Không có. | grep = 0; `retrieval_results` có cột dense/sparse/fused nhưng 0 dòng | — | RRF (k=60) làm baseline vì điểm cosine và `ts_rank_cd` không cùng thang; candidate union; dedupe; giữ rank của từng retriever (§5.4, §8). |
| **Reranking** | Không có. Thiết kế cũ ghi Cohere Rerank. | `SKILL.md` §8 | Rerank qua API gửi chunk ra ngoài, nằm ngoài phạm vi ủy quyền (chỉ embedding). Key trial bị giới hạn. Reranker cục bộ cần package/model mới. | Quyết định trước 6.2 (§9). Đánh giá D sau A–C. Không coi điểm rerank là xác suất đúng. |
| **Top-K** | Không có cấu hình. Chỉ có `LIMIT 3` viết cứng trong script kiểm tra. `retrieval_logs.top_k` tồn tại. `config/` chỉ có `chunking_profiles.json`, `embedding_profiles.json`. | `ls config`; `embed_research.py:369` | Chọn K tuỳ ý. | `config/retrieval_profiles.json`: candidate K riêng cho dense/lexical, final K, giới hạn mỗi tài liệu, ngân sách token. Chọn bằng thí nghiệm (§6). |
| **Metadata Filtering** | Ở mức dữ liệu: preflight + allowlist + view `v_research_embedding_candidates` (current, không quarantine, `core`/`gaps`, `retrieval_eligible`, status đã kiểm chứng). Ở mức truy vấn: không có. | migration 006 §4; `embedding_manifest.py` | Lọc thời điểm truy vấn chưa tồn tại (xem Vector Search). Chưa có lọc theo chủ đề/độ tuổi/loại nguồn. | Research retrieval view gom vector + provenance + điều kiện active. Lọc tuỳ chọn theo `source_type` / `publisher` qua metadata đã có. |
| **Evidence Gate** | Chỉ có enum trong schema (`sufficient`/`partial`/`conflicting`/`insufficient`/`blocked`). Không có logic. | `001_core_schema.sql` `retrieval_logs.evidence_status` | Không có gate thì câu ngoài phạm vi vẫn nhận "bằng chứng". | Thiết kế ở 6.2/6.3, ngưỡng hiệu chỉnh trên câu thiếu bằng chứng của bộ eval. Reranker không thay thế gate. |
| **Provenance** | Đầy đủ ở dữ liệu: chunk → document (version, URL qua sources) → source; section_path; page (PDF) hoặc char range; `content_sha256`; `chunking_profile`. Vector có `model_id`, `vector_dimension`, `run_id`, `embedding_input_hash`, `authorization_id`. 13/13 kiểm tra provenance đạt. | `embedding_quality_check.md`; `test_research_embeddings.py` | `retrieval_results` không lưu `content_sha256`, scope hay profile cho từng kết quả (chỉ ở cấp log qua `profile_id`/`configuration`). | Kiểu `RetrievalCandidate` mang đủ trường (§8, T2). Khi ghi kết quả, lưu scope + hash trong `configuration` hoặc migration sau. |
| **Research Isolation** | Đạt cho role app (VERIFIED, §4). Đọc research = owner hoặc ingest (thừa quyền ghi). | `has_table_privilege` §4; `db_check` 34/34; integration test | Dùng ingest cho eval làm tăng bề mặt rủi ro (DELETE chunks). | Điều kiện C1 (§9). |

---

## 4. Database Security Review (migration 006 và quyền hiện tại)

Mọi kết quả dưới đây là truy vấn chỉ đọc trên DB thật, ngày 14/11/2026.

| # | Câu hỏi | Kết quả | Nhãn |
|---|---|---|---|
| 1 | Bảng/đối tượng 006 tạo ra | `research_embedding_authorizations`, `…_authorization_sources`, `…_authorization_chunks`, view `v_research_embedding_candidates`, `research_chunk_embeddings` (+ index `run_id`), function `research_embedding_guard()` (SECURITY INVOKER) + trigger BEFORE INSERT/UPDATE. Owner sở hữu tất cả. | VERIFIED |
| 2 | Role được cấp quyền | ingest: `SELECT` trên 3 bảng authorization + view; `SELECT, INSERT` trên `research_chunk_embeddings`. app: không có. PUBLIC: không có ACL bảng. | VERIFIED (`has_table_privilege`) |
| 3 | Quyền ingest (toàn schema, liên quan) | `chunks` S/I/D; `chunk_embeddings` S/I/D; `research_chunk_embeddings` S/I (không U/D); các view S; `retrieval_logs/results/answer_runs` chỉ S. | VERIFIED |
| 4 | App đọc được research vector? | **Không**: `research_chunk_embeddings`, `v_research_embedding_candidates` và các bảng authorization đều `-`. Không có column grant. Không membership role nào (`pg_auth_members` rỗng). Không role nào có `BYPASSRLS`/superuser. | VERIFIED; integration test `test_app_role_cannot_read_research_vectors` |
| 5 | Đường gián tiếp qua view/function | Chỉ `v_research_embedding_candidates` phụ thuộc bảng research (`pg_depend`), và chỉ ingest được cấp. Không có function SECURITY DEFINER trong schema. App có `EXECUTE` mặc định trên `research_embedding_guard()` (PUBLIC execute mặc định), nhưng đây là trigger function, không gọi trực tiếp được, và vẫn là SECURITY INVOKER. | VERIFIED; rủi ro thấp (vệ sinh: `REVOKE EXECUTE … FROM PUBLIC` ở migration sau) |
| 6 | Production view có lấy research vector? | Không. `v_retrieval_ready_chunks` dựa trên {chunks, sources, source_rights, v_embedding_eligible_documents}; `v_embedding_eligible_documents` dựa trên {documents, sources, source_rights}; không view nào chứa `chunk_embeddings` hay research. | VERIFIED (`pg_depend`, `pg_get_viewdef`) |
| 7 | Truy vấn chéo research ↔ production | Chỉ role có SELECT trên cả hai (owner, ingest). App thì không. Hai bảng vector tách biệt, khác tên, không UNION trong view nào. | VERIFIED |
| 8 | Ghi vector sai chunk/model | Bị chặn bởi trigger (allowlist ∩ current candidate ∩ content hash ∩ model ∩ dimension ∩ input_type), `UNIQUE(chunk_id, profile_id)`, `CHECK vector_dims = 1536`, FK. Đã kiểm bằng 21 probe trên container cô lập (`embedding_research_gate_proposal_2026-11-14.md`) và 13 kiểm tra trên dữ liệu thật. | VERIFIED |

Phát hiện thêm (không thuộc 006):

- **F1:** App có `SELECT` trực tiếp trên `chunk_embeddings` (production, hiện 0 dòng), không qua gate theo chunk.
  - Khi production có vector, dense search của app trên bảng này sẽ trả về `chunk_id` của tài liệu chưa duyệt. Nội dung thì không lộ, vì app không đọc được `chunks`.
  - Đề xuất: khi mở production, dense search phải qua một view gated, và thu hồi SELECT trực tiếp. INFERRED, tương lai.
- **F2:** `retrieval_results.chunk_id` là FK `ON DELETE RESTRICT`. Khi có log, chunk không xoá được nữa; điều này phù hợp chủ trương không re-chunk.
- **F3:** Không có RLS. Tất cả view là security-definer theo kiểu view mặc định (chạy bằng quyền owner); đây là thiết kế cố ý để app đọc chunk qua gate.

---

## 5. Retrieval Evaluation Design

### 5.1 Tính khả thi với dữ liệu hiện có
- **Khả thi về độ phủ chủ đề** (INFERRED từ tiêu đề 71 nguồn, §A5):
  - Cơ bản: CDC, NIMH, review tổng quan.
  - Dấu hiệu: CDC signs, milestones 2–36 tháng.
  - Giao tiếp: NIDCD, AAC, minimally verbal.
  - Hành vi: food selectivity, elopement, WHO-CST.
  - Chẩn đoán: M-CHAT, DSM, Việt Nam.
  - Can thiệp: NDBI, parent-mediated, ABA, social skills, giấc ngủ, melatonin.
  - Cảm giác: SenITA, ASI, sensory-based.
  - Phát triển trẻ nhỏ: WHO ECD, parenting 0–3 tuổi.
- **Giới hạn:**
  - Corpus tiếng Anh, nên người gán nhãn phải đọc tiếng Anh.
  - Chủ đề ít nguồn: hành vi lặp lại không có tài liệu chuyên biệt; vắc-xin, chế độ ăn, thuốc cụ thể thiếu hoặc rất ít.
  - Không có `relevant_chunk_ids` nào được xác nhận.
- **Kết luận:** xây được bộ đánh giá đáng tin, **với điều kiện** gán nhãn theo pooling + người duyệt (§5.3). Bộ câu hỏi nháp ở Phụ lục B chỉ là **ứng viên**: mọi `relevant_chunk_ids = pending_annotation`; `expected_sources` suy từ tiêu đề nên cũng `pending_annotation`.

### 5.2 Định dạng (tương thích `references/data-contracts.md` §5, mở rộng)

`eval/datasets/retrieval_vi_v1.jsonl`, mỗi dòng:
```json
{"question_id": "q007", "question": "…", "question_en_reference": "…", "category": "signs",
 "expected_route": "expert_qa", "expected_sources": ["CDC-ASD-SIGNS"], "relevant_document_ids": "pending_annotation",
 "relevant_chunk_ids": "pending_annotation", "grades": {}, "requires_multiple_chunks": true,
 "expected_evidence": "≥1 chunk nêu dấu hiệu giao tiếp xã hội ở 12–24 tháng", "expected_evidence_status": "sufficient",
 "must_refuse": false, "annotation_status": "pending_annotation", "notes": ""}
```

`question_en_reference` là bản tiếng Anh do người viết, dùng để đo khoảng cách cross-lingual. Không được dùng làm truy vấn của hệ thống.

### 5.3 Quy trình gán nhãn
1. **Pooling:** hợp top-20 của mỗi cấu hình A, B, C (và D nếu có), cộng các chunk từ `expected_sources`. Gán nhãn *cả pool*, không chỉ kết quả của một hệ.
2. **Thang điểm theo từng (câu hỏi, chunk):**
   - 2 = Relevant: nội dung trực tiếp là bằng chứng trả lời.
   - 1 = Partially relevant: đúng chủ đề, thiếu một phần hoặc gián tiếp.
   - 0 = Irrelevant: kể cả khi chỉ trùng từ khóa.
   - Cờ `conflicting` khi chunk mâu thuẫn với chunk relevant khác.
3. **Người gán:** 2 người độc lập. Đo Cohen's κ trên nhãn nhị phân (≥1) và weighted κ trên thang 0–2. Mục tiêu κ ≥ 0,6. Nếu thấp hơn thì sửa hướng dẫn rồi gán lại. Bất đồng do người thứ ba quyết.
4. **Chuyên gia ASD** duyệt câu hỏi và các chunk mang khẳng định lâm sàng. Chưa duyệt thì ghi `expert_review: pending`.
5. Đánh dấu `requires_multiple_chunks` và liệt kê các *khía cạnh bằng chứng* (aspects) cho câu nhiều khía cạnh, để đo Evidence Coverage.
6. **Chia tập:** dev ~60% (chọn K/fusion/ngưỡng) và test ~40% (chỉ chạy một lần khi chốt). Phân tầng theo category.
7. **Phiên bản hoá:** `retrieval_vi_v1` gắn với `section_v2_1` + `cohere_embed_v4_1536_v1` + manifest `542cce21…`. Đổi corpus thì phải đánh giá lại pool.

### 5.4 Metrics
| Metric | Mức | Định nghĩa |
|---|---|---|
| Recall@K | chunk & source | số mục relevant (grade 2; biến thể ≥1) trong top-K ÷ tổng mục relevant đã gán |
| Precision@K | chunk | số mục relevant trong top-K ÷ K |
| Hit Rate@K | chunk & source | tỉ lệ câu có ≥1 mục relevant trong top-K |
| MRR | chunk | 1 / hạng của mục relevant đầu tiên |
| nDCG@K | chunk | gain theo grade 0/1/2, IDCG từ toàn bộ nhãn |
| Evidence Coverage@K | câu nhiều khía cạnh | số khía cạnh có ≥1 chunk grade 2 trong top-K ÷ tổng số khía cạnh |
| Source Diversity@K | kết quả | số nguồn khác nhau trong top-K; tỉ lệ chunk thuộc nguồn chiếm nhiều nhất |
| Duplicate Rate@K | kết quả | tỉ lệ cặp trong top-K có cosine > 0,95 hoặc cùng hash |
| Latency | hệ thống | p50/p95 cho từng bước (embed query, dense, lexical, fusion, rerank) |
| Abstention signal | câu thiếu/ngoài phạm vi | phân bố điểm cao nhất; AUROC phân biệt câu có và không có bằng chứng (đầu vào cho evidence gate) |

**Ưu tiên cho ASD:**
- **Evidence Coverage@K và Recall@K ở mức chunk là chỉ số chính.** Câu trả lời y khoa sai thường do *thiếu* bằng chứng hoặc bằng chứng một chiều, chứ không do thừa. Bỏ sót một khuyến nghị (ví dụ "chưa đủ bằng chứng cho SIT") nguy hiểm hơn có thêm một chunk thừa.
- **nDCG@K là chỉ số phụ**, vì context bị giới hạn token nên thứ hạng quan trọng.
- Source-level recall dễ đạt hơn và **không đủ**: đúng nguồn chưa chắc đúng đoạn.
- Báo cáo kèm khoảng tin cậy bootstrap (n nhỏ) và kiểm định cặp (paired bootstrap / Wilcoxon) khi so sánh cấu hình.

### 5.5 Baseline (cùng câu hỏi, cùng tập 2.338 chunk, cùng lọc)
| Cấu hình | Mô tả |
|---|---|
| A | Dense only: `embed-v4.0` `search_query` trên câu tiếng Việt gốc; biến thể A′ chạy trên câu tiếng Anh tham chiếu (chỉ để đo khoảng cách ngôn ngữ) |
| B | Lexical only: FTS `english` trên truy vấn tiếng Anh sinh ra từ câu tiếng Việt (cách sinh là biến thí nghiệm: glossary / dịch máy) |
| C | Hybrid: A ∪ B, RRF k=60, dedupe, giới hạn mỗi tài liệu |
| D | C + reranker (sau quyết định §9) |

Mọi cấu hình ghi vào báo cáo: profile chunk/embedding, manifest SHA, bộ lọc, K, phiên bản code. Query embedding được **cache** (chỉ câu hỏi, không nội dung tài liệu) để lặp thí nghiệm không tốn API: 62 câu × 2 ngôn ngữ ≈ 124 input ≈ 2 lời gọi.

### 5.6 Test cases bắt buộc ngoài metric
- Câu thiếu bằng chứng hoặc ngoài phạm vi (Phụ lục B nhóm 10) phải ra `insufficient`/`blocked`, không được ép thành `sufficient`.
- Câu có từ viết tắt (ASD, AAC, ADHD, DSM-5, M-CHAT-R/F).
- Câu yêu cầu cụm từ chính xác ("joint attention").
- Câu có thể bị boilerplate chen vào (§7: workbook, footer CDC).
- Câu về độ tuổi cụ thể (milestones), để phát hiện nhầm giữa các trang tuổi gần nhau.

---

## 6. Top-K Experiment Plan

| Biến | Giá trị |
|---|---|
| Candidate K (mỗi retriever) | 10, 20, 30 |
| Final K | 3, 5, 8, 10 |
| Max chunk / tài liệu trong final | 1, 2, 3, không giới hạn |
| Cấu hình | A, B, C, D |
| Ngân sách token context | ghi lại (median chunk 323 token, p90 563, max 704), nên 8 chunk ≈ 2,6k token median, ≤ 5,6k p90 |

Tổng: 3 × 4 × 4 × 4 = 192 ô. Dense và lexical tính một lần ở K=30, các ô còn lại cắt trên kết quả đã cache, nên chi phí API không tăng.

**Cách chọn:**
1. Trên **dev**: lọc các ô đạt Evidence Coverage@finalK cao nhất ±1 SE (bootstrap).
2. Trong nhóm đó, chọn **final K nhỏ nhất** (tiết kiệm token, giảm nhiễu cho LLM), rồi candidate K nhỏ nhất nếu reranker không cải thiện với K lớn hơn.
3. Ràng buộc phụ: Duplicate Rate@K ≤ ngưỡng, Source Diversity không giảm, p95 latency trong ngân sách.
4. Chạy cấu hình đã chọn **một lần** trên **test** và báo cáo kèm CI. Không tinh chỉnh tiếp trên test.
5. Không tuyên bố "Top-5 tối ưu" nếu khác biệt giữa các K nằm trong CI.

---

## 7. Risk Register

| Risk | Severity | Evidence | Mitigation |
|---|---|---|---|
| R1: Lệch ngôn ngữ VI ↔ EN làm hỏng lexical và giảm dense | **High** | 3.740/3.740 chunk `en`; FTS "dấu hiệu sớm tự kỷ" = 0; cosine VI 0,46–0,50 vs EN 0,53–0,66 (n=5) | Bước query processing sinh truy vấn tiếng Anh (glossary ASD + dịch); đo A vs A′; giữ câu gốc trong log ở dạng hash |
| R2: Không có bộ eval có nhãn nên chọn K/fusion/rerank tuỳ ý | **High** | `eval/datasets/` trống | §5, điều kiện C2 |
| R3: Retrieval research chạy bằng role ingest (có DELETE) | Medium | §4 #3 | C1: role/view chỉ đọc hoặc kết nối read-only bắt buộc |
| R4: Truy vấn không lọc authorization/profile nên vector của ủy quyền đã thu hồi vẫn được dùng | Medium | `embed_research.py:365-369` | Research retrieval view có điều kiện active + profile (C5) |
| R5: Rerank qua API gửi chunk ra ngoài, nằm ngoài phạm vi ủy quyền | Medium | `SKILL.md` §8; authorization 1 chỉ cho embedding | Quyết định C3; ưu tiên reranker cục bộ hoặc ủy quyền mở rộng có ghi DB |
| R6: Gần-trùng chiếm top-K (chunk bảng nối tiếp cùng header) | Medium | 108 cặp cosine > 0,95, 107 cùng nguồn (ASD-SUP-PMC11754701: 18 chunk bảng) | Giới hạn chunk/tài liệu, gộp chunk bảng liên tiếp, đo Duplicate Rate |
| R7: Boilerplate lọt vào kết quả | Medium | workbook "check your answers" 14 chunk; footer CDC "Updates may include…" 15 chunk/13 nguồn; "Content source" 18; placeholder hình 102 chunk | Cờ chất lượng ở thời điểm truy vấn (bảng cờ riêng, không sửa chunk), đo trong eval trước khi loại |
| R8: Nguồn dài lấn át (SENITA 171, ASD-NEW-002 115 chunk; 4 nguồn lớn nhất = 20,9%) | Low–Med | §A4 | Diversity cap; đo Source Diversity |
| R9: AND-semantics của FTS làm recall thấp | Medium | "early signs autism toddler" = 2 kết quả | Chế độ OR / tách từ khóa; đo recall B |
| R10: Gọi FTS là BM25 làm hiểu sai kết quả | Low | `ts_rank_cd` không có IDF | Đặt tên đúng "PostgreSQL FTS (ts_rank_cd)" trong code/báo cáo |
| R11: Điểm similarity/rerank bị hiểu là "độ đúng y khoa" | High (khi có answer) | — | Evidence gate tách biệt; không hiển thị điểm cho người dùng |
| R12: Trial key (trần token/phút, 1.000 request/tháng) | Low | `embedding_run_report.md` | Cache query embedding; nhóm câu theo lô 96 |
| R13: Nội dung hữu ích bị loại (32 `unclassified`, gồm WHO-CST session 7; 11 bảng chờ duyệt) | Medium | `embedding_excluded.csv`; SENITA 16, PARTICIPANTS 14, ECD 2 | Người duyệt chọn từng chunk, rồi authorization mới cho phần chênh lệch (không re-chunk) |
| R14: Index FTS phủ 3 profile, quên lọc sẽ trả chunk v1/v2 | Low | EXPLAIN FTS: 205 hàng khớp trên mọi profile | Mọi truy vấn lexical JOIN tập research |
| R15: App có SELECT trực tiếp `chunk_embeddings` (production) | Low (hiện 0 dòng) | §4 F1 | View gated + revoke khi mở production |

---

## 8. Phase 6.2 Implementation Roadmap

Thứ tự theo phụ thuộc. Không task nào đổi chunk hay vector.

Cấu trúc thư mục giữ nguyên:
- `app/retrieval/` (chỉ tầng này gọi API embedding/rerank — `SKILL.md`).
- `app/expert_qa/` cho query processing.
- `config/` cho tham số.
- `scripts/` cho entry point.
- `eval/`.

| # | Objective | Files/modules | Expected output | Acceptance criteria | Tests | Risks |
|---|---|---|---|---|---|---|
| T0 | Chốt C1–C4 (§9) | báo cáo quyết định; nếu chọn role mới: `migrations/007_*` + rollback | quyết định ghi trong `SKILL.md` §8 | Có quyết định cho C1–C4; nếu có migration: chạy thử trên container cô lập, `db_check` pass | db_check, integration | thay đổi quyền phải trình bày phạm vi trước |
| T1 | Bộ câu hỏi v1 + công cụ gán nhãn | `eval/datasets/retrieval_vi_v1.jsonl`, `scripts/retrieval_pool.py` (xuất pool), bảng gán nhãn CSV | ≥ 60 câu, 10 nhóm, `pending_annotation` | Schema hợp lệ; mọi trường bắt buộc có; không chunk ID bịa | unit: validate schema | thiên lệch câu hỏi theo nguồn đã biết |
| T2 | Kiểu dữ liệu + dense retriever research | `app/retrieval/types.py` (`RetrievalQuery`, `RetrievalCandidate` mang provenance đầy đủ + rank/score theo retriever), `app/retrieval/dense.py`, research retrieval view (nếu C1) | top-K kèm source/document/chunk/title/URL/section/page/char range/hash/profile/model | Lọc profile + authorization active + current; kết quả giống truy vấn exact tham chiếu | unit (fake vector), integration read-only (self-hit, lọc revoke trên container test) | thừa quyền nếu C1 chưa xong |
| T3 | Query processing VI→EN + lexical retriever | `app/expert_qa/query_processing.py` (glossary ASD trong `config/`), `app/retrieval/lexical.py` | truy vấn EN + tsquery OR/phrase; kết quả FTS trên tập research | 0 kết quả từ profile khác; acronyms/phrases qua test | unit (tsquery builder), integration | chất lượng dịch; nếu dịch bằng LLM thì cần quyết định provider |
| T4 | Fusion + dedupe + diversity | `app/retrieval/fusion.py`, `config/retrieval_profiles.json` | RRF, dedupe theo chunk_id/hash/near-dup, cap theo tài liệu | Không mất provenance; deterministic (tie-break theo chunk_id) | unit (RRF toán học, tie, dedupe) | trọng số tuỳ ý (chỉ dùng RRF thuần ở baseline) |
| T5 | Harness đánh giá | `scripts/retrieval_eval.py`, cache query embedding trong `data/index/` (git-ignored) | báo cáo A/A′/B/C: metric + CI + latency | Chạy lại cho cùng kết quả; 0 lời gọi API ở lần chạy lại | unit (metric trên ví dụ tay), integration | n nhỏ nên CI rộng |
| T6 | Gán nhãn pool + κ | kết quả T1/T5 | nhãn v1, báo cáo κ | κ ≥ 0,6 hoặc vòng sửa hướng dẫn | — | thiếu người gán / chuyên gia |
| T7 | Reranker (theo C3) | `app/retrieval/rerank.py` | cấu hình D | Không gửi dữ liệu ra ngoài khi chưa có ủy quyền ghi DB; điểm không hiển thị cho người dùng | unit (fake reranker), eval | package/model mới; chi phí |
| T8 | Thí nghiệm Top-K + chọn cấu hình | §6 | `eval/reports/retrieval_benchmark_<date>.md` | Chọn trên dev, xác nhận một lần trên test | — | overfit dev |
| T9 | Thiết kế evidence gate (có thể sang 6.3) | `app/expert_qa/evidence.py` | trạng thái 5 mức | Hiệu chỉnh trên câu nhóm 10; không dùng điểm rerank thay gate | unit + eval | false "sufficient" |
| T10 | Logging retrieval (research) | quyết định: file JSON trong `eval/reports` hoặc migration bổ sung scope | log không lưu nguyên văn câu hỏi | Hash câu hỏi; scope research ghi rõ | integration | trộn log research/production |

Interface gợi ý (để test độc lập, không phá cấu trúc):
- `DenseRetriever.search(q: RetrievalQuery, k: int) -> list[RetrievalCandidate]`
- `LexicalRetriever.search(q, k)` với cùng kiểu kết quả
- `fuse(lists, cfg) -> list[RetrievalCandidate]`
- `Reranker.rerank(q, cands) -> list[RetrievalCandidate]`
- `EvidenceGate.assess(q, cands) -> EvidenceStatus`

DB access được truyền vào qua connection factory, nên unit test chạy được với fake.

---

## 9. Final Decision

**READY WITH CONDITIONS.** Database isolation và trạng thái thực của retrieval đã được kiểm (VERIFIED). Phase 6.2 có thể bắt đầu khi xử lý xong:

| ID | Điều kiện | Lựa chọn |
|---|---|---|
| C1 | Đường đọc research tối thiểu quyền | (a) migration 007: view `v_research_retrieval_chunks` + role chỉ đọc mới, trình bày phạm vi trước; hoặc (b) không đổi DB: retriever research dùng ingest qua kết nối bắt buộc `read_only`, có test chứng minh |
| C2 | Bộ eval v1 (T1) phải có **trước** khi chọn K, fusion, reranker | — |
| C3 | Quyết định reranker và dữ liệu đi ra ngoài | Cohere Rerank cần mở rộng ủy quyền (ghi DB, phạm vi `rerank`); reranker cục bộ đa ngữ (ví dụ họ BGE reranker) cần cài package/model, chạy CPU; hoặc tạm bỏ D |
| C4 | Chiến lược truy vấn tiếng Việt | glossary + dịch (LLM nào, gửi câu hỏi ra ngoài thế nào); coi là biến thí nghiệm A vs A′ |
| C5 | Retriever lọc theo authorization active + `profile_id` + document current | bắt buộc trong T2 |

---

## 10. Trả lời 12 câu hỏi của Phase 6.1

| # | Câu hỏi | Trả lời | Nhãn |
|---|---|---|---|
| 1 | Thành phần retrieval hiện có | Vector store research + guard; cột FTS + GIN; schema log; client embedding. Không có retriever runtime. | VERIFIED |
| 2 | Vector search đã chạy trên research vector? | Chỉ ở mức kiểm tra kỹ thuật (5 câu, exact, `LIMIT 3`); self-hit đúng; không có retriever dùng được. | VERIFIED |
| 3 | Index / operator | Không ANN; Seq Scan + top-N heapsort; operator `<=>` cosine distance; score `1 − d`. | VERIFIED |
| 4 | FTS | Có cột/index (`english`), không có code truy vấn; không xử lý tiếng Việt; không phải BM25. | VERIFIED |
| 5 | Hybrid | Không. | VERIFIED |
| 6 | Hợp nhất nhiều retriever | Không (chỉ có cột trong `retrieval_results`). | VERIFIED |
| 7 | Reranking | Không. | VERIFIED |
| 8 | Top-K | Chỉ `LIMIT 3` viết cứng trong script kiểm tra; không có cấu hình. | VERIFIED |
| 9 | Metadata filter | Ở mức dữ liệu (preflight/allowlist/view); không có ở mức truy vấn. | VERIFIED |
| 10 | Chặn app đọc research | Không grant, không membership, không view/function gián tiếp, production view không phụ thuộc. | VERIFIED |
| 11 | Xây bộ eval khách quan được không | Được, với pooling + 2 người gán + chuyên gia; bộ câu hỏi ứng viên ở Phụ lục B. Độ phủ thấp ở vài chủ đề. | INFERRED (chưa có nhãn) |
| 12 | Việc trước 6.2 | C1–C5, T0–T1. | — |

## 11. Acceptance criteria của Phase 6.1

| # | Tiêu chí | Kết quả |
|---|---|---|
| 1 | Workspace & kiến trúc thực tế | PASS (§2) |
| 2 | Bảng & đường truy cập research | PASS (§4) |
| 3 | Audit 006 & quyền hiện tại | PASS (§4, truy vấn trên DB thật) |
| 4 | Vector search implementation | PASS (§3; không tồn tại ngoài script kiểm tra) |
| 5 | FTS | PASS (§3, §A3) |
| 6 | Hybrid | PASS (không có) |
| 7 | Reranking | PASS (không có) |
| 8 | Vị trí/cơ chế Top-K | PASS |
| 9 | Provenance & metadata filter | PASS |
| 10 | Thiết kế eval dataset | PASS (thiết kế); nhãn: NOT VERIFIED (chưa gán) |
| 11 | Ma trận Top-K | PASS (§6) |
| 12 | Roadmap 6.2 | PASS (§8) |
| 13 | Không thay đổi ngoài ý muốn | PASS. Vân tay 65 file code/migration/config/test trước và sau giống nhau; số đếm DB trước và sau giống nhau (§A1) |

---

## Phụ lục A — Bằng chứng đo đạc

**A1. Vân tay (trước = sau)**
- Code: SHA-256 của danh sách hash 65 file trong `app/ scripts/ migrations/ config/ tests/ deploy/ pyproject.toml` = `efb284533cc517d4…`.
- DB: chunks 5.470; research vector 2.338; production vector 0; ingestion_runs 17; authorizations 1; retrieval_logs 0; migrations 6.
- Checksum (chunk_id + input hash + norm) của research vector không đổi.

**A2. Vector (EXPLAIN ANALYZE, dùng một vector đã lưu làm truy vấn, không gọi API)**
- Plan: `Limit → Sort (top-N heapsort, 31kB) → Seq Scan on research_chunk_embeddings (2.338 rows)`, 28.184 buffer hit.
- Thời gian: 61,7 ms lần đầu; 5 lần đo ấm phía client 11,5–13,0 ms (top-30).
- Kích thước: `research_chunk_embeddings` 20 MB, `chunks` 50 MB.

**A3. FTS (`english`)**
- `ts_debug`:
  - `ASD` → `asd`, `ADHD` → `adhd`, `AAC` → `aac`.
  - `DSM-5` → `dsm` + `-5`.
  - `M-CHAT-R/F` → `m-chat-r`, `m`, `chat`, `r`, `/f`.
  - `tự kỷ` → `tự`, `kỷ` (không stem; corpus không có từ này).
- Số kết quả trên tập đã embed:

  | Truy vấn | Kết quả |
  |---|---:|
  | "sensory integration therapy" | 63 |
  | "early signs autism toddler" | 2 |
  | "dấu hiệu sớm tự kỷ" | 0 |
  | "ADHD comorbidity" | 72 |
  | `"joint attention"` (phrase) | 50 |

- Plan: Bitmap Index Scan trên `chunks_content_tsv_idx`, 9,8 ms; 205 hàng khớp trên **mọi profile** trước khi lọc.

**A4. Chất lượng tập đã embed**
- Ngôn ngữ: `en` 2.338/2.338. Có 14 chunk mang dấu tiếng Việt, đều là tên người/địa danh trong ASD-OA-PMC13005892.
- Token: median 323, p90 563, max 704. Có 110 chunk < 40 token.
- `content_kind`: text 1.981, table 357.
- Nguồn nhiều chunk nhất:

  | Nguồn | Chunk |
  |---|---:|
  | NIHR-SENITA-2022 | 171 |
  | ASD-NEW-002 | 115 |
  | ASD-OA-PMC12468522 | 104 |
  | WHO-ECD-GUIDELINE-2020 | 98 |
  | 4 nguồn trên cộng lại | 20,9% |
  | Số nguồn ≤ 5 chunk | 4 |

- Gần-trùng (cosine > 0,95): 108 cặp, trong đó 107 cùng nguồn và chủ yếu là chunk bảng nối tiếp (ASD-SUP-PMC11754701: 18, ASD-CSV-062: 8). Cặp khác nguồn duy nhất là footer CDC giống nhau.
- Boilerplate:
  - workbook "check your answers / questions to check your own learning": 14 (WHO-CST-PARTICIPANTS);
  - footer CDC "Updates may include minor edits": 15 chunk / 13 nguồn; "Content source": 18 / 17;
  - placeholder "Image:" / "[Original asset:": 102 (ASD-NEW-002 15, …);
  - thông báo public domain NIH: 4.
- **Ghi chú phương pháp:** một "lỗi mất chữ s" quan sát được ban đầu là **artefact của chính truy vấn audit** (regex trong `regexp_replace`). Kiểm tra từng code point cho thấy văn bản gốc đúng; tỉ lệ chữ "s" mọi tài liệu bình thường (min 5,98%, median 7,17%); không có ký tự private-use/replacement. **Không phải lỗi dữ liệu.**

**A5. Thành phần nguồn đã embed:**
- research: 44 nguồn, 1.771 chunk;
- research_report: 1 nguồn, 171 chunk;
- official_patient_information: 21 nguồn, 216 chunk;
- official_guideline: 1 nguồn, 98 chunk;
- official_training_manual: 2 nguồn, 67 chunk;
- official_health_education: 2 nguồn, 15 chunk.

**A6. Câu cần xác minh thêm (UNKNOWN)**
- Mức giảm thật của dense retrieval khi hỏi bằng tiếng Việt (chỉ có 5 câu thử).
- Hiệu quả của reranker đa ngữ trên corpus này.
- Có nên đưa tiêu đề tài liệu vào FTS không (hiện chỉ có heading + content).
- Model/phiên bản reranker cụ thể và điều khoản dữ liệu tại thời điểm quyết định.

---

## Phụ lục B — Bộ câu hỏi ứng viên (v0, chưa duyệt)

`expected_sources` suy từ **tiêu đề**, chỉ là ứng viên. Tất cả `relevant_chunk_ids` / `relevant_document_ids` = `pending_annotation`; `expert_review = pending`.

| ID | Nhóm | Câu hỏi | Nguồn ứng viên | Bằng chứng kỳ vọng |
|---|---|---|---|---|
| q001 | 1 Cơ bản | Rối loạn phổ tự kỷ là gì? | CDC-ASD-ABOUT, NIH-NIMH-ASD-2025, ASD-OA-PMC12468522 | định nghĩa + "phổ" |
| q002 | 1 | Tự kỷ phổ biến như thế nào ở trẻ em? | CDC-ASD-ABOUT, ASD-OA-PMC6487529, ASD-OA-PMC12468522 | số liệu tỉ lệ, có nguồn/năm |
| q003 | 1 | Những yếu tố nào làm tăng nguy cơ tự kỷ? | NIH-NIMH-ASD-2025, CDC-ASD-ABOUT, ASD-OA-PMC12468522 | nhiều yếu tố, nhiều chunk |
| q004 | 1 | Tự kỷ có chữa khỏi được không? | CDC-ASD-TREATMENT, NIH-NIMH-ASD-2025 | không chữa khỏi + hỗ trợ cải thiện |
| q005 | 1 | Nghiên cứu về tự kỷ ở Việt Nam hiện nay ra sao? | ASD-OA-PMC13005892, ASD-CSV-038 | tổng quan bối cảnh VN |
| q006 | 1 | Tự kỷ ở trẻ gái có biểu hiện khác trẻ trai không? | ASD-OA-PMC12468522 (?) | có thể thiếu → partial |
| q007 | 2 Dấu hiệu | Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì? | CDC-ASD-SIGNS, CDC-MILESTONES-18, ASD-CSV-091 | dấu hiệu giao tiếp xã hội + hành vi |
| q008 | 2 | Khi nào cha mẹ nên lo lắng về sự phát triển của con? | CDC-CONCERNED | các bước khi lo lắng |
| q009 | 2 | Trẻ không quay lại khi gọi tên có phải dấu hiệu tự kỷ? | CDC-ASD-SIGNS, NIH-NIMH-ASD-2025 | là một dấu hiệu, không đủ để chẩn đoán |
| q010 | 2 | Có thể nhận ra dấu hiệu tự kỷ ở trẻ dưới 12 tháng không? | ASD-NEW-001, CDC-ASD-SIGNS | bằng chứng sơ sinh/infant |
| q011 | 2 | Tự kỷ ở tuổi dậy thì có những thách thức gì? | ASD-OA-PMC12593641, NIH-NIMH-TEEN-BRAIN | chuyển tiếp tuổi vị thành niên |
| q012 | 2 | Trẻ mất kỹ năng đã có (thoái lui) thì cần làm gì? | CDC-ASD-SIGNS, CDC-CONCERNED | dấu hiệu cảnh báo + đi khám |
| q013 | 3 Giao tiếp | Trẻ tự kỷ thường gặp những khó khăn giao tiếp nào? | NIH-NIDCD-ASD-COMMUNICATION-2020 | các dạng khó khăn |
| q014 | 3 | Làm sao hỗ trợ trẻ tự kỷ chưa biết nói? | ASD-SUP-PMC13414371, ASD-CSV-084 | can thiệp cho trẻ ít lời |
| q015 | 3 | Giao tiếp thay thế (AAC) có làm trẻ chậm nói hơn không? | ASD-CSV-084, ASD-CSV-017, ASD-OA-PMC13393316 | bằng chứng AAC và ngôn ngữ nói |
| q016 | 3 | "Chú ý chung" (joint attention) là gì và tập thế nào? | ASD-OA-PMC10774556, ASD-CSV-017 | định nghĩa + can thiệp |
| q017 | 3 | Câu chuyện xã hội (social stories) ở trường có hiệu quả không? | ASD-SUP-PMC11754701 | kết quả RCT ASSSIST-2 |
| q018 | 3 | Huấn luyện kỹ năng xã hội cho thiếu niên tự kỷ có hiệu quả không? | ASD-SUP-PMC9399988, ASD-SUP-PMC10981608 | RCT + chất lượng phương pháp |
| q019 | 4 Hành vi lặp lại | Hành vi lặp lại ở trẻ tự kỷ gồm những gì? | CDC-ASD-SIGNS, NIH-NIMH-ASD-2025 | ví dụ hành vi/sở thích hạn hẹp |
| q020 | 4 | Trẻ tự kỷ kén ăn nghiêm trọng thì đánh giá và can thiệp thế nào? | ASD-NEW-003 | hướng dẫn đánh giá + can thiệp |
| q021 | 4 | Cha mẹ làm gì khi trẻ có hành vi thách thức ở nhà? | WHO-CST-PARTICIPANTS-2022, WHO-CST-INTRO-2022 | session 7 (một phần bị loại → kiểm tra coverage) |
| q022 | 4 | Làm sao phòng tránh trẻ tự kỷ đi lạc, bỏ chạy? | ASD-OA-PMC4742252, ASD-OA-PMC13427885 | tỉ lệ + yếu tố + an toàn |
| q023 | 4 | Sở thích hạn hẹp có ảnh hưởng đến việc học không? | CDC-ASD-SIGNS (?) | có thể partial |
| q024 | 5 Chẩn đoán | Tự kỷ được chẩn đoán như thế nào? | CDC-ASD-CLINICAL, ASD-CSV-002, NIH-NIMH-ASD-2025 | quy trình, ai chẩn đoán |
| q025 | 5 | M-CHAT-R/F là gì và độ chính xác ra sao? | ASD-CSV-029, ASD-CSV-091 | độ nhạy/đặc hiệu |
| q026 | 5 | Nên sàng lọc tự kỷ cho trẻ vào độ tuổi nào? | CDC-ASD-SCREENING, ASD-CSV-091 | mốc tuổi sàng lọc |
| q027 | 5 | Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì? | ASD-CSV-002, NIH-NIMH-ASD-2025 | 2 nhóm tiêu chí |
| q028 | 5 | Sàng lọc và chẩn đoán sớm tự kỷ ở Việt Nam được thực hiện thế nào? | ASD-CSV-038, ASD-OA-PMC13005892 | nghiên cứu dân số VN |
| q029 | 5 | Trẻ tự kỷ có hay bị ADHD hoặc lo âu kèm theo không? | ASD-CSV-062, ASD-CSV-088, ASD-CSV-007, ASD-CSV-078 | tỉ lệ đồng mắc |
| q030 | 5 | Trẻ tự kỷ có hay gặp vấn đề tiêu hóa không? | ASD-OA-PMC9003052, ASD-OA-PMC12620806 | tổng quan hệ thống |
| q031 | 6 Can thiệp | Can thiệp sớm mang lại lợi ích gì? | CDC-EARLY-INTERVENTION, ASD-SUP-PMC10783429, ASD-NEW-001 | bằng chứng + dịch vụ |
| q032 | 6 | Can thiệp NDBI là gì? | ASD-SUP-PMC4513196, ASD-CSV-017 | định nghĩa + hiệu quả |
| q033 | 6 | Can thiệp do cha mẹ thực hiện có hiệu quả không? | ASD-CSV-011, ASD-CSV-018, ASD-CSV-089 | meta-analysis + từ xa |
| q034 | 6 | Chương trình huấn luyện kỹ năng cho người chăm sóc của WHO gồm những gì? | WHO-CST-INTRO-2022, WHO-CST-PARTICIPANTS-2022 | cấu trúc session |
| q035 | 6 | Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì? | ASD-OA-PMC10774556 | tổng quan + hướng dẫn |
| q036 | 6 | Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào? | ASD-OA-PMC7407189, ASD-OA-PMC4271434 | biện pháp hành vi/vệ sinh giấc ngủ |
| q037 | 6 | Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không? | ASD-CSV-095 | kết quả + lưu ý (không liều) |
| q038 | 6 | Có thuốc nào điều trị tự kỷ không? | CDC-ASD-TREATMENT, NIH-NIMH-MEDICATIONS, NIH-NIMH-ASD-2025 | thuốc cho triệu chứng đi kèm, không chữa cốt lõi |
| q039 | 6 | Làm sao hỗ trợ trẻ tự kỷ hòa nhập ở trường phổ thông? | ASD-CSV-019, ASD-CSV-020, ASD-CSV-081, ASD-OA-PMC10900867 | nhiều can thiệp/quan điểm |
| q040 | 6 | Trẻ tự kỷ học bơi có lợi gì và cần lưu ý an toàn gì? | ASD-OA-PMC10018050, ASD-OA-PMC13427885 | trải nghiệm + an toàn nước |
| q041 | 7 Cảm giác | Liệu pháp điều hòa cảm giác có hiệu quả không? | NIHR-SENITA-2022, ASD-SUP-PMC6590432, ASD-SUP-PMC12658592, ASD-SUP-PMC7726187 | bằng chứng **trái chiều** → kiểm tra conflicting |
| q042 | 7 | Ayres Sensory Integration khác các can thiệp cảm giác khác thế nào? | ASD-SUP-PMC6590432, ASD-SUP-PMC7726187 | phân biệt khái niệm |
| q043 | 7 | Trẻ tự kỷ nhạy cảm với âm thanh vì sao? | ASD-OA-PMC11638897 | xử lý thính giác |
| q044 | 7 | Thử nghiệm SenITA cho kết quả gì? | NIHR-SENITA-2022 | kết quả chính + kết luận |
| q045 | 7 | Liệu pháp tích hợp cảm giác có đáng chi phí không? | NIHR-SENITA-2022 | phân tích chi phí-hiệu quả |
| q046 | 8 Phát triển | Trẻ 2 tuổi thường làm được những gì? | CDC-MILESTONES-24 | mốc 24 tháng (không nhầm 18/30) |
| q047 | 8 | Mốc phát triển của trẻ 9 tháng là gì? | CDC-MILESTONES-09 | mốc 9 tháng |
| q048 | 8 | Cha mẹ có thể làm gì để thúc đẩy phát triển trong 3 năm đầu? | ASD-NEW-002, WHO-ECD-GUIDELINE-2020 | can thiệp nuôi dạy |
| q049 | 8 | WHO khuyến nghị gì để cải thiện phát triển trẻ thơ? | WHO-ECD-GUIDELINE-2020 | khuyến nghị 1–4 |
| q050 | 8 | Trẻ 15 tháng chưa nói từ nào có đáng lo không? | CDC-MILESTONES-15, CDC-CONCERNED | mốc + hành động |
| q051 | 8 | Dấu hiệu chậm phát triển ở trẻ 4 tháng? | CDC-MILESTONES-04 | mốc 4 tháng |
| q052 | 9 Nhiều khía cạnh | Con 2 tuổi chưa nói, không chỉ tay: đó có thể là dấu hiệu gì, sàng lọc ở đâu, can thiệp ra sao? | CDC-MILESTONES-24, CDC-ASD-SCREENING, CDC-EARLY-INTERVENTION | ≥3 khía cạnh |
| q053 | 9 | Trẻ tự kỷ kèm ADHD lại hay mất ngủ thì hỗ trợ thế nào? | ASD-CSV-062, ASD-OA-PMC7407189 | 2 khía cạnh |
| q054 | 9 | Nên ưu tiên can thiệp tại nhà do cha mẹ hay tại trường? | ASD-CSV-018, ASD-CSV-019 | so sánh, có thể partial |
| q055 | 9 | Kén ăn và rối loạn tiêu hóa ở trẻ tự kỷ có liên quan không? | ASD-NEW-003, ASD-OA-PMC9003052 | 2 khía cạnh |
| q056 | 9 | Khi trẻ tự kỷ bước vào tuổi teen, cần chú ý những thay đổi tâm lý nào? | ASD-OA-PMC12593641, NIH-NIMH-TEEN-DEPRESSION, NIH-NIMH-TEEN-BRAIN | nhiều nguồn |
| q057 | 10 Thiếu/ngoài phạm vi | Vắc-xin có gây tự kỷ không? | (chưa rõ nguồn) | kỳ vọng `insufficient` hoặc `partial`, cần xác minh |
| q058 | 10 | Liều risperidone cho trẻ 5 tuổi là bao nhiêu? | — | `blocked` (kê đơn) |
| q059 | 10 | Tế bào gốc có chữa được tự kỷ không? | — | `insufficient` |
| q060 | 10 | Chế độ ăn không gluten, không casein có chữa tự kỷ không? | (có thể ASD-OA-PMC9003052) | `insufficient` hoặc `partial`, cần xác minh |
| q061 | 10 | Con tôi 3 tuổi hay xếp đồ thành hàng, có phải bị tự kỷ không? | CDC-ASD-SIGNS | `blocked` cho chẩn đoán cá nhân, kèm hướng dẫn đi khám |
| q062 | 10 | Hôm nay thời tiết thế nào? | — | `expected_route` ≠ `expert_qa` |
