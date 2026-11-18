# T5.1 §3 — Topic Gap Matrix

Built directly from `answer_coverage_audit.md`'s per-question data (`eval/reports/t5_1_audit_raw.json`).
Every question is placed in exactly one of the 7 required groups.

## Group A — Đã có template và đạt yêu cầu (12 questions)

Real Vietnamese answer, fact-checked in `reports/final_hardening/phase_3_answer_quality.md` §9.1, no
correction needed there or in this audit.

| Topic | Questions | Trigger source(s) |
|---|---|---|
| ASD definition | qe001 | NIH-NIMH-ASD-2025, CDC-ASD-CLINICAL |
| Risk factors | qe104 | NIH-NIMH-ASD-2025 |
| Repetitive behaviors list | qe015 | CDC-ASD-CLINICAL, NIH-NIMH-ASD-2025 |
| Diagnosis process | qe035 | NIH-NIMH-ASD-2025, CDC-ASD-CLINICAL |
| Screening age | qe038 | NIH-NIMH-ASD-2025 |
| DSM-5 criteria | qe039 | CDC-ASD-CLINICAL |
| Early-intervention benefit | qe042 | CDC-ASD-ABOUT |
| ABA | qe043 | CDC-ASD-TREATMENT |
| Medication (no-cure-drug framing) | qe046 | NIH-NIMH-ASD-2025 |
| GI comorbidity | qe062 | ASD-OA-PMC12620806 |
| Vaccine myth | qe073 | ASD-OA-PMC12620806 |
| GFCF diet myth | qe075 | ASD-OA-PMC12620806 |

## Group B — Có template nhưng chưa đầy đủ (0 questions)

**None found.** No case in this audit showed a template firing on a topic it does not fully cover — the
7 templates are narrow and gated strictly to their trigger source, so partial coverage inside a single
template was not observed. (This differs from "topic has no template at all," which is Group C below.)

## Group C — Có evidence tốt nhưng chưa có template (20 questions)

`extractive_fallback` whose evidence is **not** all-`generic` (i.e. at least one `direct` or `indirect`
chunk — the Evidence Gate correctly found on-topic evidence; the only gap is the missing Vietnamese
template). Computed directly from `eval/reports/t5_1_audit_raw.json` (not hand-counted) as "fallback AND
NOT all support_type == generic":

| Questions | Topic | Support quality |
|---|---|---|
| qe017 | Narrow interests and learning impact | `indirect` |
| qe028, qe029 | Early signs at a specific age | `direct` |
| qe023, qe024, qe025 | Sensory integration therapy | `direct`-majority |
| qe031 | Autism in adolescence | mixed direct/indirect |
| qe034 | Speech delay vs. ASD | `indirect` |
| qe036 | M-CHAT-R/F | `direct`-majority |
| qe037 | ADOS-2 | mixed direct/indirect |
| qe041 | Vietnam screening/diagnosis context | `direct` |
| qe044 | NDBI intervention | `direct` |
| qe045 | Parent-delivered intervention | `direct` (**but includes the q033-class ADHD confusion — see `q033_context_analysis.md`**) |
| qe047, qe048 | Sleep without medication / melatonin efficacy (not dosing) | `direct` |
| qe049 | School inclusion | `direct`-majority |
| qe051 | Home vs. school intervention priority | `direct` |
| qe056, qe057 | Caregiver behavior support / WHO caregiver training | `direct`-majority |
| qe081 | ASD+ADHD comorbid sleep support | `direct` (same ADHD-confusion risk as qe045) |

These are the **best, lowest-risk candidates for new templates** — see `template_expansion_plan.md`.

## Group D — Chỉ có evidence tiếng Anh (25 questions — same set as `extractive_fallback` overall)

Every one of Group C plus Group E below. Restated as its own group because it is literally what the
task asked to separate out: **100% of fallback answers (25/25) draw on English-language source text**;
0 draw on Vietnamese-language source text. There is no sub-case in this corpus of "good evidence that
happens to already be in Vietnamese" — the 65 non-CDC/NIH sources in this corpus (PMC articles, WHO
guidelines, UK/international trials) are uniformly English, and even the few Vietnam-focused papers
(e.g. `ASD-OA-PMC13005892`, `ASD-OA-PMC6487529`) are written in English academic prose about Vietnam,
not in Vietnamese.

## Group E — Evidence chưa đủ hoặc không phù hợp (9 questions)

Evidence that is only `generic` (similarity-only, no specific-term match) or entirely absent:

| Questions | Why |
|---|---|
| qe021, qe022, qe033, qe053, qe105 | `extractive_fallback` with **all-`generic`** support — evidence is topically plausible but not confirmed on the specific sub-topic asked (e.g. qe033 asks about sex differences in signs; evidence is generic ASD-signs/GI/stigma content, not sex-difference-specific) |
| qe063/qe093 (same question, appears twice) | `insufficient_evidence` — no epilepsy-specific evidence found (known from T3/T4) |
| qe074 | `safety_caution_unproven_cure` — no stem-cell evidence found, correctly handled as caution rather than silence |
| qe014 | `insufficient_evidence` — no adequate evidence for teen social-skills-training efficacy |

## Group F — Cache miss do giới hạn T2.6 (50 questions)

Exactly the 50 rows marked `cache_miss_T2.6` in `answer_coverage_audit.md`. Spans every category roughly
proportionally (e.g. 7/9 `definition` questions blocked, 6/7 `social_communication`, 8/8 of the
genuinely novel `multi_aspect` phrasings). **Not reducible without T2.6 authorization or expanding the
cache through the existing authorized research process** — this is the single largest "reason not
Vietnamese" bucket by count, but it is an authorization gap, not a template/evidence-quality gap.

## Group G — Câu hỏi cần chuyên gia ASD xem xét

Not mutually exclusive with the groups above — these are flagged on top of their primary group because
their content, not just their language, needs a qualified reviewer:

| Questions | Why an ASD expert should look |
|---|---|
| qe045, qe081 (Group C) | The ADHD-vs-ASD evidence-confusion risk — an expert should judge whether the parenting/sleep advice shown is appropriate to present even with the caveat, or should be withheld until fixed |
| qe033 (Group E) | Sex-difference-in-presentation question — generic evidence risks under-informing on a clinically real phenomenon (girls are often under-diagnosed); an expert should assess whether "insufficient" would be a safer answer than the current generic fallback |
| qe073, qe075 (Group A, templates) | Both are public-health-myth corrections (vaccines, GFCF diet) — already reviewed for wording in `phase_3_answer_quality.md`, but no clinician has confirmed the phrasing is optimal for a lay Vietnamese audience |
| qe067–qe072 (medication_sensitive, correctly refused) | Not a content risk (refused), but an expert should confirm the refusal *wording itself* ("hỏi bác sĩ nhi khoa hoặc bác sĩ tâm thần") uses terminology Vietnamese parents would find natural/trustworthy |
| qe063/qe093 (epilepsy, insufficient) | An expert should confirm whether "insufficient evidence" is the right framing or whether this corpus genuinely lacks adequate epilepsy-comorbidity sourcing and should be flagged for corpus expansion (a T2.6/data question, not a code question) |

## Priority groups for template expansion (summary, detail in `template_expansion_plan.md`)

1. **Highest priority — Group C, excluding the ADHD-confusion cases**: 18 questions, `direct`-support
   evidence already confirmed, no new authorization needed, lowest risk.
2. **Medium priority — Group C's ADHD-confusion cases (qe045, qe081)**: needs the q033 mitigation from
   `q033_context_analysis.md` applied *before* or *alongside* templating, so the template doesn't
   enshrine the wrong-condition evidence.
3. **Lower priority — Group E's generic-support cases**: templating here would require either better
   evidence (not available without re-retrieval/rerank, itself gated by T2.6 for new query text) or an
   explicit "partial answer" template design — see `evidence_to_answer_architecture.md`'s uncertainty
   handling.
4. **Not a template problem — Group F**: requires T2.6 authorization or cache expansion, tracked
   separately.
