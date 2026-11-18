# Dense Retrieval Test Report — T2.5-DEV-1

## Unit tests

- Focused retrieval/embedding suite: **57 passed** (`tests/unit/test_dense_retrieval.py`, `tests/unit/test_embeddings.py`).
- Complete unit suite: **251 passed** (`tests/unit`).
- Ruff: **passed** for `app/retrieval` and the two modified unit test files.
- The first focused pytest attempt had 53 passing tests and 4 setup errors because pytest tried to enumerate a sandbox-protected Windows temp directory. Rerunning with `--basetemp reports/demo_mvp/.pytest-tmp` and the cache plugin disabled passed all 57.
- Mock tests verify embedding failures and database authorization/error handling. They are not reported as real service tests.

## Real database retrieval and baseline regression

The first real read-only evaluation attempt failed with `psycopg.errors.ConnectionTimeout: connection timeout expired`. On a subsequent diagnostic run, DNS/loopback resolution and TCP port 5433 succeeded; `asd_rag_v2_research_reader` authenticated to `asd_rag_v2`, the session was read-only, and the authorized view returned rows. The reason for the earlier transient timeout is unknown.

Then `scripts/dense_retrieval_eval.py` ran offline from cached query vectors: 66/66 cache hits, 0 misses, 0 Cohere calls. The full 66-query regression completed. Current Top-20 results were compared with the frozen T2.3 log and identical for 66/66 questions. Metrics and candidate-pool artifacts are `dense_retrieval_regression_metrics.json` and `dense_retrieval_regression_pool.csv` under this folder. A direct real smoke test also retrieved Top-5 and Top-10 for q001, with deterministic repeated Top-10 ordering; actual Top-5 rows are recorded in `dense_retrieval_smoke_test.md`.

Integration tests were not run. The existing integration file includes a fixture query through the owner role, which was excluded from the authorized service path; real retrieval was instead exercised directly through `DenseRetriever` and `research_reader`.

## Embedding provider

No live Cohere request was made. This is intentional because the inspected approval covers prior research/test query texts and does not authorize arbitrary demo-user queries. Mocked provider tests passed; external provider availability and live query behavior are not claimed.

## Final test conclusion

Local unit behavior and a real cached-query database retrieval are validated. Live Cohere embedding of arbitrary user queries remains untested and unauthorized. Do not treat mock embedding tests or the cached query path as proof that arbitrary user queries may be sent externally.
