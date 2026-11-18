# Phase 6.2 – T2.3.2: Pre-annotation Audit — 2026-11-14

**Kết quả: không có sai lệch** giữa báo cáo T2.3.1, các file CSV/JSON, dataset và database. Annotation được phép tiếp tục.

Mọi truy vấn DB chạy bằng `asd_rag_v2_research_reader` qua `asd_rag.v_research_retrieval_chunks`, chế độ chỉ đọc. Không dùng owner hay ingest. Không gọi API.

## 1. File đã đọc
- Báo cáo T2.3.1:
  - `phase_6_2_t2_3_1_dense_retrieval_report_2026-11-14.md`
  - `phase_6_2_t2_3_1_preimplementation_review_2026-11-14.md`
  - `…_dense_retrieval_metrics_2026-11-14.json` và bản `_r2`
  - `…_candidate_pool_expansion_2026-11-14.csv` và bản `_r2`
- Dataset:
  - `eval/datasets/retrieval_eval_v1.jsonl`, `_schema.json`, `_annotation_guidelines.md`, `_annotation_status.csv`
- Báo cáo T2.0, T2.1, T2.2
- `docs/research_retrieval_access.md`
- Manifest:
  - `research_authorization_d1_exclusions_2026-11-14.csv`
  - `research_authorization_allowlist_rev_d1_2026-11-14.csv`
  - `embedding_manifest.csv`

## 2. Kết quả kiểm tra
| Kiểm tra | Giá trị thực tế | Khớp báo cáo |
|---|---|---|
| SHA-256 pool r1 = r2 | `19c337b7…` = `19c337b7…` | ✔ |
| Cột của pool | `question_id`, `question_group`, `chunk_id`, `source_id`, `rank`, `cosine_distance`, `cosine_similarity`, `current_annotation_status`, `suggested_review_priority` | ✔ |
| Tổng số ứng viên | **1.103** | ✔ |
| Theo ưu tiên | high **246** · medium 260 · low 597 | ✔ |
| Trạng thái | 1.103 `unjudged` | ✔ |
| Số câu hỏi có ứng viên / có ứng viên high | 66 / 66 (1–10 dòng high mỗi câu) | — |
| Chunk khác nhau (toàn pool / nhóm high) | 696 / 201 | — |
| Cặp (câu hỏi, chunk) trùng | 0 | ✔ |
| Dòng đã có nhãn cho chính câu hỏi đó | **0** (không có nguy cơ ghi đè nhãn cũ) | ✔ |
| Dòng có chunk đã chấm cho câu **khác** | 175. Vẫn là `unjudged` cho câu này; một nhãn không được dùng cho câu khác | — |
| Thuộc 47 chunk D-1 | **0** | ✔ |
| Có trong `embedding_manifest.csv` / allowlist authorization 2 | 1.103 / 1.103 | ✔ |
| Hiển thị trong view (reader) lúc audit | 1.103; `authorization_id` = {2} | ✔ |
| `source_id` trong CSV = view | 1.103 / 1.103 | ✔ |
| `content_sha256` trong view = manifest | 1.103 / 1.103 (nội dung không đổi kể từ khi embed) | ✔ |
| Có trang hoặc khoảng ký tự | 1.103 / 1.103 | ✔ |
| Dataset gốc | SHA `7704bb51…`, 66 câu | ✔ (không đổi từ T1) |
| Nhóm câu hỏi của 246 dòng high | answerable 175 · unanswerable 20 · conflicting 19 · refusal 18 · partial pool 9 · out-of-scope 5 | — |

## 3. Quyết định trước annotation
- Đơn vị chấm là **cặp (câu hỏi, chunk)**. Nhãn của một chunk cho câu hỏi khác không được tái sử dụng.
- **q062** (thời tiết, out of scope): 5 ứng viên được đánh dấu `excluded` (câu hỏi không có mục tiêu bằng chứng), không chấm grade.
- **Đọc nội dung:** lấy qua view bằng role reader và lưu snapshot tạm, kèm `content_sha256` để đối chiếu. Mỗi nhãn ghi lại hash nội dung đã đọc.
- **Thứ tự chấm:** 246 high → q033/q054 → câu nhiều nguồn/nhiều chunk → chủ đề yếu (AAC, sensory, parent-mediated, tuổi dậy thì) → phần còn lại nếu chất lượng cho phép.
