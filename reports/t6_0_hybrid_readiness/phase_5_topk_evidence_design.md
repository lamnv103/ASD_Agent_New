# T6.0 Phase 5 ? Top-K and evidence-set design

**Status:** design recommendation only; no K defaults, profiles, thresholds, or Evidence Gate behavior changed.

## Separate candidate retrieval from evidence selection

Keep the current Dense Top-10 and FTS Top-10 as the baseline. In T6.1, compare candidate K values from the existing supported range (10, 20, 50) for each retriever, and fused output K values 5, 10, 20. Use a small prespecified matrix rather than selecting K after looking at favorable examples. The database FTS/Dense profile caps K at 50. Record retrieval latency and result count at each setting.

Candidate Top-K is not the same as the final evidence set. Any future answer pipeline should have a distinct, auditable evidence-selection stage that checks direct support, query aspect coverage, source diversity where useful, metadata completeness, and authorization/provenance. It must not assume the top-ranked K chunks are sufficient, nor increase K to mask poor ranking.

## Fusion and score handling

- Preserve each retriever's own rank and score type.
- Prefer RRF as the first rank-only fusion experiment; vary a small prespecified constant set, for example `c ? {20, 60, 100}`.
- Keep source/chunk deduplication deterministic and preserve all contributing ranks.
- Do not directly blend `1 - cosine_distance` with `ts_rank_cd`; their scales and meanings differ.
- Do not set universal cutoffs from current observations. No relevance-calibrated threshold exists.

## Evidence Gate compatibility

The live Evidence Gate is built around existing Dense/cosine-style evidence and lexical/topic checks. FTS score is not a probability and does not establish support. No synthetic similarity, placeholder URL/hash, inferred quote, or fabricated match-term evidence may be inserted to satisfy the existing contract. A future typed adapter should include exact matched terms/phrases when available, retriever profile/rank, actual chunk text and hash, source citation metadata, and authorization provenance; then be independently tested for false accepts and false rejects before integration.

## Safety and scope

Keep medication safety and B8 behavior untouched. Increased candidate K can increase exposure to weak, contradictory, or off-topic chunks; test high-risk and out-of-scope questions with explicit review. Retrieval relevance is not medical validation. No retrieval result should be described as a diagnosis, dosage recommendation, or clinical confidence.
