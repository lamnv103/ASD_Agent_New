# Implementation follow-up — 2026-11-14 (Phase 3 completion & Phase 4 readiness)

Trạng thái: **COMPLETED** = đã chạy và xác minh · **PARTIAL** · **BLOCKED** · **NOT STARTED**.

## A. Executive summary

| Hạng mục | Trạng thái | Tóm tắt |
|---|---|---|
| Phase A – License & rights audit | **COMPLETED** (bằng chứng) · quyết định **BLOCKED** | 73/73 tài liệu có giấy phép đọc từ bản gốc; nhãn 48 tài liệu được đối chiếu: 13 NC thật, 35 CC BY. Không cờ quyền nào được bật. |
| Cohere terms | **COMPLETED** (tra cứu) · gửi nội dung **BLOCKED** | Key hiện tại là **trial**; dữ liệu trial chịu Terms of Use cho phép Cohere dùng input để cải thiện dịch vụ ⇒ 13 tài liệu NC bị chặn với trial key. |
| Phase B – Chunking `section_v2` | **PARTIAL** | 7/9 tiêu chí đạt; header/footer trong chunk truy xuất được 386 → 1; danh sách tham khảo/người đóng góp truy xuất được → 0. Chưa đạt: bảng PDF dẹt, 3 PDF WHO không có số trang (cần trích xuất lại). |
| Phase C – Quarantine review | **COMPLETED** (điều tra) · gỡ cách ly **BLOCKED** (cần người duyệt) | Cả hai là lỗi chuyển đổi, không phải lỗi nội dung. NIMH được v2 xử lý; ASD-CSV-077 cần trích xuất lại ô bảng từ XML. |
| Phase D – Testing & acceptance | **COMPLETED** | 56/56 unit test; regression v1↔v2 trên 71 tài liệu; duyệt thủ công 15 chunk PDF. |
| Phase E – Embedding readiness | **COMPLETED** (chuẩn bị, dry-run) · chạy thật **BLOCKED** | Client + pipeline + dry-run sẵn sàng; 0 tài liệu qua cổng; không gửi nội dung nào. |
| Migration 004 | **COMPLETED** | Backup → thử trên container cô lập (apply / rollback / re-apply) → áp dụng; 25/25 kiểm tra phân quyền. |

**Sự cố trong phiên:** lệnh `CREATE DATABASE … TEMPLATE asd_rag_v2` (tạo DB nháp để thử migration) làm một backend PostgreSQL thoát bất thường (exit code 2); server tự phục hồi từ WAL. Đã xác minh DB thật nguyên vẹn (hash 599 chunk v1 không đổi, `db_check` đạt, 004 chưa áp dụng lúc đó). Đổi sang thử nghiệm trên container tạm cô lập khôi phục từ backup — cách này cũng chứng minh backup khôi phục được.

## B. Rights audit

Chi tiết: [license_audit_2026-11-14.md](license_audit_2026-11-14.md) · ma trận: [license_review_matrix.csv](license_review_matrix.csv)

| Nhóm | Số | Bằng chứng |
|---|---:|---|
| Tổng tài liệu | 73 | 55 có câu giấy phép trong bản gốc (JATS `<license>`, câu public domain NIH, trang giấy phép PDF); 18 chỉ có chính sách cơ quan (17 CDC + 1 NIDCD) |
| Nhãn `verified_noncommercial_research` | 48 | = 10 CC BY-NC + 3 CC BY-NC-SA 3.0 IGO (**13 NC thật**) + **35 CC BY** (34 × 4.0, 1 × 3.0) |
| Còn lại | 25 | 24 Public Domain (cơ quan Mỹ) + 1 CC BY 4.0 (NIHR SENITA) |
| Xung đột catalog ↔ bản gốc | 0 | — |

Nhãn không bị đổi tự động: chính sách "phi thương mại cho toàn kho" có thể là chủ đích dự án → quyết định của chủ dự án.

Quyền theo hành động (chỉ theo giấy phép, KHÔNG phải quyết định): CC BY → `yes_by_license`; CC BY-NC(-SA) → `nc_only_by_license`, ShareAlike áp dụng khi chia sẻ bản chuyển thể; Public Domain có câu trong trang → `yes_by_license`, chỉ có chính sách cơ quan → `conditional`.

| Quyền xử lý bên thứ ba | Kết quả |
|---|---|
| `cohere_processing_allowed` | **blocked** 13 (NC + trial key) · **pending_decision** 60 |
| `external_llm_processing_allowed` | **pending_decision** 73 (chưa chọn nhà cung cấp LLM → chưa có điều khoản để đối chiếu) |
| Cờ trong DB (`*_allowed`, `verified_by/at`) | tất cả NULL — chưa có người phê duyệt |

Nguồn chưa xác minh đầy đủ: 18 trang `agency_policy_only` (CDC-ASD-*, CDC-CONCERNED, CDC-EARLY-INTERVENTION, CDC-MILESTONES-* , NIH-NIDCD-ASD-COMMUNICATION-2020) — chưa kiểm tra nội dung bên thứ ba từng trang.

## C. Chunking v2

Chi tiết: [2026-11-14_chunking_section_v2.md](2026-11-14_chunking_section_v2.md)

- Toàn kho (71 tài liệu, chạy trong bộ nhớ): 3.862 chunk, 2.592 truy xuất được, token median 360 (max 704 — 1 hàng bảng không cắt được).
- Lưu DB: pilot 10 tài liệu = 1.131 chunk `section_v2`, hai lần chạy cùng hash; 599 chunk `section_v1` giữ nguyên.
- Header/footer trong chunk truy xuất được: 386 → 1 · References/contributors truy xuất được: 14 → 0 · bảng có header: 0 → 286 · `table_structure_lost`: 178 (loại khỏi truy xuất).
- Duyệt thủ công: 15 chunk PDF có lý do chọn và nhận xét; 10 lỗi phát hiện trong vòng duyệt đã sửa và có test.
- Chưa đạt: bảng PDF dẹt; 3 PDF WHO không có số trang; chunk nhỏ tăng ở sách bài tập WHO.

## D. Quarantine review

Chi tiết: [quarantine_review_2026-11-14.md](quarantine_review_2026-11-14.md) · chunk để duyệt: [2026-11-14_quarantine_chunks_section_v2.md](2026-11-14_quarantine_chunks_section_v2.md)

| source_id | Bản chất | Số liệu | Sau v2 | Còn cần |
|---|---|---|---|---|
| ASD-CSV-077 | `<break/>` trong ô bảng FYI bị bỏ khi chuyển XML → corpus | đủ 6 cut-off + 3 trích dẫn | v2 giữ "(Reznick et al., 2007)" mà v1 làm mất; dấu ngắt giữa các cut-off vẫn thiếu | trích xuất lại ô từ XML; người duyệt gỡ cách ly |
| NIH-NIMH-CHILDREN | mục `<li>` trong bảng 2 cột bị nối liền khi bỏ thẻ | không có số; 19/19 mục khớp bản gốc | v2 tách mục bằng `; ` | người duyệt đối chiếu chunk bảng; nội dung có mục tự hại/ý nghĩ tự sát → nhánh safety |

Cả hai vẫn `quarantined`; không có thay đổi trong `data/raw`.

## E. Database integrity

| Kiểm tra | Kết quả |
|---|---|
| Migration | 001, 002, 003, **004** applied (`db_migrate.py --status`: nothing to apply) |
| PostgreSQL / pgvector | 16.15 / 0.8.6; cột `vector(1536)`; không có index HNSW/IVF |
| Bảng / view / index | 12 bảng nghiệp vụ (+ `schema_migrations`), 3 view (`v_embedding_eligible_documents`, `v_retrieval_ready_chunks`, `v_chunk_provenance`), 31 index |
| Phân quyền | 25/25 phép thử đúng (thêm 9 cho 004: ingest không bật được `archive/chunking/share_alike`, app không đọc được bằng chứng quyền/provenance) |
| Dữ liệu | 174 nguồn (33/40/88/13), 174 hồ sơ quyền, 73 tài liệu khớp hash, 2 cách ly, 0 phê duyệt, 0 quyền xử lý được đặt |
| Chunk | `section_v1` 599 (hash `4c41854…` không đổi), `section_v2` 1.131 |
| Cổng embedding | 0 tài liệu, 0 chunk; cổng 004 đòi thêm `archive_allowed` và `chunking_allowed` |
| Cách ly | không thể vào truy xuất: view yêu cầu `content_review_status='approved'` và `content_warning IS NULL`, ràng buộc `approval_requires_review` chặn ở mức bảng |
| Backup | `backups/asd_rag_v2_pre004_20261114_094807.dump`, `backups/asd_rag_v2_pre004_apply_20261114_095104.dump` (đã khôi phục thử thành công) |
| Rollback 004 | `migrations/rollback/004_down.sql` — đã chạy thử trên container cô lập |

## F. Embedding readiness

| Kiểm tra | Kết quả |
|---|---|
| Model | `embed-v4.0` (từ cấu hình dự án cũ; model tồn tại theo `GET /v1/models/embed-v4.0`) |
| Dimension | 1536 — có trong danh sách `output_dimension` {256, 512, 1024, 1536} của embed-v4; khớp cột `vector(1536)` |
| Input type | `search_document` (tài liệu) / `search_query` (câu hỏi) |
| Truncate | `NONE` (vượt giới hạn → lỗi, không cắt ngầm); chunk ≤ 704 token |
| API status | key hợp lệ; **trial** (100 lời gọi/endpoint theo header, 1.000/tháng) |
| Client | `app/retrieval/embeddings.py`: lô 96, retry giới hạn + exponential backoff cho 429/5xx/timeout, không retry 401/403, kiểm tra số chiều/giá trị hữu hạn, không lộ key; 8 test với transport giả |
| Pipeline | `app/ingest/embed_pipeline.py` + `scripts/embed_chunks.py`: chỉ đọc qua cổng DB, checkpoint mỗi lô, bỏ qua vector đã có cùng `embedding_input_hash`; ghi `ingestion_runs` |
| Dry-run (đã chạy) | 0 chunk đủ điều kiện; 73 tài liệu bị chặn (lý do: `approved_for_embedding=false` 73, 5 quyền NULL 73, review pending 71, quarantined 2) |
| Ước tính nếu duyệt (what-if, v2) | CC BY 35 tài liệu / 1.661 chunk / 18 lời gọi · Public Domain 23 / 275 / 3 · NC (đang blocked) 13 / 668 / 8 · tổng 29 lời gọi |
| Tài liệu thực sự đủ điều kiện | **0** |

Không gửi nội dung tài liệu nào lên Cohere hay LLM trong phiên này. Lời gọi API duy nhất: `GET /v1/models/embed-v4.0` và `POST /v1/check-api-key` (không có nội dung).

## G. Changed files

**Mới**
- Code: `app/ingest/pdf_layout.py`, `app/ingest/embed_pipeline.py`, `app/retrieval/__init__.py`, `app/retrieval/embeddings.py`, `app/rights/__init__.py`, `app/rights/license_audit.py`
- Script: `scripts/license_audit.py`, `scripts/chunking_regression.py`, `scripts/embed_chunks.py`
- Cấu hình: `config/embedding_profiles.json`
- Migration: `migrations/004_rights_evidence_and_chunk_v2.sql`, `migrations/rollback/004_down.sql`
- Test: `tests/unit/test_chunking_v2.py` (18), `tests/unit/test_embeddings.py` (8), `tests/unit/test_license_audit.py` (5)
- Bằng chứng/báo cáo: `docs/provider_terms/cohere_2026-11-14.md`, `eval/reports/license_audit_2026-11-14.md`, `eval/reports/license_review_matrix.csv`, `eval/reports/quarantine_review_2026-11-14.md`, `eval/reports/2026-11-14_chunking_section_v2.md`, `eval/reports/2026-11-14_chunking_pilot_section_v2.{json,md}`, `eval/reports/2026-11-14_chunking_regression_section_v1_vs_section_v2.json`, `eval/reports/2026-11-14_quarantine_chunks_section_v2.{json,md}`, file này
- Backup (git-ignored): `backups/*.dump`

**Sửa**
- `app/ingest/chunking.py` (tính năng v2 sau cờ profile; v1 tái tạo y hệt), `app/ingest/markdown_blocks.py` (bộ chuẩn hoá có phiên bản), `config/chunking_profiles.json` (+`section_v2`), `scripts/chunk_pilot.py` (pilot v2, mẫu duyệt, `--review-quarantined`), `scripts/db_check.py` (+kiểm tra 004), `pyproject.toml` (`allowed-confusables`), `.gitignore` (+`backups/`), `README.md`, `.claude/skills/asd-agent-dev/SKILL.md`

**Xoá**: `.gitkeep` thừa trong `config/`, `migrations/`, `eval/reports/`, `deploy/`, `app/retrieval/`. Không xoá dữ liệu hay database.

## H. Git status

Thư mục **không phải git repository** (`fatal: not a git repository`): không có branch, commit, diff hay danh sách untracked. Không commit/push. Đề xuất: `git init` + commit đầu tiên khi chủ dự án đồng ý (`.gitignore` đã loại `.env`, `.venv/`, `data/index/*`, `logs/*`, `backups/`).

## I. Next actions (theo thứ tự)

1. **Chủ dự án quyết định quyền** (chặn Phase 4): (a) giữ hay bỏ chính sách phi thương mại cho 35 tài liệu CC BY; (b) phương án Cohere — production key + opt-out huấn luyện / ZDR / chỉ embed 58 tài liệu không-NC / embedding local cho NC; (c) chấp nhận mức bằng chứng `agency_policy_only` cho 18 trang CDC/NIDCD; (d) ghi quyết định bằng role owner vào `source_rights` (`*_allowed`, `verified_by`, `verified_at`) và nạp bằng chứng vào `rights_assessments`.
2. **Duyệt báo cáo chunking v2** và quyết định: chạy v2 cho toàn bộ 71 tài liệu; trích xuất lại 3 PDF WHO (dấu trang + bảng GRADE) và ô bảng FYI của ASD-CSV-077 từ bản gốc.
3. **Duyệt nội dung** (`content_review_status='approved'`, `approved_for_embedding`) cho tài liệu đã được cấp quyền; quyết định gỡ cách ly 2 tài liệu.
4. Khi 1–3 xong: `scripts/embed_chunks.py --execute --confirm-rights-approved` trên tập được phép (dự kiến ≤ 29 lời gọi API), rồi kiểm tra số vector/profile.
5. Phase 5: exact vector search baseline + PostgreSQL FTS + fusion + Cohere Rerank; dựng bộ câu hỏi chuẩn (cần chuyên gia ASD duyệt).
6. `git init` và commit đầu tiên khi được đồng ý.
