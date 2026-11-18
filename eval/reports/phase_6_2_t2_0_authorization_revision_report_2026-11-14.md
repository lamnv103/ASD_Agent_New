# Phase 6.2 – T2.0: Research Authorization Revision (D-1) — 2026-11-14

**Trạng thái: COMPLETED.** 47 chunk danh mục tài liệu tham khảo đã được loại khỏi phạm vi truy xuất bằng authorization 2. Authorization 1 bị thu hồi nhưng vẫn giữ nguyên để truy vết. Không xoá vector, không sửa chunk, không re-embed, không gọi API.

## 1. Mục tiêu và phạm vi
- **Mục tiêu:** loại 47 chunk chỉ chứa danh mục tham khảo (phát hiện ở T1) khỏi phạm vi retrieval nghiên cứu.
- **Phạm vi:** tạo authorization mới (D-1) theo cơ chế sẵn có của migration 006 (`revoked_at` + bảng allowlist).
- **Ngoài phạm vi:**
  - sửa chunker (bộ phát hiện References);
  - re-chunk;
  - sửa nhãn trong dataset.

## 2. File đã đọc
- `retrieval_architecture_audit_2026-11-14.md`
- `phase_6_2_t0_technical_decisions_2026-11-14.md`
- `phase_6_2_t1_*`
- `migrations/006_research_embedding_track.sql`
- `eval/reports/embedding_manifest.csv`
- Nội dung chunk (snapshot chỉ đọc và DB chỉ đọc)
- `eval/datasets/retrieval_eval_v1.jsonl`

## 3. Xác định 47 chunk (không suy từ vị trí)
1. **Theo nội dung và heading:** trong tập đã embed, đúng 47 chunk có heading là danh mục tham khảo:
   - ASD-CSV-017: "*Indicates studies included in the systematic review", **27 chunk** (#0057–#0082, #0084);
   - ASD-CSV-018: "*References marked with an asterisk indicate…", **20 chunk** (#0041–#0060).

   Phép quét nội dung độc lập ở T1 (mật độ DOI) cho ra **đúng cùng tập này**.
2. **Chỉ số nội dung từng chunk:**
   - Đo: số năm xuất bản trên 1.000 ký tự, số tên tạp chí/nhà xuất bản trên 1.000 ký tự, số DOI, và dấu hiệu văn xuôi kiến thức ("we found", "results showed", "in conclusion", "limitations", …).
   - 43 chunk đạt mọi ngưỡng.
   - 4 chunk bị đánh dấu xem lại (ASD-CSV-017 #0057, #0063, #0067, #0069).
3. **Đọc toàn văn 4 chunk đó:** cả 4 chỉ gồm các mục tham khảo. "Dấu hiệu văn xuôi" thực ra nằm trong tiêu đề bài báo, ví dụ "…Implications for urban education". Với 43 chunk còn lại, đoạn đầu và đoạn cuối của từng chunk đều đã được đọc.
4. **Ranh giới:**
   - Phía trước danh mục là chunk "Conflict of interest" (`back_matter`, không embed). Phía sau là hết tài liệu.
   - ASD-CSV-017 #0083 cùng danh mục nhưng đã được chunker gắn `references_detected` nên không embed. Đây là bằng chứng bộ phát hiện References không ổn định (đề xuất ở mục 9).
5. **Chunk trộn kiến thức và tham khảo:** **0**. **Chunk chưa xác định chắc chắn:** **0**.

## 4. Manifest
- **[research_authorization_d1_exclusions_2026-11-14.csv](research_authorization_d1_exclusions_2026-11-14.csv)** (47 dòng, SHA-256 `d3bb36fc…0ed8`).
  - Các cột: `authorization_version`, `previous_authorization_id`, `chunk_id`, `document_id`, `source_id`, `chunk_index`, `content_sha256`, `section_type`, `section_heading`, `exclusion_reason`, `previous_authorization_status`, `new_authorization_status`, `verification_status`, `doi_count`, `year_count`, `char_count`, `vector_retained`, `chunk_content_modified`.
  - `verification_status`: `verified_full_read` 4 chunk, `verified_content_metrics_and_excerpts` 43 chunk.
- **[research_authorization_allowlist_rev_d1_2026-11-14.csv](research_authorization_allowlist_rev_d1_2026-11-14.csv)**: allowlist mới, 2.291 chunk. SHA-256 `59c3d6cf…8919`, đồng thời là `manifest_sha256` của authorization 2.

## 5. Áp dụng
- **Script:** `scripts/research_authorization_revise.py` (role owner). Mặc định chạy dry-run; khi chạy thật, mọi thao tác nằm trong một transaction.
- **Dry-run trước khi áp dụng:**
  - 47/47 chunk khớp allowlist của authorization 1, cả `chunk_id`, `content_sha256` và `source_id`;
  - mọi chunk của allowlist mới đều có vector.
- **Thao tác:**
  1. `UPDATE research_embedding_authorizations SET revoked_at = now() WHERE authorization_id = 1`. Hàng được giữ, chỉ đổi `revoked_at`.
  2. `INSERT` authorization 2:
     - `scope = research_test`, `production_approval = false`;
     - `notes` ghi `revision_of_authorization_id = 1`, quyết định D-1, tên và SHA-256 của manifest loại trừ.
  3. Thêm 71 hàng nguồn (giữ nguyên nhóm A/B/C) và 2.291 chunk vào allowlist.
- **Thứ tự:** chạy trên bản sao cô lập trước (port 5439, khôi phục từ backup), sau đó mới chạy trên DB thật.

## 6. Trước / sau
| Chỉ số | Trước | Sau |
|---|---:|---:|
| Chunk trong allowlist đang hiệu lực | 2.338 (auth 1) | **2.291** (auth 2) |
| Chunk bị loại | — | **47** |
| Chunk truy xuất được (qua view 007) | — (chưa có view) | **2.291** |
| Research vectors | 2.338 | **2.338** (không xoá) |
| Nguồn trong authorization | 71 | 71 |
| Nội dung chunk (md5 tổng hợp) | `e40dc061…` | `e40dc061…` (không đổi) |
| Vector (md5 tổng hợp chunk + hash + norm + vector + authorization gốc) | `1b1c15ce…` | `1b1c15ce…` (không đổi) |
| Authorization | 1 hiệu lực | 1 đã thu hồi (giữ nguyên), 2 hiệu lực |

Mỗi vector vẫn mang `authorization_id = 1`. Đó là authorization **khi tạo** vector, tức là provenance. Còn authorization **khi truy xuất** là authorization đang hiệu lực.

Vì vậy `db_check` và integration test đổi kiểm tra "vector phải là ứng viên của authorization hiện hành" thành hai kiểm tra riêng:
- **khi tạo:** vector nằm trong allowlist của authorization đã tạo ra nó, với cùng hash nội dung;
- **khi truy xuất:** view chỉ trả các chunk thuộc allowlist đang hiệu lực.

## 7. Ảnh hưởng tới dataset đánh giá
- Dataset không bị sửa.
- 3 nhãn chạm vào chunk D-1, đều là grade 0 (hard negative):
  - q016: ASD-CSV-017 #0068, #0070;
  - q023: ASD-CSV-017 #0075.
- Không có chunk relevant nào bị loại.
- Validator vẫn PASS (dataset SHA `7704bb51…`), vì validator đối chiếu với `embedding_manifest.csv`, tức tập đã embed. Ở T2.3, các nhãn này cần được coi là "không truy xuất được" khi tính metric.

## 8. Khôi phục authorization cũ
Chạy:
```
python -B scripts/research_authorization_revise.py --restore --revoke 2 --reactivate 1
```
- Lệnh thu hồi authorization 2 và bỏ `revoked_at` của authorization 1, trong một transaction.
- **Đã kiểm thử trên bản sao:** khôi phục → so fingerprint → áp dụng lại, đều đạt (xem báo cáo T2.1).

## 9. Chưa làm và đề xuất
- **Bộ phát hiện References của chunker** bỏ sót danh mục có heading dạng "*Indicates studies…" / "*References marked with an asterisk…". Nên sửa sau cờ của một profile chunk mới; không sửa `section_v2_1`.
- **`scripts/embed_research.py` chưa được cập nhật cho việc sửa đổi authorization** (ngoài phạm vi, chưa chạy lại):
  - `run` sẽ dừng an toàn ở preflight, vì `embedding_manifest.csv` không còn khớp `manifest_sha256` của authorization 2. Không có lời gọi API nào xảy ra.
  - `verify` sẽ báo sai ở kiểm tra "every vector is an authorized current candidate", vì kiểm tra này còn dùng ngữ nghĩa cũ.
  - Đề xuất: cập nhật theo ngữ nghĩa khi tạo / khi truy xuất như đã làm cho `db_check`.
- Có thể có các danh mục tham khảo khác lọt vào tập embed mà không theo hai mẫu heading này. Phép quét T1 (mật độ DOI) không tìm thấy, nhưng chưa có kiểm tra toàn diện.

## 10. Kết luận
D-1 hoàn thành và có thể truy vết: có manifest, allowlist và hai hàng authorization với SHA-256. Có thể khôi phục. Đạt T2-AC01, T2-AC02, T2-AC03.
