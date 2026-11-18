# Phase 2 — Retrieval Quality & Evidence Sufficiency Gate

## What was built

`app/retrieval/evidence_gate.py`: `assess(query, results) -> EvidenceAssessment(sufficient, reason,
supported, unsupported_dropped)`. It **wraps** `DenseRetriever`'s output and never edits `dense.py`, so
the T2.3 benchmark (which calls `DenseRetriever` directly) is unaffected by construction — confirmed at
the end by re-running `scripts/dense_retrieval_eval.py` (see `phase_6_test_report.md`).

## 2.1 — Retrieval inspection (re-verified, not re-guessed)

The four confirmed failures from the independent expert evaluation were re-run live against the real
database before writing the gate, to check the exact current evidence (not trust a summary):

| Question | Live Top-5 (unfiltered) | Classification |
|---|---|---|
| "Vắc-xin có gây tự kỷ không?" | 4/5 chunks off-topic (Vietnamese stigma, GI symptoms, immune response) — **but rank 4 (`ASD-OA-PMC12620806`) contains**: *"the firestorm of controversy surrounding the alleged role of routine childhood vaccinations in autism... infamously suggested in a now retracted study"* | **Relevant evidence exists — it was missed in the prior report because its preview excerpt was truncated before reaching that sentence.** Corrected here. |
| "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?" | 5/5 about melatonin/antihistamines for sleep, not risperidone | No evidence — confirmed wrong-topic retrieval |
| "Tế bào gốc có chữa được tự kỷ không?" | 5/5 about genetics, Vietnam stigma, tics, research-communication barriers | No evidence at all |
| "Trẻ tự kỷ có hay bị động kinh không?" | 5/5 about anxiety/ADHD/tic comorbidity, never epilepsy/seizure | No evidence at all |

This correction matters: it means the corpus is not uniformly missing safety-critical content (the vaccine
myth *is* debunked somewhere in it), but **cosine similarity alone cannot surface it reliably** — rank 4,
not rank 1, and buried mid-paragraph. This is exactly the problem the gate below targets.

## 2.2 — Evidence Sufficiency Gate design

A chunk counts as **supporting** only if BOTH:
1. `cosine_similarity >= 0.12` (a low floor to reject pure noise — **not** used as proof of sufficiency by
   itself, per the task's explicit instruction not to rely on an arbitrary threshold alone).
2. **Topic check**: if the query contains no topic-specific glossary term (e.g. "Rối loạn phổ tự kỷ là
   gì?" — the question *is* the generic topic), the similarity floor alone is the check. If the query
   *does* contain a specific term (vaccine, risperidone, stem cell, epilepsy, school, parent, …), the
   chunk's title + section heading + content must contain a matching English/Vietnamese fragment for that
   term — **not** the generic "tự kỷ"/"autism" words, which are present in nearly every chunk and would
   make the check meaningless if counted.

When nothing qualifies, the result is `insufficient`, never a forced guess — the conservative-by-default
behavior the task requires when sufficiency can't be determined reliably.

A real bug was found and fixed while validating this against live data: the first version only checked
`chunk.content`, and missed `q007` ("Dấu hiệu sớm... 18 tháng") because the matching word ("signs") lived
in the chunk's **title** (`"Signs and Symptoms of Autism Spectrum Disorder"`), not repeated in the excerpt
body. Fixed by checking title + section + content together; regression test added
(`test_title_and_section_signal_counts_even_when_body_excerpt_does_not_repeat_the_word`).

## Live re-verification after the fix

| Question | Gate result | Matches expectation? |
|---|---|---|
| "Rối loạn phổ tự kỷ là gì?" (generic) | sufficient, 5/5 kept | Yes |
| "Dấu hiệu sớm... 18 tháng" | sufficient, 1/5 kept (the actual Signs/Symptoms chunk) | Yes |
| "Vắc-xin có gây tự kỷ không?" | **sufficient**, 1/5 kept — the retracted-study chunk | **Fixed** (was wrongly "no evidence" in the prior report) |
| "Liều risperidone..." | insufficient, 0/5 kept | Correct (no risperidone-dosing evidence exists) |
| "Tế bào gốc..." | insufficient, 0/5 kept | Correct |
| "Trẻ tự kỷ có hay bị động kinh không?" | insufficient, 0/5 kept | Correct |
| "Hôm nay thời tiết thế nào?" | never reaches the gate — rejected by the router (Phase 1) first | Correct, and more efficient (no DB call at all) |

## 2.3 — Safety-sensitive questions

Handled in `app/answer/answer_generator.py` (Phase 3), layered **on top of** (not instead of) the Evidence
Gate:
- **Medication dosing** (risperidone/aripiprazole + a dose-related word): hard refusal, *independent of
  what evidence was retrieved* — a correct-looking dosing number is never synthesized even if some chunk
  happened to mention a number.
- **Unproven-cure claims** (e.g. "tế bào gốc chữa tự kỷ") with no supporting evidence: an explicit caution
  message distinguishing "no evidence this cures ASD" from "ASD can be cured" — never silent, never a
  guess.
- Vaccine, epilepsy, and other factual safety topics are not hard-refused; they go through the normal
  gate + template/fallback path, because refusing to discuss them outright would be worse than answering
  from evidence when evidence exists (vaccine) or saying "not enough evidence" when it doesn't (epilepsy).

## Stated limitation

This lexical method cannot detect a topically-adjacent-but-wrong-condition chunk when both share the
queried specific term (e.g. ADHD-specific medication text could pass a check keyed only on "medication").
This needs real semantic understanding, unavailable without an authorized LLM (T2.6). The task's own
example of this exact risk is covered by a dedicated regression test,
`test_irrelevant_evidence_is_rejected_by_the_gate_even_when_retrieval_returns_rows`, which passes because
the **dosing safety override** (not the lexical gate) is what actually protects that specific case — the
report does not claim the lexical gate alone solves it.

## Tests

`tests/unit/test_evidence_gate.py` — 11 tests. No change to `app/retrieval/dense.py`,
`app/retrieval/embeddings.py`, `app/retrieval/query_embedding.py`, or any embedding/profile config.
