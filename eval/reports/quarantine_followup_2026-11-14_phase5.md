# Quarantine follow-up — 2026-11-14 (Phase 5, Task C/D)

**Trạng thái: COMPLETED** (điều tra + hồ sơ đề xuất). Gỡ cách ly: **BLOCKED** — cần người có thẩm quyền.

Cả hai tài liệu vẫn `content_review_status = quarantined`, không có chunk nào trong DB (integration test `test_quarantined_documents_stay_quarantined_and_unchunked`). Không đổi raw, corpus hay `clinical_reviewed`. Báo cáo trước: [quarantine_review_2026-11-14.md](quarantine_review_2026-11-14.md).

## 1. ASD-CSV-077 — Systematic Review of Level 1 and Level 2 Screening Tools for ASD

| Hạng mục | Kết quả |
|---|---|
| Bản gốc | `originals/ASD-CSV-077/snapshot-20261017-e72907221967.xml`, SHA-256 `e72907221967d34b…ffd95` |
| Corpus | `data/corpus/gaps/ASD-CSV-077.md`, SHA-256 `7e89a09a…c810` |
| Loại lỗi | **Chuyển đổi** (không phải OCR/encoding): thẻ JATS `<break/>` trong ô bảng bị bỏ |
| Phạm vi thật | **61 ô ở cả 3 bảng** (Bảng 1: 11, Bảng 2: 48, Bảng 3: 2) — catalog chỉ ghi 1 ô (FYI) |
| Số liệu | 61/61 ô: tập số giống hệt giữa văn bản hiện tại và bản đề xuất; 61/61 ô hiện tại khớp nguyên văn corpus (so sánh trên văn bản đã bỏ thẻ) |
| Trích dẫn | Ô FYI có `[73](Reznick et al., 2007)`: profile v1 làm mất "(Reznick et al., 2007)"; v2/v2_1 giữ đủ |
| Hồ sơ đề xuất | `data/extractions/ASD-CSV-077/table_cells.jats-breaks.v1.json`, SHA-256 `ea9d92e2…5b73` |

**Quy tắc đề xuất:** thay mỗi `<break/>` bằng **một khoảng trắng** — không suy ra dấu phân tách. Bản nháp đầu tiên chèn "; " và tạo ra "40; (98th)" (sai nghĩa: `<break/>` ở đó chỉ là xuống dòng hiển thị của "40 (98th)"); đã sửa. Ô FYI theo đề xuất:

> 30 (95th); 40 (98th); 50 (99th) [73] (Reznick et al., 2007); 22.55 (95th); 28.14 (98th) [39]; 19.2 (96th) [84].

35/61 ô có ranh giới mục **mơ hồ** (phần trước không có dấu câu, phần sau viết hoa, ví dụ "Study 1 N = 19 ASD N = 13 ODD…") — đánh dấu `ambiguous_item_boundaries` để người duyệt quyết định cách tách mục.

## 2. NIH-NIMH-CHILDREN — Children and Mental Health: Is This Just a Stage?

| Hạng mục | Kết quả |
|---|---|
| Bản gốc | `originals/NIH-NIMH-CHILDREN/snapshot-20261017-831beee50434.html`, SHA-256 `831beee5…0158` |
| Corpus | `data/corpus/gaps/NIH-NIMH-CHILDREN.md`, SHA-256 `9a87949a…e119` |
| Loại lỗi | **Chuyển sang văn bản thuần**: các mục `<li>` trong bảng 2 cột bị nối liền khi bỏ thẻ |
| Kiểm tra | 19/19 mục có nguyên văn trong bản gốc; 19/19 mục xuất hiện tách biệt (phân cách "; ") trong chunk bảng của `section_v2_1` |
| Hồ sơ đề xuất | `data/extractions/NIH-NIMH-CHILDREN/table_list_items.v1.json`, SHA-256 `8194646a…e758` (kèm toàn văn chunk bảng v2_1 và SHA-256 của nó) |
| Nội dung nhạy cảm | Cột "Older children" có tự gây hại và ý nghĩ tự sát → khi được dùng, câu hỏi liên quan phải đi nhánh safety |

Không cần sửa raw: bộ chuẩn hoá v2 đã tách mục đúng.

## 3. Lệnh đã chạy
```
python -B scripts/quarantine_reextraction.py
python -B scripts/chunk_pilot.py --profile section_v2_1 --review-quarantined   # chỉ báo cáo, không ghi DB
```
Chunk để duyệt: [2026-11-14_quarantine_chunks_section_v2_1.md](2026-11-14_quarantine_chunks_section_v2_1.md) (ASD-CSV-077: 53 chunk; NIH-NIMH-CHILDREN: 14 chunk).

## 4. Quyết định cần người có thẩm quyền
| source_id | Cần quyết định | Sau khi quyết định |
|---|---|---|
| ASD-CSV-077 | (a) duyệt quy tắc "<break/> → khoảng trắng"; (b) cách tách 35 ô mơ hồ | tạo phiên bản tài liệu mới từ XML (thay đổi corpus, có phiên bản), chunk lại, rồi mới xét gỡ cách ly |
| NIH-NIMH-CHILDREN | đối chiếu chunk bảng v2_1 với bản gốc | gỡ cách ly bằng role owner (`content_review_status`, xoá `content_warning`) — chưa làm |

Không trạng thái nào được tự chuyển: `quarantined → active`, `excluded → eligible`, `clinical_reviewed false → true`.

## 5. Kết luận
Điều tra **COMPLETED**; hai tài liệu vẫn **cách ly**; hồ sơ đề xuất sẵn sàng cho người duyệt.
