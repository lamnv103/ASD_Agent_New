# Final Project Assessment — T3.1–T3.6 Repair

**Final status: `PROJECT_READY_FOR_EXPERT_REVIEW`**

This status means exactly what its name says: the system is ready for a human ASD-domain expert to review
its routing, evidence handling, and the 7 answer templates — it is **not** a declaration that the product
is clinically validated or finished. See §6 for exactly what still needs a human ASD expert's sign-off,
and `demo_limitations.md` (T3.0, still accurate) plus this report's §5 for what is intentionally
incomplete.

## 1. What was actually implemented

- **Phase 1** (`app/router/classifier.py`, `app/nlp/text_match.py`): a lexical, diacritic-/typo-tolerant,
  bilingual intent classifier with 3 branches (greeting / out-of-scope / ASD question). Greeting and
  out-of-scope messages never call the embedder or the database.
- **Phase 2** (`app/retrieval/evidence_gate.py`): an Evidence Sufficiency Gate wrapping `DenseRetriever`'s
  output, using cosine similarity + bilingual topic-term matching (title+section+content) to separate
  genuinely supporting evidence from Top-K noise. Caught all 4 confirmed safety-sensitive failure cases
  from the independent expert evaluation, and **corrected** one of them (vaccine) where real debunking
  evidence existed but had been missed due to excerpt truncation in the prior report.
- **Phase 3** (`app/answer/answer_generator.py`): non-LLM answer generation — 7 hand-authored,
  evidence-gated Vietnamese templates, a labeled extractive fallback (no bare chunk codes), explicit
  insufficient-evidence handling, and two safety overrides (medication dosing refusal, unproven-cure
  caution).
- **Phase 4** (`app/retrieval/citation_validation.py` + `app/api.py`): `source_url` now included in every
  evidence/citation item (was missing before despite the data existing); a validation step drops any
  citation whose name/URL/excerpt doesn't exactly match the real retrieved chunk, or that isn't among the
  Evidence-Gate-approved sources.
- **Phase 5** (`frontend/*`): evidence cards show "Nguồn N" + a clickable source link instead of a bare
  citation code; per-answer-mode tags replace the single "MOCK ANSWER" label, each honestly naming the
  generation method.
- **Phase 6**: 39 new unit/integration tests; all pre-existing tests updated where their fixtures assumed
  the old (now-replaced) behavior; full regression suite re-run; T2.3 benchmark re-confirmed 66/66.

## 2. Exact files changed

**New:**
- `app/nlp/__init__.py`, `app/nlp/text_match.py`
- `app/router/__init__.py`, `app/router/classifier.py`
- `app/retrieval/evidence_gate.py`, `app/retrieval/citation_validation.py`
- `app/answer/answer_generator.py`
- `tests/unit/test_intent_classifier.py`, `test_evidence_gate.py`, `test_answer_generator.py`,
  `test_citation_validation.py`
- `reports/project_repair/*` (10 files, this one included)

**Modified:**
- `app/api.py` — `/api/chat` now runs intent routing → retrieval → Evidence Gate → Citation Validation →
  answer generation; `_chat_evidence`/`_chat_citations` include `source_url`. `/api/retrieve` and
  `build_offline_retriever()` **unchanged**.
- `frontend/app.js`, `frontend/style.css`, `frontend/index.html` — evidence card rendering, per-mode tags,
  updated disclaimer text.
- `tests/unit/test_chat_api.py`, `tests/integration/test_chat_api_db.py` — rewritten to reflect the new
  pipeline and to use realistic ASD-domain query text in fixtures (the old generic placeholder text, e.g.
  "câu hỏi", is no longer routable to the retriever by the new router, which is itself evidence the
  router works).

**Not touched:** `app/retrieval/dense.py`, `embeddings.py`, `query_embedding.py`, `research_reader.py`,
`types.py`; `config/embedding_profiles.json`, `config/retrieval_profiles.json`; `migrations/`;
`data/index/query_embeddings/`; `app/config.py`'s flag defaults; `eval/datasets/`; any annotation file;
`app/answer/mock_answer.py` (kept as a historical artifact of the T3.0 state, no longer imported by
`app/api.py`).

## 3. Root causes addressed (mapped to the independent expert evaluation's findings)

| Finding | Root cause | Fix |
|---|---|---|
| Weather question returned "ok" with ASD evidence | No relevance/sufficiency check anywhere in the pipeline | Router (no ASD domain signal → rejected pre-retrieval) + Evidence Gate (defense in depth) |
| Greeting routed through embedding/retrieval | No intent classification existed at all | Router Branch 1 |
| 4 safety-sensitive questions got unrelated evidence treated as "ok" | Cosine similarity dominated by the ubiquitous "tự kỷ"/"autism" anchor; no topic-specific check | Evidence Gate's specific-term matching (title+section+content) |
| Missing `source_url` | Field existed in `RetrievedChunk` but was never read by `_chat_evidence()` — an omission, not a data gap | Added to the response |
| Answer was a raw chunk dump with `C1`/`C2`/`C3` labels | No answer-generation layer existed beyond excerpt-dumping | Template generator for canonical topics; honestly-labeled, numbered (not lettered-code) fallback for the rest |

## 4. Tests run / not run

See `phase_6_test_report.md` for full detail. Summary: 343 unit + 48 integration tests, all passing;
`ruff check` clean; T2.3 regression 66/66 identical. Not run: any browser-rendered visual test (no
tooling), any live Cohere/LLM/reranking call (not authorized, and verified absent via
`/api/system/status` and the `ConfigError` fail-loud guard).

## 5. Results: before vs. after (live, same database, same code path family)

| Case | Before | After |
|---|---|---|
| "Rối loạn phổ tự kỷ là gì?" | Chunk dump labeled `[MOCK]`, with `C1 <raw English excerpt>` lines | Short, grounded Vietnamese paragraph matching the task's own worked example, with 2 real cited sources incl. working URLs |
| "Hôm nay thời tiết thế nào?" | `retrieval_status: "ok"`, 5 unrelated ASD chunks | `retrieval_status: "out_of_scope"`, no DB call |
| "Xin chào..." | `503 QUERY_NOT_CACHED` | `retrieval_status: "skipped_greeting"`, friendly reply, no DB/embedder call |
| "Liều risperidone..." | Unrelated sleep-medication chunks shown as "evidence" | Explicit medical-refusal message, no evidence shown |
| "Vắc-xin có gây tự kỷ không?" | Evaluated (incorrectly, due to excerpt truncation) as "no evidence" | Correct evidence found and cited; answer states the claim traces to a retracted study |
| "Trẻ tự kỷ có hay bị động kinh không?" | Unrelated anxiety/ADHD evidence shown as "ok" | `insufficient_evidence`, no fabricated comorbidity claim |

## 6. Items that need a human ASD-domain expert's confirmation before wider use

1. **Wording accuracy of the 7 templates** — each was authored by cross-checking retrieved evidence, but
   none have been reviewed by a clinician or ASD-education specialist for register, nuance, or omissions.
2. **The vaccine-myth template's phrasing** — the underlying evidence (a narrative review mentioning "a
   now retracted study") is solid, but a public-health-communication expert should confirm the Vietnamese
   phrasing is maximally clear and non-alarming for a lay audience.
3. **Risk-factor vs. cause framing** (template #2) — written to match clinical convention, but should be
   checked against current Vietnamese-language patient-education norms.
4. **Coverage gaps**: signs/symptoms (q007-style), GFCF diet, and screening-age edge cases fall to
   extractive fallback, not a template — an expert should judge whether the raw excerpt presentation is
   acceptable for a public demo or whether those need templates before any wider release.
5. **The ADHD-vs-ASD lexical-overlap limitation** (Phase 2's stated limitation) — an expert should assess
   how often this class of error actually occurs across the full 66-question set, which this task did not
   exhaustively re-run question-by-question (it re-verified the specific confirmed cases, not all 66).

## 7. How to run the demo

See `reports/project_repair/updated_demo_user_guide.md` (same commands as before — nothing about how the
demo is started changed in this task, only what happens once it's running).
