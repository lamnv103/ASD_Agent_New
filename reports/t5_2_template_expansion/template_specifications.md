# T5.2 Phase A — Template Specifications

Each of the 18 questions permitted by T5.1 was re-checked against **fresh, live-retrieved evidence**
(not assumed from the T5.1 snapshot). 11 questions, covered by 10 new templates, passed a stricter
content-level check than the Evidence Gate's own topical `support_type` label — i.e. some `direct`/
`indirect`-labeled evidence was still rejected here because, on reading, it did not cleanly support the
specific claim the question asks for. 7 questions are documented as rejected, staying in extractive
fallback. This is the "chất lượng quan trọng hơn coverage" decision named in `phase_0_preflight.md`.

## Accepted (10 templates, 11 questions)

### 1. `signs_by_age` — qe028, qe029
- **Topic**: ASD warning signs tied to a specific age.
- **Intent**: "what are the signs at age X."
- **Claims**: a list of (age, sign) pairs.
- **Evidence**: `CDC-ASD-SIGNS`, a literal age-tagged bulleted list ("Does not respond to name by 9
  months of age," ... "by 18 months of age," etc.) — `direct` support.
- **Activation**: fires only when (a) the trigger source is present AND (b) `evidence_normalization.
  classify()` successfully parses the excerpt as a `list` with at least one age-tagged item. Renders
  every age-tagged item found (CDC presents them as one cumulative checklist, not per-question subsets).
- **Non-activation**: if the excerpt isn't list-shaped, or has no age-tagged item at all, the function
  returns `None` and the caller falls through to extractive fallback — never a guessed age.
- **Insufficient-evidence case**: handled by the existing `insufficient_evidence` path if the trigger
  source itself is absent (unchanged, not new to this template).

### 2. `mchat_screening` — qe036
- **Claims**: tool name/purpose, completion time (~10 min), sensitivity 0.85, specificity 0.99, cutoff
  score ≥8 = high risk, "screening not diagnosis" caveat.
- **Evidence**: `ASD-CSV-029`/`ASD-CSV-002` — direct numeric statements, each number traced to the
  excerpt verbatim (re-verified live in this task, not copied from memory).
- **Activation**: trigger source present AND query contains "m-chat"/"mchat"/"m chat" (gated — see
  Lỗi #1 below).
- **Non-activation**: ADOS-2 questions, even when they retrieve the same shared source `ASD-CSV-002`.

### 3. `ados2_screening` — qe037
- **Claims**: semi-structured observational tool, "gold standard," interrater reliability 0.79–0.98,
  part of a diagnostic process (not a self-test).
- **Evidence**: `ASD-CSV-062`/`ASD-CSV-002`, direct.
- **Activation**: trigger source present AND query contains "ados". Checked **before** `mchat_screening`
  in the query-gated list (see Lỗi #1).

### 4. `ndbi_intervention` — qe044
- **Claims**: NDBI definition (naturalistic setting, shared control, natural contingencies), AAC-plus-
  NDBI shows additional language-development benefit over NDBI alone.
- **Evidence**: `ASD-SUP-PMC4513196` (definition) + `ASD-CSV-017` (AAC finding), both direct.
- **Activation**: trigger source present — no query-term gate (no other template shares this source;
  see `test_template_negative_cases.py` for the explicit boundary test documenting this choice).

### 5. `sleep_nonpharma` — qe047
- **Claims**: sleep disturbance is a common ASD comorbidity (50–80%); non-pharmacological measures are
  generally tried first; the single highest-confidence recommendation found is consistent sleep/wake/
  nap timing ("Strong" evidence tier in the source's own table).
- **Evidence**: `ASD-OA-PMC7407189`, a 14-row table ("ABCs of SLEEPING" mnemonic) plus narrative
  paragraphs. **Only 1 of 14 rows could be safely parsed** (see `evidence_normalization_audit.md` —
  continuation rows with fewer cells than the header are correctly not force-fit). The template cites
  only that one safely-extracted recommendation, with an explicit sentence stating it is one of several
  recommendations the source lists, not the complete table.
- **Activation**: trigger source present AND query does **not** match the melatonin-specific gate (see
  item 6 — checked first in priority order).

### 6. `melatonin_efficacy` — qe048
- **Claims**: melatonin (with behavioral interventions) is one of the few treatments with well-
  established efficacy for ASD sleep problems in the literature. **No dosage number is ever stated**,
  even though the source document elsewhere gives a specific RCT dose (3 mg/night) — deliberately
  excluded per the task's rule against stating thresholds/doses (Phase B rule 7); the existing
  `is_dosing_question` safety override independently and additionally refuses any phrasing that asks
  for a dose directly.
- **Evidence**: `ASD-OA-PMC7407189`, the same document as item 5, different paragraph: "For some
  treatments—such as melatonin and behavioral interventions—effectiveness in ASD is well established in
  the literature."
- **Activation**: trigger source present AND query contains "melatonin" — checked before `sleep_
  nonpharma` in `_QUERY_GATED_TEMPLATES`.

### 7. `school_inclusion` — qe049
- **Claims**: a systematic review of 56 studies found school-based inclusion interventions increase
  accessibility of school activities for autistic pupils, **but** do not necessarily improve friendship/
  reciprocity with peers — both the positive and the limiting finding are stated, not just the positive
  one (avoids overclaiming "school inclusion works").
- **Evidence**: `ASD-CSV-019`, direct.
- **Activation**: trigger source present, no query-term gate needed (no sharing template).

### 8. `who_caregiver_training` — qe057 (**qe056 excluded — see Rejected #7 below**)
- **Claims**: WHO Caregiver Skills Training program description; session 6 = daily living skills,
  sessions 7–8 = positive behavior / reducing challenging behavior, session 9 = caregiver well-being —
  explicitly framed as "a part of," not the complete 1–9 session arc (the evidence only names sessions
  6–9).
- **Evidence**: `WHO-CST-PARTICIPANTS-2022`/`WHO-CST-INTRO-2022`, direct, the session-description
  paragraph (not the workbook-quiz chunk that disqualified qe056).
- **Activation**: trigger source present, no query-term gate (shares no source with another new
  template).

### 9. `ayres_si_definition` — qe024 (narrowed from "efficacy" to "definition")
- **Claims**: Ayres SI is an intervention approach (A. Jean Ayres) defining sensory integration
  dysfunction as difficulty "organizing sensory information for use," linked to motor function; it is
  one specific approach among sensory therapies, distinct in theoretical basis and assessment.
- **Evidence**: `ASD-SUP-PMC7726187`, direct — a clean definitional sentence. **Does not** attempt an
  efficacy/cost claim (the original qe024 question asked "how does it differ," which this answers; the
  efficacy-flavored qe023/qe025 using messier methodology/cost evidence were rejected — see below).
- **Activation**: trigger source present, no query-term gate.

### 10. `adolescence_asd` — qe031
- **Claims**: adolescence is a significant biopsychosocial transition, particularly challenging for
  neurodevelopmental conditions including ASD; autistic teens may face heightened executive-function
  demands and social complexity versus childhood, which can contribute to anxiety and "camouflaging."
- **Evidence**: `ASD-OA-PMC12593641` + `ASD-OA-PMC12468522`, direct/indirect, both general-statement
  paragraphs (not, e.g., any specific unverified statistic).
- **Activation**: trigger source present, no query-term gate.

## Rejected (7 questions, stay in extractive fallback — reasons, not just labels)

| Question | Gate's label | Why rejected at the content level |
|---|---|---|
| qe017 (narrow interests & learning) | `indirect` | Evidence (`ASD-OA-PMC12468522`) discusses monotropism/systemizing *theory* for why restricted interests occur — it does not address the literal question (impact on learning) |
| qe023 (sensory integration efficacy) | `direct`/`indirect` | Evidence is a methodology table (search terms) and a qualitative-interview excerpt, not a clean efficacy statement |
| qe025 (sensory integration cost-worth) | `direct` | Evidence is cost-effectiveness statistics in GBP from one RCT's economic analysis — translating this into a plain "is it worth the cost" answer would misrepresent a specific trial's figures as a general answer |
| qe034 (speech delay vs. ASD) | `indirect` | **Safety-relevant, deliberately rejected despite being the highest template priority candidate**: the actual retrieved evidence (`ASD-CSV-091`) is about a specific screening tool (ICT) predicting language delay, not a direct "speech delay ≠ autism" statement; re-running retrieval at `k=5` found no chunk in this corpus that makes that clean distinguishing claim. Templating the clean claim anyway would be adding content the evidence does not say — exactly what Phase B rule 5 (claims removed if unsupported) forbids. Stays in extractive fallback. |
| qe041 (Vietnam screening context) | `direct` | Evidence (`ASD-CSV-038`) describes one specific survey's data-collection methodology (provinces selected, staff trained) — presenting this as "how Vietnam does screening" in general would overgeneralize a single study |
| qe051 (home vs. school intervention) | `direct` | Evidence source (`ASD-NEW-002`, "Parenting interventions to promote early child development in the first three years of life") is a **general child-development** review, not ASD-specific — the same root-cause pattern as q033 (a generic-parenting source retrieved for an ASD question); flagged for Phase E, not templated |
| qe056 (what to do for challenging behavior) | `direct` | The top-ranked `direct` chunk from `WHO-CST-PARTICIPANTS-2022` is literal workbook quiz boilerplate ("Only check the answers after you have tried...") — not actual guidance; the same source's OTHER chunk (used for qe057) is clean, but that chunk does not answer qe056's specific question |

No claim in any of the 10 accepted templates was found unsupported during this specification pass; where
a source only partially supports a broader topic (sleep table, WHO sessions), the template text says so
explicitly rather than presenting a partial finding as complete.
