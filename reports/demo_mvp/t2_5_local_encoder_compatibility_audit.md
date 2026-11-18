# T2.5 — Local Query Encoder Compatibility Audit

**Scope:** read-only audit. No PostgreSQL writes, no vectors created or modified, no model downloaded,
no package installed, no API request sent, no change to the running Retrieval API, no change to the
T2.3 benchmark, no Git commit. Status transition authority (`QUERY_EMBEDDING_BLOCKED` → anything else)
is explicitly **not** exercised by this report.

Everything below was verified directly against this machine and this repository on 2026-11-17
(working directory `d:\AI4LIFE\ASD_AGENT_FINALL`). Where the prior audit
[`query_embedding_options_audit.md`](query_embedding_options_audit.md) (T2.5-DEV-3) already reached the
same finding, that is stated and re-confirmed, not assumed.

---

## 1. Environment inventory

| Item | Finding | Evidence |
|---|---|---|
| Python | 3.12.4 (MSC v.1940 64-bit, Windows) | `.venv/Scripts/python.exe -c "import sys; print(sys.version)"` |
| Virtualenv packages | 108 entries total in `.venv/Lib/site-packages`; full list captured below | directory listing |
| PyTorch | **Not installed** | `import torch` → `ModuleNotFoundError` |
| transformers | **Not installed** | `import transformers` → `ModuleNotFoundError` |
| sentence-transformers | **Not installed** | `import sentence_transformers` → `ModuleNotFoundError` |
| onnxruntime | **Not installed** | `import onnxruntime` → `ModuleNotFoundError` |
| fastembed | **Not installed** | `import fastembed` → `ModuleNotFoundError` |
| Cohere Python SDK | **Not installed** (project calls the HTTP API directly via `httpx`, not the SDK) | `import cohere` → `ModuleNotFoundError` |
| `huggingface_hub` | Installed (2.4.0) — a transitive dependency, not an embedding runtime by itself | site-packages listing |
| GPU | NVIDIA GeForce RTX 2050, driver 610.78, 4096 MiB VRAM | `nvidia-smi --query-gpu=name,driver_version,memory.total` |
| GPU usable for inference | **No** — no CUDA-enabled ML runtime (torch/onnxruntime) is installed | consequence of the above |
| Local model weights | **None found.** Only `prajjwal1/bert-tiny`'s `config.json` (285 bytes) is cached under `~/.cache/huggingface/hub/models--prajjwal1--bert-tiny/blobs/`. `tokenizer.json`, `tokenizer_config.json`, `added_tokens.json`, `special_tokens_map.json`, `chat_template.jinja`, `tokenizer.model` are all recorded as `.no_exist` (Hugging Face's own marker that a resolve attempt found them absent on that revision). No `pytorch_model.bin`, `model.safetensors`, `.onnx`, or `.gguf` file exists anywhere searched. | `find ~/.cache/huggingface`, blob content dump |
| Other model caches | None found under the project tree or common cache roots (`*.gguf`, `*.onnx`, `*huggingface*`) | filesystem search |
| Installed packages relevant to the app | `fastapi 0.163.1`, `uvicorn 0.54.0`, `starlette 1.10.0`, `pydantic 2.14.3`, `httpx 0.28.1`, `psycopg[binary] 3.3.9`, `pypdf 6.11.0`, `pdfplumber 0.11.10`, `tokenizers 0.23.3`, `pytest 9.2.0`, `ruff 0.17.5`, plus their transitive deps (full list in site-packages, no ML runtime among them) | `ls .venv/Lib/site-packages` |

**Conclusion of Phase 2:** the only locally-cached artifact that resembles an embedding model
(`prajjwal1/bert-tiny`) is a *config stub with no weights and no tokenizer files*, and no library capable
of loading or running any embedding model (PyTorch, TensorFlow, ONNX Runtime, sentence-transformers,
FastEmbed) is installed. There is no local encoder of any kind that can currently produce a vector. This
matches and reconfirms the T2.5-DEV-3 finding; nothing in the environment has changed since that audit
except the addition of the FastAPI/Uvicorn/Pydantic web-serving stack, which is unrelated to embedding.

No model was downloaded and no package was installed during this audit.

---

## 2. Document embedding provenance (the 2,338 stored vectors)

Source: `config/embedding_profiles.json` (profile `cohere_embed_v4_1536_v1`), `migrations/001_core_schema.sql`
(`embedding_profiles`, `chunk_embeddings` DDL), `app/retrieval/embeddings.py`, `app/ingest/embed_pipeline.py`,
and `eval/reports/embedding_run_report.md` (the actual run report for the 2,338 vectors).

| Attribute | Value | Source |
|---|---|---|
| Provider | Cohere | `embedding_profiles.json` |
| Model name | `embed-v4.0` | `embedding_profiles.json`; `embedding_run_report.md` §1 |
| Model version/revision | `model_revision: null` — Cohere does not expose a pinned revision/checkpoint id for this hosted model | `embedding_profiles.json` |
| API | Embed API **v2**, `POST https://api.cohere.com/v2/embed` | `embedding_profiles.json`; `app/retrieval/embeddings.py:21` |
| Embedding dimension | 1536 (`output_dimension` requested explicitly in the payload) | `embeddings.py:67` (`payload()`); DB column `embedding public.vector(1536)`; DB check confirms `vector_dims` = 1536 for all 2,338 rows (`embedding_run_report.md` §6) |
| Embedding type | `float` (code rejects any other `embedding_types` value) | `embeddings.py:55-56` |
| Document input_type | `search_document` | `embedding_profiles.json`; used for all document chunks |
| Query input_type | `search_query` | `embedding_profiles.json`; used for test questions only |
| Document input text format | `"{title}\n{section_heading}\n\n{content}"`, stripped | `embedding_profiles.json` (`input_template`); `embed_pipeline.py:52` (`build_input`) |
| Input preprocessing | Only the template substitution + `.strip()` above; `truncate = "NONE"` (the API errors instead of silently truncating oversized input) — no other normalization, lowercasing, or tokenization performed client-side | `embed_pipeline.py:52-53`; `embedding_profiles.json` |
| Chunking profile feeding the embedder | `section_v2_1` | `embedding_profiles.json`; `embed_pipeline.py:25` |
| Task type / instruction | Cohere's built-in `input_type` parameter is the only task-type signal (`search_document` vs `search_query`); no additional instruction prefix is added by this codebase | `embeddings.py:67` |
| Pooling | **Not disclosed.** `embed-v4.0` is a closed, hosted Cohere model; Cohere does not publish its internal architecture or pooling strategy, and nothing in this codebase or its docs records one | absence of any pooling code/config — the client only POSTs text and receives vectors |
| Normalization | Vectors are returned already close to unit length: DB check reports L2 norm range **0.99999–1.00000** across all 2,338 vectors. The pipeline does not renormalize; `l2_norm()` in `embed_pipeline.py:62-63` is used only to record the observed norm, not to transform the vector | `embedding_run_report.md` §6; `embed_pipeline.py` |
| Vector dtype | Stored as Postgres `pgvector` `vector(1536)` (32-bit float internally); validated client-side as Python `float`/`int`, rejecting booleans, non-finite, and non-list values before storage | `embeddings.py:71-78` (`validate_vector`); `001_core_schema.sql:143` |
| Similarity metric | Cosine (`similarity_metric` column constrained to `'cosine'`; retrieval uses pgvector `<=>`) | `001_core_schema.sql:130`; `dense_retrieval_audit.md` |
| Batch size / rate limits | ≤ 96 texts/call; paced ≤ 1,800 inputs/min and ≤ 90k tokens per rolling 60 s window (added after a trial-key rate-limit failure in run 1) | `embedding_profiles.json`; `embedding_run_report.md` §5 |
| Provenance recorded per vector | `chunk_id`, `profile_id`, `embedding_input_hash` (sha256 of `provider|model_id|dimension|document_input_type|text`), `vector_norm`, `created_at`; 100% of the 2,338 rows have source/document/URL + page-or-character-range provenance | `001_core_schema.sql:139-148`; `embed_pipeline.py:56-59`; `embedding_run_report.md` §6 |
| Run identity | 3 `ingestion_runs` (`db86b899…`, `9ff0e23c…`, `d09c8410…` idempotency re-run); 2,338 rows in `research_chunk_embeddings`, 0 wrong-dimension, 0 duplicate `chunk_id` | `embedding_run_report.md` §4, §6 |

**No speculative attributes.** Cohere's internal tokenizer, pooling layer, and any instruction-tuning
applied inside `embed-v4.0` are not published by the provider and are not recorded anywhere in this
project; this report states that gap explicitly rather than guessing at it.

---

## 3. Candidate encoders found

Only one candidate exists on this machine, and it is not runnable:

| Candidate | What exists | What is missing |
|---|---|---|
| `prajjwal1/bert-tiny` (Hugging Face cache) | `config.json` only (hidden_size 128, 2 layers, 2 attention heads, vocab 30522) | Model weights, tokenizer files (all marked `.no_exist`), and any installed library (`transformers`/`torch`) to load or run it |

No other local embedding model, ONNX export, GGUF file, or embedding-capable runtime was found anywhere
on the machine or in the project tree. No local encoder candidate was downloaded or installed as part of
this audit.

---

## 4. Compatibility matrix

| Criterion | `prajjwal1/bert-tiny` (if it were runnable) |
|---|---|
| 1. Same model + version as document embedding | **No.** BERT-tiny is an unrelated open checkpoint; `embed-v4.0` is a proprietary Cohere model. |
| 2. Same architecture + weights | **No / unverifiable.** BERT-tiny's architecture (2-layer, hidden 128, 2 heads) is fully published; Cohere's `embed-v4.0` architecture is undisclosed. They cannot be the same, and there is no public weight overlap. |
| 3. Same preprocessing + task instruction | **No.** The document pipeline's exact template (`{title}\n{section_heading}\n\n{content}`) and Cohere's `input_type=search_document/search_query` signal are specific to the Cohere API; BERT-tiny has no equivalent built-in task conditioning. |
| 4. Same pooling | **Unverifiable.** Cohere's pooling is not published (see §2). BERT-tiny's pooling would have to be chosen arbitrarily (e.g., mean or CLS), with no reference to match against. |
| 5. Same normalization | **Partially observable, not reproducible.** Document vectors are empirically near-unit-norm (L2 ≈ 1.0), but nothing says bert-tiny embeddings would land in the same space even after normalization — normalization only rescales a vector, it does not move it into a different model's semantic space. |
| 6. Same dimension | **No.** BERT-tiny's native hidden size is 128, not 1536 (and even a dimension match would not establish compatibility — see constraint below). |

**Classification: INCOMPATIBLE.**

`prajjwal1/bert-tiny` fails criteria 1–4 and 6 outright, independent of whether it were installed and
runnable. No other candidate exists to classify. Per the task constraint, this conclusion is **not**
based on dimension alone — dimension is only one of six criteria, and five others independently fail
first.

A vector produced by any encoder other than the exact Cohere `embed-v4.0` endpoint and profile
configuration above must **not** be stored or compared against the existing 2,338 Cohere vectors in the
same column/index. Mixing vector spaces this way silently corrupts cosine-distance ranking (the geometry
is incommensurable even at matching dimension). Using a genuinely different encoder for new queries would
require a **separate re-embedding study**: a new `embedding_profiles` row, a parallel vector column/table,
and a full re-embed-and-evaluate pass — never an in-place substitution for `search_query` inputs against
the current `cohere_embed_v4_1536_v1` document vectors.

---

## 5. Evidence summary per conclusion

- **No local encoder is installed or runnable** — direct import failures for `torch`, `transformers`,
  `sentence_transformers`, `onnxruntime`, `fastembed`, `cohere` SDK in `.venv`; `.venv/Lib/site-packages`
  listing contains no ML runtime.
- **No local model weights exist** — only a 285-byte `config.json` for `bert-tiny` is cached; every other
  file for that repo is `.no_exist`; no `.bin`/`.safetensors`/`.onnx`/`.gguf` anywhere searched.
- **Document embeddings are Cohere `embed-v4.0`, dimension 1536, `search_document` input, template
  `{title}\n{section_heading}\n\n{content}`, cosine metric, near-unit L2 norm** — `config/embedding_profiles.json`,
  `app/retrieval/embeddings.py`, `app/ingest/embed_pipeline.py`, `eval/reports/embedding_run_report.md` §1 and §6
  (actual DB-verified run report for the 2,338 vectors, not a plan document).
- **Cohere's internal pooling/tokenization is not published anywhere this project has access to** — absence
  of any such documentation or code; stated as a gap, not inferred.
- **GPU exists but is unusable for local inference today** — `nvidia-smi` shows an RTX 2050, but no
  CUDA-capable ML library is installed to use it.
- **No authorization exists for sending arbitrary user queries to Cohere** — `docs/provider_terms/cohere_2026-11-14.md`
  documents a trial key with unresolved licence/data-handling conflicts for 13 CC BY-NC(-SA) documents and
  a `pending_decision` for the remaining 60; `eval/reports/embedding_run_report.md` records only
  pre-approved test questions (`search_query`, 5 questions, "no document text sent") as authorized Cohere
  query traffic, not demo/arbitrary user input.

---

## 6. Recommended options (two independent paths — neither is executed by this audit)

### Option A — Use a compatible local encoder
**Not currently available.** §4 found no candidate that passes the compatibility criteria, and none can
be loaded in this environment regardless (no ML runtime installed). This option is not actionable without
a separate re-embedding study: pick an open encoder, register a new `embedding_profiles` row, re-embed all
2,338+ chunks with it into a new column/table, and re-run the T2.3 benchmark against the new space. That
is out of scope for T2.5.

### Option B — Request authorization for Cohere to process arbitrary user queries
This is the only path that reuses the existing, already-verified `CohereQueryEmbedder` /
`CachedQueryEmbedder` code in `app/retrieval/query_embedding.py` without new model risk. If the project
owner grants it, the following should be specified explicitly:

- **Data sent:** only the end user's query text, as `search_query` input, batched through the existing
  `CohereEmbedder.embed()` call. Document chunk text is never part of a query-embedding request (this is
  already structurally true: `CohereQueryEmbedder.embed_queries` only ever receives `texts` passed in by
  the caller, never chunk content).
- **API / model used:** Cohere Embed API v2, model `embed-v4.0`, `output_dimension=1536`, `input_type=search_query`
  — i.e., exactly the existing profile `cohere_embed_v4_1536_v1`, unchanged.
- **Must not send:** document chunks or any retrieved content (already excluded by the data flow above);
  no personal or sensitive data — this requires the demo UI itself to avoid inviting users to type personal
  health information into the query box, since the embedder sends whatever text it is given verbatim.
- **Enable/disable control:** construct `CachedQueryEmbedder` with `inner=CohereQueryEmbedder(...)` to
  enable live fallback on cache miss, versus `inner=None` (current default) to stay fail-closed/offline.
  This should be a single explicit config flag (e.g., an environment variable gating whether `inner` is
  constructed), not a code change, so it can be flipped back without redeploying.
- **Error/revocation handling:** the existing `EmbeddingError`/`RetrievalError` mapping already fails
  closed on provider auth errors (401/403 → `provider_auth`), HTTP/network errors, and malformed
  responses, surfacing as HTTP 503 `embedding_unavailable`/`embedding_failed` (`app/api.py`). Revoking
  authorization only requires reverting to `inner=None`; no vectors or cache entries need to be deleted
  since the cache stores vectors and hashes only, never query text (`query_embedding.py` module docstring).
- **Outstanding legal gap to resolve first:** the trial key's Terms of Use grant Cohere a broad licence to
  use submitted data to improve its own services, which conflicts with the CC BY-NC/CC BY-NC-SA licence
  terms on 13 source documents *for document embedding*. This conflict is about document text, not query
  text, but the owner should confirm whether query text (which could echo or paraphrase NC-licensed
  content) raises the same concern before enabling live query traffic, and should decide whether a
  production key + training opt-out, or Zero Data Retention, is required first (see
  `docs/provider_terms/cohere_2026-11-14.md` §"Đánh giá").

---

## 7. Limitations and risks

- Cohere's pooling, exact tokenizer, and any instruction-tuning inside `embed-v4.0` are undisclosed by the
  provider; no local encoder can be verified bit-for-bit compatible even in principle, only operationally
  compatible (same provider endpoint, same parameters).
- This audit did not attempt to download, install, or run any model or package, per task constraints — so
  "no local encoder is runnable" reflects the *current* machine state and would need to be re-verified if
  the environment changes.
- `prajjwal1/bert-tiny`'s cache entry is incomplete (config only); it is unknown why it was ever fetched
  partially, and no inference was made about intended past use.
- The GPU (RTX 2050, 4 GB) was not exercised in any way; its presence is reported only as an inventory
  fact, not evidence of capability, since no ML runtime is installed to use it.
- The Cohere trial-key terms and licence-conflict analysis in `docs/provider_terms/cohere_2026-11-14.md`
  are from 2026-11-14 and the document itself flags unresolved items (current Terms of Use version,
  whether trial accounts can opt out of training use, Privacy Policy not yet read) — Option B should not
  be enabled on the strength of this audit alone without re-checking those open items.

---

## 8. Final status

**`NO_COMPATIBLE_LOCAL_ENCODER_FOUND`**

No local encoder exists on this machine or in this repository that is installed, runnable, or compatible
with the Cohere `embed-v4.0` / `cohere_embed_v4_1536_v1` document embedding space by the six stated
criteria. The only candidate found (`prajjwal1/bert-tiny`, config-only) fails on model identity,
architecture/weights, preprocessing/task instruction, and dimension — independent of the fact that it
cannot currently be loaded at all. `QUERY_EMBEDDING_BLOCKED` is **not** changed by this report; the
decision between Option A (a future re-embedding study) and Option B (requesting Cohere query
authorization) is left to the project owner.
