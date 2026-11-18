# T5.3 Phase 5 — Special Case Review

## q033 (ADHD/ASD confusion)

**Preserved exactly as instructed — no Evidence Gate change made.** Re-confirmed live this task
(`test_4_asd_vs_adhd_parent_education` and the pre-existing `tests/integration/test_chat_api_db.py::
test_q033_adhd_confusion_is_still_present_and_unfixed_in_this_task`): the `NIH-NIMH-ADHD` chunk still
surfaces as `direct` support for "Can thiệp do cha mẹ thực hiện có hiệu quả không?"

**The ASD-anchor-only rule was NOT introduced**, per instruction. It remains characterized only
(`tests/unit/test_q033_isolation.py::test_mitigation_option_require_asd_anchor_in_chunk_would_fix_the_
false_positive`, from T5.2, re-run and still passing) — a plain substring check outside the gate, not
wired in. Its false-negative risk on ASD+ADHD comorbidity questions (qe081-style: "Trẻ tự kỷ kèm ADHD
lại hay mất ngủ thì hỗ trợ thế nào?") was already tested in T5.2
(`test_asd_plus_adhd_comorbidity_evidence_is_legitimately_relevant_not_a_false_positive`) and re-run
this task — still confirms the trade-off is real: a blanket anchor-only rule would have excluded that
legitimately relevant comorbidity content. **No sufficient false-positive/false-negative test coverage
exists yet to responsibly propose adopting the rule** — this task did not add more such coverage (out of
Phase 5's explicit scope: "preserve," not "resolve"), so the open decision remains exactly where T5.1/
T5.2 left it.

Note: `q033`/`qe045` (parent-delivered intervention) and `qe051` (home vs. school intervention) remain
in `extractive_fallback`, unaffected by the Phase 1 gating fix in this task — neither question was
templated in T5.2 specifically *because* of this root cause, and that decision is unchanged.

## qe034 (speech delay vs. ASD)

**Still not templated, confirmed unchanged this task.** Re-ran the question live with `k=5`: no chunk in
the Top-5 states the clean distinguishing claim ("speech delay alone ≠ autism"); the only retrieved
content discusses a specific screening tool (ICT) that predicts language delay, not the general
distinction the question asks for. This is the same finding T5.2 recorded in
`template_specifications.md`'s rejection table — re-verified, not assumed stale. **Recorded here again
as the reason evidence is insufficient for this specific claim**: the corpus has adjacent-but-not-
identical content (a screening tool description) and no direct statement of the distinction itself. No
template was created. This remains a candidate for either corpus expansion (new source) or an
ASD-expert-reviewed decision about whether the adjacent content is an acceptable partial answer — not
decided here.

## Table evidence

Re-ran both named real-world cases live this task (not from memory):

- **The 14-row sleep table** (`ASD-OA-PMC7407189`, "ABCs of SLEEPING" mnemonic): `evidence_normalization.
  classify()` still parses exactly **1 of 14 rows** safely — the continuation rows (fewer cells than the
  3-column header) are still correctly refused rather than guessed. Headings (`columns`), the row/column
  relationship (each value keyed to its actual column name, not position), and the unit-bearing cell text
  are all preserved verbatim in the one parsed row, re-verified by direct inspection this task.
- **The CDC age-tagged signs list** (`CDC-ASD-SIGNS`): all 11 list items parsed correctly, with every age
  mention preserved per item (including the dual "24 months (2 years)" case, which correctly extracts
  both "24" and "2" rather than losing either). The age context survives normalization exactly as T5.2
  built it; the only change this task made was fixing the regex to also recognize diacritic-free "thang"/
  "tuoi" forms (for no-diacritics query matching — this does not affect the English-only excerpt parsing
  shown here, since the excerpt itself uses "months"/"years").

No table-parsing or list-parsing regression was found. No corpus file was read differently or modified
to produce this verification — the same `ASD-OA-PMC7407189`/`CDC-ASD-SIGNS` chunks already in the
database were re-queried live.
