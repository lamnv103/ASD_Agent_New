# Phase 6.2 – T2.3.1: Dense Retrieval Baseline — 2026-11-14

**Kết luận: READY FOR T2.3.2.**

Dense retriever đã hoạt động đúng:
- truy xuất qua role reader và view được cấp quyền, lọc trước LIMIT;
- provenance được kiểm từng kết quả; lỗi xử lý theo kiểu fail-closed;
- 144 unit + 33 integration test, kiểm tra bảo mật 74/74, `db_check` 66/66;
- fingerprint không đổi;
- baseline tái lập được: lần chạy lại offline trùng hệt lần đầu và không gọi API.

**Metric chỉ là baseline thăm dò trên nhãn SILVER, không phải hiệu năng gold.** Chúng bị đánh giá thấp có hệ thống do pool nhãn chưa đủ (mục 6).

## 1. Kiến trúc thực tế
```
question_vi ──validate──► CachedQueryEmbedder ──(miss & --allow-api)──► CohereQueryEmbedder ──► Cohere /v2/embed
                          (data/index/query_embeddings, khoá sha256)        embed-v4.0, search_query, 1536
            ──► check: 1536 chiều, hữu hạn, đúng profile
            ──► ResearchVectorReader  [connect("research_reader") · assert current_user · read_only]
                  SELECT …, embedding <=> %(q)s::vector AS distance
                  FROM asd_rag.v_research_retrieval_chunks WHERE profile_code = %(profile)s
                  ORDER BY embedding <=> %(q)s::vector LIMIT %(k)s          (C5 nằm trong view)
            ──► kiểm provenance từng hàng (id, page/char range, sha256(content), model/chiều/profile,
                một authorization) → RetrievalResponse
            ──► log JSONL (logs/retrieval/, chỉ hash của câu hỏi)
```

| Thành phần | File |
|---|---|
| Cấu hình | `config/retrieval_profiles.json` → `dense_baseline_v1` (profile, view, metric, `k_default 10`, `k_max 50`, `k_probe [5, 10, 20]`, `max_query_chars 1000`, `query_expansion false`) |
| Schema kết quả + lỗi | `app/retrieval/types.py` (`RetrievedChunk`, `RetrievalResponse`, `RetrievalError` với 14 nhóm lỗi) |
| Adapter query embedding | `app/retrieval/query_embedding.py` (`CohereQueryEmbedder`, `CachedQueryEmbedder` — mặc định offline) |
| Reader DB | `app/retrieval/research_reader.py` (SQL cố định; view và toán tử lấy từ whitelist; tham số được bind) |
| Service | `app/retrieval/dense.py` (`retrieve`, và `retrieve_by_vector` cho fixture/đánh giá) |
| Log | `app/retrieval/audit_log.py` (JSONL, chặn các khoá nhạy cảm) |
| Đánh giá | `scripts/dense_retrieval_eval.py` (mặc định offline; `--allow-api --max-api-inputs N`) |
| Test | `tests/unit/test_dense_retrieval.py` (43), `tests/integration/test_dense_retrieval_db.py` (9) |

Không sửa file có sẵn nào (đã đối chiếu hash). Không có FTS, hybrid, RRF, reranker, evidence gate, LLM, router hay query expansion.

## 2. File đã đọc
Xem [pre-implementation review](phase_6_2_t2_3_1_preimplementation_review_2026-11-14.md), mục 1.

## 3. Model, profile, SQL, authorization
| Mục | Giá trị (đã xác minh) |
|---|---|
| Embedding | `cohere_embed_v4_1536_v1`: `embed-v4.0`, 1536 chiều, câu hỏi `search_query` / tài liệu `search_document`, `output_dimension = 1536`, `float` |
| Chuẩn hoá | vector tài liệu: L2 norm 0,9999999–1,0000001; vector câu hỏi: L2 norm 1,000000 (66/66) |
| Metric | cosine; `<=>` là cosine distance, khoảng [0, 2], càng nhỏ càng gần |
| Điểm trả về | `score_type = "cosine_distance"`, `score = distance`, `cosine_similarity = 1 − distance` (khoảng [−1, 1]). Không điểm nào là xác suất |
| Tìm kiếm | exact, không có chỉ mục ANN |
| Authorization | phiên bản **2** (mọi kết quả của 66 truy vấn) |
| Corpus version | `section_v2_1@<document_version>` |
| Role | `asd_rag_v2_research_reader`. Mọi kết nối khác bị từ chối (`wrong_role`) |

## 4. Kiểm thử (đã chạy thật)
| Nhóm | Kết quả |
|---|---|
| E1 Unit (43) | kiểm tra câu hỏi (rỗng, kiểu, độ dài); K (0, −1, > max, float, bool, str); lệch profile; lệch chiều; lỗi embedding; SQL tham số hoá (chỉ một `FROM` là view, không JOIN, `ORDER BY` trước `LIMIT`, không chèn text); view/metric lạ bị từ chối; reader đặt read-only và kiểm `current_user`; 5 loại lỗi DB ánh xạ fail-closed; không fallback khi mất kết nối; schema và ngữ nghĩa điểm; định dạng trang; 8 kiểu provenance hỏng làm hỏng **cả** response; trộn authorization; không có kết quả; log không chứa câu hỏi; adapter Cohere gửi `search_query`/1536 (transport giả); lỗi 401 → `embedding_failed`; cache offline và không lưu text; cache của profile khác bị từ chối |
| E2 Integration (9, DB thật, role reader, vector fixture, **không API**) | phạm vi view = 2.291; **top-5/10/20 khớp phép tính cosine brute-force độc lập bằng Python** trên cả 2.291 vector (5 fixture × 3 K); top-1 là chính chunk đó (distance ≈ 0); distance tăng dần; provenance hợp lệ (hash, trang/khoảng ký tự, URL, model, authorization 2); vector của chunk D-1 → 20 kết quả, 0 chunk D-1; phiên chạy là reader với read-only; reader bị từ chối khi đọc bảng gốc; reader từ chối kết nối của role ingest (`wrong_role`); truy vấn văn bản không có cache và không có phép gọi API → `embedding_unavailable` |
| E3 Security | `verify_research_access.py` (DB thật) **74/74**; `db_check` **66/66** |
| E4 Integrity | fingerprint (chunk, vector, schema, view production, view 006, ACL app/ingest/owner/PUBLIC, role, authorization, migration) **giống hệt** giữa cuối T2, đầu T2.3.1 và sau baseline; `ingestion_runs` 17 → 17; `retrieval_logs` 0 → 0; raw 199/199 |
| E5 Regression | ruff sạch; unit **144/144**; integration **33/33**; validator dataset PASS (SHA `7704bb51…`, không sửa) |

## 5. Baseline (thăm dò, nhãn SILVER)
- **API (đã được phê duyệt):** 1 lời gọi, **66 input** (chỉ `question_vi`), 953 token tính phí. Vector được cache, nên lần chạy lại dùng **0** lời gọi.
- **Latency:**
  - embed theo lô: 1,85 s cho 66 câu;
  - DB mỗi truy vấn: trung vị **104 ms**, p95 119 ms, max 123 ms (exact scan qua view có JOIN và `security_barrier`).

### 5.1 Quy tắc tính
- **Gold:** chunk đã chấm có grade ≥ 2 **và** đang truy xuất được (authorization 2). Không có chunk gold nào bị loại bởi D-1.
- **Chunk chưa chấm không bao giờ bị coi là không liên quan.** Vì vậy:
  - `precision_lb` và `ndcg_lb` là **cận dưới**;
  - báo cáo kèm `judged_precision` (chỉ trên các chunk đã chấm) và `judged_coverage`.
- **Gain cho nDCG:** 3/2/1/0; grade −1 có gain 2 (theo schema). IDCG tính từ mọi chunk đã chấm còn truy xuất được.
- **Nhóm câu hỏi:**
  - `answerable` (55): metric chính;
  - `answerable_partial_pool` (q010, q040), `conflicting` (q033, q041, q054, q060): báo cáo riêng;
  - `unanswerable` (q057, q059), `refusal` (q058, q061), `out_of_scope` (q062): **không** tính recall/precision, chỉ báo độ tương đồng top-1.
- **Khoảng tin cậy:** CI 95% bootstrap (2.000 lần lặp, seed cố định), lấy trung bình theo câu hỏi.

### 5.2 Kết quả: nhóm answerable (n = 55)
| Metric | @5 | @10 | @20 |
|---|---|---|---|
| Recall (chunk) | **0,348** [0,275–0,423] | **0,491** [0,405–0,573] | **0,646** [0,564–0,720] |
| Hit rate (≥ 1 chunk gold) | 0,836 | 0,909 | 0,964 |
| nDCG (cận dưới) | 0,381 | 0,428 | 0,490 |
| Precision (cận dưới, chưa chấm = 0) | 0,316 | 0,227 | — |
| Judged precision (chỉ trên chunk đã chấm) | 0,894 (n = 47) | — | — |
| Judged coverage (tỉ lệ top-k đã chấm) | **0,36** | 0,27 | **0,19** |
| Source hit (≥ 1 nguồn gold) | 0,982 | 0,982 | 1,000 |
| Source recall | 0,632 | 0,737 | 0,824 |
| MRR@20 | **0,585** [0,483–0,684] | | |

Hạng của chunk gold đầu tiên: hạng 1 ở 24 câu, hạng 2–5 ở 22 câu, > 5 ở 7 câu, không có trong top-20 ở 2 câu (q016, q066).

Theo nhóm câu hỏi (recall@10 / recall@20 / MRR):

| Nhóm | Số câu | recall@10 | recall@20 | MRR |
|---|---:|---:|---:|---:|
| repetitive_restricted | 5 | 0,64 | 0,84 | 0,77 |
| signs_symptoms | 6 | 0,55 | 0,78 | 0,50 |
| sensory | 4 | 0,43 | 0,71 | 0,40 |
| intervention_support | 8 | 0,57 | 0,68 | 0,81 |
| development_milestones | 6 | 0,65 | 0,67 | 0,75 |
| assessment_diagnosis | 9 | 0,50 | 0,65 | 0,64 |
| multi_aspect | 4 | 0,33 | 0,57 | 0,19 |
| basic_knowledge | 6 | 0,42 | 0,52 | 0,67 |
| social_communication | 5 | 0,33 | 0,47 | 0,34 |
| aac_communication_support | 2 | 0,20 | 0,32 | 0,25 |

Mỗi nhóm chỉ có 2–9 câu, nên đây là chỉ báo, không phải kết luận.

### 5.3 Các nhóm khác
| Nhóm | Kết quả |
|---|---|
| Partial pool (2) | recall@20 lần lượt 1,0 (q010) và 0,5 (q040) |
| Conflicting (4) | recall@20 = 0,125. q033, q041, q054: 0 chunk đã chấm trong top-20 (judged coverage = 0). q060: recall 0,5 và **bao phủ chunk −1 = 1,0**. Source hit@20 = 1,0, tức là đã tìm đúng nguồn nhưng đều là chunk chưa chấm |
| Unanswerable | độ tương đồng top-1: q057 vắc-xin 0,359; q059 tế bào gốc 0,316 |
| Refusal | q058 0,398; q061 0,453 |
| Out of scope | q062 thời tiết 0,226 |
| So sánh | top-1 của nhóm answerable: trung vị 0,464 (min 0,280, max 0,592). **Hai phân bố chồng lên nhau**, nên một ngưỡng similarity đơn lẻ **không** đủ làm evidence gate |

## 6. Diễn giải và giới hạn
1. **Nhãn SILVER:** một người gán, là AI, chưa có người xác minh. Không có kết luận gold.
2. **Pool chưa đủ, thiên lệch lexical:**
   - Chỉ 19% top-20 (36% top-5) đã được chấm.
   - Judged precision@5 = 0,89 cho thấy khi một chunk đã được chấm, nó thường liên quan.
   - Source hit@5 = 0,98, cao hơn hẳn recall chunk.
   - Ví dụ: q041 (tích hợp cảm giác) lấy đúng 3 nguồn kỳ vọng (SUP-PMC12658592, SENITA, SUP-PMC7726187) nhưng đều là chunk chưa chấm.

   Recall, precision và nDCG ở mức chunk vì vậy là **cận dưới**. Cần chấm pool (mục 7) trước khi so sánh với FTS hoặc hybrid.
3. **Lỗi thật của dense (định tính):**
   - **q033** "can thiệp do cha mẹ" → top-1 là chunk ADHD của NIMH ("parents play an active role"), đúng chủ đề cha mẹ nhưng sai bệnh.
   - **q054** → hạng 2 là boilerplate sổ tay WHO "Only check the answers…".
   - **q066** "động kinh" → các bảng bệnh đi kèm tâm thần trả về trước; nguồn đúng (PMC12620806) chỉ ở hạng 3, và là chunk về tic.
   - **q016** "chú ý chung" → các ví dụ "shared engagement" của WHO-CST (có thể liên quan nhưng chưa chấm).
4. **Thuật ngữ tiếng Việt:** câu q041 dùng "liệu pháp **điều hoà** cảm giác", trong khi tài liệu dùng "sensory integration" (tích hợp cảm giác). Đây là dữ liệu đầu vào cho glossary C4, chưa được dùng ở baseline này.
5. **Tập trung nguồn và boilerplate (66 câu × top-5):**
   - Nguồn xuất hiện nhiều nhất: WHO-CST-PARTICIPANTS 21 lần, PMC12620806 17, PMC7407189 17.
   - Placeholder "Image:" 8 lần, "Only check the answers" 2, "[Original asset" 1.
   - Trung vị chỉ 4 nguồn khác nhau trong top-10 (thấp nhất 1).
6. **Latency** ~100 ms/truy vấn với exact scan 2.291 vector. Chưa cần chỉ mục ANN; chưa tối ưu (đúng chủ trương).

## 7. Mở rộng candidate pool
| Mục | Giá trị |
|---|---|
| File | [phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv](phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv) |
| Quy mô | **1.103 dòng**: top-20 chưa chấm của 66 câu, 696 chunk khác nhau |
| Cột | `question_id`, `question_group`, `chunk_id`, `source_id`, `rank`, `cosine_distance`, `cosine_similarity`, `current_annotation_status = unjudged`, `suggested_review_priority` |
| Ưu tiên | high = hạng ≤ 5, hoặc hạng ≤ 10 với câu unanswerable/refusal (có thể làm lộ bằng chứng có thật): **246** · medium = hạng 6–10: **260** · low: **597** |

Dataset gốc **không** bị sửa. Các chunk trong pool chưa được gán là không liên quan.

## 8. Logging
- Hiện ghi JSONL vào `logs/retrieval/` (git-ignore), 66 bản ghi `status = ok` cho mỗi lần chạy. Mỗi bản ghi có `request_id`, `question_id`, `query_sha256`, profile, `query_expansion = false`, authorization, k, danh sách chunk (hạng và distance), latency.
- **Không** ghi câu hỏi gốc, mật khẩu hay key. Module log từ chối các khoá `query`, `question_vi`, `content`, `api_key`…
- Lỗi được ghi với `error_category`.
- **Không** dùng `retrieval_logs`: chỉ role `app` được INSERT, và mình không mở thêm quyền cho reader.
- Đề xuất (cần phê duyệt riêng): một role ghi log nghiên cứu riêng, chỉ có INSERT trên một bảng log nghiên cứu, tạo bằng migration mới.

## 9. Fingerprint và bảo mật
- **Fingerprint:** giống hệt trước và sau ở mọi mục; chi tiết ở E4.
- **Bảo mật:** reader chỉ đọc được view. Kết quả của 66 truy vấn có **0 chunk D-1**, một authorization duy nhất (2), và không có kết nối nào ngoài role reader.

## 10. Tiêu chí nghiệm thu
| ID | Kết quả | Bằng chứng |
|---|---|---|
| AC01 | ✔ | profile, model, chiều, metric được xác minh từ DB + config (mục 3) |
| AC02 | ✔ | `search_query`, `output_dimension = 1536` (unit test với transport giả); 66 vector thật 1536 chiều, hữu hạn, norm 1,0 |
| AC03 | ✔ | kiểm `current_user`; từ chối `wrong_role` |
| AC04 | ✔ | SQL chỉ có một `FROM` là view (unit); reader bị từ chối khi đọc bảng gốc (integration) |
| AC05 | ✔ | top-k khớp brute-force độc lập; `ORDER BY distance` rồi `LIMIT` |
| AC06 | ✔ | C5 trong view; 74/74 kiểm tra bảo mật; một authorization |
| AC07 | ✔ | 0 chunk D-1 trong 66 × 20 kết quả và trong test vector D-1 |
| AC08 | ✔ | kiểm provenance từng hàng (hash, trang/khoảng ký tự, model, chiều, profile) |
| AC09 | ✔ | K = 5/10/20 trong integration và evaluation |
| AC10 | ✔ | 14 nhóm lỗi, không fallback, không trả kết quả một phần |
| AC11 | ✔ | unit 144, integration 33, bảo mật 74/74, `db_check` 66/66 |
| AC12 | ✔ | fingerprint giống hệt |
| AC13 | ✔ | silver, cận dưới, judged coverage và các nhóm được nêu rõ |
| AC14 | ✔ | 1.103 ứng viên kèm mức ưu tiên |
| AC15 | ✔ | không đổi production, authorization, migration hay quyền |

## 11. Vấn đề chưa giải quyết và việc tiếp theo
1. **Chấm candidate pool**, ưu tiên 246 dòng high. Nên có người đánh giá là con người để bắt đầu nâng lên gold. Chưa xong việc này thì không so sánh dense với FTS hay hybrid bằng metric ở mức chunk.
2. **Boilerplate trong index** (placeholder "Image:", câu tự kiểm tra của WHO-CST, footer CDC): ứng viên cho một D-2 theo đúng cơ chế authorization revision, cần duyệt riêng.
3. Glossary C4 (T2.3.x) nên gồm các cặp như "điều hoà cảm giác / tích hợp cảm giác" → "sensory integration". Mọi thuật ngữ phải được kiểm là có trong corpus.
4. **Evidence gate:** độ tương đồng top-1 của câu unanswerable/refusal chồng lên câu answerable, nên ngưỡng đơn thuần không đủ.
5. `scripts/embed_research.py` vẫn cần cập nhật theo ngữ nghĩa authorization mới (tồn đọng từ T2).
6. Luồng log DB cho nghiên cứu: cần phê duyệt (mục 8).

## 12. File đầu ra
- `phase_6_2_t2_3_1_dense_retrieval_metrics_2026-11-14.json`: lần chạy đầu, có gọi API.
- `phase_6_2_t2_3_1_dense_retrieval_metrics_2026-11-14_r2.json`: chạy lại offline, **thêm metric ở mức nguồn**.
  - Thứ hạng, metric ở mức chunk và pool trùng hệt lần đầu.
  - 0 lời gọi API.
- `phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv`, cùng bản `_r2` trùng SHA-256.
- Log: `logs/retrieval/dense_eval_20261114T153253.jsonl` (lần 1), `…T153403.jsonl` (lần 2).
- Cache vector câu hỏi: `data/index/query_embeddings/` (66 file, không chứa câu hỏi dạng văn bản, git-ignore).
