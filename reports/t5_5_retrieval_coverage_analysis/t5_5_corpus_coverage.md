# T5.5 Phase 3 — Corpus Coverage Audit

Read-only `content ILIKE` keyword sweep across all 2,291 retrievable chunks (`asd_rag_v2_research_reader`
role), for the 12 topics named in the task, plus cross-reference against the cache-miss taxonomy
(`t5_5_cache_miss_taxonomy.md`) and the existing 17 live templates (which prove certain sources are not
just present but already validated as answer-quality content).

| Topic | Representative keyword counts | Coverage verdict |
|---|---|---|
| ASD definition | "autism spectrum disorder" 140, "neurodevelopmental" 89 | **Strong.** Also the basis of the live `asd_definition` catch-all template. |
| Early signs | "early signs" 5, "warning sign" 0 | **Thin on this exact phrasing**, but the dedicated `CDC-ASD-SIGNS` source (used by the live `signs_by_age` template) covers this topic by content, just not by this literal English phrase — a vocabulary-sweep artifact, not a true gap (confirmed by `ie007`/`ie008`/`ie009`'s category-3 classification in Phase 1). |
| Social communication | "social communication" 132, "joint attention" 47 | **Strong.** |
| Repetitive behaviors | "repetitive behavior" 65, "restricted interest" 7, "lining up" 4 | **Adequate**, though narrower phrasings ("lining up," a literal translation of a common Vietnamese example) are thin — consistent with the T2.4 audit's own finding that "restricted interests" (7 chunks) is much narrower than "restricted, repetitive" (26 chunks; different phrase). |
| Sensory differences | "sensory integration" 88, "sensory processing" 77 | **Strong.** Basis of the live `ayres_si_definition` template. |
| Diagnosis and screening | "M-CHAT" 49, "ADOS" 72, "DSM-5" 50 | **Strong.** Basis of 5 live templates (`dsm5_criteria`, `screening_age`, `diagnosis_process`, `mchat_screening`, `ados2_screening`). |
| Intervention | "applied behavior analysis" 15, "NDBI" 81 | **Adequate to strong.** Basis of `aba_intervention`/`ndbi_intervention`. |
| Speech and language | "speech delay" **1**, "language delay" 6 | **Weak.** This is the thinnest topic found in this sweep. It directly explains why `qe034` (speech-delay-vs-ASD, from T5.4) has never had a dedicated template and remains `extractive_fallback`-only, and why `ie004`/`ie005`/`ie006`/`ie029` (all language-development questions in the new independent set) found only indirect, general-ASD-overview content via FTS rather than any chunk specifically about language/speech delay as its own topic. |
| ASD and ADHD | "comorbid" 144, "ADHD" 171 | **Strong** as an epidemiology/comorbidity-prevalence topic, but — see note below — this is a different angle than what several `ie001`/`ie002`/`ie003`/`ie028` questions actually ask. |
| Age-related differences | "adolescen" 223, "toddler" 65 | **Strong**, and the basis of the live `adolescence_asd` template; however coverage concentrates on adolescence/early-childhood, not adulthood (see the "adulthood" finding below). |
| Sleep and associated difficulties | "sleep disorder" 30, "melatonin" 28 | **Strong.** Basis of `sleep_nonpharma`/`melatonin_efficacy`. |
| Safety-related medical questions | "risperidone" 3, "aripiprazole" 1, "dosage" 48 | **Thin but sufficient for the safety-refusal design** — the live system never needs to *answer* a dosing question (it refuses, by design, before retrieval), so thin dosage-specific content is not itself a functional gap; it would only become one if a future task tried to make the system answer dosing questions directly, which is explicitly out of scope. |

## A finding the keyword counts alone understate: "comorbid"/"ADHD" being *present* does not mean the
*specific angle* asked is covered

144 "comorbid" chunks and 171 "ADHD" chunks sound like strong coverage, and for a prevalence/epidemiology
question they are. But `ie001` ("are ASD and ADHD the same disease or two different things") and `ie002`
("which should be prioritized when both co-occur") ask a *definitional* or *care-prioritization* question,
not a prevalence question — and the FTS diagnostics in Phase 1/2 found the retrieved comorbidity chunks to
be tables of co-occurrence statistics (e.g. `ASD-CSV-062`'s "Mean scores... in the ASD alone, ASD+ADHD..."
table), not prose that directly states "these are two distinct, separately-diagnosable conditions" or
gives care-prioritization guidance. This is the category-2 pattern from Phase 1: the topic area exists,
but the chunk granularity does not match the question's actual angle. A simple topic-presence keyword
count would have missed this; only reading the actual retrieved chunk content (done in Phase 1/2) surfaces
it.

## Topics with a genuine, confirmed absence (not just a thin keyword count)

Cross-referencing Phase 1's category-1 findings (direct content inspection, not just a count):

- **Adult-life topics (marriage, independent adult living/parenting)**: "marriage" = 0 matches anywhere
  in the corpus. The corpus's age coverage, confirmed above, concentrates on childhood/adolescence; there
  is no adult-outcomes content at all. (`ie026`.)
- **Culturally-specific non-Western causal beliefs**: "folk belief"/"superstition"/"traditional belief" =
  0 matches. The corpus is Western biomedical literature; this is an expected, not surprising, gap.
  (`ie018`.)
- **Adolescent sexuality/sex education**: "sex education"/"sexual education" = 0 matches. (`ie024`.)
- **ASD-vs-hearing-impairment differential content**: "hearing loss" mentions (6) are incidental
  (participant-exclusion-criteria tables), not substantive differential-diagnosis prose. (`ie029`.)
- **The specific myth "high-dose vitamin B6 cures autism"**: the corpus's only B6 mentions (2) are about
  B6 as a sleep-aid supplement ingredient, not about megavitamin-therapy-as-cure. (`ie017`.)

## Conclusion of Phase 3

Of the 12 named topics, 9 have strong-to-adequate corpus coverage (ASD definition, social communication,
sensory differences, diagnosis/screening, intervention, ASD+ADHD epidemiology, age-related differences,
sleep, safety-medical-for-refusal-purposes). **Speech and language is the one topic with genuinely thin
coverage** ("speech delay": 1 chunk), a specific, actionable, pre-existing gap. Separately, several
sub-topics *within* otherwise well-covered general areas are genuinely absent (adulthood/marriage,
non-Western folk beliefs, adolescent sex education, ASD-vs-hearing-impairment differentiation, the
specific vitamin-B6-cure myth) — these are narrow, confirmed gaps, not broad topic-level failures. No
corpus edit was made or proposed as part of this audit (Phase 3 is explicitly audit-only).
