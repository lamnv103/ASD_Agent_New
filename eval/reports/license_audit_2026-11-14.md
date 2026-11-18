# License & rights audit — 2026-11-14

Phạm vi: 73 tài liệu toàn văn (core 33 + gaps 40). Không ghi DB, không gửi nội dung ra ngoài. Đây là thu thập bằng chứng kỹ thuật, **không phải tư vấn pháp lý**; mọi cờ quyền trong DB vẫn NULL cho tới khi chủ dự án phê duyệt.

Ma trận chi tiết: [license_review_matrix.csv](license_review_matrix.csv) (1 dòng / source_id).

## 1. Giấy phép theo bằng chứng trong bản gốc

| Giấy phép | Phiên bản | Số tài liệu |
|---|---|---:|
| CC BY | 3.0 | 1 |
| CC BY | 4.0 | 35 |
| CC BY-NC | 3.0 | 1 |
| CC BY-NC | 4.0 | 9 |
| CC BY-NC-SA | 3.0 IGO | 3 |
| Public Domain | — | 24 |

| Trạng thái bằng chứng | Số |
|---|---:|
| evidence_in_original_document | 55 |
| agency_policy_only | 18 |

- `evidence_in_original_document`: câu giấy phép đọc được trong file gốc (JATS `<license>`, câu public domain trong HTML của NIH, trang giấy phép trong PDF).
- `agency_policy_only`: trang đã lưu không có câu giấy phép; chỉ có chính sách chung của cơ quan (CDC: "most of the information … is in the public domain"; NIDCD: "unless otherwise stated … public domain"). Chưa kiểm tra nội dung bên thứ ba từng trang.

## 2. 48 tài liệu mang nhãn `verified_noncommercial_research` (48)

- **CC BY** (35): `ASD-CSV-007`, `ASD-CSV-011`, `ASD-CSV-017`, `ASD-CSV-018`, `ASD-CSV-019`, `ASD-CSV-020`, `ASD-CSV-062`, `ASD-CSV-077`, `ASD-CSV-078`, `ASD-CSV-081`, `ASD-CSV-088`, `ASD-CSV-089`, `ASD-CSV-091`, `ASD-CSV-095`, `ASD-NEW-001`, `ASD-NEW-002`, `ASD-NEW-003`, `ASD-OA-PMC12468522`, `ASD-OA-PMC12593641`, `ASD-OA-PMC13005892`, `ASD-OA-PMC13393316`, `ASD-OA-PMC13427885`, `ASD-OA-PMC4271434`, `ASD-OA-PMC4742252`, `ASD-OA-PMC6487529`, `ASD-OA-PMC7407189`, `ASD-OA-PMC9003052`, `ASD-SUP-PMC10981608`, `ASD-SUP-PMC11754701`, `ASD-SUP-PMC12658592`, `ASD-SUP-PMC13414371`, `ASD-SUP-PMC4513196`, `ASD-SUP-PMC6590432`, `ASD-SUP-PMC7726187`, `ASD-SUP-PMC9399988`
- **CC BY-NC** (10): `ASD-CSV-002`, `ASD-CSV-029`, `ASD-CSV-038`, `ASD-CSV-084`, `ASD-OA-PMC10018050`, `ASD-OA-PMC10774556`, `ASD-OA-PMC10900867`, `ASD-OA-PMC11638897`, `ASD-OA-PMC12620806`, `ASD-SUP-PMC10783429`
- **CC BY-NC-SA** (3): `WHO-CST-INTRO-2022`, `WHO-CST-PARTICIPANTS-2022`, `WHO-ECD-GUIDELINE-2020`

Kết luận: nhãn catalog chặt hơn giấy phép ở các tài liệu CC BY — giấy phép CC BY cho phép cả sử dụng thương mại. Nhãn này có thể là chính sách dự án có chủ đích; audit **không tự đổi nhãn**, chỉ ghi `catalog_label_matches_license` trong CSV. Đề xuất: lưu `license_type` thật vào DB (migration 004) và để chủ dự án quyết định có giữ chính sách phi thương mại cho toàn kho hay không.

## 3. 25 tài liệu còn lại

- **CC BY** (1): `NIHR-SENITA-2022`
- **Public Domain** (24): `CDC-ASD-ABOUT`, `CDC-ASD-CLINICAL`, `CDC-ASD-SCREENING`, `CDC-ASD-SIGNS`, `CDC-ASD-TREATMENT`, `CDC-CONCERNED`, `CDC-EARLY-INTERVENTION`, `CDC-MILESTONES-02`, `CDC-MILESTONES-04`, `CDC-MILESTONES-06`, `CDC-MILESTONES-09`, `CDC-MILESTONES-12`, `CDC-MILESTONES-15`, `CDC-MILESTONES-18`, `CDC-MILESTONES-24`, `CDC-MILESTONES-30`, `CDC-MILESTONES-36`, `NIH-NIDCD-ASD-COMMUNICATION-2020`, `NIH-NIMH-ADHD`, `NIH-NIMH-ASD-2025`, `NIH-NIMH-CHILDREN`, `NIH-NIMH-MEDICATIONS`, `NIH-NIMH-TEEN-BRAIN`, `NIH-NIMH-TEEN-DEPRESSION`

## 4. Đánh giá theo từng hành động (chỉ theo giấy phép)

| Hành động | CC BY | CC BY-NC | CC BY-NC-SA | Public Domain |
|---|---|---|---|---|
| `archive_allowed` | yes_by_license (36) | nc_only_by_license (10) | nc_only_by_license (3) | conditional (18), yes_by_license (6) |
| `text_mining_allowed` | yes_by_license (36) | nc_only_by_license (10) | nc_only_by_license (3) | conditional (18), yes_by_license (6) |
| `chunking_allowed` | yes_by_license (36) | nc_only_by_license (10) | nc_only_by_license (3) | conditional (18), yes_by_license (6) |
| `embedding_allowed` | yes_by_license (36) | nc_only_by_license (10) | nc_only_by_license (3) | conditional (18), yes_by_license (6) |
| `cohere_processing_allowed` | pending_decision (36) | blocked (10) | blocked (3) | pending_decision (24) |
| `external_llm_processing_allowed` | pending_decision (36) | pending_decision (10) | pending_decision (3) | pending_decision (24) |
| `commercial_use_allowed` | yes_by_license (36) | no_by_license (10) | no_by_license (3) | conditional (18), yes_by_license (6) |
| `attribution_required` | yes_by_license (36) | yes_by_license (10) | yes_by_license (3) | conditional (24) |
| `share_alike_required` | no_by_license (36) | no_by_license (10) | yes_by_license (3) | no_by_license (24) |

Ghi chú: ShareAlike chỉ phát sinh nghĩa vụ khi **chia sẻ** bản chuyển thể; chunk/embedding nội bộ không chia sẻ ra ngoài. Public domain của cơ quan Mỹ không cấp quyền dùng logo/hình ảnh bên thứ ba và yêu cầu không ngụ ý xác nhận (endorsement).

## 5. Danh sách BLOCKED / chưa xác minh

- `cohere_processing_allowed = blocked` (13): `ASD-CSV-002`, `ASD-CSV-029`, `ASD-CSV-038`, `ASD-CSV-084`, `ASD-OA-PMC10018050`, `ASD-OA-PMC10774556`, `ASD-OA-PMC10900867`, `ASD-OA-PMC11638897`, `ASD-OA-PMC12620806`, `ASD-SUP-PMC10783429`, `WHO-CST-INTRO-2022`, `WHO-CST-PARTICIPANTS-2022`, `WHO-ECD-GUIDELINE-2020` — lý do: giấy phép NC + trial key chịu Terms of Use cho phép Cohere dùng dữ liệu cải thiện dịch vụ.
- Xung đột/không rõ bằng chứng (0): —
- `external_llm_processing_allowed`: `pending_decision` cho cả 73 — chưa chọn nhà cung cấp LLM nên chưa có điều khoản để đối chiếu.
- `verified_by` / `verified_at` để trống: chưa có người chịu trách nhiệm phê duyệt.

## Cohere — điều khoản áp dụng cho API key hiện tại (kiểm tra 14/11/2026)

Chỉ dùng nguồn chính thức của Cohere. Không gửi nội dung tài liệu nào trong lúc kiểm tra: chỉ gọi `GET /v1/models/embed-v4.0` và `POST /v1/check-api-key` (không có nội dung).

| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Loại key | **Trial (evaluation)** | Header phản hồi `x-trial-endpoint-call-limit: 100`, `x-trial-endpoint-call-remaining: 99`, `x-endpoint-monthly-call-limit: 1000`; `check-api-key` → `valid: true` |
| Giới hạn trial | 1.000 lời gọi/tháng; Embed 2.000 input/phút | [Rate limits](https://docs.cohere.com/docs/rate-limits): "Trial keys … limited to 1,000 API calls a month" |
| Trial dùng cho production | Phải nâng cấp để "serve Cohere in production"; trang không cấm rõ việc dùng thương mại | [Going live](https://docs.cohere.com/docs/going-live) |
| Điều khoản áp dụng cho trial | Terms of Use + Privacy Policy, **không** phải Enterprise Data Commitments | [Enterprise Data Commitments](https://cohere.com/data-usage-policy) (Last update 5/12/2025): "Our Terms of Use and Privacy Policy apply to data we receive from users using a trial API key" |
| Cam kết dữ liệu (khách trả phí) | Prompt/generation có thể dùng để huấn luyện **trừ khi opt-out** (Settings → Data Controls); log xoá sau 30 ngày; ZDR chỉ cho enterprise được duyệt | cùng trang trên |
| Quyền Cohere với dữ liệu gửi lên (Terms of Use) | Cấp cho Cohere quyền không độc quyền, vĩnh viễn để truy cập, lưu, dùng dữ liệu nhằm "improve and enhance the Cohere solution and our other offerings", kể cả chia sẻ API data với bên thứ ba cung cấp dịch vụ cho Cohere (§4.1); khách hàng phải có đủ quyền với dữ liệu tải lên (§13.5) và bồi hoàn cho Cohere (§21.4) | [Terms of Use](https://cohere.com/terms-of-use) — bản truy cập được ghi ngày 7/9/2022 |
| Đặc tả kỹ thuật | `embed-v4.0`, `output_dimension` ∈ {256, 512, 1024, 1536}, mặc định 1536; tối đa 96 văn bản/lời gọi; `input_type` gồm `search_document`, `search_query`; `truncate=NONE` báo lỗi khi vượt giới hạn | [Models](https://docs.cohere.com/docs/models), [Embed API v2](https://docs.cohere.com/reference/embed) |

### Đánh giá

1. **Với trial key, dữ liệu gửi lên chịu Terms of Use cho phép Cohere dùng để cải thiện dịch vụ thương mại của họ.** 13 tài liệu CC BY-NC / CC BY-NC-SA chỉ cho phép sử dụng phi thương mại; việc một bên thứ ba thương mại được quyền dùng lại nội dung là xung đột tiềm ẩn ⇒ `cohere_processing_allowed` cho 13 tài liệu này: **BLOCKED** khi còn dùng trial key.
2. Với 60 tài liệu CC BY / public domain, giấy phép không cản trở, nhưng việc chấp nhận điều khoản dữ liệu của Cohere là **quyết định vận hành của chủ dự án** ⇒ `pending_decision`.
3. Phương án gỡ chặn (cần chủ dự án chọn): (a) chuyển sang production key + bật opt-out huấn luyện trong Data Controls (log vẫn giữ 30 ngày); (b) xin Zero Data Retention (enterprise); (c) chỉ embed 60 tài liệu không-NC; (d) dùng mô hình embedding chạy local cho tài liệu NC (phải đổi profile, không trộn vector).

### Điểm chưa rõ (cần xác minh lại, không suy đoán)

- Bản Terms of Use hiện hành: bản truy cập được ghi ngày 7/9/2022; có thể đã có bản mới hơn hoặc SaaS Agreement riêng cho production. Cần đọc trực tiếp trong dashboard khi nâng cấp.
- Trial account có truy cập được toggle opt-out "Data Controls" hay không: trang chính thức không nói.
- Privacy Policy chưa được đọc trong lượt kiểm tra này.
- Câu hỏi pháp lý về việc gửi văn bản CC BY-NC tới nhà xử lý dữ liệu (data processor) có cấu thành "commercial use" hay không cần người có thẩm quyền pháp lý trả lời — audit này không phải tư vấn pháp lý.

## 6. Việc cần chủ dự án quyết định

1. Giữ hay bỏ chính sách "phi thương mại cho toàn kho" với 35 tài liệu CC BY.
2. Phương án Cohere (production key + opt-out / ZDR / chỉ embed tài liệu không-NC / embedding local).
3. Chấp nhận mức bằng chứng `agency_policy_only` (17 trang CDC + 1 trang NIDCD), hay yêu cầu kiểm tra từng trang.
4. Sau khi quyết định: ghi `*_allowed`, `verified_by`, `verified_at` bằng role owner (một lệnh SQL có kiểm toán cho mỗi nhóm), rồi chạy lại `scripts/db_check.py`.
