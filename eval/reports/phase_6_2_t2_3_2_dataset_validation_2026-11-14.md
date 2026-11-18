# Phase 6.2 – T2.3.2: Dataset Validation — 2026-11-14 (chạy 15/11/2026)

**Kết quả: hợp lệ.** Validator báo 0 lỗi, 0 cảnh báo. File merge được tạo lại giống hệt từng byte từ file gốc cộng file nhãn. File gốc không thay đổi.

**Kiểm tra DB (chạy sau khi bật Docker, 15/11/2026):** `db_check` ok (13/13 nhóm kiểm tra), `verify_research_access` live không mutation **74/74** (quyền 45/45, authorization 13/13, rò rỉ 16/16). Fingerprint DB (16 mục) **giống hệt cuối T2.3.1**, tức T2.3.2 không thay đổi gì trong DB. Ban đầu hai kiểm tra này chưa chạy được vì Docker Desktop tắt.

Kết quả máy đọc: `phase_6_2_t2_3_2_dataset_validation_2026-11-14.json`.

## 1. File và fingerprint
| File | SHA-256 | Ghi chú |
|---|---|---|
| `eval/datasets/retrieval_eval_v1.jsonl` | `7704bb51…4c2b` | **Gốc, không đổi** (trước = sau) |
| `backups/datasets/retrieval_eval_v1_pre_t2_3_2_2026-11-15.jsonl` | `7704bb51…4c2b` | Bản sao lưu trước annotation |
| `eval/datasets/retrieval_eval_v1_schema.json` | `18517b92…5efe` | Không đổi |
| `eval/reports/phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv` | `19c337b7…79ff` | Pool T2.3.1, không đổi |
| `eval/datasets/retrieval_eval_v1_candidate_judgments_2026-11-14.jsonl` | `de526dd0…563f` | **Mới:** 1.103 dòng, mỗi dòng pool có đúng một dòng |
| `eval/datasets/retrieval_eval_v1_candidate_judgments_schema.json` | `aa255539…4145` | **Mới** |
| `eval/datasets/retrieval_eval_v1_merged_2026-11-14.jsonl` | `6bd3ad78…e7ab` | **Mới:** gốc + nhãn `judged` |
| `scripts/candidate_judgments.py` | `b2c03714…f8ec` | **Mới:** merge và validator |
| `tests/unit/test_candidate_judgments.py` | `0cd5a1cf…f36e` | **Mới:** 25 test |

Phiên bản cố định trong mỗi dòng nhãn:
- Corpus: `section_v2_1` / `cohere_embed_v4_1536_v1`, manifest `542cce21…`.
- Authorization: `authorization_id` 2, allowlist `research_authorization_allowlist_rev_d1_2026-11-14.csv` (`59c3d6cf…`).
- Dataset gốc: `7704bb51…`.

## 2. Quy tắc merge (tất định)
- Nhãn cũ giữ nguyên và đứng trước. Chỉ dòng `status = judged` được thêm vào `judgments`.
- `relevant_chunk_ids`, `relevance_grade`, `relevant_document_ids`, `expected_sources` được tính lại từ `judgments`, với quy tắc grade ≥ 2 như schema v1.
- Dòng `unjudged` và `needs_adjudication` được đưa vào `candidate_chunk_ids`. **Không bao giờ thành grade 0.**
- Dòng `excluded` (q062) không là nhãn, cũng không là ứng viên.
- Một câu có ứng viên chưa chấm thì `annotation_completeness` = `partial`.
- `search_log`, `annotation_method` và `annotation_notes` được ghi thêm nguồn và hash của file nhãn.
- Nếu một chunk đã có nhãn cũ cho cùng câu hỏi thì merge **dừng với lỗi**, không ghi đè.

Lệnh:
```
python -B scripts/candidate_judgments.py merge --check   # tạo lại, so byte, không ghi
python -B scripts/candidate_judgments.py validate        # 14 kiểm tra + validator v1 cho file gốc và file merge
```

## 3. Mười bốn kiểm tra theo yêu cầu
| # | Kiểm tra | Cách kiểm | Kết quả |
|---|---|---|---|
| 1 | Schema | Trường bắt buộc, không có trường lạ (`*_schema.json`) | 1.103/1.103 đạt |
| 2 | Question ID tồn tại | So với 66 câu của dataset gốc | Đạt |
| 3 | Chunk ID tồn tại | So với `embedding_manifest.csv` | Đạt |
| 4 | Grade hợp lệ | judged/needs_adjudication ∈ {−1..3} và `evidence_class` khớp grade; unjudged/excluded **không có** grade | Đạt |
| 5 | Status hợp lệ | ∈ {judged, needs_adjudication, excluded, unjudged} | Đạt: 303 / 4 / 5 / 791 |
| 6 | Không trùng nhãn | Duy nhất theo (câu hỏi, chunk, annotator) và theo cặp (câu hỏi, chunk) | 0 trùng |
| 7 | Không mất nhãn cũ | 435 nhãn gốc đứng đầu, giống hệt từng trường; không ứng viên gốc nào bị bỏ | Đạt (435 → 738, chỉ thêm) |
| 8 | Unjudged không thành irrelevant | Không chunk unjudged/needs_adjudication/excluded nào xuất hiện trong `judgments` hay `relevance_grade` | Đạt |
| 9 | Không đưa lại chunk bị loại | So với 47 chunk D-1 (`…_d1_exclusions_…csv`) | 0 |
| 10 | Provenance | annotator, thời điểm, protocol; rank/priority khớp file pool; corpus/authorization pin | Đạt |
| 11 | Không lệch source/doc/chunk | `document_id`, `source_id`, `content_sha256` = manifest | Đạt |
| 12 | Có rationale | judged, needs_adjudication, excluded (thêm `exclusion_reason`) | Đạt |
| 13 | Trong authorization hiện hành | Chunk thuộc allowlist authorization 2; pin `authorization_id` = 2 | 1.103/1.103 |
| 14 | Merge tái lập được | `merge(gốc, nhãn)` so byte với file merge | Giống hệt (`6bd3ad78…`) |

Mỗi kiểm tra có ít nhất một test âm trong `tests/unit/test_candidate_judgments.py`, ví dụ sửa hash, hạ nhãn cũ, chèn grade 0 cho chunk chưa chấm, chunk D-1, chunk ngoài allowlist, hay file merge bị sửa tay.

## 4. Validator v1 (`validate_retrieval_eval.py`)
| | File gốc | File merge |
|---|---|---|
| Lỗi / cảnh báo | 0 / 0 | 0 / 0 |
| Số nhãn | 435 | 738 |
| Grade ≥ 2 (lượt) | 300 | 395 |
| Chunk relevant khác nhau | 238 | 315 |
| Chunk đã chấm khác nhau | 339 | 555 |
| Số nguồn trong `expected_sources` | 60 | 63 |
| Phân bố grade (−1/0/1/2/3) | 5 / 64 / 66 / 186 / 114 | 5 / 184 / 154 / 249 / 146 |
| `annotation_completeness = partial` | 4 | 63 |

## 5. Kiểm tra code
| Lệnh | Kết quả |
|---|---|
| `ruff check .` | Đạt |
| `pytest` (unit) | 169 passed, 33 deselected (test cần DB, như các phase trước); có 25 test mới |
| `db_check.py` | ok, 13/13 nhóm kiểm tra |
| `verify_research_access.py` (live, không mutation) | 74/74; fingerprint DB = cuối T2.3.1 |

Không có thao tác DB nào trong T2.3.2. Nội dung chunk được đọc lúc audit (T2.3.2 pre-annotation) qua view bằng role `research_reader`. Hash của nội dung đã đọc trùng với manifest cho cả 696 chunk.
