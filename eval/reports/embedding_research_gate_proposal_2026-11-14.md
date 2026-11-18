# Research embedding gate (migration 006): scope and impact — 2026-11-14

## 1. The gate that blocks embedding
The production gate is `v_embedding_eligible_documents`. It admits a document only when all of these hold:
- `content_review_status = 'approved'`;
- `content_warning IS NULL`;
- `approved_for_embedding`;
- `archive_allowed`, `text_mining_allowed`, `chunking_allowed`, `embedding_allowed` and `cohere_processing_allowed` are all TRUE.

Current state:
- All 174 sources have every `*_allowed` set to NULL.
- All 73 documents have `approved_for_embedding = false`.
- 71 documents have `content_review_status = pending`; 2 are quarantined.

Result: **0 documents pass**. The breakdown is in section 6 of [embedding_preflight_report.md](embedding_preflight_report.md).

What we deliberately do not do:
- Write `*_allowed = true`.
- Approve content.
- Modify the production views.
- Use the `--confirm-rights-approved` flag on `embed_chunks.py`.

## 2. Mechanism: a separate research track
The project owner requested a research/test embedding of groups A/B/C. Migration 006 records that request as a **research authorization** that is separate from production approval.

| Object | Role |
|---|---|
| `research_embedding_authorizations` | Who requested it, the basis, the profile and the manifest SHA-256. Constraints: `scope = 'research_test'` and `production_approval = false`. Can be revoked via `revoked_at`. |
| `research_embedding_authorization_sources` | The authorized sources and their groups (A/B/C). |
| `research_embedding_authorization_chunks` | The exact allowlist from preflight (`chunk_id` + `content_sha256`). |
| `v_research_embedding_candidates` | Allowlist ∩ (current document, not quarantined, `core`/`gaps`, `retrieval_eligible`, verified structure status). |
| `research_chunk_embeddings` | Research vectors with chunk_id, model, dimension, input type, run ID, content hash, input hash and timestamp. Constraint `UNIQUE (chunk_id, profile_id)`. |
| Trigger `research_chunk_embeddings_guard` | Accepts a vector only for a current candidate with the same content hash, the profile's model and dimension, and `search_document`. |

## 3. Impact
| Area | Changes? |
|---|---|
| `source_rights`, `documents` (approvals), `chunks`, `chunk_embeddings` (production), the 2 production gate views | **No** |
| Existing grants of the 3 roles | **No** (no GRANT/REVOKE on existing objects) |
| Grants on **new** objects | ingest: SELECT on the 3 authorization tables + candidate view; SELECT/INSERT on `research_chunk_embeddings` (no UPDATE/DELETE). owner: object owner. **app: none.** |
| Production retrieval | Not enabled: the app role cannot read the research vectors, and `v_retrieval_ready_chunks` is unchanged (still 0). |
| Re-chunking `section_v2_1` for embedded documents | **Blocked** by `ON DELETE RESTRICT`, so vectors can never point at changed content. A content change requires a new chunk profile, or a deliberate dump + delete of the research vectors. |
| `clinical_reviewed` | Unchanged (false). |
| Rollback | `migrations/rollback/006_down.sql` drops only the research objects (it deletes research vectors). |

## 4. Tests on an isolated container
Setup:
- `docker run --tmpfs` on port 5439, restored from `backups/asd_rag_v2_pre006_20261114_192229.dump` (SHA-256 `3fb1bac7…5d82`).
- `CREATE DATABASE … TEMPLATE` was not used.

Sequence and results:
1. Apply 006 → passed.
2. 21 behaviour probes → **21/21 passed**:
   - These were stored: an allowlisted vector.
   - These were blocked:
     - A duplicate vector.
     - A `text_encoding_lost` chunk.
     - A chunk not on the allowlist.
     - A wrong content hash.
     - A wrong model.
     - A 1024-dimension vector.
     - A NaN value.
     - ingest UPDATE/DELETE on research vectors.
     - ingest writing an authorization.
     - ingest setting `embedding_allowed`.
     - Deleting a chunk that has a vector.
     - The app role reading the 3 research objects.
     - A scope other than `research_test`.
   - These stayed unchanged: the production gate (still 0) and `chunk_embeddings` (still 0).
3. Rollback → 0 research objects remain.
4. Re-apply → passed.
5. `db_check` → ok, with **34/34** permission probes (25 existing + 9 new).

## 5. Limits
- This is a research authorization, **not** a legal/licence decision.
- 13 NC documents (group B) and 18 documents whose evidence is only agency-level policy (group C) are included at the project owner's request, for non-commercial student research.
- The Cohere key is a trial key: [docs/provider_terms/cohere_2026-11-14.md](../../docs/provider_terms/cohere_2026-11-14.md).
- Before any production use, the owner must record real rights decisions and content approval through the production gate. Research vectors can be promoted only when the input hash is identical.
