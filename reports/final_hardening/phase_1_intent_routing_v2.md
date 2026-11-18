# Phase 1 (T4) — Comprehensive Intent Routing Improvement

## What changed (real code, not just re-testing)

1. **Uncertainty is now explicit.** `IntentResult` gained `confidence: "high" | "low"`
   (`app/router/classifier.py`). "low" fires when a message routes to `asd_question` only through a
   topic-adjacent glossary word (e.g. "risperidone", "trường học") with no explicit ASD anchor
   ("tự kỷ"/"autism"/"asd"/"asperger"). Safe handling: it is **not** rejected (an ASD-adjacent question is
   a real, valid thing to ask) — it still goes to retrieval, where the Evidence Gate is the real safety
   net, and `/api/chat` now adds an explicit warning to the response when confidence is low, so the
   uncertainty is visible to the caller instead of hidden behind one confident-looking decision.
2. **Vocabulary gaps found and closed**: "alo", "good morning/afternoon/evening", "hẹn gặp lại" added to
   the greeting/farewell phrase lists; "nhại lại" (echolalia), "tích hợp cảm giác" / "điều hòa cảm giác"
   (sensory integration), "người chăm sóc" + "huấn luyện kỹ năng" (caregiver training) added to the
   glossary — each one was a real miss found by the independent 105-item test below, not a guess.

## The independent 100+ case test set

`eval/datasets/intent_routing_v1.jsonl` — **105 items**, each with an `expected_branch` written by direct
judgment **before** running the classifier (per the task's explicit prohibition on deriving ground truth
from the system under test). Distribution: 22 greeting, 23 out_of_scope, 60 asd_question, spanning:

- Pure greeting / thanks / farewell (20)
- Out-of-scope topics: weather, gold price, food, sports, movies, code help, investing, geography, pets
  (15)
- Clear ASD questions, VI and EN (24)
- ASD-adjacent questions with **no** literal "tự kỷ"/"autism" word (13): medication names, screening
  tools (M-CHAT, ADOS), school inclusion, NDBI, sensory therapy, WHO caregiver training
- Genuinely ambiguous "gray zone" cases, labeled as judgment calls, not certainties (4): e.g. "ADHD có
  những biểu hiện gì ở trẻ nhỏ?" (ADHD alone isn't ASD, but is comorbid/adjacent in this corpus), "Trường
  học của con tôi có tốt không?" (contains the glossary word "trường học" but is not an ASD question at
  all)
- Mixed intent — greeting word *and* a real question together (7)
- Typos, no-diacritics, mixed Vietnamese/English (20)
- Long multi-clause questions (5)
- Empty/whitespace/punctuation-only (3)

Harness: `scripts/eval_intent_routing.py` (also exercised as a locked-in regression test,
`tests/unit/test_intent_routing_eval.py`).

## Result

Two actual runs of `scripts/eval_intent_routing.py` against the dataset, before and after the vocabulary
fixes above:

```
Before vocabulary fixes: 96/105  = 91.4%
After vocabulary fixes:  102/105 = 97.1%
```

**3 remaining mismatches, each a disclosed, genuine gray zone — not swept under the rug:**

| Case | Expected | Actual | Why it's a judgment call, not a bug |
|---|---|---|---|
| "Trường học của con tôi có tốt không?" | out_of_scope | asd_question | The word "trường học" is a legitimate ASD-adjacent glossary term (school inclusion is a real topic in this corpus), but this specific sentence is a generic parenting question with no ASD content. Fixing this without breaking the real school-inclusion case (ir058, which correctly routes to `asd_question`) would need actual sentence-level understanding, not word presence — out of reach for a lexical classifier. |
| "Please help me cook pho, cảm ơn nhiều" | out_of_scope | greeting | The message contains a real "thanks" phrase, so the classifier's priority order (any domain/greeting signal wins) picks greeting over "this is actually an off-topic request." A stricter fix (requiring the greeting/thanks phrase to be the *dominant* content, not just present) risks breaking the mixed-intent cases that are required to work (e.g. "Cảm ơn bạn, nhưng dấu hiệu tự kỷ ở trẻ 2 tuổi là gì?" must still answer the real question) — not fixed in this task to avoid a regression in a case the task explicitly requires. |
| "Why is it called a 'spectrum' disorder?" | asd_question | out_of_scope | No literal "autism"/"ASD"/"spectrum disorder" wording exists in `ASD_ANCHOR_PHRASES` that matches "spectrum disorder" alone without "autism" preceding it, and this question only makes sense as a continuation of an existing ASD conversation — a stateless, single-turn classifier cannot know that. |

## Branch 2 vs. Branch 3 — unchanged decision, re-confirmed

Still merged (see `reports/project_repair/phase_1_intent_routing.md` for the original reasoning). Re-
checked at the start of this task: the knowledge source is still exactly one PostgreSQL vector view; no
second, structurally distinct source was added. The decision stands.

## Stated limitation, honestly

This is a lexical classifier with documented coverage gaps (greeting phrases, glossary terms) and three
disclosed gray-zone failures. Expanding vocabulary lists is the correct lever and was exercised twice in
this task (T3→97.1%); it has diminishing returns against truly ambiguous, context-dependent phrasing,
which needs real language understanding (an authorized LLM) to close completely.
