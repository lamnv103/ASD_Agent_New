# T6.0 Phase 2 ? Full-text search audit

**Status:** VERIFIED for configuration, implementation, and observed candidate retrieval. No FTS profile was promoted or modified.

## Existing index and search

The migration builds `content_tsv` from section heading (weight B) and content (weight A) using PostgreSQL `english`; the GIN index is declared in migration `002_indexes.sql`. The configured profiles use the same `english` configuration, the authorized research view, the Cohere document profile code, and `ts_rank_cd` with normalization 0. That score is an ordering signal, not BM25, probability, or clinical evidence strength.

`app/retrieval/fts.py` enforces the allowlisted view, research-reader role, expected DB user, read-only session, fixed SQL, and bound parameters. Raw Vietnamese query text is processed with PostgreSQL `plainto_tsquery`; glossary terms are parsed via `plainto_tsquery`/`phraseto_tsquery`, then combined from PostgreSQL-produced tsquery strings. Results are ranked descending by `ts_rank_cd`, with `chunk_id` as a deterministic tie-breaker, and limited to K (default 10, maximum 50). No result is reranked by a model.

## Profiles and comparative observations

| Profile | Query construction | Original 66 benchmark queries with results | Empty | Returned candidate rows for originals |
|---|---|---:|---:|---:|
| FTS-A | Raw Vietnamese, `plain_and` | 0 | 66 | 0 |
| FTS-B | Original query OR all glossary concept groups (`glossary_and_groups`) | 55 | 11 | 433 |
| FTS-C | Original query OR any glossary concept group (`glossary_or_groups`) | 65 | 1 | 646 |
| T5.7 isolated EXP-1c-style harness | Separate experimental harness | 61 | 5 | 503 |

The CSV includes one empty-status record per empty query. Its per-profile total rows also include 12 extra accent/no-diacritic variants for each FTS profile/harness; those variants were not run through Dense because no matching cached query vectors were available.

FTS-A's zero-hit result is consistent with its raw Vietnamese terms being sent to the configured English text-search index without translation. It is a measured result on this set, not proof that every Vietnamese query will fail. FTS-C's greater coverage than FTS-B is accompanied by substantially broader candidate output; without independent judgments, this does not establish improved relevance.

## Glossary and language limits

The FTS glossary notes that its entries were written using the 66 `retrieval_eval_v1` questions (development vocabulary overlaps the evaluation set), and explicitly calls for a held-out set. A separate historical reconciliation recorded 63 app NLP glossary entries versus 94 FTS entries, with 37 compatible overlaps and scope differences. They are separate resources; no shared glossary is wired into the live app/Evidence Gate. Treat this as a maintenance and leakage/generalization risk, not an audited complete taxonomy.

For six selected questions, exact and accent-stripped text variants were run against FTS profiles. All 66 original questions contain diacritics. An offline glossary expansion check found identical English term expansions for 66/66 exact/diacritic-stripped original pairs; this check measures expansion output only, not retrieval equivalence. The twelve retrieval variants are a small diagnostic sample, not a representative language benchmark.

**Limitation:** FTS is available as an isolated retriever, not as the production/API retrieval path. Before integration, evidence provenance must represent FTS's actual matched terms/rank and metadata. Do not synthesize a cosine similarity for FTS results or feed its raw rank score into a cosine-based Evidence Gate.
