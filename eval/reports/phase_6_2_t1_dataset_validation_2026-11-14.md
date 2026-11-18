# Phase 6.2 – T1: Dataset Validation — 2026-11-14

**Kết quả: PASS** (0 lỗi, 0 cảnh báo).

- Lệnh: `python -B scripts/validate_retrieval_eval.py --report eval/reports/phase_6_2_t1_dataset_validation_2026-11-14.json`
- Validator chỉ đọc file: không kết nối DB, không gọi mạng hay API.

| Đối tượng | SHA-256 |
|---|---|
| `eval/datasets/retrieval_eval_v1.jsonl` | `7704bb510c9ab4a5…` (đầy đủ trong file JSON đi kèm) |
| `eval/reports/embedding_manifest.csv` (tập chunk hợp lệ) | `542cce21378b302312f6f509ba69db0fc346b98d2c47bc0e639775a6d12b4fd3` |

## 1. Các kiểm tra
| # | Kiểm tra | Kết quả |
|---|---|---|
| 1 | Mọi dòng JSONL parse được | ✔ 66/66 |
| 2 | `question_id` không trùng, đúng định dạng `qNNN` | ✔ |
| 3 | Trường bắt buộc đủ, không có trường lạ (schema `additionalProperties: false`) | ✔ |
| 4 | `query_category`, `query_style`, `answerability`, trạng thái… thuộc enum của schema | ✔ |
| 5 | Grade ∈ {-1, 0, 1, 2, 3} | ✔ 435/435 |
| 6 | Mọi chunk đã chấm tồn tại trong tập đã embed, khớp document/source | ✔ 339 chunk duy nhất |
| 7 | `content_sha256` của nhãn khớp manifest (không lệch nội dung) | ✔ |
| 8 | `relevant_chunk_ids` = đúng các chunk đã chấm có grade ≥ 2 (không ID bịa, không candidate) | ✔ |
| 9 | `relevant_document_ids` = document của các chunk relevant | ✔ |
| 10 | Không có gold khi chưa có người đánh giá là con người | ✔ (0 gold) |
| 11 | Bản ghi pending không mang nhãn relevant | ✔ (0 pending) |
| 12 | Câu unanswerable / out-of-scope không có chunk relevant; câu answerable có ít nhất 1 | ✔ |
| 13 | Không có câu hỏi rỗng; không có câu trùng (chuẩn hoá) hay gần trùng (Jaccard ≥ 0,8) | ✔ |
| 14 | Không có email, số điện thoại hay chuỗi giống secret | ✔ |
| 15 | `corpus.embedding_manifest_sha256` khớp manifest hiện tại | ✔ |

## 2. Thống kê (do validator tính)
| Chỉ số | Giá trị |
|---|---:|
| Tổng câu hỏi | 66 |
| Đã gán nhãn single-pass (`annotated_single` + `verified_unanswerable`) | 65 |
| — trong đó pool chưa đầy đủ (`annotation_completeness = partial`) | 4 |
| — hoàn chỉnh trong phạm vi pool đã chấm | 61 |
| Không áp dụng (ngoài luồng expert_qa) | 1 |
| Pending | 0 |
| Đã được con người xác minh (gold) | **0** |
| Partially answerable / unanswerable / blocked / out of scope | 12 / 2 / 2 / 1 |
| Câu có bằng chứng mâu thuẫn (-1) | 4 |
| Câu cần nhiều chunk | 40 |
| Câu có bằng chứng relevant từ ≥ 2 nguồn | 54 |
| Nhãn (chunk đã chấm) / relevant (≥ 2) | 435 / 300 |
| Chunk duy nhất: đã chấm / relevant | 339 / 238 |
| Nguồn có ít nhất 1 chunk relevant | 60 / 71 |
| Phân bố grade (-1/0/1/2/3) | 5 / 64 / 66 / 186 / 114 |

## 3. Kiểm thử của validator
`tests/unit/test_retrieval_eval_validator.py`: **19 test pass**. Mỗi quy tắc đều có cả trường hợp dương và âm:
- JSON hỏng;
- ID trùng;
- chunk lạ;
- relevant bịa;
- grade ngoài thang;
- hash lệch;
- gold không có người đánh giá;
- pending mang nhãn;
- unanswerable mang nhãn;
- answerable thiếu bằng chứng;
- câu rỗng, trùng, chứa email;
- corpus pin sai;
- trường lạ hoặc enum sai;
- thống kê pending;
- đủ 5 mức grade.

## 4. Ghi chú
- Validator đầu tiên báo 10 lỗi "chuỗi nhạy cảm". Đó là **dương tính giả**: `document_id` dạng `…@PMC10981608.1;` khớp mẫu email. Đã loại `relevant_document_ids` khỏi phép quét, vì trường này được đối chiếu chặt với manifest ở kiểm tra 9. Sau khi sửa, kết quả là 0 lỗi.
- Một lần build lại dataset (`--force`) để thêm trường `annotation_completeness`. Đây là file tạo trong cùng phiên, không ghi đè dữ liệu có trước.
