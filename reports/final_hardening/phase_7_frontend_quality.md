# Phase 7 — Frontend & Product Quality

## Real changes made this phase

1. **Accessibility**: the query textarea had no associated `<label>` (only a placeholder, which screen
   readers don't reliably announce) — added a visually-hidden `<label for="query-input">` plus
   `aria-label` on the form and send button. `.sr-only` utility class added to `style.css`.
2. **Evidence transparency**: each evidence card now shows a short italic note when `support_type !=
   "direct"` ("Nguồn đề cập chủ đề này một cách gián tiếp, không phải chuyên biệt") or when
   `age_mismatch` is true ("Nguồn không xác nhận rõ độ tuổi cụ thể được hỏi") — the Phase 2 classification
   is now visible per-source, not just in the aggregate warning banner.

## Checklist (re-verified against the live frontend code, not assumed)

| Requirement | Status |
|---|---|
| Enter a question | Yes — `<textarea>` with `maxlength="1000"`, now labeled |
| Receive an understandable answer | Yes — template/extractive text, never a raw chunk dump with codes |
| Know whether the answer has enough evidence | Yes — distinct tags per `answer_mode`, plus the new per-source support notes |
| Open a reference source | Yes — "Nguồn N" links to `source_url` when present |
| Receive an appropriate warning | Yes — fixed safety banner + per-message tags + per-source support notes |
| No raw chunks / internal IDs / similarity / embedding / debug logs exposed | Re-checked: `app.js` never renders `rank`, `cosine_similarity`, `chunk_id`, `embedding_profile`, `model_id`, or `corpus_version` — these fields are not even present in what `/api/chat` sends to the browser (Phase 3/4 already strip them server-side) |
| Loading state | Yes, unchanged from T3 (`isLoading` bubble) |
| Empty state | Yes — "Không có bằng chứng cho câu hỏi gần nhất." when evidence is empty |
| Cache miss | Yes — distinct `QUERY_NOT_CACHED` error tag |
| Insufficient evidence | Yes — distinct tag, now also per-source notes |
| Out-of-scope | Yes — distinct tag, verified live to never show ASD evidence |
| Greeting | Yes — distinct tag, no evidence panel content |
| API errors | Yes — generic error bubble with the safe error code, never a stack trace or exception string |
| Mobile layout | CSS grid collapses to one column under 860px (unchanged from T3); not re-tested in an actual mobile browser (no device/emulator tooling in this environment) |
| Basic accessibility | Textarea/button now labeled; `aria-live="polite"` on the message log (unchanged from T3); no other ARIA audit performed (no automated accessibility checker available in this project) |
| Demo/prototype label kept honest | Yes — DEMO MODE badge, safety banner, and composer hint all still present and updated in T3 to say "không phải LLM" |
| Not marketed as a diagnostic tool | Confirmed — no page text claims diagnostic capability; the safety banner explicitly says the opposite |

## Not done (disclosed)

No real browser/device testing, no automated accessibility audit tool, no Lighthouse/axe run — none of
this tooling exists in the project and none was added, consistent with the same limitation stated in
`t3_0_test_report.md` and `phase_5_frontend.md` (T3). The checklist above was verified by reading the
actual served files and their JS behavior, not by rendering them in a browser.
