# PDF extraction repair — 2026-11-14 (Phase 5, Task B)

| Hạng mục | Trạng thái |
|---|---|
| B1 – Số trang của 3 PDF WHO | **COMPLETED** — khôi phục chính xác, không đổi corpus |
| B2 – Bảng PDF mất cấu trúc | **PARTIAL** — 0 bảng được đưa vào truy xuất; 1 bảng dựng lại chờ người duyệt; còn lại `table_structure_unrecoverable` |
| Phát hiện mới – lỗi mã hoá glyph | **PARTIAL** — đã phát hiện và loại; có bản trích xuất lại đề xuất, chờ duyệt |

Không gọi API bên ngoài. Không sửa `data/raw` (digest `83f5f377…` không đổi), không sửa corpus. Mọi đầu ra mới nằm trong `data/extractions/<source_id>/` với tên có phiên bản.

## B1. Ba PDF WHO thiếu số trang

### Điều tra
| source_id | Trang PDF | Trang có chữ | Producer | Nhãn trang in |
|---|---:|---:|---|---|
| WHO-CST-INTRO-2022 | 20 | 17 | Adobe PDF Library 16.0 (InDesign 16.4) | 1, 2, i, ii, iii… |
| WHO-ECD-GUIDELINE-2020 | 80 | 79 | Adobe PDF Library 15.0 (InDesign 15.0) | A, B, i, ii… |
| WHO-CST-PARTICIPANTS-2022 | 278 | 276 | Adobe PDF Library 16.0 (InDesign 16.4) | 1, 2, I, II… |

**Nguyên nhân:** bộ chuyển đổi cũ (`Carobud_ASD_2026/scripts/source_library/build_library.py`) trích từng trang bằng `pypdf 6.11.0` rồi `clean("\n\n".join(pages))` — **không chèn dấu trang** (khác SENITA, được trích kèm `SOURCE_PDF_PAGE`).

### Giải pháp (không trích xuất lại nội dung)
Chạy lại đúng `pypdf 6.11.0` + cùng phép ghép và `clean()` → văn bản **trùng từng byte** với thân corpus của cả 3 tài liệu; độ dài từng trang **trùng** với bằng chứng độc lập `conversion_checks/<id>.json` của dự án cũ. Ranh giới trang được tính bằng cách dịch vị trí ký tự qua đúng phép biến đổi đó (`app/ingest/pdf_page_map.py`). Mỗi trang được kiểm: đoạn corpus gán cho trang = văn bản trang (chuẩn hoá khoảng trắng).

| File (verified = true) | Trang | Trang rỗng | Nhãn null | SHA-256 |
|---|---:|---:|---:|---|
| `data/extractions/WHO-CST-INTRO-2022/page_map.pypdf-6.11.0.v1.json` | 20 | 3 | 0 | 19094532…dd4b |
| `data/extractions/WHO-ECD-GUIDELINE-2020/page_map.pypdf-6.11.0.v1.json` | 80 | 1 | 0 | 2a330110…532a |
| `data/extractions/WHO-CST-PARTICIPANTS-2022/page_map.pypdf-6.11.0.v1.json` | 278 | 2 | 7 (tr. 272–278) | f76b235f…a0 |

- Mỗi trang ghi số trang vật lý (1-based) **và** nhãn in trong PDF; nhãn mà `pypdf` cảnh báo "không xác định chắc chắn" được ghi `null`, không đoán.
- Script từ chối ghi đè bản đồ đã có cho input khác (phải tăng phiên bản).
- Không đạt kiểm chứng → không ghi bản đồ → chunk mang `page_provenance_incomplete` và bị loại khỏi truy xuất (có test).
- Kết quả trong `section_v2_1`: **100% chunk của 4 PDF có `page_start/page_end`** (integration test `test_pdf_chunks_of_section_v2_1_have_page_provenance`).

## B2. Bảng PDF mất cấu trúc

### Phương pháp
`scripts/pdf_table_recovery.py`: chạy `pdfplumber 0.11.10` (MIT) `find_tables` (dựa trên đường kẻ) trên **PDF gốc**, chỉ ở các trang có chunk bị gắn cờ bảng. Ứng viên chỉ qua khi: ≥ 2 hàng, ≥ 2 cột, hình chữ nhật, ô trống ≤ 50%, ≥ 90% token có trong văn bản đã trích của chính trang đó, ≥ 90% **từ chữ** có trong trang, ≥ 90% token hàng tiêu đề có trong trang. Ngoài ra phát hiện chữ bị đọc ngược (tiêu đề xoay) và ghi vào `defects`. Ô giữ nguyên văn, ô trống để trống, không suy giá trị.

### Kết quả (lần quét cuối, trên mọi trang có chunk bị gắn cờ trong `section_v2_1` cuối cùng)
| source_id | Trang quét | Ứng viên | Qua kiểm tra | Lý do thất bại chính | Sidecar SHA-256 |
|---|---:|---:|---:|---|---|
| NIHR-SENITA-2022 | 87 | 74 | 0 | bảng không kẻ ô → chỉ bắt được hàng tiêu đề; ô trống > 50%; độ phủ từ thấp | 87a4d830… |
| WHO-ECD-GUIDELINE-2020 | 29 | 21 | **6** | tiêu đề xoay đọc ngược; độ phủ thấp | 8771a5eb… |
| WHO-CST-PARTICIPANTS-2022 | 19 | 1 | 0 | biểu mẫu trống | 59edc763… |
| WHO-CST-INTRO-2022 | 0 | 0 | 0 | — | e3b0c442… (rỗng) |

Sáu ứng viên WHO-ECD qua kiểm tra, trạng thái `recovered_pending_human_review` (**không truy xuất**):

| Trang | Kích thước | Nội dung | Lỗi phát hiện |
|---:|---|---|---|
| 27 | 9 × 7 | hệ số hiệu ứng theo kết cục (trẻ / người chăm sóc) | không |
| 31 | 8 × 7 | hệ số hiệu ứng | không |
| 37 | 10 × 10 (2 bảng) | hệ số hiệu ứng, KTC, N | không |
| 38 | 10 × 10 | hệ số hiệu ứng, KTC, N | không |
| 78 | 18 × 13 | bảng GRADE | 11 ô hàng 1 (tiêu đề cột xoay) bị đọc ngược ("seiduts fo .oN") |

Lặp lại việc quét cho tới khi ổn định: lần chạy cuối cho file sidecar trùng hash với lần trước.

**Kết luận:** các bảng không kẻ ô của SENITA (và phần lớn bảng GRADE) không khôi phục tự động một cách tin cậy được; dựng bảng bằng căn vị trí chữ sẽ tạo "bảng giả" từ văn bản phẳng — trái nguyên tắc — nên không dùng.

### Trạng thái chunk (`section_v2_1`, 4 PDF) — chi tiết: [pdf_extraction_diff.csv](pdf_extraction_diff.csv) (244 dòng, SHA-256 5f555a03…)
| Trạng thái | SENITA | ECD | PARTICIPANTS | CST-INTRO |
|---|---:|---:|---:|---:|
| `table_structure_unrecoverable` | 133 | 40 | 20 | 0 |
| `table_recovered_pending_review` | 0 | 11 | 0 | 0 |
| `text_encoding_lost` | 0 | 0 | 40 | 0 |

Tất cả đều `retrieval_eligible = false`; migration 005 thêm ràng buộc `chunks_unverified_structure_not_retrievable` để **ngay cả role owner** cũng không bật được truy xuất cho các trạng thái này (đã thử: CheckViolation).

Phát hiện bảng trong `section_v2_1` (chỉ PDF): chạy ô ngắn ≥ 8 dòng; ≥ 3 dòng hàng số liệu liên tiếp; vùng sau tiêu đề in hoa "TABLE n" tới hết đoạn; đoạn ngắn toàn số ("None 289 295 – SMD 0.3 SD higher"); chunk có tỷ lệ số cao; chuỗi ≥ 5 con số liền nhau trong văn xuôi (≥ 4 nếu trang có bảng khôi phục được — khi đó chunk chờ duyệt cùng bảng đó). Bảng được chuyển thành ô có cấu trúc chỉ khi nguồn là HTML/JATS (286 bảng có hàng tiêu đề, giữ caption, chú thích, đơn vị).

## Phát hiện mới: lỗi mã hoá glyph (WHO-CST-PARTICIPANTS-2022)
- 8 trang (62, 73, 87, 95, 121, 144, 168, 192), 83 dòng, 2.248 chuỗi `/gidNNNNN` — font thiếu bảng ToUnicode, `pypdf` xuất mã glyph thay vì chữ.
- `pdfium` đọc được chữ bình thường ở cả 8 trang → bản đề xuất: `data/extractions/WHO-CST-PARTICIPANTS-2022/page_text.pypdfium2-5.15.2.gid_pages.v1.jsonl` (496cc2e0…), không còn `/gid`.
- 40 chunk `text_encoding_lost`, không truy xuất. Áp dụng bản trích xuất lại cần duyệt và tạo phiên bản tài liệu mới (thay đổi corpus).

## Lệnh đã chạy
```
python -B scripts/pdf_page_map.py WHO-CST-INTRO-2022 WHO-ECD-GUIDELINE-2020 WHO-CST-PARTICIPANTS-2022
python -u -B scripts/pdf_table_recovery.py      (chạy 6 lần: siết kiểm tra, rồi quét lại sau mỗi lần quy tắc gắn cờ đổi; 2 lần cuối trùng hash)
python -B scripts/acceptance_artifacts.py       → pdf_extraction_diff.csv, section_v2_regression.csv
```
Thư viện thêm vào `pyproject.toml`: `pypdf==6.11.0` (ghim đúng phiên bản bộ chuyển đổi cũ), `pdfplumber>=0.11,<0.12` (MIT; kéo theo `pdfminer.six` MIT, `pypdfium2` BSD/Apache). Không dùng PyMuPDF (AGPL).

## Vấn đề còn tồn tại
1. 193 chunk bảng PDF không khôi phục được — cần nhập tay hoặc công cụ trích bảng theo bố cục có người kiểm.
2. Văn xuôi ngay sau một bảng PDF có thể bị loại cùng vùng bảng (vùng kéo tới hết đoạn) — sai lệch về phía an toàn.
2b. Còn 4 chunk truy xuất được có chuỗi 4 con số — đã đọc: 1 trích dẫn có "…" (SENITA #77) và 3 thang đánh số "1 2 3 4" trong biểu mẫu; không phải dữ liệu bảng ([section_v2_1_residual_numeric_runs.csv](section_v2_1_residual_numeric_runs.csv)).
3. 8 trang lỗi glyph chờ áp dụng bản trích xuất pdfium.

## Quyết định cần
- Người duyệt nội dung: 6 bảng WHO-ECD chờ duyệt (sửa hàng tiêu đề ngược ở trang 78) và 8 trang pdfium.
- Chủ dự án: có đầu tư nhập/kiểm tay các bảng lâm sàng của SENITA/ECD không.

## Kết luận nghiệm thu
B1 **COMPLETED** (kiểm chứng từng byte, từng trang). B2 **PARTIAL**: không bảng chưa kiểm chứng nào vào truy xuất, nhưng bảng PDF chưa được khôi phục.
