# T5.6 Phase 0 — Baseline Audit (re-verified directly, not inferred from T5.5)

Every claim below was re-checked against the current code/config/DB this task, not copied from
`reports/t5_5_retrieval_coverage_analysis/`. Where this re-check confirms T5.5's findings unchanged, that
is stated as "re-confirmed," not re-derived from scratch narration; where anything differs, it is called
out explicitly (nothing did, this task).

## 1. The two glossaries — re-confirmed unchanged, counted directly

- `app/nlp/text_match.py`'s `GLOSSARY` dict: **63 entries** (re-counted live: `len(GLOSSARY) == 63`).
  Used by the live answer path: template query-gating (`_template_for`/`_new_template_for` in
  `app/answer/answer_generator.py`) and the Evidence Gate's `specific_terms()`/`chunk_matches_terms()`
  (`app/retrieval/evidence_gate.py`).
- `config/query_glossary_vi_en_v1.json`: **94 entries** (re-counted live), used only by
  `app/retrieval/fts.py`'s glossary-expansion query modes (FTS-B/FTS-C). Not imported by, or reachable
  from, `app/answer/` or `app/retrieval/evidence_gate.py` at all — re-confirmed via `grep` for any
  cross-import; none exists.
- Full reconciliation (overlap, conflicts, gaps) is in `t5_6_glossary_reconciliation.md`.

## 2. FTS implementation — re-confirmed unchanged

`app/retrieval/fts.py` (437 lines), 3 configured profiles in `config/fts_profiles.json`
(`fts_a_baseline_v1`, `fts_b_glossary_and_v1`, `fts_c_glossary_or_v1`), all using PostgreSQL's `english`
text-search config and `ts_rank_cd` ranking. **Still not imported anywhere in `app/api.py`** (re-confirmed
by `grep -n "fts" app/api.py` — zero matches), i.e. still not reachable from the live chat endpoint. This
matches T5.5's finding exactly; re-verified, not assumed.

## 3. Dense retrieval — re-confirmed unchanged

`app/retrieval/dense.py` + `app/retrieval/query_embedding.py`'s `CachedQueryEmbedder`. Re-read live:
`app/api.py`'s app-construction path still builds the embedder with `inner=None`. `config/
retrieval_profiles.json`'s `dense_baseline_v1` still has `"query_expansion": false` — dense retrieval
applies zero text normalization or glossary expansion to the query before embedding it.

## 4. Query normalization — a more precise statement than T5.5's, re-derived this task

T5.5's baseline audit stated "no explicit VI→EN term mapping participates in what dense retrieval
returns." Re-checking this task, more precisely: the ONLY normalization dense retrieval's query path
performs is `DenseRetriever.validate_query()`'s `.strip()` (whitespace trim) — there is no lowercasing, no
Unicode normalization (NFC/NFD), no diacritic folding, and no punctuation stripping before the text is
handed to the embedder. FTS, by contrast, does apply `unicodedata.normalize("NFC", ...)` and whitespace
collapsing (`fts.py`'s `normalize_query()`) before building a tsquery. This asymmetry was not previously
stated this precisely and is relevant to Phase 2's experiments (which only touch the FTS side).

## 5. Cache lookup and cache-miss flow — re-confirmed unchanged

`CachedQueryEmbedder.embed_queries()` (`app/retrieval/query_embedding.py:98-117`): cache key =
`sha256(profile_code|model_id|vector_dimension|input_type|text)` — the literal, un-normalized query text
is part of the hash input (re-read the function directly: `raw = f"{profile.profile_code}|...|{text}"`,
no `.lower()`/`.strip()`/fold applied before hashing). A cache miss raises `RetrievalError
("embedding_unavailable", ...)` before any DB call. Re-confirmed by direct code read, not assumed.

## 6. Evidence Gate — re-confirmed unchanged

`app/retrieval/evidence_gate.py`'s `assess()` still requires `chunk.cosine_similarity` on every item in
`results`; this field only exists on dense retrieval's `RetrievedChunk`, never on FTS's `FtsHit`
(`app/retrieval/fts.py`'s dataclass, re-checked: no `cosine_similarity` field). The Gate is therefore
still structurally unusable on FTS output without an adapter — a design point developed further in
`t5_6_integration_design.md`.

## 7. Answer generation — re-confirmed unchanged, 17 templates, all query-term-gated except one catch-all

`app/answer/answer_generator.py` (365 lines, byte count unchanged since T5.3/T5.4): 7 old
`_TOPIC_TEMPLATES` + 10 new `_QUERY_GATED_TEMPLATES`/`signs_by_age`, all requiring a specific query term
except the single `asd_definition` catch-all (checked last). No LLM call anywhere in this file —
re-confirmed by `grep` for any import of an LLM client; none exists.

## 8. Source/citation validation — re-confirmed unchanged

`app/retrieval/citation_validation.py`'s `validate()` still checks `source_id`/`title`/`source_url`/
`excerpt` field-for-field against a real `RetrievedChunk`. It is never called on an `FtsHit` today, since
FTS is never reached at all in the live path (per §2).

## 9. Answer Quality Reference — baseline check against the current pipeline, this task

The task's reference example ("ASD là gì?" must get a structured Vietnamese answer, never raw English or
internal metadata) was checked live against the current pipeline before any experiment:

| Query | HTTP | `answer_mode` | Note |
|---|---|---|---|
| "ASD là gì?" | 503 | `none` | `QUERY_NOT_CACHED` — cache miss, no answer of any kind, structured or not |
| "Trẻ tự kỷ có những biểu hiện gì?" | 503 | `none` | cache miss |
| "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?" | 200 | `topic_template` | **already meets the reference today** — a cached, structured Vietnamese `signs_by_age` answer with citations |
| "ASD và ADHD khác nhau như thế nào?" | 503 | `none` | cache miss |
| "Trẻ tự kỷ có thể gặp khó khăn về ngôn ngữ không?" | 503 | `none` | cache miss |
| "Người tự kỷ có thể gặp khó khăn về giấc ngủ không?" | 503 | `none` | cache miss |

5 of the 6 Phase-5 evaluation questions cache-miss today — this is the concrete starting point this task's
remaining phases work from (not a hypothetical). Full detail in `t5_6_answer_quality_evaluation.md`.

## 10. Protected boundaries re-confirmed before any experimental change

- `ASD_DEMO_MODE=true`, all three `ENABLE_LIVE_*` flags `False`, fail-loud gate unchanged
  (`app/config.py:57-65`, re-read this task).
- DB container already running; a `research_reader` connection succeeded at the start of this task without
  this task starting or stopping Docker.
- No row of `asd_rag.v_research_retrieval_chunks` or the underlying vector table was written to at any
  point in this task (read-only `conn.read_only = True` on every connection opened).
