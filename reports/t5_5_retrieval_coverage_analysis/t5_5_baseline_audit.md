# T5.5 Phase 0 — Baseline Audit

Read-only. All facts below are re-derived from the current code/config/DB this task, not assumed from
older reports where the code might have since diverged (the older FTS reports from T2.4, 2026-11-15, are
cited explicitly where still accurate, and the audit re-confirms them live rather than trusting them).

## 1. What actually powers `/api/chat` today

- **Dense retrieval only.** `app/retrieval/dense.py`'s `DenseRetriever`, wrapped by `CachedQueryEmbedder`
  (`app/retrieval/query_embedding.py`), reading `asd_rag.v_research_retrieval_chunks` as the
  `asd_rag_v2_research_reader` role.
- **No query expansion for dense.** `config/retrieval_profiles.json`'s `dense_baseline_v1` sets
  `"query_expansion": false` — the Vietnamese query text is embedded exactly as typed, no synonym
  substitution, no glossary, no stemming. All cross-lingual matching (Vietnamese question → English
  corpus) is done entirely by the embedding model's semantics, not by any text normalization step.
- **Cache-only query embedding.** `CachedQueryEmbedder` (`app/retrieval/query_embedding.py:64-117`) has
  `inner=None` in the live app — confirmed by re-reading `app/api.py`'s app-construction code. Any query
  text whose `sha256(profile|model|dim|input_type|text)` is not already a file in
  `data/index/query_embeddings/` raises `RetrievalError("embedding_unavailable", ...)`, surfaced as HTTP
  503 `QUERY_NOT_CACHED`. This happens **before** the DB is ever touched — no dense search, no Evidence
  Gate, no citation validation runs for a cache-miss query. This is the single most important
  architectural fact for this task: **a cache miss is not a retrieval failure or a gate rejection — it
  is the pipeline refusing to even attempt retrieval**, by the T2.6 cache-only design.
- **Evidence Gate** (`app/retrieval/evidence_gate.py`) only ever sees chunks that dense retrieval already
  returned for a cached query — it never runs at all for a cache-miss query. Its `assess()` requires each
  `RetrievedChunk.cosine_similarity`, a field only dense retrieval populates.
- **Reranking: OFF.** No reranker code is called anywhere in `app/api.py`'s handler. `ENABLE_LIVE_RERANKING`
  defaults `False` and is fail-loud if set `True` (`app/config.py:59-65`).
- **LLM: OFF.** No LLM call exists anywhere in the answer path; `app/answer/answer_generator.py` is
  entirely deterministic template/fallback logic. `ENABLE_LIVE_LLM` defaults `False`, same fail-loud gate.
- **Live Cohere query embedding: OFF.** `ENABLE_LIVE_QUERY_EMBEDDING` defaults `False`, same fail-loud
  gate. T2.6 remains `APPROVAL_REQUIRED` — not touched, not re-evaluated, not changed by this task.

## 2. A second retrieval system exists in the codebase but is NOT wired into the live demo

`app/retrieval/fts.py` — a complete, independently tested PostgreSQL full-text-search (sparse/lexical)
retriever, built and evaluated in an earlier task (T2.4, 2026-11-15; see
`eval/reports/phase_6_2_t2_4_fts_baseline_report_2026-11-15.md`,
`eval/reports/fts_architecture_audit_2026-11-15.md`). Re-confirmed this task:

- **Needs no query embedding at all** — it runs `plainto_tsquery`/`phraseto_tsquery` directly against
  `asd_rag.v_research_retrieval_chunks.content_tsv`, via the same read-only `research_reader` role. This
  makes it the **only tool available under this task's cache-only constraints** that can examine whether
  the corpus contains relevant content for a brand-new, never-cached query — it was used for exactly that
  purpose in Phase 1/2 of this task (see `t5_5_retrieval_diagnostics.md`).
- **`import app.api`: grep confirms zero references to `fts.py`, `FtsRetriever`, or `FtsProfile` anywhere
  in `app/api.py`.** The live demo has never used sparse retrieval as a fallback when dense/cache misses.
- **Three configured profiles** (`config/fts_profiles.json`): `fts_a_baseline_v1` (raw Vietnamese text,
  AND), `fts_b_glossary_and_v1` (glossary-expanded English terms, AND over concepts), `fts_c_glossary_or_v1`
  (same expansion, OR over concepts). All three use PostgreSQL's `english` text-search config and
  `ts_rank_cd` (cover-density rank — explicitly **not** BM25, and the T2.4 report is careful never to call
  it that).
- **Status carried forward unchanged since T2.4**: a blind candidate-annotation pool was built
  (`eval/reports/fts_candidate_pool_2026-11-15.jsonl`, 2,791 question–chunk pairs) but **never
  human-annotated** — `eval/reports/phase_6_2_t2_4_fts_baseline_report_2026-11-15.md` states
  "PENDING ANNOTATION... không dùng nhãn AI" (pending annotation; AI labels not substituted). This project's
  memory record confirms 0 human labels exist as of this task. Every FTS-vs-dense comparison number from
  T2.4 is therefore still only EXPLORATORY, not a validated benchmark — re-stated here, not re-derived,
  because the pool and its annotation status are unchanged.

## 3. Two separate, not-fully-aligned glossaries exist

- `app/nlp/text_match.py`'s `GLOSSARY` dict: **63 entries**, used by the live answer path (template
  query-gating, Evidence Gate's `specific_terms()`/`chunk_matches_terms()`). Simple VI phrase → list of
  English substrings, matched by plain substring search (no tsquery, no stemming awareness).
- `config/query_glossary_vi_en_v1.json`: **94 entries** (+ 3 age-pattern regexes), used only by
  `app/retrieval/fts.py`'s glossary-expansion query modes (FTS-B/FTS-C). Built independently in T2.4 for
  a different purpose (boolean tsquery construction) and never reconciled with the 63-entry glossary.
- **Neither glossary is used by dense retrieval at all** (dense has no query expansion step, per §1).
  They currently only affect: (a) which of the 17 answer templates fire (`text_match.py`'s 63 entries),
  and (b) FTS's search terms, which in turn are not even wired into the live app (per §2). This means the
  demo's actual query-time cross-lingual bridging is *entirely* the embedding model's own semantics — no
  explicit VI→EN term mapping participates in what dense retrieval returns at all today.

## 4. Chunk / source metadata actually available (re-confirmed by direct query this task)

`asd_rag.v_research_retrieval_chunks` exposes, per chunk: `chunk_id, source_id, document_id, title,
source_url, section_heading, section_path, page_start, page_end, char_start, char_end, content,
content_sha256, chunking_profile, document_version, authorization_id, profile_code` (dense) plus
`content_tsv` (FTS only). **2,291 chunks** currently retrievable (re-counted live this task via
`SELECT count(*) FROM asd_rag.v_research_retrieval_chunks` as the research reader — this is the number of
*chunks*, distinct from the "2,338 embedding vectors" figure cited in this project's protected-boundary
language, which likely includes a small number of non-retrievable/quarantined vectors; this task did not
investigate that difference further, as it is outside T5.5's scope and the vector set itself must not be
touched).

## 5. Cache-only limitations, stated precisely

- The query **cache keys on exact text** (`sha256(profile|model|dim|input_type|text)` — literally the
  full query string, not a normalized or semantic key). Any character-level difference (a comma, a typo,
  a synonym, a reordered clause) produces a different key and therefore a cache miss, **even if the
  underlying information need is identical to an already-cached, already-answered question.**
- There is no semantic nearest-neighbor fallback among cached vectors — a cache miss is terminal, not "use
  the closest cached query instead." This is a deliberate design choice (avoids silently answering a
  different question than the one asked) but it means the 2,291-chunk corpus's effective reachable
  surface, for any given demo session, is only as large as the literal set of previously-cached query
  strings (171 cached vectors across the 105-set + 66-set, confirmed by this project's prior T2.3/T5.1
  reports), not the corpus's true semantic coverage.

## 6. Summary table — what is ON vs OFF today

| Component | State | Evidence |
|---|---|---|
| Dense retrieval (cache-only) | **ON** — sole retriever for `/api/chat` | `app/api.py` imports only `dense.py`/`query_embedding.py` |
| Live query embedding (Cohere) | **OFF** (fail-loud) | `app/config.py:58`, T2.6 `APPROVAL_REQUIRED` |
| FTS / sparse retrieval | Built, tested, **NOT wired into `/api/chat`** | `app/retrieval/fts.py` unreferenced by `app/api.py` |
| Reranking | **OFF** (fail-loud) | `app/config.py:59` |
| LLM generation | **OFF** (fail-loud), templates are static strings | `app/config.py:60`, `answer_generator.py` has no LLM call |
| Query expansion (dense) | **OFF** by profile config | `config/retrieval_profiles.json` |
| Query expansion (FTS, unused live) | present in 2 of 3 FTS profiles | `config/fts_profiles.json` |
| Evidence Gate | **ON**, but only reachable after a cache hit | `evidence_gate.py` requires `cosine_similarity` |
| FTS human annotation pool | Built, **0 human-annotated** | `eval/reports/phase_6_2_t2_4_fts_baseline_report_2026-11-15.md` |

This baseline is the foundation for Phases 1–5: because dense retrieval cannot be run live on any text
that is not already cached, and FTS is the only cache-only-compliant tool that can inspect corpus content
for new text, **FTS (plus direct keyword inspection of chunk content) is used throughout this task as the
diagnostic instrument for the independent 31-question cache-miss set — not as a claim that FTS is, or
should become, the production retriever.**
