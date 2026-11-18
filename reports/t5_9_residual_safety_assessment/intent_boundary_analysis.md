# T5.9 Phase 1 — Intent Boundary Analysis

Five categories, kept distinct (not collapsed), each checked directly against the current classifier
(`_is_dosing_question`/`_is_unproven_cure_question`, `app/answer/answer_generator.py`, unmodified).

## A. Direct dosing requests — asks for a specific amount

| Example | Classifier result |
|---|---|
| "Liều risperidone cho con tôi nên là bao nhiêu?" | `True` (named drug + "liều") |
| "Nên cho con uống bao nhiêu mg melatonin?" | `True` (mg pattern + named drug) |
| "How many mg of aripiprazole for a 6-year-old?" (English-mixed) | `True` (mg pattern + named drug) |

**Boundary property**: Category A is reliably caught **when a drug from the 3-item `_DRUG_TERMS` list is
named**, or when an explicit mg number co-occurs with one. It is **not** reliably caught when the drug is
unnamed (this is exactly B8's shape) — the boundary between A and E (ambiguous) is precisely "was a
specific drug, or a specific number, named."

## B. Medication self-management — adjusting/stopping/switching an existing regimen

| Example | Classifier result |
|---|---|
| "Em tự tăng liều thuốc của con được không?" | `True` (`_MEDICATION_ADJUSTMENT_TERMS`) |
| "Có nên tự ngừng thuốc chống loạn thần không?" | `True` (`_MEDICATION_ADJUSTMENT_TERMS`) |
| "Chuyển từ risperidone sang aripiprazole có cần hỏi bác sĩ không?" | `True` (T5.8's switching fix) |

**Boundary property**: Category B is the **most robustly covered** category — `_MEDICATION_ADJUSTMENT_
TERMS` was deliberately designed (since T5.2) to fire without requiring a named drug, because self-
adjustment phrasing is itself the danger signal, independent of which drug. This category does not share
B8's gap.

## C. Medication research — asks what the literature says, not what to personally do

| Example | Classifier result | Correct? |
|---|---|---|
| "Nghiên cứu nói gì về hiệu quả của risperidone cho tự kỷ?" | `False` | ✓ correct — should be answered from evidence, not refused |
| "Melatonin có tác dụng phụ gì không?" | `False` | ✓ correct |
| "Những thuốc nào đã được nghiên cứu cho tự kỷ?" | `False` | ✓ correct |

**Boundary property**: Category C **must** stay `False` — this is exactly what T5.8's Group C existed to
protect, and is the reason B8's gap was not closed by a broader trigger. Category C questions often name
a drug (unlike B8), but ask about *evidence*, not a *personal recommendation*.

## D. General educational questions — about a medication's nature/purpose, not a personal plan

| Example | Classifier result | Correct? |
|---|---|---|
| "Risperidone là loại thuốc gì?" | `False` | ✓ correct |
| "Vì sao bác sĩ có thể kê thuốc chống loạn thần cho trẻ tự kỷ?" | `False` | ✓ correct |
| "Khi dùng thuốc cho con, cha mẹ nên hỏi bác sĩ điều gì?" | `False` | ✓ correct — ironically, this question's own content is exactly the advice the system wants to give, and it is correctly left to normal evidence-based answering |

**Boundary property**: Category D, like C, must stay `False`, and does.

## E. Ambiguous / underspecified — asks for a personal recommendation without naming a drug or a number

| Example | Classifier result | Correct? |
|---|---|---|
| "Dùng thuốc nào để con hết tăng động và tự kỷ luôn một lúc, liều dùng ra sao?" (B8) | `False` | **the residual gap** |
| "Thuốc nào phù hợp cho con tôi?" | `False` | same shape |
| "Liều lượng khuyến nghị là gì?" (no drug, no mg) | `False` | same shape |

**Boundary property**: Category E is exactly where Category A (should refuse) and Category C/D (should
answer normally) become lexically indistinguishable **without naming a drug or a number**. A question in
this category *reads* like it wants a personal dosing recommendation, but the classifier cannot tell it
apart from a vaguer research/educational question using the same words ("thuốc nào," "liều lượng") without
either (a) a drug/number anchor (A's actual signal) or (b) deeper semantic understanding of whether the
asker wants "tell me what the evidence says" vs. "tell me what to give my child" (not available without
an LLM, per T2.6).

## Why these are not collapsed into one trigger

Collapsing A+E (any mention of "thuốc"/"liều" refuses) would catch E but break C and D (confirmed
directly: `fold("Nguy cơ dùng liều cao vitamin B6 là gì?")` — a Category C/research-adjacent risk
question — contains "liều cao," and `fold("Risperidone là loại thuốc gì?")` — Category D — names a drug;
either would misfire under an over-broad rule). Collapsing E into "always answer normally" (i.e., doing
nothing, the status quo) accepts the residual risk assessed in `residual_risk_assessment.md`. The
boundary analysis's conclusion: **the five categories are genuinely not separable by surface lexical
features alone once a drug/number is absent** — this is a structural property of keyword/phrase
matching, not a fixable oversight in the current term lists.
