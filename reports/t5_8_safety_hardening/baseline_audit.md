# T5.8 Phase 0 — Baseline Audit

Read this task: `reports/t5_7_fts_integration_readiness/final_report.md`,
`reports/t5_7_fts_integration_readiness/false_positive_safety_audit.md` (the finding this task fixes),
T2.6's authorization status (`app/config.py`'s fail-loud gate, unchanged), the original safety-override
design intent (`reports/project_repair/phase_3_answer_generation.md`, T3.1–T3.6 — no single file is
literally titled "T4 safety hardening report" in this project; the closest equivalents are
`reports/final_hardening/phase_2_evidence_gate_audit.md` and `phase_3_answer_quality.md`, both re-read),
and `reports/t5_3_answer_quality_audit/template_selection_audit.md`. Code re-verified directly, not
inferred from any of these.

## 1. The safety branches that exist today, read directly from `app/answer/answer_generator.py`

```python
def generate(query, evidence):
    folded = fold(query)
    if _is_dosing_question(folded):
        return dosing_refusal()
    if _is_unproven_cure_question(folded) and not evidence:   # <-- the bug, see root_cause_analysis.md
        ...
        return AnswerResult(..., "safety_caution_unproven_cure", [], False)
    if not evidence:
        return AnswerResult(..., "insufficient_evidence", [], False)
    ... (template/fallback logic, evidence-dependent)
```

- **`_is_dosing_question`** (`_DOSING_TERMS` + `_DRUG_TERMS`, or `_MEDICATION_ADJUSTMENT_TERMS` alone):
  fires **unconditionally** on the query text — never reads `evidence` at all.
- **`_is_unproven_cure_question`** (`_CURE_CLAIM_TERMS`: "te bao goc", "chua khoi", "chua duoc",
  "chua tu ky"): before this task's fix, fired **only when `evidence` was empty**.
- **Trigger terms, re-confirmed narrow**: `_is_unproven_cure_question` does not match generic
  medication/vitamin/intervention vocabulary — only specific cure-claim phrasing. This was re-verified
  directly in code; it is why Phase 2's fix does not need to guard against "every vitamin question becomes
  a refusal" (that risk was never structurally present — see `root_cause_analysis.md`).

## 2. Relationship between safety and evidence availability, before this task

| Branch | Evidence-dependent? |
|---|---|
| Dosing refusal | **No** — fires regardless of evidence |
| Unproven-cure caution | **Yes (the bug)** — only fired when evidence was empty |
| Insufficient-evidence | Yes, by design (this is its entire purpose) |
| Topic templates | Yes, by design (require a specific trigger source) |
| Extractive fallback | Yes, by design (shows whatever evidence exists, honestly labeled) |

**Only the unproven-cure branch's evidence-dependence was ever a defect** — the others' dependence on
evidence is their correct, intended behavior (a template must have evidence; a fallback must have
evidence to show; "insufficient" must mean no evidence was found). This distinction matters for Phase 2:
the fix must touch only the one actually-broken branch, not re-architect how evidence-dependence works
elsewhere in the function.

## 3. Processing order, re-confirmed

`app/api.py`: validate query/k → `classify_intent` (greeting/out_of_scope short-circuit, no retrieval) →
`active_retriever.retrieve()` → `assess_evidence` (gate) → `validate_citations` → `generate_answer`. Inside
`generate_answer`, dosing and (now) unproven-cure checks run **before** any evidence-dependent branch,
on the query text alone — re-confirmed unchanged by this task's fix (the fix only changes *what happens
after* the cure-question check fires, not *when* it fires).

## 4. Branches that could be changed in outcome by what retrieval returns

- **Unproven-cure caution** — confirmed changeable before the fix (T5.7's Finding #6); fixed this task.
- **Topic templates** — changeable by design (a different source present → a different or no template)
  — this is the system working as intended, not a safety defect, and T5.3/T5.7 already audited this
  surface for false-fire risk (per-template term+source gating holds).
- **Extractive fallback vs. insufficient-evidence** — changeable by design (more/less evidence found)
  — again, intended behavior.
- **Dosing refusal** — confirmed **not** changeable by retrieval (unconditional check), re-verified this
  task (Phase 3/4 testing below).

## 5. Existing tests found before this task

`tests/unit/test_answer_generator.py::test_unproven_cure_claim_with_no_evidence_gets_a_caution_message_
not_silence` — the **only** existing test of the unproven-cure branch, and it only covers the
empty-evidence case, which is exactly why the bug was never caught by the existing suite. No test existed
for "unproven-cure question + non-empty evidence."

## 6. Bug reproduced with an isolated harness, before any fix (this task)

Using `scripts/t5_7_e2e_harness.py` (T5.7's isolated, `app/`-external harness, unmodified by this task),
re-run fresh this task, saved to `eval/reports/t5_8_before_fix_repro.json`:

| Query | FTS evidence | Mode (before fix) |
|---|---|---|
| "Nghe nói uống vitamin B6 liều cao chữa được tự kỷ, có đúng không?" | 8 hits (weak/adjacent — a sleep-disorder paper mentioning B6 as a supplement ingredient) | **`extractive_fallback`** — caution skipped |
| "Tế bào gốc có chữa được tự kỷ không?" | 0 hits | `safety_caution_unproven_cure` (correct, since this case never had evidence to trigger the bug) |

Also reproduced at the unit level (not dependent on any live DB/FTS call), added to the permanent test
suite as `test_unproven_cure_claim_still_cautions_when_weak_topically_adjacent_evidence_exists` —
confirmed to **fail** against the pre-fix code (`AssertionError: assert 'extractive_fallback' ==
'safety_caution_unproven_cure'`) before any change was made, then confirmed to **pass** after the fix
(see `implementation_changes.md` and `root_cause_analysis.md`).

## 7. Protected boundaries re-confirmed before touching any code

- `ASD_DEMO_MODE=true`, all `ENABLE_LIVE_*` flags `False` (unchanged).
- DB already running; `research_reader` connection confirmed without starting Docker.
- T2.6 (`APPROVAL_REQUIRED`) not touched, not revisited.
- This task's fix (Phase 2) is the first and only `app/` change across T5.5–T5.8; it was made only after
  this baseline audit and the before-fix reproduction were both complete and recorded.
