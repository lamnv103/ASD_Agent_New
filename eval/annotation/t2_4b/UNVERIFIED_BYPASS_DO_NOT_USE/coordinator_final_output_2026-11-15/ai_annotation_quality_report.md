# T2.4-B AI Annotation Quality Report

**Generated:** 2026-11-15T15:35:54.655002+00:00  
**Status:** INCOMPLETE — Annotation Not Fully Done  
**Note:** Labels are AI-generated, not human expert-reviewed. This is a provisional dataset.

---

## Phase 1 – Preflight

| Check | Result |
|---|---|
| Package A size | 2791 / 2791 |
| Package B size | 2791 / 2791 |
| Coverage A | 1600 / 2791 (⚠ missing 1191) |
| Coverage B | 2666 / 2791 (⚠ missing 125) |
| Parse errors | 0 |
| Grade errors | 0 |

### Missing A by Question
- q002: 52
- q003: 48
- q018: 52
- q019: 55
- q020: 50
- q022: 42
- q023: 42
- q025: 34
- q026: 51
- q027: 45
- q029: 33
- q030: 39
- q033: 56
- q036: 41
- q037: 39
- q040: 34
- q041: 55
- q042: 37
- q043: 41
- q048: 45
- q049: 34
- q054: 54
- q056: 54
- q057: 38
- q059: 39
- q060: 38
- q064: 43

### Missing B by Question
- q021: 48
- q030: 39
- q047: 38

---

## Phase 3 – Inter-Annotator Agreement

> ⚠️ This is AI-to-AI agreement, not human inter-rater reliability.

| Metric | Value |
|---|---|
| Items with both valid grades | 1504 |
| Exact agreement (all grades) | 1085/1504 = 72.1% |
| Ordinal items (grade 0–3 only) | 1501 |
| Ordinal exact agreement | 1085/1501 = 72.3% if ord_pairs else 'N/A' |
| Cohen's κ (exact) | 0.5764 if not math.isnan(kappa_exact) else 'N/A' |
| Cohen's κ (linear weighted) | 0.7204 if not math.isnan(kappa_lin) else 'N/A' |
| Cohen's κ (quadratic weighted) | 0.8400 if not math.isnan(kappa_quad) else 'N/A' |
| One-conflicting (-1) pairs | 3 |
| Both-conflicting pairs | 0 |
| needs_review A | 2 |
| needs_review B | 10 |

### Agreement by Question (ordinal)
| Question | N | Agree | % | Priority |
|---|---|---|---|---|
| q001 | 37 | 16 | 43.2% |  |
| q004 | 39 | 29 | 74.4% |  |
| q005 | 36 | 33 | 91.7% |  |
| q006 | 40 | 31 | 77.5% |  |
| q007 | 40 | 28 | 70.0% |  |
| q008 | 55 | 49 | 89.1% |  |
| q009 | 40 | 27 | 67.5% |  |
| q010 | 40 | 27 | 67.5% |  |
| q011 | 40 | 18 | 45.0% |  |
| q012 | 40 | 38 | 95.0% |  |
| q013 | 47 | 34 | 72.3% |  |
| q014 | 58 | 32 | 55.2% |  |
| q015 | 33 | 18 | 54.5% |  |
| q016 | 30 | 22 | 73.3% | ⚑ |
| q017 | 54 | 49 | 90.7% |  |
| q024 | 49 | 25 | 51.0% |  |
| q028 | 43 | 37 | 86.0% |  |
| q031 | 42 | 22 | 52.4% |  |
| q032 | 48 | 43 | 89.6% |  |
| q034 | 33 | 25 | 75.8% |  |
| q035 | 54 | 35 | 64.8% |  |
| q038 | 47 | 40 | 85.1% |  |
| q039 | 47 | 37 | 78.7% |  |
| q044 | 42 | 18 | 42.9% |  |
| q045 | 35 | 22 | 62.9% |  |
| q046 | 38 | 32 | 84.2% |  |
| q050 | 39 | 16 | 41.0% |  |
| q051 | 37 | 30 | 81.1% |  |
| q052 | 39 | 28 | 71.8% |  |
| q053 | 41 | 16 | 39.0% |  |
| q055 | 38 | 27 | 71.1% |  |
| q058 | 32 | 32 | 100.0% |  |
| q061 | 40 | 37 | 92.5% |  |
| q062 | 20 | 20 | 100.0% |  |
| q063 | 25 | 21 | 84.0% | ⚑ |
| q065 | 33 | 23 | 69.7% |  |
| q066 | 50 | 48 | 96.0% | ⚑ |

---

## Phase 4 – Disagreements

| Type | Count |
|---|---|
| needs_review | 10 |
| one_conflicting | 3 |
| one_grade_diff | 392 |
| one_missing | 1246 |
| two_plus_grade_diff | 24 |
| **Total disagreement rows** | **1665** |
| **Adjudication queue** | **1287** |

---

## Dataset Files

| File | Records | Status |
|---|---|---|
| ai_annotation_agent_a_final.jsonl | 2791 | provisional |
| ai_annotation_agent_b_final.jsonl | 2791 | provisional |
| ai_annotation_merged.jsonl | 2791 | provisional |
| ai_annotation_agreement.json | — | provisional |
| ai_annotation_disagreements.csv | 1665 | provisional |
| ai_annotation_adjudication_queue.jsonl | 1287 | awaiting human review |

---

## Limitations

- `annotation_method = ai_assisted_independent_annotation`
- `human_expert_reviewed = false`
- `annotation_status = provisional`
- Labels are **not gold standard** and have not been expert-reviewed.
- Coverage is INCOMPLETE.
- Adjudication queue requires researcher decision before T2.5.
- Do NOT call these labels final until researcher approves.

---

## Conclusion

**INCOMPLETE — Annotation Not Fully Done**

⚠ Both agents must complete all 2,791 pairs before final merge. Resume annotation after quota resets.

Researcher must review this report and approve before proceeding to T2.5.
