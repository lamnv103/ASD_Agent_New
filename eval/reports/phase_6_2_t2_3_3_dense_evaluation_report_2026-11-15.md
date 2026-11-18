# Phase 6.2 – T2.3.3: Dense Retrieval Baseline Evaluation — 2026-11-15

**Kết luận: READY WITH CONDITIONS cho T2.4.** Không tự chuyển sang T2.4. Điều kiện ở mục 12.

| Kiểm tra | Kết quả |
|---|---|
| Cohort | Đóng băng theo T2.3.1, không lệch |
| Kết quả truy xuất | Tái lập **66/66 danh sách xếp hạng giống hệt T2.3.1**; số liệu T2.3.1 tái tạo với 0 sai khác |
| Hai bộ số liệu | Báo cáo riêng: A = nhãn gốc, B = nhãn merge |
| Thay đổi ngoài phạm vi | Không có: 0 lệnh gọi API, DB fingerprint trước = sau, dataset và cache không đổi |
| Giới hạn còn lại | Nhãn silver; judged coverage thấp ở run A; run B thiên lệch về dense; q057 và q016 chờ phân xử |

## 1. Mục tiêu và phạm vi
- **Mục tiêu:** đo dense retrieval (`dense_baseline_v1`) trên 66 câu với hai bộ nhãn tách biệt; đo judged coverage; phân tích lỗi; xử lý q057 bằng phân tích độ nhạy.
- **Chỉ đánh giá.** Không đổi retriever, Top-K, cấu hình, chunk, vector, authorization, migration hay quyền. Không thêm FTS, hybrid, RRF, reranker, query expansion hay evidence gate. Không loại boilerplate hay placeholder. Không sửa dataset.

## 2. Phiên bản và hash đầu vào
| Đầu vào | SHA-256 |
|---|---|
| `eval/datasets/retrieval_eval_v1.jsonl` (A) | `7704bb51…4c2b` (trước = sau) |
| `eval/datasets/retrieval_eval_v1_merged_2026-11-14.jsonl` (B) | `6bd3ad78…e7ab` (trước = sau) |
| `…_candidate_judgments_2026-11-14.jsonl` | `de526dd0…563f` |
| `phase_6_2_t2_3_2_unresolved_adjudications_2026-11-14.csv` | `f7697d66…f553` |
| Cohort: `phase_6_2_t2_3_1_dense_retrieval_metrics_2026-11-14_r2.json` | `d74cd710…30de` |
| Query cache `data/index/query_embeddings/` (66 file) | `7038b000…2235` (trước = sau) |
| `config/retrieval_profiles.json` / `embedding_profiles.json` | `17595edc…` / `b4c26b6e…` |
| `app/retrieval/dense.py` · `research_reader.py` · `query_embedding.py` · `types.py` · `embeddings.py` | `46561e4b…` · `3bf30477…` · `0ee603cc…` · `34a31cf7…` · `645cce82…` (không sửa) |
| `scripts/dense_retrieval_eval.py` (T2.3.1, chỉ import hàm) | `519b9543…` |
| `scripts/dense_eval_t2_3_3.py` (mới, chỉ đánh giá) | `2579bdc2…` |
| Manifest cohort (`dense_eval_frozen_cohort_manifest_2026-11-15.csv`) | `0d88846e…380c` |

**Cấu hình truy xuất:**
- Model `embed-v4.0`: `search_query` cho câu hỏi, `search_document` cho tài liệu; 1536 chiều.
- Cosine `<=>`, exact search, k = 20 (cắt 5/10/20).
- Role `asd_rag_v2_research_reader`, view `asd_rag.v_research_retrieval_chunks`: 2.291 chunk, authorization {2}.

## 3. Phương pháp
1. **Đóng băng cohort (R1).**
   - Lấy nhóm của từng câu từ metrics T2.3.1 (`_r2`): answerable 55, answerable_partial_pool 2 (q010, q040), conflicting 4 (q033, q041, q054, q060), unanswerable 2 (q057, q059), refusal 2 (q058, q061), out_of_scope 1 (q062).
   - Script đối chiếu: `group_of(dataset gốc)` khớp nhóm T2.3.1 ở 66/66 câu; answerability của file gốc và file merge giống nhau 66/66. Nếu lệch, script dừng.
   - Cột `group_if_rederived_from_merged` trong manifest cho thấy nếu suy lại nhóm từ file merge, 55 câu answerable sẽ thành `partial_pool`. **Không dùng cột này.**
2. **Truy xuất một lần, chấm hai lần.**
   - Query vector chỉ lấy từ cache. `CachedQueryEmbedder` **không có API client**: cache miss thì dừng.
   - Danh sách top-20 của mỗi câu được chấm riêng bằng nhãn A và nhãn B.
3. **Tái lập.**
   - So danh sách top-20 với log T2.3.1 (`logs/retrieval/dense_eval_20261114T153403.jsonl`): **66/66 giống hệt, chênh lệch cosine distance tối đa 0,0**.
   - Tính lại số liệu T2.3.1 bằng chính hàm của T2.3.1: **0 sai khác**.
   - Chạy lần hai với `--check`: mọi file kết quả giống hệt, trừ timestamp và latency.
4. **Kiểm tra bất biến** (chỉ role reader, chỉ đọc): fingerprint trước và sau gồm
   - (a) hash nội dung và vector của toàn bộ view;
   - (b) ma trận quyền `has_table_privilege` của 4 role × 22 relation × 5 quyền;
   - (c) thuộc tính 4 role;
   - (d) bộ đếm ghi `pg_stat_all_tables` (ins/upd/del) của 17 bảng.
5. **Error analysis:** đọc nội dung top-k và kiểm tra từ khoá toàn corpus qua view (chỉ để kiểm toán, không phải retriever). Xem `dense_eval_error_analysis_2026-11-15.md`.

## 4. Định nghĩa metric
- **R** = tập chunk đã chấm grade ≥ 2 và truy xuất được (authorization 2). Grade −1 và grade 1 không thuộc R.
- **Unjudged không bao giờ được tính là grade 0.**

| Metric | Công thức | Mẫu số / giới hạn |
|---|---|---|
| Recall@K | \|top-K ∩ R\| / \|R\| | Chỉ tính trên relevant **đã biết**. Chunk relevant ngoài pool chưa biết, nên đây không phải cận trên hay cận dưới của recall thật |
| Hit@K | 1 nếu top-K ∩ R ≠ ∅ | Câu có \|R\| ≥ 1 |
| Precision_lb@K | \|top-K ∩ R\| / K | Unjudged tính là không relevant, nên là **cận dưới** |
| Precision_ub@K | (\|top-K ∩ R\| + unjudged) / K | Unjudged tính là relevant, nên là **cận trên** |
| Judged-only precision@K | \|top-K ∩ R\| / số chunk đã chấm trong top-K | Bỏ qua unjudged |
| MRR | 1 / rank chunk ∈ R đầu tiên trong top-20 (0 nếu không có) | **Cận dưới**. `mrr_ub` = 1 / rank của chunk đầu tiên thuộc R hoặc unjudged. Báo cáo kèm số unjudged đứng trước relevant đầu tiên |
| nDCG@K | Gain 3→7, 2→3, 1→1, 0→0, unjudged→0. **Grade −1 không có gain** và không vào IDCG. IDCG lấy từ mọi chunk đã chấm truy xuất được | Cận dưới. Kèm `ndcg_t231_lb` (gain tuyến tính 3/2/1/0, −1→2) để so với T2.3.1 |
| Source recall@K | \|nguồn khác nhau trong top-K ∩ S\| / \|S\|, S = nguồn của R | **Đếm mỗi nguồn một lần**. Document recall tương tự với `document_id` (hiện trùng với source) |
| Judged coverage@K | Số chunk đã chấm trong top-K / \|top-K\| | Micro = Σ đã chấm / Σ truy xuất; macro = trung bình theo câu |
| Unjudged rate@K | 1 − coverage | |
| Conflict coverage@20 | Số chunk −1 trong top-20 / số chunk −1 truy xuất được | Chỉ nhóm conflicting |

Trung bình macro theo câu, CI95 bootstrap (2.000 lần, seed 20261114, giống T2.3.1). Câu có \|R\| = 0 thì recall/hit/nDCG = None (không tính là 0).

## 5. Kết quả: nhóm chính `answerable` (55 câu cố định)
| Metric | T2.3.1 | **A: nhãn gốc** (CI95) | **B: nhãn merge** (CI95) | Δ B−A |
|---|---|---|---|---|
| Recall@5 | 0,35 | **0,348** (0,275–0,423) | **0,473** (0,409–0,534) | +0,125 |
| Recall@10 | 0,49 | **0,491** (0,405–0,573) | **0,607** (0,535–0,673) | +0,115 |
| Recall@20 | 0,65 | **0,646** (0,564–0,720) | **0,716** (0,643–0,782) | +0,070 |
| Hit@5 | 0,84 | **0,836** | **0,964** | +0,127 |
| Hit@10 | 0,91 | **0,909** | **0,964** | +0,055 |
| Hit@20 | 0,96 | **0,964** | **0,964** | 0 |
| MRR (cận dưới) | 0,58 | **0,585** (0,483–0,684) | **0,782** (0,698–0,862) | +0,197 |
| MRR cận trên | — | 0,952 | 0,801 | |
| Unjudged trước relevant đầu tiên (TB) | — | 2,71 | 0,47 | |
| Precision@5 [lb – ub] | lb 0,32 | [0,316 – 0,953] | [0,582 – 0,589] | |
| Precision@10 [lb – ub] | lb 0,23 | [0,227 – 0,956] | [0,376 – 0,735] | |
| Judged-only precision@5 / @10 / @20 | @10 0,85 | 0,894 / 0,846 / 0,824 | 0,582 / 0,598 / 0,609 | |
| nDCG@5 / @10 / @20 (gain 7/3/1) | — | 0,388 / 0,440 / 0,496 | 0,609 / 0,608 / 0,649 | |
| nDCG@10 theo định nghĩa T2.3.1 | 0,428 | 0,428 | 0,630 | |
| Source hit@5 / @10 / @20 | 0,98 / 0,98 / 1,00 | 0,982 / 0,982 / 1,000 | 0,982 / 0,982 / 1,000 | 0 |
| Source recall@5 / @10 / @20 | — / 0,74 / 0,82 | 0,632 / 0,737 / 0,824 | 0,663 / 0,761 / 0,838 | +0,03 / +0,02 / +0,01 |

**Đọc kết quả:**
- **A tái lập T2.3.1 chính xác.** Các số trong prompt (0,35 / 0,49 / 0,65; 0,84 / 0,91 / 0,96; 0,98 / 0,98 / 1,00; MRR 0,58) được xác nhận với cùng định nghĩa (R = grade ≥ 2, truy xuất được) và cùng nhãn (`7704bb51…`).
- **B tăng mạnh vì nhãn mới đến từ chính top-20 của dense** (95/95 nhãn; 81 ở rank ≤ 5). Phần tăng này phần lớn là **giảm sai số do thiếu nhãn**, không chứng minh dense tốt hơn.
  - Ở B, precision@5 bị kẹp trong [0,582; 0,589] (coverage@5 = 99%). Đây là ước lượng gần đúng nhất hiện có của precision ở top-5 **trên tập nhãn silver**.
  - MRR thật (trên nhãn B) nằm trong [0,78; 0,80].
- **Hit@20 không đổi (0,964).** Hai câu answerable không có relevant trong top-20 ở cả A và B:
  - q066 (động kinh): lỗi truy xuất;
  - q016 (joint attention): phụ thuộc phân xử 2 chunk ở rank 1–2.
- **Judged-only precision giảm từ A sang B** (0,85 → 0,60 @10). Lý do: ở A, các chunk đã chấm phần lớn được chọn từ pool T1 vốn thiên về relevant. B thêm nhiều nhãn 0 và 1 ở top-10 thật, nên phản ánh đúng hơn.

## 6. Nhóm khác
| Nhóm | Số câu | Recall@10 A → B | Hit@10 A → B | MRR A → B | Cov@10 A → B | Ghi chú |
|---|---|---|---|---|---|---|
| answerable_partial_pool (q010, q040) | 2 | 0,25 → 0,59 | 0,5 → 1,0 | 0,55 → 1,0 | 0,05 → 0,50 | n = 2, CI rất rộng |
| conflicting (q033, q041, q054, q060) | 4 | 0,13 → 0,31 | 0,25 → 0,75 | 0,04 → 0,23 | 0,05 → 0,88 | Relevant đầu tiên: q033 rank 10, q054 rank 17. Conflict coverage@20 = 0,25 ở cả A và B |
| Tất cả câu có bằng chứng | 61 | 0,459 → 0,587 | 0,85 → 0,95 | 0,548 → 0,752 | 0,25 → 0,65 | Chỉ để tham khảo; nhóm chính vẫn là 55 câu |

| Nhóm không trả lời | Top-1 cosine sim | Relevant A / B | Ghi chú |
|---|---|---|---|
| q057 (unanswerable, chờ phân xử) | 0,359 | 0 / 0 | Chunk #0021 ở rank 4 (needs_adjudication) |
| q059 (unanswerable) | 0,316 | 0 / 0 | Kiểm tra từ khoá: 0 chunk "stem cell". Khoảng trống corpus thật |
| q058 (refusal: liều risperidone) | 0,398 | 0 / 0 | Top-10 là liều *thuốc khác* (đều grade 0): rủi ro cho evidence gate |
| q061 (refusal: xếp đồ thành hàng) | 0,453 | 3 / 4 | Có thông tin chung (DSM-5 B), đúng với nhãn "thông tin chung + đi khám" |
| q062 (out of scope) | 0,226 | 0 / 0 | Coverage 0 vì 5 ứng viên `excluded` (không tính là grade 0) |

Top-1 similarity của q057, q058 và q061 nằm trong khoảng của câu answerable (0,280–0,592, trung vị 0,464). **Ngưỡng cosine đơn thuần không tách được câu không trả lời được.** Chỉ q062 (0,226) nằm dưới khoảng này.

## 7. Judged coverage và unjudged rate (nhóm answerable, 55 câu)
| K | Số lượt truy xuất | Đã chấm A | Coverage A micro / macro | Unjudged rate A | Đã chấm B | Coverage B micro / macro | Unjudged rate B |
|---|---|---|---|---|---|---|---|
| 5 | 275 | 100 | 0,364 / 0,364 | 0,636 | 273 | 0,993 / 0,993 | 0,007 |
| 10 | 550 | 149 | 0,271 / 0,271 | 0,729 | 353 | 0,642 / 0,642 | 0,358 |
| 20 | 1.100 | 208 | 0,189 / 0,189 | 0,811 | 412 | 0,375 / 0,375 | 0,625 |

Micro và macro bằng nhau vì mọi câu đều trả đủ K kết quả.

**Số câu answerable có coverage < 0,5 (độ tin cậy thấp, cột `low_confidence` trong CSV):**

| K | A | B |
|---|---|---|
| 5 | 39/55 | 0/55 |
| 10 | 48/55 | 1/55 |
| 20 | 55/55 | 45/55 |

**Hệ quả:**
- Ở run A, mọi metric phụ thuộc vị trí (precision, nDCG, MRR) có khoảng bất định rất rộng: precision@10 ∈ [0,23; 0,96].
- Ở run B, số liệu top-5 và top-10 đáng tin hơn. Top-20 vẫn có 62,5% chưa chấm.
- Chi tiết theo câu × K × run: `dense_eval_judged_coverage_2026-11-15.csv`.

## 8. Theo từng câu hỏi (A → B)
"Rank đầu" = rank của chunk relevant đầu tiên; ">20" = không có trong top-20. Đầy đủ mọi metric: `dense_eval_per_question_metrics_2026-11-15.csv`.

A 5 answerable q with coverage<0.5: 39
B 5 answerable q with coverage<0.5: 0
A 10 answerable q with coverage<0.5: 48
B 10 answerable q with coverage<0.5: 1
A 20 answerable q with coverage<0.5: 55
B 20 answerable q with coverage<0.5: 45
| Câu | Cohort | Relevant A→B | Rank đầu A→B | Recall@10 A→B | MRR A→B | nDCG@10 A→B | Cov@10 A→B | Cov@20 A→B |
|---|---|---|---|---|---|---|---|---|
| q001 | answerable | 7→9 | 1→1 | 0.14→0.33 | 1.00→1.00 | 0.35→0.45 | 0.10→0.50 | 0.05→0.25 |
| q002 | answerable | 7→10 | 3→2 | 0.14→0.40 | 0.33→0.50 | 0.17→0.47 | 0.20→0.60 | 0.25→0.45 |
| q003 | answerable | 5→7 | 1→1 | 0.40→0.57 | 1.00→1.00 | 0.73→0.82 | 0.20→0.50 | 0.15→0.30 |
| q004 | answerable | 5→6 | 2→2 | 0.40→0.50 | 0.50→0.50 | 0.36→0.42 | 0.20→0.60 | 0.10→0.30 |
| q005 | answerable | 7→9 | 5→3 | 0.43→0.56 | 0.20→0.33 | 0.30→0.53 | 0.30→0.70 | 0.20→0.40 |
| q006 | answerable | 3→3 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.82→0.85 | 0.30→0.60 | 0.15→0.30 |
| q007 | answerable | 4→4 | 4→4 | 0.50→0.50 | 0.25→0.25 | 0.34→0.38 | 0.50→0.70 | 0.40→0.50 |
| q008 | answerable | 7→8 | 1→1 | 0.86→0.88 | 1.00→1.00 | 0.81→0.83 | 0.60→0.70 | 0.30→0.35 |
| q009 | answerable | 4→4 | 2→2 | 0.50→0.50 | 0.50→0.50 | 0.56→0.62 | 0.20→0.50 | 0.10→0.25 |
| q010 | partial_pool | 2→4 | 1→1 | 0.50→0.75 | 1.00→1.00 | 0.31→0.52 | 0.10→0.50 | 0.10→0.30 |
| q011 | answerable | 4→5 | 1→1 | 0.75→0.80 | 1.00→1.00 | 0.71→0.73 | 0.50→1.00 | 0.35→0.60 |
| q012 | answerable | 3→4 | 13→2 | 0.00→0.25 | 0.08→0.50 | 0.14→0.44 | 0.10→0.50 | 0.15→0.35 |
| q013 | answerable | 5→8 | 1→1 | 0.80→0.88 | 1.00→1.00 | 0.87→0.93 | 0.40→0.70 | 0.25→0.40 |
| q014 | answerable | 7→9 | 6→2 | 0.14→0.33 | 0.17→0.50 | 0.07→0.37 | 0.10→0.60 | 0.05→0.30 |
| q015 | answerable | 4→8 | 3→2 | 0.25→0.62 | 0.33→0.50 | 0.23→0.58 | 0.30→1.00 | 0.20→0.55 |
| q016 | answerable | 4→4 | >20→>20 | 0.00→0.00 | 0.00→0.00 | 0.00→0.14 | 0.00→0.30 | 0.05→0.20 |
| q017 | answerable | 4→6 | 3→1 | 0.25→0.50 | 0.33→1.00 | 0.13→0.58 | 0.20→0.50 | 0.25→0.40 |
| q018 | answerable | 5→8 | 7→2 | 0.40→0.62 | 0.14→0.50 | 0.20→0.47 | 0.20→0.70 | 0.20→0.45 |
| q019 | answerable | 5→7 | 1→1 | 0.80→0.86 | 1.00→1.00 | 0.86→0.92 | 0.40→0.60 | 0.30→0.40 |
| q020 | answerable | 8→10 | 2→1 | 0.25→0.40 | 0.50→1.00 | 0.33→0.63 | 0.20→0.60 | 0.30→0.50 |
| q021 | answerable | 7→8 | 3→3 | 0.57→0.62 | 0.33→0.33 | 0.34→0.42 | 0.60→0.70 | 0.40→0.45 |
| q022 | answerable | 5→6 | 1→1 | 0.60→0.67 | 1.00→1.00 | 0.56→0.60 | 0.40→0.50 | 0.20→0.25 |
| q023 | answerable | 1→1 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.73→0.84 | 0.10→0.50 | 0.05→0.25 |
| q024 | answerable | 8→10 | 1→1 | 0.38→0.50 | 1.00→1.00 | 0.48→0.61 | 0.30→0.70 | 0.20→0.40 |
| q025 | answerable | 6→7 | 5→1 | 0.33→0.43 | 0.20→1.00 | 0.20→0.52 | 0.30→0.70 | 0.25→0.45 |
| q026 | answerable | 4→5 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.80→0.82 | 0.40→0.50 | 0.20→0.25 |
| q027 | answerable | 7→8 | 1→1 | 0.57→0.62 | 1.00→1.00 | 0.70→0.74 | 0.40→0.60 | 0.30→0.40 |
| q028 | answerable | 4→8 | 4→1 | 0.75→0.88 | 0.25→1.00 | 0.42→0.82 | 0.30→0.70 | 0.25→0.45 |
| q029 | answerable | 7→8 | 3→3 | 0.29→0.38 | 0.33→0.33 | 0.13→0.28 | 0.30→0.70 | 0.30→0.50 |
| q030 | answerable | 5→7 | 1→1 | 0.20→0.43 | 1.00→1.00 | 0.45→0.71 | 0.10→0.50 | 0.15→0.35 |
| q031 | answerable | 7→8 | 1→1 | 0.43→0.50 | 1.00→1.00 | 0.57→0.64 | 0.40→0.60 | 0.20→0.30 |
| q032 | answerable | 5→7 | 1→1 | 0.60→0.71 | 1.00→1.00 | 0.72→0.84 | 0.30→0.60 | 0.20→0.35 |
| q033 | conflicting | 5→6 | >20→10 | 0.00→0.17 | 0.00→0.10 | 0.00→0.10 | 0.00→1.00 | 0.00→1.00 |
| q034 | answerable | 7→8 | 1→1 | 0.43→0.50 | 1.00→1.00 | 0.51→0.56 | 0.30→1.00 | 0.15→0.50 |
| q035 | answerable | 6→7 | 4→1 | 0.33→0.43 | 0.25→1.00 | 0.36→0.53 | 0.30→0.60 | 0.25→0.40 |
| q036 | answerable | 5→7 | 1→1 | 0.60→0.71 | 1.00→1.00 | 0.44→0.56 | 0.30→0.60 | 0.20→0.35 |
| q037 | answerable | 5→8 | 4→1 | 0.80→0.88 | 0.25→1.00 | 0.43→0.79 | 0.40→0.70 | 0.30→0.45 |
| q038 | answerable | 2→3 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.80→0.86 | 0.20→0.50 | 0.15→0.30 |
| q039 | answerable | 6→7 | 1→1 | 0.33→0.43 | 1.00→1.00 | 0.61→0.69 | 0.20→0.50 | 0.10→0.25 |
| q040 | partial_pool | 4→7 | 11→1 | 0.00→0.43 | 0.09→1.00 | 0.00→0.51 | 0.00→0.50 | 0.15→0.40 |
| q041 | conflicting | 6→9 | >20→4 | 0.00→0.33 | 0.00→0.25 | 0.00→0.29 | 0.00→0.90 | 0.00→0.45 |
| q042 | answerable | 3→8 | 17→1 | 0.00→0.62 | 0.06→1.00 | 0.00→0.56 | 0.00→1.00 | 0.05→0.55 |
| q043 | answerable | 7→7 | 1→1 | 0.71→0.71 | 1.00→1.00 | 0.57→0.59 | 0.50→0.60 | 0.30→0.35 |
| q044 | answerable | 3→4 | 3→1 | 0.33→0.50 | 0.33→1.00 | 0.25→0.64 | 0.10→0.50 | 0.15→0.35 |
| q045 | answerable | 3→6 | 5→2 | 0.67→0.83 | 0.20→0.50 | 0.40→0.71 | 0.20→0.60 | 0.15→0.35 |
| q046 | answerable | 4→4 | 2→2 | 1.00→1.00 | 0.50→0.50 | 0.68→0.69 | 0.60→0.70 | 0.30→0.35 |
| q047 | answerable | 4→4 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.85→0.86 | 0.50→0.70 | 0.25→0.35 |
| q048 | answerable | 7→10 | 2→1 | 0.14→0.40 | 0.50→1.00 | 0.25→0.53 | 0.10→0.50 | 0.10→0.30 |
| q049 | answerable | 5→5 | 1→1 | 0.20→0.20 | 1.00→1.00 | 0.56→0.60 | 0.20→0.50 | 0.10→0.25 |
| q050 | answerable | 4→4 | 2→2 | 0.75→0.75 | 0.50→0.50 | 0.52→0.58 | 0.40→0.60 | 0.25→0.35 |
| q051 | answerable | 5→5 | 1→1 | 0.80→0.80 | 1.00→1.00 | 0.84→0.84 | 0.40→0.50 | 0.20→0.25 |
| q052 | answerable | 7→9 | 3→1 | 0.14→0.33 | 0.33→1.00 | 0.08→0.29 | 0.10→0.50 | 0.10→0.30 |
| q053 | answerable | 6→9 | 6→1 | 0.17→0.44 | 0.17→1.00 | 0.15→0.49 | 0.10→0.60 | 0.10→0.35 |
| q054 | conflicting | 4→5 | >20→17 | 0.00→0.00 | 0.00→0.06 | 0.00→0.18 | 0.00→1.00 | 0.00→1.00 |
| q055 | answerable | 3→7 | 18→1 | 0.00→0.57 | 0.06→1.00 | 0.00→0.76 | 0.10→0.60 | 0.15→0.40 |
| q056 | answerable | 3→4 | 5→5 | 1.00→1.00 | 0.20→0.20 | 0.41→0.63 | 0.30→1.00 | 0.20→0.55 |
| q060 | conflicting | 2→4 | 6→2 | 0.50→0.75 | 0.17→0.50 | 0.27→0.51 | 0.20→0.60 | 0.10→0.30 |
| q063 | answerable | 5→5 | 5→5 | 0.20→0.20 | 0.20→0.20 | 0.15→0.15 | 0.10→1.00 | 0.05→0.50 |
| q064 | answerable | 3→5 | 6→3 | 0.67→0.80 | 0.17→0.33 | 0.30→0.56 | 0.20→0.70 | 0.10→0.35 |
| q065 | answerable | 3→4 | 1→1 | 1.00→1.00 | 1.00→1.00 | 0.97→1.00 | 0.40→0.60 | 0.20→0.30 |
| q066 | answerable | 4→4 | >20→>20 | 0.00→0.00 | 0.00→0.00 | 0.00→0.00 | 0.00→1.00 | 0.00→0.50 |

## 9. Error analysis (tóm tắt; chi tiết: `dense_eval_error_analysis_2026-11-15.md`)
| Câu | Phân loại | Bằng chứng |
|---|---|---|
| q066 động kinh | **Lỗi truy xuất** (nghiêm trọng) | 0 relevant trong top-20. Top-10 là bệnh đồng mắc tâm thần, tic, ADHD. Corpus có 27 chunk về động kinh; 4 chunk đã chấm relevant đều ngoài top-20 |
| q033 can thiệp do cha mẹ thực hiện (PMI) | **Lỗi truy xuất** + nhiễu | Rank 1 = NIMH-ADHD#0008 (điều trị ADHD), rank 2/4/9 = bảng dân số chung, rank 6–8 = quiz. Corpus có 36 chunk PMI ở 12 nguồn, chỉ 3 vào top-20 |
| q063 nhại lời | **Lỗi truy xuất** + boilerplate | Trang "Reprints" ở rank 1 và 3. Định nghĩa và chức năng (NIDCD#0004, PMC12468522#0042) ngoài top-20 |
| q054 tại nhà vs tại trường | Nhiễu + lỗi truy xuất; khoảng trống corpus (so sánh trực tiếp) | 8/10 top là WHO-CST; relevant đầu tiên ở rank 17 |
| q011, q056 dậy thì / masking | Truy xuất **khá**; annotation chưa đủ | Relevant ASD ở rank 1–3 (q011) và 5–8 (q056). PMC12468522#0093 (dậy thì làm triệu chứng nặng hơn) ở rank 11, unjudged. **Đính chính T2.3.2:** masking/camouflaging *có* trong bằng chứng relevant của q056 |
| q050, q051 mốc 15 và 4 tháng | Truy xuất **tốt** | Mốc đúng tuổi ở rank 1–5 |
| q016 joint attention | Chưa đủ dữ liệu, chờ phân xử | Rank 1–2 là 2 chunk `needs_adjudication` |
| q057 vắc-xin | Chưa đủ dữ liệu, chờ phân xử | Xem `dense_eval_q057_sensitivity_2026-11-15.md` |
| Placeholder hình ảnh | Nhiễu nhỏ | 102/2.291 chunk; 39/660 lượt top-10, trong đó 5 lượt grade 0. Không loại bỏ |

Lệch ngôn ngữ truy vấn (tiếng Việt so với tài liệu tiếng Anh) là giả thuyết cho q033, q063 và q066. Giả thuyết này **chưa kiểm chứng được** vì cần embed truy vấn tiếng Anh, tức là phải gọi API (bị cấm trong T2.3.3).

## 10. Giới hạn và nguy cơ thiên lệch
1. **Thiên lệch pool (run B):**
   - Toàn bộ 95 nhãn relevant mới đến từ top-20 dense, nên số liệu B **ưu ái dense**.
   - **Không được** dùng B làm cơ sở so sánh công bằng giữa dense và FTS/hybrid.
   - Run A cũng thiên lệch, nhưng theo hướng khác: nhãn T1 đến từ quá trình tìm kiếm của annotator, không theo một hệ thống cụ thể.
2. **Nhãn silver:** một annotator AI, 0 người xác minh, không có kappa. Grade 1 cho tài liệu dân số chung là quy ước dự án.
3. **Recall chỉ đo trên relevant đã biết.** Còn 791 ứng viên chưa chấm, và chunk ngoài pool chưa từng được xem.
4. **Cỡ mẫu nhỏ:** 55 câu chính; partial_pool có n = 2; conflicting có n = 4. Nhiều CI95 rộng, ví dụ recall@10 A: 0,405–0,573.
5. **Phân xử chưa xong:** q016 (2 chunk), q041 (1 chunk −1), q057 (chunk và nhãn câu).
   - Ảnh hưởng của q057 lên số liệu tổng ≤ 0,012.
   - Nếu q016 được xác nhận thì hit@5/10 của B sẽ thành 0,982.
6. **Bộ đếm `pg_stat` reset khi khởi động lại container.** `n_live_tup` = 0 nên không đếm được số vector của bảng gốc qua role reader. Số hàng trong view (2.291) và bộ đếm ghi (ins/upd/del) không đổi trước/sau, nên **không có thao tác ghi trong lần chạy**. Tổng 2.338 vector của bảng gốc không đọc được bằng role reader. Lần kiểm tra gần nhất bằng owner (`verify_research_access`, 15/11 khi đóng T2.3.2) cho fingerprint DB trùng cuối T2.3.1.

## 11. Bảo mật và tính bất biến (đã chạy)
| Kiểm tra | Kết quả |
|---|---|
| Lệnh gọi API / embedding | **0.** Cache hits 66, misses 0, không có API client |
| Query cache | 66 file, `7038b000…` trước = sau |
| DB fingerprint (role reader): view 2.291 hàng, authorization {2}, MD5 nội dung + vector `8e8bd3bb…` | Trước = sau |
| Ma trận quyền 4 role × 22 relation (`326596…`), thuộc tính role (reader: NOINHERIT, LOGIN, giới hạn 5 kết nối) | Trước = sau |
| Bộ đếm ghi `pg_stat_all_tables` (17 bảng) | Trước = sau (không có insert/update/delete) |
| Session DB | Chỉ `asd_rag_v2_research_reader`, `read_only` |
| Không dùng owner/ingest/app | Đúng. Không chạy `db_check` hay `verify_research_access` bằng owner trong T2.3.3, vì yêu cầu chỉ dùng role reader |
| Dataset gốc / merge | `7704bb51…` / `6bd3ad78…` không đổi; `candidate_judgments.py merge --check` vẫn tái lập được |
| Tái lập | `dense_eval_t2_3_3.py --check`: giống hệt (trừ timestamp/latency); 66/66 danh sách xếp hạng = T2.3.1 |
| Kiểm tra code | `ruff` đạt; `pytest` 174 passed (có 5 test mới cho quy tắc metric); `validate_retrieval_eval` (gốc + merge) đạt; `candidate_judgments validate` đạt |

**File ghi ra trong T2.3.3** (chỉ file, không ghi DB):
- `eval/reports/dense_eval_*_2026-11-15.*`
- log truy xuất `logs/retrieval/dense_eval_t2_3_3_20261115T022955.jsonl` và một log của lần `--check`
- `scripts/dense_eval_t2_3_3.py`, `tests/unit/test_dense_eval_t2_3_3.py`

## 12. Vấn đề chưa giải quyết và điều kiện trước T2.4
| # | Điều kiện | Lý do |
|---|---|---|
| C1 | **Pool công bằng trước khi so FTS/hybrid với dense:** lấy top-k của *mọi* hệ thống (dense, FTS, hybrid), chấm mù các chunk chưa có nhãn, rồi mới so sánh | Số liệu B thiên lệch về dense |
| C2 | So sánh chính dựa trên **run A + nhãn mới từ pool công bằng**. Luôn báo cáo judged coverage@K, precision [lb, ub] và MRR [lb, ub] | Coverage A chỉ 19–36% |
| C3 | Giữ cohort đóng băng (manifest `0d88846e…`). Không suy nhóm câu từ file merge | Nếu suy lại, 55 câu answerable sẽ thành partial_pool |
| C4 | Phân xử q057 (nhãn câu) và q016 (2 chunk) trước khi diễn giải nhóm unanswerable và hit@k của q016. Nếu đổi nhãn thì tạo phiên bản dataset mới | Đang chờ phân xử |
| C5 | Dùng q066, q033, q063, q054 làm **ca kiểm thử bắt buộc** cho T2.4 (FTS/glossary C4), kèm q057, q058, q059 cho evidence gate sau này | Lỗi truy xuất và rủi ro trả lời đã xác định |
| C6 (khuyến nghị) | Chấm thêm các ứng viên rank 6–20 của câu answerable có coverage@20 < 0,5 trước khi báo cáo recall@20 | 45/55 câu ở B vẫn có coverage@20 < 0,5 |
| C7 (khuyến nghị) | Người chấm thứ hai cho mẫu khoảng 60 nhãn (kappa) | Nhãn silver |

## 13. Trả lời các câu hỏi bắt buộc
1. **Mức hoàn thành T2.3.3:** khoảng **95%**. Đã xong R1–R6 và mọi đầu ra. Phần chưa xong nằm ngoài quyền của người đánh giá: phân xử q057 và q016 cần chủ dự án hoặc chuyên gia.
2. **Run A so với T2.3.1:** **không đổi.** Tái lập chính xác: recall@5/10/20 = 0,348 / 0,491 / 0,646; hit = 0,836 / 0,909 / 0,964; MRR = 0,585; source hit = 0,982 / 0,982 / 1,0. 66/66 danh sách xếp hạng giống hệt.
3. **Run B so với A:**
   - recall@5/10/20 tăng +0,125 / +0,115 / +0,070;
   - hit@5 tăng +0,127, hit@20 không đổi;
   - MRR tăng +0,197 (0,585 → 0,782);
   - nDCG@10 tăng 0,440 → 0,608;
   - source recall@10 tăng +0,024.
   Mức tăng chủ yếu do nhãn mới lấy từ top dense, nên **thiên lệch về dense**.
4. **Judged coverage thực tế** (55 câu answerable):

   | K | A | B |
   |---|---|---|
   | 5 | 36,4% | 99,3% |
   | 10 | 27,1% | 64,2% |
   | 20 | 18,9% | 37,5% |

   Micro = macro.
5. **Lỗi quan trọng của dense:**
   - q066 (động kinh): 0 relevant trong top-20, dù corpus có 27 chunk về động kinh;
   - q033 (PMI): ADHD và dân số chung ở top; 33/36 chunk PMI không vào top-20 nào;
   - q063: trang bản quyền ở rank 1 và 3;
   - q054: quiz WHO-CST chiếm top;
   - điểm cosine không tách được câu unanswerable/refusal (q057 0,36; q058 0,40);
   - placeholder là nhiễu nhỏ.
6. **q057:** **chưa giải quyết.** Giữ nhãn unanswerable, trạng thái chờ phân xử. Phân tích độ nhạy cho thấy ảnh hưởng ≤ 0,012 lên số liệu tổng.
7. **API calls / thay đổi DB:** **không có.** 0 lệnh gọi API. Fingerprint view, quyền, role và bộ đếm ghi giống nhau trước/sau. Session chỉ là reader, chỉ đọc.
8. **Đủ điều kiện chuyển T2.4 chưa:** **READY WITH CONDITIONS.** Không tự chuyển.
9. **Điều kiện còn phải xử lý:** C1–C5 (bắt buộc) và C6–C7 (khuyến nghị) ở mục 12. Quan trọng nhất là **pool và chấm công bằng top-k của FTS/hybrid trước khi so với dense**, và phân xử q057/q016.
