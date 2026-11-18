# License classification repair — 2026-11-14 (Phase 5, Task A)

**Trạng thái: COMPLETED** (phân loại). Quyền xử lý: **BLOCKED** — không thay đổi, tất cả vẫn NULL.

## 1. Mục tiêu và phạm vi
Sửa phân loại của 35 tài liệu CC BY đang mang nhãn `verified_noncommercial_research`, dựa trên giấy phép đọc từ bản gốc. Không cấp quyền, không đổi chính sách sử dụng của dự án, không động tới 13 tài liệu NC và 25 tài liệu còn lại.

## 2. Trạng thái trước
- Catalog raw: 48 tài liệu `verified_noncommercial_research` = 10 CC BY-NC + 3 CC BY-NC-SA + 35 CC BY ([license_audit_2026-11-14.md](license_audit_2026-11-14.md)).
- DB: `source_rights.rights_status` theo nhãn raw; `license_type/version/rights_holder` NULL.

## 3. Thiết kế: lớp hiệu chỉnh thay vì sửa raw
Prompt yêu cầu "sửa raw source-of-truth" đồng thời "hash raw không đổi, không ghi đè tài liệu gốc". Hai yêu cầu chỉ cùng thoả được bằng một **lớp hiệu chỉnh có phiên bản**:

- `data/curation/license_corrections.jsonl` — nguồn chuẩn cho việc phân loại lại; mỗi dòng có `correction_id`, trạng thái from→to, loại/phiên bản/URL giấy phép, chủ sở hữu, **đường dẫn + SHA-256 của file bằng chứng gốc**, trích đoạn, `permissions_changed=false`, `project_usage_policy=null`, người/căn cứ uỷ quyền.
- `scripts/build_corpus.py` áp dụng lớp này khi sinh `data/catalog/sources.jsonl` và `data/corpus/manifest.jsonl`, sau khi kiểm tra: nguồn tồn tại, nhãn raw khớp `from`, hash bằng chứng không đổi, không có trường `*_allowed`, không có dòng trùng. `--check` báo lỗi nếu bản build cũ chưa áp dụng hiệu chỉnh (đã kiểm chứng: báo đúng 35 dòng "rebuild needed" trước khi build lại).
- Rollback: xoá file hiệu chỉnh và build lại → nhãn raw trở lại y nguyên.

## 4. Lệnh đã chạy
```
python -B scripts/license_classification_repair.py --dry-run   # 35 corrections; skipped: CC BY-NC 10, CC BY-NC-SA 3
python -B scripts/license_classification_repair.py             # sha256 fceb63db…7a1671
python -B scripts/build_corpus.py --check                       # (trước build) phát hiện 35 dòng cần build lại
python -B scripts/build_corpus.py   (×2)                        # hai lần build: manifest/sources giống hệt
python -B scripts/build_corpus.py --check                       # check: OK
docker exec asd-rag-v2-db pg_dump … > backups/asd_rag_v2_pre_license_fix_20261114_104702.dump
python -B scripts/import_sources.py                             # run 62ed4f56-e26d-4e91-bcf3-89e418fdba52
```
Tiêu chí chọn (thu thập lại bằng chứng trực tiếp từ bản gốc, không dùng CSV cũ): nhãn raw = `verified_noncommercial_research` **và** giấy phép trong bản gốc = CC BY **và** bằng chứng nằm trong chính tài liệu (JATS `<license>`) **và** không xung đột.

## 5. Kết quả
| Kiểm tra | Kết quả |
|---|---|
| Số hiệu chỉnh | **35** (CC BY 4.0 × 34, CC BY 3.0 × 1) — danh sách ID: mục 2 của [license_audit_2026-11-14.md](license_audit_2026-11-14.md) |
| Thay đổi trong catalog sinh ra | đúng 35 dòng (manifest và sources), chỉ các trường `rights_status`, `license_type`, `license_version`, `rights_holder` (33 dòng có holder trong XML), `rights_status_original`, `license_correction_id`; không trường nào khác đổi |
| Chuyển trạng thái | `verified_noncommercial_research → verified_cc_by` × 35 |
| 13 tài liệu NC | giữ `verified_noncommercial_research` |
| 25 tài liệu còn lại | giữ `verified`; **không** gán `license_type` (18 trong số đó chỉ có bằng chứng cấp chính sách cơ quan) |
| DB (73 tài liệu) | `verified_cc_by`/CC BY 4.0: 34 · `verified_cc_by`/CC BY 3.0: 1 · `verified_noncommercial_research`: 13 · `verified`: 25 |
| Cờ quyền trong DB | 0 khác NULL; `verified_by`/`verified_at`: 0 |
| Raw | digest toàn cây `data/raw` (199 file) `83f5f377…1d02` — **không đổi** (đối chiếu `backups/raw_baseline_2026-11-14.sha256`) |
| Test | `test_rights_row_uses_curated_classification_but_never_permissions`; integration `test_licence_classification_matches_the_curation` |

## 6. Vấn đề còn tồn tại
- Ghi `license_type` cho 13 tài liệu NC và 7 tài liệu public domain/CC BY có bằng chứng trong bản gốc chưa nằm trong phạm vi Task A (chỉ 35 tài liệu được sửa) — đề xuất làm ở bước sau bằng cùng cơ chế.
- 18 trang CDC/NIDCD chỉ có bằng chứng chính sách chung — giữ nguyên, không phân loại thêm.

## 7. Quyết định cần chủ dự án / pháp lý
1. Có áp dụng chính sách "chỉ dùng phi thương mại" cho cả kho (bất kể giấy phép) hay không — trường `project_usage_policy` đang để trống.
2. Mọi quyền xử lý (`archive/text_mining/chunking/embedding/cohere/external_llm/commercial`) — vẫn NULL.

## 8. Kết luận nghiệm thu
Phân loại 35 tài liệu CC BY: **COMPLETED**, có bằng chứng gốc, tái tạo được, rollback được, không đổi raw. Quyền: **BLOCKED** (chờ quyết định).
