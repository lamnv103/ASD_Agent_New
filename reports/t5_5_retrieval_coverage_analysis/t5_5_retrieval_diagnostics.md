# T5.5 Phase 2 — Retrieval Diagnostics

## What was run, and what was not

- **Dense retrieval**: NOT run on any of the 31 independent-set questions, because none of them are
  cached and live Cohere embedding is not authorized (T2.6). This is a hard tooling limit, not a choice.
  Dense retrieval WAS re-confirmed working correctly on its existing cached cohort (454/454 tests, T2.3's
  66/66 regression — see T5.4's `regression_report.md`), so this phase's findings are about *coverage*,
  not about dense retrieval being broken.
- **FTS (3 profiles: A/B/C)**: run live, read-only, via `app/retrieval/fts.py`, against all 31 questions,
  top-10 each (`scripts/t5_5_fts_diagnostics.py`, output `eval/reports/t5_5_fts_diagnostics.json`).
- **Direct `content ILIKE` keyword search**: run for a targeted set of ambiguous cases, bypassing FTS's
  tsquery AND/OR construction entirely, as an even more permissive (recall-maximizing) check for whether
  a keyword appears anywhere in the corpus at all.
- **No embedding was generated, cached, or sent to any external API at any point in this phase.**

## Dense vs. FTS — relative strengths and weaknesses, re-confirmed on this new question set

| Property | Dense (cache-only) | FTS (A: raw VI / B: glossary AND / C: glossary OR) |
|---|---|---|
| Needs an embedding | Yes — the whole reason this task exists | No — pure PostgreSQL `tsvector`/`tsquery` |
| Works on brand-new text | **No**, unless cached | **Yes**, always (DB-only) |
| Cross-lingual (VI question → EN corpus) | Handled implicitly by the embedding model's semantics (no explicit term mapping) | Handled only by an explicit glossary (A has none and returns **0/31** results on raw Vietnamese text, confirming T2.4's finding generalizes to brand-new questions, not just the original 66) |
| Precision on a known, cached, well-formed question | High (T2.3: Recall@20 0.646 original / 0.716 merged labels, exploratory) | Lower and noisier; B found genuinely on-topic content for roughly a third of the 31 (the 11 category-3 cases); C is frequently swamped by generic terms |
| Known failure mode | Cache-text-exact-match only; no semantic nearest-neighbor fallback | **AND-loss**: combining too many glossary concepts with AND silently returns 0 or near-0 results (`ie004`, `ie012`, `ie013`, `ie029` all returned 0 via FTS-B in this task, each for a different combination of concepts); **OR-dilution**: FTS-C frequently returns the *same two generic, high-document-frequency chunks* regardless of the actual question (`ASD-OA-PMC4742252` "Elopement" and `ASD-CSV-062` "Comorbid ADHD and Anxiety" appeared as FTS-C's top-2 for 14 of the 31 questions in this run, including ones with no topical connection to either paper — e.g. `ie010`, a pure greeting) |
| Vocabulary sensitivity | Lower (embeddings are somewhat robust to paraphrase) | **High** — `ie027` ("ăn ít rau củ quả", eats few vegetables) returned nothing useful from FTS/glossary even though the corpus has 48 chunks matching "food selectivity" directly, because the question's phrasing never triggered the `"ken an"` glossary key, which expects the more clinical Vietnamese phrase "kén ăn" |

## Synonym / phrasing effects, specifically observed this task

1. **Exact-string cache keying (dense) is the dominant effect.** Every one of the 31 questions is a
   *paraphrase* of a topic the corpus plausibly covers; none of the 31 is word-for-word identical to any
   of the 171 already-cached queries (the 105-set + the old 66-set). A single punctuation or word-order
   change is enough to produce a cache miss, regardless of how semantically close the new text is to an
   already-answered question. This is the largest single factor behind the 50/105 and 31/32 cache-miss
   rates reported in T5.4 — not retrieval quality, not corpus content.
2. **FTS's AND-over-many-concepts construction loses recall fast as sentence complexity grows.**
   `ie012` (a genuine 3-part question: signs + where to seek help + intervention) collapsed FTS-B to a
   single, likely-unrelated hit. This reproduces the T2.4 architecture audit's finding ("AND trên cả câu
   làm mất kết quả") on entirely new text, confirming it is a structural property of the AND query mode,
   not an artifact of the original 66-question set's specific wording.
3. **Vietnamese-English token mismatch remains total for FTS-A.** 0/31 raw-Vietnamese FTS-A queries
   returned any result, exactly reproducing the 0/66 finding from T2.4. This is not new information, but
   its exact reproduction on fully independent text is itself a useful confirmation that the original
   finding was a property of the PostgreSQL configuration (no Vietnamese `tsconfig`, no `unaccent`), not
   an artifact of those particular 66 questions.
4. **Generic, high-frequency clinical vocabulary ("can thiệp"/intervention, "treatment") produces false
   "direct" matches.** The term-matching heuristic reused from `app/nlp/text_match.py` (the same one the
   live Evidence Gate uses) marked an irrelevant sensory-integration-therapy chunk as "direct" evidence
   for `ie002` (a comorbidity-intervention-priority question) purely because both contain the word
   "intervention." This is the exact limitation the Evidence Gate's own module docstring already
   discloses ("cannot resolve... a topically-adjacent-but-wrong condition... when both conditions happen
   to share the queried specific term") — re-confirmed here as a live, reproducible false-positive, not a
   hypothetical.
5. **A small number of English-source technical terms and codes, when present verbatim in the Vietnamese
   question, help FTS regardless of glossary coverage.** `ie028` ("ADHD") surfaced the dedicated
   `NIH-NIMH-MEDICATIONS` source via FTS-C precisely because "ADHD" is written the same way in both
   languages and needs no translation — the acronym passes through `plainto_tsquery` unchanged and
   happens to co-occur with medication content. This mirrors the T2.4 audit's finding that acronyms
   (`ADHD`, `ASD`, `DSM-5`) are the one class of term that survives FTS's English-only configuration
   without glossary help.

## Why this cannot be reported as an official Recall@K

No independently-adjudicated relevance label exists for any chunk against any of these 31 questions —
they are brand new, created this task's predecessor (T5.4), specifically to be *independent* and were
never submitted for annotation. Reporting a Recall@K number here would be inventing a ground truth this
task does not have, which the task's own instructions explicitly forbid ("Không được tự đặt số liệu để
lấp khoảng trống" / "Không tuyên bố kết quả retrieval là Recall@K chính thức"). The classifications in
`t5_5_cache_miss_taxonomy.md` are therefore phrased as qualitative findings ("FTS found a direct hit on
the same source an existing template already uses"), not as a quantitative benchmark score. A path to a
real, labelled benchmark for this new question set is proposed in `t5_5_benchmark_proposal.md`.
