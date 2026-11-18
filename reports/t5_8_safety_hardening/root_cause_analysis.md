# T5.8 Phase 2 — Root-Cause Analysis

## Exact root cause

`app/answer/answer_generator.py`'s `generate()`, before this task:

```python
if _is_unproven_cure_question(folded) and not evidence:
    ... return the caution ...
```

The caution's condition included `and not evidence`. This was a deliberate design choice from the
original T3.1–T3.6 implementation (`reports/project_repair/phase_3_answer_generation.md`: "Query
claims/asks about a cure **with no supporting evidence**") — not a later regression, and not an
oversight introduced by any T5.x task. It went uncaught for every prior task because **dense retrieval,
the only retriever the live demo has ever used, essentially never returns any evidence at all for a
query phrased as an unproven-cure claim** that is not already specifically cached and vetted — so
`evidence` was empty in every real case anyone tested, and the condition's second half never mattered in
practice until T5.6/T5.7 introduced FTS, whose broader lexical recall surfaces *some* evidence (even
weak, topically-adjacent evidence) far more often.

## Why this is a genuine defect, not a reasonable design choice that just needs documenting

The condition conflates two things that this task's taxonomy (`safety_taxonomy.md`) explicitly
distinguishes: "evidence exists" and "evidence proves this specific method cures ASD." Before the fix,
*any* non-empty evidence list — including a chunk that only mentions the named substance for an unrelated
purpose — was treated as equivalent to "evidence of a cure," which is never what the retrieved content
actually says. The condition was checking the wrong thing.

## Why the fix is minimal and isolated

**One function, one conditional, one new helper.** No change to:
- `app/retrieval/evidence_gate.py` (unchanged — the Gate's own sufficiency judgment is not the problem;
  the problem is what `generate()` does with evidence the Gate already approved).
- `app/retrieval/citation_validation.py` (unchanged).
- `app/api.py` (unchanged — per this task's explicit protected boundary, and because the fix does not
  need to touch the API layer at all).
- `_is_dosing_question`/dosing refusal (unchanged — it was never the broken branch).
- Any of the 17 topic templates' text or trigger logic (unchanged).
- Either glossary file (unchanged — this is not a vocabulary problem).

## The fix, principle by principle (from the task's Phase 2 instructions)

1. **"Safety classification không được phụ thuộc đơn thuần vào việc retrieval có trả về evidence hay
   không"** — the `and not evidence` clause is removed entirely. `_is_unproven_cure_question(folded)`
   alone now determines whether the caution fires, exactly like `_is_dosing_question` already did.
2. **"Weak evidence không được làm mất safety caution"** — direct consequence of (1): no amount or
   strength of evidence can suppress the caution once the query is classified as an unproven-cure claim.
3. **"Citation phải phản ánh chính xác phạm vi nội dung được hỗ trợ"** — the caution response now
   *includes* the found evidence's citation IDs (so the response's `evidence` field, filtered by
   `app/api.py`'s existing `cited = set(answer.citation_ids)` logic, shows exactly what was retrieved) and
   appends an honest sentence stating explicitly what that evidence does and does not show (mentions/
   evaluates the substance, but does not confirm it cures ASD) — never silently dropping the citations,
   and never implying they support the cure claim.
4. **"Không biến mọi câu hỏi về vitamin, thuốc hoặc intervention thành câu hỏi cần từ chối"** — unaffected
   by construction: `_is_unproven_cure_question`'s trigger terms were already narrow (cure-claim phrasing
   only) and were not broadened by this fix. Verified directly in `adversarial_test_cases.md` (Group C,
   10 cases, 0 incorrectly swept into Group A's caution).
5. **"Không đưa ra khẳng định y khoa vượt quá tài liệu"** — the new evidence-addendum sentence is
   deliberately generic ("tài liệu đề cập... nhưng không xác nhận hiệu quả chữa khỏi") rather than
   attempting to characterize *what* the evidence does show in medical terms — avoiding any new claim this
   task cannot verify is accurate for every possible Group A query's retrieved content.
6. **"Giữ khả năng trả lời các câu hỏi kiến thức ASD thông thường"** — verified directly: `asd_definition`,
   `vaccine_myth`, `melatonin_efficacy`, and the cached `signs_by_age` question all still produce their
   correct, unaffected answers after the fix (spot-checked live against the unmodified `/api/chat`,
   `regression_report.md`).

## Before/after evidence (required by the task; full detail in `implementation_changes.md`)

- **Before**: a dedicated unit test (`test_unproven_cure_claim_still_cautions_when_weak_topically_
  adjacent_evidence_exists`) added to the permanent suite, confirmed to **fail** against the pre-fix code.
- **After**: the same test, confirmed to **pass** against the fixed code, alongside all 21 pre-existing
  `test_answer_generator.py` tests (including the original empty-evidence caution test, still passing
  unchanged) and the full 454→456 test suite (2 new tests added, 0 removed, 0 modified beyond the fix
  itself).
- **Live, end-to-end**: the isolated harness's vitamin-B6 reproduction, re-run after the fix, now returns
  `safety_caution_unproven_cure` instead of `extractive_fallback` (`eval/reports/t5_8_after_fix_repro.
  json`).

## Rollback

`git diff`-equivalent scope: one file (`app/answer/answer_generator.py`, ~15 added lines, 1 condition
changed), one test file (2 new tests added, 0 changed). Reverting both files to their pre-T5.8 content
restores the exact pre-fix behavior; no other file, config, or data was touched, so no other rollback step
is needed.
