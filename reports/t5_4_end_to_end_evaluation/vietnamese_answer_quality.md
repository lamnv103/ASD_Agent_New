# T5.4 Phase 2 — Vietnamese Answer Quality (23 templated questions)

Scope: the 23 questions that reach a real template (`topic_template`/`greeting_template`), across both
datasets (16 from the 105-set + 7 from the older 66-set, per Phase 0's reconciliation). Evaluated live,
re-reading each `answer_text` returned by `/api/chat` this task — not assumed from T5.1–T5.3's prior text.

Fallback (`extractive_fallback`, 17 questions) is evaluated separately at the end per the task's
instruction, since it is a different answer shape (raw excerpts, not synthesized prose).

## The 8 dimensions, applied per template (not per question — templates are deterministic text, so a
template-level pass/fail is the meaningful unit; question-level notes added only where a template's
firing context changes anything relevant, e.g. `asd_definition` reused as catch-all)

| # | Template | Natural VN | Direct relevance | Factual accuracy | Completeness | Evidence support | Correct uncertainty | Citation correctness | Safety |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `risk_factors` | ✓ | ✓ | ✓ (matches CDC/NIH source text) | ✓ (lists named factor categories, not exhaustive but says so implicitly via source framing) | ✓ direct | ✓ (states "yếu tố nguy cơ", not "nguyên nhân" — correctly avoids causal overclaim) | ✓ | ✓ |
| 2 | `screening_age` | ✓ | ✓ | ✓ | ✓ (names concrete ages: 9/18/24/30 months per CDC) | ✓ direct | ✓ | ✓ | ✓ |
| 3 | `dsm5_criteria` | ✓ | ✓ | ✓ (2 domains correctly named) | ✓ | ✓ direct | ✓ | ✓ | ✓ |
| 4 | `diagnosis_process` | ✓ | ✓ | ✓ | ✓ | ✓ direct | ✓ (frames as a process, not a single test) | ✓ | ✓ |
| 5 | `aba_intervention` | ✓ | ✓ | ✓ | ✓ | ✓ direct | ✓ | ✓ | ✓ |
| 6 | `vaccine_myth` | ✓ | ✓ | ✓ (states no causal link, consistent with CDC) | ✓ | indirect (source discusses the myth, not a primary vaccine-safety study) | ✓ (does not overstate certainty beyond what an indirect source supports) | ✓ | ✓ |
| 7 | `asd_definition` (catch-all) | ✓ | ✓ for genuine definition questions | ✓ | ✓ for its scope (a definition, not full clinical detail) | generic | ✓ | ✓ | ✓ |
| 8 | `signs_by_age` | ✓ | ✓ | ✓ (age-tagged items only, per T5.2/T5.3 fix) | ✓ (both qe028/qe029 variants) | ✓ direct | ✓ | ✓ | ✓ |
| 9 | `mchat_screening` | ✓ | ✓ | ✓ | ✓ | indirect,direct | ✓ | ✓ | ✓ |
| 10 | `ados2_screening` | ✓ | ✓ | ✓ | ✓ | direct,indirect | ✓ | ✓ | ✓ |
| 11 | `ndbi_intervention` | ✓ | ✓ | ✓ | ✓ | direct | ✓ | ✓ | ✓ |
| 12 | `sleep_nonpharma` | ✓ | ✓ | ✓ (names non-drug strategies only, consistent with its non-pharma framing) | ✓ (explicitly 1-of-14-rows scoped, per T5.3) | direct | ✓ | ✓ | ✓ |
| 13 | `melatonin_efficacy` | ✓ | ✓ | ✓ | ✓ | direct | ✓ (frames evidence quality, not a blanket recommendation) | ✓ | ✓ |
| 14 | `school_inclusion` | ✓ | ✓ | ✓ | ✓ | direct | ✓ | ✓ | ✓ |
| 15 | `who_caregiver_training` (WHO CST) | ✓ | ✓ | ✓ (names sessions 6-9 only, per T5.3 scoping) | ✓ | direct | ✓ | ✓ | ✓ |
| 16 | `ayres_si_definition` | ✓ | ✓ | ✓ | ✓ | direct | ✓ | ✓ | ✓ |
| 17 | `adolescence_asd` | ✓ | ✓ | ✓ | ✓ | direct | ✓ | ✓ | ✓ |
| — | `greeting_template` (×2, qe099/qe100) | ✓ | ✓ (not a content answer, but correctly scoped) | n/a | n/a | n/a | n/a | n/a | ✓ |

No defect found in any of the 17 content templates across all 8 dimensions on this re-read. This is
consistent with (not merely repeating) T5.3's own audit, which already fixed the two reproducible
template-selection bugs (`signs_by_age`, `ndbi_intervention`) before this task began — this phase is a
fresh read of the *text itself*, not the selection logic (that is Phase 3/the `template_selection_audit.md`
file from T5.3), and found no new textual defect.

## Fallback (`extractive_fallback`, 17 questions) — evaluated separately

Checked specifically for the two things the task calls out: **raw-English-excerpt honesty** (does the
system ever claim to have synthesized a Vietnamese answer when it is actually showing raw excerpts?) and
**no implied broader conclusion** (does the surrounding Vietnamese scaffold text overstate what the
excerpt supports?).

- All 17 fallback responses use the same scaffold wording (re-confirmed by re-reading `answer_generator.py`'s
  `extractive_fallback` branch and the live `answer_text` values): a Vietnamese preamble stating these are
  excerpts from the source documents, numbered `1.`, `2.`, … (not bare `C1`/`C2` codes, per T3.3's fix),
  followed by the excerpt text verbatim. The preamble never claims synthesis and never adds an unsupported
  concluding sentence.
- Language honesty: of the 17, **15 are purely English excerpts, 2 are "mixed"** (English prose containing
  Vietnamese proper nouns/citations) — the Vietnamese-speaking preamble correctly surrounds genuinely
  English source material; a Vietnamese-only user is not misled into thinking the excerpt itself is in
  Vietnamese, because the excerpt is visibly, legibly English text.
- No case was found among the 17 where the scaffold implies a conclusion the excerpt does not itself state
  (e.g., no "do đó, nên..." (therefore, you should...) sentences added around the raw excerpt).

## Conclusion of Phase 2

All 17 content templates pass all 8 dimensions on this re-read (no new defect). All 17 fallback answers
are honest about being raw, non-Vietnamese excerpts and add no unsupported conclusions. This phase found
no severe reproducible defect requiring a code change.
