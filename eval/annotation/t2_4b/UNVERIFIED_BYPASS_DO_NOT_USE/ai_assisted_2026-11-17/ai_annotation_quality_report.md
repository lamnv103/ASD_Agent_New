# T2.4-B AI-assisted annotation ? provisional report (2026-11-17)

Coverage is complete for both 2,791-pair packages. Labels remain **provisional AI annotations**, not human gold labels or expert-validated labels. Do not use these results to claim clinical accuracy or automatically advance to T2.5.

- 66 questions; 2,791 pairs.
- Exact AI-to-AI agreement: 2129/2791 (76.3%).
- Ordinal subset (both 0?3, neither needs review): n=2786; exact=2129/2786 (76.4%); quadratic weighted kappa=0.8604; linear weighted kappa=0.7633. Grade -1 was excluded from ordinal kappa.
- Pair disagreements/review flags: 662; types: {"one_grade": 372, "relevant_vs_irrelevant": 285, "needs_review": 5}. At least one needs-review: 5; grade -1 on either side: 0.
- Evidence checks passed. Derived outputs shorten A's 20 overlength spans and repair 13 B spans (including non-verbatim spans); originals were not changed. Three A grade -1 labels that failed the defined conflict rule are marked needs_review in derived output.

## Duplicate continuation outputs

The earlier AI continuation files contained duplicate codes already present in the current returned sets: A 699 (249 grade differences) and B 666 (208 grade differences). These overlapping continuation rows were excluded. Existing returned rows were kept; only codes missing from those files were filled from the gap completion. No duplicate label was silently selected.

## Provenance limitation

Pre-existing returned labels do not record model name/version, prompt version, or annotation timestamp. These remain null; no values were inferred. Gap completions record model/prompt/timestamp (A gpt-6.1-sol; B gpt-6.1-terra). Full-run model consistency cannot be established.

## Pending student decisions

- 665 pending adjudication rows, including pair disagreements/review flags and question-level q016, q041, and q057.
- No mean, higher-grade selection, or automatic adjudication. Final grade is set only when A and B agree and neither requests review.
- `human_expert_reviewed=false`; labels remain provisional.
