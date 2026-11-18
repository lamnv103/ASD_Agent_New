# Phase 4 — Source & Citation Validation

## The confirmed bug and its fix

`RetrievedChunk.source_url` (`app/retrieval/types.py`) was already populated from real database records
but `app/api.py`'s `_chat_evidence()` omitted it from the `/api/chat` response. Fixed: `source_url` is now
included in every `evidence` item and every `citations` item. Verified live — every evidence item for
`"Rối loạn phổ tự kỷ là gì?"` now carries a real, working NIH/CDC URL
(e.g. `https://www.nimh.nih.gov/health/publications/autism-spectrum-disorder`).

`/api/retrieve` (the T2.5 raw passthrough route) was **not** touched — it still returns exactly the same
shape as before this task, confirmed by the fact that no `/api/retrieve` test needed any change.

## Citation Validation

New module: `app/retrieval/citation_validation.py`, `validate(evidence_items, supported_chunks) ->
list[dict]`. Checked against the task's 6 required points:

1. **Nguồn tồn tại** — a citation is dropped unless its `citation_id` matches an actual chunk in
   `supported_chunks` (the set the Evidence Gate already judged topically supporting).
2/3. **Tên/URL không bịa** — every field (`source_id`, `title`, `source_url`, `excerpt`) is compared
   field-for-field against the real `RetrievedChunk`; any mismatch drops the citation rather than showing
   an unverified value.
4/5/6. **Thực sự hỗ trợ / không chỉ vì ở Top-K / không đưa nguồn không liên quan** — enforced upstream:
   this function is only ever called with the Evidence-Gate-filtered `supported` list, never the raw
   Top-K, so a chunk that merely appeared in the ranking without being judged on-topic never reaches
   validation at all.

`app/api.py`'s `/api/chat` now calls `validate_citations(_chat_evidence(gate.supported), gate.supported)`
before constructing the response, and further narrows the result to only the sources the generated answer
actually cites (`answer.citation_ids`) — so a template grounded in 1 of 4 approved sources shows only that
1 source, not all 4.

## Tests

`tests/unit/test_citation_validation.py` — 6 tests: a genuine match passes; a citation not in the
supported set is dropped; a fabricated URL, a fabricated title, and an altered excerpt are each
independently dropped even when everything else matches.

## Result

Live: every citation shown by `/api/chat` now has a name **and** a working URL, satisfying the task's
"tên tài liệu hoặc đường link" requirement with both, not just the name as before.
