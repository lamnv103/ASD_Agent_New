# Phase 2 (T4) — Retrieval & Evidence Gate Hardening

## 8.1 — Retrieval baseline: confirmed untouched

No edit was made to `app/retrieval/dense.py`, `embeddings.py`, `query_embedding.py`,
`config/embedding_profiles.json`, or `config/retrieval_profiles.json` in this task. The only new file is
`app/retrieval/evidence_gate.py`, which wraps the retriever's output and is called from `app/api.py`
*after* `DenseRetriever.retrieve()` returns — it cannot affect what the benchmark script
(`scripts/dense_retrieval_eval.py`, which never imports this module) sees. Re-confirmed by re-running the
regression at the end of this task (Phase 8): 66/66, identical.

## 8.2 — Evidence Gate: from binary to classified support

The T3 gate only returned `sufficient: bool`. This task adds `EvidenceAssessment.details: list[SupportDetail]`,
one entry per kept chunk, each carrying:

- **`support_type`**: `"direct"` (the specific term the query asked about is in the chunk's **title or
  section heading** — this chunk is actually about that topic), `"indirect"` (the term only appears in
  the body text — the chunk mentions it but may not be centrally about it), or `"generic"` (the query had
  no specific term to check, e.g. "what is ASD?" — support rests on similarity alone, a weaker signal,
  now labeled as such instead of silently treated the same as "direct").
- **`age_mismatch`**: `True` when the query names a specific age (regex for "`<number> tháng/tuổi/month/
  year`") that the chunk's content does not corroborate with a nearby number — directly answering the
  task's explicit requirement to check "câu hỏi có độ tuổi cụ thể."

`support_type` and `age_mismatch` are now in the `/api/chat` response's `evidence` array (verified live),
and `/api/chat` appends a "Giới hạn" warning when **all** kept evidence for an answer is indirect/generic,
or when an age mismatch is detected — surfacing the distinction to the user instead of only to internal
logic.

**What this does NOT do** (stated, not hidden): it does not implement true "partial" (some but not all of
a multi-part question answered), "contradictory" (two sources disagreeing), or "indirect-via-inference"
support detection. Building a real contradiction detector needs semantic comparison between sources, which
needs an LLM (not authorized) — attempting a lexical approximation here (e.g. "look for negation words
near shared terms") was considered and rejected as more likely to produce false contradiction flags than
real ones; it is listed as a recommended next step in `remaining_issues.md` rather than faked.

## 8.3 — Safety evidence policy for the four sensitive topics (re-verified live, with the new classification)

| Topic | Source says | Quality/limits | Supported conclusion | Not concludable |
|---|---|---|---|---|
| Vaccine–autism | A narrative review (`ASD-OA-PMC12620806`) states the claim traces to "a now retracted study" | Single secondary source (a review, not a primary RCT); `support_type: "indirect"` (the term is in the body, not a dedicated vaccine-safety section heading) — flagged to the user accordingly | No causal link established; the original claim's source was retracted | This single review does not constitute an exhaustive vaccine-safety literature review — the template says what the evidence says, not "vaccines are proven 100% safe in all respects" |
| Risperidone dosing | No chunk in the Top-5 for this question mentions risperidone at all | N/A — no evidence | Nothing — correctly refused regardless (Phase 3 safety override, independent of evidence quality) | A specific dose, ever, from this system |
| Stem-cell "cure" | No chunk in the Top-5 mentions stem cells | N/A — no evidence | Nothing — explicit caution issued instead of silence | That stem cells do or don't work — the system states it doesn't know, not that the answer is "no" |
| Epilepsy comorbidity | No chunk in the Top-5 mentions epilepsy/seizures (only anxiety/ADHD/tic comorbidities) | N/A — no evidence | Nothing | The system does **not** claim "autism and epilepsy are unrelated" — it says it found no evidence, which is a different, weaker, and correct claim |

No single weak source is escalated to a strong claim: the vaccine template's wording ("các tổng quan y văn
không tìm thấy bằng chứng..."/"literature reviews find no evidence...") was re-checked in this task and
confirmed to state what the evidence says, not an absolute scientific certainty. No change to this
template's text was needed, but the `support_type: "indirect"` flag now accompanies it so the UI can show
the "chỉ đề cập chủ đề này gián tiếp" (only indirectly addresses this topic) limitation note — previously
this nuance existed only in a report, not in the live API or UI.

## Tests

`tests/unit/test_evidence_gate.py` grew from 11 to 17 tests, adding direct/indirect/generic classification
and both age-mismatch directions. All pass; see `phase_8_test_report.md`.
