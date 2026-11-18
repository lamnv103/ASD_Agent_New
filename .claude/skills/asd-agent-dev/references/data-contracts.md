# Hợp đồng dữ liệu

Định dạng chung giữa các module. Đổi một hợp đồng ⇒ cập nhật file này và mọi nơi đọc/ghi nó trong cùng một thay đổi. Schema DB là nguồn sự thật cho dữ liệu trong PostgreSQL: `migrations/001_core_schema.sql`.

Mục lục: 1. corpus manifest · 2. catalog · 3. bảng DB · 4. chunk · 5. eval dataset · 6. eval report

## 1. `data/corpus/manifest.jsonl` — sinh bởi `scripts/build_corpus.py`

Một dòng / tài liệu (73). Trường chính:

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `source_id` | str | khoá chính, ví dụ `ASD-CSV-002` |
| `tier` | `"core"` \| `"gaps"` | |
| `status` | str | trạng thái gốc trong catalog raw |
| `title`, `authors`, `organization`, `publication_date` | | `authors` là list |
| `source_type`, `language`, `topics` | | `topics` là list |
| `source_url`, `full_text_url` | str \| null | |
| `license`, `rights_status`, `rights_conditions` | | nhãn catalog, KHÔNG phải quyền xử lý API |
| `applicability_0_18_years`, `original_age_scope`, `limits` | | giới hạn độ tuổi / diễn giải |
| `conversion_gaps` | dict[str, int] | loại phần thiếu → số lượng |
| `text_fidelity_warning` | bool | |
| `path`, `sha256`, `characters` | | file trong `data/corpus/` |
| `raw_document_path`, `raw_original_path`, `version` | | truy ngược về `data/raw/` |

## 2. `data/catalog/sources.jsonl`

Một dòng / nguồn (174): trường mô tả như manifest, thêm `tier` (`core` | `gaps` | `metadata_only` | `excluded`), `in_corpus`, `corpus_path`, `audit_conclusion`.

## 3. Bảng DB (schema `asd_rag`)

| Bảng | Khoá | Ghi bởi | Ghi chú |
|---|---|---|---|
| `sources` | `source_id` | ingest | `catalog_payload` = bản ghi raw đầy đủ |
| `source_rights` | `source_id` | ingest (mô tả), owner (quyền `*_allowed`) | NULL = chưa xác minh = không được phép |
| `documents` | `document_id` = `<source_id>@<version>` | ingest (mô tả), owner (review/approve) | một bản `is_current` / nguồn |
| `chunks` | `chunk_id` = `<document_id>#<profile>#<NNNN>` | ingest | `content_tsv` sinh tự động (FTS tiếng Anh) |
| `embedding_profiles` | `profile_id` | ingest (tạo), owner (kích hoạt) | `vector_dimension` = 1536 |
| `chunk_embeddings` | `(chunk_id, profile_id)` | ingest | `embedding_input_hash` để không gọi lại API |
| `ingestion_runs`, `ingestion_run_documents` | | ingest | audit từng lần chạy |
| `retrieval_logs`, `retrieval_results`, `answer_runs` | | app | chỉ hash câu hỏi, không lưu nguyên văn |

## 4. Chunk (profile `section_v1`)

`content` là văn bản đã chuẩn hoá (bỏ thẻ HTML/JATS, MathML → chữ, bảng → dòng `a | b | c`). `char_start`/`char_end` trỏ vào file trong `data/corpus/` (phần nội dung mới, không gồm overlap). `section_path` là danh sách heading (không gồm tiêu đề bài); `section_heading` = nối bằng `" > "`. `section_type` ∈ abstract, abstract_inferred, overview_inferred, introduction, methods, results, discussion, limitations, conclusion, body, floating_table, references, back_matter. `completeness_status` ∈ complete, document_has_gaps, references_missing_component.

Văn bản gửi embedding (Phase 4, chốt khi viết embedder): tiêu đề tài liệu + `section_heading` + `content`; băm thành `embedding_input_hash`.

## 5. `eval/datasets/<tên>_v<N>.jsonl`

```json
{"id": "q001", "question": "Trẻ tự kỷ hay khó ngủ thì có những cách hỗ trợ nào?", "expected_route": "expert_qa", "relevant_source_ids": ["ASD-OA-PMC7407189", "ASD-OA-PMC4271434"], "must_refuse": false, "notes": ""}
```

`expected_route` ∈ `greeting` | `info_lookup` | `expert_qa` | `safety`. `must_refuse=true` cho câu không có nguồn hoặc đòi chẩn đoán/kê đơn. Bộ câu hỏi chuẩn phải được chuyên gia ASD duyệt; chưa duyệt thì ghi rõ trong `notes`.

## 6. `eval/reports/<YYYY-MM-DD>_<nội dung>.{json,md}`

Ghi cấu hình đã dùng (profile chunking/embedding, top K, fusion, model) và chỉ số theo từng lớp (source, chunking, retrieval, answer, safety). Không chứa API key, không chứa câu hỏi thật của người dùng.
