# T6.1 Phase 2 - Candidate pool construction

## Construction

Candidate union was formed per original query from the existing Dense, FTS-A/B/C, and isolated T5.7 EXP-1c-style result lists, using stable `chunk_id` for deduplication. All original retriever ranks and raw typed scores are preserved in evaluator-only [`candidate_pool_provenance_map.json`](candidate_pool_provenance_map.json); the map is not annotator-facing. No source was omitted on score thresholds. Empty results remain represented in the source comparison CSV even though they contribute no chunk to the pool.

| Pool | Queries | Query-chunk pairs after deduplication | Unique chunks |
|---|---:|---:|---:|
| Core 66-query pool | 66 | 1,631 | 906 |
| 12 accent/no-diacritic diagnostic variants | 12 | 230 | 103* |

*Variant unique chunk count is separate from the core pool; chunk IDs can overlap the core pool. Each pool row's content and SHA-256 were retrieved/validated against the authorized research view; 906 unique IDs fetched for the combined pools and zero IDs were missing. Every chunk hash matched its content.

The two core annotator sheets each contain the same 1,631 query-chunk pairs; the two variant sheets each contain the same 230 variant pairs. Query order and within-query chunk order are deterministically randomized with different seeds for the two annotators. The core pool has 24.71 deduplicated candidate pairs per query on average. Query coverage is 66/66 because Dense has candidates for each core query.

## Blindness and files

Annotator sheets omit retriever names, ranks, raw scores, latencies, tsquery, and selection stratum. They retain query ID, query text, chunk ID, source ID/title/location, content, and hash. Distribute only the intended individual sheet and instructions; do not distribute the evaluator provenance map or T6.0 CSV. Candidate content must not be edited.

- [`human_annotation_sheet_annotator_1_core.csv`](human_annotation_sheet_annotator_1_core.csv)
- [`human_annotation_sheet_annotator_2_core.csv`](human_annotation_sheet_annotator_2_core.csv)
- [`human_annotation_sheet_annotator_1_diacritic_variants.csv`](human_annotation_sheet_annotator_1_diacritic_variants.csv)
- [`human_annotation_sheet_annotator_2_diacritic_variants.csv`](human_annotation_sheet_annotator_2_diacritic_variants.csv)
- [`human_annotation_pool_core.csv`](human_annotation_pool_core.csv) and [`human_annotation_pool_diacritic_variants.csv`](human_annotation_pool_diacritic_variants.csv) are master templates; use the per-annotator sheets to maintain independence.

## Pooling limitation

This is pooled evaluation over candidates retrieved by the listed systems at K=10, not an exhaustive corpus judgment. A chunk absent from the pool is **unjudged**, not grade 0 or irrelevant. Recall relative to the pool can overstate corpus recall, and unique relevant evidence outside all pools will be missed. The 12 variants are diagnostic and not part of the core denominator; no Dense retrieval is available for these variants without a new vector, and no external embedding was called.

