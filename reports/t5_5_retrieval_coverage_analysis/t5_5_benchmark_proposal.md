# T5.5 Phase 5 — Retrieval Benchmark Proposal

**Status: PROVISIONAL.** No human-adjudicated relevance label exists for any (query, chunk) pair in the
31-question independent set. This proposal defines the benchmark's schema and process; it does not
contain any invented relevance judgment, and it must not be read as a completed benchmark.

## Why a new benchmark, not a reuse of the existing one

The existing frozen benchmark (`eval/datasets/retrieval_eval_v1.jsonl`, 66 questions) has its own
candidate pool and its own `PENDING ANNOTATION` FTS pool (T2.4, 2,791 pairs, still unlabeled). This task's
31 independent-set questions are a *different* frozen set (`eval/datasets/independent_eval_v1.jsonl`,
created in T5.4 specifically to avoid template-tuning contamination). A retrieval benchmark for them must
be built the same way, from scratch, not retrofitted onto the 66-question pool — mixing the two would
undermine both sets' independence guarantees.

## Required schema (per the task's specification)

| Field | Source | Notes |
|---|---|---|
| `query` | `eval/datasets/independent_eval_v1.jsonl` | the 31 cache-miss questions (the other 1, `ie016`, is a safety refusal with no retrieval attempt at all, so it is out of scope for a retrieval benchmark) |
| `relevant_source` / `relevant_chunk` | **not yet populated — requires human annotation** | candidate chunk IDs come from the union of FTS-A/B/C top-10 (this task's diagnostic run, `eval/reports/t5_5_fts_diagnostics.json`) plus, if/when C1 (live query embedding) is ever authorized, dense top-20 |
| `relevance_judgment` | **not yet populated** | proposed scale: reuse the existing project's 3/2/1/0/−1 grade scale (T2.3/T2.4), for direct comparability with the 66-question benchmark's own scale |
| `dense_rank` | **not available** | dense retrieval cannot be run on this uncached text without live embedding (T2.6); this field is structurally `null` for every row until/unless C1 is authorized — stated explicitly, not left ambiguous |
| `fts_rank` | populated, this task | FTS-A/B/C ranks, already captured in `eval/reports/t5_5_fts_diagnostics.json` |
| `evidence_type` | populated, this task (direct/indirect/generic/none) | produced via the same `app.nlp.text_match` term-matching logic the live Evidence Gate uses, applied manually to FTS hits (Phase 2's method) — itself only a proxy, disclosed as such |
| `evidence_gate_result` | **not available for any row** | the Evidence Gate never runs on a cache-miss query (Phase 1's architectural finding); this field is structurally `null` for every row in this benchmark by construction, not a missing value to fill in |
| `failure_category` | populated, this task | the 5-category taxonomy from `t5_5_cache_miss_taxonomy.md`, applied per question (not yet per chunk — see "what remains before this is a real benchmark" below) |

## What exists today vs. what remains

**Exists today** (produced this task, read-only): the 31 queries; FTS-A/B/C ranks and raw content for
their top-10 each; the per-question failure-category classification; cross-references to which corpus
sources already power live templates (a strong but informal relevance signal, not a substitute for
adjudication).

**Remains before this is a genuine benchmark**, in order:
1. **Human relevance adjudication**, per (query, chunk) pair, not per question — the same blind-export /
   sealed-key pattern already used for the 66-question FTS pool in T2.4
   (`eval/reports/fts_candidate_pool_2026-11-15.jsonl` / `fts_candidate_pool_key_2026-11-15.jsonl` is the
   template to follow exactly: blind content export with no system/rank/score visible to the annotator,
   a separately sealed key file with provenance).
2. **A decision on whether to pool FTS candidates alone, or also run dense** (requires C1's authorization
   decision; until then, the pool can only be FTS-derived, which under-represents whatever dense might
   find — the same labeled caveat the T2.4 report already carries for its own exploratory numbers).
3. Only after (1) and ideally (2): compute Recall@K/nDCG/MRR on the FTS systems against this new set, with
   the same honesty standard T2.4 already set (recall/precision/MRR are EXPLORATORY until coverage is high
   enough to trust, and the report must say so, not silently present a number as final).

## Explicit disclosure required of anyone using this benchmark later

- **No number in this proposal or its eventual filled-in version may be called a final Recall@K** until
  step 1 (human adjudication) is complete, following T2.4's own precedent exactly (that pool is also still
  `PENDING ANNOTATION`, never promoted to a "real" benchmark in any report since).
- **This benchmark must never be used to tune the glossary, FTS profiles, or any answer template and then
  still be called an independent test** — the same prohibition T5.4 stated for the 31-question
  independent-evaluation set, carried forward here because this benchmark is built directly from that
  same frozen set.
- `dense_rank` and `evidence_gate_result` being structurally `null` for every row is a **statement about
  this task's tooling limits** (cache-only, no live embedding), not a property of the questions or the
  corpus — a future task with different authorization could fill these in without changing the `query` or
  `relevant_chunk` columns at all.

## Deliberately not produced in this task

No `t5_5_benchmark.jsonl` data file is created, because creating it would require either (a) inventing
relevance judgments (explicitly forbidden — "Không được tự đặt số liệu để lấp khoảng trống") or (b)
copying the already-gathered FTS diagnostic data into a new filename while implying it is adjudicated,
which it is not. `eval/reports/t5_5_fts_diagnostics.json` already contains everything needed to build the
blind export once annotation is actually commissioned; duplicating it under a new name would not add
information, only the risk of the two files drifting apart.
