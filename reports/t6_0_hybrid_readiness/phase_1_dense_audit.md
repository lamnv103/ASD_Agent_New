# T6.0 Phase 1 ? Dense retrieval audit

**Status:** VERIFIED for the existing baseline and audit run; no dense implementation changes made.

## Existing path

`app/retrieval/dense.py` validates query text and K, uses the configured query embedder, validates the vector, calls `ResearchVectorReader`, validates result provenance and content hashes, and reports `1 - cosine_distance` as a similarity ranking signal. `app/retrieval/research_reader.py` constructs SQL only for `asd_rag.v_research_retrieval_chunks`, filters the selected embedding profile, sorts by cosine distance then `chunk_id`, and binds the vector/profile/K. It asserts the research reader role and opens a read-only session. View-side authorization and eligibility filters apply before `LIMIT`.

The stored document vectors and query vectors share the configured Cohere `embed-v4.0` profile, 1536 dimensions, with document input type `search_document` and query input type `search_query`. **Matching dimension alone would not establish cross-model compatibility;** this compatibility is profile/provenance-specific.

## Reproduction evidence

- The 66 question texts in `eval/datasets/retrieval_eval_v1.jsonl` all had a cache hit for the configured dense query profile. Audit retrieval made zero external embedding calls.
- Dense Top-10 returned 10 rows for each of the 66 benchmark queries: 660 result rows, no empty result sets. These rows and observed per-query latency are in the phase 3 CSV.
- Existing T2.3 regression evidence reports Top-20 IDs identical for 66/66 queries. T6.0 did not modify that artifact or labels.
- Live database snapshot: the research view exposed 2,291 rows/unique chunk IDs for the target embedding profile. The audit used only that view; it did not query base tables.

## Boundaries and limitations

- **BLOCKED:** Arbitrary new query text cannot be embedded through the current cache-only configuration. No new text was sent to Cohere. A cache hit is not evidence that arbitrary demo queries work.
- No standalone retrieval relevance metric is claimed. Existing judgments are not an independent, human-adjudicated gold set suitable for selecting a Hybrid strategy.
- Dense Top-10 is a baseline candidate list, not a complete or medically validated evidence set. Similarity is not probability or confidence.
- The current dense implementation is unchanged. T6.0 is design/audit only and does not integrate FTS or reranking into the app/API.

**Design implication:** preserve the existing Dense path as the comparison baseline. Any future fusion should retain its raw rank, distance, similarity, chunk identity, source metadata, and authorization provenance.
