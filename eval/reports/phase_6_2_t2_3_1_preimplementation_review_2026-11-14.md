# Phase 6.2 – T2.3.1: Pre-implementation Review (Dense Retrieval) — 2026-11-14

Mọi thông tin dưới đây được **kiểm trực tiếp** bằng truy vấn chỉ đọc (role `research_reader` và `owner` read-only) và bằng cách đọc config/code. Không gọi API.

## 1. File đã đọc
- Các báo cáo 6.2:
  - `phase_6_2_t0_technical_decisions_2026-11-14.md`
  - `phase_6_2_t1_evaluation_dataset_report_2026-11-14.md`
  - `phase_6_2_t1_unresolved_annotations_2026-11-14.md`
  - `phase_6_2_t2_0_authorization_revision_report_2026-11-14.md`
  - `phase_6_2_t2_1_migration_007_report_2026-11-14.md`
  - `phase_6_2_t2_2_security_verification_2026-11-14.md`
- Tài liệu và migration:
  - `docs/research_retrieval_access.md`
  - `migrations/006_research_embedding_track.sql`, `migrations/007_research_retrieval_access.sql`, `migrations/rollback/007_down.sql`
- Code và config:
  - `config/embedding_profiles.json`
  - `app/retrieval/embeddings.py` (client Cohere duy nhất)
  - `scripts/embed_research.py`, `app/ingest/embed_pipeline.py`
  - `app/config.py`, `app/db.py`
- Embedding và dataset:
  - `eval/reports/embedding_manifest.csv`, `embedding_run_report.md`, `embedding_quality_check.md`
  - `eval/datasets/retrieval_eval_v1.jsonl`, `_schema.json`, `_annotation_guidelines.md`
- Khác: `README.md`, `.claude/skills/asd-agent-dev/SKILL.md`, `.gitignore`
- Catalog DB: cột của view, chỉ mục, ràng buộc, quyền trên `retrieval_logs`

Cấu trúc code thực tế:
- `app/retrieval/` chỉ có `embeddings.py`.
- Chưa có module retriever, schema kết quả hay cấu hình retrieval.
- `config/` chỉ có `chunking_profiles.json` và `embedding_profiles.json`.

## 2. Thông số đã xác minh
| Mục | Giá trị | Nguồn |
|---|---|---|
| Embedding profile | `cohere_embed_v4_1536_v1` (`profile_id` 1) | `embedding_profiles` (DB) = `config/embedding_profiles.json` |
| Model | Cohere `embed-v4.0`, API v2 `/v2/embed`, `embedding_types=["float"]`, `truncate=NONE` | config + DB |
| Dimension | **1536** (`output_dimension=1536` khi gọi API) | config; cột `vector(1536)`; CHECK `vector_dimension = 1536` và `vector_dims(embedding) = vector_dimension` |
| Input type | tài liệu `search_document` (CHECK trong DB); **câu hỏi `search_query`** | config, `query_input_type` trong DB |
| Chuẩn hoá vector tài liệu | L2 norm 0,9999999–1,0000001 (2.291 hàng trong view) | view |
| Similarity metric | **cosine** | `embedding_profiles.similarity_metric` |
| Toán tử pgvector | `<=>` = cosine distance, khoảng [0, 2], càng nhỏ càng gần. Cosine similarity = 1 − distance, khoảng [−1, 1] | pgvector 0.8.6 |
| Chỉ mục vector | **không có ANN** (chỉ btree) → exact search, recall 100% | `pg_indexes` |
| View truy xuất | `asd_rag.v_research_retrieval_chunks` (`security_barrier`), **2.291 hàng** | view |
| Authorization hiện hành | **2** (manifest `59c3d6cf…`), `chunking_profile = section_v2_1` | view + owner read-only |
| Corpus version | `chunking_profile = section_v2_1` + `document_version` của từng tài liệu | view |
| Role kết nối | `asd_rag_v2_research_reader`: `session_user = current_user`, `default_transaction_read_only = on`, `statement_timeout = 1min` | kết nối thật |

Cột của view dùng cho dense retrieval:
- định danh và vector: `chunk_id`, `document_id`, `source_id`, `embedding`, `vector_norm`;
- phiên bản: `authorization_id`, `profile_code`, `model_id`, `vector_dimension`, `chunking_profile`, `document_version`;
- nguồn: `title`, `source_url`;
- vị trí: `section_path`, `section_heading`, `section_type`, `page_start`, `page_end`, `char_start`, `char_end`;
- nội dung: `content`, `content_sha256`, `completeness_status`.

## 3. Ràng buộc
- Chỉ đọc qua view bằng role reader. Không JOIN bảng gốc. Không fallback sang owner hay ingest.
- C5 đã nằm trong view. Truy vấn của retriever chỉ thêm `WHERE profile_code = %s`, rồi `ORDER BY embedding <=> %s::vector LIMIT %s`.
- **Logging vào DB:** `retrieval_logs` và `retrieval_results` chỉ cho role `app` INSERT, reader không có quyền. Sẽ **không** mở thêm quyền; dùng log JSONL có cấu trúc trong `logs/retrieval/` (đã git-ignore). Đề xuất luồng log riêng ở mục 6.
- **Query embedding phải gọi API ngoài.** `embed-v4.0` chỉ chạy được qua Cohere API, không có bản chạy cục bộ. Model khác sẽ khác không gian vector, nên không được thay.

## 4. Query embedding: cần phê duyệt (điểm dừng)
| Mục | Nội dung |
|---|---|
| API | Cohere `POST https://api.cohere.com/v2/embed`, `model=embed-v4.0`, `input_type=search_query`, `output_dimension=1536`, `embedding_types=["float"]`, `truncate=NONE` |
| Key | `COHERE_API_KEY` trong `.env` (key **trial**) |
| Dữ liệu gửi đi | **chỉ câu hỏi**, không gửi chunk hay nội dung tài liệu. Với baseline: 66 câu `question_vi` của dataset v1 (câu thử nghiệm do người gán nhãn viết, không có thông tin cá nhân). Không gửi `reference_query_en` (T2.3.1 không có query expansion) |
| Khối lượng | 66 input → **1 lời gọi** (batch tối đa 96), khoảng 1,5–2 nghìn token |
| Giới hạn | trial: 1.000 lời gọi/tháng (đã dùng ~81), trần token/phút (dư nhiều cho 1 lời gọi) |
| Điều khoản | key trial: input có thể được Cohere dùng theo Terms of Use (`docs/provider_terms/cohere_2026-11-14.md`). Ở đây chỉ gửi câu hỏi tổng hợp, không gửi tài liệu |
| Tái lập | vector câu hỏi được **cache cục bộ** (`data/index/query_embeddings/`, git-ignore) theo khóa `profile + sha256(câu hỏi)`, nên các lần chạy lại không gọi API |
| Phương án thay thế không cần API | chỉ kiểm thử phần DB bằng **vector fixture** (vector tài liệu đọc qua view). Cách này kiểm được SQL, lọc và provenance, nhưng **không** đo được chất lượng truy xuất với câu hỏi thật |

Không gọi API cho đến khi chủ dự án phê duyệt. Code adapter được viết và kiểm thử bằng transport giả (mock).

## 5. Kiến trúc Dense Retriever đề xuất (đặt trong `app/retrieval/`)
```
DenseRetriever.retrieve(query, k, question_id?)
  1. validate: không rỗng sau khi bỏ khoảng trắng, ≤ max_query_chars, 1 ≤ k ≤ k_max
  2. QueryEmbedder (adapter)
       CohereQueryEmbedder  → CohereEmbedder.embed([q], "search_query")
       CachedQueryEmbedder  → file cache theo (profile, sha256(q)); chế độ offline: cache-only
     → kiểm tra: đúng 1536 chiều, giá trị hữu hạn, profile/model khớp cấu hình
  3. ResearchVectorReader (connection factory: role "research_reader")
       khẳng định current_user = asd_rag_v2_research_reader (fail closed)
       SQL tham số hoá, chỉ dùng view và cột trong whitelist:
         SELECT … , embedding <=> %(q)s::vector AS cosine_distance
         FROM asd_rag.v_research_retrieval_chunks
         WHERE profile_code = %(profile)s
         ORDER BY embedding <=> %(q)s::vector LIMIT %(k)s
  4. kiểm tra provenance từng hàng:
       id không rỗng; page hoặc char range; sha256(content) = content_sha256;
       model/dimension/profile khớp; cùng một authorization_id
  5. RetrievalResponse
       rank, chunk_id, source_id, document_id, content, section, page,
       score_type = "cosine_distance", score, cosine_similarity, authorization_version,
       embedding_profile, corpus_version
     + log JSONL (không ghi câu hỏi gốc, chỉ hash; không ghi secret)
```
- Toán tử và tên view chọn qua whitelist: metric `cosine` → `<=>`. Không nối chuỗi từ input.
- Mọi lỗi (DB, quyền, view không tồn tại, lệch chiều/profile, provenance) đều ném `RetrievalError(category)`. Không có fallback.
- Cấu hình: `config/retrieval_profiles.json` → `dense_baseline_v1`: profile, view, metric, `k_default 10`, `k_max 50`, `k_probe [5, 10, 20]`, `max_query_chars 1000`.
- Các module độc lập (schema kết quả, reader, embedder, service) để sau này cắm FTS, hybrid, reranker và evidence gate mà không phải sửa.

## 6. Logging: đề xuất, chưa triển khai trên DB
Đề xuất cho sau này: một view hoặc bảng log nghiên cứu riêng, kèm một role ghi riêng chỉ có INSERT. Cần migration và phê duyệt riêng; **không** cấp INSERT trên `retrieval_logs` cho reader. Hiện tại dùng JSONL cục bộ (giới hạn: không tập trung, không bất biến).

## 7. Điểm chưa rõ
- Cohere có chuẩn hoá vector câu hỏi giống vector tài liệu không? Sẽ đo L2 norm của vector câu hỏi khi có. Với metric cosine, chuẩn hoá không ảnh hưởng thứ hạng.
- Dữ liệu câu hỏi có được phép gửi Cohere trial không: chờ phê duyệt (mục 4).
