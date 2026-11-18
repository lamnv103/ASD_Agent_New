# T2.4 — FTS Architecture Audit — 2026-11-15

Audit **trước khi triển khai**, chỉ đọc: chạy bằng role `asd_rag_v2_research_reader`, session `read_only`, qua `asd_rag.v_research_retrieval_chunks` và catalog/hàm `pg_catalog` (`ts_debug`, `pg_ts_config`, `pg_extension`). Không đổi cấu hình FTS, schema hay quyền.

Script tạm: `fts_audit.py` (scratchpad). Mọi số liệu dưới đây là output thật.

## 1. Hiện trạng
| Hạng mục | Thực tế | Nguồn |
|---|---|---|
| PostgreSQL | 16.15 | `version()` |
| `default_text_search_config` | `pg_catalog.english` | `SHOW` |
| Config có sẵn | 29 config ngôn ngữ phương Tây/Ấn + `simple`; **không có config tiếng Việt** | `pg_ts_config` |
| Extension đã cài | `plpgsql`, `vector 0.8.6` | `pg_extension` |
| `unaccent`, `pg_trgm` | **Có sẵn nhưng chưa cài**. Cài cần `CREATE EXTENSION`, tức là migration, nằm ngoài phạm vi T2.4 | `pg_available_extensions` |
| Cột FTS | `chunks.content_tsv` (generated, STORED) = `setweight(to_tsvector('english', section_heading), 'B') ∥ setweight(to_tsvector('english', content), 'A')` | migration 001, dòng 109–112 |
| Index | `chunks_content_tsv_idx` GIN trên `content_tsv`; `sources_title_fts_idx` GIN | migration 002 |
| Truy cập qua view | View 007 trả `content_tsv`; reader đọc được 2.291 hàng, 2.291 `content_tsv` khác null | `SELECT count(*)` |
| Kế hoạch truy vấn | View có `security_barrier`, nên điều kiện `content_tsv @@ q` chạy **sau** các join và bộ lọc C5 (Subquery Scan / Filter). **GIN index không được dùng.** Với 2.291 hàng: khoảng 100–140 ms mỗi truy vấn | `EXPLAIN` |
| Trọng số | Heading = B (0,4), nội dung = A (1,0) theo trọng số mặc định của `ts_rank_cd` {D,C,B,A} = {0,1; 0,2; 0,4; 1,0}. Heading nhẹ hơn nội dung, ngược với cách thường làm | migration 001 |
| Hàm xếp hạng khả dụng | `ts_rank`, `ts_rank_cd` (cover density). **Không có BM25** trong PostgreSQL lõi; không được gọi `ts_rank_cd` là BM25 | — |

## 2. Tiếng Việt với config `english`
Đầu vào `ts_debug('english', 'Trẻ tự kỷ có hay bị động kinh không?')`:
- Mọi âm tiết thành token `word`/`asciiword`, giữ nguyên dấu (`trẻ`, `tự`, `kỷ`, `động`…).
- Snowball tiếng Anh không stem được tiếng Việt. Từ dừng tiếng Anh không trùng âm tiết tiếng Việt, nên mọi âm tiết đều bị AND.

| Truy vấn (`plainto_tsquery`, AND mọi từ) | Số chunk khớp |
|---|---|
| "Trẻ tự kỷ có hay bị động kinh không?" | **0** |
| "Can thiệp do cha mẹ thực hiện có hiệu quả không?" | **0** |
| "Con tôi hay nhại lại lời người khác, đó là gì?" | **0** |
| "Nên ưu tiên can thiệp tại nhà do cha mẹ hay tại trường?" | **0** |
| "Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?" | **0** (`dsm` & `-5` khớp, nhưng các âm tiết Việt thì không) |
| "Giao tiếp thay thế (AAC) có làm trẻ chậm nói hơn không?" | **0** |

- Âm tiết Việt hiếm khi có trong corpus: `tự` 2, `kỷ` 2, `nguyễn` 4, `việt` 1; `trẻ`, `cha`, `mẹ` đều 0.
- **Bỏ dấu:** "Tre tu ky co hay bi dong kinh khong" thành `tre`, `tu`, `ky`, `dong`, `kinh` (asciiword), cũng không khớp.
- DB không có `unaccent`, nên mọi xử lý dấu phải làm ở tầng ứng dụng (Python), trên **câu hỏi**. Corpus là tiếng Anh nên không cần bỏ dấu phía corpus.

**Kết luận:** FTS trên câu hỏi tiếng Việt thô **không dùng được** với corpus tiếng Anh. Mọi khả năng tìm kiếm phải đến từ thuật ngữ tiếng Anh: từ viết tắt có sẵn trong câu, hoặc glossary.

## 3. Từ viết tắt, ký hiệu và chính tả Anh–Mỹ
| Đầu vào | Lexeme (`english`) | Hệ quả |
|---|---|---|
| `AAC`, `ADHD`, `ASD` | `aac`, `adhd`, `asd` | Ổn: 94 / 186 / 692 chunk |
| `DSM-5` | `dsm` + `-5` (token `int`, số âm) | `phraseto_tsquery('DSM-5')` khớp 48 chunk, giống `plainto`. Ổn nếu dùng nguyên cụm |
| `ADOS-2` | **`ado`** + `-2` | Snowball stem `ADOS` thành `ado`. Vẫn khớp vì corpus bị stem giống hệt, nhưng có thể trùng từ "ado" |
| `M-CHAT-R/F` | `m-chat-r`, `m`, `chat`, `r`, `/f` (token `file`) | Phải dùng `M-CHAT` (25 chunk). Nguyên chuỗi `M-CHAT-R/F` dễ thành truy vấn quá hẹp |
| `WHO` | **từ dừng** (`who`) nên tsquery rỗng | "WHO" không bao giờ khớp. Phải dùng "World Health Organization" (8 chunk) |
| `behaviour` / `behavior` | `behaviour` / `behavior` (2 lexeme) | 196 / 680 chunk. **Phải liệt kê cả hai** |
| `behaviours` / `behaviors` | `behaviour` / `behavior` | Snowball xử lý số nhiều |
| `paediatric` / `pediatric` | `paediatr` / `pediatr` | 18 / 80 chunk |
| `colour` / `color`, `centre` / `center` | khác nhau | Cùng vấn đề |
| `parent-mediated` | `parent-medi` + `parent` + `mediat` | Phrase khớp được vì vị trí trong tsvector giống nhau |
| `epilepsy` / `epileptic` / `seizures` | `epilepsi` / `epilept` / `seizur` | Không cùng lexeme, phải liệt kê từng dạng |

## 4. AND / OR và phrase
| Truy vấn tiếng Anh | Kiểu | Số chunk |
|---|---|---|
| restricted interests | phrase / AND | **7** / 31 |
| restricted, repetitive | phrase / AND | 26 / 56 |
| parent mediated | phrase / AND | 38 / 50 |
| parent implemented | phrase / AND | 7 / 93 |
| joint attention | phrase / AND | 47 / 50 |
| challenging behaviour / behavior | phrase | 32 / 71 |
| "Do autistic children often have epilepsy?" | plainto (AND) | 5 |
| "Should parent-mediated home intervention or school-based intervention be prioritised?" | plainto (AND) | **0** |
| "My child often repeats what other people say, what is it?" | plainto (AND) | 1 |

- **AND trên cả câu làm mất kết quả** khi câu có nhiều từ không cùng xuất hiện trong một chunk.
- Phrase chính xác hơn AND rời rạc nhưng hẹp hơn: "restricted interests" chỉ có 7 chunk, trong khi "restricted, repetitive" có 26.

## 5. Đề xuất thiết kế (đã triển khai ở T2.4, không đổi schema)
1. **Không đổi `content_tsv`, index hay extension.**
   - Đổi trọng số heading, thêm `unaccent`, thêm config `simple` hay dùng GIN qua view khác đều cần migration. Mỗi thay đổi phải là đề xuất riêng, kèm backup và rollback.
   - Hiệu năng hiện tại đủ cho đánh giá (khoảng 0,1 s/truy vấn).
2. **Truy vấn ở tầng ứng dụng:**
   - Câu tiếng Việt giữ nguyên, chạy qua `plainto_tsquery`.
   - Thêm thuật ngữ tiếng Anh từ glossary có phiên bản (quyết định T0 C4), mỗi thuật ngữ qua `phraseto_tsquery` hoặc `plainto_tsquery`.
   - **Không bao giờ** đưa text người dùng vào `to_tsquery`.
3. **Ba cấu hình kiểm định độc lập**, cùng config `english` và ranker `ts_rank_cd`:
   - **A:** câu thô, AND;
   - **B:** glossary, AND giữa các khái niệm;
   - **C:** glossary, OR giữa các khái niệm.
4. **Glossary** ghi cả hai cách viết Anh–Mỹ, dùng cụm thay cho từ đơn khi cụm phổ biến hơn, và tránh `WHO` đứng một mình. Chi tiết trong `fts_retrieval_design_2026-11-15.md`.
5. **Không gọi điểm xếp hạng là BM25** và không diễn giải điểm thành xác suất.
