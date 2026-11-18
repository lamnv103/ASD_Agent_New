# T5.9 — Residual Safety Gap Assessment — Final Report

## Scope re-stated

Independently assess T5.8's deliberately unresolved B8 classifier gap ("which drug and what dose,"
unnamed drug) and determine whether this residual risk is acceptable before any future FTS integration.
Audit and assessment only — **no `app/` or `tests/` file was modified in this task**, confirmed by direct
diff against T5.8's end state (zero files changed outside new, isolated report/script files).

## What this task did, by phase

- **Phase 0**: re-verified B8's exact query, its classifier non-match, and — critically — a nuance T5.8's
  own summary table did not state precisely: B8's "actual behavior" in T5.8 described only the
  FTS-harness-simulated outcome, not what the *live, currently-deployed* demo actually does for this
  query (a plain cache-miss, since FTS is not integrated). Also re-confirmed, directly, that no live
  topic template can fire for a B8-shaped query regardless of evidence — bounding the worst case before
  any risk assessment was attempted.
- **Phase 1**: built the required 5-category boundary (direct dosing / self-management / research /
  educational / ambiguous), with each category checked directly against the live classifier, showing
  precisely why the boundary collapses only for category E (no drug, no number — the exact shape
  lexical matching cannot resolve without semantic understanding).
- **Phase 2**: **26 newly-authored adversarial test cases** (exceeding the required 25). Confirmed B8's
  shape generalizes across 6 independently-phrased Category-E variants. **Found 3 additional,
  independent classifier defects beyond B8 itself**: two new false negatives (asking for an mg amount
  without stating one; an adjustment verb with a modifier inserted before "liều") and — more
  significantly — **one confirmed, already-live false positive**: the bare phrase "thuốc tâm thần"
  causes purely educational questions to be wrongly refused with the dosing-refusal message, a bug that
  predates T5.8 and is unrelated to FTS entirely.
- **Phase 3**: assessed all 4 findings against the 6 required questions, declining to estimate real-world
  prevalence (no data exists) and declining to make clinical adequacy claims. Key conclusion: the harm
  from under-refusal (B8 and its siblings) is structurally bounded (no template can fire; no specific
  wrong dose can be fabricated), while the harm from the newly-found over-refusal (Finding 4) is a
  concrete, already-reachable usability/trust cost, independent of retrieval.
- **Phase 4 (FTS interaction)**: traced each finding through 3 conditions (classifier alone / live today
  / FTS-harness-simulated). Found that FTS changes *reachability*, never *classification*, for all 4 —
  and, on closer inspection of the actual template text (not just its mode label), found that Finding 2's
  FTS-reachable outcome already contains its own doctor-redirect sentence, making it less alarming in
  practice than its mode label alone suggested — a correction this task made by reading actual output
  text, per its own "do not assume the summary captures every nuance" instruction.
- **Phase 4 (recommendation)**: `B. RECOMMEND_NARROW_FIX` for Findings 2–4 (each with a sketched,
  not-implemented fix and the specific false-positive/false-negative tests any future implementation must
  pass), paired with `A. ACCEPT_WITH_DOCUMENTED_RESIDUAL_RISK` specifically for B8/Category E, since no
  narrow fix for that shape was found that does not reintroduce the exact over-broadening risk T5.8 and
  this task both independently verified.

## Direct answer to what "T5.9 completion" means, restated per the task's own framing

This task **does not** claim the classifier has been fixed (it has not — no `app/` change was made) and
**does not** claim the product has been clinically validated (no ASD expert has reviewed any part of
this project, restated here as it has been in every prior T5.x task). It **does** claim an independent,
evidence-based assessment of the residual risk is now documented, with concrete reproduction evidence
for every finding (not asserted, measured) and a clear, bounded, honestly-scoped recommendation.

## Protected boundaries — compliance re-confirmed

- No `app/` file modified (re-confirmed via direct diff against T5.8's end state: zero files outside
  `__pycache__`).
- No `tests/` file modified.
- No corpus, DB schema, permission, or production write; Docker was already running throughout, not
  started/stopped by this task; no Cohere/LLM call; no live query embedding; no FTS integration; no
  sealed/reveal file access; no Git commit/push.
- Two new, isolated, read-only scripts were added (`scripts/t5_9_residual_safety_tests.py`), calling only
  the pre-existing, unmodified `app.answer.answer_generator` functions and the pre-existing, unmodified
  T5.7 harness — consistent with "read-only inspection and isolated temporary test scripts are permitted
  only if they do not alter protected project files."
- Full regression (414 unit + 50 integration tests) re-confirmed unchanged after this task's work,
  because no file it depends on was touched.

## Final status

```
T5_9_COMPLETE
```

**Rationale**: the residual risk has been independently assessed, with concrete reproduction evidence
(not assumptions) for the original B8 finding and 3 further findings this task's own required
adversarial testing surfaced, a defensible recommendation with explicit trade-offs, and narrow-fix
sketches with their required pass/fail tests for a future, separately-authorized implementation task.
This status means the assessment is complete — it does **not** mean the classifier has been fixed, and
it does **not** mean this project is ready for real users or has received clinical validation, which
this report explicitly does not claim.
