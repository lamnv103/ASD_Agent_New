# T6.1 Phase 6 - Error analysis status

**Human relevance root-cause analysis: pending labels.** Without judgments, a retriever's candidate cannot be called relevant/false positive, and an absent result cannot be called a relevance false negative. The current analysis classifies only observable retrieval behavior.

## Observable failure/candidate patterns

- **FTS-A query coverage failure:** no results on all 66 core queries under raw Vietnamese `plain_and` with the English `content_tsv` configuration. This is an observed configuration/query-processing limitation; it does not establish that every raw Vietnamese query fails.
- **FTS-B no-result:** 11 queries (q004, q007, q034, q050-q052, q058-q062); FTS-C no-result: q062; isolated T5.7 harness no-result: q007, q034, q058, q059, q062. These are observed retrieval coverage outcomes; relevant evidence could still be absent/present in the corpus.
- **Different candidate sets:** Dense/FTS overlap is modest (from T6.0); RRF adds non-Dense Top-10 candidates for 52 FTS-B, 65 FTS-C, and 57 isolated-harness queries. Whether additions improve or degrade support is UNKNOWN until blind human review.
- **Out-of-scope behavior:** q062 receives no FTS result but Dense has candidates. This is an observed candidate behavior, not a validated out-of-scope detector.
- **Accent variations:** only six query concepts were tested with exact and stripped-diacritic variants. Dense has no corresponding cached vectors. No broad language robustness claim is warranted.

## Root-cause classification (provisional)

| Class | Evidence / status |
|---|---|
| Query processing / language mismatch | FTS-A raw Vietnamese + English text-search config; strongly plausible mechanism, but no lexical relevance adjudication. |
| Glossary coverage/expansion | FTS-B/C increase candidate coverage; possible missed concepts/overexpansion, **unknown** which is harmful/helpful. |
| Retriever/ranking | Candidate rank/order varies across systems; relevance impact **unknown**. |
| Corpus coverage | Cannot distinguish corpus absence from retrieval miss without exhaustive human search; **unknown**. |
| Metadata/filtering | No missing IDs or content-hash mismatch in candidate pool extraction; this does not prove all view filters are correct beyond observed authorization. |
| Annotation uncertainty | No submissions yet; **pending**. |

After adjudication, unblind the provenance map and assign error categories only where the judgments support them. Review high-risk, medication, contradictory-source, multi-aspect, and out-of-scope query discrepancies separately. Do not change T5.10 safety behavior in this task.
