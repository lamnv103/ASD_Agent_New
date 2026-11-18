# T5.7 Phase 1 — FTS Precision Audit

Per instruction: **a term is never removed just because it appeared in one false positive** — each case
below is analyzed for meaning and context before any conclusion is drawn.

## 1. The generic "autism" anchor concept — re-confirmed, context examined

`autism`/`asd_full` are necessary, correct glossary entries: almost every real ASD question legitimately
mentions "tự kỷ"/"ASD," and removing the trigger would break glossary expansion entirely, not just the
false-positive cases. **The problem is never the concept's presence; it is using it as a discriminating
signal when the question has no other topic-specific concept.** T5.6's EXP-1 already drew this
distinction correctly (exclude from scoring, not from the glossary). This audit's contribution is finding
one more place the same problem hides (see §4).

## 2. The `can thiep` → "treatment"/"intervention" mapping — context-dependent, not a blanket defect

**Context where it is correct and necessary**: any question specifically about ABA, NDBI, parent-mediated
intervention, or early intervention legitimately needs "intervention"/"treatment" as an English pivot —
there is no narrower single English word that covers the Vietnamese "can thiệp" across all of this
corpus's intervention-related sources. Removing it would break `aba_intervention`, `ndbi_intervention`,
and the `WHO-CST` caregiver-training template's own FTS discoverability.

**Context where it misfires**: `ie002` (comorbidity-priority) and `ie028`-adjacent cases, where the
question's *actual* topic is something else (comorbidity care prioritization) and "can thiệp" is
incidental phrasing ("ưu tiên can thiệp bên nào" — "which intervention to prioritize" — the question is
about *prioritization*, not about identifying a specific intervention). **The defect is not the term, it
is that the query-composition logic cannot distinguish "the question is ABOUT an intervention" from "the
question MENTIONS intervention in passing while asking something else."** This is a scope/disambiguation
problem, not a vocabulary problem — re-stated here more precisely than T5.6's framing ("over-broad
mapping"), because the fix is not to narrow the term (which would break the legitimate cases) but to
require a stronger co-occurrence signal specifically when `can thiep` is one of only two detected
concepts and the other concept (here, `adhd`) is not itself intervention-related.

**Recommendation**: do not remove or narrow `can thiep`. Flag it (and any future term found to have the
same property) as "requires a second corroborating concept, not sufficient alone even when paired" — a
refinement for a future glossary-metadata schema (see `glossary_validation.md`'s proposed structure),
not a removal.

## 3. `chua noi` — re-examined in context

TM's mapping (`["not talking", "no words", "speech delay"]`) is specific and was not found to misfire in
this task's testing. QG's same-folded-key concept (`talk`, mapping to `["speak", "speech", "talk",
"talking", "words"]`) is broader and was flagged in T5.6 as a risk, but this task's Phase 3 testing found
no concrete misfire traceable to it among the 22 end-to-end test questions — the risk is real in
principle (a bare word like "talk" could match almost any communication-related chunk) but this audit did
not find a live reproduction of it causing a wrong *template* fire (the per-template source+term gate
still held in every tested case — see `end_to_end_evaluation.md`). **Downgraded from "confirmed defect" to
"plausible risk, not yet reproduced"** — stated honestly rather than carried forward as settled.

## 4. New finding this task: a bare, short acronym term causes the same problem as the anchor concept,
regardless of which glossary concept it is filed under

**Discovered while re-verifying T5.6's own "ASD là gì?" result** (`baseline_audit.md`, §5). The
`asd_full` concept's term list is `["autism spectrum disorder", "ASD"]`. When this concept's terms are
OR'd in without distinguishing the multi-word phrase from the bare acronym, the bare "ASD" token alone —
being 3 characters, extremely common, and sometimes repeated many times within a single chunk — inflates
`ts_rank_cd`'s cover-density score for chunks that are acronym-dense (quantitative tables, prevalence
papers that write "ASD" dozens of times) rather than chunks that are actually substantively *about* ASD
as a concept.

**Verified directly**: a tsquery of `('autism' <-> 'spectrum' <-> 'disord')` alone (the connected phrase,
no bare acronym) ranks `CDC-ASD-CLINICAL` (the live `asd_definition` template's own primary source) at
rank 1 of 8 matches. Adding `| ('asd')` to that same query changes the top-3 to the familiar generic
boilerplate pair (`ASD-OA-PMC4742252`, `ASD-CSV-062`) plus `ASD-CSV-078` — the exact same failure pattern
T5.6 found with the "autism" anchor concept, now shown to also apply to a bare acronym term filed under a
*different* concept (`asd_full`, not `autism`).

**Is this a reason to remove "ASD" from the glossary? No — explicitly not**, per this phase's governing
instruction. "ASD" is essential: many real Vietnamese questions use the bare acronym (e.g. "ASD là gì?,"
"ASD và ADHD khác nhau"), and the term must stay recognized. **The fix is structural, not lexical**: when
building a fallback query that relies on a concept alone (no other concept to corroborate it — the exact
situation T5.6's EXP-1b fallback exists for), prefer that concept's multi-word phrase forms over its bare
single-word/acronym forms, since phrase adjacency (`phraseto_tsquery`) is inherently more specific than a
single common token. This is implemented and verified in this task's harness (`scripts/
t5_7_e2e_harness.py`'s "EXP-1c" refinement) and re-confirmed not to regress the 6 frozen-set spot-checks
(none of them rely on the anchor-only fallback branch at all, since all 6 have 2+ non-anchor concepts —
re-verified this task, same finding T5.6 already established for EXP-1b).

## 5. AND/OR query modes, Vietnamese diacritics, no-diacritics, synonyms, multi-topic queries — re-confirmed, no new finding beyond T5.6/T2.4

- AND-loss and OR-dilution: re-confirmed present in baseline FTS-B/FTS-C exactly as T5.6 described; EXP-1/
  EXP-1c's pair-AND composition remains the mitigation, re-verified working on this task's new 22-question
  set (§ below) in addition to the original 31+6.
- Diacritics/no-diacritics: still irrelevant to FTS-A (0 results either way); still irrelevant to the
  glossary-expansion modes, since `Glossary.expand()` already handles both forms via `strip_accents()`
  (re-read this task, unchanged since T2.4).
- Synonyms: no new finding; American/British spelling pairs remain present in the glossary's own term
  lists where relevant, unchanged.
- Multi-topic (multi-intent) queries: re-confirmed EXP-1c's pair-AND still only covers 2 concepts at a
  time (an OR of pairs, not of triples+) — a genuinely 3-concept question (like T5.5's `ie012`) still gets
  partial coverage at best; not solved by EXP-1c, consistent with T5.6's own disclosed limitation.

## 6. Summary — what changed vs. T5.6, and what did not

| Term/mechanism | T5.6's finding | This task's refinement |
|---|---|---|
| `autism`/`asd_full` as concepts | exclude from scoring when other concepts exist | **unchanged** |
| bare acronym term ("ASD") inside the anchor-only fallback | not distinguished from the phrase form | **new fix**: fallback uses phrase forms only |
| `can thiep` | "over-broad, causes a false positive" | refined: context-dependent, needs a corroboration rule, not removal |
| `chua noi` | "flagged as a scope mismatch risk" | downgraded to "plausible, not reproduced this task" |
