# Phase 6.2 – T2.3.2: Annotation Coverage & kết luận — 2026-11-14 (chạy 14–15/11/2026)

**Kết luận: READY WITH CONDITIONS cho T2.3.3** (điều kiện ở mục 8).

| Chỉ số | Giá trị |
|---|---|
| Ứng viên đã có quyết định | **312/1.103**: 303 judged, 4 needs_adjudication, 5 excluded |
| Còn unjudged | **791** |
| Nhãn mới grade ≥ 2 | 95 |
| Câu có thêm bằng chứng relevant | 49 |

Mọi nhãn là **silver**: một annotator AI, 0 người xác minh. Dataset **không đầy đủ**: chỉ phần pool đã chấm được biết, chunk relevant ngoài pool vẫn chưa biết.

## 1. Phân biệt các khái niệm (đọc trước khi dùng số liệu)
| Thuật ngữ | Nghĩa trong báo cáo này | Số lượng |
|---|---|---|
| **found** (tìm thấy) | Chunk nằm trong top-20 dense của T2.3.1 nhưng chưa có nhãn cho câu đó | 1.103 cặp (câu, chunk), 696 chunk khác nhau |
| **judged** (đã chấm) | Có grade cuối (−1..3) và rationale | 303 cặp mới (247 chunk khác nhau); 738 nhãn sau merge |
| **relevant** | Judged với grade ≥ 2 (quy ước schema v1) | 95 cặp mới; 395 nhãn sau merge (300 cũ) |
| **gold** | Relevant **và** được người xác minh | **0**: chưa có nhãn gold nào |
| unjudged / needs_adjudication / excluded | Chưa chấm / có grade tạm, chờ phân xử / loại khỏi chấm (có lý do) | 791 / 4 / 5 |

Unjudged và needs_adjudication **không phải grade 0**. Trong dataset merge chúng nằm ở `candidate_chunk_ids`.

## 2. Tiến độ theo thứ tự ưu tiên
| Ưu tiên (yêu cầu) | Phạm vi | Đã có quyết định |
|---|---|---|
| 1. 246 ứng viên high | 66 câu | **246/246**: 237 judged, 4 adjudication, 5 excluded (q062) |
| 2. q033 và q054 | Toàn bộ pool (15 + 15) | **30/30** |
| 3. Câu nhiều nguồn/nhiều chunk | Lô high đã phủ toàn bộ; không có câu nào thiếu nguồn ≥ 2 theo `requires_multiple_sources` | — |
| 4. Chủ đề yếu | medium của q011 (dậy thì), q015 (AAC), q034 (WHO CST), q041/q042 (cảm giác), q056 (tuổi teen) | 24/24 medium |
| (thêm) Câu chưa có bằng chứng mới | medium của q063 (nhại lời), q066 (động kinh) | 10/10 medium |
| 5. Phần còn lại | medium và low của các câu khác | **Chưa làm**: 791 dòng tồn đọng (214 medium, 577 low) |

## 3. Bao phủ theo câu hỏi
| Chỉ số | Gốc (T1) | Sau merge |
|---|---|---|
| Câu có ≥ 1 chunk grade 2–3 | 62 | 62 (4 câu còn lại: q057, q059 unanswerable; q058 blocked; q062 out of scope) |
| Câu có **thêm** ≥ 1 chunk grade ≥ 2 | — | **49** |
| Câu có thêm nguồn relevant mới | — | 24 |
| Câu có ≥ 2 chunk relevant (multi-chunk) | 61 | 61 (số chunk tăng ở 49 câu) |
| Câu có ≥ 2 nguồn relevant (multi-source) | 54 | 54 |
| Câu có chunk −1 (conflicting) đã merge | 4 | 4. Một −1 mới (q041) còn chờ phân xử |
| Câu cần phân xử | — | 3 câu (q016, q041, q057), 4 chunk |
| Câu unanswerable / blocked / out of scope | 2 / 2 / 1 | Giữ nguyên; q057 có thể đổi nhãn (mục 6) |
| Câu đã chấm hết pool | — | 2 (q033, q054) |
| Câu có `annotation_completeness = partial` | 4 | **63**, vì còn ứng viên chưa chấm (xem rủi ro R2) |
| Nhãn / relevant / chunk relevant khác nhau | 435 / 300 / 238 | 738 / 395 / 315 |

## 4. Bảng theo câu hỏi
"Mới" là số cặp judged trong T2.3.2 có grade ≥ 2 / có grade 3. "Pool" là số dòng T2.3.1 cho câu đó.

| Câu | Answerability | Nhóm T2.3.1 → merge | Pool | Judged | Adj. | Excl. | Unjudged | Relevant gốc → merge | Mới (≥2 / =3) | Nguồn ≥2 gốc → merge |
|---|---|---|---|---|---|---|---|---|---|---|
| q001 | answerable | ans → partial_pool | 19 | 4 | 0 | 0 | 15 | 7 → 9 | 2 / 0 | 4 → 6 |
| q002 | partial | ans → partial_pool | 15 | 4 | 0 | 0 | 11 | 7 → 10 | 3 / 2 | 5 → 7 |
| q003 | answerable | ans → partial_pool | 17 | 3 | 0 | 0 | 14 | 5 → 7 | 2 / 1 | 3 → 4 |
| q004 | answerable | ans → partial_pool | 18 | 4 | 0 | 0 | 14 | 5 → 6 | 1 / 0 | 3 → 3 |
| q005 | answerable | ans → partial_pool | 16 | 4 | 0 | 0 | 12 | 7 → 9 | 2 / 1 | 2 → 2 |
| q006 | partial | ans → partial_pool | 17 | 3 | 0 | 0 | 14 | 3 → 3 | 0 / 0 | 2 → 2 |
| q007 | answerable | ans → partial_pool | 12 | 2 | 0 | 0 | 10 | 4 → 4 | 0 / 0 | 3 → 3 |
| q008 | answerable | ans → partial_pool | 14 | 1 | 0 | 0 | 13 | 7 → 8 | 1 / 0 | 2 → 2 |
| q009 | answerable | ans → partial_pool | 18 | 3 | 0 | 0 | 15 | 4 → 4 | 0 / 0 | 3 → 3 |
| q010 | partial | partial_pool → partial_pool | 18 | 4 | 0 | 0 | 14 | 2 → 4 | 2 / 0 | 2 → 4 |
| q011 | partial | ans → partial_pool | 13 | 5 | 0 | 0 | 8 | 4 → 5 | 1 / 0 | 2 → 2 |
| q012 | partial | ans → partial_pool | 17 | 4 | 0 | 0 | 13 | 3 → 4 | 1 / 1 | 2 → 2 |
| q013 | answerable | ans → partial_pool | 15 | 3 | 0 | 0 | 12 | 5 → 8 | 3 / 2 | 4 → 5 |
| q014 | answerable | ans → partial_pool | 19 | 5 | 0 | 0 | 14 | 7 → 9 | 2 / 0 | 4 → 5 |
| q015 | answerable | ans → partial_pool | 16 | 7 | 0 | 0 | 9 | 4 → 8 | 4 / 2 | 3 → 4 |
| q016 | partial | ans → partial_pool | 19 | 3 | 2 | 0 | 14 | 4 → 4 | 0 / 0 | 3 → 3 |
| q017 | answerable | ans → partial_pool | 15 | 3 | 0 | 0 | 12 | 4 → 6 | 2 / 2 | 2 → 2 |
| q018 | answerable | ans → partial_pool | 16 | 5 | 0 | 0 | 11 | 5 → 8 | 3 / 1 | 3 → 3 |
| q019 | answerable | ans → partial_pool | 14 | 2 | 0 | 0 | 12 | 5 → 7 | 2 / 0 | 5 → 7 |
| q020 | answerable | ans → partial_pool | 14 | 4 | 0 | 0 | 10 | 8 → 10 | 2 / 1 | 1 → 1 |
| q021 | answerable | ans → partial_pool | 12 | 1 | 0 | 0 | 11 | 7 → 8 | 1 / 1 | 2 → 2 |
| q022 | answerable | ans → partial_pool | 16 | 1 | 0 | 0 | 15 | 5 → 6 | 1 / 0 | 2 → 2 |
| q023 | partial | ans → partial_pool | 19 | 4 | 0 | 0 | 15 | 1 → 1 | 0 / 0 | 1 → 1 |
| q024 | answerable | ans → partial_pool | 16 | 4 | 0 | 0 | 12 | 8 → 10 | 2 / 0 | 4 → 5 |
| q025 | answerable | ans → partial_pool | 15 | 4 | 0 | 0 | 11 | 6 → 7 | 1 / 1 | 3 → 3 |
| q026 | answerable | ans → partial_pool | 16 | 1 | 0 | 0 | 15 | 4 → 5 | 1 / 0 | 3 → 4 |
| q027 | answerable | ans → partial_pool | 14 | 2 | 0 | 0 | 12 | 7 → 8 | 1 / 0 | 3 → 4 |
| q028 | answerable | ans → partial_pool | 15 | 4 | 0 | 0 | 11 | 4 → 8 | 4 / 3 | 2 → 2 |
| q029 | answerable | ans → partial_pool | 14 | 4 | 0 | 0 | 10 | 7 → 8 | 1 / 0 | 5 → 5 |
| q030 | answerable | ans → partial_pool | 17 | 4 | 0 | 0 | 13 | 5 → 7 | 2 / 2 | 3 → 3 |
| q031 | answerable | ans → partial_pool | 16 | 2 | 0 | 0 | 14 | 7 → 8 | 1 / 0 | 5 → 6 |
| q032 | answerable | ans → partial_pool | 16 | 3 | 0 | 0 | 13 | 5 → 7 | 2 / 0 | 3 → 4 |
| q033 | answerable | conflicting → conflicting | 20 | 20 | 0 | 0 | 0 | 5 → 6 | 1 / 0 | 4 → 4 |
| q034 | answerable | ans → partial_pool | 17 | 7 | 0 | 0 | 10 | 7 → 8 | 1 / 0 | 2 → 2 |
| q035 | answerable | ans → partial_pool | 15 | 3 | 0 | 0 | 12 | 6 → 7 | 1 / 0 | 2 → 3 |
| q036 | answerable | ans → partial_pool | 16 | 3 | 0 | 0 | 13 | 5 → 7 | 2 / 0 | 2 → 2 |
| q037 | answerable | ans → partial_pool | 14 | 3 | 0 | 0 | 11 | 5 → 8 | 3 / 1 | 2 → 2 |
| q038 | answerable | ans → partial_pool | 17 | 3 | 0 | 0 | 14 | 2 → 3 | 1 / 0 | 2 → 3 |
| q039 | answerable | ans → partial_pool | 18 | 3 | 0 | 0 | 15 | 6 → 7 | 1 / 0 | 4 → 4 |
| q040 | partial | partial_pool → partial_pool | 17 | 5 | 0 | 0 | 12 | 4 → 7 | 3 / 1 | 2 → 2 |
| q041 | answerable | conflicting → conflicting | 20 | 9 | 1 | 0 | 10 | 6 → 9 | 3 / 2 | 4 → 4 |
| q042 | partial | ans → partial_pool | 19 | 10 | 0 | 0 | 9 | 3 → 8 | 5 / 2 | 3 → 6 |
| q043 | answerable | ans → partial_pool | 14 | 1 | 0 | 0 | 13 | 7 → 7 | 0 / 0 | 1 → 1 |
| q044 | answerable | ans → partial_pool | 17 | 4 | 0 | 0 | 13 | 3 → 4 | 1 / 1 | 1 → 1 |
| q045 | answerable | ans → partial_pool | 17 | 4 | 0 | 0 | 13 | 3 → 6 | 3 / 2 | 1 → 1 |
| q046 | answerable | ans → partial_pool | 14 | 1 | 0 | 0 | 13 | 4 → 4 | 0 / 0 | 1 → 1 |
| q047 | answerable | ans → partial_pool | 15 | 2 | 0 | 0 | 13 | 4 → 4 | 0 / 0 | 1 → 1 |
| q048 | answerable | ans → partial_pool | 18 | 4 | 0 | 0 | 14 | 7 → 10 | 3 / 0 | 2 → 4 |
| q049 | answerable | ans → partial_pool | 18 | 3 | 0 | 0 | 15 | 5 → 5 | 0 / 0 | 1 → 1 |
| q050 | answerable | ans → partial_pool | 15 | 2 | 0 | 0 | 13 | 4 → 4 | 0 / 0 | 2 → 2 |
| q051 | partial | ans → partial_pool | 16 | 1 | 0 | 0 | 15 | 5 → 5 | 0 / 0 | 2 → 2 |
| q052 | answerable | ans → partial_pool | 18 | 4 | 0 | 0 | 14 | 7 → 9 | 2 / 0 | 6 → 7 |
| q053 | answerable | ans → partial_pool | 18 | 5 | 0 | 0 | 13 | 6 → 9 | 3 / 0 | 5 → 6 |
| q054 | partial | conflicting → conflicting | 20 | 20 | 0 | 0 | 0 | 4 → 5 | 1 / 0 | 3 → 4 |
| q055 | answerable | ans → partial_pool | 17 | 5 | 0 | 0 | 12 | 3 → 7 | 4 / 3 | 3 → 3 |
| q056 | partial | ans → partial_pool | 16 | 7 | 0 | 0 | 9 | 3 → 4 | 1 / 0 | 2 → 3 |
| q057 | unanswerable | unans → unans | 20 | 9 | 1 | 0 | 10 | 0 → 0 | 0 / 0 | 0 → 0 |
| q058 | blocked | refusal → refusal | 19 | 9 | 0 | 0 | 10 | 0 → 0 | 0 / 0 | 0 → 0 |
| q059 | unanswerable | unans → unans | 20 | 10 | 0 | 0 | 10 | 0 → 0 | 0 / 0 | 0 → 0 |
| q060 | answerable | conflicting → conflicting | 18 | 4 | 0 | 0 | 14 | 2 → 4 | 2 / 0 | 2 → 3 |
| q061 | blocked | refusal → refusal | 19 | 9 | 0 | 0 | 10 | 3 → 4 | 1 / 0 | 3 → 3 |
| q062 | out_of_scope | oos → oos | 20 | 0 | 0 | 5 | 15 | 0 → 0 | 0 / 0 | 0 → 0 |
| q063 | answerable | ans → partial_pool | 19 | 9 | 0 | 0 | 10 | 5 → 5 | 0 / 0 | 5 → 5 |
| q064 | answerable | ans → partial_pool | 18 | 5 | 0 | 0 | 13 | 3 → 5 | 2 / 0 | 3 → 4 |
| q065 | answerable | ans → partial_pool | 16 | 2 | 0 | 0 | 14 | 3 → 4 | 1 / 0 | 2 → 3 |
| q066 | answerable | ans → partial_pool | 20 | 10 | 0 | 0 | 10 | 4 → 4 | 0 / 0 | 2 → 2 |

## 5. Phân bố grade

**Nhãn mới T2.3.2 (303 judged):**

| Grade | Số lượng |
|---|---|
| 3 | 32 |
| 2 | 63 |
| 1 | 88 |
| 0 | 120 |
| −1 | 0 |

Thêm 4 nhãn tạm đang chờ phân xử: 2, 2, −1, 1.

**Toàn bộ dataset sau merge (738 nhãn):**

| Grade | Số lượng |
|---|---|
| 3 | 146 |
| 2 | 249 |
| 1 | 154 |
| 0 | 184 |
| −1 | 5 |

**Theo nguồn (nhãn mới, các nguồn có từ 4 nhãn):**
| Nguồn | 3 | 2 | 1 | 0 | Relevant |
|---|---|---|---|---|---|
| WHO-CST-PARTICIPANTS-2022 | 1 | 3 | 7 | 15 | 4 |
| ASD-NEW-002 (can thiệp nuôi dạy, dân số chung) | 0 | 0 | 7 | 12 | 0 |
| ASD-OA-PMC12620806 (tổng quan bệnh đồng mắc) | 4 | 3 | 2 | 9 | 7 |
| ASD-OA-PMC13005892 (tự kỷ ở Việt Nam) | 1 | 1 | 4 | 11 | 2 |
| ASD-OA-PMC7407189 (giấc ngủ) | 1 | 6 | 2 | 6 | 7 |
| ASD-OA-PMC9003052 (tiêu hoá) | 2 | 3 | 4 | 4 | 5 |
| NIHR-SENITA-2022 | 5 | 1 | 4 | 2 | 6 |
| CDC-MILESTONES-36 | 0 | 2 | 3 | 5 | 2 |
| WHO-ECD-GUIDELINE-2020 | 0 | 0 | 5 | 5 | 0 |
| NIH-NIMH-ADHD | 0 | 0 | 1 | 8 | 0 |
| NIH-NIMH-TEEN-BRAIN | 0 | 0 | 7 | 1 | 0 |
| CDC-ASD-CLINICAL | 1 | 3 | 3 | 0 | 4 |
| ASD-SUP-PMC7726187 | 1 | 2 | 3 | 1 | 3 |
| ASD-SUP-PMC6590432 | 1 | 1 | 0 | 5 | 2 |
| ASD-CSV-091 (sàng lọc) | 0 | 5 | 0 | 1 | 5 |
| ASD-NEW-003 | 1 | 3 | 2 | 0 | 4 |
| ASD-CSV-038 (tỷ lệ ASD ở Việt Nam) | 3 | 1 | 0 | 0 | 4 |

Nguồn hay gây nhiễu nhất (grade 0 nhiều, relevant ít) là NIMH-ADHD, ASD-NEW-002, phần quiz của WHO-CST và các bảng/thư biên tập. Chi tiết hard negative ở báo cáo chất lượng, mục 5.

## 6. Câu còn thiếu bằng chứng và lỗ hổng chủ đề
Mọi câu answerable hoặc partially answerable đều có ≥ 1 chunk relevant từ T1. Các lỗ hổng dưới đây là phần **phạm vi trả lời** mà pool dense chưa bổ sung được:

| Câu | Phạm vi còn thiếu | Bằng chứng tìm thấy trong pool |
|---|---|---|
| q011 tuổi dậy thì | Thay đổi cơ thể, giới tính, vệ sinh riêng **ở trẻ tự kỷ** | Chỉ NDD vị thành niên nói chung (PMC12593641#0005) và teen nói chung (grade 1) |
| q056 tâm lý tuổi teen | **Nguỵ trang (masking)**; lo âu/trầm cảm riêng ASD ở tuổi teen | Một chunk khí sắc/catatonia (grade 2); còn lại là teen nói chung |
| q050 trẻ 15 tháng chưa nói | Mốc ngôn ngữ 15 tháng + khi nào cần đi khám | Mốc nhận thức và mẹo, không có grade ≥ 2 mới |
| q051 dấu hiệu chậm ở 4 tháng | Mốc 4 tháng / dấu hiệu cảnh báo | Chỉ mẹo hoạt động (grade 0) |
| q063 nhại lời (echolalia) | Chức năng của echolalia | 9 ứng viên high + medium đều grade 0; top dense bị chiếm bởi trang mốc và bản quyền |
| q066 động kinh | Tỷ lệ động kinh, liên hệ mức độ | 10 ứng viên high + medium đều grade 0 (bệnh đồng mắc tâm thần, tic); dense nhầm "comorbidity" |
| q054 tại nhà vs tại trường | So sánh trực tiếp | Không có (đúng với nhãn partially answerable); thêm bằng chứng riêng cho PMI (NEW-003#0044) |
| q049 khuyến nghị WHO ECD | Nội dung khuyến nghị chính | Pool chỉ có phụ lục và danh sách; khuyến nghị chính đã có từ T1 |
| q057 vắc-xin | — | **Có thể không còn là unanswerable**: PMC12620806#0021 nói giả thuyết đến từ nghiên cứu đã bị rút → cần phân xử |

**Chủ đề yếu so với trước:**
- **Đã cải thiện:**
  - AAC: q015 có 4 chunk relevant mới, gồm so sánh AAC với NDBI (CSV-017#0040).
  - Tích hợp cảm giác: q041 có 3 mới, q042 có 5 mới, gồm phân biệt ASI với SBI (SENITA#0045).
  - Kén ăn–tiêu hoá: q055 có 4 mới.
- **Vẫn yếu:**
  - Can thiệp do cha mẹ thực hiện: pool dense chủ yếu kéo tài liệu dân số chung (ASD-NEW-002, WHO-ECD); chỉ có thêm 1 relevant (CSV-018#0018).
  - Tuổi dậy thì và masking.
  - Nhóm tuổi 4 và 15 tháng.
  - Động kinh.

## 7. Trả lời tám câu hỏi bắt buộc
1. **Đã chấm bao nhiêu ứng viên?** 312/1.103 có quyết định: 303 judged với grade cuối, 4 needs_adjudication, 5 excluded. Có 247 chunk khác nhau được chấm.
2. **Số lượng theo grade:** 3 → 32 · 2 → 63 · 1 → 88 · 0 → 120 · −1 → 0. Ngoài ra có 1 nhãn −1 tạm trong nhóm chờ phân xử.
3. **Còn bao nhiêu chưa chấm?** 791: 214 medium và 577 low. Toàn bộ lô high đã chấm.
4. **Bao nhiêu câu có bằng chứng đầy đủ hơn?** 49 câu có thêm ≥ 1 chunk grade ≥ 2 (tổng 95 cặp; 20 câu có thêm chunk grade 3). 24 câu có thêm nguồn relevant mới.
5. **Câu nào còn thiếu bằng chứng?** Không câu answerable nào mất bằng chứng. Phạm vi còn thiếu ở q011, q056, q050, q051, q063, q066 và q054 (không có so sánh trực tiếp). q057 cần quyết định lại nhãn. Chi tiết ở mục 6.
6. **Cần bao nhiêu adjudication?** 4 chunk (q016 ×2, q041, q057) và 1 nhãn cấp câu hỏi (answerability của q057). Xem `phase_6_2_t2_3_2_unresolved_adjudications_2026-11-14.csv`.
7. **Đã sẵn sàng re-evaluate dense chưa?** Sẵn sàng **có điều kiện**. Dataset merge hợp lệ, tái lập được và không mất nhãn cũ, nhưng phải xử lý R1–R4 dưới đây trước hoặc trong lúc chạy T2.3.3.
8. **Rủi ro cần giải quyết trước T2.3.3:** xem mục 8.

## 8. Rủi ro và điều kiện cho T2.3.3
| # | Rủi ro | Điều kiện |
|---|---|---|
| R1 | ~~Chưa chạy kiểm tra DB~~ **Đã xử lý 15/11/2026:** `db_check` ok, `verify_research_access` 74/74, fingerprint DB giống cuối T2.3.1 | Chạy lại ngay trước T2.3.3 |
| R2 | **Nhóm câu bị dịch chuyển:** do còn ứng viên chưa chấm, `annotation_completeness` thành `partial` ở 63 câu. Hàm `group_of` của `dense_retrieval_eval.py` sẽ chuyển 55 câu answerable sang `answerable_partial_pool`, làm số liệu không so được với T2.3.1 | T2.3.3 cố định nhóm theo T2.3.1 (danh sách `question_id` theo nhóm trong metrics T2.3.1) hoặc dùng `answerability`, và báo cáo cả hai cách |
| R3 | **Thiên lệch pool:** 95/95 nhãn relevant mới đến từ top-20 dense (81 ở rank ≤ 5). Recall/nDCG của dense trên nhãn merge sẽ được lợi so với retriever chưa được pool | Báo cáo song song metric trên nhãn gốc (`7704bb51…`) và nhãn merge (`6bd3ad78…`). Khi so với FTS/hybrid, phải pool và chấm top-k của mọi hệ thống ngang nhau |
| R4 | 791 ứng viên chưa chấm nên metric vẫn là **cận dưới** | Báo cáo `judged_coverage@k`; không gọi metric là "đầy đủ" |
| R5 | q057 có thể đổi nhãn unanswerable | Quyết định trước khi diễn giải nhóm unanswerable; nếu đổi thì tạo phiên bản dataset mới, không sửa file gốc |
| R6 | Silver, một annotator AI, kappa không xác định | Ghi rõ trong mọi báo cáo metric; lên kế hoạch cho người chấm mẫu khoảng 60 nhãn |

**Không làm trong T2.3.2** (đúng phạm vi):
- Không đổi retriever hay Top-K; không dùng FTS, hybrid, reranker hay query expansion.
- Không gọi Cohere hay API embedding.
- Không ghi DB, không đổi authorization, migration hay quyền.
- Không dùng owner/ingest để đọc chunk.
- Không dùng git.

## 9. File tạo ra trong T2.3.2
- `eval/datasets/retrieval_eval_v1_candidate_judgments_2026-11-14.jsonl` và `…_candidate_judgments_schema.json`
- `eval/datasets/retrieval_eval_v1_merged_2026-11-14.jsonl`
- `backups/datasets/retrieval_eval_v1_pre_t2_3_2_2026-11-15.jsonl`
- `scripts/candidate_judgments.py`, `tests/unit/test_candidate_judgments.py`
- Báo cáo:
  - `phase_6_2_t2_3_2_preannotation_audit_2026-11-14.md`
  - báo cáo này
  - `…_annotation_quality_report_…md`
  - `…_unresolved_adjudications_…csv`
  - `…_dataset_validation_…md` và `.json`
