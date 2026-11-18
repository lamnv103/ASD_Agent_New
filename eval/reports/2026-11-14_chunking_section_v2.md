# Chunking `section_v2` — 2026-11-14

**Kết luận: PARTIAL.** v2 đạt 7/9 tiêu chí chấp nhận. Hai tiêu chí chưa đạt không sửa được bằng code chunking mà cần trích xuất lại PDF: (1) bảng trong PDF đã mất cấu trúc hàng/cột, (2) 3 tài liệu WHO không có dấu trang nên không có page provenance. Các phần này được **gắn cờ và loại khỏi truy xuất**, không bị che giấu.

Không gọi API bên ngoài. Profile `section_v1` giữ nguyên để đối chiếu: 599 chunk v1 trong DB có hash không đổi (`4c4185431807d35364829ce55d324415`) trước và sau mọi thay đổi.

Bằng chứng: [regression JSON](2026-11-14_chunking_regression_section_v1_vs_section_v2.json) · [pilot v2](2026-11-14_chunking_pilot_section_v2.md) · [chunk tài liệu cách ly](2026-11-14_quarantine_chunks_section_v2.md)

## 1. Thay đổi so với v1 (bật bằng `features` trong `config/chunking_profiles.json`)

| Thành phần | Thay đổi | File |
|---|---|---|
| Bộ chuẩn hoá v2 | `[73](Reznick et al., 2007)` không còn bị hiểu là link (v1 xoá mất phần ngoặc — 15 tài liệu có mẫu này); mục `<li>`, `<br>`, `<break/>` trong ô bảng tách bằng `; `; bảng xuất dạng Markdown có hàng header + `|---|` | `app/ingest/markdown_blocks.py` |
| Layout pass cho PDF | Chỉ chạy với tài liệu **không có heading Markdown** (4 tài liệu). Header/footer theo vị trí mép trang + độ lặp + độ trải; số trang; tên chương in ở lề làm tiêu đề mục trong dải trang của nó; heading trong văn bản khi **hình thức và ngữ cảnh** cùng thoả; ghép đoạn ngắt dòng cứng, bỏ gạch nối; gắn cờ bảng bị dẹt | `app/ingest/pdf_layout.py` |
| Nhận diện theo nội dung | Danh sách tài liệu tham khảo (mục bắt đầu bằng tác giả + năm), danh sách người đóng góp ("Tên (Tổ chức, Quốc gia)" chiếm ≥ 35% văn bản), mục lục (dấu chấm dẫn), trang bản quyền/ISBN của PDF, chunk không có chữ → không truy xuất | `app/ingest/chunking.py` |
| Loại mục mới | `appendix`, `glossary`, `recommendations` (truy xuất được); `front_matter`, `contributors`, `*_detected`, `noise` (không truy xuất); `unclassified` khi không đủ căn cứ đặt tên mục | `app/ingest/chunking.py` |
| DB | Migration 004: `completeness_status` thêm `table_structure_lost`; view `v_chunk_provenance` (chunk + metadata kế thừa) | `migrations/004_*.sql` |

Không viết lại parser: v2 là các bước bổ sung có cờ bật/tắt; v1 tái tạo y hệt.

## 2. Regression — 71 tài liệu (2 tài liệu cách ly không chunk)

| Chỉ số | v1 | v2 |
|---|---:|---:|
| Chunk | 3.546 | 3.862 |
| Chunk truy xuất được | 2.580 | 2.592 |
| Chunk truy xuất được **có header/footer** | **386** | **1** |
| Chunk truy xuất được trông như danh sách tham khảo | 2 | **0** |
| Chunk truy xuất được trông như danh sách người đóng góp | 12 | **0** |
| Bảng có hàng header (`|---|`) | 0 | 286 / 357 |
| Bảng kèm caption | 214 | 223 |
| Chunk `table_structure_lost` (loại khỏi truy xuất) | — | 178 |
| Văn bản giữ lại | 98,66% | 96,90% (phần giảm = header/footer 70.126 ký tự, tiêu đề chạy 11.549, số trang 312) |
| Token median / max | 414 / 670 | 360 / 704 |
| Chunk > 700 token | 0 | 1 (một hàng bảng không thể cắt — quy tắc không cắt giữa hàng) |
| Chunk < 60 token (truy xuất được) | 224 | 306 |
| Page provenance (tài liệu có dấu trang) | 100% | 100% |
| Hai lần chạy cùng kết quả | — | có (hash `0b735bf6…`, 1.131 chunk pilot trong DB) |

Kiểm tra dương tính giả ở 67 tài liệu **không phải PDF**: chỉ 16 chunk bị v2 loại thêm so với quy tắc v1; đã đọc từng chunk — 1 danh sách tham khảo thật (ASD-CSV-017) và 15 mảnh rỗng ("Not applicable.", "2.1", "3.1.1", "∧ p < 0.1."). Không có bảng nào bị loại nhầm.

Chunk header/footer duy nhất còn lại là câu ghi nguồn bản quyền xuất hiện lần đầu trên trang bìa SENITA (nội dung thật, một lần).

## 3. Bốn tài liệu PDF

| source_id | v1 chunk / truy xuất | v2 chunk / truy xuất | Cấu trúc khôi phục | Trang |
|---|---|---|---|---|
| NIHR-SENITA-2022 | 286 / 286 | 324 / 232 | 9 tiêu đề chương (QUANTITATIVE RESULTS, HEALTH ECONOMICS, METHODS, REFERENCES…), 58 heading | 1–172 ✔ |
| WHO-CST-INTRO-2022 | 20 / 20 | 20 / 9 | heading "Background"; danh sách người đóng góp + mục lục bị loại | ✘ không có dấu trang |
| WHO-CST-PARTICIPANTS-2022 | 127 / 127 | 261 / 174 | 9 session làm mục, Annex 1 tách riêng | ✘ |
| WHO-ECD-GUIDELINE-2020 | 106 / 106 | 233 / 128 | KEY QUESTION I–V, RECOMMENDATION 1–4, BACKGROUND, SCOPE…; References bị loại | ✘ |

v1 coi **mọi** chunk của 4 tài liệu này là truy xuất được, kể cả footer bản quyền 81 trang, mục lục, danh sách người đóng góp và References.

## 4. Duyệt thủ công (15 chunk PDF + nhận xét)

Lý do chọn: mỗi tài liệu PDF một chunk truy xuất được cho mỗi loại mục khôi phục được, một chunk bị loại, một bảng bị dẹt. Đọc toàn văn từng chunk trong [pilot v2](2026-11-14_chunking_pilot_section_v2.md).

| Chunk | Lý do chọn | Nhận xét |
|---|---|---|
| SENITA #0006 | abstract, trang 10 | ✔ Phần Results của abstract, mạch lạc, không còn footer |
| SENITA #0008 | bảng dẹt | ✔ Thực ra là mục lục (đánh số la mã); bị loại đúng, nhãn chưa chính xác (TOC chứ không phải bảng) |
| SENITA #0037 | methods, trang 25–26 | ✔ Câu vắt qua trang được nối; đường dẫn "Methods" (trước khi sửa là "CONTENTS > Methods" — đã sửa bằng giới hạn dải trang của tiêu đề chạy) |
| SENITA #0235 | noise | ✔ Trục số biểu đồ "0 100 200 … 1000" bị loại |
| CST-INTRO #0000 | bảng dẹt | ✔ Tiêu đề bìa lặp, bị loại |
| CST-INTRO #0005 | contributors_detected | ✔ Danh sách "Tên (Tổ chức, Quốc gia)" bị loại |
| CST-INTRO #0010 | introduction | ✔ Đoạn Background đầy đủ; **không có số trang** |
| PARTICIPANTS #0000 | bảng dẹt | ✔ Tiêu đề bìa, bị loại |
| PARTICIPANTS #0010 | introduction | ✔ Background đầy đủ |
| PARTICIPANTS #0124 | front_matter_detected | ✔ Mục lục của session ("What we will learn today ……") bị loại |
| PARTICIPANTS #0251 | appendix | ✔ Annex 1 tách khỏi Session (trước khi sửa bị đặt dưới "Session 2") |
| ECD #0002 | bảng dẹt | ✔ Trang thông tin xuất bản + mục lục, bị loại |
| ECD #0014 | recommendations | ✔ Khuyến nghị kèm "Strength of recommendation: Strong / Quality of evidence: Moderate" |
| ECD #0015 | introduction | ✔ BACKGROUND đầy đủ |
| ECD #0125 | back_matter | ⚠ Mảnh bảng GRADE "WAZ 1 RCT No serious" nằm dưới đường dẫn "ANNEX 6 > DECLARATIONS OF CONFLICTS OF INTEREST" — bị loại (đúng kết quả) nhưng đường dẫn sai do bảng GRADE dẹt chèn giữa các annex |

Lỗi phát hiện trong vòng duyệt và **đã sửa, có test**: trang tác giả/đơn vị vẫn truy xuất được (SENITA); trang ISBN/bản quyền truy xuất được (CST-INTRO); tiêu đề chạy kéo sang trang không thuộc nó; chunk chỉ có số trang "263"; Annex bị đặt dưới Session; heading "13 Thirteen of"; nhãn bảng "HIGH"/"VERY LOW" bị coi là chương; "METHODS" (lề) và "Methods" (văn bản) bị gộp khiến heading thật bị xoá; ngắt trang luôn tách đoạn; hàng số liệu chỉ khác số ở mép trang có thể bị xoá như header.

## 5. Tiêu chí chấp nhận

| # | Tiêu chí | Kết quả |
|---|---|---|
| 1 | Không còn header lặp thành chunk độc lập | ✔ 386 → 1 (1 là nội dung thật) |
| 2 | References/Contributors không vào truy xuất mặc định | ✔ 0 chunk truy xuất được trông như danh sách tham khảo/người đóng góp |
| 3 | Heading nhận diện hợp lý hoặc `unclassified` | ✔ 25 chunk `unclassified`; không đặt tên mục không có căn cứ |
| 4 | Bảng và footnote có liên kết ngữ cảnh | ✔ bảng HTML (286 có header, caption + chú thích gộp); ✘ **bảng PDF**: 178 chunk mất cấu trúc → gắn cờ `table_structure_lost`, loại khỏi truy xuất |
| 5 | Page provenance đầy đủ | ✔ SENITA 100%; ✘ **3 tài liệu WHO không có dấu trang** trong bản chuyển đổi |
| 6 | Gaps mang cảnh báo đúng | ✔ `document_has_gaps` / `references_missing_component` / `table_structure_lost` + `missing_context` |
| 7 | Hai lần chạy ổn định | ✔ regression và DB |
| 8 | Unit test đạt | ✔ 56/56 (31 test mới cho v2, embedding, audit giấy phép; 25 test cũ không sửa) |
| 9 | Báo cáo có bằng chứng | ✔ file này + JSON |

## 6. Rủi ro còn lại

- **3 PDF của WHO cần trích xuất lại có dấu trang** (và bảng GRADE có cấu trúc) — thay đổi ở `data/raw`, cần duyệt. Không có thư viện PDF trong môi trường hiện tại; không có thông tin font nên heading suy từ hình thức + ngữ cảnh, không từ cỡ chữ.
- Chunk nhỏ tăng (PARTICIPANTS median 48 token — sách bài tập nhiều biểu mẫu). Cần benchmark retrieval trước khi quyết định gộp.
- Nhận diện theo nội dung là heuristic: đã kiểm tra dương tính giả trên 67 tài liệu không phải PDF, nhưng cần theo dõi khi thêm nguồn mới.
- v2 mới được lưu DB cho 10 tài liệu pilot (1.131 chunk). Chạy cho toàn bộ 71 tài liệu là bước tiếp theo sau khi chủ dự án chấp nhận báo cáo này.
