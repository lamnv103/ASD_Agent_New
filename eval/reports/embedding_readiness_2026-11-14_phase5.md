# Embedding readiness — 2026-11-14 (Phase 5, Task E)

**Trạng thái: COMPLETED** (kiểm tra tĩnh/local + dry-run). Embedding thật: **BLOCKED** (quyền + điều khoản nhà cung cấp). Không gọi Embed API với văn bản; không có lời gọi Cohere nào trong Phase 5.

## 1. Cấu hình
| Kiểm tra | Kết quả |
|---|---|
| Model | `embed-v4.0` (cấu hình `cohere_existing` của dự án cũ) |
| Dimension | 1536 = cột `chunk_embeddings.embedding vector(1536)` |
| Input type | `search_document` / `search_query` |
| Similarity | cosine; chưa có index ANN (exact search là baseline) |
| Chunking profile của embedding | đổi `section_v2` → **`section_v2_1`** (`config/embedding_profiles.json`) |
| Tương thích (dry-run) | `column_matches_profile = true`, `profile_matches_verified_config = true` |
| Key | có trong `.env`, chỉ đọc bằng biến môi trường; key hiện tại là **trial** (bằng chứng: `docs/provider_terms/cohere_2026-11-14.md`) |
| Client | lô 96, retry giới hạn, không lộ key, kiểm tra 1536 chiều — 8 unit test với transport giả |

## 2. Ma trận ứng viên (bản nháp, NOT_APPROVED) — [embedding_candidate_matrix.csv](embedding_candidate_matrix.csv) (SHA-256 bdea5b9b…)
Mỗi dòng (174 nguồn) có `approval_status = NOT_APPROVED`. Không có allowlist chính thức.

| Danh mục | Số nguồn | Ghi chú |
|---|---:|---|
| Đủ điều kiện **kỹ thuật** (toàn văn, không cách ly, có chunk truy xuất được, provenance đủ) | **71** | 2.435 chunk, ~762.6k token |
| — trong đó Cohere `blocked` (giấy phép NC + trial key) | 13 | 10 CC BY-NC + 3 CC BY-NC-SA |
| — trong đó Cohere `pending_decision` | 58 | 35 CC BY + 23 public domain |
| Thiếu quyền (mọi `*_allowed` NULL) | 73 | tất cả tài liệu toàn văn |
| Cách ly | 2 | ASD-CSV-077, NIH-NIMH-CHILDREN |
| Thiếu provenance | 0 | PDF: bản đồ trang đã kiểm chứng; HTML/XML: offset ký tự |
| Cần chuyên gia thẩm định | 73 | `clinical_reviewed = false` cho tất cả |
| Chỉ truy xuất metadata | 88 | `metadata_only` |
| Không dùng trả lời chuyên môn | 13 | `excluded` |
| Bằng chứng giấy phép chỉ ở cấp chính sách cơ quan | 18 | ghi trong cột `notes` |

## 3. Dry-run (đã chạy) — `python -B scripts/embed_chunks.py [--what-if]`
- Qua cổng `v_embedding_eligible_documents`: **0 tài liệu, 0 chunk**.
- 73 tài liệu bị chặn: `approved_for_embedding=false` 73; `archive/text_mining/chunking/embedding/cohere_processing_allowed = NULL` 73; `content_review_status=pending` 71; `quarantined` 2.
- Ước tính nếu được duyệt (v2_1): CC BY 35 tài liệu ~17 lời gọi; public domain 23 ~3; NC 13 ~7 (đang blocked) — tổng ≈ 27 lời gọi (lô 96).

## 4. Quyết định cần (không thể tự làm)
1. Ghi quyết định quyền bằng role owner cho từng nguồn (`*_allowed`, `verified_by`, `verified_at`).
2. Phương án Cohere: production key + opt-out huấn luyện / ZDR / chỉ 58 tài liệu không-NC / embedding local cho NC.
3. Duyệt nội dung (`content_review_status='approved'`, `approved_for_embedding`).
Sau 1–3: `python -B scripts/embed_chunks.py --execute --confirm-rights-approved` (chỉ embed những gì cổng DB cho qua).

## 5. Kết luận
Sẵn sàng về kỹ thuật và có thể kiểm toán; **0 tài liệu được phép** gửi đi.
