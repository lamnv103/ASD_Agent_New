---
name: asd-agent-dev
description: Quy ước kiến trúc, dữ liệu, clean code và bảo mật cho dự án ASD Agent (D:\AI4LIFE\ASD_AGENT_FINALL) — trợ lý RAG hỏi đáp về tự kỷ ở trẻ 0–18 tuổi. Dùng skill này TRƯỚC mọi thay đổi trong dự án: viết hoặc sửa code trong app/, scripts/, tests/, config/; chunking, embedding, index, rerank; router/phân loại câu hỏi; prompt và cách sinh câu trả lời; thêm thư mục, file hay thư viện; đánh giá (eval); cấu hình .env, docker, database. Dùng cả khi người dùng chỉ nói "làm bước tiếp theo", "triển khai nhánh X", "sửa lỗi", "thêm tính năng" trong dự án này.
---

# ASD Agent — quy ước triển khai

Mục tiêu của skill: mọi thay đổi đều đặt đúng chỗ, theo đúng một luồng, để dự án không phình ra lộn xộn. Khi một quy tắc dưới đây có vẻ cản trở, hãy dừng lại và hỏi người dùng thay vì lách — quy tắc thường tồn tại vì một rủi ro cụ thể (y khoa, bản quyền, lộ key, index lệch dữ liệu).

Trước khi bắt đầu, đọc `README.md` ở gốc dự án để biết trạng thái hiện tại. Khi cần định dạng dữ liệu (manifest, chunk, index, eval), đọc `references/data-contracts.md`.

## 1. Kiến trúc

```
OFFLINE  raw → build_corpus.py → import_sources.py (sources/rights/documents) → chunking (section_v1)
         → [cổng: quyền + review] → Cohere embed-v4.0 (1536) → pgvector → kiểm tra index → eval retrieval

ONLINE   câu hỏi + lịch sử → safety screening → phân loại ý định → router
           ├─ greeting     → trả lời ngắn, không truy xuất
           ├─ info_lookup  → SQL/FTS trên sources (174 nguồn), không embedding
           └─ expert_qa    → xử lý câu hỏi (giữ câu gốc) → dense + FTS → fusion → rerank
                             → evidence validation (sufficient/partial/conflicting/insufficient/blocked)
                             → context builder → LLM → answer validation → phản hồi
```

Trạng thái và thứ tự phase nằm trong `README.md` (Phase 0–7). Làm theo đúng thứ tự; không nhảy phase khi phase trước chưa COMPLETED hoặc đang BLOCKED.

### Trách nhiệm từng thư mục

| Thư mục | Làm gì | Không làm gì |
|---|---|---|
| `app/router/` | Phân loại câu hỏi → 1 trong 4 nhãn; nhận cả vài lượt hội thoại gần nhất | Không truy xuất, không sinh câu trả lời |
| `app/greeting/` | Chào hỏi, cảm ơn, "bạn là ai" | Không trả lời nội dung chuyên môn |
| `app/info_lookup/` | Tra catalog: có nguồn nào về X, nguồn của tổ chức Y | Không embedding |
| `app/expert_qa/` | Điều phối: viết lại câu hỏi → retrieval → ngưỡng bằng chứng → answer | Không gọi thẳng API embedding/LLM |
| `app/safety/` | Phát hiện và trả lời cố định cho tình huống nhạy cảm | Không gọi LLM để "ứng biến" câu trả lời an toàn |
| `app/retrieval/` | Chunking, embedding, vector store, rerank | Không biết gì về router hay prompt trả lời |
| `app/answer/` | Dựng câu trả lời, gắn trích dẫn, kiểm tra trích dẫn có thật trong chunk được truy xuất, định dạng phản hồi | Không truy xuất |
| `app/llm/` | Client duy nhất gọi API sinh văn bản; retry, timeout | Không chứa logic nghiệp vụ |
| `app/ingest/` | Pipeline offline: import catalog (`catalog_import`), đọc Markdown (`markdown_blocks`), khôi phục cấu trúc PDF (`pdf_layout`), chunking (`chunking`), ghi chunk (`chunk_store`), chọn chunk qua cổng + lưu vector (`embed_pipeline`) | Không phục vụ request online |
| `app/rights/` | Thu thập bằng chứng giấy phép từ bản gốc (`license_audit`) | Không bao giờ cấp quyền / ghi `*_allowed` |
| `app/retrieval/embeddings.py` | Client Cohere duy nhất (lô 96, retry có giới hạn, kiểm tra 1536 chiều) | Không log văn bản hay key |
| `app/config.py`, `app/db.py`, `app/migrations.py` | Đường dẫn + biến môi trường; kết nối theo role (owner/ingest/app); logic migration | Không in secret |
| `config/` | Profile chunking, model, ngưỡng, top K, câu trả lời cố định | Không chứa secret |
| `deploy/` | `compose.yml` (PostgreSQL 16 + pgvector 0.8.6, digest cố định), `db/initdb/` tạo role/DB/schema | Không tạo bảng (bảng do `migrations/`) |
| `scripts/` | CLI mỏng gọi vào `app/`: `build_corpus`, `db_migrate`, `db_check`, `import_sources`, `chunk_pilot` | Không chứa logic nghiệp vụ; không bị `app/` import |
| `tests/unit/`, `tests/integration/`, `tests/regression/` | Xem mục 6 | |
| `eval/datasets/`, `eval/reports/` | Bộ câu hỏi chuẩn và kết quả đánh giá | |
| `migrations/` | Thay đổi schema database, đánh số tăng dần | Không sửa migration đã chạy |
| `logs/` | Log runtime (git ignore) | |
| `deploy/` | Docker compose, cấu hình triển khai | |

### Chiều phụ thuộc

`router → {greeting, info_lookup, expert_qa, safety} → {retrieval, answer, llm} → config`

- Các nhánh không import lẫn nhau. Thứ dùng chung đưa xuống `answer/`, `retrieval/` hoặc `llm/`.
- Chỉ `app/llm/` gọi API sinh văn bản; chỉ `app/retrieval/` gọi API embedding/rerank. Nhờ vậy đổi nhà cung cấp chỉ chạm một chỗ, và test chỉ cần mock một chỗ.
- Mọi giá trị có thể thay đổi (tên model, top K, ngưỡng điểm, đường dẫn, câu trả lời cố định) đọc từ `config/`, không viết cứng trong code.

Muốn thêm thư mục cấp cao mới, thư viện mới, hoặc đổi chiều phụ thuộc: hỏi người dùng trước, rồi cập nhật bảng trên và `README.md`.

## 2. Quy tắc dữ liệu

- **`data/raw/` chỉ đọc.** Đây là bản lưu nguồn gốc kèm hash. Không sửa, không xoá, không thêm file bằng tay.
- **`data/corpus/` và `data/catalog/` là sản phẩm sinh ra** từ `scripts/build_corpus.py`. Muốn đổi thì sửa script hoặc raw rồi chạy lại; sau đó chạy `--check`.
- **Nhánh chuyên môn chỉ dùng tier `core` và `gaps`** (73 tài liệu). Tier `metadata_only` và `excluded` không bao giờ được embedding — chúng không có toàn văn hoặc chưa rõ quyền.
- **Index nằm trong PostgreSQL `asd_rag_v2`, schema `asd_rag`** (bảng `chunks`, `chunk_embeddings`, `embedding_profiles`). Phiên bản = `chunking_profile` + `embedding_profiles.profile_code`. Không trộn vector của hai profile; đổi chunker hay model ⇒ profile mới. `data/index/` chỉ giữ tokenizer và cache (git ignore).
- **Embedding đã chốt**: `cohere_existing` = `embed-v4.0`, 1536 chiều, `/v2/embed`, `embedding_types=["float"]`, `search_document` / `search_query`, cosine (xác minh từ `D:\AI4LIFE\ASD_AGENT\rag\retriever.py`). Không cắt/đệm vector; model không trả 1536 ⇒ dừng và báo.
- **Cổng phê duyệt**: cờ `approved_*`, `content_review_status` và các quyền `*_allowed` chỉ role owner sửa được (quyết định của người). NULL = chưa xác minh = không được phép. Chỉ dữ liệu qua `v_embedding_eligible_documents` mới được gửi sang Cohere; chỉ `v_retrieval_ready_chunks` mới tới LLM.
- **Luồng embedding nghiên cứu (migration 006) tách khỏi production.** Vector thử nghiệm nằm ở `research_chunk_embeddings`, chỉ cho chunk trong allowlist của một `research_embedding_authorizations` (scope `research_test`, `production_approval=false`, owner ghi theo yêu cầu chủ dự án). Trigger chặn vector cho chunk không phải ứng viên / sai hash / sai model / sai chiều; ingest không UPDATE/DELETE được; role app không đọc được. Quy trình: `scripts/embedding_preflight.py` → `scripts/embed_research.py authorize` → `run` (dry-run) → `run --execute` → `verify`. Ủy quyền nghiên cứu **không** là quyết định quyền: không bao giờ ghi `*_allowed` hay phê duyệt production từ luồng này. Chunk đã có vector bị `ON DELETE RESTRICT` — chunk lại cần profile mới hoặc dump + xoá có chủ đích.
- **Retrieval nghiên cứu chỉ đọc qua `v_research_retrieval_chunks` bằng role `research_reader`** (migration 007). Không dùng `ingest`/`owner` để truy xuất; không lọc sau LIMIT ở Python. Mỗi profile tối đa 1 authorization hiệu lực (unique index); sửa phạm vi = `scripts/research_authorization_revise.py` (thu hồi cũ + tạo mới, một transaction; `--restore` để hoàn tác) — không xoá vector. Vector mang `authorization_id` **lúc tạo** (provenance); phạm vi truy xuất do authorization **hiện hành** quyết định. Tạo role cần superuser: `deploy/db/initdb/10_research_reader.sh` (owner không có CREATEROLE). Kiểm chứng: `scripts/verify_research_access.py` (`--mutations` chỉ trên DB cô lập).
- **Dense retrieval** (`app/retrieval/dense.py`, profile `config/retrieval_profiles.json` → `dense_baseline_v1`): câu hỏi → `CachedQueryEmbedder` (mặc định OFFLINE; gọi Cohere chỉ khi được phê duyệt, chỉ gửi câu hỏi, cache theo sha256 không lưu text) → `ResearchVectorReader` (role reader, SQL cố định, `<=>` cosine distance) → kiểm provenance từng hàng → fail-closed. Điểm là `cosine_distance` (thấp = gần), không phải xác suất. Metric trên dataset silver luôn báo cận dưới + judged coverage; chunk chưa chấm không bao giờ coi là không liên quan.
- **Nhãn bổ sung cho bộ eval** (T2.3.2): không sửa `retrieval_eval_v1.jsonl`. Nhãn mới vào file mở rộng `eval/datasets/retrieval_eval_v1_candidate_judgments_<ngày>.jsonl`, mỗi dòng pool có đúng 1 dòng với status `judged` / `needs_adjudication` / `excluded` / `unjudged`. Bản merge sinh bằng `scripts/candidate_judgments.py merge`, có tính tất định; kiểm tra bằng `merge --check` và `validate` (14 kiểm tra). Chỉ `judged` được merge; `needs_adjudication` và `unjudged` nằm trong `candidate_chunk_ids`, không bao giờ thành grade 0. Khi so sánh retriever: nhãn mới chỉ đến từ pool dense, nên phải pool và chấm mọi hệ thống ngang nhau.
- **Schema DB chỉ đổi bằng migration mới** (`migrations/NNN_*.sql`, chạy `scripts/db_migrate.py`); không sửa file đã áp dụng. Mỗi migration cần: file rollback `migrations/rollback/NNN_down.sql`; `pg_dump` vào `backups/` trước khi áp dụng; chạy thử apply → `db_check` → rollback → re-apply trên **container tạm cô lập** khôi phục từ backup (`docker run --tmpfs …`, cổng 5439 — cổng 5434 thuộc dự án khác trên máy, không đụng; bind mount dùng `--mount type=bind,source=D:/…`). **Không** dùng `CREATE DATABASE … TEMPLATE asd_rag_v2` trên container thật — ngày 14/11/2026 lệnh này làm backend PostgreSQL thoát bất thường. Thêm kiểm tra cho đối tượng mới vào `scripts/db_check.py`.
- **Quyền: bằng chứng ≠ quyết định.** `rights_assessments` + `eval/reports/license_review_matrix.csv` là bằng chứng (từ giấy phép trong bản gốc / điều khoản nhà cung cấp). `source_rights.*_allowed`, `verified_by`, `verified_at` là quyết định của chủ dự án, ghi bằng role owner. Không suy quyền API từ nhãn giấy phép hay tên tổ chức.
- **Cohere**: key hiện tại là trial (14/11/2026) → dữ liệu chịu Terms of Use, cho phép Cohere dùng input để cải thiện dịch vụ ⇒ tài liệu NC bị chặn gửi Cohere tới khi có production key + opt-out hoặc ZDR. Bằng chứng: `docs/provider_terms/cohere_2026-11-14.md`. Production: `scripts/embed_chunks.py --execute --confirm-rights-approved` (chỉ những gì cổng production cho qua); nghiên cứu: `scripts/embed_research.py` (ở trên). Mặc định luôn là dry-run. Key trial có trần token/phút (~80–150k, quan sát 14/11/2026) → `embed_research.py` giãn nhịp ≤ 90k token / 60 s và ≤ 1.800 input/phút; trần 1.000 request/tháng.
- **Chunk theo mục của bài** (profile `section_v1` trong `config/chunking_profiles.json`, token đếm bằng tokenizer thật của `embed-v4.0`): không vượt heading, bảng là chunk riêng kèm caption + chú thích, overlap chỉ trong cùng mục, references/back matter giữ nhưng `retrieval_eligible=false`, phần thiếu (hình/media) ghi vào `completeness_status` + `missing_context`.
- **`data/curation/`** là lớp hiệu chỉnh có phiên bản đặt lên catalog raw bất biến (hiện có `license_corrections.jsonl`: 35 tài liệu CC BY). Mỗi dòng phải có bằng chứng + SHA-256 file gốc, `permissions_changed=false`; `build_corpus.py` kiểm và áp dụng, `--check` phát hiện bản build cũ. Không bao giờ sửa `data/raw` để "sửa" phân loại.
- **`data/extractions/<source_id>/`** chứa sản phẩm phái sinh từ bản gốc, tên có công cụ + phiên bản (`page_map.pypdf-6.11.0.v1.json`, `tables.pdfplumber-0.11.10.v1.jsonl`, đề xuất trích xuất lại). Không ghi đè cho input khác — tăng phiên bản. Đề xuất trích xuất lại không tự áp vào corpus; áp dụng = phiên bản tài liệu mới, cần người duyệt. `pypdf` ghim `==6.11.0` vì bản đồ trang phải tái tạo đúng từng byte bộ chuyển đổi cũ.
- **Profile `section_v2_1`** (mặc định cho embedding từ 14/11/2026, `features.rules = "v2_1"`): v2 + bản đồ trang đã kiểm chứng cho PDF không có dấu trang; giữ heading lặp thật; vùng "TABLE n", hàng số liệu, mảnh số ngắn, chuỗi ≥ 5 số (hoặc ≥ 4 trên trang có bảng khôi phục) → `table_structure_unrecoverable` / `table_recovered_pending_review`; `/gidNNNNN` → `text_encoding_lost`; không xác định được trang → `page_provenance_incomplete`. Migration 005 cấm ở mức bảng việc bật truy xuất cho các trạng thái này. Danh sách chunk còn nghi ngờ: `eval/reports/section_v2_1_residual_numeric_runs.csv`.
- **Profile `section_v2`** thêm: bộ chuẩn hoá v2, layout pass cho PDF không heading, loại danh sách tham khảo/người đóng góp/mục lục/trang bản quyền theo nội dung, cờ `table_structure_lost`, `unclassified` khi không đủ căn cứ. Mọi thay đổi chunking phải nằm sau cờ trong profile để profile cũ tái tạo y hệt (kiểm bằng hash chunk trong DB).
- Chạy chunking pilot trước khi chạy toàn bộ; báo cáo ở `eval/reports/<ngày>_chunking_pilot_<profile>.{json,md}`. Thay đổi chunker ⇒ chạy `scripts/chunking_regression.py` (so profile cũ ↔ mới trên toàn kho) và đọc danh sách `non_layout_chunks_newly_excluded` để bắt dương tính giả.
- Ký tự `–`, `’`, `×` trong regex là cố ý (khớp văn bản thật) — đã khai báo `allowed-confusables` trong `pyproject.toml`; công cụ Write/Edit tự đổi `\uXXXX` thành ký tự thật, đừng cố escape.
- Không nạp lại nội dung lịch sử từ `D:\AI4LIFE\ASD_AGENT` hay `Carobud_ASD_2026` (bản dịch biên soạn, sách tải lậu, SQL cũ) vào corpus nếu người dùng chưa duyệt rõ ràng.

## 3. Quy tắc nội dung y khoa

Đây là ứng dụng về sức khoẻ trẻ em và chưa nguồn nào được thẩm định lâm sàng, nên sai một câu có thể gây hại thật.

- Câu trả lời chuyên môn chỉ dựa trên chunk được truy xuất. Ý không có nguồn thì bỏ. Trích dẫn nội bộ (chunk_id, điểm) lưu ở `answer_runs`/`retrieval_results`, KHÔNG hiển thị cho người dùng.
- **Định dạng câu trả lời bắt buộc**: A. Câu trả lời trực tiếp → B. Giải thích chi tiết (đoạn/danh sách/bảng) → C. Lưu ý chuyên môn (chỉ khi cần) → D. **Nguồn**: chỉ tên tài liệu hoặc link, không trích nguyên văn, không mã chunk, không điểm.
- Không đủ bằng chứng ⇒ dùng đúng câu: "Kho tài liệu hiện tại chưa có đủ bằng chứng để đưa ra câu trả lời chính xác cho nội dung này." Không để LLM tự lấp chỗ trống. Không dùng một ngưỡng similarity duy nhất thay cho evidence validation.
- Không chẩn đoán cá nhân, không đưa liều thuốc, không thay thế bác sĩ. Các yêu cầu này đi nhánh `safety`.
- Khi dựa vào tier `gaps`, ghi chú nguồn thiếu hình/bảng. Nguồn có `text_fidelity_warning` (hiện là `ASD-CSV-077`, `NIH-NIMH-CHILDREN`) xếp sau.
- Giữ giới hạn độ tuổi của nguồn (`applicability_0_18_years`, `limits`): nghiên cứu trên người lớn không được trình bày như kết luận cho trẻ.
- Trả lời người dùng bằng tiếng Việt. Giữ câu hỏi gốc; truy vấn tiếng Việt / dịch sang tiếng Anh / kết hợp là các phương án phải benchmark, không mặc định dịch.
- Corpus có nội dung về liều thuốc (ví dụ bảng liều kháng histamin, melatonin trong `ASD-OA-PMC7407189`): truy xuất được không có nghĩa là được đưa liều cho người dùng.
- 48/73 tài liệu mang nhãn `verified_noncommercial_research` (chỉ 13 có giấy phép NC thật; 35 là CC BY nhưng người rà catalog xếp vào phi thương mại). `commercial_use_allowed` để NULL cho tới khi người dùng quyết định. Nhãn phi thương mại không suy ra được quyền gửi sang API bên thứ ba.

## 4. Clean code

- Python 3.12, khai báo phụ thuộc trong `pyproject.toml`. Type hint cho mọi hàm public.
- Dữ liệu đi qua ranh giới module bằng kiểu rõ ràng (`dataclass` hoặc pydantic), không truyền dict tuỳ ý. Hợp đồng dữ liệu ở `references/data-contracts.md`.
- Hàm nhỏ, một việc. Logic thuần (chunking, chấm điểm, dựng trích dẫn) tách khỏi I/O và gọi API để test được không cần mạng.
- Tên biến, hàm, file bằng tiếng Anh. Câu chữ hiển thị cho người dùng (tiếng Việt) và prompt nằm trong `config/` hoặc file prompt riêng, không rải trong code.
- Dùng `logging`, không `print` trong `app/`. Lỗi rõ ràng: bắt lỗi ở biên (API, I/O) và báo nguyên nhân, không nuốt lỗi bằng `except: pass`.
- Không để code chết, code comment-out, file nháp, `utils.py` ôm đồm. Không trừu tượng hoá trước khi có ít nhất hai chỗ dùng thật.
- Comment giải thích *tại sao*, không lặp lại *cái gì*.
- Định dạng và lint bằng `ruff`.

## 5. Bảo mật

- Key chỉ đọc từ biến môi trường (`.env`, đã git ignore). Chỉ commit `.env.example` với giá trị trống hoặc minh hoạ.
- Không ghi key ra log, lỗi, báo cáo eval hay output terminal. Khi cần xem `.env`, chỉ xem tên biến (che giá trị).
- Log không chứa nội dung hội thoại đầy đủ của người dùng ở mức INFO; nếu cần debug, che thông tin cá nhân (tên trẻ, số điện thoại, địa chỉ).
- `eval/datasets/` không chứa dữ liệu người dùng thật.
- Database chỉ bind `127.0.0.1` khi chạy local; mật khẩu nằm trong `.env`.

## 6. Kiểm thử và đánh giá

- `tests/unit/`: logic thuần, mock mọi lời gọi API. Chạy nhanh, không cần key.
- `tests/integration/`: gọi API hoặc database thật; đánh dấu `@pytest.mark.integration` để mặc định bỏ qua.
- `tests/regression/`: câu hỏi từng trả lời sai → cố định kết quả mong đợi để không tái phát.
- `eval/datasets/<tên>_v<N>.jsonl`: bộ câu hỏi chuẩn, không sửa phiên bản cũ — tạo phiên bản mới.
- `eval/reports/<YYYY-MM-DD>_<index_version>_<dataset>.json`: kết quả kèm config đã dùng, để so sánh giữa các lần.

## 7. Quy trình cho mỗi thay đổi

1. Xác định thay đổi thuộc thư mục nào theo bảng ở mục 1. Không rõ ⇒ hỏi.
2. Làm từng bước nhỏ, chạy được ngay. Một bước = một mục đích.
3. Kiểm tra trước khi báo xong (dùng `.venv`):
   - `python -B scripts/build_corpus.py --check` (nếu chạm dữ liệu)
   - `.venv/Scripts/ruff check .`
   - `.venv/Scripts/python -m pytest` (unit) và `.venv/Scripts/python -m pytest -m integration` (đọc DB thật, chỉ đọc)
   - Đổi chunker ⇒ kiểm mọi profile đã lưu vẫn tái tạo y hệt DB (hash từng chunk), không chỉ profile mới
   - `.venv/Scripts/python -B scripts/db_check.py` (nếu chạm DB)
4. Cập nhật `README.md` (bảng trạng thái phase) nếu đổi cấu trúc, lệnh chạy hoặc trạng thái dữ liệu.
5. Báo cáo không ghi đè báo cáo cũ: nếu trùng ngày, thêm hậu tố (`…_2026-11-14_phase5.md`). Báo cáo sau mỗi phase gồm: mục tiêu, trạng thái ban đầu, file đã kiểm tra, file tạo/sửa, bảng DB thay đổi, lệnh đã chạy, kết quả kiểm tra, số liệu thực tế, lỗi/rủi ro, việc tiếp theo. Gắn nhãn COMPLETED (đã chạy và xác minh) / PARTIAL / BLOCKED / NOT STARTED. Viết code chưa chạy thì không gọi là hoàn thành.

## 8. Quyết định

**Đã chốt (master prompt 14/11/2026):** PostgreSQL mới `asd_rag_v2`, schema `asd_rag`, pgvector, role owner/app/ingest; embedding `embed-v4.0` 1536 chiều cosine; hybrid retrieval (dense + FTS + fusion + Cohere Rerank); logging chi tiết nhưng không lưu nguyên văn câu hỏi; chunking pilot 5–10 tài liệu trước khi chạy toàn bộ.

**Chưa chốt — không tự chọn, hỏi người dùng rồi ghi vào `config/` và cập nhật mục này:**
- Quyền xử lý của từng nguồn: archive, text mining, chunking, embedding, gửi Cohere, gửi LLM ngoài, thương mại (chặn Phase 4). Bằng chứng sẵn trong `eval/reports/license_audit_2026-11-14.md`.
- Giữ hay bỏ chính sách phi thương mại cho 35 tài liệu CC BY; loại key Cohere (trial / production + opt-out / ZDR).
- Áp dụng các đề xuất trích xuất lại (ô `<break/>` của ASD-CSV-077, 8 trang pdfium của WHO-CST-PARTICIPANTS) và duyệt các bảng PDF `recovered_pending_human_review`; gỡ cách ly 2 tài liệu.
- `project_usage_policy` (có giữ "chỉ phi thương mại" cho cả kho hay không).
- Duyệt nội dung tài liệu (`content_review_status`), và xử lý 2 tài liệu cách ly `ASD-CSV-077`, `NIH-NIMH-CHILDREN`.
- Model sinh câu trả lời; model rerank cụ thể; framework API/giao diện.
- Fusion (RRF hay khác), top K, ngưỡng — chốt sau benchmark.
