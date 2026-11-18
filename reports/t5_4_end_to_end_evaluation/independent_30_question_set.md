# T5.4 Phase 5 — Independent Question Set

The task required ≥30 genuinely new questions, not reused from the 105-question set or the older 66-
question set, not used to tune any template, and frozen before being evaluated. **32 questions were
created** (`eval/datasets/independent_eval_v1.jsonl`, IDs `ie001`–`ie032`), exceeding the minimum.

## File integrity

```
SHA256: 5572a29d029803259df8cdb873fdb1d78117200ae7bd09cae68c49cb84c91bd9
```
Re-computed directly this task from the file on disk — matches the hash recorded at creation time. The
file has not been edited since being frozen.

## No-overlap verification

Checked programmatically (exact-text comparison) against both `eval/datasets/asd_qa_eval_v2.jsonl` (105
questions) and `eval/datasets/retrieval_eval_v1.jsonl` (the older 66). **Zero exact-text duplicates
found.** Several questions deliberately revisit similar topics from a different angle (e.g. `ie029`
language-development vs. hearing impairment, a different angle than `qe034`'s speech-delay-vs-ASD; `ie025`
puberty *timing* vs. the existing `adolescence_asd` template's executive-function/social-complexity claim)
— these are intentionally adjacent-but-distinct, not disguised duplicates, and are noted as such in each
record's `notes` field.

## Categories (14 total, with question counts)

| Category | Count | Question IDs |
|---|---:|---|
| `comorbidity_asd_adhd` | 4 | ie001, ie002, ie003, ie028 |
| `language_development` | 4 | ie004, ie005, ie006, ie029 |
| `age_distinction` | 4 | ie007, ie008, ie009, ie030 |
| `greeting_mixed` | 2 | ie010, ie011 |
| `multi_intent` | 3 | ie012, ie013, ie014 |
| `medication_safety` | 2 | ie015, ie016 |
| `unproven_cure` | 2 | ie017, ie018 |
| `vaccine_myth` | 2 | ie019, ie020 |
| `out_of_scope_mixed` | 2 | ie021, ie022 |
| `screening_diagnosis` | 1 | ie023 |
| `adolescence` | 3 | ie024, ie025, ie031 |
| `adulthood` | 1 | ie026 |
| `feeding_nutrition` | 1 | ie027 |
| `education_inclusion` | 1 | ie032 |

## Phrasing variety (per the task's requirement)

- **Natural/colloquial phrasing**: ie002, ie004, ie011, ie023, ie032 (e.g. "Con tui bị...", "Cô tôi làm
  giáo viên mầm non hỏi là...")
- **No-diacritic phrasing**: ie003, ie006, ie010, ie024, ie027, ie031 (6 questions — tests the system
  without relying on proper Vietnamese typing)
- **Multi-intent phrasing**: ie012 (3-part), ie013 (2-part), ie014 (2-part), ie028 (medication +
  comorbidity combined)
- **ASD+ADHD comorbidity**: ie001, ie002, ie003, ie028 (4 questions, a topic not covered by any existing
  template)
- **Language development**: ie004, ie005, ie006, ie029 (4 questions)
- **Age-distinction topics**: ie007, ie008, ie009, ie030 (4 questions, explicitly requiring the system to
  reason about differing signs/behavior across different named ages)

## Freeze discipline

This set was created and frozen (hash recorded) **before** `scripts/eval_independent_30.py` was run
against it. No template in `app/answer/answer_generator.py` was modified after this set was created or
after seeing its results — confirmed by the fact that zero code changes were made anywhere in this task
(see `regression_report.md`). This satisfies the task's explicit prohibition on "điều chỉnh template theo
kết quả rồi tiếp tục gọi đây là test độc lập" (adjusting a template based on results and still calling it
independent) — no such adjustment occurred, by construction.
