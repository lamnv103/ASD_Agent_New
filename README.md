# ASD-RAG Agent

Trợ lý hỏi đáp tiếng Việt về rối loạn phổ tự kỷ (ASD) cho trẻ 0–18 tuổi, trả lời dựa trên bằng chứng trong kho tài liệu được phép sử dụng.

> **Chỉ dùng cho prototype/nghiên cứu.** Chưa nguồn nào được thẩm định lâm sàng độc lập. Chưa nguồn nào được xác nhận quyền text mining / embedding / gửi sang Cohere hay LLM ngoài cho production. Vector hiện có là của **luồng nghiên cứu** (ủy quyền `research_test` theo yêu cầu chủ dự án), không phải phê duyệt quyền.

Quy ước triển khai: [.claude/skills/asd-agent-dev/SKILL.md](.claude/skills/asd-agent-dev/SKILL.md) · Hợp đồng dữ liệu: [data-contracts.md](.claude/skills/asd-agent-dev/references/data-contracts.md)

## Trạng thái (14/11/2026)

| Phase | Trạng thái | Ghi chú |
|---|---|---|
| 0 – Audit workspace | COMPLETED | Không có migration pack cũ; `cohere_existing` = `embed-v4.0` 1536 chiều |
| 1 – Database readiness | COMPLETED | `asd_rag_v2`, migration 001–007, 4 role (thêm `research_reader` chỉ đọc); 66/66 kiểm tra phân quyền đạt; trạng thái chunk chưa kiểm chứng bị cấm truy xuất ở mức bảng |
| 2 – Import data | COMPLETED | 174 nguồn (33/40/88/13), 174 hồ sơ quyền, 73 tài liệu khớp hash, 2 tài liệu cách ly |
| 3 – Chunking | COMPLETED (`section_v2_1`) | 9/9 tiêu chí, 71 tài liệu, 3.740 chunk trong DB; 100% số trang PDF; bảng PDF không khôi phục được bị loại khỏi truy xuất (khôi phục: PARTIAL) — [nghiệm thu](eval/reports/section_v2_acceptance_2026-11-14_phase5.md), [PDF](eval/reports/pdf_extraction_repair_2026-11-14_phase5.md) |
| Rights audit | COMPLETED (bằng chứng + phân loại 35 CC BY) · quyền BLOCKED | `data/curation/license_corrections.jsonl`; 35 `verified_cc_by`, 13 NC giữ nguyên — [audit](eval/reports/license_audit_2026-11-14.md), [phân loại](eval/reports/license_classification_repair_2026-11-14_phase5.md) |
| 4 – Embedding | COMPLETED (nghiên cứu) · production BLOCKED | 2.338 vector `embed-v4.0`/1536 cho 71 nguồn (nhóm A/B/C) trong `research_chunk_embeddings` (migration 006), 13/13 kiểm tra đạt; production 0 vector, 0 quyền — [báo cáo chạy](eval/reports/embedding_run_report.md), [preflight](eval/reports/embedding_preflight_report.md), [kiểm tra](eval/reports/embedding_quality_check.md), [cổng nghiên cứu](eval/reports/embedding_research_gate_proposal_2026-11-14.md) |
| 5 – Retrieval | PARTIAL — dense (T2.3.1–T2.3.3) + FTS baseline (T2.4): READY WITH CONDITIONS; T2.4-B chấm mù: gói sẵn sàng, 0/2.791 nhãn | T2.4-B: pool xác minh 66/2.791/1.218; gói mù A/B `eval/annotation/t2_4b/` (mã HMAC, thứ tự độc lập); công cụ `scripts/annotation_t2_4b.py` (import/agreement/finalize); hồ sơ q057/q016 chờ quyết định — [T2.4-B](eval/reports/fts_annotation_quality_report_2026-11-15.md) · T2.4: FTS `app/retrieval/fts.py` (A thô / B glossary AND / C glossary OR, `english` + `ts_rank_cd`, role reader); câu Việt thô = 0 kết quả; glossary `config/query_glossary_vi_en_v1.json`; pool mù Dense ∪ FTS 2.791 cặp / 1.218 chunk — PENDING ANNOTATION, metric so sánh chỉ exploratory — [T2.4](eval/reports/phase_6_2_t2_4_fts_baseline_report_2026-11-15.md) · T2.3.3: cohort đóng băng theo T2.3.1, tái lập 66/66; nhãn gốc recall@10 0,49 / MRR 0,58 (coverage@10 27%), nhãn merge recall@10 0,61 / MRR 0,78 (thiên lệch về dense, coverage@10 64%); lỗi chính q066/q033/q063 — [T2.3.3](eval/reports/phase_6_2_t2_3_3_dense_evaluation_report_2026-11-15.md) · T2.3.2: 312/1.103 ứng viên có quyết định (303 judged, 4 chờ phân xử, 5 loại), 791 chưa chấm; +95 nhãn relevant ở 49 câu → `retrieval_eval_v1_merged_2026-11-14.jsonl` (silver, tái lập từ gốc + `…_candidate_judgments_2026-11-14.jsonl`) — [coverage](eval/reports/phase_6_2_t2_3_2_annotation_coverage_2026-11-14.md) · Dense `embed-v4.0` qua role `research_reader` + view lọc C5: recall@10 0,49 / recall@20 0,65 / MRR 0,58 trên 55 câu (SILVER, cận dưới; source hit@5 0,98) — [T2.3.1](eval/reports/phase_6_2_t2_3_1_dense_retrieval_report_2026-11-14.md) ·  Audit 6.1: READY WITH CONDITIONS — [audit](eval/reports/retrieval_architecture_audit_2026-11-14.md) · 6.2 T0 quyết định C1–C5 — [T0](eval/reports/phase_6_2_t0_technical_decisions_2026-11-14.md) · T2 D-1 (loại 47 chunk danh mục tham khảo, authorization 2) + migration 007 (role chỉ đọc + view lọc C5) + kiểm chứng bảo mật 74/74 — [T2.2](eval/reports/phase_6_2_t2_2_security_verification_2026-11-14.md) · T1 bộ đánh giá `eval/datasets/retrieval_eval_v1.jsonl` (66 câu, 300 nhãn relevant, silver — chưa có người xác minh) — [T1](eval/reports/phase_6_2_t1_evaluation_dataset_report_2026-11-14.md) |
| 6 – Agent | NOT STARTED | |
| 7 – Evaluation | NOT STARTED | |

## Luồng xử lý

```
OFFLINE  data/raw → build_corpus.py → import_sources.py → chunking (section_v1)
         → [cổng quyền + duyệt nội dung] → Cohere embed-v4.0 → pgvector → kiểm tra → eval

ONLINE   câu hỏi → safety screening → phân loại → ┬ greeting
                                                  ├ info_lookup (SQL/FTS trên 174 nguồn)
                                                  └ expert_qa: dense + FTS → fusion → rerank
                                                     → evidence validation → LLM → answer validation
```

## Cấu trúc thư mục

```
.
├─ .claude/skills/asd-agent-dev/   quy ước triển khai + hợp đồng dữ liệu
├─ app/
│  ├─ config.py, db.py, migrations.py   cấu hình từ .env, kết nối theo role, logic migration
│  ├─ ingest/        pipeline offline: catalog_import, markdown_blocks, pdf_layout, chunking, chunk_store,
│  │                 embed_pipeline
│  ├─ rights/        license_audit (bằng chứng giấy phép, không cấp quyền)
│  ├─ retrieval/     embeddings (client Cohere duy nhất)
│  ├─ router/ greeting/ info_lookup/ expert_qa/ safety/ answer/ llm/   (chưa triển khai)
├─ config/           chunking_profiles.json (section_v1, section_v2), embedding_profiles.json
├─ docs/provider_terms/   bằng chứng điều khoản nhà cung cấp (có ngày kiểm tra)
├─ data/
│  ├─ curation/             hiệu chỉnh có phiên bản đặt lên catalog raw (license_corrections.jsonl)
│  ├─ extractions/<id>/     bản đồ trang, bảng PDF, đề xuất trích xuất lại (có phiên bản, không ghi đè)
│  ├─ raw/source_library/   kho nguồn gốc — CHỈ ĐỌC
│  ├─ corpus/{core,gaps}/ + manifest.jsonl   73 tài liệu (sinh bởi build_corpus.py)
│  ├─ catalog/sources.jsonl                  174 nguồn (sinh bởi build_corpus.py)
│  └─ index/tokenizers/     tokenizer embed-v4.0 (không commit)
├─ deploy/compose.yml, deploy/db/initdb/   PostgreSQL 16.15 + pgvector 0.8.6, tạo role/DB/schema
├─ migrations/       001–006 (+ rollback/004–006_down.sql)
├─ scripts/          build_corpus, db_migrate, db_check, import_sources, chunk_pilot, chunking_regression,
│                    license_audit, embed_chunks, embedding_preflight, embed_research
├─ tests/unit/       56 test
├─ backups/          pg_dump trước mỗi migration (không commit)
├─ eval/reports/     báo cáo (chunking pilot…)
├─ logs/             (không commit)
├─ pyproject.toml    phụ thuộc; môi trường ảo .venv/
└─ CLAUDE.md
```

## Chạy

```powershell
# 1. Môi trường
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"

# 2. Database (biến trong .env: ASD_RAG_DB_*, POSTGRES_SUPERUSER_PASSWORD, ASD_RAG_*_PASSWORD)
docker compose -p asd-rag-v2 --env-file .env -f deploy/compose.yml up -d --wait
.venv\Scripts\python -B scripts\db_migrate.py
.venv\Scripts\python -B scripts\db_check.py

# 3. Dữ liệu
python -B scripts\build_corpus.py --check
.venv\Scripts\python -B scripts\import_sources.py
.venv\Scripts\python -B scripts\chunk_pilot.py --profile section_v2
.venv\Scripts\python -B scripts\chunking_regression.py          # so sánh v1 ↔ v2, không ghi DB
.venv\Scripts\python -B scripts\license_audit.py                # ma trận giấy phép, không ghi DB
.venv\Scripts\python -B scripts\embed_chunks.py --what-if       # production dry-run: không gọi API
.venv\Scripts\python -B scripts\embedding_preflight.py         # manifest nhóm A/B/C, không gọi API
.venv\Scripts\python -B scripts\embed_research.py run          # luồng nghiên cứu: dry-run (--execute để gọi Cohere)
.venv\Scripts\python -B scripts\embed_research.py verify       # kiểm tra vector trong DB
.venv\Scripts\python -B scripts\validate_retrieval_eval.py     # kiểm tra bộ đánh giá retrieval (chỉ đọc file)
.venv\Scripts\python -B scripts\candidate_judgments.py merge --check   # T2.3.2: tái lập dataset merge từ gốc + nhãn bổ sung
.venv\Scripts\python -B scripts\candidate_judgments.py validate        # T2.3.2: 14 kiểm tra nhãn bổ sung + validator v1
.venv\Scripts\python -B scripts\dense_eval_t2_3_3.py --check   # T2.3.3: đánh giá A/B trên cohort cố định, OFFLINE, chỉ đọc (role reader)
.venv\Scripts\python -B scripts\fts_eval_t2_4.py --check       # T2.4: FTS A/B/C + pool mù, OFFLINE (không API), chỉ đọc (role reader)
.venv\Scripts\python -B scripts\dense_retrieval_eval.py        # baseline dense, OFFLINE từ cache (--allow-api cần phê duyệt)

# 4. Kiểm tra code
.venv\Scripts\ruff check .
.venv\Scripts\python -m pytest
```

Mọi lệnh nạp dữ liệu đều chạy lại được (idempotent) và ghi vào `ingestion_runs`.

## Database `asd_rag_v2`

- Container `asd-rag-v2-db`, volume `asd_rag_v2_pgdata`, chỉ bind `127.0.0.1:5433`.
- Role: `asd_rag_v2_owner` (migration, duyệt, cấp quyền xử lý), `asd_rag_v2_ingest` (nạp dữ liệu, không duyệt được), `asd_rag_v2_app` (chỉ đọc qua view cổng, ghi log).
- Cổng: `v_embedding_eligible_documents` (đã duyệt + quyền archive/text mining/chunking/embedding/Cohere = true) → `v_retrieval_ready_chunks` (thêm duyệt truy xuất + quyền LLM ngoài).
- Quyền: `source_rights.*_allowed` là **quyết định** của owner; `rights_assessments` là **bằng chứng** (giấy phép / điều khoản nhà cung cấp), không bao giờ tự cấp quyền.
- `v_chunk_provenance`: chunk kèm metadata kế thừa từ document/source (chỉ ingest/owner đọc được).
- Truy xuất nghiên cứu (007): role `asd_rag_v2_research_reader` (LOGIN, NOINHERIT) chỉ có SELECT trên `v_research_retrieval_chunks` — view `security_barrier` áp đủ C5 (authorization hiện hành, allowlist, profile/model/chiều, tài liệu hiện hành, không cách ly, trạng thái đã kiểm chứng, provenance) trước mọi LIMIT. Chi tiết: [docs/research_retrieval_access.md](docs/research_retrieval_access.md).
- Luồng nghiên cứu (006): `research_embedding_authorizations` (+ nguồn, allowlist chunk) → `v_research_embedding_candidates` → `research_chunk_embeddings` (trigger chặn ngoài allowlist; app không đọc được).
- Chưa có index HNSW: dùng exact search làm baseline, chỉ thêm ANN khi đo được cần thiết.

## Dữ liệu

| Tier | Số nguồn | Dùng ở nhánh |
|---|---|---|
| `core` | 33 | chuyên môn + truy xuất thông tin |
| `gaps` | 40 | chuyên môn + truy xuất thông tin (thiếu hình/media/phụ lục, ghi rõ trong chunk) |
| `metadata_only` | 88 | chỉ truy xuất thông tin |
| `excluded` | 13 | không dùng trả lời chuyên môn |

Cách ly: `ASD-CSV-077`, `NIH-NIMH-CHILDREN` (lỗi độ trung thực khi chuyển đổi). Nhãn `verified_noncommercial_research` có ở 48 tài liệu nhưng chỉ 13 có giấy phép NC thật.

Không sửa trực tiếp `data/corpus` hay `data/catalog`; sửa nguồn trong `data/raw` hoặc logic trong `scripts/build_corpus.py` rồi chạy lại.
