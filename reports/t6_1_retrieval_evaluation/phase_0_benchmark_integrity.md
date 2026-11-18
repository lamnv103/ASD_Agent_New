# T6.1 Phase 0 - Benchmark integrity and provenance

**Outcome: PASS for artifact integrity/eligibility to construct a blinded candidate pool; relevance evaluation remains pending.**

## Inputs and hashes

The exact SHA-256 values for the core benchmark, T6.0 reports and comparison artifact, retrieval/embedding/FTS profiles, glossary, and inspected retrieval modules are recorded in [`phase_0_input_sha256.json`](phase_0_input_sha256.json). Key hashes:

- `eval/datasets/retrieval_eval_v1.jsonl`: `7704bb510c9ab4a545d9195b18ffa2dc32f10b705df909a9201e11c96f104c2b`
- `reports/t6_0_hybrid_readiness/phase_3_retrieval_comparison.csv`: `9ad662d8d11548da06d45d630dbedd17b239cb2c8f9160457d38dd3c12383e75`
- T6.0 final report: `fe5b3a557d88538cb0aa2ffee05e48fc2a8a4ce1be8408a4006d1faab56fc00b`

**Git:** `git status --short` returned "not a git repository"; workspace has no `.git`. Branch and repository cleanliness cannot be established. No Git mutation was run.

## Input checks

- Frozen evaluation data has 66 core query IDs q001-q066. Each ID in the T6.0 result CSV has exact query text matching the benchmark's `question_vi` field (66/66). The comparison CSV contains 2,661 rows and columns for question ID/text/category, retriever/profile, candidate K, rank, chunk/source, typed raw score, latency, status, and FTS tsquery.
- The T6.0 CSV includes Dense 660 rows; FTS-A 78; FTS-B 546; FTS-C 767; isolated T5.7 harness 610. FTS profile totals include six exact/diacritic-stripped query pairs (12 variant IDs); these are kept separate from the 66 core queries. Dense was not run on variants because compatible cached vectors were unavailable.
- Original-core result coverage matches T6.0: Dense 66/66; FTS-A 0/66; FTS-B 55/66; FTS-C 65/66; T5.7 isolated harness 61/66. This describes returned candidates, not relevance.
- The Dense cache availability was 66/66 for the original exact texts. No new query vector was generated. No Cohere or LLM API was called.
- The profile definitions specify FTS-A raw Vietnamese `plain_and`, FTS-B bilingual glossary concept groups with AND across groups, FTS-C OR across groups, all using `english`, `ts_rank_cd`, K default 10/max 50. Dense uses cached `embed-v4.0` query vectors and cosine distance. These score types are not commensurate.
- T2.6 remains `APPROVAL_REQUIRED` for arbitrary query text to Cohere. The 2,338 embedding count from prior context cannot be reconciled from the authorized view; this run only used the permitted research reader/view and did not inspect base tables.

## Preservation

The frozen evaluation JSONL, T6.0 result CSV, configs, source modules, and database were read-only. The T6.1 script reads only `question_id` and `question_vi` from benchmark records for query text; no relevance grades, gold chunk lists, or annotation rationales were used to build candidate pools or fusion. T6.0 66/66 regression remains a separate historical retrieval check, not a relevance metric.

**Evidence:** [`build_t6_1_artifacts.py`](build_t6_1_artifacts.py) uses the research-reader connection and fixed authorized view for content; [`artifact_build_summary.json`](artifact_build_summary.json) records candidate counts and input hashes.
