# T5.10 Implementation Changes

## Files changed

- `app/answer/answer_generator.py`
- `tests/unit/test_answer_generator.py`
- `tests/unit/test_t5_10_medication_safety.py` (new focused regression tests)

No template, Evidence Gate, retriever, corpus, embedding, benchmark, database, or API code was changed.

## Classifier changes

### Defect A — intent-based direct dosage recognition

Added bounded patterns for direct amount questions: `bao nhieu mg`, `may mg`, `lieu ... bao nhieu`, and `uong/dung ... luong bao nhieu`. They recognize an unanswered dose amount even without a numeric value or a named medication.

Added non-personal context guards for research, trials, efficacy, risk, and side-effect questions before generic dose-plus-drug checks. Explicit self-management remains higher priority, so a query that asks whether the user should personally change a dose is still refused even if it also mentions a side effect.

This was necessary to preserve the intent boundary: the old numeric-mg-plus-known-drug rule would otherwise refuse `Nghiên cứu sử dụng 5 mg melatonin như thế nào?` and dose-related side-effect questions.

### Defect B — distinguish self-management from education/research

Added bounded patterns for self-directed increase, decrease, adjustment, stopping, and switching. Intervening wording such as `tăng gấp đôi liều` and `tự điều chỉnh lại liều` is recognized. The classifier no longer treats `đổi thuốc` or a named-drug `chuyển ... sang` phrase alone as proof of self-management.

As required by the clarification, a clinician-supervised switch question and medication-switch research are not automatically routed to the dosage refusal. Existing explicit self-switch cases remain refused.

### Defect C — psychiatric medication phrase is no longer a standalone trigger

Removed the unconditional `thuoc tam than` trigger. Education, research, and side-effect questions containing that phrase remain answerable through the normal evidence path. Self-stop, self-adjustment, and direct dose questions containing the same phrase remain refused.

## Test changes

- Added 34 classifier and `generate(query, [])` intent-boundary cases, plus a medication-choice fallback assertion.
- Updated the old T5.8 unit-test expectation for the supervised-switch question because the mandatory T5.10 clarification supersedes that historical expectation. The old script and its recorded results were left unchanged.

## Verification and limitations

- Focused suite: 35 passed.
- `test_answer_generator.py`: 30 passed.
- Full unit suite: 449 passed.
- Full integration suite: 50 passed.
- Ruff on all three changed Python files: passed.
- FTS-backed spot checks confirmed the same classification boundaries with actual retrieved evidence; these use the isolated T5.7 harness and do not integrate FTS into the demo API.

Medication-choice questions return the existing non-prescriptive source-excerpt fallback in the observed FTS run. The output states that it is not a verified Vietnamese synthesis; no drug is selected for the child. This is a software behavior check, not a clinical assessment.

## Rollback

Restore the prior dosing-classifier constants and helper logic in `app/answer/answer_generator.py`, and restore the previous supervised-switch expectation in `tests/unit/test_answer_generator.py`. Remove `tests/unit/test_t5_10_medication_safety.py` and the `reports/t5_10_targeted_safety_repair/` task artifacts if rolling back the entire task. No data migration or database rollback is involved.
