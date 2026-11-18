# T6.0 Phase 4 ? Hybrid architecture proposal

**Design only.** No Hybrid code or app route was implemented.

## Recommended candidate pipeline for an offline T6.1 experiment

1. Validate request/query and K at each retriever boundary.
2. Run existing Dense retrieval only when an authorized compatible vector is available; in the current configuration, this means a cache hit for a known evaluation query. Preserve fail-closed behavior on a miss.
3. Run the selected FTS profile against the same authorized view and research reader.
4. Build the candidate union and deduplicate by stable `chunk_id`. If the same chunk is returned twice, retain per-retriever rank/score records and verify that its content hash and source/provenance agree. A conflict must fail closed and be surfaced, not silently resolved.
5. Apply an explicitly chosen rank fusion (RRF is the first method to test) using ranks only. Retain raw retriever ranks/scores separately. Never add cosine similarity to `ts_rank_cd`.
6. Pass actual source metadata, content hash, authorization ID, and retriever evidence into a typed evidence contract. Existing Evidence Gate currently relies on dense-style similarity/lexical checks; do not invent a cosine score for FTS. FTS support needs a separately designed, tested evidence representation before any answer-generation integration.
7. Return fused candidates with deterministic tie-breaking and complete provenance. Any future answer stage must cite source metadata from the retrieved chunks and preserve the current safety refusal/fallback behavior.

## Data contract to preserve

For each chunk: `chunk_id`, `source_id`, `document_id`, title, URL, section/page/character span, content, content hash, corpus/document version, authorization version, and for each retriever the raw rank/score type/profile. A fused rank is derived provenance and must not replace individual ranks.

## Failure policy

- No authorized dense vector: report Dense unavailable; do not call external embedding.
- Database/view or permission failure: fail closed; no base-table or elevated-role fallback.
- One retriever failure: for research experiments, record it explicitly and report whether the run is partial; do not silently label it as full Hybrid. For a future user-facing service, fail closed unless a separately approved degraded-mode policy defines acceptable behavior.
- No candidates, conflicting provenance, invalid/duplicate IDs, missing required citation fields, or gate inability to interpret FTS evidence: do not produce an answer.

## Proposed ranking option

Evaluate reciprocal rank fusion as the first controlled method: `RRF(chunk) = ?_r 1/(c + rank_r(chunk))`, with candidate ranks preserved and fixed deterministic tie-breaks. Test a small prespecified set of `c` values; do not tune against the same 66-query benchmark and present it as generalization. Candidate union without fusion can serve as a diagnostic baseline; weighted score blending is deferred until relevance labels and score calibration exist.

This design is a proposal for an isolated research evaluation. It is not authorization to call Cohere, change database schema/indexes, ship an endpoint, or use Hybrid for clinical decisions.
