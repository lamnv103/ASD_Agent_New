# T2.4-B — Blind Human Annotation & Adjudication: Quality Report — 2026-11-15

**Kết luận: READY WITH CONDITIONS cho T2.5.** Hạ tầng chấm mù đã sẵn sàng và đã được kiểm chứng, nhưng **chưa có nhãn nào: 0 / 2.791 cặp được người chấm** (A và B đều chưa bắt đầu). q057 và q016 chưa được phân xử.

Vì vậy **T2.5 chưa được đánh giá hay so sánh dense, FTS, hybrid một cách công bằng**. Có thể dựng hybrid về mặt kỹ thuật, nhưng không được tuyên bố chất lượng cho đến khi xong C1–C3 (mục 9). Không tự chuyển sang T2.5.

**Lý do không có nhãn:** phiên làm việc này không có người chấm. Theo yêu cầu, **không dùng nhãn do AI tạo** để thay thế hay gợi ý. Mọi nhãn silver cũ (T1, T2.3.2) bị loại khỏi gói chấm.

## 1. R1 — Kiểm tra pool (đã chạy: `annotation_t2_4b.py verify`)
Kết quả máy đọc: `fts_annotation_pool_integrity_2026-11-15.json`.

| Kiểm tra | Kết quả |
|---|---|
| Hash đầu vào khớp lúc tạo ở T2.4 | pool `851dc471…`, key `0de3cc6c…`, manifest `e9e7c072…`, overlap `0da42455…`, dataset gốc `7704bb51…`, merge `6bd3ad78…` ✔ |
| Số câu / số cặp / số chunk duy nhất | **66 / 2.791 / 1.218** ✔ |
| Cặp trùng / `item_id` trùng | 0 / 0 ✔ |
| Pool = khoá (cặp và `item_id`) | ✔ |
| Mã câu hỏi và nội dung câu khớp dataset gốc | 0 lỗi ✔ |
| sha256(nội dung) = `content_sha256` = `embedding_manifest.csv` (cùng source và document) | 0 lỗi ✔ |
| Provenance (source, document, tiêu đề, trang hoặc khoảng ký tự) | 0 thiếu ✔ |
| Trong allowlist authorization 2 | 2.791 / 2.791 ✔ |
| **Đối chiếu trực tiếp với view** (role reader, chỉ đọc): hash nội dung + `authorization_id` = 2 | 0 lệch ✔ |
| Manifest (union theo câu) = pool | ✔ |
| Nguồn gốc trong khoá = danh sách xếp hạng trong `fts_run_record` | 0 lỗi ✔ |
| Theo nguồn gốc | chỉ dense 997 · chỉ FTS 1.471 · cả hai 323 ✔ |

**Không có bất nhất. Pool gốc không bị sửa.**

## 2. R2 — Gói chấm mù (đã tạo: `annotation_t2_4b.py package`)
| File | Nội dung |
|---|---|
| `eval/annotation/t2_4b/annotator_a/fts_blind_annotation_package_annotator_a_2026-11-15.{csv,jsonl}` | 2.791 dòng cho người chấm A (CSV có BOM UTF-8 để mở bằng Excel; nội dung dài nhất khoảng 3.800 ký tự) |
| `eval/annotation/t2_4b/annotator_b/…_annotator_b_2026-11-15.{csv,jsonl}` | Cùng 2.791 cặp; **mã và thứ tự độc lập** với A |
| `…/annotator_{a,b}/annotation_guidelines_t2_4b_2026-11-15.md` | Rubric và hướng dẫn (giống nhau) |
| `eval/annotation/t2_4b/coordinator/` | `annotation_code_map` (mã → câu, chunk, item), `hmac_secret.txt`, `annotators.json`, mẫu quyết định ca đặc biệt. **Chỉ người điều phối giữ** |

**Mỗi dòng gói chấm chứa:**
- `annotation_code`, `question_id`, `question_vi`;
- `document_title`, `section`, `page` (ngữ cảnh cần thiết);
- `content` (đầy đủ);
- các ô trống: `grade`, `rationale`, `evidence_span`, `confidence`, `needs_review`, `review_note`.

**Không có trong gói chấm:**
- `chunk_id`, `item_id`, `source_id`/`document_id`, `content_sha256`, `char_range`;
- hệ thống, rank, điểm;
- nhãn cũ;
- `expected_answer_scope` (do AI viết ở T1).

**Kiểm tra rò rỉ** (tự động, có test `test_packages_have_no_leaking_fields_or_ids_and_independent_codes`):
- Trường đúng danh sách cho phép; không có ID nội bộ nào xuất hiện.
- Mã là HMAC-SHA256 với khoá bí mật 256 bit. Không suy ngược được về chunk, rank hay hệ thống khi không có khoá.
- 0 mã trùng giữa A và B; các ô chấm đều trống.
- Thứ tự câu và thứ tự ứng viên được xáo trộn bằng RNG lấy từ khoá bí mật, độc lập cho A và B. **Spearman trung bình giữa vị trí trong file và rank tốt nhất của ứng viên: A = 0,007, B = 0,024** (≈ 0). Thứ tự không mang thông tin về truy xuất.
- Tái lập: `package --check` sinh lại giống hệt từng byte từ khoá bí mật.

**Cảnh báo:** file `fts_candidate_pool_2026-11-15.jsonl` của T2.4 **không được** giao cho người chấm. File đó chứa `chunk_id`, `item_id` (suy ra được từ chunk) và `expected_answer_scope`. Tương tự với `…_key_…`, `fts_run_record_…` và mọi file trong `eval/reports`, `eval/datasets`. Danh sách đầy đủ ở `fts_annotation_freeze_manifest_2026-11-15.json`.

**Sửa trước khi phát hành:** bản đầu của hướng dẫn có ví dụ trùng câu eval (q066 động kinh, q041 SENITA) và **trùng chính ca phân xử q016** ("shared engagement" và "joint attention"). Đã thay bằng ví dụ trung tính ngoài bộ câu (viêm tai giữa) **trước khi** phát hành. Ghi nhận trong freeze manifest (`4647c1be…` thành `b8cd5025…`). Gói chấm không đổi.

## 3. R3 — Rubric
Thang 3/2/1/0/−1 đúng như yêu cầu. Mỗi nhãn bắt buộc có: grade, lý do, `evidence_span` (chép nguyên văn, validator kiểm tra là chuỗi con của nội dung), `confidence` (high/medium/low). Khi không đủ thông tin: `needs_review` kèm `review_note`, và **không ghi grade**. Ô bỏ trống được tính là **chưa chấm**, không bao giờ là 0.

## 4. R4 — Hai người chấm: **CHƯA THỰC HIỆN**
- Chưa có người chấm A hoặc B. **0 / 2.791 cặp được chấm.** Không tuyên bố pool đã được annotation.
- **Khối lượng:** khoảng 1 phút/cặp, nên **45–50 giờ mỗi người** để chấm toàn bộ.
- **Phương án dự phòng nếu không đủ nguồn lực** (đề xuất, cần phê duyệt; không tự chọn tập thuận tiện):
  - Lấy mẫu phân tầng theo **câu hỏi × loại ứng viên** (chỉ dense / chỉ FTS / cả hai): 188 tầng (66 / 65 / 57).
  - Lấy ngẫu nhiên n cặp mỗi tầng (lấy hết nếu tầng ít hơn n), bằng RNG có seed ghi lại. **Người điều phối** chọn bằng khoá; người chấm vẫn chỉ thấy gói mù.

| n mỗi tầng | Số cặp | % pool | Giờ/người (≈1 phút/cặp) |
|---|---|---|---|
| 4 | 706 | 25,3% | ≈ 12 |
| 6 | 1.024 | 36,7% | ≈ 17 |
| 8 | 1.314 | 47,1% | ≈ 22 |
| 10 | 1.582 | 56,7% | ≈ 26 |

  Nếu lấy mẫu thì metric phải dùng trọng số nghịch đảo xác suất chọn, và báo cáo rõ phạm vi đã chấm.

## 5. R5 — Đồng thuận: **chưa tính** (chưa có dữ liệu). Công cụ đã sẵn sàng và đã kiểm thử
`annotation_t2_4b.py agreement` sẽ tính:
- exact agreement;
- specific agreement theo từng grade;
- ma trận nhầm lẫn 6×6 (−1, 0–3, `needs_review`);
- **Cohen's kappa có trọng số quadratic và linear trên thang thứ tự 0–3**, kèm kappa không trọng số và kappa nhị phân (≥ 2 hay không);
- tỷ lệ bất đồng theo grade;
- tỷ lệ `needs_review`;
- phân bố grade của mỗi người.

**Grade −1 được xử lý riêng:** không nằm trên trục thứ tự. Các cặp có −1 hoặc `needs_review` ở một trong hai người bị **loại khỏi kappa** và được báo cáo riêng (số lượng, tỷ lệ cả hai cùng −1). Không đánh giá độ tin cậy chỉ dựa trên một con số kappa: phải đọc kèm phân bố grade và các nhóm bất đồng.

**Đã kiểm chứng toán:**
- kappa = 1 khi đồng ý hoàn toàn; −1 khi đảo ngược hoàn toàn;
- ví dụ 2×2 trong sách: po = 0,7, pe = 0,5, kappa = 0,4;
- kappa không xác định khi không có biến thiên.

## 6. R6 — Phân xử: công cụ sẵn sàng, chưa có bất đồng để xử lý
- `agreement` ghi `fts_annotation_disagreement_2026-11-15.csv`: mọi cặp khác grade hoặc có `needs_review`, kèm hai grade, hai lý do, hai `evidence_span` và loại bất đồng.
- **Loại bất đồng:** `needs_review`, `conflicting_involved`, `relevance_boundary_1_vs_2`, `relevant_vs_irrelevant`, `adjacent_or_other`.
- **Người phân xử thứ ba** ghi `fts_annotation_adjudication_2026-11-15.jsonl`. Validator yêu cầu: lý do, `adjudicator_id` khác A và B (đối chiếu `coordinator/annotators.json`), grade thuộc −1..3, và chỉ áp cho cặp có bất đồng.
- **`finalize`:**
  - A = B (và không có `needs_review`) thì `agreed`;
  - đã có quyết định thì `adjudicated`;
  - còn lại `pending_adjudication`, hoặc `single_annotator_only` nếu chỉ một người chấm (grade = null).
  - **Không bao giờ lấy trung bình** và không điền cặp chưa chấm (có unit test).
- Lưu riêng 4 file: nhãn A, nhãn B, nhãn phân xử, nhãn cuối.

## 7. R7 — q057 và q016: **chưa phân xử**. Hồ sơ đã chuẩn bị
`fts_adjudication_dossier_q057_q016_2026-11-15.md` và mẫu quyết định `coordinator/special_case_decisions_template_2026-11-15.json`:
- **q057:** nguyên văn chunk PMC12620806#0021 và nguồn.
  - Bảng phân biệt *nghiên cứu lịch sử / nghiên cứu đã bị rút / bằng chứng hiện tại (corpus không có) / khẳng định nhân quả (không có)*.
  - Các lựa chọn (a) `partially_answerable`, (b) giữ `unanswerable`, (c) khác.
  - Người quyết định: chủ dự án và chuyên gia.
- **q016:** nguyên văn 2 chunk WHO-CST (#0023, #0024).
  - Câu hỏi cần quyết định: "shared engagement" có được coi là joint attention không, và mức hỗ trợ của từng chunk.
- Hồ sơ **cố ý không nêu ảnh hưởng lên metric**. Grade tạm của AI được ghi rõ là không phải nhãn.
- Kèm tồn đọng q041 SENITA#0309 để không bị bỏ sót.

## 8. R8 / R10 — Kiểm soát glossary bias và bất biến
- **Đóng băng:** `fts_annotation_freeze_manifest_2026-11-15.json` ghi SHA-256 của 16 file (glossary, profile FTS và dense, code retrieval, pool, khoá, manifest, hai dataset, hai gói chấm, hướng dẫn). Kiểm tra lại cuối phiên: **0 sai lệch**.
- Không thêm từ vào glossary, không đổi FTS-A/B/C, không chạy lại hay thử biến thể truy xuất trong T2.4-B.
- Backlog glossary v2 (chỉ làm sau khi chấm xong, đánh giá trên **bộ câu hold-out**):
  - `WHO` thành "World Health Organization";
  - giữ `stem cell` làm dấu hiệu vắng;
  - xem lại 7 thuật ngữ có 0 kết quả khớp, dựa trên bằng chứng.
- Không ghi DB; không gọi API (chỉ một truy vấn đọc bằng role reader để kiểm tra nội dung); dataset gốc và merge không đổi; pool gốc không đổi.
- **Test:** `ruff` đạt; `pytest` unit **245 passed** (23 test mới cho quy trình chấm). Chạy thử toàn bộ quy trình (`import → agreement → finalize`) trên gói thật với **grade giả lập trong bộ nhớ**: không ghi file nào và không dùng làm nhãn.

## 9. Điều kiện trước T2.5
| # | Điều kiện | Ai làm |
|---|---|---|
| C1 | Hai người chấm độc lập (hoặc phương án lấy mẫu ở mục 4 được phê duyệt) chấm gói mù. Nhập bằng `import --annotator a/b --returned <file>` | Chủ dự án tuyển người chấm; người điều phối giữ khoá |
| C2 | Chạy `agreement`, đọc kappa cùng phân bố và nhóm bất đồng; người phân xử thứ ba xử lý danh sách bất đồng; chạy `finalize` | Người điều phối + chuyên gia |
| C3 | Quyết định q057 và q016 (và q041) theo hồ sơ; nếu đổi nhãn câu hỏi thì tạo phiên bản dataset mới | Chủ dự án / chuyên gia |
| C4 | Chỉ sau C1–C3: tính lại metric dense / FTS-A/B/C trên nhãn cuối; sau đó mới đến T2.5 hybrid | — |
| C5 | Glossary v2 và bộ câu hold-out cho FTS | Sau C4 |

## 10. Trả lời các câu hỏi bắt buộc
1. **Đã chấm bao nhiêu cặp?** **0 / 2.791.** Gói chấm cho A và B đã sẵn sàng; chưa có người chấm.
2. **Bao nhiêu cặp cần phân xử?** Chưa xác định được vì chưa có nhãn. Đã biết: 3 ca đặc biệt (q057 nhãn câu + 1 chunk, q016 2 chunk, q041 1 chunk) đang chờ.
3. **Exact agreement và weighted kappa?** **Chưa tính được** (không có dữ liệu). Công cụ tính quadratic và linear trên thang 0–3, −1 báo cáo riêng, đã kiểm thử.
4. **Các nhóm bất đồng phổ biến?** Chưa có dữ liệu. Công cụ phân 5 nhóm (`needs_review`, có −1, ranh giới 1/2, relevant vs không relevant, kề nhau/khác).
5. **q057 đã giải quyết chưa?** **Chưa.** Hồ sơ và mẫu quyết định đã có; cần chủ dự án và chuyên gia.
6. **q016 đã giải quyết chưa?** **Chưa.** Hồ sơ đã có; cần chuyên gia ngôn ngữ trị liệu hoặc can thiệp sớm.
7. **Có rò rỉ thông tin mù không?** **Không** trong gói chấm: không có trường hay ID cấm, mã không suy ngược được, thứ tự không tương quan với rank (Spearman ≈ 0,01–0,02). Đã phát hiện và **sửa trước khi phát hành** các ví dụ trong hướng dẫn trùng câu eval và trùng ca q016. Rủi ro còn lại: nếu ai đó giao nhầm các file bị cấm trong freeze manifest cho người chấm.
8. **Kiểm soát glossary bias thế nào?** Đóng băng bằng SHA (manifest 16 file, 0 sai lệch); không sửa glossary hay profile; không chạy lại truy xuất; glossary v2 chỉ làm sau khi chấm và đánh giá trên bộ hold-out.
9. **Bộ dữ liệu cuối có hợp lệ và tái lập không?** **Chưa tồn tại** vì chưa có nhãn. Quy trình tạo nó tất định, có validator (import và phân xử) và unit test; gói chấm tái lập từng byte từ khoá.
10. **Có đủ điều kiện chuyển T2.5 không?** **READY WITH CONDITIONS**, với điều kiện bắt buộc C1–C3. Trước khi xong, không được so sánh hay tuyên bố chất lượng của dense, FTS hay hybrid.
