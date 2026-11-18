# T6.1 Phase 5 - Offline Hybrid experiments

**Execution:** candidate union and rank-only RRF were run offline from the T6.0 Top-10 lists. No code/API integration, query embedding, database write, or score blending occurred. No relevance metric was computed.

## RRF setup and outputs

For each core query, RRF combined the Dense Top-10 with one FTS list at a time (FTS-A, FTS-B, FTS-C, or the isolated T5.7 harness). RRF used `sum(1/(c + rank))` with `c in {20, 60, 100}`; missing system rank contributes zero. Candidate ID ties break by `chunk_id`. Candidate union is the deduplicated set, with source lists/ranks retained in the provenance map. Weighted score fusion was deliberately not run because `cosine_distance` and `ts_rank_cd` are incommensurate and no calibration labels exist.

[`offline_rrf_top10.csv`](offline_rrf_top10.csv) contains 7,920 rows (66 queries x four sparse lists x three c values x Top-10). It retains FTS profile, RRF rank/score, Dense rank, FTS rank, and source ID. The T5.7 harness is experimental and is reported separately, not as a production FTS profile.

## Observed Top-10 changes (not quality gains)

| Dense + list | Queries whose Top-10 ordering differs from Dense | Queries adding at least one non-Dense-Top-10 candidate |
|---|---:|---:|
| FTS-A | 0/66 | 0/66 |
| FTS-B | 55/66 | 52/66 |
| FTS-C | 65/66 | 65/66 |
| T5.7 isolated harness | 61/66 | 57/66 |

For this candidate set, `c=20`, `60`, and `100` produced identical Top-10 lists for every query within each combination. This is a property of these observed lists/ranks, not evidence that c is generally irrelevant. FTS-A adds nothing because it returned no candidates in the core benchmark. No method is selected as best: changes/additions may be useful, irrelevant, or harmful until judged.

## Decision

Candidate union and RRF artifacts are suitable for blinded annotation and later evaluation. RRF output is not a relevance result. Do not tune c/K using these 66 questions after labels are examined and then report the same set as held-out validation. A separate held-out query set is needed for final method selection.
