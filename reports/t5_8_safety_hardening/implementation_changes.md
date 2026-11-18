# T5.8 Phase 2 — Implementation Changes

## Files changed (exhaustive list)

1. `app/answer/answer_generator.py` — the fix itself.
2. `tests/unit/test_answer_generator.py` — 2 new permanent regression tests.

No other file was changed. No config, glossary, corpus, embedding, schema, or frontend file was touched.

## Diff, in full

### `app/answer/answer_generator.py`

**Added**, immediately after `_CURE_CLAIM_CAUTION_TEMPLATE`:

```python
_CURE_CLAIM_EVIDENCE_ADDENDUM = (
    " Hệ thống có tìm thấy {n} tài liệu đề cập đến chủ đề liên quan, nhưng không tài liệu nào trong đó "
    "xác nhận hiệu quả chữa khỏi tự kỷ — việc một chất hoặc phương pháp được nhắc đến hoặc được nghiên cứu "
    "cho mục đích khác (ví dụ hỗ trợ giấc ngủ) không có nghĩa là nó chữa được tự kỷ."
)


def _unproven_cure_evidence_note(evidence: list[dict]) -> str:
    if not evidence:
        return ""
    return _CURE_CLAIM_EVIDENCE_ADDENDUM.format(n=len({e["source_id"] for e in evidence}))
```

**Changed**, inside `generate()`:

```diff
     if _is_dosing_question(folded):
         return dosing_refusal()
-    if _is_unproven_cure_question(folded) and not evidence:
+    if _is_unproven_cure_question(folded):
         claim = "phương pháp này" if "te bao goc" not in folded else "liệu pháp tế bào gốc"
-        return AnswerResult(_CURE_CLAIM_CAUTION_TEMPLATE.format(claim=claim), "safety_caution_unproven_cure",
-                            [], False)
+        text = _CURE_CLAIM_CAUTION_TEMPLATE.format(claim=claim) + _unproven_cure_evidence_note(evidence)
+        citation_ids = [e["citation_id"] for e in evidence]
+        return AnswerResult(text, "safety_caution_unproven_cure", citation_ids, False)
```

### `tests/unit/test_answer_generator.py`

Two tests added immediately after the existing
`test_unproven_cure_claim_with_no_evidence_gets_a_caution_message_not_silence`:

- `test_unproven_cure_claim_still_cautions_when_weak_topically_adjacent_evidence_exists` — the
  before/after reproduction test (fails pre-fix, passes post-fix).
- `test_unproven_cure_claim_with_no_evidence_has_no_evidence_addendum_text` — guards against the new
  addendum sentence ever appearing when there is nothing to disclose.

No existing test was modified or removed.

## Verification performed, in order

1. Added the 2 new tests against the **unfixed** code; confirmed `test_unproven_cure_claim_still_
   cautions_when_weak_topically_adjacent_evidence_exists` **fails** with
   `AssertionError: assert 'extractive_fallback' == 'safety_caution_unproven_cure'` (the before-evidence,
   saved in `baseline_audit.md`).
2. Applied the fix.
3. Re-ran `tests/unit/test_answer_generator.py` in full: **22/22 passed** (20 pre-existing + 2 new).
4. Re-ran the full suite: **406 unit + 50 integration = 456 passed**, 0 failed (404→406 reflects the 2 new
   tests; 0 removed, 0 newly failing).
5. `ruff check app/answer/answer_generator.py tests/unit/test_answer_generator.py` — clean.
6. Re-ran the isolated T5.7 harness's vitamin-B6 reproduction live: now returns
   `safety_caution_unproven_cure` (`eval/reports/t5_8_after_fix_repro.json`).
7. Live-checked 4 unaffected normal-ASD-question cases against the real, running `/api/chat`
   (`asd_definition`, `vaccine_myth`, `melatonin_efficacy` via its exact cached phrasing, and the cached
   18-month signs question) — all 4 produce their unchanged, correct answers.
8. Re-ran the T2.3 66-question dense-retrieval regression: byte-identical to the recorded baseline
   (ignoring timestamp/log/latency).
9. Re-ran the 32-question independent set live: identical outcome to every prior run (32/32 routing,
   1/32 safety refusal, 31/32 cache miss) — unaffected, as expected, since none of those 32 questions
   reach the unproven-cure branch with non-empty evidence live (dense is cache-only and FTS is still not
   wired into `/api/chat`, per this task's own protected boundary).

## Explicitly not done, per the "minimal fix" instruction

- Did not refactor `_is_dosing_question`/`_is_unproven_cure_question`'s term lists.
- Did not change how any other branch (`insufficient_evidence`, topic templates, `extractive_fallback`)
  depends on evidence.
- Did not attempt to classify evidence into the full 4-state taxonomy (`safety_taxonomy.md`) inside the
  code itself — the fix only needs to know "is there any evidence to disclose," not which of the 4
  states it occupies, because the caution's own wording already correctly handles every state short of
  state 4 (which this corpus is not expected to ever produce for a Group A term) by never asserting more
  than "mentioned/evaluated, not proven to cure."
- Did not touch `app/api.py`, any glossary, or wire FTS into the live endpoint.
