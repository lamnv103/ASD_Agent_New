# Dense Retrieval Real Smoke Test ? T2.5-DEV-2

**Result: successful read-only real retrieval**  
**Run date:** 2026-11-17

## Database access

- Configured target: `127.0.0.1:5433/asd_rag_v2` (no connection string or secret recorded).
- Host resolved to: `127.0.0.1`; TCP probe: `connected`.
- Authenticated as `asd_rag_v2_research_reader` into `asd_rag_v2`; transaction read-only setting: `on`.
- Authorized view: `asd_rag.v_research_retrieval_chunks`; query for embedding profile `cohere_embed_v4_1536_v1` returned **2,291** eligible rows.
- The actual dense reader uses the same research role, asserts its identity, sets read-only, and reads only the authorized view.

## Query embedding

- Evaluation item: `q001` from the approved existing 66-question benchmark.
- Model/profile: `embed-v4.0` / `cohere_embed_v4_1536_v1`, `1536` dimensions, `search_query`.
- Embedding path: **local cached vector**; cache hits: 3; misses: 0; live Cohere requests: **0**.
- No arbitrary user query was sent externally.

## Top-5 result

| Rank | Chunk ID | Source | Document title | Section | Page / character range | Cosine distance | Cosine similarity |
|---:|---|---|---|---|---|---:|---:|
| 1 | NIH-NIMH-ASD-2025@NIH Publication No. 25-MH-8084; Revised 2025#section_v2_1#0000 | NIH-NIMH-ASD-2025 | Autism Spectrum Disorder | What is autism spectrum disorder? | chars 1403-2750 | 0.610554675 | 0.389445325 |
| 2 | ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0003 | ASD-CSV-007 | Population-Based Psychiatric Comorbidity in Children and Adolescents With Autism Spectrum Disorder: A Meta-Analysis | Introduction | chars 8936-11670 | 0.640961311 | 0.359038689 |
| 3 | ASD-CSV-007@snapshot-20261017-2a36db9fd179#section_v2_1#0002 | ASD-CSV-007 | Population-Based Psychiatric Comorbidity in Children and Adolescents With Autism Spectrum Disorder: A Meta-Analysis | Introduction | chars 6126-8935 | 0.641732078 | 0.358267922 |
| 4 | ASD-OA-PMC12620806@PMC distributed version 1#section_v2_1#0012 | ASD-OA-PMC12620806 | Parallel paths: A narrative review exploring autism and its co-occurring conditions | AUTISM PRESENTATION ASSOCIATED WITH KNOWN ENVIRONMENTAL EXPOSURES > Neurological conditions | chars 30981-33559 | 0.646005902 | 0.353994098 |
| 5 | CDC-ASD-CLINICAL@snapshot-20261017-982fb2058ee3#section_v2_1#0006 | CDC-ASD-CLINICAL | Clinical Testing and Diagnosis for Autism Spectrum Disorder | Diagnostic Criteria for ASD > B. Restricted, repetitive patterns of behavior, interests, or activities, as manifested by at least two of the following, currently or by history (examples are illustrative, not exhaustive; see text): | chars 4887-6155 | 0.648312453 | 0.351687547 |

Top-5 status: `ok`; authorization version: `2`. Top-10 also returned 10 rows with sequential ranks, unique chunk IDs, finite scores, source metadata, and ascending cosine distance. The Top-5 IDs exactly matched the prefix of Top-10. Repeating Top-10 returned identical ordered chunk IDs.

Cosine distance is the ranking distance (lower ranks first); cosine similarity is `1 - distance`. Neither is a relevance probability.

## Regression and safety checks

- Full offline baseline rerun: **66/66** evaluation queries retrieved; 66 cache hits, 0 misses, 0 API calls.
- Compared Top-20 IDs with the frozen T2.3 run `dense_eval_20261114T153403.jsonl`: **66/66 questions identical** to `dense_eval_20261117T090712.jsonl`.
- All returned Top-5/Top-10 rows came from the authorized research view; they carry authorization version 2 and profile/model provenance.
- Database operations in this smoke/evaluation were `SELECT` only. No DB writes, permission changes, corpus edits, or embedding writes were performed.

## Limitations

This proves the research reader, authorized view, cached evaluation embedding, and existing dense service can execute in the current environment. It does not authorize live Cohere embedding of arbitrary demo-user queries, does not test a production path, and does not implement an HTTP endpoint.
