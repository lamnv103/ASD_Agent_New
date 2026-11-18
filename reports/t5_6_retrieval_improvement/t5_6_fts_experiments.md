# T5.6 Phase 2 — FTS Improvement Experiments

All experiments live in a single new, isolated file: `scripts/t5_6_fts_experimental.py`. It imports but
does not modify `app/retrieval/fts.py`, `config/fts_profiles.json`, or either glossary file. **Rollback is
deleting this one file** — nothing else in the codebase references it.

## What was tested

1. **AND-loss** — re-confirmed present (T2.4/T5.5's finding reproduces): FTS-B's full-AND composition
   returned 0 results for `ie004`, `ie012`, `ie013`, `ie029` (4/31) in this task's own re-run.
2. **OR-dilution** — re-confirmed and, this task, root-caused precisely: FTS-C's full-OR composition
   always includes the generic ASD-anchor concepts (`autism`→"autism"/"autistic"/"ASD",
   `asd_full`→"autism spectrum disorder"/"ASD") alongside every specific concept, because
   `config/query_glossary_vi_en_v1.json`'s `generic_not_expanded` list only filters Vietnamese filler
   words ("trẻ", "là gì", ...), never filters a *concept*. Since nearly every chunk in an ASD corpus
   contains the word "autism," and PostgreSQL's `ts_rank_cd` rewards chunks where many OR'd terms cluster
   densely, two specific chunks (`ASD-OA-PMC4742252` "Elopement," `ASD-CSV-062` "Comorbid ADHD and
   Anxiety") that happen to be dense in generic ASD/comorbidity vocabulary dominate the top-2 ranks for
   **27 of the 31** independent-set questions regardless of actual topic (re-measured this task,
   `eval/reports/t5_6_fts_experiments.json`'s `baseline_c_top2_sources` field) — a stronger, more precise
   statement than T5.5's qualitative "14 of 31" estimate, which only checked the top-2 by eye for a subset.
3. **Vietnamese diacritics / no-diacritics** — re-confirmed no difference: FTS-A (raw Vietnamese,
   diacritic or not) returns 0/31 either way, unchanged from T5.5/T2.4.
4. **Synonyms (American/British spelling, singular/plural)** — already partially handled inside the
   existing glossary's own term lists (e.g. `behavior`/`behaviour` both listed per concept where relevant)
   and by PostgreSQL's Snowball stemmer for simple plurals; no new synonym-handling code was needed to
   observe this, it was confirmed by reading the existing glossary entries' English term lists directly.
5. **ASD-specific phrase handling** — re-confirmed `phraseto_tsquery` vs `plainto_tsquery` behavior is
   unchanged from the T2.4 audit (a cross-checked fact, not re-derived with new experiments this task,
   since T2.4 already established this precisely and nothing in the code has changed).
6. **Long, multi-intent queries** — tested directly as EXP-1 below.

## Experiment 1 (EXP-1): anchor-excluded, min-2-concept pair-AND

**Design**: drop the two generic anchor concepts (`autism`, `asd_full`) from the OR expansion entirely
(they add no discriminating signal — every row already satisfies them), then require matching queries to
satisfy an OR of AND-pairs over the *remaining* specific concepts (falls back to a plain OR over a single
concept's own term variants when fewer than 2 specific concepts were detected).

**Result on the 31-question cache-miss set** (`eval/reports/t5_6_fts_experiments.json`):

| Outcome | Baseline FTS-C | EXP-1 |
|---|---:|---:|
| Top-2 dominated by the generic boilerplate pair (`ASD-OA-PMC4742252`/`ASD-CSV-062`) | **27/31** | **0/31** |
| Returns 0 results (honest "no signal" rather than noise) | 0/31 | 7/31 (`ie010`, `ie011`, `ie021`, `ie022`, `ie026`, `ie027`, `ie029`) |
| Top result changes to a plausible, differently-sourced chunk | — | 24/31 |

**Specific wins, cross-checked against known-correct sources from T5.5/the live templates**:
- `ie019` (named-vaccine question): baseline top-2 = boilerplate; EXP-1 top-2 = `ASD-OA-PMC12620806`
  (the exact source behind the live `vaccine_myth` template) — a clean, verified improvement.
- `ie030` (longitudinal monitoring narrative): baseline top-2 = `WHO-CST-PARTICIPANTS-2022`/
  `ASD-CSV-084` (unrelated caregiver-training/AAC content); EXP-1 top-2 = `CDC-MILESTONES-04`/
  `ASD-CSV-089` — `CDC-MILESTONES-04` is plausibly on-topic for a "should I still be worried" monitoring
  question, a genuinely better candidate than baseline's.
- `ie025`/`ie031` (puberty questions): EXP-1 surfaces `ASD-OA-PMC12468522` (the adolescence_asd
  template's own source) at rank 1, matching this task's T5.5 finding exactly.

**Specific limits, stated honestly**:
- `ie002` (comorbidity-priority question): even EXP-1 still surfaces `NIHR-SENITA-2022` (an unrelated
  sensory-integration paper) at rank 1 — the `can thiep`→"treatment"/"intervention" over-broad mapping
  identified in `t5_6_glossary_reconciliation.md` still causes a false pairing even after removing the
  anchor-concept noise, because the false signal here comes from a *different* overly generic concept,
  not the anchor. Anchor-exclusion alone does not fix every instance of OR-dilution.
- `ie027` (food selectivity, phrased without the glossary's trigger word): returns 0, same as baseline —
  EXP-1 is a ranking/composition fix, not a vocabulary fix; it cannot find content the glossary has no
  trigger for at all (this is `t5_6_glossary_reconciliation.md`'s problem to solve, not Phase 2's).

### Regression check against the frozen 66-question set's 6 mandatory/notable cases

| Question | Baseline FTS-C top-2 | EXP-1 top-2 | Verdict |
|---|---|---|---|
| `q066` (epilepsy) | `ASD-OA-PMC12620806` (already good) | same, reinforced (3/3 top ranks) | **no regression** |
| `q057` (vaccine) | boilerplate (`ASD-OA-PMC4742252`/`ASD-CSV-062`) | `ASD-OA-PMC12620806` (correct) | **improved** |
| `q033` (parent-mediated) | `ASD-CSV-017`/`ASD-CSV-084` | `ASD-CSV-089` ("Parent-Mediated Intervention Training") | **plausibly improved** — `ASD-CSV-089`'s title is a more precise match than either baseline source |
| `q054` (home vs. school) | `ASD-NEW-002`/`ASD-CSV-089` | `ASD-NEW-002` (reinforced, same source) | **no change** — consistent with T2.4's own finding that this question has no real corpus answer regardless of method |
| `q063` (echolalia) | already good (`NIH-NIDCD-ASD-COMMUNICATION-2020`/`CDC-ASD-SIGNS`) | unchanged | **no regression** |
| `q016` (joint attention) | already good | unchanged | **no regression** |

**No regression found on any of the 6 cases T2.4 specifically studied.** Two cases plausibly improved,
none got worse.

## Experiment 2 (EXP-2): post-hoc term-specificity filter

**Design**: run FTS-B/C unchanged, then drop any returned hit that the existing `app.nlp.text_match`
term-matching logic (the same logic the live Evidence Gate already uses) would classify as
"generic"/"none" for the query's own specific terms — i.e., require the hit to actually, lexically
contain the specific term the user asked about, not just satisfy the broader tsquery.

**Result**: much higher precision, much lower recall than EXP-1. On the 31-question set, EXP-2 reduces
results to 0 for **14/31** questions (vs. EXP-1's 7/31) — including some cases EXP-1 still found something
useful for (`ie006`, `ie013`, `ie014`, `ie017`, `ie018`, `ie019`, `ie023`). Where EXP-2 does return results,
they are consistently tighter: `ie015` (melatonin) narrows from 10 boilerplate-mixed hits to exactly 2,
both `ASD-OA-PMC7407189` — the correct source, with zero noise.

**Why EXP-2 under-performs EXP-1 on recall**: it depends entirely on `app.nlp.text_match.specific_terms()`
recognizing the query's term, which is the *narrower* (63-entry) glossary — and, per
`t5_6_glossary_reconciliation.md`, that glossary is missing several terms (`cure`, `co_occurring`, etc.)
the FTS-side glossary already has. EXP-2 also failed on `q057` in the regression check (returned 0)
specifically because `specific_terms()` did not recognize "Vắc-xin" (with a hyphen) as matching its own
`"vac xin"` key — a tokenization edge case in the *existing, unmodified* TM glossary matching logic that
this task's experiment surfaced but did not fix (fixing `app/nlp/text_match.py` would not be an isolated,
rollback-only change; it is excluded from Phase 2's scope for that reason).

## Addendum — EXP-1b, a fallback found while validating Phase 5, folded back in here for completeness

Phase 5's answer-quality testing surfaced a real blind spot in EXP-1 (also documented as Failure 3 in
`t5_6_failure_analysis.md`): when a query contains **no** non-anchor concept at all (e.g. "ASD là gì?" —
a purely generic ASD question), EXP-1 returns 0 results, because it deliberately excludes the anchor
concept from scoring. But a purely generic question is exactly the case where searching the anchor
concept *alone* (not combined with other noise) is appropriate and harmless — there is no risk of the
anchor drowning out a specific concept, because there isn't one. Tested directly this task: a tsquery of
`( autism | autistic ) | ( 'autism spectrum disorder' )` alone (no other concept OR'd in) ranks
`CDC-ASD-CLINICAL` at position 4 of 8 matching chunks (`ts_rank_cd` 13.8) — close enough to the top that,
once adapted into evidence (see `t5_6_answer_quality_evaluation.md`), the live `asd_definition` catch-all
template fires correctly end to end. **EXP-1b = EXP-1, plus: when zero non-anchor concepts are detected,
search the anchor concept alone instead of returning empty.** This is still an experiment, not a
production change, and is evaluated only for the one question it was found on plus the regression set
below — not claimed to generalize further than that.

### Regression check for EXP-1b on the same 6 frozen-set cases

Adding the anchor-only fallback cannot change behavior for any of the 6 mandatory cases (`q066`, `q057`,
`q033`, `q054`, `q063`, `q016`), because all 6 already have 2+ non-anchor concepts detected and never hit
the zero-concept fallback branch — re-confirmed by inspecting each case's `expansion.concepts` count
(all ≥ 2). **No regression risk for this specific addition**, by construction, not merely by observation.

## Conclusion of Phase 2 — explicit anti-overfitting disclosure

**EXP-1 is the stronger, more broadly applicable of the two strategies**: it fixes the OR-dilution problem
structurally (not case by case), produces zero regressions on the 6 previously-studied frozen-set cases,
and improves at least 2 of those 6 plausibly. It does **not** fix every failure mode found in T5.5 (the
`can thiep` over-broad mapping, vocabulary gaps for unflagged terms) — this is stated explicitly so that
this task does not claim more generalization than the evidence supports. **This task does not claim EXP-1
or EXP-2 "solves" retrieval for new questions in general** — both were evaluated only against the 31
questions they were partly designed in response to, plus 6 frozen-set spot-checks; this is explicitly not
the same as a validated, independently-labeled benchmark result (see `t5_6_retrieval_comparison.md`'s own
disclosure on why no official Recall@K number is reported).
