# Phase 6.2 – T2.1: Migration 007 — Research Read-only Role & Retrieval View — 2026-11-14

**Trạng thái: COMPLETED.**
- **Đã áp dụng lên DB thật** sau khi có backup, thử trên bản sao cô lập (apply → kiểm tra → rollback → re-apply) và kiểm chứng.
- Migration đang có trên DB: 001–007.

## 1. Mục tiêu và phạm vi
Tạo role chỉ đọc chuyên cho retrieval/evaluation nghiên cứu, cùng một view áp đủ C5 (quyết định C1 + C5 ở T0).

Không có trong task này:
- retriever;
- API;
- reranker;
- thay đổi quyền của production hay của role app/ingest.

## 2. File đã đọc
- `migrations/001`–`006` (đặc biệt 003 grants, 006 research track)
- `deploy/db/initdb/00_bootstrap.sh`, `deploy/compose.yml`
- `app/config.py`
- `scripts/db_migrate.py`, `scripts/db_check.py`
- Catalog DB: role, ACL database/schema, default ACL, `pg_db_role_setting`

Hai phát hiện từ catalog quyết định thiết kế:
1. `asd_rag_v2_owner` **không có CREATEROLE**, nên tạo role phải là một bước đặc quyền tách riêng.
2. Đã có sẵn: PUBLIC không có CONNECT/TEMP trên DB, schema `public` đã thu hồi khỏi PUBLIC, không có default ACL.

## 3. File tạo / sửa
| File | Mục đích |
|---|---|
| `deploy/db/initdb/10_research_reader.sh` (mới) | Bước đặc quyền, idempotent:<br>• tạo role `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 5`<br>• đặt mặc định phiên<br>• `CONNECT` trên DB, `USAGE` trên schema `public` |
| `migrations/007_research_retrieval_access.sql` (mới) | Precondition → unique index một phần → view `security_barrier` → grant → postcondition |
| `migrations/rollback/007_down.sql` (mới) | Thu hồi grant, xoá view và index |
| `deploy/db/rollback/research_reader_down.sql` (mới) | Xoá role (superuser) |
| `docs/research_retrieval_access.md` (mới) | Tài liệu role và view |
| `deploy/compose.yml` (sửa) | Thêm biến `ASD_RAG_RESEARCH_READER_PASSWORD` cho cài mới |
| `app/config.py` (sửa) | Role `research_reader` trong `connect()` |
| `.env` (sửa) | Thêm `ASD_RAG_RESEARCH_READER_PASSWORD`, giá trị ngẫu nhiên, không in ra |
| `.env.example` (sửa) | Thêm tên biến kèm giá trị mẫu |
| `scripts/db_check.py` (sửa) | 31 probe 007:<br>• chạy trong transaction READ WRITE, luôn rollback<br>• chỉ lỗi thiếu quyền mới tính là "denied"<br>• kiểm tra research đổi sang ngữ nghĩa khi tạo / khi truy xuất |
| `tests/integration/test_research_embeddings.py` (sửa 1 test) | Ngữ nghĩa provenance khi tạo |
| `tests/integration/test_research_retrieval_access.py` (mới) | 13 test chỉ đọc |
| `scripts/research_authorization_revise.py`, `scripts/verify_research_access.py` (mới) | D-1 (T2.0) và kiểm chứng (T2.2) |

Migration cũ (001–006) **không sửa**.

## 4. Thiết kế
- **LOGIN** (thay vì NOLOGIN): retriever nghiên cứu ở T2.3 kết nối trực tiếp. Nếu dùng NOLOGIN, sẽ phải để một role khác kế thừa quyền, trái với yêu cầu "không kế thừa".
- **View chạy bằng quyền owner** (mặc định của PostgreSQL, không phải `SECURITY DEFINER`), nên reader không cần quyền trên bảng gốc. `security_barrier` chặn kiểu tấn công đưa điều kiện của người gọi vào để dò dữ liệu.
- **Unique index một phần** `research_authorizations_one_active_per_profile`: "authorization hiện hành" luôn là duy nhất. Thêm một authorization hiệu lực thứ hai sẽ bị từ chối; điều này đã được kiểm thử.
- **Ánh xạ đủ 10 điều kiện C5** (bảng trong `docs/research_retrieval_access.md`). Không điều kiện nào phải bỏ qua hay làm giả.

## 5. Preflight → backup → thử nghiệm → áp dụng
| Bước | Kết quả |
|---|---|
| Preflight | `db_check` 34/34; integration 11/11; dry-run D-1 khớp 47/47 |
| Backup | `backups/asd_rag_v2_pre007_20261114_221206.dump` (SHA-256 `45119ffb…7aa4`) |
| Bản sao cô lập (`docker run --tmpfs`, port 5439, initdb mới + khôi phục backup) | `10_research_reader.sh` tự chạy trong initdb (đường cài mới); chạy lại bằng `docker exec` (đường DB đã tồn tại, idempotent) |
| Apply trên bản sao | D-1 → 007 → `db_check` **66/66** → `verify_research_access --mutations` **90/90** (lần đầu 87/90; 3 lỗi đều thuộc script kiểm chứng, xem mục 7) |
| Rollback trên bản sao | `--restore` → `007_down.sql` → xoá bản ghi `schema_migrations` → `research_reader_down.sql`. Fingerprint trở về trạng thái trước, trừ authorization 2 (giữ lại, đã thu hồi). Role trùng với DB thật trước áp dụng. `db_check` **34/34** |
| Re-apply trên bản sao | role → 007 → `--restore --revoke 1 --reactivate 2` → **90/90**, `db_check` **66/66** |
| Áp dụng DB thật | bước đặc quyền (`CREATE ROLE`) → D-1 → `db_migrate` (007 `applied`) |
| Sau áp dụng (DB thật) | `db_check` **66/66**; `verify_research_access` **74/74** (ca thay đổi dữ liệu không chạy trên DB thật); integration **24/24**; unit **101/101** |

Postcondition trong migration (chạy trong transaction migration và đã đạt):
- reader có SELECT trên view;
- reader không có quyền ghi trên view;
- reader không có quyền trên bất kỳ relation nào khác;
- reader không có CREATE trên schema, không có CREATE/TEMP trên DB;
- không có function `SECURITY DEFINER` trong `asd_rag`.

## 6. Thay đổi DB (DB thật)
| Đối tượng | Thay đổi |
|---|---|
| Role | `+ asd_rag_v2_research_reader` |
| Quyền mới (chỉ của role mới) | `CONNECT` trên DB; `USAGE` trên schema `asd_rag` và `public`; `SELECT` trên `v_research_retrieval_chunks` |
| View | `+ asd_rag.v_research_retrieval_chunks` (owner sở hữu) |
| Index | `+ research_authorizations_one_active_per_profile` |
| Dữ liệu | authorization 1 → `revoked_at` được đặt; `+` authorization 2 cùng 71 nguồn và 2.291 chunk (T2.0) |
| `schema_migrations` | `+ 007` |
| Không đổi | mọi bảng và cột; view production; view 006; quyền của app, ingest, PUBLIC; chunk; vector |

## 7. Lỗi gặp và cách xử lý (đều thuộc script kiểm tra, không phải lỗ hổng)
| Lỗi | Nguyên nhân | Xử lý |
|---|---|---|
| Probe `UPDATE`/`DELETE` qua view báo "NOT a privilege error" | View có JOIN nên không cập nhật được; PostgreSQL báo `ObjectNotInPrerequisiteState` trước bước kiểm quyền | Chuyển probe sang ghi trên bảng gốc (phải gặp lỗi thiếu quyền); kiểm "không có quyền ghi trên view" bằng catalog; thêm kiểm tra riêng "view không cập nhật được" |
| `GRANT … TO PUBLIC` của reader "allowed" | Người không có grant option chạy GRANT chỉ nhận WARNING "no privileges were granted", không có lỗi | Kiểm tra ACL ngay sau đó trong cùng transaction: **không đổi** |
| Không tìm thấy filter `is_current` trong plan | Planner dùng index một phần `documents_one_current_per_source` (điều kiện `WHERE is_current`) | Phép kiểm chấp nhận filter **hoặc** index một phần đó, sau khi đã kiểm điều kiện của index |
| Ca quarantine bị `CheckViolation` | Ràng buộc `quarantine_has_reason` | Đặt thêm `content_warning` trong ca thử |
| `has_sequence_privilege` lỗi trên `pg_toast_*` | Planner đánh giá hàm trước khi lọc `relkind` | Bọc bằng `CASE` |
| Lệnh nối bằng `&&` dừng vì ruff | — | Sửa lint rồi chạy lại toàn bộ phần kiểm chứng |

## 8. Rollback (đã kiểm chứng trên bản sao)
1. Nếu cần quay về allowlist cũ:
   ```
   python -B scripts/research_authorization_revise.py --restore --revoke 2 --reactivate 1
   ```
2. Bằng owner: chạy `migrations/rollback/007_down.sql`, rồi
   ```
   DELETE FROM asd_rag.schema_migrations WHERE version = '007'
   ```
3. Bằng superuser:
   ```
   docker exec -i asd-rag-v2-db psql -v ON_ERROR_STOP=1 -U postgres -d asd_rag_v2 < deploy/db/rollback/research_reader_down.sql
   ```
4. Kiểm tra lại:
   ```
   python -B scripts/db_check.py
   ```
   Kỳ vọng 34/34 probe ở 006.

Các bước rollback không xoá vector, chunk hay hàng authorization nào.

## 9. Kết luận
Đạt T2-AC04, AC05, AC06, AC10 (rollback đã chạy thật trên bản sao).
