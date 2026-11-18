# Phase 5 — Frontend & User Experience

## Changes made (`frontend/app.js`, `frontend/style.css`, `frontend/index.html`)

1. **Evidence cards no longer show a bare citation code as the primary label.** Previously the card header
   showed the literal `citation_id` ("C1", "C2", …) next to the source ID. Now each card is headed
   "Nguồn 1", "Nguồn 2", … (sequential display position), and the source name is a clickable link to
   `source_url` when present (falls back to plain text with the source ID if a URL is ever missing).
2. **Mode labeling overhauled** (`tagsForMode()` in `app.js`): the old single `"MOCK ANSWER"` tag is
   replaced with one label per actual `answer_mode` — `topic_template` → "MẪU CÓ KIỂM CHỨNG NGUỒN (KHÔNG
   PHẢI LLM)", `extractive_fallback` → "TRÍCH DẪN TRỰC TIẾP (CHƯA CÓ BẢN TỔNG HỢP)",
   `safety_refusal_dosing` / `safety_caution_unproven_cure` → a bold red "TỪ CHỐI VÌ AN TOÀN" /
   "CẢNH BÁO" tag, `greeting_template` → a distinct greeting tag, `out_of_scope` and
   `insufficient_evidence` → distinct muted tags. Every label is honest about the mechanism — none claims
   LLM generation.
3. **Composer disclaimer text updated** from "Mọi câu trả lời ở đây là MOCK" (no longer accurate — some
   answers are now grounded templates, not placeholder mock text) to an accurate statement that answers
   are template- or extraction-based, never an LLM, with the per-message tag stating which.

## What the UI still does, confirmed correct against the task's Phase 5 checklist

| Requirement | Status |
|---|---|
| Show user question | Yes (unchanged) |
| Show Vietnamese answer | Yes |
| Show source name or link | Yes — **now with a working link**, not just a name (Phase 4) |
| Show "insufficient evidence" notice | Yes — distinct tag + the `insufficient_evidence`/`safety_*` modes read directly from the API, not inferred client-side |
| Appropriate safety warning | Yes — the fixed safety notice banner (unchanged from T3.0) plus per-message safety tags for refusal/caution modes |
| Hide raw chunks/embedding/rank/similarity/internal IDs | Yes — the evidence card never rendered `rank`/`cosine_similarity`/`chunk_id` even before this task; the one remaining literal-code leak (`citation_id` as a visible label) is fixed in this phase |
| Distinguish demo mode / "not an LLM" / unclinical content | Yes — DEMO MODE / CACHE-ONLY badges (unchanged, still live from `/api/system/status`) plus the new per-mode tags |

## Not done in this phase (explicitly out of scope, not hidden)

No visual regression test or browser screenshot was captured — this project has no JS test runner or
headless-browser tooling, and none was added (same constraint noted in `t3_0_test_report.md` §6). The
`GET /` static-serving test (`test_frontend_is_served_at_root`) continues to pass, confirming the files are
served, but does not verify rendered appearance.
