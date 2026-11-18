# Embedding preflight — 2026-11-14

**Trạng thái: COMPLETED** (chỉ đọc DB, không gọi Cohere). Sinh lúc 2026-11-14T12:28:02+00:00 bởi `scripts/embedding_preflight.py`.

## 1. Môi trường
| Kiểm tra | Kết quả |
|---|---|
| `COHERE_API_KEY` trong môi trường | có (không in giá trị) |
| Model / dimension / input type | `embed-v4.0` / 1536 / `search_document` (tài liệu), `search_query` (câu hỏi) |
| PostgreSQL / pgvector | 16.15 (Debian 16.15-1.pgdg12+2) / 0.8.6 |
| Cột `chunk_embeddings.embedding` | `vector(1536)` → khớp |
| Vector đang có trong DB | 0 |
| Chunking profile | `section_v2_1` |

## 2. Ba nhóm và hợp nhất theo `source_id`
| Nhóm | Định nghĩa | Nguồn | Không cách ly | Nguồn có chunk đủ điều kiện | Chunk đủ điều kiện | Token |
|---|---|---:|---:|---:|---:|---:|
| A | toàn văn `core`+`gaps` | 73 | 71 | 71 | 2,338 | 825,945 |
| B | `rights_status = verified_noncommercial_research` (giấy phép NC) | 13 | 13 | 13 | 509 | 180,519 |
| C | bằng chứng giấy phép chỉ ở cấp chính sách cơ quan (`agency_policy_only`) | 18 | 18 | 18 | 170 | 28,854 |

- B ⊂ A: **True**, C ⊂ A: **True** → hợp nhất = **73 nguồn** (71 không cách ly); không cộng số đếm giữa các nhóm.
- Nhóm C theo tổ chức: Centers for Disease Control and Prevention (CDC) 15, Centers for Disease Control and Prevention (CDC), National Center on Birth Defects and Developmental Disabilities 2, National Institute on Deafness and Other Communication Disorders (NIDCD), NIH 1.
- Cách ly (loại cả tài liệu): ASD-CSV-077, NIH-NIMH-CHILDREN. Không có chunk `section_v2_1`.
- Không đưa vào: 88 nguồn `metadata_only`, 13 nguồn `excluded` (không có toàn văn).

## 3. Tập sẽ embedding (hợp nhất, mỗi chunk một lần)
| Chỉ số | Giá trị |
|---|---:|
| Nguồn / tài liệu | 71 / 71 |
| Chunk `section_v2_1` của các tài liệu này | 3,740 |
| Chunk đủ điều kiện (`embedding_manifest.csv`) | **2,338** |
| Token ước tính (tokenizer embed-v4.0 trên văn bản gửi đi: tiêu đề + heading + nội dung) | 825,945 |
| Token lớn nhất một input | 733 |
| Lô (≤ 96) / lời gọi API dự kiến | 25 |
| Payload lớn nhất một lô | 210 KiB |

Theo giấy phép:

| Giấy phép | Nguồn | Chunk | Token |
|---|---:|---:|---:|
| ? | 37 | 911 | 288,122 |
| CC BY | 34 | 1,427 | 537,823 |

## 4. Loại trừ (`embedding_excluded.csv`)
| Lý do | Số dòng |
|---|---:|
| `non_content_section` | 1,061 |
| `table_structure_unrecoverable` | 193 |
| `metadata_only_source (no full text)` | 88 |
| `duplicate_content_of` | 46 |
| `text_encoding_lost` | 40 |
| `undetermined_content_section` | 32 |
| `fragment_too_short` | 19 |
| `excluded_source (no full text)` | 13 |
| `table_recovered_pending_review` | 11 |
| `quarantined_document (no section_v2_1 chunks)` | 2 |

Quy tắc (theo thứ tự, mỗi chunk một lý do — `app/ingest/embedding_manifest.py`, có unit test):
1. Trạng thái cấu trúc chưa kiểm chứng: `table_structure_unrecoverable` (bảng PDF mất cấu trúc), `table_recovered_pending_review`, `text_encoding_lost` (chuỗi `/gid…`).
2. Mục không phải nội dung (`retrieval_eligible = false`): tham khảo, người đóng góp, front/back matter, nhiễu.
3. Chunk rỗng; còn mã glyph; thiếu provenance (PDF: trang; HTML/XML: khoảng ký tự).
4. **Nội dung chưa xác định**: `section_type = unclassified` — lẫn danh mục tham khảo, danh sách hình, boilerplate nhà xuất bản (đã đọc 32/32); loại cả nhóm, chờ duyệt thủ công.
5. **Mảnh vụn** < 6 từ (mảnh bảng GRADE "HAZ 9 RCTs No serious", mảnh lưu đồ, dòng mục lục).
6. **Trùng nguyên văn**: giữ chunk có `chunk_id` nhỏ nhất, các bản khác `duplicate_content_of:<chunk_id>` (mẫu CDC milestones lặp ở nhiều trang tuổi, thông báo NIH, câu lặp trong sổ tay WHO).
7. Cấp tài liệu/nguồn: cách ly; không thuộc nhóm; `source_url` sai định dạng.

Chunk tốt và xấu trong cùng tài liệu: chỉ loại chunk xấu. `clinical_reviewed` không đổi (false).

## 5. Kiểm tra preflight
| Kiểm tra | Số vi phạm |
|---|---:|
| duplicate content hash among eligible | 0 ✔ |
| duplicate embedding input among eligible | 0 ✔ |
| empty eligible chunks | 0 ✔ |
| eligible chunks with malformed source_url | 0 ✔ |
| eligible chunks without source_id | 0 ✔ |
| eligible chunks from quarantined documents | 0 ✔ |
| eligible chunks without provenance (page or char range) | 0 ✔ |
| eligible chunks with unverified structure status | 0 ✔ |
| eligible chunks containing /gid glyph codes | 0 ✔ |
| document traceability problems | 0 ✔ |

Truy vết: mọi tài liệu có chunk là bản hiện hành; file corpus tồn tại và SHA-256 khớp `documents.file_sha256`; mỗi chunk có `source_id`, `document_id`, URL, trang (PDF) hoặc khoảng ký tự.

## 6. Cổng quyền đang chặn
`v_embedding_eligible_documents` (production) cho qua **0** tài liệu. Lý do chặn (số tài liệu):

| Điều kiện | Tài liệu |
|---|---:|
| `approved_for_embedding=false` | 73 |
| `archive_allowed=NULL` | 73 |
| `text_mining_allowed=NULL` | 73 |
| `chunking_allowed=NULL` | 73 |
| `embedding_allowed=NULL` | 73 |
| `cohere_processing_allowed=NULL` | 73 |
| `content_review_status=pending` | 71 |
| `content_review_status=quarantined` | 2 |
| `warning=text_fidelity_needs_conversion_review` | 2 |

Không ghi `*_allowed = true`, không duyệt nội dung, không sửa view production. Cơ chế nghiên cứu tách riêng (migration 006) được mô tả trong [embedding_research_gate_proposal_2026-11-14.md](embedding_research_gate_proposal_2026-11-14.md).

## 7. File
| File | SHA-256 |
|---|---|
| [embedding_manifest.csv](embedding_manifest.csv) | `542cce21378b302312f6f509ba69db0fc346b98d2c47bc0e639775a6d12b4fd3` |
| [embedding_excluded.csv](embedding_excluded.csv) | `eac6f5d9c0427aa33f70f094291e90ebaca99da43dd8ec385fe3a150e701ae05` |
