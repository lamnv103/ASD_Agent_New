# Research retrieval access — role & view (migration 007)

Chỉ dùng cho **luồng nghiên cứu**. Không phải production; role `app` không thấy gì ở đây.

## Role `asd_rag_v2_research_reader`
| Thuộc tính | Giá trị | Lý do |
|---|---|---|
| LOGIN | có, `CONNECTION LIMIT 5` | Retriever nghiên cứu (T2.3+) kết nối trực tiếp; giới hạn số phiên |
| SUPERUSER / CREATEDB / CREATEROLE / REPLICATION / BYPASSRLS | không | least privilege |
| INHERIT | **NOINHERIT**, không có membership | không thể kế thừa quyền của role nào |
| Mặc định phiên (trong DB) | `search_path = asd_rag, public`; `default_transaction_read_only = on`; `statement_timeout = 60s` | phòng thủ nhiều lớp; read-only **không** phải cơ chế kiểm soát (role tự tắt được), quyền mới là cơ chế kiểm soát |
| Quyền | `CONNECT` trên database `asd_rag_v2`; `USAGE` trên schema `asd_rag` và `public` (cần cho kiểu `vector` và toán tử `<=>`); `SELECT` trên `asd_rag.v_research_retrieval_chunks` | Ngoài 4 quyền này không có gì khác: không TEMP, không CREATE, không đọc bảng nào |
| Mật khẩu | biến môi trường `ASD_RAG_RESEARCH_READER_PASSWORD` (`.env`, không commit) | không ghi trong code hay báo cáo |
| Kết nối trong code | `app.db.connect("research_reader", …)` | |

Tạo role (cần superuser, vì `asd_rag_v2_owner` không có CREATEROLE):
- Volume mới: `deploy/db/initdb/10_research_reader.sh` tự chạy sau `00_bootstrap.sh`.
- DB đã tồn tại:
  ```
  docker exec -i -e ASD_RAG_DB_NAME -e ASD_RAG_RESEARCH_READER_PASSWORD asd-rag-v2-db bash -s < deploy/db/initdb/10_research_reader.sh
  ```
  Script idempotent; mỗi lần chạy đều đặt lại toàn bộ thuộc tính.

## View `asd_rag.v_research_retrieval_chunks`
- `security_barrier = true`: điều kiện do người gọi viết không được đánh giá trên các hàng đã bị lọc, nên không thể dò dữ liệu qua lỗi. View chạy bằng quyền của owner (mặc định của PostgreSQL), nên reader **không** cần quyền trên bảng gốc. Không có function `SECURITY DEFINER`.
- Mỗi hàng là một chunk được phép truy xuất, gồm vector + nội dung + provenance:
  - định danh và vector: `research_embedding_id`, `authorization_id`, `profile_code`, `model_id`, `vector_dimension`, `embedding`, `vector_norm`, `embedding_input_hash`, `embedding_run_id`;
  - chunk và nguồn: `chunk_id`, `chunk_index`, `document_id`, `source_id`, `document_version`, `title`, `source_url`, `publisher`, `source_type`, `corpus_role`, `group_membership`;
  - vị trí trong tài liệu: `chunking_profile`, `section_path`, `section_heading`, `section_type`, `content_kind`, `page_start`, `page_end`, `char_start`, `char_end`;
  - nội dung và trạng thái: `content`, `content_tsv`, `content_sha256`, `token_count`, `completeness_status`, `missing_context`.
- Các điều kiện C5, nằm **trong** view, tức trước mọi `ORDER BY … LIMIT` của người gọi:

| C5 | Điều kiện |
|---|---|
| 1 | `research_embedding_authorizations.revoked_at IS NULL`, `scope = 'research_test'`, `NOT production_approval` |
| 2 | chunk nằm trong `research_embedding_authorization_chunks` của authorization đó |
| 3 | `research_chunk_embeddings.profile_id` = profile của authorization |
| 4 | `model_id` của vector = `embedding_profiles.model_id` |
| 5 | `vector_dimension` = profile, và `vector_dims(embedding)` = profile (1536) |
| 6 | `documents.is_current` |
| 7 | `chunks.chunking_profile` = authorization; `content_sha256` của chunk = allowlist = vector |
| 8 | `documents.content_review_status <> 'quarantined'` |
| 9 | chunk có trong allowlist (danh sách loại trừ = phần không có trong allowlist); `retrieval_eligible`; `completeness_status` thuộc nhóm đã kiểm chứng |
| 10 | chunk → document → source khớp nhau, và khớp `authorization_sources`; `corpus_role` ∈ core/gaps |

- Mỗi profile có **tối đa 1 authorization còn hiệu lực**, bảo đảm bằng unique index một phần `research_authorizations_one_active_per_profile`.

## Sửa đổi authorization
Dùng `scripts/research_authorization_revise.py`:
- Một lần sửa đổi = thu hồi authorization cũ (giữ nguyên hàng, đặt `revoked_at`) + tạo authorization mới với allowlist mới, **trong cùng một transaction**.
- Hoàn tác: `--restore --revoke <mới> --reactivate <cũ>`.
- Không có thao tác nào động đến vector, chunk hay embedding.

## Kiểm tra
- `scripts/db_check.py`: probe phân quyền cho reader, app và ingest.
- `scripts/verify_research_access.py`:
  - phần chạy được trên DB thật: quyền, authorization, rò rỉ quyền, fingerprint;
  - `--mutations`: các ca âm tính có thay đổi dữ liệu, chỉ chạy trên DB cô lập.
- `tests/integration/test_research_retrieval_access.py`.

## Rollback
1. Nếu cần quay về allowlist cũ:
   ```
   python -B scripts/research_authorization_revise.py --restore --revoke 2 --reactivate 1
   ```
2. Chạy `migrations/rollback/007_down.sql` bằng owner, rồi xóa bản ghi migration:
   ```
   DELETE FROM asd_rag.schema_migrations WHERE version = '007'
   ```
3. Chạy `deploy/db/rollback/research_reader_down.sql` bằng superuser để xóa role.
