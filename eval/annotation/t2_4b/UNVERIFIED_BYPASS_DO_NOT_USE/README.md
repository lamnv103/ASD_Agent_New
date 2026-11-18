# KHÔNG DÙNG — dữ liệu từ quy trình chấm không được điều phối

Hai thư mục con ở đây (`ai_assisted_2026-11-17/`, `coordinator_final_output_2026-11-15/`) được một tiến trình khác tạo ra ngoài quy trình T2.4-B chính thức (không qua `show_question.py`, không qua `scripts/annotation_t2_4b.py`), trong lúc phiên làm việc bị gián đoạn giữa các lần chạy.

Lý do không tin:
- Gán tên model giả: `gpt-6.1-sol`, `gpt-6.1-terra`, `claude-sonnet-4-6` — không model nào tồn tại hoặc đúng tên thật của hai annotator thật (Opus = A, Sonnet = B).
- Tự tính đồng thuận, tự gộp nhãn, tự tạo file "final" ngoài hàm `agreement`/`finalize` chính thức của `scripts/annotation_t2_4b.py`.
- Không qua bước xác minh provenance, không qua cách ly khi vi phạm (khác với quy trình đã áp dụng cho các câu bị phát hiện đọc trực tiếp batch file: q033, q026, q057, q029, q042, q049, q003).
- Có "duplicate continuation outputs" tự gộp mà không rõ cơ chế chọn nhãn khi trùng.

Giữ lại chỉ để truy vết. Không dùng làm nhãn hay số liệu trong bất kỳ báo cáo T2.4-B hay T2.4-C.
