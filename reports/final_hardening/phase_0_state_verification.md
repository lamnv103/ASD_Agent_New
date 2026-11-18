# Phase 0 — Verify Current Project State

Direct re-verification performed at the start of this task (not trusted from the prior reports alone).

## Wiring check (grep + live call, not just file existence)

```
app/api.py:16  from app.answer.answer_generator import generate as generate_answer
app/api.py:17  from app.retrieval.citation_validation import validate as validate_citations
app/api.py:20  from app.retrieval.evidence_gate import assess as assess_evidence
app/api.py:24  from app.router.classifier import classify as classify_intent
app/api.py:184 intent = classify_intent(text)
app/api.py:206 gate = assess_evidence(text, response.results)
app/api.py:207 evidence = validate_citations(_chat_evidence(gate.supported), gate.supported)
app/api.py:208 answer = generate_answer(text, evidence)
```

| Component | Status |
|---|---|
| Intent router (`app/router/classifier.py`) | **Implemented and wired** — called at the top of `/api/chat`, before retrieval |
| Evidence Sufficiency Gate (`app/retrieval/evidence_gate.py`) | **Implemented and wired** — called on every `asd_question` retrieval result |
| Answer Generator (`app/answer/answer_generator.py`) | **Implemented and wired** — the only place `/api/chat` builds `answer` from |
| Citation Validator (`app/retrieval/citation_validation.py`) | **Implemented and wired** — called before evidence is returned |
| `source_url` in API response | **Implemented and verified** — present in both `evidence` and `citations` |
| `/api/retrieve` (T2.5 raw route) | **Unchanged**, does not use any of the above (confirmed: no new import touches it) |
| `app/answer/mock_answer.py` | **Implemented but not wired** — kept as a historical artifact of the T3.0 state; not imported by `app/api.py` anymore |
| `app/greeting/`, `app/expert_qa/`, `app/info_lookup/`, `app/llm/`, `app/safety/` | **Not implemented** — still empty placeholder packages; their intended role (routing branches, LLM calls, safety filtering) is actually performed by `app/router/`, `app/retrieval/evidence_gate.py`, and `app/answer/answer_generator.py` instead |
| Frontend (`frontend/app.js`) | **Implemented and wired** — reads `answer_mode`/`retrieval_status`/`source_url` from the live API, confirmed by reading the current file (not re-tested in a browser; see Phase 7) |

## Database / retrieval layer

- `app/retrieval/research_reader.py` still connects only as `asd_rag_v2_research_reader`, asserts
  `current_user`, sets `read_only = True`, runs one fixed parameterized statement. **Unchanged since T2.5.**
- `docker ps` shows `asd-rag-v2-db` **Up 2 hours (healthy)** — already running; not started or stopped by
  this task.
- `config/embedding_profiles.json`, `config/retrieval_profiles.json`: unchanged (diffed mentally against
  the known T2.3 values; no edit tool was used on either file in this task).

## Configuration flags

```
app/config.py:57  DEMO_MODE = _flag("ASD_DEMO_MODE", True)
app/config.py:58  ENABLE_LIVE_QUERY_EMBEDDING = _flag(..., False)
app/config.py:59  ENABLE_LIVE_RERANKING = _flag(..., False)
app/config.py:60  ENABLE_LIVE_LLM = _flag(..., False)
app/config.py:62  if ENABLE_LIVE_QUERY_EMBEDDING or ENABLE_LIVE_RERANKING or ENABLE_LIVE_LLM: raise ConfigError(...)
```
**Verified, not just read**: still default-false, still fail-loud on attempted enable. Unchanged.

## Existing tests

`tests/unit/` has 15 files including `test_intent_classifier.py` (15), `test_evidence_gate.py` (11),
`test_answer_generator.py` (7), `test_citation_validation.py` (6), `test_chat_api.py` (22). Re-run at the
start of this task: **343 unit passed, 48 integration passed, ruff clean** — matches what
`phase_6_test_report.md` claimed. **Verified.**

## Current demo behavior (re-run live, same database)

Re-ran the exact probe battery from the T3.1–T3.6 task (greeting, thanks, 7 standard topics, vaccine,
risperidone, stem cell, epilepsy, weather, mixed-intent, uncached) — results identical to what
`final_project_assessment.md` §5 reported. **Verified, not assumed.**

## Conclusion

Every claim in `final_project_assessment.md` and `remaining_blockers.md` that this phase checked holds up
under direct re-verification. No gap was found between "reported" and "actually wired." This clears the
way to focus Phases 1–9 entirely on *improving* the system rather than re-discovering problems already
known to exist (template coverage, lexical-only classifier/gate limits, no clinical review) — those are
carried forward as starting points, not re-litigated from scratch.
