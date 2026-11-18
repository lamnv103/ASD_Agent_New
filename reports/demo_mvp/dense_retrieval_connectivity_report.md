# Dense Retrieval Connectivity Report ? T2.5-DEV-2

**Final status: `DB_CONNECTIVITY_RESTORED`**

## Previous timeout and diagnosis

The prior execution failed with the recorded exception **`psycopg.errors.ConnectionTimeout: connection timeout expired`** while establishing a connection, before authentication or SQL execution. This places that failure at the connection-establishment layer; it was not a schema/view permission error.

No persistent configuration correction was needed. The current `.env` target is `ASD_RAG_DB_HOST=127.0.0.1`, `ASD_RAG_DB_PORT=5433`, `ASD_RAG_DB_NAME=asd_rag_v2`. The host resolves to `127.0.0.1`, and TCP port 5433 accepts connections. A separate diagnostic connection completed in 0.062 seconds; the current user/database/read-only setting were `asd_rag_v2_research_reader` / `asd_rag_v2` / `on`.

The exact transient cause of the earlier connection timeout cannot be established from current evidence. Docker CLI diagnostics failed with a sanitized local permission error: access to the Docker config and Docker engine named pipe was denied. Therefore container name/status and Docker healthcheck state were not directly inspected. The PostgreSQL endpoint is operationally healthy now: authenticated SQL and the authorized view query succeed. No attempt was made to start Docker or change configuration.

## Phase 1 diagnostic results

| Check | Result | Evidence |
|---|---|---|
| PostgreSQL container running | Not directly verifiable | `docker ps` denied access to the Docker engine named pipe; no container was started. |
| PostgreSQL healthcheck | Not directly verifiable | Docker daemon inaccessible. SQL endpoint is accepting authenticated queries. |
| Port 5433 listening | Yes | `Test-NetConnection 127.0.0.1 -Port 5433` returned `True`; Python TCP connect succeeded. |
| Hostname/configuration | Correct for this process | `.env` target is `127.0.0.1:5433`; resolves to `127.0.0.1`; connection succeeded. |
| Database `asd_rag_v2` reachable | Yes | Current session returned database `asd_rag_v2`. |
| Research reader authentication | Yes | `current_user` is `asd_rag_v2_research_reader`. |
| View permission and query | Yes | `SELECT ... FROM asd_rag.v_research_retrieval_chunks ... LIMIT 1` returned a row; profile count is 2,291. |

Passwords, API keys, tokens, and full connection strings were not printed. No admin role was used.

## Retrieval result

The real Top-5 and Top-10 smoke test succeeded using cached evaluation vector `q001` with `DenseRetriever` and the research reader. See [dense_retrieval_smoke_test.md](dense_retrieval_smoke_test.md) for actual Top-5 metadata, scores, validation, and regression evidence.

The 66-query regression was reproduced offline: 66 cache hits, 0 misses, 0 Cohere calls. Its Top-20 ranking was identical to the recorded T2.3 baseline for **66/66** questions. Metrics are exploratory Silver-label metrics only; this task did not change labels or tune retrieval.

## Authorization and next action

The only remaining query-embedding authorization blocker concerns **arbitrary live demo-user queries**. The successful smoke/regression used pre-existing evaluation embeddings and sent no query to Cohere. Before any live Cohere request with user text, the project owner must explicitly authorize that processing and resolve the provider data-handling questions in `docs/provider_terms/cohere_2026-11-14.md`, or provide an approved local embedder. No user action is needed to restore current database access.
