# Phase 3 (T4) — Answer Quality & Generation Audit

Per the task's explicit instruction: unit tests passing is **not** treated as proof the 7 templates are
correct. Each was re-read against its real trigger evidence (re-fetched live from the database during
this task) and checked for scope, accuracy, completeness, naturalness, and overclaiming risk.

## 9.1 — Per-template audit

| Template | Trigger source(s) | Scope check | Accuracy check | Overclaim check | Verdict |
|---|---|---|---|---|---|
| `asd_definition` | NIH-NIMH-ASD-2025, CDC-ASD-CLINICAL | Only fires for "what is ASD"-type questions (no specific term) | Every clause traces to the source ("developmental disorder," "communication/social interaction," "restricted/repetitive behaviors," "characteristics vary") | None — "biểu hiện khác nhau ở mỗi người" mirrors the source's own "range of characteristics, needs, strengths, and challenges" | OK, unchanged |
| `risk_factors` | CDC-ASD-ABOUT | Fires on risk-factor questions | Sibling/genetic conditions/birth complications/older parents — all 4 items trace directly to the source | Explicitly states "không có một nguyên nhân duy nhất" and "không có nghĩa là trẻ chắc chắn mắc ASD" — actively prevents the overclaim risk named in the task (correlation vs. causation) | OK, unchanged |
| `screening_age` | CDC-ASD-SCREENING, CDC-CONCERNED | Fires on screening-age questions | 9/18/30-month general + 18/24-month ASD-specific — matches both sources exactly, including the AAP attribution | None | OK, unchanged |
| `dsm5_criteria` | CDC-ASD-CLINICAL | Fires on DSM-5/criteria questions | 2-domain + 2-of-4 structure, 3 severity levels — matches the source | None | OK, unchanged |
| `diagnosis_process` | NIH-NIMH-ASD-2025 | Fires on "how is it diagnosed" questions | "No single medical test," "diagnosis from age 2," explicit self-assessment limit — matches source | Already states the self-assessment limitation the task requires (Phase 3.4) | OK, unchanged |
| `aba_intervention` | CDC-ASD-TREATMENT | Fires on ABA/behavioral-intervention questions | "Most evidence for treating ASD symptoms" is a direct paraphrase of the source's own wording, not an invented superlative | None | OK, unchanged |
| `vaccine_myth` | ASD-OA-PMC12620806 | Fires on vaccine-autism questions | States the claim traces to "a now-retracted study" — directly from the source | Checked specifically for the task's "không biến một nghiên cứu đơn lẻ thành kết luận khoa học tuyệt đối" rule: the template says what this one review states, not "science has proven vaccines 100% safe"; `support_type: "indirect"` (Phase 2) now accompanies it in the API so the UI can show that this evidence only indirectly addresses the question, rather than presenting it with the same confidence as a `"direct"` match | OK, unchanged text; now paired with the new indirect-support flag for transparency |

**No template text required a correction.** The real issue found in this phase was not inside the
templates themselves but in how confidently their evidence was presented — fixed structurally in Phase 2
(the `support_type`/`age_mismatch` flags), not by rewriting template prose.

## 9.2 — Answer generation policy, re-checked

- **Extractive fallback** (`app/answer/answer_generator.py`): presents excerpts verbatim, numbered, never
  merges two unrelated excerpts into one sentence, never adds a causal connector between them. Re-read
  during this task; unchanged, still correct.
- **No template "papers over" missing evidence**: `insufficient_evidence`, `safety_refusal_dosing`, and
  `safety_caution_unproven_cure` remain separate, explicit modes — a template never fires without its
  specific trigger source present (enforced by `_template_for()`, tested).
- **Not called an LLM anywhere** — re-confirmed by grep: no string "LLM" appears attached to any of these
  modes in a way that would claim AI generation; the frontend tags explicitly say "KHÔNG PHẢI LLM."

## 9.3 — Output contract

The task's suggested text layout ("**Câu trả lời**" / "**Nguồn**" / "**Giới hạn**" as in-text headers) is
implemented as **structured JSON fields** instead of in-text headers: `answer` (the content), `citations`
(name + URL, rendered as a separate linked panel by the frontend), and `warnings` (holds the "Giới hạn"
content — now including the new support-type/age-mismatch notices from Phase 2). This is a deliberate
architectural choice for a web UI (the frontend already renders these as visually distinct sections —
see `phase_5_frontend.md`/Phase 7 below) rather than a gap; a plain-text-only interface (e.g. a CLI) would
need the headers inlined, which is not this project's interface.

## 9.4 — Answer length by question type, re-checked

| Type | Observed (live) | Matches the task's guidance? |
|---|---|---|
| Definition | 2 sentences | Yes — short but complete |
| Risk factors | 2 sentences + explicit "no single cause" framing | Yes |
| Screening age | 1 sentence, 2 concrete age ranges | Yes |
| DSM-5 criteria | 2 sentences covering both domains + severity levels | Yes |
| Diagnosis process | 2 sentences incl. the self-assessment limit | Yes |
| Signs (q007-style) | Falls to extractive excerpt (no template) — necessarily longer, literal source text | Honest, not padded — the length comes from showing the real excerpt, not from artificially expanding a short answer |
| Multi-part questions | No template decomposes a compound question into parts | **Not solved in this task** — falls to extractive fallback, which does not reorganize the excerpt by sub-question. Listed in `remaining_issues.md`. |

No template was found to be artificially lengthened "to look complete" — each is as short as its source
material supports, consistent with the task's "không mở rộng câu trả lời chỉ để làm cho nó có vẻ đầy đủ"
rule.
