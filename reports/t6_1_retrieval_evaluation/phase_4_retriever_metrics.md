# T6.1 Phase 4 - Retriever metrics

**Official relevance metrics: BLOCKED pending human-adjudicated judgments.** No Recall@K, Precision@K, MRR, or nDCG value was computed. Existing benchmark judgments were not read or used by the T6.1 construction/evaluation script; AI/silver labels are not substituted for new independent human judgments.

Once human judgments are validated, compute each system on the same 66 core queries and pooled candidate universe:

- **Recall@K:** number of judged relevant candidates in system Top-K divided by the judged relevant candidate count for that query. Because the pool is incomplete, report as pooled recall and state that unpooled corpus candidates are unknown.
- **Precision@K:** relevant items in Top-K divided by K; report returned-count-adjusted precision separately when fewer than K results exist, and clearly specify which convention is used.
- **MRR:** mean reciprocal rank of the first relevant item; report how queries with no judged relevant pooled item are handled, separately from true no-result and unanswerable queries.
- **nDCG@K:** graded DCG using gain `2^grade - 1` and logarithmic rank discount, normalized by ideal DCG from judged pool items. Unjudged items are not treated as 0 unless the protocol explicitly and justifiably adopts that assumption; here they remain unjudged.

Separate query with no returned candidates, returned candidates but no judged relevant item, relevant item ranked below K, and no relevant evidence found in corpus after human assessment. Report query-level and topic/risk breakdowns, paired uncertainty, and denominator counts. Do not claim the last category from pooled labels alone without an exhaustive search/adjudication protocol.

**Current measurable quantities only:** query coverage and candidate-pool sizes are in Phase 2; candidate-set overlap and RRF ordering changes are unsupervised diagnostics in Phase 5. These are not relevance metrics. The historical T2.3 66/66 Top-20 equality remains a separate retrieval regression.
