# Implementation follow-up — 2026-11-14 (Phase 5)

Trạng thái chỉ dùng: COMPLETED · PARTIAL · BLOCKED · NOT_STARTED · FAILED.

| Hạng mục | Trạng thái | Bằng chứng | Blocker |
|---|---|---|---|
| License classification | **COMPLETED** | [license_classification_repair_2026-11-14_phase5.md](license_classification_repair_2026-11-14_phase5.md); `data/curation/license_corrections.jsonl` (fceb63db…); DB 35 `verified_cc_by` | Quyền xử lý: quyết định chủ dự án |
| PDF WHO extraction (số trang) | **COMPLETED** | 3 bản đồ trang tái tạo từng byte, kiểm từng trang ([pdf_extraction_repair…](pdf_extraction_repair_2026-11-14_phase5.md)) | — |
| Table extraction (bảng PDF) | **PARTIAL** | 6 bảng dựng lại chờ duyệt; 193 chunk `table_structure_unrecoverable` loại khỏi truy xuất ([pdf_extraction_diff.csv](pdf_extraction_diff.csv)) | Người duyệt / nhập tay |
| Section V2 acceptance | **COMPLETED** (`section_v2_1`, 9/9, 71 tài liệu) | [section_v2_acceptance…](section_v2_acceptance_2026-11-14_phase5.md); 52 chunk duyệt thủ công | — (giới hạn độ phủ ghi rõ) |
| Quarantine review | **COMPLETED** (hồ sơ) · gỡ cách ly **BLOCKED** | [quarantine_followup…](quarantine_followup_2026-11-14_phase5.md) | Người có thẩm quyền |
| Embedding readiness | **COMPLETED** (dry-run) · embedding thật **BLOCKED** | [embedding_readiness…](embedding_readiness_2026-11-14_phase5.md); [embedding_candidate_matrix.csv](embedding_candidate_matrix.csv) (NOT_APPROVED) | Quyền, điều khoản Cohere (trial key), duyệt nội dung |
| Regression tests | **COMPLETED** | ruff sạch; 71 unit + 7 integration đạt; v1/v2/v2_1 tái tạo y hệt DB | — |
| Database integrity | **COMPLETED** | `db_check` ok, 25/25 phân quyền; migration 001–005 | — |

## 1. Những gì đã hoàn thành thật sự
- **Giấy phép:** 35 tài liệu CC BY phân loại lại `verified_cc_by` qua lớp hiệu chỉnh có phiên bản, kiểm hash bằng chứng gốc; raw không đổi; DB cập nhật bằng role ingest (không thể chạm `*_allowed`).
- **Số trang PDF WHO:** nguyên nhân là bộ chuyển đổi cũ ghép trang không dấu; tái tạo đúng `pypdf 6.11.0` → trùng từng byte, khớp độ dài trang của bằng chứng cũ → bản đồ trang 20/80/278 trang, nhãn trang in (null khi không chắc).
- **Bảng PDF:** dò bảng trên PDF gốc với 7 kiểm tra tự động + phát hiện chữ đọc ngược; 6 bảng (WHO-ECD) chờ duyệt; còn lại không khôi phục tin cậy được → gắn cờ, không truy xuất; ràng buộc DB cấm truy xuất các trạng thái chưa kiểm chứng.
- **Phát hiện mới:** 8 trang PARTICIPANTS lỗi mã glyph (`/gid…`) từng truy xuất được → loại; bản pdfium chờ duyệt.
- **`section_v2_1`:** 3.740 chunk / 71 tài liệu trong DB; header/footer 312 → 1; danh sách tham khảo/người đóng góp truy xuất được → 0; 100% page provenance PDF; 10 lỗi phát hiện khi duyệt thủ công đã sửa và có test.
- **Cách ly:** ASD-CSV-077 có 61 ô mất `<break/>` (catalog ghi 1); đề xuất "thay bằng khoảng trắng", số liệu khớp 61/61; NIH-NIMH-CHILDREN 19/19 mục đúng trong chunk v2_1.
- **Embedding readiness:** ma trận 174 nguồn NOT_APPROVED; 71 đủ điều kiện kỹ thuật; dry-run 0 chunk qua cổng.

## 2. Những gì chưa đạt và nguyên nhân
| Việc | Nguyên nhân |
|---|---|
| Khôi phục bảng PDF (193 chunk) | Bảng SENITA không kẻ ô; GRADE xoay chữ; dựng theo vị trí chữ sẽ tạo bảng giả |
| Áp dụng bản trích xuất lại (ASD-CSV-077, 8 trang pdfium, 6 bảng) | Thay đổi corpus/nội dung y khoa → cần người duyệt |
| Gỡ cách ly, quyền xử lý, embedding | Quyết định của chủ dự án/pháp lý/chuyên gia |
| Độ phủ: văn xuôi ngay sau bảng PDF có thể bị loại cùng vùng bảng | Đổi lấy an toàn: không để số liệu bảng mất cột vào truy xuất |

## 3. Thay đổi source code và dữ liệu
**Mới:** `app/ingest/pdf_page_map.py`; `scripts/license_classification_repair.py`, `pdf_page_map.py`, `pdf_table_recovery.py`, `quarantine_reextraction.py`, `embedding_candidates.py`, `acceptance_artifacts.py`; `migrations/005_chunk_status_v2_1.sql` + `rollback/005_down.sql`; `tests/unit/test_chunking_v2_1.py` (14), `tests/integration/test_database_gates.py` (7); `data/curation/license_corrections.jsonl`; `data/extractions/` (3 bản đồ trang, 4 file bảng, 1 file pdfium, 2 hồ sơ cách ly).
**Sửa:** `app/ingest/chunking.py`, `pdf_layout.py` (quy tắc v2_1 sau cờ profile; v1/v2 không đổi hành vi), `catalog_import.py` (đọc phân loại đã hiệu chỉnh), `scripts/build_corpus.py` (áp dụng + kiểm lớp hiệu chỉnh), `chunk_pilot.py` (`--all`), `chunking_regression.py` (ngưỡng chuỗi dò ≥ 40 ký tự), `db_check.py` (kiểm 005), `config/chunking_profiles.json` (+`section_v2_1`), `config/embedding_profiles.json` (→ `section_v2_1`), `pyproject.toml` (`pypdf==6.11.0`, `pdfplumber`, ký tự `−`), test catalog import (+1), README, skill.
**Dữ liệu sinh lại:** `data/catalog/sources.jsonl` (a544159e…), `data/corpus/manifest.jsonl` (9c97552f…) — chỉ 35 dòng đổi trường quyền. File corpus `.md`: không đổi.
**Xoá:** không có (không xoá raw, dữ liệu DB nghiệp vụ hay database). Chunk `section_v2_1` được ghi đè theo cơ chế thay-toàn-bộ-theo-tài-liệu trong các lần lặp.

## 4. Các file báo cáo được tạo (không ghi đè báo cáo cũ — hậu tố `_phase5`)
`license_classification_repair_2026-11-14_phase5.md`, `pdf_extraction_repair_2026-11-14_phase5.md`, `section_v2_acceptance_2026-11-14_phase5.md`, `quarantine_followup_2026-11-14_phase5.md`, `embedding_readiness_2026-11-14_phase5.md`, file này; CSV: `embedding_candidate_matrix.csv`, `pdf_extraction_diff.csv`, `section_v2_regression.csv`, `section_v2_1_residual_numeric_runs.csv`; JSON: regression v1/v2 → v2_1, `2026-11-14_section_v2_1_manual_review_samples.json`, `2026-11-14_chunking_full_section_v2_1.{json,md}`, `2026-11-14_quarantine_chunks_section_v2_1.{json,md}`.

## 5. Kết quả kiểm tra database
| Kiểm tra | Kết quả |
|---|---|
| Migration | 001–005 applied, `nothing to apply` |
| PostgreSQL / pgvector / cột vector | 16.15 / 0.8.6 / `vector(1536)`; 31 index; không ANN |
| Phân quyền | 25/25 (gồm: ingest không bật được quyền, app không đọc được chunk/bằng chứng) |
| Ràng buộc mới | `chunks_unverified_structure_not_retrievable` — owner cũng bị chặn (đã thử) |
| Nguồn / quyền / tài liệu | 174 (33/40/88/13) / 174 / 73, hash khớp |
| Cách ly | ASD-CSV-077, NIH-NIMH-CHILDREN — không có chunk |
| Chunk | v1 599 · v2 1.131 · v2_1 3.740 — cả 3 tái tạo y hệt |
| Phê duyệt / cờ quyền / embedding | 0 / 0 / 0 |
| Cổng embedding / retrieval | 0 / 0 |
| Backup Phase 5 | `pre_license_fix_20261114_104702`, `pre005_20261114_105808`, `pre005_final_20261114_143233`, `pre_v2_1_rewrite_20261114_144203` (`backups/`, git-ignored) |
| Raw | digest 199 file `83f5f377…1d02` — không đổi so với mốc đầu phiên |

Sự cố: không. Migration 005 thử 2 lần trên container cô lập (`docker run --tmpfs`, khôi phục từ backup), không dùng `CREATE DATABASE … TEMPLATE`.

## 6. Các quyền vẫn đang bị khoá
`archive_allowed`, `text_mining_allowed`, `chunking_allowed`, `embedding_allowed`, `cohere_processing_allowed`, `external_llm_processing_allowed`, `commercial_use_allowed`, `attribution_required`, `share_alike_required` — NULL cho 174/174 nguồn; `approved_for_embedding/retrieval` false cho 73/73; `clinical_reviewed` false.

## 7. Quyết định cần chủ dự án / pháp lý / chuyên gia
1. Chính sách sử dụng toàn kho (`project_usage_policy`): có giữ "chỉ phi thương mại" cho 35 tài liệu CC BY không.
2. Quyền xử lý từng nhóm nguồn; chấp nhận hay không bằng chứng cấp chính sách cơ quan (18 trang).
3. Cohere: production key + opt-out / ZDR / chỉ nhóm không-NC / embedding local.
4. Duyệt nội dung: 6 bảng PDF chờ duyệt, 8 trang pdfium, quy tắc `<break/>` của ASD-CSV-077, gỡ cách ly 2 tài liệu.
5. Chuyên gia ASD: thẩm định nội dung trước khi bất kỳ tài liệu nào được phê duyệt.

## 8. Đề xuất bước tiếp theo
1. Chủ dự án ghi quyết định quyền (role owner) → `db_check` → `embed_chunks.py` dry-run để xác nhận đúng tập được phép.
2. Người duyệt xử lý hàng chờ: bảng PDF, pdfium, ASD-CSV-077; áp dụng = phiên bản tài liệu mới + chunk lại.
3. Đánh dấu `license_type` cho 13 tài liệu NC và 7 tài liệu có bằng chứng trong bản gốc (cùng cơ chế curation).
4. Khi có quyền: embedding trên tập được phép (~27 lời gọi tối đa), rồi Phase 5 retrieval (exact search baseline + FTS + fusion + rerank) và bộ câu hỏi chuẩn có chuyên gia duyệt.
5. `git init` + commit đầu tiên khi được yêu cầu (chưa làm — đúng yêu cầu).
