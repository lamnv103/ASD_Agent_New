# T6.0 Phase 6 ? Evaluation plan and gates

## Evaluation protocol for T6.1

1. Freeze the candidate profiles, query set, K/fusion matrix, metrics, and failure handling before running. Keep current T2.3 66/66 retrieval regression separately identified and unchanged.
2. Use query-level splits. The existing glossary was authored from the 66-question vocabulary, so these questions are development evidence. Create a genuinely held-out query set with new paraphrases, accentless text, colloquial/technical forms, multi-intent and multi-source questions, age-specific terms, medication/safety topics, and out-of-scope controls. Do not tune the glossary or fusion on the held-out set.
3. Obtain independent human relevance judgments for each query/chunk pair using a documented rubric, blinded to retriever/profile/rank/score. Adjudicate disagreements and keep reviewer provenance. No expert-reviewed gold labels are currently established by this audit.
4. Report Recall@5/10/20, MRR@10, nDCG@10 (graded judgments where appropriate), no-result rate, per-category/per-risk breakdowns, source diversity, duplicate/provenance errors, and latency. Include confidence intervals or query-level paired uncertainty for comparisons. Treat out-of-scope detection and high-risk safety behavior as separate gates, not aggregate retrieval metrics.
5. Compare Dense, FTS-A/B/C, candidate union, and rank fusion on the identical queries and authorized corpus snapshot. Retain raw outputs and deterministic run metadata. Report partial runs as partial; never count missing, unauthorized, or unexecuted cases as passing.
6. Do a failure analysis for false negatives, boilerplate/lexical false positives, query expansion misses, acronym ambiguity, accent variation, age mismatch, multi-aspect coverage, conflicting sources, and medication-related candidates. Review every high-risk discrepancy.

## Coverage and known test-set limitation

The current 66 queries cover these categories: basic knowledge (6), signs/symptoms (7), social communication (5), AAC (2), restricted/repetitive behavior (5), assessment/diagnosis (9), intervention/support (10), sensory (5), development milestones (6), multi-aspect (4), multi-source (1), and insufficient/out-of-scope (6). Style tags include colloquial (20), multi-chunk (61), multi-source (54), short (14), synonym (4), age-specific (7), false-positive risk (7), technical (13), long (7), and conflicting (4). Tags can overlap. All 66 texts contain Vietnamese diacritics; only six received the limited FTS accent-variant probe. Coverage counts do not establish representativeness.

The FTS glossary itself documents development from the same 66 questions; no official independent adjudication or held-out generalization result is evidenced. Thus the current analysis can describe candidate behavior, not estimate retrieval accuracy.

## Readiness gates

Before any user-facing Hybrid integration: (a) receive explicit data-processing authorization for arbitrary query embedding or keep Dense restricted to cache-only; (b) define and test typed FTS evidence/provenance compatibility with the Evidence Gate; (c) obtain held-out blinded human judgments and adjudication; (d) pass existing safety, out-of-scope, source citation, authorization and regression suites; (e) establish operational failure/degraded-mode policy; (f) separately approve any schema/index/production changes. T6.0 ran no application test suites because it made no code changes; no unexecuted suite is reported as passed.
