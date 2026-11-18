# T5.3 Phase 4 — Fallback Quality Audit

All six properties re-verified live against the real database this task, not assumed from prior
reports.

| Property | Verified how | Result |
|---|---|---|
| Fallback clearly identified | `answer_mode: "extractive_fallback"`, distinct frontend tag "TRÍCH DẪN TRỰC TIẾP (CHƯA CÓ BẢN TỔNG HỢP)" (unchanged from T4 Phase 7) | Pass |
| English excerpts not misrepresented as Vietnamese | Every fallback answer's fixed preamble sentence ("Hệ thống chưa có bản tổng hợp tiếng Việt được kiểm chứng... dưới đây là trích dẫn trực tiếp từ nguồn") is itself Vietnamese and explicitly says the excerpts that follow are *not* a translation/synthesis — re-read the literal string in `app/answer/answer_generator.py:generate()`, unchanged | Pass |
| No unsupported translation/paraphrase | `extractive_fallback`'s code path (`generate()`'s final branch) only ever does `_truncate(item["excerpt"])` — a length cut, never a translation call (no translation library/API imported anywhere in `answer_generator.py`, confirmed by `grep`) | Pass |
| Insufficient evidence reported honestly | Distinct `answer_mode: "insufficient_evidence"`, distinct `retrieval_status: "insufficient_evidence"`, fixed Vietnamese text stating the system could not find adequate evidence — re-verified live for qe063 (epilepsy) this task | Pass |
| Cache miss distinguished from evidence insufficiency | Cache miss → HTTP 503, `error.code: "QUERY_NOT_CACHED"`, `retrieval_status: "blocked_uncached"` (re-verified live for an unanswered paraphrase this task). Evidence insufficiency → HTTP 200, `retrieval_status: "insufficient_evidence"`, no error object. These are structurally different response shapes (one is an HTTP error, the other is a normal 200 with an honest content), not just a different string | Pass |
| Safety refusal takes precedence | Re-verified live: `"Liều risperidone cho trẻ tự kỷ 5 tuổi là bao nhiêu?"` (a question that also contains the ASD anchor and could plausibly retrieve evidence) returns `safety_refusal_dosing`/`refused_before_retrieval` with **zero** evidence items — confirming the dosing check runs and short-circuits before the embedder or database is ever touched, not just before a template is selected | Pass |

## No regressions introduced by this task's gating fix

The Phase 1 fix (adding query-term gates to 6 templates) only changes **when a template fires**, never
the fallback code path itself — `extractive_fallback`'s logic (`generate()`'s final `lines.append(...)`
block) was not touched. Re-confirmed by `test_no_template_matches_falls_back_to_labeled_extractive_
presentation` (pre-existing, still passing) and the 2 new negative tests that now correctly land in
fallback after the fix (`test_t5_3_fix_...`).
