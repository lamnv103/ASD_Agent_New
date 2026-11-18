# T6.0 Phase 0 ? Workspace and authorization audit

**Evidence status:** VERIFIED unless marked otherwise. Read-only audit; no application, corpus, evaluation, database, or frozen artifact was changed. No secrets were printed.

## Environment and scope

- **VERIFIED:** The workspace is `D:\AI4LIFE\ASD_AGENT_FINALL`. This path has no `.git` directory; Git branch and worktree status are therefore **UNKNOWN**. No Git initialization, commit, or push was attempted.
- **VERIFIED:** The audit wrote its artifacts only under `reports/t6_0_hybrid_readiness/`. The comparison artifact is [`phase_3_retrieval_comparison.csv`](phase_3_retrieval_comparison.csv).
- **VERIFIED:** The live query embedding, reranking, and LLM flags in the inspected app configuration are disabled. No Cohere/LLM request was made.
- **VERIFIED:** T2.6 authorization remains `APPROVAL_REQUIRED` for sending arbitrary demo-user query text to Cohere. The cache-only path is available for the existing evaluation set; a miss must fail closed.
- **VERIFIED:** Comparative database retrieval used the research reader and the allowlisted `asd_rag.v_research_retrieval_chunks` view in read-only sessions. No database writes or permission changes were performed.
- **VERIFIED:** No T2.4-C reveal/coordinator file was opened. No production database, corpus source, frozen benchmark, or stored document embedding was edited.

## Authorization boundary

| Activity | T6.0 outcome |
|---|---|
| Read-only Dense/FTS candidate retrieval through authorized research view | Performed for audit |
| Reuse cached vectors for the 66 existing benchmark questions | Performed; no external calls |
| Embed arbitrary/new query text with Cohere | Not authorized; not performed |
| Write database, alter permissions/index/schema, change source corpus | Not performed; outside scope |
| Change retrieval algorithm or promote a profile | Not performed |

## Provenance and limitations

The live database observation is a snapshot: PostgreSQL 16.15, database `asd_rag_v2`, current user matched the configured research reader, and the authorized view exposed 2,291 distinct chunks for `cohere_embed_v4_1536_v1` (2,291 rows). This is not a claim about base-table totals. A previously recorded 2,338 embedding count does not reconcile through the authorized view; this audit did not inspect protected/base tables to explain the difference.

The configured dense profile is Cohere `embed-v4.0`, 1536 dimensions, document task `search_document`, query task `search_query`, cosine distance, default K=10/max K=50. Local cached query vectors exist for the 66 benchmark question texts. Existing code continues to enforce the research role, fixed authorized view, profile filter, bound K/vector, and read-only transaction.

**Conclusion:** the permitted research-only comparative audit path was available. General live-query embedding remains blocked pending explicit authorization. This report does not authorize T6.1 implementation or broader data access.
