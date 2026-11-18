# T6.0 Phase 3 ? Dense and FTS candidate comparison

**Status:** OBSERVED candidate behavior only. No relevance/accuracy conclusion is possible from this experiment.

## Method

The frozen 66-query file `eval/datasets/retrieval_eval_v1.jsonl` was read without modification. Dense used the existing cached Cohere `embed-v4.0` query vectors. FTS-A, FTS-B, FTS-C, and the isolated T5.7 EXP-1c-style harness queried the same authorized research view. Candidate K=10. No external embedding call, reranker, human labeling, or score calibration was used. An optional small accent robustness probe added exact/stripped-diacritic variants for q001, q025, q036, q038, q041, and q058 to FTS only.

Raw rows, IDs, rank, score type, latency, query and generated tsquery are recorded in [`phase_3_retrieval_comparison.csv`](phase_3_retrieval_comparison.csv). The CSV contains 2,661 rows: Dense 660; FTS-A 78; FTS-B 546; FTS-C 767; EXP-1c-style harness 610. Each FTS total includes 12 added probe query variants; empty queries have an explicit `no_results` row. The 66 original questions are distinguishable from the probe IDs.

## Coverage, overlap, and runtime observations

| Retriever | Original queries with ?1 result / 66 | Candidate rows | Median observed latency (ms) |
|---|---:|---:|---:|
| Dense baseline | 66 | 660 | 111.09 |
| FTS-A | 0 | 0 | 105.84 |
| FTS-B | 55 | 433 | 114.01 |
| FTS-C | 65 | 646 | 147.92 |
| T5.7 isolated EXP-1c-style harness | 61 | 503 | 127.80 |

For candidate-set comparison, each retriever's successful original-query Top-10 chunk-ID set was intersected with Dense Top-10. FTS-B had 114 overlapping chunk occurrences over its 55 successful queries (2.07/query); 12 successful-query lists had zero overlap. FTS-C had 67 overlaps over 65 successful queries (1.03/query); 28 had zero overlap. The isolated harness had 107 overlaps over 61 successful queries (1.75/query); 18 had zero overlap. These are **candidate overlap counts**, not Recall@K, precision, relevance, or agreement with truth. FTS-A returned no candidates, so overlap is undefined.

Latencies are single-run, local, observed wall measurements; they are not a controlled performance benchmark. FTS-A's low observed latency accompanies zero results and is not a useful quality/performance win.

## Qualitative examples (candidate identity only)

- q001 (ASD definition): Dense top result is an NIH-NIMH chunk; FTS-B/C top result is an ASD-OA boilerplate chunk; isolated EXP-1c-style top result is a CDC clinical chunk.
- q014 (AAC): Dense top result is WHO-CST; FTS-B and FTS-C top result IDs differ; the isolated harness returns a different ASD-CSV chunk.
- q036 (sleep): Dense returns a sleep-paper chunk; B and isolated harness return another chunk from the same sleep paper; C selects a different paper.
- q058 (risperidone dosage): Dense returns a sleep-paper chunk; B and isolated harness have no result; C returns an ASD-CSV chunk. This is a candidate discrepancy only and is not labeled relevant/irrelevant here.
- q062 (weather): Dense returns corpus candidates for an out-of-scope query while FTS profiles return none. No official out-of-scope judgment is inferred from retrieval alone.

See CSV for exact chunk IDs, ranks, scores, source metadata, and raw query text. Scores are not comparable: Dense's CSV score type is cosine distance (lower ranks better); FTS uses `ts_rank_cd` (higher ranks better). Do not add scores or interpret them as probabilities.

## Interpretation

The results support testing a union/fusion candidate stage in T6.1 because the systems retrieve different candidates and FTS contributes coverage for many questions. They do not show that Hybrid improves retrieval quality, safety, evidence sufficiency, or answer quality. The FTS glossary was developed against the same 66-question vocabulary, so these observations are development-set evidence and may be optimistic. A held-out, independently adjudicated relevance set is a prerequisite for selecting a winner or claiming gains.
