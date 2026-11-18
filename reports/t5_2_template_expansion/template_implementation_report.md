# T5.2 Phase B — Template Implementation Report

## Files changed

**New:**
- `app/answer/evidence_normalization.py` — Phase C normalization (table/list/paragraph classification,
  age extraction, boilerplate stripping).
- `tests/unit/test_evidence_normalization.py` (10 tests)
- `tests/unit/test_q033_isolation.py` (5 tests, Phase E — no Evidence Gate change)
- `tests/unit/test_template_negative_cases.py` (10 tests, Phase F — independent negative/diacritic tests)

**Modified:**
- `app/answer/answer_generator.py`:
  - Added 10 new templates (`_NEW_TOPIC_TEMPLATES` + `_QUERY_GATED_TEMPLATES`) covering 11 of the 18
    permitted questions, wired into `generate()` after the existing 7-template check and before
    extractive fallback.
  - **Fixed a pre-existing bug** (found live during this task's own regression testing, not introduced
    by T5.2): the original 7 templates matched on trigger-source presence alone, and because
    `NIH-NIMH-ASD-2025`/`CDC-ASD-CLINICAL` are each cited by multiple templates, the generic
    `asd_definition` template (checked first) silently hijacked `risk_factors`, `screening_age`,
    `dsm5_criteria`, and `diagnosis_process` whenever its shared source appeared — e.g. a DSM-5 question
    returned the generic "what is ASD" paragraph. Fixed by adding a required-query-term gate to each of
    the 6 specific old templates (text unchanged) and moving `asd_definition` to the end of the list as
    the true catch-all. See `regression_report.md` for the live before/after evidence.
  - Added a second, analogous fix for 3 of the **new** templates that also share a source
    (`mchat_screening`/`ados2_screening` both can retrieve `ASD-CSV-002`; `melatonin_efficacy`/
    `sleep_nonpharma` both retrieve `ASD-OA-PMC7407189`) — caught live before it ever reached a
    committed test, via the same query-term-gating pattern (`_QUERY_GATED_TEMPLATES`, checked before the
    source-only `_NEW_TOPIC_TEMPLATES`).
- `app/api.py`: **no changes needed** — `generate()`'s existing signature and return contract were
  reused unchanged; the new templates are invisible to the API layer.

## Compliance with Phase B's 10 rules (checked against the actual template text, not assumed)

1. Trả lời trực tiếp — each of the 10 templates' first sentence directly answers its question's core ask
   (verified live, see `template_specifications.md`).
2/3. No raw English excerpts as the main answer, no mechanical translation — every template is a
   hand-written Vietnamese sentence; technical terms (M-CHAT-R/F, ADOS-2, NDBI, DSM-5, Ayres SI) are kept
   in their original form, consistent with rule 8.
4. Meaning/certainty/scope preserved — `sleep_nonpharma` and `who_caregiver_training` explicitly say
   they cover only part of their source's full content (rule 9); `school_inclusion` states both the
   positive and the limiting finding, not just the positive one.
5. No added medical recommendation beyond evidence — none of the 10 templates recommends an action not
   stated in its source.
6. No correlation→causation — `adolescence_asd` and `risk_factors` (unchanged, old) both use hedged
   language ("có thể," "liên quan đến," not "gây ra").
7. No invented age/dose/diagnostic threshold — `melatonin_efficacy` explicitly omits the source's own
   3 mg/night figure; `signs_by_age` only ever states ages the evidence itself names.
8. English terms kept where needed — done for all 5 named tools/methods above.
9. No generic answer when evidence is partial — `sleep_nonpharma`/`who_caregiver_training` say so
   explicitly in-text (see Phase A spec).
10. Only supporting sources cited — citation lists are built from the same `trigger_sources`/`matching`
    evidence the template actually used, same mechanism as the original 7 (unchanged `citation_ids`
    construction pattern).

## No LLM, no external service

`grep`-confirmed: no new import of any network client, no call to Cohere/OpenAI/any HTTP client in
`answer_generator.py` or `evidence_normalization.py`. All 10 templates are fixed Python strings or
pure-Python string/regex processing over already-retrieved text.
