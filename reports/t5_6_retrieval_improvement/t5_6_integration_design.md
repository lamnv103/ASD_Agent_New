# T5.6 Phase 4 — Integration Design (proposal only; `app/api.py` not modified)

## Required flow, as specified by the task

```
Cache lookup → Cache miss → Retrieval → Evidence Gate → Vietnamese Answer Generation
             → Citation Validation → Final Answer
```

## The key design insight this task found: templates are gated by (query term + source_id), not by score

Re-reading `app/answer/answer_generator.py`'s `_template_for()`/`_new_template_for()` (Phase 0, re-
confirmed): every one of the 17 templates fires based on (a) the query containing a specific glossary
term and (b) a matching `source_id` being present among the *supported* evidence. **Neither check reads
`cosine_similarity` or any dense-only field.** This means a `RetrievedChunk`-shaped object built from an
FTS hit, carrying the right `source_id`, would make the *exact same* template fire, producing the *exact
same* structured Vietnamese answer with citations — no new template code is needed for any question whose
topic already has a template, regardless of whether the evidence came from dense or FTS. This is the
single most important design conclusion of this phase, and it directly serves the Answer Quality
Reference: for a subset of cache-miss questions, the structured-Vietnamese-answer requirement is already
solvable with zero new template logic — only a retrieval-and-adaptation layer, not more Python answer
strings.

## Proposed component: an `FtsEvidenceAdapter`

A new, additive module (not sketched as a diff to any existing file) that:

1. Takes an `FtsHit` (from `app/retrieval/fts.py`, unmodified) and produces a `RetrievedChunk`-compatible
   object, filling the fields the Evidence Gate and answer generator actually read (`source_id`, `title`,
   `section`, `content`, `chunk_id`) and setting `cosine_similarity` to a **conservative, explicitly
   synthetic placeholder** — not a real similarity score, since none exists for a lexical hit. Two options,
   neither implemented in this task, both named so a future task does not have to rediscover them:
   - **Option X (binary pass)**: set `cosine_similarity` to exactly `evidence_gate.MIN_SIMILARITY` (the
     existing floor) whenever the hit's own term-match classification (direct/indirect, reusing
     `app.nlp.text_match`) is at least "indirect," and refuse to adapt a "generic"/"none" hit at all —
     i.e., FTS hits never pass the Gate on similarity-floor grounds alone, only on the SAME term-specificity
     logic the Gate already applies to dense hits, just computed up front instead of inside `assess()`.
   - **Option Y (rank-derived)**: normalize `ts_rank_cd` into the gate's similarity range via a fixed,
     documented mapping — rejected as the weaker option in this design, because `ts_rank_cd` and cosine
     similarity measure fundamentally different things (lexical density vs. semantic distance) and mapping
     one onto the other's numeric range risks implying a false equivalence the Evidence Gate's own
     module docstring explicitly warns against ("cosine similarity alone cannot catch this").
   - **This design recommends Option X** specifically because it reuses, rather than reinvents, the exact
     term-specificity check already validated (if imperfectly — see `t5_6_failure_analysis.md`'s Failure
     1/2) throughout this project, and because it never lets a purely-generic FTS hit through on the
     strength of a fabricated similarity number.

2. Runs **EXP-1b's query composition** (`t5_6_fts_experiments.md`'s addendum: EXP-1's anchor-excluded
   pair-AND, plus an anchor-concept-only fallback when zero non-anchor concepts are detected), not
   baseline FTS-C, as the source of candidate hits — justified by Phase 2's finding that EXP-1 removes the
   dominant OR-dilution failure mode with no regression on the 6 frozen-set spot-checks, and that the
   EXP-1b fallback is specifically needed to serve purely-generic questions like the task's own "ASD là
   gì?" reference example (verified end-to-end in `t5_6_answer_quality_evaluation.md`).

## Proposed pipeline (where each existing module plugs in, nothing renamed or rewritten)

```
1. Cache lookup           CachedQueryEmbedder (UNCHANGED)
2. Cache miss              -> today: raises QUERY_NOT_CACHED, request ends here
                            -> proposed: fall through to step 3 instead of ending here
3. Retrieval (NEW path)    FtsRetriever(fts_c_glossary_or_v1-derived EXP-1 composition)  [NEW, isolated]
                           -> FtsEvidenceAdapter -> RetrievedChunk-shaped list           [NEW, isolated]
4. Evidence Gate           evidence_gate.assess()  (UNCHANGED — now receives adapted chunks too)
5. Vietnamese Answer Gen   answer_generator.generate()  (UNCHANGED — same 17 templates + fallback)
6. Citation Validation     citation_validation.validate()  (UNCHANGED)
7. Final Answer            response, now carrying an explicit "evidence_source: lexical_search" flag
                           not present today, so the frontend/response can disclose lower-confidence
                           provenance per the task's Answer Quality Reference (never silently presenting
                           FTS-sourced evidence as if it were dense-retrieved)
```

**No step 4/5/6 module is modified.** The only new code is step 3 (retrieval) and the adapter between 3
and 4. `app/api.py` is not touched by this design — wiring it in would be a future task's job, after this
proposal is reviewed; this task only designs it.

## What this design does and does not close, against the Answer Quality Reference

- **Closes**: every cache-miss question whose topic already has a live template AND whose EXP-1 hits land
  on that template's trigger source — confirmed this task for `ie019`/`ie020` (vaccine_myth),
  `ie025`/`ie031` (adolescence_asd), and (on the frozen set) `q057` (vaccine_myth). For these, the
  proposed flow would produce the *same* structured Vietnamese answer with concept, characteristics, and
  citations the Answer Quality Reference asks for — not a new answer, the existing one, now reachable
  from previously-unreachable phrasings.
- **Does not close**: questions with no existing template at all, regardless of retrieval quality — e.g.
  `ie001`'s "is ASD the same as ADHD" framing has no dedicated template today; even perfect retrieval of
  the comorbidity papers would fall to `extractive_fallback` (raw English excerpts), not a structured
  Vietnamese answer, because the *answer text itself* does not exist as Vietnamese prose anywhere in the
  codebase for that specific question shape. Closing this requires either a new template (explicitly
  discouraged as the primary fix by this task's own framing, "tạo nền tảng... không chỉ mở rộng Answer
  Templates một cách máy móc") or an authorized LLM (T2.6, not revisited here). This gap is stated
  plainly, not glossed over, in `t5_6_answer_quality_evaluation.md`'s per-question findings.
- **Does not close**: the `extractive_fallback` mode's raw-English-excerpt honesty problem — an
  FTS-sourced fallback would have exactly the same property as today's dense-sourced fallback (English
  excerpts, clearly labeled, never silently presented as Vietnamese prose). This design does not propose
  machine-translating excerpts, since that would need either a translation API (external, unauthorized) or
  an LLM (same).

## Risk, cost, and rollback for this proposed integration (not implemented)

- **Risk**: FTS's known false-positive mode (`t5_6_failure_analysis.md`'s Failure 1) could let a
  template fire on a wrong source if that source happens to be what EXP-1 (imperfectly) returns for an
  over-broad concept match — e.g. a future `aba_intervention` false-fire is conceivable if a question's
  only recognized concept is `can thiep`. Mitigation: Option X's conservative all-or-nothing similarity
  floor, plus the existing per-template source-ID gate, which still requires the *specific* trigger
  source to be present, not just any evidence.
- **Cost**: implementation effort for the adapter + a new retrieval branch; zero new external-service cost
  (FTS needs no embedding).
- **Rollback**: a feature flag, same `_flag()` pattern as `ENABLE_LIVE_*`, defaulting `False` — disabling
  it returns exactly to today's behavior, since the new path is purely additive on top of a cache-miss
  that today ends the request immediately.
