"""Intent routing: decides which of the three branches a user message goes to, before any embedding,
database call, or answer generation happens.

Branch "greeting": small talk (hello/thanks/goodbye) with no ASD content. Answered directly, no
retrieval of any kind.

Branch "out_of_scope": no ASD-domain signal at all (e.g. "what's the weather today?"). Rejected before
retrieval, so an off-topic question can never come back with `retrieval_status: "ok"` and unrelated ASD
evidence attached to it — this was the Critical finding in the independent expert evaluation (q062).

Branch "asd_question": everything else. This is where retrieval + the Evidence Sufficiency Gate (Phase 2)
+ answer generation (Phase 3) run. The task brief describes this as two branches ("Nhánh 2 – general
information retrieval" and "Nhánh 3 – professional ASD questions"); this project has exactly one
knowledge source and one retrieval pipeline (the research vector view), so there is nothing for a
separate Branch 2 to do differently from Branch 3 today — they are intentionally merged here, and this
is disclosed in `reports/project_repair/phase_1_intent_routing.md` rather than faked with a second branch
that would behave identically to the first.

This is a deterministic lexical classifier (see `app/nlp/text_match.py` for the method and its stated
limits), not a trained model and not an LLM — no live provider call is made here, consistent with T2.6.

`confidence` ("high"/"low") makes the classifier's uncertainty visible instead of hiding it behind a
single always-confident decision. "low" fires when the only reason a message was routed to
`asd_question` is a topic-adjacent glossary word (e.g. "risperidone", "trường học") with no explicit ASD
anchor ("tự kỷ"/"autism"/"asd"/"asperger") — such a message is plausibly, but not certainly, about ASD.
The safe handling for "low" confidence is NOT to reject it (an ASD-adjacent question like a medication or
school question is exactly the kind of thing a real user asks) — it still proceeds to retrieval, where the
Evidence Sufficiency Gate (Phase 2) is the actual safety net, and the uncertainty is surfaced to the
caller (`/api/chat` adds a warning) rather than silently assumed away.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.nlp.text_match import ASD_ANCHOR_PHRASES, GLOSSARY, GREETING_PHRASES, contains_any, contains_word, fold

Branch = Literal["greeting", "out_of_scope", "asd_question"]

# The actual reply text lives in app.answer.answer_generator.GREETING_REPLY — this module only classifies.

_THANKS_PHRASES = ["cam on", "cảm ơn", "thank you", "thanks"]
_FAREWELL_PHRASES = ["tam biet", "tạm biệt", "bye", "goodbye"]


Confidence = Literal["high", "low"]


@dataclass(frozen=True)
class IntentResult:
    branch: Branch
    reason: str
    greeting_kind: str | None = None  # "greeting" | "thanks" | "farewell", only when branch == "greeting"
    confidence: Confidence = "high"


def _domain_signal(folded: str) -> tuple[bool, bool]:
    """(has_anchor, has_glossary_term_only) — distinguishes a clear ASD anchor from a merely topic-adjacent word."""
    has_anchor = contains_any(folded, ASD_ANCHOR_PHRASES)
    has_glossary = any(contains_word(folded, key) for key in GLOSSARY)
    return has_anchor, (not has_anchor and has_glossary)


def classify(query: str) -> IntentResult:
    if not isinstance(query, str) or not query.strip():
        return IntentResult("out_of_scope", "empty_message")
    folded = fold(query)

    has_anchor, glossary_only = _domain_signal(folded)
    if has_anchor or glossary_only:
        # An ASD/topic signal always wins over a greeting word in the same message (mixed intent:
        # "Chào bạn, tự kỷ là gì?" must answer the real question, not just say hello back).
        confidence: Confidence = "low" if glossary_only else "high"
        reason = "asd_adjacent_term_only_no_anchor" if glossary_only else "asd_domain_signal_present"
        return IntentResult("asd_question", reason, confidence=confidence)

    if contains_any(folded, _THANKS_PHRASES):
        return IntentResult("greeting", "thanks_only", "thanks")
    if contains_any(folded, _FAREWELL_PHRASES):
        return IntentResult("greeting", "farewell_only", "farewell")
    if contains_any(folded, GREETING_PHRASES):
        return IntentResult("greeting", "greeting_only", "greeting")

    return IntentResult("out_of_scope", "no_asd_domain_signal_found")
