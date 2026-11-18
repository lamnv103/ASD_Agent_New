"""Deterministic, no-ML text matching shared by the intent router and the evidence sufficiency gate.

There is no authorization for a live embedding or LLM call on arbitrary user text (T2.6:
APPROVAL_REQUIRED), and no ML classifier library is installed (T2.5 audit). Everything here is plain
Python string matching, made more robust than a literal keyword list by: Unicode NFD diacritic folding
(so "tu ky", "tự  kỷ", "Tự Kỷ" all match), substring (not token-exact) phrase matching, and a bilingual
VI/EN glossary (most of the stored corpus is English-language source text, while users ask in
Vietnamese — a pure Vietnamese keyword match would never overlap with the retrieved evidence at all).

Known limitation, stated once here rather than repeated at every call site: this catches clear-cut
cases (no shared vocabulary at all, or a specific topic word absent from every candidate) but cannot
resolve deeper semantic cases such as a topically-adjacent-but-wrong condition (e.g. ADHD text surfacing
for an ASD-parenting question) — that needs real language understanding, which is out of scope without
an authorized LLM.
"""

from __future__ import annotations

import re
import unicodedata

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_SPACE = re.compile(r"\s+")


def fold(text: str) -> str:
    """Lowercase, strip Vietnamese diacritics, collapse whitespace/punctuation. Used for ALL matching."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("đ", "d")
    text = _PUNCT.sub(" ", text)
    return _SPACE.sub(" ", text).strip()


def _padded(folded_text: str) -> str:
    return f" {folded_text} "


def contains_word(folded_text: str, phrase: str) -> bool:
    """Word/phrase-boundary match: `fold(phrase)` must appear as whole word(s), not as a substring run
    inside another word (e.g. the greeting word "hi" must not match inside "nhiêu" or "thích")."""
    return f" {fold(phrase)} " in _padded(folded_text)


def contains_any(folded_text: str, phrases: list[str]) -> bool:
    return any(contains_word(folded_text, p) for p in phrases)


def matched_phrases(folded_text: str, phrases: list[str]) -> list[str]:
    return [p for p in phrases if contains_word(folded_text, p)]


# Phrases that identify a message as being about ASD at all (as opposed to being about anything else).
# Deliberately narrow: broad words like "trẻ" (child) or "phát triển" (development) are excluded because
# they occur constantly in non-ASD contexts too and would make the out-of-scope check useless.
ASD_ANCHOR_PHRASES = [
    "tu ky", "tự kỷ", "autism", "asd", "roi loan pho", "rối loạn phổ",
    "asperger", "tu ki", "tự kỉ",
]

# Greeting / social small-talk phrases (Vietnamese + English). Matched only when no ASD anchor is present
# (see classifier.py) — "Chào bạn, tự kỷ là gì?" must route to the real question, not to small talk.
GREETING_PHRASES = [
    "xin chao", "xin chào", "chao ban", "chào bạn", "chao anh", "chào anh", "chao chi", "chào chị",
    "hello", "hi", "chao", "chào", "cam on", "cảm ơn", "thank you", "thanks", "tam biet", "tạm biệt",
    "bye", "goodbye", "chuc ban", "chúc bạn", "rat vui", "rất vui", "alo", "good morning", "good afternoon",
    "good evening", "hen gap lai", "hẹn gặp lại",
]

# Bilingual glossary: Vietnamese/mixed phrase -> English fragments to look for in (mostly English) chunk
# text. Keys are specific/topical terms, deliberately excluding the generic ASD anchor terms above, so
# that "what is ASD" (no specific term) and "does X cause ASD" (a specific term) are handled differently —
# see evidence_gate.py. Coverage is partial by design (covers this project's known question set plus
# adjacent common topics); extend as new topics are demoed.
GLOSSARY: dict[str, list[str]] = {
    "vac xin": ["vaccine", "vaccination", "immuniz"],
    "vacxin": ["vaccine", "vaccination", "immuniz"],
    "tiem chung": ["vaccine", "vaccination", "immuniz"],
    "te bao goc": ["stem cell"],
    "dong kinh": ["epilepsy", "seizure"],
    "co giat": ["seizure", "convulsion"],
    "risperidone": ["risperidone"],
    "aripiprazole": ["aripiprazole"],
    "lieu luong": ["dose", "dosage", "mg"],
    "lieu dung": ["dose", "dosage", "mg"],
    "nguy co": ["risk"],
    "yeu to": ["factor"],
    "di truyen": ["genetic", "gene", "heredit"],
    "can thiep": ["intervention", "treatment"],
    "cha me": ["parent"],
    "phu huynh": ["parent"],
    "giao duc": ["education", "educat"],
    "truong hoc": ["school"],
    "lop hoc": ["classroom", "school"],
    "hoa nhap": ["inclusion", "inclusive"],
    "chan doan": ["diagnos"],
    "sang loc": ["screen"],
    "hanh vi": ["behavior", "behaviour"],
    "giao tiep": ["communicat"],
    "dau hieu": ["sign", "symptom"],
    "trieu chung": ["symptom"],
    "phat trien": ["develop"],
    "moc phat trien": ["milestone"],
    "ken an": ["food selectivity", "picky eat", "feeding", "mealtime"],
    "giac ngu": ["sleep"],
    "melatonin": ["melatonin"],
    "gluten": ["gluten"],
    "casein": ["casein"],
    "aba": ["applied behavior analysis", " aba "],
    "ndbi": ["ndbi", "naturalistic developmental"],
    "dsm-5": ["dsm-5", "dsm5", "diagnostic and statistical manual"],
    "dsm 5": ["dsm-5", "dsm5", "diagnostic and statistical manual"],
    "m-chat": ["m-chat", "mchat"],
    "ados": ["ados"],
    "dong mac": ["comorbid"],
    "nhai lai": ["echolalia", "repeat"],
    "tich hop cam giac": ["sensory integration"],
    "dieu hoa cam giac": ["sensory integration", "sensory processing"],
    "nguoi cham soc": ["caregiver"],
    "huan luyen ky nang": ["caregiver skills training", "caregiver training"],
    "tang lieu": ["increase the dose", "dosage"],
    "giam lieu": ["decrease the dose", "dosage"],
    "ngung thuoc": ["discontinu", "stop", "medication"],
    "doi thuoc": ["change medication", "switch medication"],
    "thuoc tam than": ["psychiatric medication", "antipsychotic"],
    "chu y chung": ["joint attention"],
    "so thich han hep": ["restricted interest"],
    "khong chi tay": ["not pointing", "does not point"],
    "chua noi": ["not talking", "no words", "speech delay"],
    "cham noi": ["speech delay", "language delay"],
    "xep do thanh hang": ["lines up", "lining up"],
    "xep do vat": ["lines up", "lining up"],
    "adhd": ["adhd", "attention-deficit", "attention deficit"],
    "lo au": ["anxiety"],
    "truong thanh": ["adult"],
    "nguoi lon": ["adult"],
    "day thi": ["puberty", "adolescen"],
    "thanh nien": ["adolescen", "teen"],
}


def specific_terms(query: str) -> list[str]:
    """Glossary keys whose folded form appears in the (folded) query — the query's topic-specific words."""
    q = fold(query)
    return [key for key in GLOSSARY if contains_word(q, key)]


def chunk_matches_terms(chunk_text: str, terms: list[str]) -> bool:
    text = chunk_text.lower()
    return any(frag in text for term in terms for frag in GLOSSARY[term])
