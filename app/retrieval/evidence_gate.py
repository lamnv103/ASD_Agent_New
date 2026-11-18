"""Evidence Sufficiency Gate: decides whether retrieved evidence actually supports the question asked.

Wraps `DenseRetriever`'s output; never modifies `dense.py`, so the T2.3 benchmark (which calls
`DenseRetriever` directly, not through this module) is byte-for-byte unaffected by this file's existence.

Why this exists: the independent expert evaluation found that a dense-retrieval "ok" status does not mean
the evidence is on-topic. Four confirmed cases (vaccines, risperidone dosing, stem cells, epilepsy
comorbidity) returned `retrieval_status: "ok"` with Top-5 evidence that never mentions the actual topic
asked about. Cosine similarity alone cannot catch this: the corpus-wide anchor terms ("tự kỷ"/"autism")
dominate the similarity signal for nearly every chunk, so an off-topic-but-ASD-flavored chunk can still
score a moderate similarity.

Method (deliberately conservative, per instruction not to use an arbitrary similarity threshold as proof
of sufficiency): a chunk is "supporting" only if BOTH (a) its cosine similarity clears a low floor
(rejects pure noise) AND (b) it passes a topic check. The topic check has two cases:
  - If the query contains no topic-SPECIFIC glossary term (e.g. "Rối loạn phổ tự kỷ là gì?" — the
    question *is* the generic ASD topic), the topic check is satisfied by the similarity floor alone.
  - If the query DOES contain a specific term (vaccine, risperidone, stem cell, epilepsy, ...), the chunk
    must actually contain a matching English/Vietnamese fragment for at least one of those terms. A chunk
    that only shares the generic "tự kỷ"/"autism" wording does not count — that is exactly what let the
    four confirmed failures through before.

Stated limitation (required by the task brief rather than hidden): this lexical check cannot detect a
topically-adjacent-but-wrong-condition chunk (e.g. ADHD-specific text surfacing for an ASD-parenting
question) when both conditions happen to share the queried specific term. That needs real semantic
understanding, which is unavailable without an authorized LLM. When this method cannot determine
sufficiency with confidence, it defaults to the cautious outcome (`insufficient`), not the permissive one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.nlp.text_match import chunk_matches_terms, specific_terms
from app.retrieval.types import RetrievedChunk

MIN_SIMILARITY = 0.12  # a conservative floor, not a sufficiency proof; see module docstring.

# Support strength, surfaced per chunk (not just a single sufficient/insufficient bit) so the task's
# distinction between direct / partial / generic evidence is visible, not collapsed into one boolean:
#   "direct"   — the specific term the query asked about is in the chunk's TITLE/SECTION heading, i.e.
#                this chunk is actually *about* that topic, not just mentioning it in passing.
#   "indirect" — the specific term only appears in the body content, not the heading — the chunk mentions
#                the topic but may not be centrally about it.
#   "generic"  — the query had no specific topic term to check (e.g. "what is ASD?"); support rests on
#                similarity alone, which is a weaker signal, stated here rather than hidden behind "ok".
SupportType = str  # "direct" | "indirect" | "generic"

_AGE_PATTERN = re.compile(r"\b(\d{1,3})\s*(tháng|thang|tuổi|tuoi|month|year)", re.IGNORECASE)


@dataclass(frozen=True)
class SupportDetail:
    chunk: RetrievedChunk
    support_type: SupportType
    age_mismatch: bool  # query names a specific age/number this chunk's content does not corroborate


@dataclass(frozen=True)
class EvidenceAssessment:
    sufficient: bool
    reason: str
    supported: list[RetrievedChunk]  # the subset of results that actually back the question (unchanged shape)
    unsupported_dropped: int
    details: list[SupportDetail] = field(default_factory=list)  # 1:1 with `supported`, extra classification


def _query_ages(query: str) -> list[str]:
    return [m.group(1) for m in _AGE_PATTERN.finditer(query)]


def assess(query: str, results: list[RetrievedChunk]) -> EvidenceAssessment:
    if not results:
        return EvidenceAssessment(False, "no_results", [], 0, [])

    terms = specific_terms(query)
    query_ages = _query_ages(query)
    supported: list[RetrievedChunk] = []
    details: list[SupportDetail] = []
    for chunk in results:
        if chunk.cosine_similarity < MIN_SIMILARITY:
            continue
        heading = f"{chunk.title} {chunk.section}"
        # Title/section are checked too: the topic word (e.g. "Signs and Symptoms of ...") often lives in
        # the heading rather than being repeated in the excerpt body itself.
        searchable = f"{heading} {chunk.content}"
        if not terms:
            support_type: SupportType = "generic"
        elif chunk_matches_terms(heading, terms):
            support_type = "direct"
        elif chunk_matches_terms(searchable, terms):
            support_type = "indirect"
        else:
            continue  # no match anywhere -> not supporting at all, dropped

        age_mismatch = bool(query_ages) and not any(age in chunk.content for age in query_ages)
        supported.append(chunk)
        details.append(SupportDetail(chunk, support_type, age_mismatch))

    dropped = len(results) - len(supported)
    if not supported:
        reason = "no_topic_specific_evidence" if terms else "below_similarity_floor"
        return EvidenceAssessment(False, reason, [], dropped, [])
    return EvidenceAssessment(True, "ok", supported, dropped, details)
