# ASD-RAG Student Demo — User Guide (CACHE-ONLY, post-repair)

Supersedes `reports/demo_mvp/demo_user_guide.md` for what to expect once running — the startup commands
are unchanged. This demo runs **entirely locally**. It never calls Cohere, never reranks, and never calls
an external LLM (verified live via `GET /api/system/status` and enforced by a fail-loud startup check in
`app/config.py`). Only questions whose vector is already cached (the 66 evaluation questions, or anything
added to the cache the same way) can be answered with real retrieved evidence; a greeting or a message
with no ASD-domain content never reaches the database at all; anything else returns a clear error instead
of a fake result.

All commands below are PowerShell, run from the project root `D:\AI4LIFE\ASD_AGENT_FINALL`.

## 1. Prerequisites (unchanged)

- `.venv` with dependencies installed (`python -m venv .venv` then `.\.venv\Scripts\pip.exe install -e .[dev]`
  if it doesn't exist yet).
- A `.env` file with the research-reader database credentials (copy `.env.example`).
- Docker Desktop with the `asd-rag-v2-db` container already created and running:
  ```powershell
  docker ps --filter "name=asd-rag-v2-db"
  ```
  If it's not running, start Docker Desktop, then `docker start asd-rag-v2-db`. This guide does not create
  a database from scratch.

## 2. Start the backend (unchanged)

```powershell
cd D:\AI4LIFE\ASD_AGENT_FINALL
.\.venv\Scripts\uvicorn.exe app.api:app --host 127.0.0.1 --port 8000
```

One process serves both the API and the static frontend.

## 3. Open the demo

```
http://127.0.0.1:8000/
```

## 4. What's different since the previous guide

- **Answers are no longer a raw chunk dump.** For 7 common topics (ASD definition, risk factors,
  screening age, DSM-5 criteria, diagnosis process, ABA/behavioral intervention, and the vaccine-autism
  myth), you'll see a short, grounded Vietnamese paragraph with a tag reading "MẪU CÓ KIỂM CHỨNG NGUỒN
  (KHÔNG PHẢI LLM)" — a template, not an AI-generated answer, but also not a literal excerpt. For other
  cached questions, you'll see numbered excerpts tagged "TRÍCH DẪN TRỰC TIẾP (CHƯA CÓ BẢN TỔNG HỢP)" — still
  real evidence, honestly labeled as not yet having a Vietnamese summary.
- **Sources are now clickable links**, not just names — click any "Nguồn N" entry in the right-hand panel
  to open the real source page.
- **A plain greeting** ("Xin chào!", "Cảm ơn bạn!") gets a short, direct reply and never touches the
  database.
- **An off-topic question** ("Hôm nay thời tiết thế nào?") is now rejected immediately with a clear
  "không thuộc phạm vi ASD" message instead of returning unrelated ASD evidence as if it were a match.
- **Medication-dose questions** (e.g. "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?") get a firm "ask
  your doctor" refusal, tagged in red, instead of any attempt to answer from retrieved text.
- **"Cure" claims with no supporting evidence** (e.g. about stem cells) get an explicit caution message
  rather than silence or a guess.

## 5. Try it — updated suggested questions

- `Rối loạn phổ tự kỷ là gì?` — template answer, 2 real cited sources with links.
- `Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?` — extractive fallback (no dedicated template yet).
- `Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?` — template answer.
- `Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì?` — template answer.
- `Vắc-xin có gây tự kỷ không?` — template answer citing the actual debunking evidence found in the
  corpus (a narrative review referencing a retracted study).
- `Liều risperidone cho trẻ 5 tuổi là bao nhiêu?` — safety refusal, on purpose.
- `Tế bào gốc có chữa được tự kỷ không?` — safety caution, on purpose (no supporting evidence exists).
- `Trẻ tự kỷ có hay bị động kinh không?` — explicit "insufficient evidence", on purpose.
- `Hôm nay thời tiết thế nào?` — out-of-scope rejection, on purpose.
- `Xin chào!` — greeting reply, on purpose.
- A typed question that is **not** cached (and is a real ASD question, not a greeting/off-topic one)
  still returns the "chưa có trong cache" (not cached) HTTP 503 message — this remains expected behavior,
  unchanged by this task; see `reports/demo_mvp/demo_limitations.md`.

## 6. Stop the demo (unchanged)

`Ctrl+C` in the `uvicorn` terminal. Stop the DB container separately with `docker stop asd-rag-v2-db` if
desired.

## 7. Running the test suite

```powershell
cd D:\AI4LIFE\ASD_AGENT_FINALL
.\.venv\Scripts\python.exe -m pytest -m "not integration" -q   # 343 tests, fast, mocked, no DB
.\.venv\Scripts\python.exe -m pytest -m integration -q         # 48 tests, needs the DB container running
.\.venv\Scripts\ruff.exe check app tests                        # lint
```

## 8. Changing which questions are cached (unchanged)

Still requires the T2.6-authorized Cohere path to add new vectors; not possible from this demo alone.
