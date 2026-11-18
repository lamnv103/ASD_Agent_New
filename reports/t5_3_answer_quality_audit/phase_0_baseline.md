# T5.3 Phase 0 — Baseline

## Preflight: code re-verified directly, not assumed from reports

Read in full before any change: `app/answer/answer_generator.py` (365 lines), `app/retrieval/
evidence_gate.py`, `app/answer/evidence_normalization.py`, `app/router/classifier.py`,
`app/retrieval/citation_validation.py`, `frontend/app.js`. Confirmed: 17 templates exist exactly as
T5.2's reports describe (7 old, fixed-text; 10 new, 6 of which — at the START of this task — fired on
trigger-source presence alone with no query-term gate: `signs_by_age`, `ndbi_intervention`,
`sleep_nonpharma`, `school_inclusion`, `who_caregiver_training`, `ayres_si_definition`,
`adolescence_asd`). This last point — later found to be a real defect, see
`template_selection_audit.md` — was **not** flagged as a risk in T5.2's own reports, which only
documented the 3 templates that were *known* to share a source with another template (M-CHAT/ADOS-2,
melatonin/sleep) and gated those; the other 6 were left ungated because they didn't *appear* to share a
source with each other — T5.3 found that this reasoning was incomplete (see Phase 1).

## Baseline capture (before any T5.3 code change)

All 23 previously-templated questions plus 8 representative non-templated/special-case questions were
run live against `/api/chat` and recorded. Printed in full in this task's working transcript (not
re-attached here as a file — overwritten during the "after" capture, a process error disclosed in
`regression_report.md`, with the actual before/after comparison reconstructed from the preserved
transcript output, not re-guessed).

**Before-fix result**: all 23 templated questions returned `answer_mode: "topic_template"` with their
correct, topic-specific text (re-verified individually by inspecting each answer's opening sentence);
all 8 representative cases matched documented T4/T5.2 behavior exactly (greeting skipped retrieval,
weather rejected pre-retrieval, risperidone refused pre-retrieval, epilepsy/stem-cell/speech-delay
unchanged, q033's ADHD evidence still present).

## Scope decision carried into Phase 1

Because the preflight re-read found 6 templates with no query-term gate (a broader pattern than T5.2's
reports disclosed), Phase 1's audit was designed to specifically probe for "does this template fire on
source presence alone, and could that source realistically co-occur with an unrelated question's
evidence" for **every** template, not just the ones already known to share a source — this is what
surfaced the two real bugs documented in `template_selection_audit.md` and `template_conflict_report.md`.
