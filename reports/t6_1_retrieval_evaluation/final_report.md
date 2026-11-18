# T6.1 - Offline Retrieval Evaluation & Human Relevance Assessment

## Final status: `READY_WITH_CONDITIONS`

**What is ready:** benchmark-preserving candidate pool, blinded human annotation materials, and offline Dense+FTS union/RRF lists are prepared for human review.

**What is not complete:** no human annotations were supplied. Official relevance metrics and a validated Dense-versus-FTS/Hybrid quality conclusion are therefore **blocked**. No claim is made that Hybrid improves relevance or that any retrieval strategy is best. T6.2 integration is **not ready**.

## Findings

1. **Integrity:** 66 core query IDs q001-q066; input query text matches T6.0 candidate CSV 66/66. The T6.0 2,661-row artifact separates core queries from 12 FTS-only accent variants. Git status could not be established because the workspace is not a Git repository. Input SHA-256 values are recorded in `phase_0_input_sha256.json`.
2. **Pool:** 1,631 deduplicated core query-chunk pairs, 906 unique chunks, 66/66 query coverage. Separate accent-variant pool: 230 pairs across 12 query variants. All candidate IDs were found in the authorized research view; all retrieved content SHA-256 hashes matched; no external query embeddings were generated.
3. **Blinding:** two independent core sheets and two separate variant sheets are prepared. They contain no retriever, rank, raw score, RRF score, or stratum. Grades/rationale/evidence/reviewer fields are empty and status is `PENDING_HUMAN_REVIEW`. Provenance mapping is evaluator-only and must not be shared with annotators.
4. **Fusion:** offline candidate union and 792 RRF query/config runs (`c=20,60,100`, Dense paired separately with each FTS list/harness) produced 7,920 Top-10 rows. RRF changed candidate ordering/additions but without labels this is not evidence of quality. Candidate K=10 is inherited from T6.0; no new Top-K optimum is inferred.
5. **Metrics:** Recall@K, Precision@K, MRR, nDCG@K, inter-annotator agreement, and adjudication are not computed. Existing AI/silver benchmark judgments were not used as replacement ground truth. The candidate pool is incomplete; absent candidates are unjudged, never grade 0 by default.
6. **Validation:** structural validator returned `PASS_STRUCTURAL_VALIDATION`: both annotator sheets have exact matching pair sets, empty labels/evidence/rationales, content hashes match, and all 792 RRF runs have ranks 1-10. This is artifact validation only; no human review or application test suite was run.
7. **Preservation:** no application code, source corpus, stored document vectors, DB schema/permissions/data, frozen benchmark, T2.6 boundary, T2.4-C artifacts, or reveal files were changed/accessed. Research view use was SELECT-only. No Cohere/LLM calls or Git mutations occurred.

## Answers to decision questions

- **Dense remains baseline?** Yes, for comparison: it is the existing 66/66 cache-backed baseline and separate T2.3 regression remains intact.
- **Does FTS add relevant candidates?** Unknown; it adds distinct candidates, but relevance is unjudged.
- **Does Hybrid improve recall without harming ranking?** Unknown; no human relevance labels.
- **Is RRF better than candidate union?** Unknown; RRF is prepared as a rank-only experiment, not evaluated against relevance.
- **Is weighted fusion justified?** No; score scales are incompatible and no calibration data exist.
- **Best K/topics with missing evidence?** Not determined. K=10 is the existing candidate source setting. Topic-level relevance gaps are pending annotation.
- **What is needed before T6.2?** Human double annotation, adjudication, held-out evaluation, relevance metrics, safety/out-of-scope error analysis, FTS evidence contract compatible with the Evidence Gate, and any needed authorization approvals.

## Required next steps

1. Appoint two qualified, independent annotators and run calibration on examples outside the benchmark.
2. Distribute only each person's assigned blinded core CSV and protocol; keep evaluator provenance map and T6.0 CSV private until both annotations are locked.
3. Receive completed sheets; validate IDs, grade/status, rationale, evidence spans, and reviewer metadata without modifying original submissions.
4. Compute agreement and adjudicate disagreements; publish disagreement/adjudication artifacts.
5. Unblind and calculate pooled relevance metrics with explicit denominators and query-level uncertainty; keep 12 accent variants separate.
6. Decide on T6.2 only after results, safety error analysis, and authorization review. Do not promote to production or clinical use based on this report.

## Artifact index

- [Phase 0 benchmark integrity](phase_0_benchmark_integrity.md)
- [Phase 1 annotation protocol](phase_1_annotation_protocol.md)
- [Phase 2 candidate pool](phase_2_candidate_pool.md)
- [Phase 3 annotation execution](phase_3_human_annotation_execution.md)
- [Phase 4 retriever metrics](phase_4_retriever_metrics.md)
- [Phase 5 hybrid experiments](phase_5_hybrid_experiments.md)
- [Phase 6 error analysis](phase_6_error_analysis.md)
- [Disagreement/adjudication status](phase_3_disagreement_and_adjudication.md)
- [Annotation sheets and evaluator artifacts](artifact_build_summary.json)
- [Structural validation result](artifact_validation_report.json)
- [Artifact builder](build_t6_1_artifacts.py) and [validator](validate_t6_1_artifacts.py)

`READY_WITH_CONDITIONS` means ready for blinded human relevance assessment and subsequent offline evaluation only. It does not mean human review is complete, the systems are validated, Hybrid is superior, or T6.2 is approved.
