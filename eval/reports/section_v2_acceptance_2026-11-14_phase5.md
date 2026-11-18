# Section V2 acceptance — 2026-11-14 (Phase 5, Task C nghiệm thu chunking)

**Kết luận: `section_v2_1` đạt 9/9 tiêu chí trên corpus 71 tài liệu — COMPLETED về kỹ thuật chunking**, với giới hạn được nêu rõ ở mục 6 (bảng PDF không khôi phục được bị *loại khỏi truy xuất* chứ không được *khôi phục*; khôi phục là việc của Task B, trạng thái PARTIAL).

## 1. Phạm vi và quyết định đặt tên profile
- Profile được nghiệm thu là **`section_v2_1`**, không sửa `section_v2`: mọi thay đổi nằm sau `features.rules = "v2_1"`, `page_maps`, `table_review`, để `section_v1` (599 chunk) và `section_v2` (1.131 chunk) trong DB **vẫn tái tạo y hệt** (đã kiểm sau từng thay đổi; lần cuối: cả 3 profile IDENTICAL).
- Corpus: 71 tài liệu (73 trừ 2 cách ly). Không gọi API, không đổi raw/corpus.

## 2. Trạng thái trước
`section_v2`: 7/9 tiêu chí — thiếu page provenance của 3 PDF WHO và bảng PDF bị dẹt; có thêm lỗi phát hiện trong lượt này (mục 4).

## 3. Kết quả regression (71 tài liệu) — [section_v2_regression.csv](section_v2_regression.csv), JSON: `2026-11-14_chunking_regression_section_v1_vs_section_v2_1.json`, `…_section_v2_vs_section_v2_1.json`

| Chỉ số | v1 | v2 | v2_1 |
|---|---:|---:|---:|
| Chunk | 3.546 | 3.862 | 3.740 |
| Truy xuất được | 2.580 | 2.592 | 2.435 |
| Truy xuất được có header/footer (chuỗi ≥ 40 ký tự đã bị loại) | 312 | 1 | 1 (trang bìa sau SENITA, xuất hiện một lần) |
| Truy xuất được trông như danh sách tham khảo / người đóng góp | 2 / 12 | 0 / 0 | 0 / 0 |
| Bảng HTML có hàng tiêu đề / có caption | 0 / 214 | 286 / 223 | 286 / 223 |
| `table_structure_unrecoverable` / `table_recovered_pending_review` / `text_encoding_lost` | — | (178 `table_structure_lost`) | 193 / 11 / 40 |
| Page provenance, 4 PDF | 1/4 tài liệu | 1/4 | **4/4 (100% chunk)** |
| Văn bản giữ lại | 98,66% | 96,90% | 96,98% |
| Token median / max | 414 / 670 | 360 / 704 | 373 / 704 (1 hàng bảng không cắt được) |
| Hai lần chạy giống hệt | — | có | có (regression + DB: 3.740 chunk, ghi 2 lần cùng hash) |
| Chunk tài liệu không-PDF bị loại thêm so với quy tắc v1 | — | 16 | 16 (đã đọc: 1 danh sách tham khảo thật + 15 mảnh rỗng như "Not applicable.") |

PDF (v1 → v2 → v2_1, chunk/truy xuất được): SENITA 286/286 → 324/232 → 354/190 · CST-INTRO 20/20 → 20/9 → 18/9 · CST-PARTICIPANTS 127/127 → 261/174 → 156/73 · ECD 106/106 → 233/128 → 188/114.

## 4. Lỗi phát hiện trong lượt này và cách sửa (mỗi lỗi có test)
| Lỗi | Phát hiện bởi | Sửa |
|---|---|---|
| 3 PDF WHO không có số trang | báo cáo trước | bản đồ trang tái tạo từng byte (Task B1) |
| Quy tắc "trùng nguyên văn ở mép trang thì giữ bản đầu" **xoá heading thật** lặp theo session ("What we will learn today", "WHO recommends:") | đọc danh sách dòng bị xoá | v2_1 không xoá trùng lặp; boilerplate rải rác còn phải chiếm ≥ 15% số trang |
| "METHODS" (lề) và "Methods" (văn bản) bị gộp do so khớp không phân biệt hoa thường | test | khoá so khớp giữ hoa/thường |
| Tiêu đề session ở trang mục lục/annex kéo dài "dải trang" của tiêu đề chạy → 5/9 session | đếm tiêu đề | dải trang liên tục (cách ≤ 2 trang), bỏ lần xuất hiện lẻ |
| Heading giả "69 For all ABC subscales…" | duyệt thủ công | số nguyên trần chỉ là heading khi chữ có dạng tiêu đề |
| **Chuỗi mã glyph `/gid…` truy xuất được** (8 trang PARTICIPANTS) | duyệt thủ công | `text_encoding_lost` |
| Nội dung khảo sát bị coi là "trang đầu" do mẫu "Health Board 12" | duyệt thủ công | mẫu tác giả–đơn vị chỉ xét ở 10% trang đầu |
| Hàng số liệu dài, vùng "TABLE n", mảnh hệ số hiệu ứng ngắn, chuỗi số trong văn xuôi **truy xuất được** | duyệt thủ công + đo | 5 quy tắc gắn cờ bảng (mục 5, tiêu chí 4) |
| Hàng số liệu chỉ khác số ở mép trang có thể bị xoá như footer | test | số của footer phải cố định hoặc chạy theo số trang |

## 5. Tiêu chí chấp nhận
| # | Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Heading detection (hoa/thường, đánh số, Chapter/Session/Annex, đặc biệt) | ✔ | SENITA 9 tiêu đề chương + heading; PARTICIPANTS 9 session + Annex; ECD KEY QUESTION I–V, RECOMMENDATION 1–4; không đủ căn cứ → `unclassified` (25 chunk) |
| 2 | Header/footer removal | ✔ | 312 → 1; không xoá heading thật (test `test_repeated_real_headings_are_kept_in_v2_1_but_deduplicated_in_v2`) |
| 3 | References exclusion (giữa/cuối tài liệu) | ✔ | 0 chunk truy xuất được trông như danh sách tham khảo; References giữ trong raw/DB với `retrieval_eligible=false` |
| 4 | Contributor/acknowledgement exclusion | ✔ | 0; `contributors`, `contributors_detected`, `back_matter` |
| 5 | Table preservation | ✔ theo chính sách | Bảng HTML/JATS: cấu trúc Markdown + caption + chú thích + đơn vị. Bảng PDF: **không bảng chưa kiểm chứng nào truy xuất được** (193 unrecoverable, 11 chờ duyệt cùng bảng dựng lại); bảng sau References → `floating_table`. Dư lượng: 4 chunk có chuỗi 4 số — đã đọc, không phải dữ liệu bảng ([section_v2_1_residual_numeric_runs.csv](section_v2_1_residual_numeric_runs.csv)) |
| 6 | Citation preservation | ✔ | bộ chuẩn hoá v2 giữ "[73] (Reznick et al., 2007)" (v1 làm mất ở 15 tài liệu) |
| 7 | Page provenance | ✔ | 100% chunk của 4 PDF có trang (integration test); tài liệu HTML/XML không có trang → `char_start/char_end` |
| 8 | Deterministic output | ✔ | regression 2 lần + ghi DB 2 lần cùng hash; v1/v2/v2_1 tái tạo y hệt DB |
| 9 | Retrieval eligibility & completeness flags | ✔ | `complete` 1.526, `document_has_gaps` 1.658, `references_missing_component` 312, + 3 trạng thái mới; ràng buộc DB cấm truy xuất trạng thái chưa kiểm chứng (thử bằng owner: CheckViolation) |

Kiểm thử: 71 unit test (25 cũ không sửa, 46 mới), 7 integration test trên DB thật (`pytest -m integration`), ruff sạch.

## 6. Duyệt thủ công
52 chunk (SENITA 17, CST-INTRO 11, CST-PARTICIPANTS 12, ECD 12) chọn có quy tắc (mỗi loại mục một chunk giữa, mỗi trạng thái bảng một chunk, rải đều trên tài liệu): [2026-11-14_section_v2_1_manual_review_samples.json](2026-11-14_section_v2_1_manual_review_samples.json) (SHA-256 23c57a87…). Đọc lại sau mỗi vòng sửa; nhận xét vòng cuối:

- Đạt: phần thân SENITA (Introduction, Methods, Discussion, Strengths and limitations) mạch lạc, câu vắt trang được nối, không footer; vùng "TABLE 13", "TABLE 35" bị loại còn văn xuôi trước bảng được giữ; WHO Background/Recommendations đầy đủ; danh sách người đóng góp, trang ISBN, mục lục, References bị loại.
- Chờ duyệt đúng: ECD #40, #50 chứa bảng hệ số hiệu ứng → `table_recovered_pending_review` cùng bảng 9×7 / 8×7 dựng từ PDF.
- Giới hạn đã biết (sai lệch về phía an toàn): một câu văn ngay sau bảng có thể bị loại cùng vùng bảng (SENITA "Ninety (56.5%) carers…"); trang bài tập PARTICIPANTS #69 bị gắn nhầm `front_matter_detected`; mảnh GRADE "HAZ 1 RCT No serious" mang đường dẫn sai (ANNEX 6) nhưng đã bị loại.

## 7. Theo từng tài liệu
| Nhóm | Kết luận |
|---|---|
| 67 tài liệu HTML/XML | 9/9 |
| NIHR-SENITA-2022 | 9/9; 133 chunk bảng không khôi phục được (bị loại) — mất độ phủ số liệu |
| WHO-CST-INTRO-2022 | 9/9 |
| WHO-CST-PARTICIPANTS-2022 | 9/9; 40 chunk lỗi glyph bị loại (8 trang, có bản pdfium chờ duyệt), 20 chunk biểu mẫu dẹt |
| WHO-ECD-GUIDELINE-2020 | 9/9; 11 chunk chờ duyệt cùng 6 bảng dựng lại; 40 chunk GRADE không khôi phục được |

## 8. Thay đổi DB
Migration **005** (`completeness_status` thêm 4 trạng thái + ràng buộc cấm truy xuất): backup → thử apply/rollback/re-apply trên container cô lập (2 lần, lần 2 sau khi thêm `text_encoding_lost`) → áp dụng. `section_v2_1`: 3.740 chunk cho 71 tài liệu (ingestion run cuối `5a6156c5-2bb9-4139-8885-bcc1445d70a8`). **Lưu ý minh bạch:** chunk v2_1 được ghi vào DB trong quá trình lặp, trước khi lượt sửa cuối hoàn tất; chúng không truy xuất được (0 tài liệu qua cổng) và đã được ghi lại bằng code cuối. Backup ngay trước lần ghi cuối: `backups/asd_rag_v2_pre_v2_1_rewrite_20261114_144203.dump`.

## 9. Quyết định cần
Duyệt 11 chunk/6 bảng chờ duyệt; quyết định có nhập tay bảng PDF quan trọng; áp dụng bản pdfium cho 8 trang lỗi glyph.
