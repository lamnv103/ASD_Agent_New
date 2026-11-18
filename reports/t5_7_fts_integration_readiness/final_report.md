# T5.7 — FTS Integration Readiness & End-to-End Validation — Final Report

## Scope re-stated

Verify whether T5.6's proposed FTS-integration design (reuse live Vietnamese answer templates by adapting
FTS evidence into the same `RetrievedChunk` shape dense retrieval uses) is ready for isolated,
flag-gated integration — using "ASD là gì?" as the user-accepted Answer Quality Reference. Strictly
`app/`-unmodified throughout the audit and validation phases, per explicit instruction. One new, isolated,
rollback-only test harness (`scripts/t5_7_e2e_harness.py`) was added; nothing in `app/` was touched.

## What this task found, by phase

- **Phase 0**: re-verified `app/` unmodified since T5.5/T5.6; T2.3 regression byte-identical; T2.6
  unchanged. Also caught a gap in T5.6's own worked example (its "ASD là gì?" demonstration relied on a
  hand-built tsquery that happened to exclude a problematic term, without documenting that exclusion as a
  rule) — corrected in Phase 1.
- **Phase 1**: found that a **bare, short acronym term ("ASD")**, not just the "autism" concept itself,
  behaves like a generic anchor and causes the same OR-dilution problem T5.6 already fixed for "autism" —
  a refinement (EXP-1c: prefer multi-word phrase forms in the anchor-only fallback) was built and verified
  to fix this without regressing any of the 6 frozen-set cases. `can thiep` and `chua noi` were
  re-examined in context (per instruction, not removed): `can thiep` is a genuine, necessary term whose
  problem is conditional reliability, not wrongness; `chua noi`'s risk was downgraded from "confirmed" to
  "plausible, not reproduced" after this task's own testing found no live misfire traceable to it.
- **Phase 2**: reused T5.6's glossary mapping (unchanged); proposed a unified term-management schema
  (provenance + specificity/reliability metadata) that would let a future task record exactly the
  nuance Phase 1 found — not built, not auto-merged, per instruction.
- **Phase 3**: 22 new, independently-authored questions across all 11 required topic groups, run through
  the real `evidence_gate` → `answer_generator` → `citation_validation` chain via the harness. **6 of 22
  reached a genuine, cited, structured Vietnamese answer that is a cache-miss today** (4 topic groups);
  10 fell to honest `extractive_fallback`; 2 honestly declined (`insufficient_evidence`); 4 already met
  the reference today, unaffected. **0 of 22 produced a wrong or fabricated answer.**
- **Phase 4**: 11 safety/false-positive scenarios tested against the real pipeline. **10 safe. 1
  confirmed, reproduced risk**: the unproven-cure safety caution (`safety_caution_unproven_cure`) is only
  shown when the evidence list is empty (`app/answer/answer_generator.py`'s own, unmodified condition) —
  FTS's broader recall can populate that list with weak, topically-adjacent-but-substantively-irrelevant
  evidence (demonstrated live with the vitamin-B6 cure-claim question), silently replacing the caution
  with a neutral raw-excerpt fallback that never states the claim is unsupported. Dosing refusal, by
  contrast, is unconditional and was confirmed robust in every tested scenario.
- **Phase 5**: full regression clean — 454/454 tests, T2.3 identical, the 32-question independent set
  identical to every prior run (because zero `app/` code changed) — with an explicit anti-overfitting
  disclosure that the EXP-1c refinement was validated against the frozen set, the original 31, and this
  task's own separate 22, not tuned to inflate any single one of them.
- **Phase 6**: **B. PARTIAL** — not A, because of the confirmed Finding #6 safety risk and the remaining
  coverage/precision gaps; not C, because authorization, data integrity, and the dosing-safety path are
  all fully intact, with a clear, narrow, already-understood path to A.

## Protected boundaries — compliance re-confirmed

- `ASD_DEMO_MODE=true`, all `ENABLE_LIVE_*` flags `False`, unchanged throughout.
- No Cohere, LLM, or reranker call at any point; every retrieval action was `research_reader` read-only
  SQL (FTS, no embedding) or local Python logic.
- No write to the DB; no change to the 2,291 retrievable chunks, their vectors, the embedding
  model/dimension, any corpus/annotation/frozen-benchmark file, any sealed/reveal file, the DB
  schema/roles/permissions, or Docker's running state (already up throughout). No Git commit/push.
- **`app/` was not modified at any point in this task.** The only new file is
  `scripts/t5_7_e2e_harness.py`, isolated, never imported by `app/api.py` or any other production path,
  rollback = delete the file. Full unit-test suite (404 tests) re-run after all work: unchanged pass
  count, confirming zero interference.

## Final status

```
T5_7_PARTIAL
```

(Mapped from Phase 6's required B/A/C scale — `B. PARTIAL` — into this project's standing
COMPLETE/PARTIAL/BLOCKED convention for consistency with every prior T5.x final-status line.)

**Rationale**: every phase was completed with evidence measured by actually running the real, unmodified
downstream pipeline against experimentally-adapted data — not predicted, not asserted. The design is
closer to integration-ready than at any prior point in this project (a working, reproducible mechanism
for reaching 6 new structured-Vietnamese-answer cases with zero new template code), but it cannot be
called `T5_7_COMPLETE` or "ready for isolated integration" while a confirmed safety-message-suppression
risk remains open and unfixed, and cannot be called `T5_7_BLOCKED` while every protected boundary, the
dosing-safety path, and the core data integrity guarantees all remain fully intact. This is **not**
`DEMO_READY_FOR_USER_VALIDATION`, which this report does not claim.
