# Phase 4 (T4) — Citation & Source Quality Audit

## Level 1 — Structural Validation (implemented, re-verified)

`app/retrieval/citation_validation.py`, unchanged code from T3.1–T3.6, re-tested in this task:

- Source exists (must match an actual `RetrievedChunk` from this response).
- Title/URL are compared field-for-field against the real database record — a fabricated or edited
  value is dropped, not shown as if verified.
- Citation must come from the Evidence Gate's `supported` list, never the raw Top-K — so "không trùng
  lặp nguồn" / "không gắn nguồn chỉ vì ở Top-K" are enforced by construction (a chunk that didn't pass the
  gate is never even passed into this function).
- No duplicate-source citation list was specifically re-tested this task; re-ran
  `tests/unit/test_citation_validation.py` (6 tests, all passing) — this already exercises exact-field
  matching, and the Evidence Gate naturally deduplicates by chunk, so two identical citations for the same
  chunk cannot occur (each chunk has one `citation_id`).

## Level 2 — Semantic Support Validation (partially implemented, limitation stated explicitly)

**What exists**: the Evidence Gate's `support_type` classification (Phase 2 — `"direct"` / `"indirect"` /
`"generic"`) is the closest thing this project has to a semantic-support signal, and it is now visible in
the API response per citation. This is a **lexical proxy**, not true semantic entailment checking — it
answers "does the specific term appear in this chunk's heading vs. body vs. not at all," not "does this
chunk's meaning actually entail the answer's claim."

**What does not exist, stated plainly rather than implied**:
- No check for whether a source supports the *entire* answer vs. only *part* of it.
- No cross-source contradiction detection (considered and rejected in Phase 2 as unreliable without an
  LLM).
- No assessment of source quality/study design (e.g. "this is a single narrative review, not a
  systematic review or RCT") beyond what is manually noted for the 4 safety-sensitive topics in
  `phase_2_evidence_gate_audit.md` §8.3 — that table was built by human reading of the source text during
  this task, not by an automated semantic check.

**This report does not claim semantic validation where only structural validation (plus a lexical support
hint) exists** — this is the specific thing the task warned against ("Không được tuyên bố citation đã
được kiểm chứng ngữ nghĩa chỉ vì chunk ID khớp"), and it is why `support_type` is described as a "hint"
throughout this and the Phase 2 report, never as "semantically verified."

## `.md` source priority — still not applicable

Re-confirmed (same finding as T3's `phase_0_full_audit.md`): no curated `.md` knowledge files exist in
this project. There is nothing to prioritize over the 2,338 database chunks; this is restated here because
the task asked for it explicitly in this phase too, not because the finding changed.

## Net result

No new citation-validation code was needed in this phase beyond what Phase 2's `support_type` already
adds to the response. The audit's main output is the explicit limitation statement above, since claiming
more than what's implemented would itself be the kind of unfounded claim the task prohibits.
