# Retrieval API Test Report — T2.5-DEV-3

**Conclusion: `QUERY_EMBEDDING_BLOCKED` for new uncached user queries.** The route and authorized database retrieval work for cached evaluation input, but no authorized encoder exists for new query text.

## Mocked unit tests

Full unit suite: **267 passed**. This includes 16 HTTP contract tests in `tests/unit/test_retrieval_api.py` using mocked embedding and reader dependencies:

1. Valid new Vietnamese query: route response tested with a fake embedder; this does not prove a real encoder is available.
2. Empty and whitespace-only query: rejected with 422.
3. Invalid Top-K values (0, negative, above 50, float, string, boolean): rejected with 422.
4. Query length over configured maximum: rejected with 422.
5. Embedding unavailable/cache miss: 503, fail-closed.
6. Database unavailable: 503, fail-closed.
7. Empty retrieval: explicit `no_results` response.
8. Duplicate chunk IDs: response rejected with provenance error.
9. Missing source metadata: response rejected with provenance error.
10. Default app has no external embedder; a unique uncached query returns `embedding_unavailable`.

Ruff passed for the API, retrieval modules, and new tests.

## Real HTTP and database integration

One marked integration test passed against PostgreSQL using FastAPI `TestClient`, `DenseRetriever`, `research_reader`, and cached evaluation query q001. In addition, Uvicorn was started on loopback `127.0.0.1:8765`; a real HTTP `POST /api/retrieve` returned status `success`, method `dense_baseline_v1`, model `embed-v4.0`, and 5 results. The server was stopped after the request.

Embedding was a **local cached evaluation vector** (1536-dimension `search_query` profile); no Cohere call occurred. The DB session used `asd_rag_v2_research_reader`, read-only, against `asd_rag.v_research_retrieval_chunks`; it returned the existing authorization version 2. This validates the HTTP route and real retrieval path for q001 only.

Actual Top-5 results from the real HTTP request:

| Rank | Chunk ID | Source ID | Document title | Section | Page | Cosine similarity |
|---:|---|---|---|---|---|---:|
| 1 | `NIH-NIMH-ASD-2025@NIH Publication No. 25-MH-8084; Revised 2025#section_v2_1#0000` | `NIH-NIMH-ASD-2025` | Autism Spectrum Disorder | What is autism spectrum disorder? | — | 0.389445325 |
| 2 | `ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0003` | `ASD-CSV-007` | Population-Based Psychiatric Comorbidity in Children and Adolescents With Autism Spectrum Disorder: A Meta-Analysis | Introduction | — | 0.359038689 |
| 3 | `ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0002` | `ASD-CSV-007` | Population-Based Psychiatric Comorbidity in Children and Adolescents With Autism Spectrum Disorder: A Meta-Analysis | Introduction | — | 0.358267923 |
| 4 | `ASD-OA-PMC12620806@PMC distributed version 1#section_v2_1#0012` | `ASD-OA-PMC12620806` | Parallel paths: A narrative review exploring autism and its co-occurring conditions | AUTISM PRESENTATION ASSOCIATED WITH KNOWN ENVIRONMENTAL EXPOSURES > Neurological conditions | — | 0.353994098 |
| 5 | `CDC-ASD-CLINICAL@snapshot-20261017-982fb2058ee3#section_v2_1#0006` | `CDC-ASD-CLINICAL` | Clinical Testing and Diagnosis for Autism Spectrum Disorder | Diagnostic Criteria for ASD > B. Restricted, repetitive patterns of behavior… | — | 0.351687547 |

The API response included each chunk's content. The report omits the passage text while retaining returned metadata and score. Similarity values are ranking signals, not probabilities.

## New-query behavior and authorization

A new Vietnamese query reached the route with a mocked embedder in unit tests. With the actual default app, a unique uncached query fails closed with 503 because its vector is absent. No live Cohere embedding was performed. The existing Cohere approval records cover earlier evaluation inputs and do not authorize arbitrary user queries; matching the 1536 dimension alone would not make another model compatible.

Thus **successful real retrieval with a new query and authorized query embedder has not been demonstrated**. This is the remaining release blocker.

## Regression and restrictions

- The recorded T2.3 66/66 Top-20 regression artifact remains unchanged. No retrieval algorithm, label, source corpus, or stored document embedding was changed.
- The API reuses the existing cosine DenseRetriever and authorization view.
- No DB writes, production access, permission changes, external embedding calls, T2.4-C edits, or reveal-file access occurred.
