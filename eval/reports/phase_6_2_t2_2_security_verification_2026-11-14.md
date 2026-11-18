# Phase 6.2 – T2.2: Security Verification — 2026-11-14

**Kết quả: PASS.**

| Nơi chạy | Kết quả |
|---|---|
| DB thật | **74/74** kiểm tra (`scripts/verify_research_access.py`): quyền 45/45, authorization 13/13, rò rỉ quyền 16/16 |
| Bản sao cô lập | **90/90**, gồm thêm 16 ca âm tính có thay đổi dữ liệu, chạy ở cả lần áp dụng đầu và lần áp dụng lại |
| `db_check` (DB thật) | **66/66** probe |
| Integration test (DB thật) | **24/24** |

Kiểm tra hành vi được thực hiện bằng cách **kết nối thật bằng role mới** (`session_user = current_user = asd_rag_v2_research_reader`), không chỉ đọc định nghĩa SQL.

Bằng chứng chi tiết:
- [phase_6_2_t2_2_security_verification_2026-11-14.json](phase_6_2_t2_2_security_verification_2026-11-14.json) (DB thật)
- [phase_6_2_t2_2_isolated_mutation_tests_2026-11-14.json](phase_6_2_t2_2_isolated_mutation_tests_2026-11-14.json) (bản sao)

## A. Quyền (45/45, kết nối bằng role mới)
Mọi lệnh ghi/DDL chạy trong transaction **READ WRITE**, luôn rollback. Cách này buộc kết quả phản ánh **quyền**, không phải mặc định read-only (role có thể tự tắt read-only, nên đó không phải cơ chế kiểm soát).

| Nhóm | Kết quả |
|---|---|
| SELECT `v_research_retrieval_chunks` (gồm `embedding`, `content`, `content_tsv`) | được phép |
| SELECT 15 bảng/view khác | **bị từ chối**:<br>• `chunks`, `research_chunk_embeddings`, các bảng authorization, `v_research_embedding_candidates`<br>• `chunk_embeddings`, `documents`, `sources`, `source_rights`, `rights_assessments`<br>• `v_retrieval_ready_chunks`, `v_embedding_eligible_documents`, `v_chunk_provenance`<br>• `retrieval_logs`, `schema_migrations` |
| INSERT / UPDATE / DELETE / TRUNCATE trên bảng gốc | bị từ chối |
| Ghi **qua** view | bị chặn hai lớp: không có quyền (catalog, nhóm C) + view có JOIN nên không cập nhật được |
| CREATE TABLE (asd_rag, public), CREATE TEMP TABLE, CREATE VIEW/FUNCTION/SCHEMA, ALTER, DROP | bị từ chối |
| `SET ROLE` sang ingest/owner/app | bị từ chối |
| `pg_read_file`, `COPY … TO PROGRAM`, `lo_import` | bị từ chối |
| `GRANT … TO PUBLIC` | PostgreSQL trả WARNING "no privileges were granted"; **ACL không đổi** (đọc lại trong cùng transaction) |
| `default_transaction_read_only` | `on` |

## B. Authorization (13/13 trên DB thật + 16/16 ca có thay đổi dữ liệu trên bản sao)
Trên DB thật:
| Kiểm tra | Kết quả |
|---|---|
| Đúng 1 authorization hiệu lực | authorization 2 |
| Các hàng view trả về = allowlist hiện hành | 2.291 = 2.291; không thừa, không thiếu; 1 hàng mỗi chunk |
| 47 chunk D-1 | **0** xuất hiện (vector vẫn còn: 47/47) |
| Profile / model / chiều | `cohere_embed_v4_1536_v1` / `embed-v4.0` / 1536 cho mọi hàng |
| Trạng thái completeness | chỉ các trạng thái đã kiểm chứng |
| Tài liệu bị quarantine hoặc không còn hiện hành | 0 |
| **Lọc trước LIMIT** | Truy vấn bằng vector của một chunk D-1 (các chunk gần nhất của nó là danh mục tham khảo khác):<br>• top-10 trên bảng gốc (đối chứng) chứa ≥ 5 chunk D-1;<br>• top-10 qua view trả **đủ 10 hàng, 0 chunk bị loại** |
| Plan | Node trên cùng là `Limit`. Mọi filter (`revoked_at IS NULL`, `content_review_status`, `retrieval_eligible`, `completeness_status`, `vector_dims`, `corpus_role`) nằm dưới node này. `is_current` được bảo đảm bằng index một phần `documents_one_current_per_source` (`WHERE is_current`) |
| Định nghĩa view | chứa đủ các điều kiện C5; `security_barrier=true` |

Trên bản sao: mỗi ca thay đổi dữ liệu chạy trong transaction của owner rồi ROLLBACK. Số hàng chuẩn là 2.291.

| Ca | Kết quả |
|---|---|
| Đối chứng dương: chunk hợp lệ | có mặt |
| Thu hồi authorization | 0 hàng |
| Bỏ chunk khỏi allowlist (loại trừ) | vắng (2.290) |
| Hash trong allowlist ≠ hash chunk | vắng |
| Tài liệu bị quarantine | vắng (cả tài liệu, 2.248) |
| Tài liệu không còn hiện hành | vắng (2.248) |
| Chunk `retrieval_eligible = false` | vắng |
| Trạng thái `text_encoding_lost` | vắng |
| Sai corpus version (`chunking_profile` của authorization) | 0 hàng |
| Vector ứng với nội dung khác (hash vector ≠ hash chunk) | vắng |
| Vector có `model_id` khác | vắng |
| Vector thuộc profile embedding khác | vắng |
| Hỏng provenance (tài liệu chuyển sang nguồn khác) | vắng |
| Nguồn không thuộc core/gaps | vắng |
| Chunk có vector nhưng không có trong allowlist | vắng |
| Thêm authorization hiệu lực thứ hai | bị từ chối (`UniqueViolation`) |

Ca "chiều vector sai" không tạo được bằng dữ liệu, vì cột `vector(1536)` và CHECK từ chối từ khi ghi; view vẫn có điều kiện `vector_dims(...)`.

## C. Rò rỉ quyền (16/16)
| Kiểm tra | Kết quả |
|---|---|
| Thuộc tính role | LOGIN, NOSUPERUSER, NOINHERIT, NOCREATEROLE, NOCREATEDB, NOREPLICATION, NOBYPASSRLS, CONNECTION LIMIT 5 |
| Membership (cả hai chiều) | không có |
| Quyền trên bảng, view, matview, foreign table (mọi schema không thuộc hệ thống) | **chỉ** SELECT trên `asd_rag.v_research_retrieval_chunks`; không có quyền ghi trên view |
| Quyền trên cột | không có |
| Quyền trên sequence | không có |
| Quyền trên schema | USAGE trên `asd_rag` và `public`; CREATE ở **không** schema nào |
| Quyền trên database | chỉ CONNECT (không CREATE, không TEMP) |
| Function `SECURITY DEFINER` (ngoài `pg_catalog`) | không có |
| Function trong asd_rag mà reader EXECUTE được | chỉ `research_embedding_guard` (EXECUTE mặc định của PUBLIC). Đây là trigger function, không gọi trực tiếp được |
| Default privileges | không có |
| Phụ thuộc của view | chỉ `chunks`, `documents`, `sources`, `embedding_profiles`, 3 bảng authorization, `research_chunk_embeddings`. Không phụ thuộc đối tượng production hay đối tượng về quyền |
| View production tham chiếu đối tượng research | không |
| app / ingest đọc được view mới | không / không |
| Danh sách ACL của reader | `CONNECT asd_rag_v2`, `USAGE asd_rag`, `USAGE public`, `SELECT v_research_retrieval_chunks`. Không có gì khác |

## D. Toàn vẹn (fingerprint DB thật trước 007 / sau T2)
| Thành phần | Kết quả |
|---|---|
| Số chunk (5.470), nội dung chunk (`e40dc061…`) | **không đổi** |
| Research vectors (2.338) và md5 vector (`1b1c15ce…`) | **không đổi** |
| Production vectors (0), phê duyệt + cờ quyền production (0) | **không đổi** |
| Cột của mọi bảng/view (trừ view mới) | **không đổi** |
| View production (`v_retrieval_ready_chunks`, `v_embedding_eligible_documents`, `v_chunk_provenance`) | **không đổi** |
| View 006 `v_research_embedding_candidates` | **không đổi** |
| ACL của **app**, **ingest**, PUBLIC (relations) | **không đổi** |
| ACL của owner | đổi **chỉ** do 7 quyền mặc định của chủ sở hữu trên view mới. Bỏ view mới ra thì hash = trước (đã kiểm) |
| Role | `+ asd_rag_v2_research_reader` (đã duyệt) |
| Authorization | 1 → thu hồi (hàng giữ nguyên); `+ 2` (D-1, đã duyệt) |
| Migration | `+ 007` (đã duyệt) |
| Raw | 199/199 file khớp baseline |
| Dataset đánh giá | không đổi (SHA `7704bb51…`); validator PASS |
| API call | không có (không chạy module nào gọi Cohere; `ingestion_runs` không tăng) |

Mọi thay đổi đều nằm trong phạm vi đã duyệt. **Không có thay đổi ngoài phạm vi.**

## E. Lệnh đã chạy (không có secret)
- `python -B scripts/verify_research_access.py --out eval/reports/phase_6_2_t2_2_security_verification_2026-11-14.json` (DB thật)
- `ASD_RAG_DB_PORT=5439 python -B scripts/verify_research_access.py --mutations --out …` (bản sao; script từ chối chạy trên port 5433)
- `python -B scripts/db_check.py` (DB thật và bản sao)
- `python -m pytest` (101) và `python -m pytest -m integration` (24)
- `python -B scripts/validate_retrieval_eval.py`
- `ruff check .`
- `sha256sum -c` cho raw

## F. Rủi ro còn tồn tại
1. **`scripts/embed_research.py` chưa cập nhật theo việc sửa đổi authorization** (xem T2.0 §9). `run` dừng an toàn; `verify` sẽ báo sai. Không ảnh hưởng truy cập hay authorization, nhưng cần sửa trước lần embedding tiếp theo.
2. **Mật khẩu reader** nằm trong `.env`, cùng chỗ với các role khác. Giới hạn 5 kết nối; chỉ bind `127.0.0.1`.
3. **Reader đọc được catalog hệ thống** (tên bảng, định nghĩa view): đây là mặc định của PostgreSQL, chỉ lộ metadata, không lộ dữ liệu.
4. **`research_embedding_guard` vẫn có EXECUTE mặc định cho PUBLIC.** Rủi ro thấp vì là trigger function. Có thể `REVOKE … FROM PUBLIC` ở một migration sau, nhưng việc đó đổi quyền của app/ingest nên cần duyệt riêng.
5. **Ca thay đổi dữ liệu chỉ chạy trên bản sao**, có chủ đích. DB thật được kiểm bằng các phép chỉ đọc và probe luôn rollback.

## G. Tiêu chí nghiệm thu T2
| ID | Kết quả | Bằng chứng |
|---|---|---|
| T2-AC01 | ✔ | 47 chunk xác định theo heading và nội dung, đọc kiểm (T2.0) |
| T2-AC02 | ✔ | Authorization 2 + manifest + allowlist SHA-256; authorization 1 giữ nguyên |
| T2-AC03 | ✔ | md5 chunk và md5 vector không đổi; 2.338 vector; không gọi API |
| T2-AC04 | ✔ | 007 `applied` trên DB thật sau khi đã thử trên bản sao |
| T2-AC05 | ✔ | Thuộc tính role và ACL đúng thiết kế (C) |
| T2-AC06 | ✔ | Đủ C5 trong view; lọc trước LIMIT; 16/16 ca âm tính |
| T2-AC07 | ✔ | Mọi lệnh ghi/DDL/SET ROLE bị từ chối (A) |
| T2-AC08 | ✔ | View trả đúng allowlist; không đọc được relation nào khác |
| T2-AC09 | ✔ | View production, quyền app, vector production, phê duyệt: không đổi |
| T2-AC10 | ✔ | Rollback và re-apply đã chạy thật trên bản sao |
| T2-AC11 | ✔ | Unit 101, integration 24, `db_check` 66/66, ruff sạch |
| T2-AC12 | ✔ | Fingerprint: chỉ có thay đổi đã duyệt (D) |

## Kết luận
**READY FOR T2.3.** D-1, migration 007 và security verification đều đạt.

Việc nên làm, không chặn retriever:
- cập nhật `embed_research.py` theo ngữ nghĩa khi tạo / khi truy xuất;
- sửa bộ phát hiện References trong một profile chunk mới;
- dataset vẫn là silver (điều kiện của T1: human verification + mở rộng pool ở T5).
