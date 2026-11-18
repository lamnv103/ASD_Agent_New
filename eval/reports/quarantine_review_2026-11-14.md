# Quarantine review — 2026-11-14

Đối tượng: `ASD-CSV-077`, `NIH-NIMH-CHILDREN` (cờ `text_fidelity` trong catalog, `content_review_status = quarantined` trong DB).

**Kết luận chung: cả hai vẫn CÁCH LY.** Audit này chỉ xác định bản chất lỗi chuyển đổi; không gỡ cách ly, không đặt `approved`, không kết luận nội dung đúng chuyên môn. Gỡ cách ly cần người chịu trách nhiệm phê duyệt (role owner) sau khi xem các bằng chứng dưới đây.

Phương pháp: đối chiếu đoạn `original_text` mà catalog ghi lại với (1) file gốc trong `data/raw/source_library/originals/`, (2) file corpus `data/corpus/gaps/<id>.md`, (3) văn bản do bộ chunking tạo ra. Không gửi nội dung ra ngoài.

## 1. ASD-CSV-077 — Systematic Review of Level 1 and Level 2 Screening Tools for ASD (Brain Sci 2020, CC BY 4.0)

| Hạng mục | Kết quả |
|---|---|
| File gốc | `originals/ASD-CSV-077/snapshot-20261017-e72907221967.xml` (JATS) |
| Vị trí nghi ngờ | Bảng công cụ sàng lọc, dòng **First Year Inventory (FYI)**, cột **Cut-Off** |
| Bản gốc (XML) | `30 (95th); 40<break/>(98th); 50 (99th) [<xref>73</xref>]<break/>(Reznick et al., 2007);<break/>22.55 (95th);<break/>28.14 (98th) [<xref>39</xref>];<break/>19.2 (96th) [<xref>84</xref>].` |
| Corpus (đã chuyển đổi) | `30 (95th); 40(98th); 50 (99th) [73](Reznick et al., 2007);22.55 (95th);28.14 (98th) [39];19.2 (96th) [84].` |
| Loại lỗi | **Chuyển đổi**: thẻ `<break/>` trong ô bảng bị bỏ, không thay bằng dấu ngắt. Không phải OCR, không phải encoding. |
| Số liệu | Đủ 6 giá trị cut-off và 3 trích dẫn; không mất hay đổi số nào. |
| Ảnh hưởng khoa học | Trung bình: ranh giới giữa các bộ cut-off (theo từng nghiên cứu 73 / 39 / 84) khó đọc; đọc sai có thể gán nhầm cut-off cho nghiên cứu. |
| Lỗi phát sinh thêm ở bộ chunking v1 | Chuỗi `[73](Reznick et al., 2007)` bị bộ chuẩn hoá v1 hiểu nhầm là link Markdown và **xoá mất "(Reznick et al., 2007)"**. Lỗi này có ở 15 tài liệu (42 chỗ khớp mẫu, phần lớn là link ảnh hợp lệ). Đã sửa trong bộ chuẩn hoá v2 (chỉ coi là link khi đích giống URL/đường dẫn). |

**Đề xuất:** trích xuất lại bảng này từ XML gốc, thay `<break/>` bằng `; ` (hoặc xuống dòng trong ô) — đây là thay đổi ở bước chuyển đổi raw → corpus, cần được duyệt vì `data/raw` là chỉ đọc. Sau khi trích xuất lại: so khớp 6 giá trị số với XML, rồi người duyệt quyết định gỡ cách ly.

## 2. NIH-NIMH-CHILDREN — Children and Mental Health: Is This Just a Stage? (NIMH, public domain)

| Hạng mục | Kết quả |
|---|---|
| File gốc | `originals/NIH-NIMH-CHILDREN/snapshot-20261017-831beee50434.html` |
| Vị trí nghi ngờ | Bảng 2 cột "Younger children" / "Older children", mỗi ô là danh sách `<ul><li>` các dấu hiệu nên đi khám |
| Corpus | Giữ nguyên HTML `<table>…<ul><li>…</li></ul>…</table>` — **cấu trúc danh sách còn đầy đủ** |
| Kiểm tra | 19/19 mục `<li>` trong corpus có nguyên văn trong bản gốc |
| Loại lỗi | **Chuyển đổi sang văn bản thuần**: khi bỏ thẻ, các mục danh sách bị nối liền không dấu ngắt ("…irritable much of the time Often seem fearful…"). Lỗi xảy ra ở bước tạo `original_text` của catalog và ở bộ chuẩn hoá bảng v1 (ô bảng nối mục `<li>` không có dấu ngắt). |
| Ảnh hưởng khoa học | Thấp về số liệu (không có số), nhưng đáng kể về nghĩa: ranh giới giữa các dấu hiệu bị mất; danh sách "Older children" có mục **tự gây hại** và **ý nghĩ tự sát** — nội dung nhạy cảm, cần hiển thị đúng từng mục. |
| Xử lý ở chunking v2 | Bộ chuẩn hoá v2 tách mục `<li>` trong ô bảng bằng "; " và `<br>` thành "; " — không cần sửa raw. |

**Đề xuất:** sau khi chạy chunking v2, người duyệt xem lại chunk bảng của tài liệu này (đối chiếu từng mục với bản gốc). Lưu ý cho tầng trả lời: đây là danh sách dấu hiệu cần đánh giá chuyên môn, không phải tiêu chí chẩn đoán; câu hỏi liên quan tự hại phải đi nhánh safety.

## 3. Trạng thái

| source_id | Trước | Sau audit | Ai gỡ cách ly |
|---|---|---|---|
| ASD-CSV-077 | quarantined | quarantined — chờ trích xuất lại bảng FYI từ XML | chủ dự án / người duyệt nội dung |
| NIH-NIMH-CHILDREN | quarantined | quarantined — chờ duyệt chunk bảng do v2 tạo | chủ dự án / người duyệt nội dung |

Không có thay đổi nào trong DB hay `data/raw`.
