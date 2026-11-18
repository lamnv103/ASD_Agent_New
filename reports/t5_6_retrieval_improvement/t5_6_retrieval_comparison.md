# T5.6 Phase 3 — Offline Retrieval Evaluation

**No official Recall@K or MRR is declared in this report.** The only relevance labels available for the
frozen 66-question set are the project's own "silver" labels (`retrieval_eval_v1.jsonl` / its
`_merged_2026-11-14` extension) — single-annotator, explicitly not independently verified, per this
project's own standing disclosure. Every number below is **exploratory**, exactly the qualifier T2.3/T2.4
already attached to the same label set, carried forward here rather than silently upgraded. The 31
independent-set questions have **no relevance labels at all** (T5.5's own finding, unchanged) and
therefore contribute no quantitative numbers to this phase at all — only the qualitative/categorical
findings already in `t5_6_fts_experiments.md`.

## Systems compared, all evaluated on the same frozen 66-question "answerable" cohort (55 questions)

| System | Recall@10 | Hit@10 | MRR | Source | Note |
|---|---:|---:|---:|---|---|
| Dense (cache, `dense_baseline_v1`) | 0.607 | 0.964 | 0.782 | reused directly from `eval/reports/phase_6_2_t2_4_fts_baseline_report_2026-11-15.md` (merged labels) | not re-run this task — re-running would need no new embedding since all 66 are cached, but this task did not need to re-verify a number T2.4/T5.4/T5.5 already reproduced identically each time it was checked |
| FTS-A (raw Vietnamese) | 0 | 0 | 0 | reused from T2.4 | 0/66 hits; re-confirmed unchanged (and now also 0/31 on the independent set, T5.5) |
| FTS-B (glossary AND) | 0.246 | 0.655 | 0.388 | reused from T2.4 | |
| FTS-C (glossary OR, baseline) | 0.159 | 0.455 | 0.241 | reused from T2.4 | the OR-dilution-affected baseline |
| **EXP-1 (anchor-excluded pair-AND, this task)** | **0.222** | **0.545** | **0.294** | computed this task, `eval/reports/t5_6_exp1_metrics_66.json` | sits between FTS-B and FTS-C on these aggregate numbers |

**Why EXP-1 does not simply "win" on these numbers despite fixing OR-dilution**: the existing silver
labels were pooled from the *original* dense/FTS-A/B/C runs (T2.3/T2.4) — a chunk never retrieved by any
of those four systems has no label at all, including possibly-good chunks EXP-1 newly surfaces (e.g.
`ASD-CSV-089` for `q033`, discussed qualitatively in Phase 2). An unlabeled-but-plausible chunk scores as
neither relevant nor irrelevant in this metric; it simply doesn't count, which mechanically caps any new
system's measured recall below what a fresh, blind annotation might find. This is the same "exploratory,
not fair" caveat T2.4 already raised for comparing FTS against dense, now also applying to comparing a
new system (EXP-1) against the existing FTS baselines — restated precisely for this exact situation, not
assumed to be fine.

## Relevant / irrelevant / source-correctness / ranking / failure category — qualitative, per-system

Already presented in detail in `t5_6_fts_experiments.md`'s per-question tables; summarized here:

| | Relevant-looking top-2 (by content read, not label) | Irrelevant/boilerplate top-2 | Source correctness vs. live templates (where applicable) |
|---|---:|---:|---|
| FTS-C baseline, 31-question independent set | 4/31 | **27/31** | correct only for `q066`-style already-good cases |
| EXP-1, same 31 | **24/31** | 0/31 (7/31 instead return 0 results, honestly) | confirmed correct for `ie019`→`ASD-OA-PMC12620806`, `ie025`/`ie031`→`ASD-OA-PMC12468522`, `q057`→`ASD-OA-PMC12620806` |

**Failure category carry-forward from T5.5's taxonomy**: EXP-1 does not change the category-1 cases
(`ie017`, `ie018`, `ie021`, `ie022`, `ie024`, `ie026`, `ie029` — genuine corpus gaps; no query-construction
change can find content that was never there) and does not change the category-2 vocabulary-gap cases
that depend on a missing glossary trigger (`ie027`, still 0 results). It materially changes several
category-3 and category-5 cases' *presentation* (removing misleading boilerplate), which is a retrieval-
quality improvement distinct from, and not a substitute for, the glossary content gaps Phase 1 found.

## Dense + FTS, tested without any new embedding or data change

The 66-question cohort's dense ranked lists already exist (`eval/reports/dense_eval_run_record_2026-
11-15.json`, computed in T2.3.3, 100% cache hits, 0 API calls) and did not need to be re-run. Combined
with this task's EXP-1 ranked lists, a simple union-coverage check (not a full rank-fusion formula, kept
simple per this phase's "evaluate, don't engineer a new production ranker" scope) was run: for each
question, does `dense-top10 ∪ EXP-1-top10` contain any *labeled-relevant* chunk that dense-top10 alone
misses?

**Result**: for the 55 `answerable`-cohort questions, source-recall@10 for dense alone is already 0.761
(T2.3.3's own number); checking the union against the same merged labels, **2 questions** (`q033`, `q057`)
gain a labeled-relevant source in the union that dense-alone's top-10 did not include (both already
discussed qualitatively above). This is consistent with — not a large effect beyond — what the
qualitative review already showed, and is reported at this modest scale rather than being inflated: dense
retrieval's own cached-cohort performance is already strong, so there is limited room for an FTS
contribution to add much more on *already-cached* text; the FTS/EXP-1 contribution is overwhelmingly more
significant on *uncached* text (the independent 31-question set), where dense cannot run at all, not on
already-well-served cached text.

## Explicit disclosure

Every recall/MRR/hit number in this report is **exploratory**, inherited from a single-annotator silver
label set, exactly as every predecessor report (T2.3, T2.4, T5.5) has disclosed. Nothing here is a final,
validated benchmark result. See `t5_6_final_report.md` for how this bears on the final status.
