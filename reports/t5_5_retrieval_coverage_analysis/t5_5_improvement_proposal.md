# T5.5 Phase 4 — Improvement Proposals

None of these are implemented in this task. Each is a proposal only, per the task's explicit instruction
("Không triển khai các thay đổi thuộc B hoặc C," and no code change at all in T5.5).

---

## Level A — cache-only, no new approval needed

### A1. Wire FTS-B as a labeled, lower-confidence fallback when dense cache-misses

- **Problem**: 31/32 (97%) of brand-new, realistically-phrased questions in the independent set cache-miss
  and get nothing at all — not even a best-effort lexical answer. 11 of those 31 (Phase 1, category 3)
  have demonstrably on-topic corpus content findable by FTS alone.
- **How**: in `app/api.py`'s `/api/chat` handler, when `CachedQueryEmbedder` raises `QUERY_NOT_CACHED`,
  fall through to `FtsRetriever(fts_b_glossary_and_v1)` instead of returning 503 immediately. Run the
  existing Evidence Gate's term-matching logic (adapted, since FTS hits lack `cosine_similarity`) against
  the FTS results, and if evidence passes, return an `extractive_fallback`-style answer explicitly labeled
  "found via keyword search, not semantic search — lower confidence" in the response.
- **Risk**: FTS's known false-positive mode (Case F, `ie002` — a generic term like "intervention" producing
  a "direct" match on an unrelated chunk) would now reach end users, not just this internal report. Needs
  a stricter term-specificity filter than the current glossary (see A2) before this is safe to ship.
- **Cost/dependency**: moderate code change (new retrieval branch + a dedicated evidence classifier for
  FTS hits, since `evidence_gate.assess()` cannot be reused as-is); no new external dependency.
- **Before/after evaluation**: re-run the 31-question independent set end to end; measure how many move
  from `cache_miss` to a genuine `extractive_fallback`-equivalent, and separately measure false-positive
  rate on a sample via manual review (same method as this task's Phase 1/2).
- **Rollback**: a feature flag (`ASD_ENABLE_FTS_FALLBACK`, same `_flag()` pattern as the existing
  `ENABLE_LIVE_*` flags) defaulting `False`; disabling it returns to today's exact behavior with zero
  residual effect, since FTS code is entirely additive and touches no existing dense/cache code path.

### A2. Reconcile the two glossaries and add the specific vocabulary gaps found in T5.5

- **Problem**: `app/nlp/text_match.py`'s 63-entry glossary (gates templates + Evidence Gate) and
  `config/query_glossary_vi_en_v1.json`'s 94-entry glossary (gates FTS-B/C) were built independently and
  never reconciled (Phase 0, §3). This task found specific, concrete missing terms: "học riêng"/"học
  chung" (separate/mainstream schooling — blocked `ie032`'s FTS match to a confirmed-relevant chunk),
  "chữa dứt điểm" (cure completely — `ie013`), "khiếm thính" (hearing-impaired — `ie029`), a broader
  phrasing of "kén ăn" that covers "ăn ít rau củ quả" (`ie027`).
- **How**: add the missing entries to both glossaries (or merge them into one shared file both modules
  import), each mapped to the corpus-confirmed English terms this task already identified via direct
  `content ILIKE` checks.
- **Risk**: low — this is additive vocabulary, same risk profile as every prior glossary edit in
  T5.1–T5.3. The main risk is scope creep (adding terms not actually grounded in a confirmed corpus match).
- **Cost/dependency**: small, no external dependency.
- **Before/after evaluation**: re-run FTS diagnostics (`scripts/t5_5_fts_diagnostics.py`) on the same 31
  questions before/after; expect `ie027`/`ie032`/`ie013`/`ie029`'s FTS-B hit counts and classifications to
  improve measurably.
- **Rollback**: revert the glossary file(s) to their current committed version; no other state depends on
  the new entries.

### A3. Replace FTS's pure-AND/pure-OR modes with a minimum-concept-match threshold mode

- **Problem**: FTS-B's full-AND construction returns 0 results whenever a question combines more than
  ~2 glossary concepts (`ie004`, `ie012`, `ie013`, `ie029` all returned 0 in this task). FTS-C's full-OR
  construction is swamped by generic, high-document-frequency terms (the same two chunks dominate 14/31
  questions' top results). This exact next-step was already identified, but not built, in the T2.4
  report's condition C4 ("mọi biến thể mới... phải là thí nghiệm riêng... sau khi có nhãn mù").
- **How**: add a 4th FTS profile requiring at least `min(2, len(concepts))` concepts to match (OR-of-ANDs
  over concept subsets, or a rank bonus proportional to the number of distinct concepts matched) — the
  IDF-weighting idea the T2.4 report itself names as the candidate next experiment.
- **Risk**: a new ranking heuristic needs its own validation before being trusted; without the human
  annotation this task could not obtain (see A4), "better" is still only measurable qualitatively, same
  caveat as this entire task's own findings.
- **Cost/dependency**: small-to-moderate (new query-construction function + SQL, following the existing
  `fts.py` pattern); no external dependency.
- **Before/after evaluation**: compare top-10 hit classifications (direct/indirect/generic/none, same
  method as `t5_5_retrieval_diagnostics.md`) on the 31 independent questions and the original 66 frozen
  set, before/after.
- **Rollback**: a new profile code in `config/fts_profiles.json`; the existing A/B/C profiles are
  untouched, so rollback is simply not selecting the new profile.

### A4. Complete human annotation of the existing frozen FTS candidate pool

- **Problem**: the 2,791-pair blind candidate pool from T2.4 (`eval/reports/fts_candidate_pool_2026-11-
  15.jsonl`) has been `PENDING ANNOTATION` with 0 human labels since 2026-11-15, carried forward
  unchanged through every subsequent task (confirmed in this project's own memory record). Every FTS-vs-
  dense comparison to date, including this task's, is only exploratory as a direct result.
- **How**: assign 1 (ideally 2, for weighted-kappa inter-rater agreement) human annotators to grade the
  2,791 blind pairs on the existing 3/2/1/0/−1 scale defined in the T2.4 report. No code or pipeline
  change needed — the blind export file already exists and is ready to annotate.
- **Risk**: annotator time/availability, not a technical risk; single-annotator labels (if only 1 person
  is available) must be disclosed as such, same as the existing dense-retrieval benchmark's
  "silver_single_annotator (0 human-verified)" label tier.
- **Cost/dependency**: human labor only; no Cohere/LLM/external service; this is why it is Level A, not B.
- **Before/after evaluation**: once labeled, every exploratory metric in T2.4's report and this task's
  Phase 2 can be recomputed as a real, defensible Recall@K/nDCG comparison.
- **Rollback**: not applicable — annotation is additive data, never a destructive change.

---

## Level B — needs corpus/pipeline change, needs evaluation and approval

### B1. Database migration: install `unaccent`, reweight `ts_rank_cd`'s heading/content weights, and/or
restructure the view so the GIN index is actually used

- **Problem**: the `fts_architecture_audit_2026-11-15.md` audit (re-confirmed unchanged this task) found
  the `content_tsv` GIN index is bypassed because the `security_barrier` view runs the `@@` filter after
  its own joins; `unaccent`/`pg_trgm` extensions are available but not installed; heading is weighted
  lower (`B`=0.4) than content (`A`=1.0), backwards from the usual convention.
- **How**: a dedicated migration proposal (schema change), exactly as condition C5 of the T2.4 report
  already specifies: `CREATE EXTENSION unaccent`, a reweighted `setweight()` definition for a new
  generated column (never mutating the existing `content_tsv` in place), and/or a view restructuring that
  preserves the C5 authorization/eligibility filters while allowing the index to be used.
- **Risk**: schema changes are inherently higher-risk than application code; must not touch the 2,338
  document embedding vectors or any authorization/eligibility filter; needs its own backup/rollback plan
  per this project's standing protected-boundary rules.
- **Cost/dependency**: a DBA-level migration task, with its own review cycle; no external API dependency.
- **Before/after evaluation**: re-run the full T2.4 FTS evaluation script (`scripts/fts_eval_t2_4.py
  --check`) before and after, confirming authorization/reproducibility invariants still hold, plus the
  qualitative diagnostics from this task on the Vietnamese-text-matching improvement from `unaccent`.
- **Rollback**: a reversible migration (`DROP EXTENSION`/revert the generated column) with a pre-migration
  backup, per this project's standard migration discipline (see migrations 001/002/007 in this codebase).

### B2. Source new or expanded corpus content for the confirmed thin/absent topics

- **Problem**: Phase 3 found genuinely thin or absent coverage for: speech/language delay as its own topic
  (1 chunk corpus-wide), adult-life outcomes (marriage/parenting, 0 matches), adolescent sex education (0
  matches), ASD-vs-hearing-impairment differential diagnosis (0 substantive matches), and the specific
  vitamin-B6-cure myth (0 substantive matches).
- **How**: identify, license-review, and chunk new source documents addressing these topics specifically
  — the same process this project's corpus went through originally (T1/T2.0's license audit and chunking
  pipeline), not a shortcut.
- **Risk**: licensing risk (every existing source went through an explicit license audit —
  `eval/reports/license_audit_2026-11-14.md` — before inclusion; new sources need the same review);
  quality/authority risk (not every source is as authoritative as CDC/NIH/peer-reviewed-journal content
  already in the corpus).
- **Cost/dependency**: content-sourcing and review effort; **embedding the new chunks requires a Cohere
  document-embedding call**, which is a different authorization track than T2.6's query-embedding
  authorization but still needs its own explicit approval before any API call is made — flagged here, not
  assumed to be free.
- **Before/after evaluation**: re-run this task's corpus-coverage keyword sweep and the FTS diagnostics on
  the specific confirmed-gap questions (`ie017`, `ie018`, `ie024`, `ie026`, `ie029`) after any new content
  is added, before deciding whether a new template is warranted.
- **Rollback**: new source documents and their chunks/vectors can be excluded from the authorized
  allowlist (the same mechanism already used for D-1 exclusions in this project) without touching
  existing content.

---

## Level C — needs Cohere, LLM, or another external service

### C1. Re-authorize live query embedding (revisit T2.6) so dense retrieval can run on any new text

- **Problem**: this task's single largest, most consistent finding is that the dominant cause of both the
  105-set's 50 cache misses and the independent set's 31 cache misses is **exact-text cache keying**, not
  missing corpus knowledge (11/31 independent-set cache misses have demonstrable, specific corpus content
  per Phase 1's category 3) and not retrieval-quality (dense retrieval's own cached-cohort performance is
  good, per T2.3). Enabling live query embedding would directly address the dominant cause.
- **How**: not decided by this task — T2.6 remains `APPROVAL_REQUIRED` and this task does not propose,
  recommend, or lobby for a specific authorization decision; it only states that this is the change that
  would most directly address the finding.
- **Risk**: whatever risk T2.6's original review already identified (data sent externally, cost,
  licensing of query text sent to a third party) — unchanged by this task, not re-litigated here.
- **Cost/dependency**: Cohere API cost per query, ongoing; the explicit approval this project has
  deliberately withheld pending a separate decision.
- **Before/after evaluation**: re-run the 31-question independent set and measure the cache-miss rate
  directly; expect most of the 11 category-3 cases (and plausibly several of the 9 category-2 cases) to
  resolve to a real retrieval attempt.
- **Rollback**: the existing `ENABLE_LIVE_QUERY_EMBEDDING` flag already exists specifically for this —
  flipping it back to `False` is the rollback, already built and already tested (`test_demo_config_gates.py`).

### C2. Embed newly-sourced corpus content (if B2 is approved)

- **Problem/How/Risk/Cost/Evaluation/Rollback**: identical reasoning to C1 but for document embedding
  instead of query embedding — listed separately because it is a distinct authorization decision (adding
  new vectors to the corpus) from query-time embedding, even though both ultimately call the same Cohere
  API. Not evaluated further here since it is conditional on B2 being approved first.
