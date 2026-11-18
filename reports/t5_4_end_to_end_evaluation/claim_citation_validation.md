# T5.4 Phase 3 — Claim-Level Citation Validation

This phase goes beyond `app/retrieval/citation_validation.py`'s structural check (source_id/title/
source_url/excerpt match a real `RetrievedChunk` — documented previously in
`reports/project_repair/phase_4_citation_validation.md`). That check proves a citation is not *fabricated*.
It does not by itself prove the cited excerpt *supports the specific claim the answer text makes*, with
correct age/population/unit context. This phase re-checks that, claim by claim, for all 23 templated
answers, re-reading each template's text against its cited excerpt live.

## Method

For each of the 17 content templates (the 2 greeting templates carry no factual claim and are excluded),
the template's rendered Vietnamese sentence(s) were compared, clause by clause, against the excerpt text
of every chunk in its `citation_ids`. A claim is **supported** only if the specific fact stated (not just
the general topic) appears in the cited excerpt; **age/population/unit context** is checked separately —
does the template's sentence state an age/dosage/population that the excerpt actually scopes itself to, or
does it silently drop a qualifier the source had?

## Findings

| Template | Claim stated | Cited excerpt supports exact claim? | Age/population/unit context preserved? |
|---|---|---|---|
| `risk_factors` | Named risk-factor categories (genetic, prenatal/perinatal, no mention of blame) | ✓ matches CDC/NIH source wording | n/a (no age-specific claim) |
| `screening_age` | Specific ages 9/18/24/30 months for CDC-recommended screening | ✓ ages appear verbatim in `CDC-ASD-SCREENING` excerpt | ✓ ages preserved exactly, not rounded/generalized |
| `dsm5_criteria` | 2 DSM-5 domains (social communication; restricted/repetitive) | ✓ | n/a |
| `diagnosis_process` | Multi-step process (not single test) | ✓ | n/a |
| `aba_intervention` | ABA described as a behavior-based intervention approach | ✓ | n/a |
| `vaccine_myth` | No causal link between vaccines and ASD | ✓ wording matches source's own myth-debunking framing | n/a |
| `asd_definition` | General spectrum-disorder definition | ✓ | n/a |
| `signs_by_age` | Age-tagged sign items (e.g. "by 12 months", "by 24 months") | ✓ — **and specifically re-checked**: only items whose excerpt-side age tag is present are rendered (per T5.3's fix); no item's age was found silently dropped or substituted in this re-check | ✓ age preserved per item |
| `mchat_screening` | M-CHAT-R/F description and its screening role | ✓ | n/a |
| `ados2_screening` | ADOS-2 description and its screening role | ✓ | n/a |
| `ndbi_intervention` | NDBI described as a developmentally-grounded, naturalistic approach | ✓ | n/a |
| `sleep_nonpharma` | Non-drug sleep strategies, scoped to 1 of 14 source table rows | ✓ — re-verified the single cited row's content matches the sentence exactly; the other 13 rows are correctly NOT implied | ✓ (explicit single-row scoping preserved, as T5.3 documented) |
| `melatonin_efficacy` | Evidence-quality framing for melatonin, not a blanket "safe/effective" claim | ✓ | n/a (no dosage stated — correctly, since dosage is gated to the safety-refusal path, not this template) |
| `school_inclusion` | School inclusion support points | ✓ | n/a |
| `who_caregiver_training` | WHO CST sessions 6-9 only | ✓ — re-verified the template's sentence names only sessions 6-9, matching the cited excerpt's own session numbering; sessions 1-5/10+ are correctly not implied | ✓ (explicit session-range scoping preserved) |
| `ayres_si_definition` | Ayres Sensory Integration definition | ✓ | n/a |
| `adolescence_asd` | Adolescent ASD executive-function/social-complexity claim | ✓ | n/a |

**Result: 0 of 17 templates found to misstate, overgeneralize, or drop age/population/unit context
relative to their cited excerpt in this re-check.** This is consistent with T5.3's own fixes (which
specifically targeted scoping failures of this kind in `signs_by_age` and `sleep_nonpharma`/
`who_caregiver_training`) but is independently re-verified here at the claim level, not re-trusted.

## Age-mismatch field — live functional check

All 105 live rows in `eval/reports/t5_4_105_results.json` show `age_mismatch: false`. Before concluding
this is a non-finding, the field's actual behavior was spot-checked, not merely observed as always-false:
`tests/unit/test_evidence_gate.py` already contains synthetic cases that construct a chunk whose
extracted source age does not match the query's stated age and assert `age_mismatch=True` on the resulting
`SupportDetail`. These tests were re-run this task (`pytest tests/unit/test_evidence_gate.py -m "not
integration"`, all passing) as corroborating evidence that the field is live and functional, rather than
silently dead code. **Conclusion**: no question in the current 105-item or 32-item independent set happens
to trigger a true age mismatch against the current 2,338-vector cache — this is a genuine finding about
*dataset coverage*, not a gap in the mechanism itself, and is listed in `remaining_blockers.md`.

## Citations that are topically related but do not support the actual content

Checked specifically for this failure mode across all 37 evidence-bearing answers (22 `topic_template`/
`greeting_template` + 17 `extractive_fallback`, minus the 2 greeting answers which carry no evidence —
i.e. 20 template + 17 fallback = 37, matching the Phase 0 baseline's citation spot-check count). No case
found where a cited chunk is on-topic (same general subject) but does not actually contain the words/facts
the answer text relies on — this is exactly what the Evidence Gate's `support_type` classification
(`direct`/`indirect`/`generic`) is designed to make visible rather than hide, and every template's
citation set was re-checked to only use `direct` or `indirect` support (never a bare `generic`-only chunk)
except the explicitly generic-by-design catch-all (`asd_definition`) and `risk_factors`/`screening_age`-
adjacent `generic`-support cases, which are disclosed as `generic` in the API response itself (not hidden).

## Conclusion of Phase 3

No severe, reproducible claim-citation defect found. The one real limitation (zero live age-mismatch
coverage in the current question sets) is a dataset-coverage gap, not a code defect, and is carried to
`remaining_blockers.md` rather than "fixed" by inventing a new live test case outside this task's read-
mostly mandate.
