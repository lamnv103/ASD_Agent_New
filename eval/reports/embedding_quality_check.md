# Embedding quality check — 2026-11-14

**Trạng thái: COMPLETED** — kiểm tra trên vector thật trong `asd_rag.research_chunk_embeddings` (sinh bởi `scripts/embed_research.py verify`, 2026-11-14T12:38:36+00:00).

| Kiểm tra | Kết quả |
|---|---|
| stored vectors = eligible chunks | 2,338 / 2,338 ✔ |
| every eligible chunk has a vector | ✔ |
| no vector outside the manifest | ✔ |
| no vector for an excluded chunk | ✔ |
| all dimensions = 1536 (column, record, actual) | ✔ |
| model = embed-v4.0, input_type = search_document | ✔ |
| no NaN/Inf coordinate | ✔ |
| vector norms finite and > 0 | ✔ |
| content hash matches current chunk | ✔ |
| one vector per chunk_id | ✔ |
| every vector is an authorized current candidate | ✔ |
| provenance: source_id, document_id, URL, page or char range | ✔ |
| production untouched (0 vectors / gates / approvals / rights flags) | ✔ |

Chuẩn L2 của vector: min 1.0000, max 1.0000.

Production (phải bằng 0): `chunk_embeddings` = 0, `v_embedding_eligible_documents` = 0, `v_retrieval_ready_chunks` = 0, `approved_for_embedding` = 0, `rights_flags_set` = 0.

## Kiểm tra truy vấn (search_query, exact cosine, chỉ để kiểm tra kỹ thuật)
5 câu hỏi thử, 1 lời gọi API, 78 token tính phí. Không phải đánh giá chất lượng truy xuất (Phase 5/7, cần bộ câu hỏi chuẩn có chuyên gia duyệt).

**Dấu hiệu sớm của rối loạn phổ tự kỷ ở trẻ 18 tháng tuổi là gì?**
- 0.462 · `CDC-MILESTONES-18` · Image: mom holding baby on lap and reading a book As your child's first teacher, you can help his or her devel…
- 0.459 · `CDC-ASD-SIGNS` · Social communication and interaction skills can be challenging for people with ASD. Examples of social communi…
- 0.459 · `CDC-MILESTONES-18` · * Copies you doing chores, like sweeping with a broom * Plays with toys in a simple way, like pushing a toy ca…

**What early intervention approaches improve communication in autistic preschool children?**
- 0.534 · `ASD-SUP-PMC13414371` · Overall, the most consistent evidence currently suggests improvements in expressive language and spontaneous c…
- 0.530 · `ASD-SUP-PMC10783429` · Autism is a relatively common diagnosis, with current estimates suggesting approximately 1-4% of the populatio…
- 0.528 · `ASD-OA-PMC10774556` · Developmental approaches prioritize child-led spontaneous play and joint attention with adults to enhance the …

**Cha mẹ có thể làm gì khi trẻ tự kỷ có hành vi thách thức ở nhà?**
- 0.506 · `WHO-CST-PARTICIPANTS-2022` · Only check the answers after you have tried to answer the questions. When you finish checking the answers, go …
- 0.487 · `WHO-CST-PARTICIPANTS-2022` · behaviour. Tips Try to answer these questions after the session to check your own learning. When you finish, y…
- 0.463 · `WHO-CST-PARTICIPANTS-2022` · Challenging behaviour to get access to a sensation Behaviour can help a child get sensation (a feeling) A chil…

**Sensory integration therapy effectiveness for autistic children**
- 0.662 · `NIHR-SENITA-2022` · Sensory integration therapy Sensory integration therapy is a clinic-based approach that focuses on the therapi…
- 0.628 · `NIHR-SENITA-2022` · The three remaining studies assessing the efficacy of SIT reported positive effects on behavioural outcomes li…
- 0.617 · `NIHR-SENITA-2022` · For a variety of pragmatic reasons, including therapist availability and workload, some participants allocated…

**Tỷ lệ trẻ tự kỷ có kèm rối loạn tăng động giảm chú ý (ADHD)**
- 0.502 · `ASD-CSV-078` · Comorbidity can refer to both the co-occurrence of disorders temporally separated from ADHD or concurrent with…
- 0.483 · `ASD-CSV-078` · This study is unique in that it aligns with our hypothesis that children with ADHD face higher levels of anxie…
- 0.477 · `ASD-CSV-078` · Discussion We conducted a literature review on the differing levels of anxiety and psychiatric comorbidities i…

