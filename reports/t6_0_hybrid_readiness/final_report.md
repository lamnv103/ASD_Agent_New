# T6.0 ? Hybrid Retrieval Readiness Audit & Design

**Final status: `READY_WITH_CONDITIONS`**

## Executive finding

The existing Dense and isolated PostgreSQL FTS implementations are technically available for a **read-only, offline T6.1 research comparison** on the current authorized view. The audit retrieved candidates for the 66 fixed benchmark queries (Dense from cache, FTS directly) and recorded results in [`phase_3_retrieval_comparison.csv`](phase_3_retrieval_comparison.csv). Dense baseline regression evidence remains 66/66 identical to the recorded T2.3 Top-20 baseline.

This is not evidence that Hybrid improves relevance or safety: there is no independent adjudicated gold set, and the FTS glossary was developed using the same 66-query vocabulary. Arbitrary new Dense queries remain blocked because live Cohere query embedding is `APPROVAL_REQUIRED`. FTS evidence is not currently represented in a way that can safely satisfy the Dense/cosine-oriented Evidence Gate. Therefore this is **not ready for user-facing integration, answer generation, clinical use, or performance claims**.

## Evidence summary

- **VERIFIED:** Research reader authenticated and accessed the authorized view read-only. The observed view had 2,291 rows and distinct chunk IDs for the target 1536-dimensional Cohere profile. The count discrepancy with a previously cited 2,338 embedding total was not reconciled because base tables were outside this audit boundary.
- **OBSERVED:** Dense Top-10 returned 660 candidates across 66/66 queries. FTS-A returned zero; FTS-B returned results for 55/66; FTS-C for 65/66; isolated T5.7 EXP-1c-style harness for 61/66. Twelve extra FTS accent variants are included in CSV totals, not in those 66-query counts.
- **OBSERVED:** candidate sets differ. Intersections with Dense among successful FTS queries were modest (B 114 chunk overlaps / 55 queries, C 67 / 65, isolated harness 107 / 61). These are set overlaps, not relevance metrics.
- **VERIFIED:** No external embedding request, DB write, permission change, production query, corpus edit, frozen benchmark edit, T2.4-C edit, or app/retrieval implementation change occurred.
- **UNKNOWN:** Whether fusion improves retrieval or final answer evidence quality. No human-adjudicated labels support that inference.

## Conditions for T6.1

1. Keep T6.1 isolated, read-only, and research-only; use cached Dense vectors for the known benchmark only until separate Cohere authorization is granted.
2. Pre-register the comparison matrix and metrics. Preserve T2.3 regression as a separate check.
3. Prepare a held-out query set and independently blinded/adjudicated relevance judgments; do not tune and validate on the glossary's development vocabulary.
4. Define FTS evidence provenance for the Evidence Gate without fabricated cosine similarity, metadata, or citations; validate it against false accepts/rejects before any integration.
5. Keep safety and out-of-scope review separate from retrieval ranking metrics, and retain authorization, failure, and reproducibility checks.

## Report index

- [Phase 0 ? Workspace and authorization audit](phase_0_workspace_audit.md)
- [Phase 1 ? Dense audit](phase_1_dense_audit.md)
- [Phase 2 ? FTS audit](phase_2_fts_audit.md)
- [Phase 3 ? Comparative analysis](phase_3_comparative_analysis.md)
- [Phase 4 ? Hybrid architecture proposal](phase_4_hybrid_architecture.md)
- [Phase 5 ? Top-K and evidence design](phase_5_topk_evidence_design.md)
- [Phase 6 ? Evaluation plan](phase_6_evaluation_plan.md)

## Scope and status boundary

`READY_WITH_CONDITIONS` means only that a bounded T6.1 offline research comparison can proceed within the constraints above. It does not authorize arbitrary query embedding, live app/API changes, database schema/index changes, production use, answer generation, or a clinical claim. No tests were executed because T6.0 was an audit/design task with no code modifications; test results remain unreported, not passed.
