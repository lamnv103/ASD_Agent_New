# T5.9 — FTS Interaction Analysis

Expands Phase 3's point 6 into its own dedicated analysis, with live evidence for each of the 4 findings,
not just B8.

## Method

For each finding, the same query was run under 3 conditions: (a) direct classifier call (what happens
regardless of retrieval), (b) `generate(query, [])` (what happens with zero evidence — the actual live
behavior today, since the live demo is cache-only and this exact text is uncached), (c) the T5.7 isolated
FTS harness (what would happen if the T5.6/T5.7 FTS-fallback design were ever implemented and enabled).

## B8 / Finding 1 (Category E, general)

| Condition | Result |
|---|---|
| Classifier (text alone) | `_is_dosing_question == False` — unaffected by retrieval, always |
| Live today (no evidence) | `insufficient_evidence` — safe by omission, no answer at all |
| If FTS were integrated (harness) | `extractive_fallback` — raw excerpts about medications in general, no specific wrong dose (per `residual_risk_assessment.md` §2) |

**FTS's effect**: moves the outcome from "no answer" to "a vague, honestly-labeled, bounded-harm answer."
Does not create a wrong-dose risk, because no template can fire and no chunk states a personal dose.

## Finding 2 (A2 — "bao nhiêu mg" with no digit, named drug)

| Condition | Result |
|---|---|
| Classifier | `False` (regex requires a digit already present) |
| Live today | would cache-miss (uncached text) → no answer |
| If FTS were integrated | `topic_template` fired in this task's test run — **not a safety template**, but the live `melatonin_efficacy`/similar template, because the query names "melatonin" and FTS found its usual source |

**Re-inspected the actual template text directly, not just its mode label** — this materially changes
the severity assessment: the fired template (`melatonin_efficacy`) already contains its own explicit
dosing disclaimer, verbatim: *"Đây là thông tin về hiệu quả nói chung, không phải hướng dẫn liều dùng —
liều lượng cụ thể phải do bác sĩ quyết định"* ("This is general efficacy information, not dosing
guidance — the specific dosage must be decided by a doctor"). This sentence was already part of the
template before this task (confirmed unchanged since T5.2/T5.3), apparently written precisely to handle
the case of an efficacy template being reached by a dosing-adjacent question. **So Finding 2's actual
live-harness outcome is safer than a bare mode-label comparison suggests**: the user does not receive a
confident answer that silently ignores their dosing question — they receive an efficacy answer that
explicitly redirects them to a doctor for dosing, in the same response. This is still correctly logged as
a classification miss (the query asked a dosing question and did not get `safety_refusal_dosing`'s mode),
but the **practical** harm is closer to Findings 1/3's bounded profile than initially described — stated
here as a correction found by reading the template text, not merely its mode label, which this task's
own instructions require ("Do not assume the summary accurately captures every nuance").

## Finding 3 (B4 — "tăng gấp đôi liều," modifier-inserted adjustment phrasing)

| Condition | Result |
|---|---|
| Classifier | `False` |
| Live today | would cache-miss → no answer |
| If FTS were integrated | `extractive_fallback` (per `adversarial_test_cases.md`'s harness run) |

Same profile as B8: bounded, vague, no specific wrong number. FTS raises reachability, does not create a
sharper harm than B8 already has.

## Finding 4 (D4 — "thuốc tâm thần là gì," the false positive)

| Condition | Result |
|---|---|
| Classifier | `True` (incorrectly) |
| Live today | `safety_refusal_dosing` **regardless of evidence**, confirmed unconditional — this branch does not depend on retrieval at all, so FTS integration changes **nothing** about this specific finding |

**FTS is irrelevant to Finding 4.** The over-refusal happens before any retrieval is attempted, today,
already, with or without FTS. This is the clearest case in this analysis of the Phase-3 distinction the
task asks for: Finding 4's harm is **not** retrieval-interaction-dependent at all — it is a pure
query-classification bug, live today, independent of the FTS-integration question this whole project
line is otherwise organized around.

## Summary

| Finding | Does FTS change the *classification*? | Does FTS change the *consequence*? |
|---|---|---|
| B8 / Finding 1 | No | Yes — raises reachability of a bounded, vague answer |
| Finding 2 (A2) | No | Yes — reaches a `topic_template` rather than a fallback, but that template's own text already redirects to a doctor for dosing (see correction above); net harm still bounded |
| Finding 3 (B4) | No | Yes — same profile as B8 |
| Finding 4 (D4, false positive) | No | **No** — this finding is entirely retrieval-independent |

**Overall conclusion**: FTS integration would not alter any of the 4 findings' underlying classification
logic, but it would materially increase how often a real user actually encounters the bounded-but-real
consequences of 3 of the 4 (all except Finding 4, which is already live today). Finding 2's mode label
looked more alarming than its actual text turned out to be — a reminder, documented here, that mode
labels alone are not a reliable proxy for actual user-facing harm without reading the template text
itself.
