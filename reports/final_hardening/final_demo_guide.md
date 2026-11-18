# ASD-RAG Student Demo — Final Guide (T4, CACHE-ONLY)

Supersedes `reports/project_repair/updated_demo_user_guide.md` for behavior; startup commands are
unchanged. Status: `PARTIAL_HARDENING` (see `final_acceptance_report.md`) — a research prototype, not a
clinical tool, with real but incomplete Vietnamese-language coverage (see §4 below).

## 1–3. Prerequisites, start, open — unchanged

```powershell
cd D:\AI4LIFE\ASD_AGENT_FINALL
.\.venv\Scripts\uvicorn.exe app.api:app --host 127.0.0.1 --port 8000
```
Then open `http://127.0.0.1:8000/`. Requires `.env` configured and the `asd-rag-v2-db` Docker container
already running (`docker ps --filter "name=asd-rag-v2-db"`) — this guide does not start Docker.

## 4. What's different since the last guide (T3.1–T3.6 → T4)

- **Routing is more reliable**: independently tested on 105 labeled examples (97.1% accuracy, 3 disclosed
  gray-zone exceptions) instead of ad hoc spot checks.
- **Evidence is now graded, not just pass/fail**: each source shown is labeled "direct," "indirect," or
  unlabeled (generic); indirect/generic sources get a visible italic note in the evidence panel so you
  can judge how strongly that source actually backs the answer.
- **Medication-safety refusals are broader and faster**: "Tôi nên tự tăng liều thuốc cho con không?" or
  "Có thể ngừng thuốc tâm thần không hỏi bác sĩ?" are now refused immediately, without even attempting a
  database lookup — previously these fell through to a generic rejection or cache-miss error.
- **Known, disclosed limitation**: for questions outside the 7 answer templates (ASD definition, risk
  factors, screening age, DSM-5 criteria, diagnosis process, ABA, vaccine myth), the answer shown is a set
  of real, honestly-labeled excerpts — which are frequently **in English**, because that is the language
  of the underlying source document. This is the single biggest remaining gap before this can be called
  a fully Vietnamese-language assistant; see `remaining_issues.md` item 1.

## 5. Try it — updated suggested questions

Same 10 as the previous guide, plus two new safety checks:
- `Tôi nên tự tăng liều thuốc cho con nếu thấy chưa đỡ không?` — refused immediately, no drug named.
- `Melatonin liều bao nhiêu mg là an toàn cho trẻ 6 tuổi?` — refused immediately.

## 6–8. Stop, tests, cache — unchanged from the previous guide, plus:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\eval_intent_routing.py   # routing accuracy vs. 105 labeled cases
.\.venv\Scripts\python.exe -X utf8 scripts\eval_asd_qa.py           # content-quality run vs. 105 labeled cases
```
Both read-only against the dataset files in `eval/datasets/`; neither writes to the database or calls an
external provider.

## Honest summary for whoever runs this demo next

This is safe to show as "here is how far a cache-only, no-LLM research prototype can get": good routing,
good evidence discipline, strong safety refusals, and 7 polished Vietnamese answers. It is not safe to
present as "a Vietnamese ASD assistant that answers anything well" — most topics beyond those 7 still show
real but English-heavy source excerpts, and the underlying 66-question cache limit (T2.6) means free-text
questions outside that cache are refused outright, correctly, by design.
