# Embedding run report — 2026-11-14 (research/test track, groups A/B/C)

**Status: COMPLETED** (research/test track). 2,338/2,338 vectors are stored in `asd_rag.research_chunk_embeddings` and pass all 13 checks against the database ([embedding_quality_check.md](embedding_quality_check.md)).

Production is unchanged and stays **BLOCKED**:
- 0 `chunk_embeddings`.
- Production gate 0 / retrieval 0.
- 0 approvals; all `*_allowed` = NULL.
- `clinical_reviewed` = false.

Sequence followed: AUDIT → PREFLIGHT → BACKUP → (research gate: migration 006) → EMBEDDING → DATABASE VERIFICATION → REPORT.

## 1. Configuration
| Item | Value |
|---|---|
| Provider / model | Cohere `embed-v4.0`, Embed API v2 (`https://api.cohere.com/v2/embed`) |
| Dimension / type | 1536 / `float`; `truncate = NONE` (never truncated or padded) |
| Input type | `search_document` (chunks); `search_query` (test questions only) |
| Input text | `{title}\n{section_heading}\n\n{content}` from `section_v2_1` chunks |
| Batch | ≤ 96 inputs; pace ≤ 1,800 inputs/min and ≤ 90k tokens per rolling 60 s window (added after run 1, see §5) |
| Key | `COHERE_API_KEY` read from the environment (trial key); never written to code, logs or reports |
| Embedding profile | `cohere_embed_v4_1536_v1` (registered in `embedding_profiles` by the owner role) |

## 2. Data: three groups merged by `source_id`
| Group | Definition | Sources | Eligible chunks | Vectors stored |
|---|---|---:|---:|---:|
| A | Full text, `core` + `gaps` (excluding the 2 quarantined documents) | 71 | 2,338 | 2,338 |
| B | Non-commercial licence (10 CC BY-NC + 3 CC BY-NC-SA) | 13 | 509 | 509 |
| C | Licence evidence at agency-policy level only (CDC 17, NIDCD 1) | 18 | 170 | 170 |
| **Union** (B ⊂ A, C ⊂ A; group counts not added together) | | **71 sources / 71 documents** | **2,338** | **2,338** |

Not included:
- 88 `metadata_only` sources and 13 `excluded` sources.
- 2 quarantined documents: `ASD-CSV-077` and `NIH-NIMH-CHILDREN`. Neither has a `section_v2_1` chunk; the quarantine was not lifted.

## 3. Exclusions (chunk level, out of the 3,740 `section_v2_1` chunks of the 71 documents)
| Reason | Chunks |
|---|---:|
| Non-content section (`retrieval_eligible=false`: references, contributors, front/back matter, noise) | 1,061 |
| `table_structure_unrecoverable` (PDF table lost its structure) | 193 |
| `text_encoding_lost` (`/gid…` glyph codes) | 40 |
| `table_recovered_pending_review` | 11 |
| `undetermined_content_section` (`unclassified`) | 32 |
| `fragment_too_short` (< 6 words) | 19 |
| `duplicate_content_of:<chunk_id>` (identical content; the first copy is kept) | 46 |
| **Total excluded** | **1,402** (3,740 − 2,338) |

The rules are in `app/ingest/embedding_manifest.py` (10 unit tests). Each chunk's details are in [embedding_excluded.csv](embedding_excluded.csv) (1,402 chunk rows plus 103 source/document rows). If a document has both good and bad chunks, only the bad chunks are excluded.

## 4. Runs and API requests
| Run (`ingestion_runs`) | Status | Batches | HTTP requests | Vectors stored | Tokens billed | Duration |
|---|---|---:|---:|---:|---:|---:|
| `db86b899-e323-4e53-a07b-369a7a3a804f` | partial | 25 (14 ok, 11 failed) | 66 | 1,282 | 463,767 | 262.9 s |
| `9ff0e23c-acd0-4964-9085-40668119bac0` | succeeded | 11 (11 ok) | 11 | 1,056 | 353,658 | 247.8 s |
| `d09c8410-0c90-4e00-bf41-83e5e6a2c84d` (idempotency re-run) | succeeded | 0 | 0 | 0 | 0 | 0.0 s |
| **Total documents** | | 25 successful batches | **77** | **2,338** | **817,425** | ≈ 8.5 min |
| `verify --query-check` (5 test questions, no document text sent) | — | — | 2 (1 run whose stdout output was lost to an encoding error, then re-run) | — | 78 per run | — |

Notes:
- Token estimate from preflight was 825,945 (tokenizer `embed-v4.0`); Cohere billed 817,425 (−1.0%).
- Trial key: 79 / 1,000 requests per month used.
- Each batch is its own transaction. Vectors are written only when the response count equals the batch size and every vector passes the 1536-dimension / finite-value check. The vector count in the DB is checked again before commit.

## 5. Errors and how they were handled
| Error | Handling |
|---|---|
| **Run 1: 11/25 batches got an HTTP error after 4 attempts** (`provider_http`, retryable). Pattern: at each new minute 2–4 batches (~80–150k tokens) went through, and the remainder failed until the next minute. Most likely a **per-minute token limit on the trial key** (429). The exact status code was not recorded in run 1 because the client stored only the error code. | No vectors were written for the failed batches; all 11 are recorded in [embedding_failed_batches.csv](embedding_failed_batches.csv) (`error` column is empty for run 1). Fixes: the error now includes the HTTP status, and pacing uses a rolling 60 s window of ≤ 90k tokens. Run 2 embedded only the 1,056 missing chunks: 11/11 batches, each in a single request. |
| `verify` stdout used cp1252 on Windows and crashed while printing Vietnamese text (after the checks had finished) | Added `sys.stdout.reconfigure(encoding="utf-8")` and re-ran `verify`, which cost 1 extra query request. |
| `embedding_run_manifest.csv` was overwritten by the idempotency re-run, so every status became "already_stored" | Status is now the final state (`stored` + `run_id` of the run that stored it); the file was regenerated without calling the API. `embedding_failed_batches.csv` now accumulates across runs. |

No unsafe errors occurred: the provider was not switched, the dimension did not change, nothing was deleted and nothing was overwritten.

## 6. Database checks (`scripts/db_check.py`, tests)
| Check | Result |
|---|---|
| Migrations | 001–006; `db_check` ok |
| Permissions | **34/34** (25 existing + 9 for 006) |
| Research vectors | 2,338; wrong dimension 0; not a candidate 0; duplicate `chunk_id` 0; production authorization 0 |
| Dimension | column `vector(1536)`, recorded value 1536, `vector_dims` 1536 for all rows |
| NaN/Inf | 0; L2 norm 0.99999–1.00000 |
| Provenance | 100%: source_id, document_id, URL, page (PDF) or character range |
| Re-run | 0 new vectors, 0 API requests |
| Tests | ruff clean; **82 unit** (+11 new); **11 integration** (+4 new: `tests/integration/test_research_embeddings.py`) |
| Production | `chunk_embeddings` 0; `v_embedding_eligible_documents` 0; `v_retrieval_ready_chunks` 0; approvals 0; rights flags 0 |
| Chunks | v1 599 · v2 1,131 · v2_1 3,740 — unchanged |
| Raw | 199/199 files match `backups/raw_baseline_2026-11-14.sha256` |

## 7. Database changes
Backup before any change: `backups/asd_rag_v2_pre006_20261114_192229.dump` (SHA-256 `3fb1bac7…5d82`).

**Migration 006 `research_embedding_track`**: new objects only; no existing object or grant was changed. Scope and impact are in [embedding_research_gate_proposal_2026-11-14.md](embedding_research_gate_proposal_2026-11-14.md).

Testing:
- Run on an isolated container (tmpfs, port 5439; port 5434 belongs to another project and was left alone).
- Sequence: apply, 21/21 behaviour probes, rollback, re-apply, then `db_check`.

Records written:
- Owner role: 1 research authorization (`authorization_id = 1`, scope `research_test`, `production_approval = false`) covering 71 sources and 2,338 chunks (manifest `542cce21…`). It records this task's request from the project owner; it is not a licence decision.
- Ingest role: 3 `ingestion_runs` and 2,338 `research_chunk_embeddings` rows.

## 8. Code changes
**New**
- `app/ingest/embedding_manifest.py`.
- `scripts/embedding_preflight.py`, `scripts/embed_research.py` (`authorize` / `run` / `verify`).
- `migrations/006_research_embedding_track.sql` + `rollback/006_down.sql`.
- `tests/unit/test_embedding_manifest.py`, `tests/integration/test_research_embeddings.py`.

**Modified**
- `app/retrieval/embeddings.py`: counts billed tokens; +1 test.
- `scripts/db_check.py`: 006 checks.

**Unchanged**
- `scripts/embed_chunks.py` (production path, still guarded by the production gate).
- Chunking, raw, corpus.

## 9. Open issues
1. **Not legal approval:** groups B (NC) and C (agency policy) are embedded for non-commercial student research at the owner's request. Production use still needs owner decisions on `*_allowed` plus content approval. Research vectors can be promoted only when the input hash is identical.
2. The trial key has a per-minute token limit and a 1,000-request monthly limit. Cohere's terms for trial keys are recorded in `docs/provider_terms/cohere_2026-11-14.md`.
3. 32 `unclassified` chunks (some are real content, e.g. WHO-CST-PARTICIPANTS session 7) and 11 tables pending review are not embedded. Once they are reviewed: new preflight → new authorization → `run --execute` (only the delta is embedded).
4. Query check: some top hits are workbook boilerplate ("check your answers…"), and the CDC page has the "Image: …" placeholder. Handle this in Phase 5 (FTS + rerank + filtering) and in evaluation with an expert-reviewed question set.
5. No ANN index yet (exact search over 2,338 vectors is fine for now). `section_v2_1` cannot be re-chunked for embedded documents (`ON DELETE RESTRICT`) unless the research vectors are first dumped and deleted deliberately.
