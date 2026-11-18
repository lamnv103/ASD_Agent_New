# Phase 1 — Intent Classification & Three-Branch Routing

## What was built

`app/nlp/text_match.py` (shared matching primitives) and `app/router/classifier.py` (the router).

`classify(query) -> IntentResult(branch, reason, greeting_kind)` with three branches:

- **`greeting`** — small talk with no ASD content. `/api/chat` answers directly from a fixed reply table
  (`app/answer/answer_generator.py:GREETING_REPLY`) and **never** calls the embedder, the cache, or the
  database. Verified live: `"Xin chào, bạn có thể giúp gì cho tôi?"` and `"Cảm ơn bạn nhiều!"` both return
  `retrieval_status: "skipped_greeting"`.
- **`out_of_scope`** — no ASD-domain signal at all. Rejected **before** retrieval. Verified live:
  `"Hôm nay thời tiết thế nào?"` returns `retrieval_status: "out_of_scope"` with empty evidence — this is
  the exact case the task brief calls out by name, and it no longer reaches the database at all (confirmed
  by a unit test that fails the test double's embedder/reader with `RuntimeError("must not be called")`
  and still gets a clean response).
- **`asd_question`** — everything else. Goes through retrieval → Evidence Sufficiency Gate (Phase 2) →
  Citation Validation (Phase 4) → answer generation (Phase 3).

## Why Branch 2 and Branch 3 are merged

The task brief's architecture describes two separate branches: "Nhánh 2 – general information retrieval"
and "Nhánh 3 – professional ASD questions". This project has exactly **one** knowledge source (the
2,338-chunk research vector view) and **one** retrieval pipeline. There is nothing a separate Branch 2
classifier could route to that would behave any differently from Branch 3 — building one would be a second
branch that always ends up calling the same code as the first, which is not a real distinction, just an
appearance of one. This is disclosed here rather than faked. If a second, structurally different knowledge
source (e.g. a small FAQ/glossary table) is added later, splitting them becomes meaningful and should be
revisited.

## Method and why it is not "just a keyword list"

A plain `if word in query` keyword list was explicitly disallowed by the task brief, and for good reason —
it breaks on diacritics, typos, and cross-language mixing. `app/nlp/text_match.py` instead:

- **Folds** text through Unicode NFD diacritic stripping (`fold()`), so `"Tự Kỷ"`, `"tu ky"`, and `"tự  kỷ"`
  (extra space) all normalize identically.
- Matches on **word boundaries** (`contains_word()`), not raw substrings — this was not cosmetic: a bug
  was caught and fixed during this task where the English greeting word `"hi"` matched as a substring
  inside unrelated Vietnamese words like `"nhiêu"` and `"thích"`, misrouting ordinary questions (e.g. "Giá
  vàng hôm nay là bao nhiêu?") to the greeting branch. Fixed by requiring the matched phrase to be
  surrounded by spaces in the folded text, confirmed by a regression test
  (`test_unrelated_topics_route_to_out_of_scope`).
- Uses a **bilingual VI/EN glossary** (`GLOSSARY`) for topic-specific terms, because most stored chunk
  content is English-language source text while users ask in Vietnamese — a Vietnamese-only keyword list
  would never find anything to match downstream in the Evidence Gate either.
- Separates a narrow **ASD anchor** list (`tự kỷ`, `autism`, `asd`, `asperger`, …) from the broader
  glossary, so that domain-signal detection isn't polluted by overly generic clinical words.

## Required edge cases (tested, `tests/unit/test_intent_classifier.py`)

| Case | Result |
|---|---|
| Pure greeting ("Xin chào!", "Hello") | `greeting` |
| Thanks / farewell | `greeting` (sub-kind recorded) |
| Unrelated topic (weather, gold price, food preference) | `out_of_scope` |
| Empty / whitespace-only message | `out_of_scope` |
| No diacritics at all ("Tieu chuan DSM-5 cho tu ky gom nhung gi?") | `asd_question` |
| English phrasing ("What is autism spectrum disorder?") | `asd_question` |
| No literal "tự kỷ"/"autism" but a clinical ASD-adjacent term (risperidone dosing) | `asd_question` |
| Mixed EN/VI, typo-ish casing ("...có phải bị asd không ạ?") | `asd_question` |
| Long multi-clause, multi-topic question | `asd_question` |
| Mixed intent — greeting word *and* a real question in the same message | `asd_question` (the real question wins; verified live with `"Chào bạn, tự kỷ được chẩn đoán như thế nào?"`, which correctly proceeded to retrieval rather than being answered as a greeting) |
| Single short token ("ASD?") | `asd_question` |

## Stated limitation

This is a deterministic lexical classifier, not a trained model or an LLM (none is authorized — T2.6).
It will misroute genuinely novel phrasings that share no vocabulary with the curated anchor/glossary lists
and are not greetings either (they fall to `out_of_scope`, the conservative default — never silently
treated as an ASD question with fabricated relevance). Expanding glossary coverage is the main lever for
improving routing recall over time; this is explicit, cheap, low-risk work (adding dictionary entries), not
a redesign.

## Tests

`tests/unit/test_intent_classifier.py` — 15 tests, all passing (see `phase_6_test_report.md` for the full
run). No change to `app/retrieval/*`, `config/embedding_profiles.json`, or the T2.3 benchmark path.
