# T5.7 Phase 6 — Integration Readiness

## The three permitted conclusions, applied

**B. PARTIAL — còn lỗi precision, coverage, hoặc evidence.**

## Why not A (READY FOR ISOLATED INTEGRATION)

A requires the design to be safe enough to gate behind a default-OFF feature flag with no known
confirmed safety regression waiting behind that flag. `false_positive_safety_audit.md`'s Finding #6 is a
**confirmed, reproduced safety-message-suppression risk**: the unproven-cure caution can be silently
replaced by a neutral raw-excerpt fallback once FTS evidence (even weak, topically-adjacent evidence) is
introduced into the pipeline. A feature flag defaulting OFF would prevent this from reaching real users
*today*, but it does not make the design itself ready — "ready for isolated integration" should mean the
isolated path is itself safe to turn on for testing, and this one specific path (unproven-cure questions)
is not, until `app/answer/answer_generator.py`'s `_is_unproven_cure_question(...) and not evidence`
condition is revisited (an `app/` change explicitly out of this task's scope).

## Why not C (BLOCKED)

C requires a problem with authorization, safety-as-a-whole, or data integrity that prevents any further
work. That is not the case here:
- **Authorization**: fully compliant. No Cohere/LLM call, no live query embedding, T2.6 untouched.
- **Data integrity**: fully compliant. No corpus/vector/schema/benchmark change; T2.3's regression is
  byte-identical; the 32-question independent set's live behavior is unchanged.
- **Safety**: 10 of 11 audited scenarios are safe; the one confirmed issue (Finding #6) is narrow, well-
  understood, has a clear fix shape already described (even though not implemented), and does not
  indicate a systemic breakdown of the safety-override architecture — the dosing-refusal path (the more
  acute safety concern, since it involves specific medication/dosage) was confirmed robust to FTS
  evidence in every tested scenario.

**B is therefore the accurate, evidence-based conclusion**, not a default or a hedge.

## What would need to be true to move from B to A

1. **Fix Finding #6** (the unproven-cure/evidence interaction) in `app/answer/answer_generator.py` — an
   `app/` change, requiring a new task with that explicit mandate (this task's own protected boundaries
   forbid it here: "Không sửa app/ trong giai đoạn audit và validation").
2. **Resolve or explicitly accept** the remaining precision issues named in `fts_precision_audit.md`
   (`can thiep`'s conditional-reliability risk) and the coverage gaps named in `end_to_end_evaluation.md`
   (4 of 11 topic groups got zero newly-reachable structured answers in this task's 22-question test) —
   either with further glossary/query-composition work, or with an explicit, documented decision that the
   current coverage is "good enough to ship behind a flag, gaps disclosed to users via the response's
   evidence-source field" (the flag design already proposed in T5.6's `integration_design.md`).
3. **Implement the `FtsEvidenceAdapter` and the new retrieval branch for real**, behind the flag, with its
   own dedicated unit/integration tests (none exist yet, since nothing in `app/` has been touched) —
   this task's harness is a one-off validation tool, not shippable code, and was never intended to be.

## What is already true and does not need to be re-proven

- Template reuse via source-ID + query-term gating works end-to-end, measured on 6 genuinely new
  questions this task, in addition to T5.6's own 2 — a reproducible mechanism, not a one-off demo.
- The dosing-refusal safety path is robust to FTS evidence in every tested case (4/4 dosing-related
  scenarios across T5.6 and T5.7 combined).
- Zero regression on any existing benchmark or template, confirmed twice now (T5.6, T5.7) with the second
  confirmation adding a precision refinement (EXP-1c) without disturbing the first confirmation's results.

## Final determination

```
B. PARTIAL
```
