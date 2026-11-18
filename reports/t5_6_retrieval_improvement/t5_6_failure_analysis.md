# T5.6 — Failure Analysis (where the Phase 2 experiments still fail, and why)

This is not a repeat of T5.5's `t5_5_failure_examples.md` (which analyzed the *unmodified* baseline). This
analyzes specifically where **EXP-1** (the stronger of this task's two experiments) still fails, with
concrete evidence, so Phase 4's integration design does not overstate what Phase 2 actually fixed.

## Failure 1 — an over-broad glossary term survives anchor-exclusion: `ie002`

**Question**: "Con tui bị tự kỷ với ADHD cùng lúc thì ưu tiên can thiệp bên nào trước ạ?"

**EXP-1 top result**: `NIHR-SENITA-2022` (a sensory-integration-therapy qualitative study), still
unrelated to comorbidity care-prioritization.

**Root cause, confirmed in `t5_6_glossary_reconciliation.md`**: the query's only recognized concept pair
involves `can thiep`("treatment"/"intervention", generic) paired with `adhd`. Even after excluding the
two *anchor* concepts (`autism`/`asd_full`), `can thiep`'s own mapping is itself nearly as generic — it
matches almost any clinical intervention paper. Anchor-exclusion only removes the single worst offender;
it does not generalize to every overly broad concept in the glossary. **This is a glossary-content
problem (Phase 1's scope), not something a query-composition change alone can fix.**

## Failure 2 — a vocabulary gap that no ranking change can close: `ie027`

**Question**: "Tre tu ky an it rau cu qua co anh huong den suc khoe lau dai khong" (eats few vegetables,
long-term health effect)

**EXP-1 result**: 0 hits (same as baseline). The corpus has 48 chunks matching "food selectivity"
directly (confirmed in T5.5), but the glossary's `ken an` trigger expects the phrase "kén ăn," which does
not appear in this question's actual wording at all. **No query-composition strategy can retrieve a
concept the glossary never recognized the query as containing in the first place.** This is a pure
vocabulary-coverage gap, requiring either a new glossary trigger phrase (Phase 1's domain) or abandoning
glossary-gated FTS in favor of literal English-keyword matching for a wider net (a different, riskier
design not attempted here, since it would re-introduce the AND-loss/OR-dilution problem at the keyword
level instead of the concept level).

## Failure 3 — EXP-1 returning 0 is sometimes the right call and sometimes a missed opportunity, and this
task cannot always tell which

For `ie021`/`ie022` (weather/pricing questions) and `ie026`/`ie029` (confirmed category-1 corpus gaps,
per T5.5), EXP-1 returning 0 results is the *correct*, honest behavior — there is genuinely nothing to
find. For `ie010`/`ie011` (greeting-wrapped generic ASD questions), EXP-1 also returns 0 — but the
underlying information need (basic "what is autism" content) is almost certainly well-covered in the
corpus (it is the same need `qe001`/the `asd_definition` catch-all template already serves). EXP-1 cannot
distinguish these two situations, because both produce "fewer than 2 non-anchor concepts detected," and
the anchor-exclusion strategy was specifically designed to treat the anchor concept as carrying no signal
— which is correct for ranking purposes, but means EXP-1 has no way to fall back to "search for generic
ASD-overview content" when that is genuinely what the question wants. **This is a disclosed, structural
blind spot of EXP-1, not a bug**: it trades away exactly the signal (the anchor concept) that a
fallback-to-generic-content strategy would need.

## Failure 4 — EXP-2's precision comes at a steep, glossary-dependent recall cost

Already quantified in `t5_6_fts_experiments.md` (14/31 zero-result vs. EXP-1's 7/31). The specific
mechanism, not previously detailed: EXP-2's filter uses `app.nlp.text_match.specific_terms()`, which folds
and substring-matches against the 63-entry TM glossary — a glossary that, per Phase 1, is missing 59 of
the FTS-side glossary's 94 concepts entirely. Any query whose only recognizable concept lives in the
FTS-only 59 (e.g. `cure`, `co_occurring`, `developmental_delay`) will have `specific_terms()` return an
empty list, and EXP-2's filter explicitly refuses to operate with no specific term to check (returns 0
rather than guessing) — a conservative, honest design choice, but one that makes EXP-2 strictly worse than
EXP-1 for any question whose vocabulary happens to live only on the FTS side of the two glossaries.

## Failure 5 — neither experiment detects a topically-adjacent-but-wrong-granularity chunk

Carried forward from T5.5's Case C (`ie001`): the "comorbid" chunks genuinely discuss ASD+ADHD together,
satisfying every term-matching check this task has, while still not answering the specific "are they the
same condition" question. Classifying a chunk's *granularity match* to a question (statistical table vs.
definitional prose) is beyond what any lexical/term-presence method (this task's only available tool) can
do. This is restated here, not re-discovered, specifically so Phase 4's design does not imply this
problem is solved.

## Summary: what Phase 2 fixed vs. did not fix

| Problem (from T5.5) | Fixed by EXP-1? |
|---|---|
| OR-dilution (generic boilerplate domination) | **Yes**, structurally, 27/31 → 0/31 |
| AND-loss on 2+ concept queries | **Partially** — pair-AND recovers results for 3 of the 4 previously-0 cases (`ie004` improved to 8 results, `ie006`/`ie014` improved to 7 each); `ie012`/`ie013`/`ie029` remain weak or 0 |
| Over-broad single-concept mapping (e.g. `can thiep`) | **No** — `ie002` still fails |
| Vocabulary/trigger-phrase gaps | **No** — out of Phase 2's scope by design (Phase 1's domain) |
| Granularity mismatch (right topic, wrong specificity) | **No** — not solvable lexically |
| Genuine corpus-content gaps | **No**, correctly — EXP-1 returns 0 rather than fabricating relevance |
