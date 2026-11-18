# T5.5 Phase 1 — Cache-Miss Taxonomy (31 independent-set questions)

## Method and its honest limit

The T5.4 independent set (`eval/datasets/independent_eval_v1.jsonl`) produced 31 cache-miss questions
(`ie001`–`ie032` minus `ie016`, which was a safety refusal, not a cache miss). For every one of these 31,
**the mechanical cause is identical and architectural, not case-by-case**: `CachedQueryEmbedder` has no
cached vector for this exact text and `inner=None` in the live app, so `app/retrieval/dense.py` is never
even called — no DB query runs, no `EvidenceAssessment` is ever produced. This single mechanical fact is
stated once here, not repeated as if it were 31 separate findings.

What the task actually requires, and what this phase answers instead, is the deeper question: **if the
dense retriever had been allowed to run on this text, what would it likely have found?** Dense retrieval
itself cannot be tested on new text without a live Cohere call (never attempted — T2.6 unchanged). So this
phase uses `app/retrieval/fts.py` (no embedding required, cache-only compliant) plus direct `content ILIKE`
corpus keyword checks as the best available proxy evidence for "does suitable knowledge exist in the
corpus," cross-checked against which sources already power the demo's 17 live answer templates (a strong
corroborating signal: if an FTS hit lands on the exact source a working template already uses for an
adjacent, already-answered question, that is strong evidence the content is real and matchable, not a
coincidence of lexical overlap).

**This method cannot prove what dense specifically would have returned.** Every classification below is
disclosed as inference from a different (lexical, not semantic) retrieval mechanism, not a measured dense
result. Where the lexical evidence is itself too noisy or absent to support a confident inference, the
question is classified as category 5, not forced into 1–4.

## The 5 required categories, applied

| # | Category (as specified) | Count | IDs |
|---|---|---:|---|
| 1 | No corresponding knowledge in the corpus | **7** | ie017, ie018, ie021, ie022, ie024, ie026, ie029 |
| 2 | Document/topic area exists, but no chunk suitable for this specific sub-question | **9** | ie001, ie003, ie005, ie006, ie013, ie014, ie023, ie030, ie031 |
| 3 | Suitable chunk demonstrably exists (found via FTS/keyword search); the live pipeline never attempted retrieval because of the cache gate | **11** | ie004, ie007, ie008, ie009, ie015, ie019, ie020, ie025, ie027, ie028, ie032 |
| 4 | Retrieval ran, but the Evidence Gate rejected the result | **0** | — (see note) |
| 5 | Cannot determine, even with FTS, due to cache-only / lexical-method limits | **4** | ie002, ie010, ie011, ie012 |
| | **Total** | **31** | |

### Note on category 4 (0/31) — an architectural finding, not an absence of effort

Category 4 requires that retrieval actually ran and the Evidence Gate actually rejected its output. For
every one of these 31 questions, **retrieval never ran at all** — the cache-only gate stops the request
one step before dense search, which is itself one step before the Evidence Gate. It is architecturally
impossible for any cache-miss question to be a category-4 case in the current pipeline. This is itself an
important finding (restated in the final report): the Evidence Gate's false-permissiveness or
false-rejection behavior (studied extensively in T5.3/T5.4 for already-cached questions) is completely
invisible to, and unaffected by, the cache-coverage problem — they are two independent failure surfaces,
and fixing one does not touch the other at all.

## Per-category rationale (detail in `t5_5_failure_examples.md` and `t5_5_retrieval_diagnostics.md`)

- **Category 1 (7)**: direct `content ILIKE` keyword checks against the full corpus (not just FTS's
  AND/OR-constrained tsquery) found **zero** substantive matches: `ie017` (vitamin-B6-as-cure claim — the
  only 2 "vitamin B6" mentions in the corpus are about B6 as a sleep-aid supplement ingredient, not a cure
  claim), `ie018` (Vietnamese folk beliefs — "folk belief"/"superstition"/"traditional belief" = 0 matches;
  this corpus is Western biomedical literature and has no reason to address a culturally-specific causal
  myth), `ie021`/`ie022` (weather/pricing — not ASD clinical topics at all; a true scope boundary, not a
  coverage defect), `ie024` ("sex education"/"sexual education" = 0 matches), `ie026` ("marriage" = 0
  matches; "relationship" = 145 but in parent-child context, not spousal), `ie029` ("hearing loss" = 6
  matches, all incidental exclusion-criteria mentions in participant tables, not substantive
  ASD-vs-hearing-impairment differential content).
- **Category 2 (9)**: the general topic area is present (e.g. comorbidity papers for `ie001`/`ie003`;
  screening/diagnostic-process content for `ie006`/`ie014`/`ie023`; the CDC screening-age content for
  `ie030`), but no single chunk squarely answers the specific angle asked (e.g. "are ASD and ADHD the same
  condition," "what should a parent do after a teacher's referral," "is this a wait-and-see case").
- **Category 3 (11)**: FTS-B (glossary-AND) or direct keyword search surfaced the **exact same source** a
  live template already uses for a closely related, already-answered question — e.g. `ie015` (melatonin)
  hit `ASD-OA-PMC7407189`, the same source behind the live `melatonin_efficacy`/`sleep_nonpharma`
  templates; `ie007`/`ie008`/`ie009` (age-specific signs) hit `CDC-ASD-SIGNS`/`ASD-NEW-001`, the same
  source family behind `signs_by_age`; `ie019`/`ie020` (named-vaccine questions) hit
  `ASD-OA-PMC12620806`, the same source behind `vaccine_myth`; `ie025` (puberty timing) hit
  `ASD-OA-PMC12468522`, the same source behind `adolescence_asd`; `ie027` (food selectivity/long-term
  health) and `ie032` (preschool inclusion) correspond to confirmed, substantial corpus content
  (`ASD-NEW-003`/food-selectivity sources, 48 ILIKE matches; `ASD-CSV-019`/school-inclusion sources,
  "preschool" 71 ILIKE matches) that FTS's own glossary/AND-construction simply failed to connect to the
  specific phrasing used. **These 11 are the strongest actionable finding of this phase**: the corpus very
  likely already has matchable content for them, and the blocker is specifically the cache-text-exact-
  match gate (and, secondarily, lexical phrasing/vocabulary gaps), not missing knowledge.
- **Category 5 (4)**: `ie002` (comorbidity intervention-priority — FTS returned only generic/false-positive
  term matches from an over-broad glossary term, `can thiệp`→"intervention"/"treatment", which appears in
  nearly every paper in the corpus and carries no real discriminating signal); `ie010`/`ie011`
  (greeting-wrapped generic ASD inquiry — FTS could not isolate any specific concept, swamped by the same
  two generic boilerplate chunks every under-specified query returns); `ie012` (3-part multi-intent
  question — FTS-B's AND-over-many-concepts construction collapsed to a single, likely-irrelevant result,
  a known AND-loss failure mode from the T2.4 audit, re-confirmed here on new text). In all 4 cases the
  lexical signal is genuinely too weak or too noisy to support a specific category-1/2/3 claim one way or
  the other.

## Direct answers to the task's required questions (repeated verbatim from the completion criteria)

1. **"Trong 31 cache miss, bao nhiêu trường hợp thực sự thiếu kiến thức?"** — **7** (category 1), with the
   caveat that 2 of those 7 (`ie021`, `ie022`) are arguably not "missing knowledge" at all but questions
   outside any ASD clinical corpus's proper scope (weather/commerce), not a defect to fix.
2. **"Bao nhiêu trường hợp có kiến thức nhưng retrieval không tìm thấy?"** — **11** (category 3) have
   demonstrable, specific corpus content (confirmed via FTS and/or direct keyword search) that the live
   pipeline never got to attempt retrieving, because the cache gate stops it first. An additional 9
   (category 2) have *adjacent* but not *precisely matching* content.
3. **"Bao nhiêu trường hợp bị Evidence Gate từ chối?"** — **0**, by architecture (see note above): the
   Gate never runs on a cache-miss question.
4. **"Bao nhiêu trường hợp chưa thể kết luận do giới hạn cache-only?"** — **4** outright (category 5,
   where even FTS/keyword diagnostics are inconclusive) — though in the strict mechanical sense *all 31*
   are "cannot determine via the live demo" since dense itself never ran on any of them; category 5 is
   reserved here for the subset where even the fallback diagnostic method (FTS) could not resolve the
   underlying question either.
