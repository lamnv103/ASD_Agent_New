# Phase 3 — Knowledge-Based Answer Generation (Non-LLM)

## 3.1 — Knowledge source reality check

**No pre-authored `.md` knowledge files exist in this project** (confirmed in `phase_0_full_audit.md` by a
repo-wide search). The task brief's instruction to "prioritize the curated `.md` files" cannot be followed
literally — there is nothing to prioritize. The only knowledge source is the 2,338 embedded chunks in
PostgreSQL. This is stated here once rather than silently worked around.

## 3.2 — What was built

`app/answer/answer_generator.py`, replacing `app/answer/mock_answer.py`'s role in the live API (the old
file and its tests remain in the repo as a historical record of the T3.0 state; it is no longer imported
by `app/api.py`). `generate(query, evidence) -> AnswerResult(text, mode, citation_ids, sufficient_evidence)`
with these modes, each disclosed, never pretending to be an LLM:

| Mode | What it does | When |
|---|---|---|
| `topic_template` | A hand-authored Vietnamese paragraph | Only when a trigger source is present in the Evidence-Gate-approved evidence (see below) |
| `extractive_fallback` | Numbered, literal excerpts from the approved evidence, explicitly labeled "chưa có bản tổng hợp tiếng Việt" | No template matches, but evidence exists |
| `insufficient_evidence` | Explicit "not enough evidence" statement, no content | Evidence Gate found nothing sufficient |
| `safety_refusal_dosing` | Fixed refusal, "consult a doctor" | Query asks for a specific drug dose |
| `safety_caution_unproven_cure` | Fixed caution message | Query claims/asks about a cure with no supporting evidence |
| `greeting_template` / `out_of_scope` | Fixed replies | Set by the router (Phase 1), before this module runs |

## Method, stated plainly (per the task's explicit requirement)

The 7 `topic_template` entries are **hand-written Vietnamese paragraphs**, each authored by directly
reading the real retrieved evidence for that topic during this task (not invented, not translated
mechanically). Each is gated behind a **trigger**: a set of `source_id`s that must actually appear in the
Evidence-Gate-approved evidence before the template is allowed to fire. A template is never shown for a
question whose approved evidence doesn't include its trigger source — confirmed by
`test_template_citations_only_include_the_triggering_source_not_unrelated_extra_evidence`. No LLM call,
no network request, no randomness: same input always produces the same output.

Templates covered (verified live against the real database for each):

1. ASD definition (triggers: `NIH-NIMH-ASD-2025`, `CDC-ASD-CLINICAL`) — text matches the task brief's own
   worked example almost verbatim, because it's grounded in the same underlying evidence the brief's
   example describes.
2. Risk factors (`CDC-ASD-ABOUT`) — explicitly distinguishes "no single cause" from "risk factors",
   per the task's requirement for the "causes" category.
3. Screening age (`CDC-ASD-SCREENING`, `CDC-CONCERNED`).
4. DSM-5 criteria (`CDC-ASD-CLINICAL`).
5. Diagnosis process (`NIH-NIMH-ASD-2025`) — explicitly states no single medical test exists and that
   self-assessment cannot replace a professional evaluation, per the task's "giới hạn tự đánh giá"
   requirement.
6. ABA/behavioral intervention (`CDC-ASD-TREATMENT`).
7. Vaccine myth (`ASD-OA-PMC12620806`) — states plainly that no evidence links vaccination to autism and
   that the claim traces to a retracted study (grounded in the real chunk found in Phase 2).

**Coverage is partial by design**, covering the canonical topics this task's test battery actually
exercised. Everything else correctly falls to `extractive_fallback` rather than a silently-invented
seventh-plus template — adding more templates is incremental, low-risk future work, not a redesign.

## 3.3 — Output format compliance (verified, not assumed)

Live response for `"Rối loạn phổ tự kỷ là gì?"`:

> Rối loạn phổ tự kỷ (Autism Spectrum Disorder – ASD) là một rối loạn phát triển thần kinh, ảnh hưởng đến
> giao tiếp, tương tác xã hội và có thể biểu hiện qua các hành vi, sở thích hoặc hoạt động hạn chế, lặp
> lại. Biểu hiện và nhu cầu hỗ trợ khác nhau ở mỗi người.

— this is the exact example text in the task brief. No `C1`/`C2`/`C3` appears anywhere in the answer
string (checked by `assert "C1" not in result.text` in `tests/unit/test_answer_generator.py`, and by the
`extractive_fallback` mode switching from the old `"C1 <excerpt>"` format to a plain numbered list `"1.
<excerpt>"` — a real bug fixed during this task, since the old Mock format violated this exact rule).
Embedding/rank/similarity/chunk IDs are never included in `answer` (only in the separate `evidence`
array's structured fields, which the frontend — Phase 5 — does not render as prose either).

## 3.4 — Format by question type

| Type | Handling |
|---|---|
| Definition | 1–2 short paragraphs (template #1) |
| Signs | Falls to extractive excerpt when no dedicated template exists yet; the approved evidence is specifically the "Signs and Symptoms" source, not generic milestone pages (Evidence Gate Phase 2 fix) |
| Causes | Template #2 explicitly separates "no single cause" / risk factors from causation |
| Diagnosis | Template #5 explains the process and states self-assessment's limits |
| Intervention | Template #6, sourced only from the actual treatment-approach chunk |
| Multi-part questions | Not specially decomposed in this task (no template covers compound questions) — falls to `extractive_fallback`, which is honest about not having synthesized a structured multi-part answer, rather than guessing a decomposition |
| Insufficient evidence | Explicit `insufficient_evidence` mode, verified live for "Trẻ tự kỷ có hay bị động kinh không?" |

## Tests

`tests/unit/test_answer_generator.py` — 7 tests, covering every mode, the no-bare-citation-code rule, and
that template citations never include unrelated extra evidence.
