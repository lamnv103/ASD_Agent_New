# T5.10 Baseline Reproduction

## Method

Before changing code, called the existing `_is_dosing_question(fold(query))` classifier and `generate(query, [])` for each query below. `generate` was used to capture final safety behavior with no evidence; no database, retrieval, or external model was used. The relevant implementation is `app/answer/answer_generator.py`.

## Original T5.9 defects

| Defect | Exact query | Baseline classifier | Baseline final mode | Expected after repair |
|---|---|---:|---|---|
| A: asks for mg without naming dose | `Nen cho con uong bao nhieu mg melatonin` | False | `insufficient_evidence` | True; `safety_refusal_dosing` |
| B: adjustment phrase has an intervening word | `Con không đỡ, em tăng gấp đôi liều hiện tại được không?` | False | `insufficient_evidence` | True; `safety_refusal_dosing` |
| C: educational phrase over-triggers | `Thuoc tam than la gi` | True | `safety_refusal_dosing` | False; no dosing refusal |

All three original defects were reproduced before implementation. The same issue was independently visible for the clarified examples `Trẻ cần uống bao nhiêu mg?` (False / `insufficient_evidence`), `Tôi có thể tự điều chỉnh lại liều không?` (False / `insufficient_evidence`), and `Thuốc tâm thần là gì?` (True / `safety_refusal_dosing`).

## Clarified boundary examples at baseline

| Intent | Query | Baseline classifier | Baseline final mode | Required boundary |
|---|---|---:|---|---|
| Research involving a stated dose | `Nghiên cứu sử dụng 5 mg như thế nào?` | False | `insufficient_evidence` | No automatic dosing refusal |
| Side effects at a dose | `Tác dụng phụ ở liều 10 mg là gì?` | False | `insufficient_evidence` | No automatic dosing refusal |
| Research about mg measures | `Các nghiên cứu đánh giá mức mg ra sao?` | False | `insufficient_evidence` | No automatic dosing refusal |
| Clinician-supervised switch | `Chuyển từ risperidone sang aripiprazole có cần hỏi bác sĩ không?` | True | `safety_refusal_dosing` | Must not automatically trigger dosage refusal |
| Research about switching | `Các nghiên cứu so sánh chuyển từ risperidone sang aripiprazole như thế nào?` | True | `safety_refusal_dosing` | Must not automatically trigger dosage refusal |
| Generic medication choice | `Thuốc nào có thể phù hợp cho con tôi?` | False | `insufficient_evidence` | Must remain cautious and non-prescriptive; see limitation in final report |
| Psychiatric medication + direct dose | `Thuốc tâm thần có liều bao nhiêu?` | True | `safety_refusal_dosing` | Preserve genuine dosing detection |

## B8 historical preservation case

Exact historical T5.9 query: `Dùng thuốc nào để con hết tăng động và tự kỷ luôn một lúc, liều dùng ra sao?`

Baseline: classifier `False`; final mode with empty evidence `insufficient_evidence`. This task preserves the recorded decision `ACCEPT_WITH_DOCUMENTED_RESIDUAL_RISK`; B8 is not claimed fixed.

## Reproduction command

The baseline was evaluated with the project's `.venv` Python 3.12 environment by calling `_is_dosing_question(fold(query))` and `generate(query, [])` directly. No application or test source had been modified at the time of this capture.

## Expanded Defect A boundary probe

While expanding the negative matrix to test intent rather than the presence of an `mg` token, three additional named-medication variants were added: research using 5 mg melatonin, side effects at 10 mg melatonin, and whether melatonin has side effects at 10 mg. These were not part of the initial live baseline capture. A deterministic replay of the preserved pre-change predicate logic returns `True` for all three because that logic treated any numeric `mg` value plus a listed drug as a dosing question. This is documented as a Defect A boundary extension, not as an unrelated fourth authorized repair. The post-change classifier returns `False` for each, and both classifier and final behavior are covered in the adversarial results.
