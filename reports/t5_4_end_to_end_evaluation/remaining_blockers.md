# T5.4 — Remaining Blockers

Carried forward and consolidated from Phases 1–6. None of these were fixed in this task, either because
they are not code defects (they are architecture/dataset-coverage limitations by design) or because they
were already known, open items from prior tasks that this task's read-mostly mandate does not license
fixing without a new, explicit authorization.

## 1. Cache-only coverage is narrow (T2.6 architectural constraint, not a bug)

- 50/105 (47.6%) of the content-eval set and 31/32 (96.9%) of the brand-new independent set are cache
  misses. The independent-set number is the more honest measure of real-world coverage, since the
  105-set's vocabulary was partly tuned after seeing it (disclosed test-set leakage from T5.1/T5.2).
- **Why not fixed**: fixing this requires either (a) a compatible local query encoder (T2.5 found
  `NO_COMPATIBLE_LOCAL_ENCODER_FOUND`) or (b) live Cohere query embedding (T2.6, `APPROVAL_REQUIRED`,
  never to be changed without new explicit authorization). Neither is available to this task.

## 2. `q033`/`qe033` — ADHD-confusion case, documented, unfixed

- `qe033` ("Tự kỷ ở trẻ gái có biểu hiện gì khác so với trẻ trai?") returns `extractive_fallback` (English
  excerpt) rather than a synthesized answer; this is consistent with — not a regression of —
  `tests/integration/test_chat_api_db.py::test_q033_adhd_confusion_is_still_present_and_unfixed_in_this_
  task` and `tests/unit/test_q033_isolation.py`, both of which exist specifically to document this as a
  known, accepted limitation rather than silently drifting.

## 3. `qe034` — speech-delay-vs-ASD, fallback only

- Still `extractive_fallback`, not a dedicated template, consistent with every prior T5.x report. The new
  independent-set question `ie006` (a no-diacritic rephrasing of the same underlying question) cache-
  missed entirely rather than reaching even the fallback — a slightly worse outcome for that specific
  phrasing, illustrating that the cache-miss gap, not the fallback quality, is the dominant real-world
  risk for this topic.

## 4. Zero live age-mismatch demonstration in the current cache (new finding, this task — Phase 3/4)

- No cached question in either the 105-set or the 32-question independent set triggers a true
  age/population mismatch between a query's stated age and its cited evidence's age. The mechanism
  itself (`app/retrieval/evidence_gate.py`'s `age_mismatch` field) is confirmed live-functional via its
  existing unit tests (re-run this task, all passing), so this is a **dataset-coverage gap**, not an
  unverified or dead code path. Closing it would require adding a new cached query/evidence pair
  specifically engineered to mismatch — out of scope for a read-mostly audit task.

## 5. No topics beyond the 17 templates + fallback (new finding, this task — Phase 5)

- Three independent-set topics have no dedicated coverage at all and correctly fall through to cache-miss
  rather than being forced into an ill-fitting template: adolescent sex education (`ie024`), adult
  ASD/marriage/parenting (`ie026`), and culturally-specific Vietnamese folk-belief myths about ASD causes
  (`ie018`, e.g. "trúng gió"/"vong theo"). This is reported as a coverage gap, not a defect — the system
  correctly declines rather than guessing on all three.

## 6. No ASD-expert (clinical) review has occurred at any point in this project

- Every evaluation to date, including this task's, has been done by an AI agent re-reading source text
  and code, never by a qualified clinician or ASD-domain expert. All claim-level accuracy findings in
  this and prior reports should be read with that caveat; none of them substitute for expert sign-off.

## 7. 0 human-verified labels in the underlying retrieval benchmark

- `reports/demo_mvp/dense_retrieval_regression_metrics.json`'s own `label_tier` field states
  `"silver_single_annotator (0 human-verified)"` — unchanged this task, re-confirmed in the Phase 6
  regression diff. This is a pre-existing, disclosed limitation of the T2.3 benchmark, not something this
  task could address.

## Status of each: all **open**, none fixed this task, none requiring a code fix within this task's
mandate (no severe reproducible defect was found — see Phase 1–5 conclusions). All are forwarded as
input to any future task.
