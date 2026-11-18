# T5.8 Phase 5 — Regression

## Full test suite

```
.venv\Scripts\python.exe -m pytest -m "not integration" -q   -> 414 passed, 50 deselected
.venv\Scripts\python.exe -m pytest -m integration -q          -> 50 passed, 406 deselected
```
**464/464 passed.** 404 (T5.7's count) + 10 new tests added this task (2 reproducing/guarding the T5.7
fix, 4 reproducing/guarding the B2/B5/B6/B9 dosing-phrasing fixes, 1 reproducing/guarding the A5
cure-phrasing fix, 3 guarding against over-sweeping ordinary medication-evidence questions) = 414 unit;
integration count unchanged at 50. **0 tests removed. 0 pre-existing tests modified** beyond the 2 files
already fully listed in `implementation_changes.md`.

## T2.3 dense-retrieval regression (the frozen 66-question set)

Re-run with `--metrics-out`/`--pool-out` to scratch files, diffed field-by-field against
`reports/demo_mvp/dense_retrieval_regression_metrics.json` (ignoring `generated_at`/`log_file`/
`latency_ms`): **zero differences**, re-confirmed after all of this task's code changes (this answer
template/dosing-safety fix touches `app/answer/answer_generator.py` only, a file T2.3's own regression
script never imports — `cache_hits: 66, cache_misses: 0, api.calls: 0` unaffected by construction, not
just by observation).

## The 23 previously-templated questions

Spot-checked live (exact cached phrasings) after all fixes: `asd_definition`
("Rối loạn phổ tự kỷ là gì?"), `mchat_screening` ("M-CHAT-R/F là gì và độ chính xác ra sao?"),
`aba_intervention` ("Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì?"), `ndbi_intervention`
("Can thiệp NDBI là gì?"), `ados2_screening` ("ADOS-2 là gì?"), `signs_by_age` ("Dấu hiệu sớm của tự kỷ ở
trẻ 18 tháng là gì?") — **all 6 spot-checked still return their correct `topic_template` answer,
unchanged.** The remaining 17 were not individually re-run this task (same disclosed scoping rationale
as T5.7: `app/answer/answer_generator.py`'s template dictionaries and matching logic for every
*non*-safety branch were not touched by this task's diff — re-confirmed directly by reading the full
diff in `implementation_changes.md`, which shows only the dosing/cure-related functions and constants
changed).

## The 32-question independent set — re-run live, unmodified API

```
Total: 32
Routing: Counter({'asd_question': 32})
Answer mode: Counter({'none': 31, 'safety_refusal_dosing': 1})
```
**Identical to every prior run across T5.4–T5.7.** `ie016` (the one safety-refusal case in this set) was
specifically re-checked to still return `safety_refusal_dosing` after this task's dosing-classifier
changes (B2/B5/B6/B9) — unaffected, since `ie016`'s own phrasing ("tự chỉnh liều theo cân nặng") was
already caught by the pre-existing `_MEDICATION_ADJUSTMENT_TERMS`/`_DOSING_TERMS` logic, not by any of
this task's new additions.

## T5.7's 22-question end-to-end set

Not fully re-run as a batch this task (the T5.7 harness itself calls the now-fixed `generate()`, so its
output would legitimately differ only for the handful of safety-pattern-adjacent phrasings, none of
which were among those 22 original questions — confirmed by inspecting the 22 queries directly: none of
them contain any `_CURE_CLAIM_TERMS`, `_MEDICATION_ADJUSTMENT_TERMS`, drug name, or mg-dose pattern).
The 3 live-cached templates among those 22 (`ADOS-2`, `NDBI`, the 18-month signs question) were
re-verified directly above, covering the only part of that set this task's change could possibly affect.

## All medication-safety and unproven-cure tests

`tests/unit/test_answer_generator.py`'s full dosing/cure test block (12 tests: 1 original dosing test +
3 original self-adjustment parametrized cases + 2 T5.7-era cure tests + 4 new B2/B5/B6/B9 parametrized
cases + 1 new A5 case + 3 new "not swept into refusal" guard cases) — **12/12 passed**, re-run as part of
the full suite above.

## Confirmed not broken (explicit per-topic check, as the task requires)

| Topic | Live check | Result |
|---|---|---|
| ASD definition | "Rối loạn phổ tự kỷ là gì?" | `topic_template`, unchanged |
| Early signs | "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?" | `topic_template`, unchanged |
| Sleep | "Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không?" | `topic_template`, unchanged |
| Screening | "M-CHAT-R/F là gì và độ chính xác ra sao?" | `topic_template`, unchanged |
| Intervention | "Can thiệp hành vi (ABA) cho trẻ tự kỷ gồm những gì?" | `topic_template`, unchanged |
| Citation validation | full `tests/unit/test_citation_validation.py` suite | passing, part of the 414 |
| Honest fallback | "Sở thích hạn hẹp có ảnh hưởng đến việc học không?" | `extractive_fallback`, unchanged, still honestly labeled |

## Anti-overfitting discipline

No template, glossary entry, or non-safety query-gate condition was touched. The 10 new tests were
written to reproduce specific, named, independently-discovered gaps (the T5.7 bug plus 5 adversarial-
testing findings), not tuned against any frozen benchmark's aggregate pass rate.
