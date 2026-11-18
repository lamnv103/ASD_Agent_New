# Remaining Blockers

## Hard blockers (require authorization this task cannot and did not grant)

1. **Live Cohere query embedding / reranking / external LLM** — T2.6 remains `APPROVAL_REQUIRED`. Still
   cache-only; `ASD_ENABLE_LIVE_*` flags default `false` and setting one `true` raises `ConfigError` rather
   than enabling anything. Not touched in this task. Needed to answer free-text questions outside the
   66-question cache.
2. **Clinical/ASD-expert content review** — none of the 7 answer templates, the Evidence Gate's topic
   vocabulary, or the safety-override wording has been reviewed by a clinician or ASD-education
   specialist. Listed in `final_project_assessment.md` §6.

## Soft limitations (not blockers — disclosed, bounded, fixable incrementally)

3. **Template coverage is partial.** Only 7 canonical topics have a hand-authored answer; everything else
   (including signs/symptoms-style questions) falls to the labeled extractive excerpt presentation. This
   is honest, not broken, but is less polished than a template for a wider demo audience.
4. **The lexical Evidence Gate cannot catch a topically-adjacent-but-wrong-condition chunk** (e.g. ADHD
   text that happens to share the queried specific term with an ASD question). Stated in
   `phase_2_retrieval_evidence_gate.md`. Needs real semantic understanding (an authorized LLM) to close
   fully.
5. **Glossary/anchor vocabulary coverage is finite.** A genuinely novel ASD-related phrasing sharing no
   vocabulary with the curated lists will be misrouted to `out_of_scope` (the conservative default, not a
   silent wrong answer, but still a missed question). Expanding the glossary is cheap, incremental work.
6. **Branch 2 vs. Branch 3 are merged** (disclosed in `phase_1_intent_routing.md`) because there is
   currently only one knowledge source. Revisit if a second, structurally different source is added.
7. **No full re-run of all 66 evaluation questions through the new pipeline** was performed in this task —
   only the specific cases named in the independent expert evaluation plus a handful of standard-topic
   checks were re-verified live. A systematic re-run (same shape as `scripts/dense_retrieval_eval.py` but
   through the Evidence Gate) would give a more complete picture of gate precision/recall across the full
   silver-labeled set, and is recommended as the next concrete task.
8. **No visual/browser test exists** for the frontend changes (Phase 5) — no JS test tooling in this
   project. `GET /` serving was verified; rendered appearance was not.

## Explicitly not blockers (addressed this task)

- `source_url` missing from `/api/chat` — fixed (Phase 4).
- Weather/off-topic question returning fabricated "ok" ASD evidence — fixed (Phases 1–2).
- Greeting routed through retrieval — fixed (Phase 1).
- Bare `C1`/`C2`/`C3` codes in answer prose — fixed (Phase 3).
- T2.3 regression — preserved at 66/66, re-verified after all changes.
