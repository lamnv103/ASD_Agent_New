# T5.1 — Template Expansion Plan

Priority-ordered, built from `topic_gap_matrix.md` Group C (good evidence, no template) and
`q033_context_analysis.md` (two exclusions). No template was written in this task — this is a plan, not
an implementation, consistent with the task's "chỉ phân tích, không sửa code" constraint.

## Tier 1 — Safe to implement now, no new authorization, no known evidence-quality risk (18 questions)

| New template topic | Covers | Trigger source(s) | Notes |
|---|---|---|---|
| Narrow interests and learning impact | qe017 | `ASD-OA-PMC12468522` | Single-source, `indirect` support — verify the source actually addresses "impact on learning" specifically, not just restricted interests generally, before templating |
| Early signs at a specific age | qe028, qe029 | `CDC-ASD-SIGNS` | Needs the table/list-aware frame design from `evidence_to_answer_architecture.md` Example 1 to list age-specific signs without conflating with developmental milestones (the exact T3/T4 "Lỗi 7" risk) |
| Autism in adolescence | qe031 | `ASD-OA-PMC12593641`, `NIH-NIMH-TEEN-BRAIN` | Mixed direct/indirect; scope the template to what these two sources actually cover, not adolescence in general |
| Speech delay vs. ASD | qe034 | `ASD-CSV-091` | High safety value — this is exactly the "chậm nói ≠ tự kỷ" distinction the independent expert evaluation flagged; prioritize within this tier despite single-source `indirect` evidence |
| Sensory integration therapy efficacy | qe023, qe024, qe025 | `NIHR-SENITA-2022`, `ASD-SUP-PMC7726187`, `ASD-SUP-PMC6590432` | Evidence is mixed/cautious in the literature — template must preserve that nuance, not oversimplify to "effective" |
| M-CHAT-R/F screening tool | qe036 | `ASD-CSV-029`, `ASD-CSV-002` | Numeric sensitivity/specificity frame — see Example 2 |
| ADOS-2 screening/diagnostic tool | qe037 | `ASD-CSV-002`, `ASD-CSV-062` | Similar structure to M-CHAT template |
| Vietnam-specific screening/diagnosis context | qe041 | `ASD-CSV-038` | Regional-context template; keep scope narrow (what the cited study found, not a general claim about all of Vietnam) |
| NDBI intervention definition | qe044 | `ASD-SUP-PMC4513196`, `ASD-CSV-017` | Short-definition template, same shape as existing `aba_intervention` |
| Sleep improvement (non-pharmacological) | qe047 | `ASD-OA-PMC7407189` | **Needs table-parsing normalization** — see Example 4; do this one after the table-handling logic exists, not before |
| Melatonin efficacy (not dosing) | qe048 | `ASD-OA-PMC7407189`, `ASD-CSV-095` | Must stay strictly about efficacy; the existing `is_dosing_question` safety override already and correctly intercepts any dosing-flavored phrasing of this same topic — this template must never emit a number of mg |
| School inclusion interventions | qe049 | `ASD-CSV-019` | See Example 3 |
| Home vs. school intervention priority | qe051 | `ASD-NEW-002` | Comparison-style template (per Phase 3.4's "so sánh" format) |
| WHO caregiver skills training program | qe056, qe057 | `WHO-CST-PARTICIPANTS-2022`, `WHO-ECD-GUIDELINE-2020`, `WHO-CST-INTRO-2022` | See Example 5 |

## Tier 2 — Blocked on the q033 ADHD-confusion mitigation (2 questions)

| Topic | Covers | Why blocked |
|---|---|---|
| Parent-delivered intervention effectiveness | qe045 | Its current best evidence set includes `NIH-NIMH-ADHD` misclassified as `direct`; templating now would enshrine the wrong-condition content as if it were a reviewed, correct answer — worse than the current honest (if English) fallback |
| ASD+ADHD comorbid sleep support | qe081 | Same root cause; this one is trickier because ADHD content is *legitimately* relevant here (the question is explicitly about the comorbid combination) — needs the project owner's decision from `q033_context_analysis.md`, not just a code fix |

**Recommendation**: implement the q033 mitigation (or an explicit owner-approved trade-off decision) from
`q033_context_analysis.md` *before* Tier 2 templates, not alongside them.

## Tier 3 — Needs evidence quality decided first, not just a missing template (5 questions)

`qe021, qe022, qe033, qe053, qe105` (Group E, `generic`-only support). A template here would need either
(a) better evidence than currently retrieved — not achievable without new retrieval/rerank work, itself
a larger change than this plan covers, or (b) an explicit "partial/uncertain" template style that states
plainly what the generic evidence does and doesn't confirm (the Stage 5 "uncertainty handling" design in
`evidence_to_answer_architecture.md`). Recommend (b) as a smaller, faster path once Tier 1 is done, but
flag qe033 specifically for ASD-expert input first (see `topic_gap_matrix.md` Group G) since it's a
clinically meaningful question (sex differences in presentation) that deserves more care than a generic
"partial evidence" disclaimer alone would provide.

## What this plan does not include

- `qe014`, `qe063/qe093`, `qe074` (insufficient_evidence / safety_caution cases) — these are already
  correctly handled by explicit, honest "not enough evidence" messages; a template is not the right fix
  for a genuine evidence gap, and attempting one would risk exactly the overclaiming the whole project is
  trying to avoid.
- Any of the 50 cache-blocked (Group F) questions — out of this plan's scope by construction; see
  `remaining_issues.md` (T4) for that authorization-gated path.

## Effort estimate (qualitative, not a committed schedule)

Tier 1 without the table-parsing cases (14 templates: signs-by-age excluded pending table work, sleep
excluded, everything else): comparable effort to the 7 existing templates, i.e. incremental and
low-risk, each one independently reviewable and testable the same way `phase_3_answer_quality.md`
reviewed the first 7. The 2 table-parsing cases (signs-by-age, sleep) need the normalization logic from
`evidence_to_answer_architecture.md` Stage 1/Example 1/4 built once, then reused by both.
