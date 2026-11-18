# ASD-RAG Student Demo — User Guide (CACHE-ONLY)

This demo runs **entirely locally**. It never calls Cohere, never reranks, and never calls an external LLM
— see `t3_0_implementation_report.md` §7 and `demo_limitations.md`. Only questions whose vector is already
cached (currently the 66 evaluation questions, or anything added to the cache the same way) can be
answered; anything else returns a clear "not cached" error instead of a fake result.

All commands below are PowerShell, run from the project root `D:\AI4LIFE\ASD_AGENT_FINALL`.

## 1. Prerequisites

- The project's Python virtual environment already exists at `.venv` with all dependencies installed
  (FastAPI, Uvicorn, psycopg, etc.). If it does not exist yet, create and install it first:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\pip.exe install -e .[dev]
  ```
- A `.env` file at the project root with the research-reader database credentials
  (`ASD_RAG_DB_HOST`, `ASD_RAG_DB_PORT`, `ASD_RAG_DB_NAME`, `ASD_RAG_RESEARCH_READER_PASSWORD`). Copy
  `.env.example` if you don't have one yet, and fill in the password — never commit this file.
- Docker Desktop, with the project's PostgreSQL container already created (it is normally left running).
  **This guide does not start Docker for you** — if it's not running, start Docker Desktop yourself, then
  start the container:
  ```powershell
  docker start asd-rag-v2-db
  ```
  Check it's up and healthy before continuing:
  ```powershell
  docker ps --filter "name=asd-rag-v2-db"
  ```
  If this command fails or the container does not exist, **stop here** — the demo cannot retrieve real
  evidence without it, and this guide does not create a new database from scratch.

## 2. Start the backend (serves both the API and the web UI)

```powershell
cd D:\AI4LIFE\ASD_AGENT_FINALL
.\.venv\Scripts\uvicorn.exe app.api:app --host 127.0.0.1 --port 8000
```

Leave this running in its own terminal window. There is no separate frontend server or build step — the
same process serves the chat UI as static files.

## 3. Open the demo

In a browser, go to:

```
http://127.0.0.1:8000/
```

You should see the "Trợ lý tra cứu ASD" page with a DEMO MODE / CACHE-ONLY badge, the required safety
notice banner, a row of suggested questions, a chat box, and an evidence panel on the right.

## 4. Try it

- Click one of the suggested question buttons (these are guaranteed to be cached), or type one of the
  following exactly (they are 5 of the 66 pre-cached evaluation questions):
  - `Rối loạn phổ tự kỷ là gì?`
  - `Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?`
  - `Tự kỷ được chẩn đoán như thế nào?`
  - `Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì?`
  - `Vắc-xin có gây tự kỷ không?` (an "unanswerable, out of current evidence scope" question — on
    purpose, to show how the demo handles that case)
- A typed question that is **not** one of the 66 cached questions will return a clear "chưa có trong
  cache" (not cached) message with HTTP 503 — this is expected, not a bug; see `demo_limitations.md`.
- The chat answer is always labeled `[MOCK …]` — it is retrieved evidence text plus a fixed disclaimer, not
  an AI-generated answer. The right-hand panel shows the real, database-sourced evidence (source, section,
  page/locator, excerpt) behind that answer.

## 5. Stop the demo

Press `Ctrl+C` in the terminal running `uvicorn`. This does not stop the database container; leave it
running or stop it yourself with `docker stop asd-rag-v2-db` if you want to shut everything down.

## 6. Running the test suite (optional, for verification)

```powershell
cd D:\AI4LIFE\ASD_AGENT_FINALL
.\.venv\Scripts\python.exe -m pytest -m "not integration" -q   # fast, mocked, no DB
.\.venv\Scripts\python.exe -m pytest -m integration -q         # needs the DB container running
.\.venv\Scripts\ruff.exe check app tests                        # lint
```

## 7. Changing which questions are cached (advanced, optional)

New query vectors cannot be added by this demo (that requires the Cohere authorization covered in T2.6).
If a project maintainer has separately added more cached vectors to `data/index/query_embeddings/` using
the project's existing authorized tooling, those questions will work in the demo automatically — no code
change needed, since the chat endpoint always checks the same cache directory.
