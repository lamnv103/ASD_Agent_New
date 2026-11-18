# ASD Agent

Trước mọi thay đổi code, dữ liệu, cấu hình, database hay cấu trúc thư mục trong dự án này, nạp skill `asd-agent-dev` (`.claude/skills/asd-agent-dev/SKILL.md`) và làm theo. Trạng thái từng phase nằm trong `README.md`.

Những điều không được quên kể cả khi chưa nạp skill:
1. `data/raw/` chỉ đọc; `data/corpus/` và `data/catalog/` chỉ sinh bằng `scripts/build_corpus.py`.
2. Schema DB chỉ đổi bằng migration mới trong `migrations/`; không sửa file đã áp dụng.
3. Không bật cờ phê duyệt hay quyền xử lý (`approved_*`, `content_review_status`, `*_allowed`) — đó là quyết định của người dùng.
4. Không gửi nội dung tài liệu sang Cohere/LLM ngoài nếu tài liệu không nằm trong `v_embedding_eligible_documents`.
5. Không chẩn đoán, không đưa liều thuốc; thiếu bằng chứng thì dùng đúng câu từ chối đã quy định.
6. Không đọc, in hay ghi log giá trị trong `.env`.
