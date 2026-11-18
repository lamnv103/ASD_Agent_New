# ASD-RAG Student Demo — Limitations

This demo is a **research/student prototype**. It is not a clinical tool and has not been clinically
validated. It must not be used to diagnose autism, to replace professional consultation, or to make any
health decision. The exact required safety notice is shown on every page and in every chat response:

> Nguyên mẫu nghiên cứu/sinh viên. Nội dung chưa được thẩm định lâm sàng. Không dùng để chẩn đoán hoặc
> thay thế tư vấn chuyên môn.

## 1. Query coverage is fixed (cache-only)

Only questions whose embedding vector already exists in the local cache
(`data/index/query_embeddings/`) can be answered. In practice, this is the 66 questions in
`eval/datasets/retrieval_eval_v1.jsonl` (or anything else manually added to that cache the same way). Any
other text returns HTTP 503 `QUERY_NOT_CACHED`, by design — the system will never fabricate a vector for a
new question. See `reports/demo_mvp/t2_6_authorization_decision_matrix.md` for why: sending arbitrary
query text to Cohere has not been authorized by the project owner (status `APPROVAL_REQUIRED`).

## 2. The answer text is not AI-generated

Every answer shown is produced by `MockAnswerGenerator`: it concatenates the retrieved evidence excerpts
with a fixed disclaimer, labeled `[MOCK …]`. There is no language model synthesizing, summarizing,
reasoning over, or paraphrasing the evidence. It is meant only to exercise the UI's answer/citation
rendering, not to demonstrate answer quality.

## 3. No reranking, no query expansion

Retrieval is exact cosine search over the research vector view, in the original ranking order the
database returns — no cross-encoder reranking, no hybrid/FTS fusion, no query rewriting. Top-ranked results
can include administrative or boilerplate text (e.g., workbook instructions), as already noted in the T2.3
evaluation reports.

## 4. Evidence coverage is partial and silver-labeled

The underlying corpus has 2,338 embedded chunks from 71 documents (research track only; production
embedding remains at 0 by design — see T2.5/T2.6). The 66-question evaluation set's relevance judgments are
single-annotator "silver" labels, not adjudicated gold labels (0 human-verified as of the last recorded
check). Recall@5 on the "answerable" question group is modest (median ≈0.35 per the existing regression
metrics) — the demo can and will sometimes retrieve incomplete or tangential evidence for a cached
question.

## 5. 13 of 71 embedded sources carry an unresolved licence/provider-terms conflict

Per `reports/demo_mvp/t2_6_cohere_license_review.md`, 13 CC BY-NC / CC BY-NC-SA documents were embedded
under a research-only authorization that is separate from, and does not resolve, the Cohere trial-key
terms conflict for that content. This demo does not re-send any document text to Cohere (it only reads
already-stored vectors), but a user could still see excerpts from those 13 sources in retrieved evidence.

## 6. No personal data protection beyond a UI warning

The chat input has no server-side filter for personal or health-identifying information — if a user types
something identifying, that text is used locally to look up the cache (it is never sent anywhere external
in cache-only mode) but it is the user's own responsibility to avoid entering it, per the on-screen notice.
Do not use real patient information with this demo.

## 7. No persistence, which also means no history

Conversation text and any future feedback are not stored anywhere outside the current browser tab (no
server-side log of chat text is written; the frontend uses no browser storage either). Closing or
refreshing the page loses the conversation. This is a safety choice (nothing is retained to leak), not a
missing feature to fix later without reconsidering the same privacy trade-off.

## 8. No production path

Nothing in this demo touches the production tables (`chunk_embeddings`, `v_retrieval_ready_chunks`, etc.),
which remain at 0 rows / fully NULL permissions by project policy. This is strictly a research-track,
read-only, cache-only demonstration.

## 9. Known UX limitations

- Suggested questions must match the cached text exactly (including punctuation) to hit the cache; the
  buttons in the UI guarantee this, free typing does not.
- No streaming; the full mock answer and evidence list render at once.
- No mobile-specific layout testing was performed beyond the CSS grid's responsive breakpoint.

## 10. Remaining blockers to a "live query" demo

To move beyond cache-only, the project owner must resolve the open items in
`t2_6_authorization_decision_matrix.md` (Scenario B) and `t2_6_approval_request.md` — none of which this
task resolves or attempts to resolve.
