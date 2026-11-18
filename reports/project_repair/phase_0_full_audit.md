# Phase 0 — Full Project Audit

Read before any code change: `independent_expert_evaluation.md`, `t2_6_*` (3 files), `t2_5_local_encoder_compatibility_audit.md`, `t3_0_*` (3 files), `demo_user_guide.md`, `demo_limitations.md`. All confirmed present at the paths given in the task and already read in full during the preceding T2.5/T2.6/T3.0 work this session; no file was missing.

## 1. Component inventory

| Component | File(s) | Status |
|---|---|---|
| Embedding client | `app/retrieval/embeddings.py` | Working, untouched by this task. |
| Document embedding profile | `config/embedding_profiles.json` | 2,338 vectors, `cohere_embed_v4_1536_v1`, dim 1536. **Not touched.** |
| Query embedding cache | `app/retrieval/query_embedding.py`, `data/index/query_embeddings/` | Working, cache-only (`inner=None`), 66/66 cache hits. **Not touched.** |
| Research DB reader | `app/retrieval/research_reader.py` | Read-only, asserts `asd_rag_v2_research_reader`, fixed parameterized SQL. **Not touched.** |
| Dense retriever | `app/retrieval/dense.py` | Validates query/k, provenance checks, no evidence-sufficiency step. **Not touched** (Evidence Gate is added as a wrapper, not an edit to this file, to keep the T2.3 benchmark path — which calls `DenseRetriever` directly — byte-identical). |
| Demo config flags | `app/config.py` | `DEMO_MODE`, `ENABLE_LIVE_*` added in T3.0, fail-loud on attempted enable. **Not touched** except adding comments; defaults unchanged. |
| HTTP API | `app/api.py` | `/api/retrieve` (T2.5, untouched), `/api/chat` (T3.0, extended this task), `/api/system/status` (T3.0). |
| Answer generation | `app/answer/mock_answer.py` | T3.0 `MockAnswerGenerator`: excerpt dump + disclaimer, explicitly non-LLM. **Confirmed by expert review as not a real answer generator** — this is the Phase 3 target. |
| Intent routing / greeting / branches | `app/greeting/`, `app/router/`, `app/expert_qa/`, `app/info_lookup/`, `app/llm/`, `app/safety/` | **All empty placeholder packages** (confirmed by directory listing: no `.py` files besides possibly `__init__`). This is the Phase 1 target. |
| Frontend | `frontend/index.html`, `style.css`, `app.js` | Static, shows `citation_id` (`C1`…) in both the evidence panel and inside the Mock answer text — **this is the literal pattern the expert evaluation and this task's Phase 3.3 explicitly forbid** ("Không hiển thị: C1, C2, C3"). Phase 5 target. |
| Knowledge `.md` files | — | **None exist.** The project's knowledge source is 2,338 embedded chunks in PostgreSQL, derived from `data/raw/source_library` (PDF/HTML/XML originals), not from any curated `.md` corpus. This is stated explicitly in `independent_expert_evaluation.md` §0 and reconfirmed here by a repo-wide search for `.md` files outside `reports/`/`docs/`/`eval/` — none found that constitute "biên soạn sẵn kiến thức ASD". **Consequence for Phase 3**: "ưu tiên nội dung `.md` đã biên soạn" cannot be satisfied literally — there is no such corpus. The closest available approximation is building a small number of hand-authored Vietnamese answer templates, each grounded in and cross-checked against specific retrieved English-language evidence, and disclosed as such (see `phase_3_answer_generation.md`). |

## 2. Confirmed-by-expert-evaluation defects (re-verified, not re-guessed)

All four re-verified live against the real DB during this task before any fix (see `phase_2_retrieval_evidence_gate.md` for the before/after evidence):

1. `q062` "Hôm nay thời tiết thế nào?" → `retrieval_status: "ok"`, 5 unrelated ASD chunks returned. Confirmed.
2. A plain greeting ("Xin chào, bạn có thể giúp gì cho tôi?") → `503 QUERY_NOT_CACHED` (routed through the same embedding/retrieval path as a real question). Confirmed.
3. `source_url` is present on `RetrievedChunk` (`app/retrieval/types.py`) but omitted by `_chat_evidence()` in `app/api.py`. Confirmed by reading the function.
4. `q057`/`q058`/`q059`/`q066` (vaccine, risperidone dose, stem cells, epilepsy) retrieved evidence with no term match to the actual question topic. Confirmed, same Top-5 as the expert evaluation reproduced live again in Phase 2.

## 3. New issues found during this audit (not in the prior report)

5. `/api/chat`'s Mock answer literally prints `C1`, `C2`, … inline in the answer **text itself** (not just as a separate evidence-panel label) — a stricter violation of the "no C1/C2/C3" output rule than the expert report's wording suggested, since it's inside the user-facing answer string, not just structured metadata.
6. No test exists anywhere for intent classification, evidence sufficiency, or citation validation — these did not exist to test.
7. The two "generic ASD anchor" words (`tự kỷ`, `autism`) appear in almost every stored chunk, which means any naive keyword-only relevance check would rubber-stamp everything as "relevant" — a real Evidence Gate must separate the generic ASD anchor from *topic-specific* terms (vaccine, risperidone, stem cell, epilepsy, …), otherwise it cannot catch exactly the 4 confirmed failure cases. This directly shapes the Phase 2 design (see that report).
8. Most retrieved chunk content is in **English** (CDC/NIH/PMC sources) while queries are Vietnamese. Any lexical overlap check between query and chunk text must bridge this with a bilingual term glossary, or it will never find any overlap at all. This also explains why natural Vietnamese answer synthesis cannot be done by naive extraction (Phase 3 constraint).

## 4. Dependency map (what Phase 1–4 touch, and what must stay untouched)

```
app/retrieval/embeddings.py        \
app/retrieval/query_embedding.py    |  frozen (T2.3 benchmark + T2.6 authorization gate depend on these)
app/retrieval/research_reader.py    |
app/retrieval/dense.py             /   (only consumed, never edited, by the new Phase 2 Evidence Gate)
            |
            v
app/retrieval/evidence_gate.py  (NEW, Phase 2) -- wraps DenseRetriever's output, does not change it
            |
            v
app/router/classifier.py        (NEW, Phase 1) -- runs BEFORE the retriever is ever called
            |
            v
app/answer/answer_generator.py  (NEW, Phase 3, replaces the role of mock_answer.py in the API path)
            |
            v
app/api.py  /api/chat            (EDITED, Phases 1/2/3/4) -- orchestrates the above
app/api.py  /api/retrieve         UNCHANGED (still the raw T2.5 passthrough, used by nothing new)
frontend/*                        (EDITED, Phase 5)
```

`scripts/dense_retrieval_eval.py` (the T2.3 regression script) calls `DenseRetriever`/`CachedQueryEmbedder`/`ResearchVectorReader` directly — it does **not** go through `app/api.py` at all. Therefore nothing in Phases 1–5 can change its output, by construction, as long as Phase 2's Evidence Gate is implemented as a separate wrapper module rather than an edit inside `dense.py`. This is confirmed again at the end of Phase 6 by re-running the regression script.

## 5. Risk flags — stop-and-ask items

None found that require pausing: all planned changes are additive (new modules) or confined to `app/api.py`'s `/api/chat` route and `frontend/`, neither of which the benchmark or the embedding/authorization layers depend on. No change to `config/embedding_profiles.json`, `migrations/`, `data/index/query_embeddings/`, `app/config.py`'s default flag values, or any annotation/eval dataset file is planned or made.
