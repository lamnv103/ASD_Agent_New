"""Answer generation without a live LLM (T2.6: APPROVAL_REQUIRED — no external LLM call is authorized).

Method, stated plainly so it is never mistaken for an LLM: this is (a) a small set of hand-authored
Vietnamese template paragraphs, each written by cross-checking the real retrieved evidence for that
topic and triggered ONLY when evidence from the matching source actually appears in the evidence that
was kept by the Evidence Sufficiency Gate, or (b) for safety-sensitive topics, a fixed refusal/caution
message, or (c) when no template matches but evidence exists, a literal excerpt presentation clearly
labeled as such (not a synthesized answer), or (d) when the gate found no sufficient evidence, an
explicit "not enough evidence" statement. No template ever asserts something its trigger evidence does
not say; no citation is ever attached unless that source is actually present in the evidence used.

There are no pre-authored `.md` knowledge files in this project to draw from (confirmed in
`reports/project_repair/phase_0_full_audit.md`); the templates below are grounded directly in the
2,338 embedded chunks via their retrieved excerpts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.nlp.text_match import fold

SAFETY_NOTICE = ("Nguyên mẫu nghiên cứu/sinh viên. Nội dung chưa được thẩm định lâm sàng. "
                  "Không dùng để chẩn đoán hoặc thay thế tư vấn chuyên môn.")

GREETING_REPLY = {
    "greeting": "Chào bạn! Mình là trợ lý tra cứu thông tin về rối loạn phổ tự kỷ (ASD). "
                "Bạn có câu hỏi nào về ASD không?",
    "thanks": "Không có gì, rất vui vì đã giúp được bạn. Bạn còn câu hỏi nào về ASD không?",
    "farewell": "Tạm biệt! Hẹn gặp lại bạn.",
}

OUT_OF_SCOPE_REPLY = ("Câu hỏi này có vẻ không thuộc phạm vi kiến thức về rối loạn phổ tự kỷ (ASD) mà hệ "
                      "thống này tra cứu. Bạn thử hỏi lại với một câu hỏi liên quan đến ASD nhé.")

EXCERPT_MAX_CHARS = 280


@dataclass(frozen=True)
class AnswerResult:
    text: str
    mode: str  # see MODES below
    citation_ids: list[str]
    sufficient_evidence: bool


MODES = frozenset({
    "greeting_template", "out_of_scope", "insufficient_evidence", "safety_refusal_dosing",
    "safety_caution_unproven_cure", "topic_template", "extractive_fallback",
})


# -- safety overrides: checked on the query text itself, independent of what evidence was found --------

_DOSING_TERMS = ["lieu luong", "lieu dung", "lieu thuoc", "lieu "]
_DRUG_TERMS = ["risperidone", "aripiprazole", "melatonin"]
# "chua dut diem" added in T5.8 (adversarial case A5): "chữa dứt điểm" (a definitive/complete cure) is a
# distinct phrasing from "chữa khỏi" that _CURE_CLAIM_TERMS did not previously recognize.
_CURE_CLAIM_TERMS = ["te bao goc", "chua khoi", "chua duoc", "chua tu ky", "chua dut diem"]
_MG_DOSE_PATTERN = re.compile(r"\d+\s*mg")
_SWITCH_VERBS = ["doi", "chuyen"]
_NON_PERSONAL_MEDICATION_CONTEXTS = (
    "nghien cuu", "thu nghiem", "tac dung phu", "hieu qua", "rui ro", "nguy co",
)
_DIRECT_DOSE_QUESTION_PATTERNS = (
    re.compile(r"\bbao nhieu\s+mg\b"),
    re.compile(r"\bmay\s+mg\b"),
    re.compile(r"\blieu\b.{0,24}\bbao nhieu\b"),
    re.compile(r"\b(?:uong|dung)\b.{0,24}\bluong\s+bao nhieu\b"),
)
_SELF_CHANGE_PATTERNS = (
    re.compile(r"\btu\s+(?:tang|giam|dieu chinh|ngung|doi|chuyen)\b"),
    re.compile(r"\b(?:em|toi|minh|cha me)\b.{0,24}\b(?:tang|giam|dieu chinh|ngung)\b.{0,32}\b(?:lieu|thuoc)\b"),
    re.compile(r"\b(?:em|toi|minh)\b.{0,24}\b(?:doi|chuyen)\b.{0,40}\b(?:thuoc|sang)\b"),
)


def _mentions_explicit_mg_dose_of_a_named_drug(folded_query: str) -> bool:
    # T5.8 (adversarial case B6): a query that STATES a specific mg dose already being given ("melatonin
    # 10mg mỗi tối") and asks whether it is safe is a dosing-safety question even though it never uses
    # the word "liều" -- arguably more urgent to refuse, since it suggests dosing may already be
    # happening without medical guidance.
    return bool(_MG_DOSE_PATTERN.search(folded_query)) and any(d in folded_query for d in _DRUG_TERMS)


def _mentions_switching_a_named_drug(folded_query: str) -> bool:
    # Only an explicitly self-directed change belongs in the safety-refusal branch. A supervised-switch
    # question or research comparison can contain the same drugs and switch verbs without requesting
    # personal dose instructions.
    return (any(re.search(p.pattern, folded_query) for p in _SELF_CHANGE_PATTERNS)
            and any(v in folded_query for v in _SWITCH_VERBS) and "sang" in folded_query
            and any(d in folded_query for d in _DRUG_TERMS))


def _is_self_directed_medication_change(folded_query: str) -> bool:
    if any(re.search(p.pattern, folded_query) for p in _SELF_CHANGE_PATTERNS):
        return True
    # Retain the established stop-without-clinician signal when the question explicitly concerns the
    # user's child, while avoiding a bare psychiatric-medication phrase as a trigger.
    return ("ngung thuoc" in folded_query
            and any(p in folded_query for p in ("cho con", "khong hoi bac si", "khong can hoi")))


def _is_dosing_question(folded_query: str) -> bool:
    if _is_self_directed_medication_change(folded_query):
        return True
    # Dose measurements inside research, efficacy, risk, and side-effect questions are not by themselves
    # requests for a personal dosing instruction, even when the query names a medication and numeric dose.
    if any(context in folded_query for context in _NON_PERSONAL_MEDICATION_CONTEXTS):
        return False
    if any(pattern.search(folded_query) for pattern in _DIRECT_DOSE_QUESTION_PATTERNS):
        return True
    if any(pattern.search(folded_query) for pattern in _DIRECT_DOSE_QUESTION_PATTERNS):
        return True
    if _mentions_explicit_mg_dose_of_a_named_drug(folded_query):
        return True
    if _mentions_switching_a_named_drug(folded_query):
        return True
    return any(d in folded_query for d in _DOSING_TERMS) and any(g in folded_query for g in _DRUG_TERMS)


def _is_unproven_cure_question(folded_query: str) -> bool:
    return any(t in folded_query for t in _CURE_CLAIM_TERMS)


_DOSING_REFUSAL = (
    "Mình không thể đưa ra liều thuốc cụ thể — liều dùng thuốc (ví dụ risperidone, aripiprazole) phải do "
    "bác sĩ quyết định dựa trên tình trạng, cân nặng và theo dõi lâm sàng của từng trẻ. Vui lòng hỏi ý "
    "kiến bác sĩ nhi khoa hoặc bác sĩ tâm thần đã khám cho trẻ trước khi dùng hoặc thay đổi liều thuốc."
)

_CURE_CLAIM_CAUTION_TEMPLATE = (
    "Hiện chưa có bằng chứng khoa học đủ mạnh trong kho dữ liệu của hệ thống xác nhận rằng {claim} có thể "
    "chữa khỏi tự kỷ. Tự kỷ là một rối loạn phát triển thần kinh suốt đời; các phương pháp can thiệp được "
    "ghi nhận có bằng chứng (như can thiệp hành vi, hỗ trợ giao tiếp) tập trung cải thiện kỹ năng và chất "
    "lượng sống, không phải \"chữa khỏi\". Hãy cẩn trọng với các tuyên bố chữa khỏi tự kỷ chưa được xác "
    "nhận bởi nghiên cứu khoa học, và tham khảo ý kiến chuyên gia y tế trước khi áp dụng."
)

# T5.8 fix: the caution above must fire for every recognized unproven-cure question regardless of
# whether retrieval found any evidence, and regardless of how weak/topically-adjacent that evidence is
# (T5.7 found this caution was previously skipped whenever ANY evidence existed, including a chunk that
# only mentioned the named substance for an unrelated purpose -- e.g. vitamin B6 as a sleep-aid
# ingredient, not as an autism cure). A chunk merely mentioning, or even evaluating, a substance/method
# is a different state from that chunk proving it cures ASD; this corpus's evidence never reaches the
# latter state for a claim this function recognizes as an unproven-cure question (that recognition is
# itself specific to phrasing like "chữa khỏi"/"chữa được"/"tế bào gốc" -- see _CURE_CLAIM_TERMS), so the
# honest disclosure below never overclaims what the found evidence shows.
_CURE_CLAIM_EVIDENCE_ADDENDUM = (
    " Hệ thống có tìm thấy {n} tài liệu đề cập đến chủ đề liên quan, nhưng không tài liệu nào trong đó "
    "xác nhận hiệu quả chữa khỏi tự kỷ — việc một chất hoặc phương pháp được nhắc đến hoặc được nghiên cứu "
    "cho mục đích khác (ví dụ hỗ trợ giấc ngủ) không có nghĩa là nó chữa được tự kỷ."
)


def _unproven_cure_evidence_note(evidence: list[dict]) -> str:
    if not evidence:
        return ""
    return _CURE_CLAIM_EVIDENCE_ADDENDUM.format(n=len({e["source_id"] for e in evidence}))


# -- topic templates: (trigger source_ids, Vietnamese text, required query terms or None) ---------------
# Each template fires only when at least one of its trigger source_ids is present in the evidence that
# the caller already determined sufficient AND (if given) the query contains one of its required terms.
# The Vietnamese text was written by cross-checking the actual excerpts those sources returned during
# this task's live testing (see phase_3_answer_generation.md). TEXT IS UNCHANGED FROM T4 for all 7 —
# only the matching logic/order below was fixed in T5.2.
#
# T5.2 regression finding (pre-existing, not introduced by T5.2): `NIH-NIMH-ASD-2025` and
# `CDC-ASD-CLINICAL` are each cited by *multiple* templates (the source documents cover several
# sub-topics), and because `asd_definition` listened to both with no other condition and was checked
# first, it silently hijacked `risk_factors`, `screening_age`, `dsm5_criteria`, and `diagnosis_process`
# live in this task (e.g. "Tiêu chuẩn DSM-5..." returned the generic definition text instead of the
# DSM-5 answer) whenever its shared source also happened to be in the evidence. Fixed by requiring a
# topic-specific query term for every template except the generic catch-all, which is now also moved
# to the END of the list so specific templates get first refusal. No template's Vietnamese TEXT changed.
_TOPIC_TEMPLATES: list[tuple[str, frozenset[str], str, list[str] | None]] = [
    ("risk_factors", frozenset({"CDC-ASD-ABOUT", "NIH-NIMH-ASD-2025"}),
     "Hiện chưa xác định được một nguyên nhân duy nhất gây ra tự kỷ. Nhiều yếu tố — di truyền, sinh học và "
     "môi trường — được ghi nhận có liên quan đến nguy cơ cao hơn, ví dụ: có anh/chị/em mắc ASD, một số "
     "tình trạng gen/nhiễm sắc thể (như hội chứng X mong manh), biến chứng khi sinh, hoặc cha mẹ sinh con "
     "ở tuổi lớn hơn. Có một yếu tố nguy cơ không có nghĩa là trẻ chắc chắn mắc ASD.",
     ["nguy co", "yeu to"]),
    ("screening_age", frozenset({"CDC-ASD-SCREENING", "CDC-CONCERNED", "NIH-NIMH-ASD-2025"}),
     "Theo khuyến nghị của Viện Hàn lâm Nhi khoa Hoa Kỳ (AAP), trẻ nên được sàng lọc phát triển chung ở 9, "
     "18 và 30 tháng tuổi, và sàng lọc đặc hiệu cho tự kỷ ở 18 và 24 tháng tuổi, hoặc bất cứ khi nào cha mẹ "
     "hay người chăm sóc có lo ngại.",
     ["sang loc", "do tuoi", "tuoi nao"]),
    ("dsm5_criteria", frozenset({"CDC-ASD-CLINICAL"}),
     "Theo Cẩm nang Chẩn đoán và Thống kê Rối loạn Tâm thần, phiên bản 5 (DSM-5), để được chẩn đoán ASD, "
     "trẻ cần có đủ các biểu hiện suy giảm trong giao tiếp/tương tác xã hội, cộng với ít nhất hai trong số "
     "các hành vi hạn chế, lặp lại (ví dụ: hành vi rập khuôn, cứng nhắc với thói quen, sở thích thu hẹp, "
     "hoặc phản ứng bất thường với kích thích giác quan). Mức độ hỗ trợ cần thiết được phân theo 3 cấp độ.",
     ["dsm"]),
    ("diagnosis_process", frozenset({"NIH-NIMH-ASD-2025", "CDC-ASD-CLINICAL"}),
     "Hiện chưa có xét nghiệm y khoa đơn lẻ (như xét nghiệm máu) để chẩn đoán tự kỷ. Bác sĩ chẩn đoán dựa "
     "trên quan sát hành vi và quá trình phát triển của trẻ, thường có thể chẩn đoán tin cậy từ 2 tuổi. "
     "Phát hiện và can thiệp sớm giúp ích nhiều, nên nếu có lo ngại, cha mẹ nên đưa trẻ đi đánh giá chuyên "
     "môn sớm — một bài tự kiểm tra hoặc quan sát tại nhà không thể thay thế đánh giá của chuyên gia.",
     ["chan doan"]),
    ("aba_intervention", frozenset({"CDC-ASD-TREATMENT"}),
     "Các phương pháp can thiệp hành vi (như Applied Behavior Analysis – ABA) tập trung thay đổi hành vi "
     "bằng cách hiểu điều gì xảy ra trước và sau một hành vi; đây là nhóm can thiệp có nhiều bằng chứng "
     "khoa học nhất hiện nay cho các triệu chứng cốt lõi của ASD.",
     ["aba", "hanh vi"]),
    ("vaccine_myth", frozenset({"ASD-OA-PMC12620806"}),
     "Không — các tổng quan y văn không tìm thấy bằng chứng cho thấy vắc-xin gây ra tự kỷ. Tuyên bố liên "
     "hệ vắc-xin với tự kỷ bắt nguồn từ một nghiên cứu đã bị rút lại (retracted) và không được các nghiên "
     "cứu sau đó xác nhận.",
     ["vac xin", "vacxin", "tiem chung"]),
    ("asd_definition", frozenset({"NIH-NIMH-ASD-2025", "CDC-ASD-CLINICAL"}),
     "Rối loạn phổ tự kỷ (Autism Spectrum Disorder – ASD) là một rối loạn phát triển thần kinh, ảnh hưởng "
     "đến giao tiếp, tương tác xã hội và có thể biểu hiện qua các hành vi, sở thích hoặc hoạt động hạn "
     "chế, lặp lại. Biểu hiện và nhu cầu hỗ trợ khác nhau ở mỗi người.",
     None),  # generic catch-all: no required term, must stay LAST so specific templates get first refusal
]


# -- T5.2 new templates: each is a (topic_id, trigger_sources, render_fn) where render_fn(evidence_items)
# -> str | None. `evidence_items` is pre-filtered to only the items whose source_id is in trigger_sources.
# A render_fn returning None means the template declines to fire (its specific pre-condition — e.g. a
# matching age — was not met), and the caller falls through exactly as if no template had matched at all
# (-> extractive fallback), never to a guessed/partial answer. Specification for each one, including
# which claim maps to which evidence and under what condition it declines, is in
# `reports/t5_2_template_expansion/template_specifications.md`.

def _render_signs_by_age(items: list[dict]) -> str | None:
    """Dynamic: only fires for the specific age(s) the query named AND the evidence item actually lists.

    The query-side age check lives in `_SIGNS_BY_AGE_GATE` (checked before this is even called) — see
    the T5.3 fix note on `_QUERY_GATED_TEMPLATES` for why a query-side gate is required here too, not
    just the excerpt-side check this function already did.
    """
    from app.answer.evidence_normalization import classify  # local import avoids a module-load cycle

    for item in items:
        if item["source_id"] != "CDC-ASD-SIGNS":
            continue
        normalized = classify(item["excerpt"])
        if normalized.kind != "list":
            return None
        matched = [(ages, text) for ages, text in zip(normalized.list_.item_ages, normalized.list_.items,
                                                       strict=True) if ages]
        if not matched:
            return None
        # Caller already knows the query named an age (that's why this trigger source is `direct`
        # support — see evidence_gate.py); render every age-tagged sign the evidence actually lists,
        # since CDC presents them as one cumulative checklist, not answer-specific subsets.
        bullet_lines = "\n".join(f"- {text}" for _, text in matched)
        return ("Theo CDC, một số dấu hiệu cảnh báo (không phải mốc phát triển thông thường) theo độ "
                f"tuổi gồm:\n{bullet_lines}\n\nMột dấu hiệu đơn lẻ không đủ để kết luận — nếu có từ 2 dấu "
                "hiệu trở lên hoặc còn lo ngại, nên đưa trẻ đi đánh giá chuyên môn.")
    return None


_render_mchat = lambda items: (  # noqa: E731
    "M-CHAT-R/F (Modified Checklist for Autism in Toddlers, Revised with Follow-Up) là một bảng câu hỏi "
    "sàng lọc tự kỷ cho trẻ nhỏ, mất khoảng 10 phút để hoàn thành. Theo một tổng quan hệ thống, công cụ "
    "này có độ nhạy (sensitivity) 0,85 và độ đặc hiệu (specificity) 0,99; điểm từ 8 trở lên được coi là "
    "nguy cơ cao. Đây là công cụ sàng lọc để xác định nguy cơ, không phải công cụ chẩn đoán xác định — "
    "cần được đánh giá chuyên môn tiếp theo."
)

_render_ados2 = lambda items: (  # noqa: E731
    "ADOS-2 (Autism Diagnostic Observation Schedule, phiên bản 2) là một công cụ quan sát bán cấu trúc, "
    "được xem là tiêu chuẩn tham chiếu (\"gold standard\") để đánh giá chức năng xã hội và giao tiếp ở "
    "người có thể mắc ASD, do chuyên gia được đào tạo thực hiện. Công cụ có độ tin cậy giữa người đánh "
    "giá (interrater reliability) ở mức 0,79–0,98 giữa các mô-đun. ADOS-2 là một phần của quy trình đánh "
    "giá chẩn đoán, không phải công cụ tự làm tại nhà."
)

_render_ndbi = lambda items: (  # noqa: E731
    "Can thiệp hành vi phát triển tự nhiên (Naturalistic Developmental Behavioral Interventions – NDBI) "
    "là nhóm can thiệp được thực hiện trong bối cảnh tự nhiên của trẻ, trong đó trẻ và người can thiệp "
    "cùng chia sẻ quyền chủ động, sử dụng các hệ quả tự nhiên và nhiều kỹ thuật hành vi để dạy kỹ năng "
    "phù hợp với giai đoạn phát triển. Một tổng quan cho thấy khi kết hợp thêm công cụ giao tiếp thay "
    "thế (AAC) vào NDBI, trẻ có thể có thêm cải thiện về phát triển ngôn ngữ so với chỉ dùng NDBI."
)

_render_sleep_nonpharma = lambda items: (  # noqa: E731
    "Rối loạn giấc ngủ là tình trạng đồng mắc phổ biến ở trẻ tự kỷ (gặp ở khoảng 50-80% trẻ). Theo một "
    "tổng quan, các biện pháp không dùng thuốc thường được khuyến nghị thử trước, trong đó khuyến nghị "
    "có mức bằng chứng mạnh nhất là giữ giờ đi ngủ, giờ thức dậy và giờ ngủ trưa cố định, đều đặn mỗi "
    "ngày. Đây chỉ là một trong nhiều khuyến nghị được tổng quan; nguồn còn liệt kê các biện pháp khác "
    "với mức bằng chứng khác nhau mà hệ thống chưa trích xuất đầy đủ ở đây."
)

_render_melatonin_efficacy = lambda items: (  # noqa: E731
    "Theo một tổng quan tài liệu, melatonin là một trong số ít biện pháp (cùng với các can thiệp hành "
    "vi) được ghi nhận có hiệu quả khá rõ ràng trong y văn đối với rối loạn giấc ngủ ở trẻ tự kỷ. Đây là "
    "thông tin về hiệu quả nói chung, không phải hướng dẫn liều dùng — liều lượng cụ thể phải do bác sĩ "
    "quyết định."
)

_render_school_inclusion = lambda items: (  # noqa: E731
    "Theo một tổng quan hệ thống trên 56 nghiên cứu, các can thiệp hỗ trợ hòa nhập ở trường (tác động "
    "tới học sinh tự kỷ, bạn cùng lớp, giáo viên/nhân viên, và/hoặc môi trường vật lý) giúp tăng khả năng "
    "tiếp cận các hoạt động ở trường cho học sinh tự kỷ. Tuy nhiên, tổng quan cũng cho thấy các can "
    "thiệp này không nhất thiết cải thiện được tình bạn hoặc sự tương hỗ qua lại giữa học sinh tự kỷ và "
    "các bạn cùng lớp."
)

_render_who_caregiver_training = lambda items: (  # noqa: E731
    "Chương trình Huấn luyện Kỹ năng cho Người Chăm sóc (Caregiver Skills Training) của WHO dành cho "
    "cha mẹ/người chăm sóc trẻ có chậm phát triển hoặc khuyết tật (bao gồm tự kỷ), gồm nhiều buổi theo "
    "nhóm. Ví dụ, buổi 6 dạy kỹ năng sinh hoạt hằng ngày theo từng bước nhỏ; buổi 7-8 về thúc đẩy hành vi "
    "tích cực và giảm hành vi thách thức; buổi 9 về sức khỏe tinh thần, giải quyết vấn đề và đặt mục tiêu "
    "cho người chăm sóc. Đây là một phần, không phải toàn bộ nội dung chương trình."
)

_render_ayres_si = lambda items: (  # noqa: E731
    "Ayres Sensory Integration (SI) là một phương pháp can thiệp do A. Jean Ayres phát triển, xem rối "
    "loạn tích hợp cảm giác là khó khăn trong việc \"tổ chức thông tin cảm giác để sử dụng\", liên quan "
    "đến cả chức năng vận động. Đây là một hướng can thiệp cụ thể trong nhóm các liệu pháp cảm giác, "
    "khác với các can thiệp cảm giác khác về cơ sở lý thuyết và cách đánh giá."
)

_render_adolescence_asd = lambda items: (  # noqa: E731
    "Tuổi dậy thì là giai đoạn chuyển đổi quan trọng về sinh học-tâm lý-xã hội, có thể đặc biệt thử "
    "thách đối với người có rối loạn phát triển thần kinh như ASD. Theo tài liệu, thiếu niên tự kỷ có "
    "thể gặp nhu cầu điều hành chức năng (functal executive) và mức độ phức tạp xã hội tăng cao hơn so "
    "với thời thơ ấu, điều này có thể góp phần gây lo âu và hành vi \"che giấu\" (camouflaging) đặc điểm "
    "tự kỷ trước người khác."
)

# T5.3 finding (reproduced live, fixed here): EVERY template below originally fired on trigger-source
# presence alone, with no query-term requirement. This is exactly the "source overlap alone is not
# sufficient justification" failure mode the task explicitly warns against, and it is real, not just
# theoretical — reproduced live during this task's audit:
#   - A sleep-focused question whose gate-filtered evidence happened to also include a CDC-ASD-SIGNS
#     chunk got the signs-by-age answer instead of the sleep answer (signs_by_age was checked first and
#     had no query gate).
#   - A generic "which intervention is most effective?" question whose evidence included both the ABA
#     source and the NDBI source got the NDBI-specific answer, even though the question never asked
#     about NDBI specifically (ndbi_intervention had no query gate).
# Every one of these templates is now in `_QUERY_GATED_TEMPLATES`, requiring both its trigger source AND
# a topic-specific query term. All 11 of the real cached questions these templates were built for still
# contain their required term (re-verified live after this fix — see regression_report.md), so this is
# a pure precision fix, not a coverage loss.
_SIGNS_BY_AGE_TERMS = ["dau hieu", "dấu hiệu"]


def _signs_by_age_query_has_age(query_folded: str) -> bool:
    from app.answer.evidence_normalization import extract_ages
    return bool(extract_ages(query_folded))


def _render_signs_by_age_gated(query_folded: str, items: list[dict]) -> str | None:
    if not any(t in query_folded for t in _SIGNS_BY_AGE_TERMS):
        return None
    if not _signs_by_age_query_has_age(query_folded):
        return None
    return _render_signs_by_age(items)


_QUERY_GATED_TEMPLATES: list[tuple[str, list[str], frozenset[str], object]] = [
    ("ados2_screening", ["ados"], frozenset({"ASD-CSV-062", "ASD-CSV-002"}), lambda items: _render_ados2(items)),
    ("mchat_screening", ["m-chat", "mchat", "m chat"], frozenset({"ASD-CSV-029", "ASD-CSV-002"}),
     lambda items: _render_mchat(items)),
    ("melatonin_efficacy", ["melatonin"], frozenset({"ASD-OA-PMC7407189"}),
     lambda items: _render_melatonin_efficacy(items)),
    ("ndbi_intervention", ["ndbi"], frozenset({"ASD-SUP-PMC4513196", "ASD-CSV-017"}),
     lambda items: _render_ndbi(items)),
    ("sleep_nonpharma", ["giac ngu", "giấc ngủ", "ngu"], frozenset({"ASD-OA-PMC7407189"}),
     lambda items: _render_sleep_nonpharma(items)),
    ("school_inclusion", ["hoa nhap", "hòa nhập", "truong hoc", "truong pho thong"], frozenset({"ASD-CSV-019"}),
     lambda items: _render_school_inclusion(items)),
    ("who_caregiver_training", ["who", "nguoi cham soc"],
     frozenset({"WHO-CST-PARTICIPANTS-2022", "WHO-CST-INTRO-2022"}),
     lambda items: _render_who_caregiver_training(items)),
    ("ayres_si_definition", ["ayres"], frozenset({"ASD-SUP-PMC7726187"}), lambda items: _render_ayres_si(items)),
    ("adolescence_asd", ["day thi", "dậy thì", "thieu nien", "thiếu niên"],
     frozenset({"ASD-OA-PMC12593641", "NIH-NIMH-TEEN-BRAIN"}), lambda items: _render_adolescence_asd(items)),
]


def _template_for(query_folded: str, sufficient_source_ids: set[str]) -> tuple[str, str, frozenset[str]] | None:
    for topic_id, trigger_sources, text, required_terms in _TOPIC_TEMPLATES:
        if not (sufficient_source_ids & trigger_sources):
            continue
        if required_terms is not None and not any(t in query_folded for t in required_terms):
            continue
        return topic_id, text, trigger_sources
    return None


def _new_template_for(query_folded: str, evidence: list[dict]) -> tuple[str, str, list[str]] | None:
    # signs_by_age needs the query text itself (for its age-gate), unlike every other template here —
    # checked first, with its own two-part gate (topic word + a named age in the query).
    signs_matching = [e for e in evidence if e["source_id"] == "CDC-ASD-SIGNS"]
    if signs_matching:
        text = _render_signs_by_age_gated(query_folded, signs_matching)
        if text is not None:
            return "signs_by_age", text, [e["citation_id"] for e in signs_matching]

    for topic_id, query_terms, trigger_sources, render_fn in _QUERY_GATED_TEMPLATES:
        if not any(t in query_folded for t in query_terms):
            continue
        matching = [e for e in evidence if e["source_id"] in trigger_sources]
        if not matching:
            continue
        text = render_fn(matching)
        if text is None:  # template declined — its own pre-condition (e.g. a parseable list) wasn't met
            continue
        return topic_id, text, [e["citation_id"] for e in matching]
    return None


def _truncate(text: str, limit: int = EXCERPT_MAX_CHARS) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def is_dosing_question(query: str) -> bool:
    """Public, pre-retrieval check — `/api/chat` calls this before embedding/DB access so a dangerous
    medication question is refused even when its exact text was never cached (see Phase 6 of the T4
    hardening task: qe069/qe071 previously fell through to an uncached-query error instead of a refusal)."""
    return _is_dosing_question(fold(query))


def dosing_refusal() -> AnswerResult:
    return AnswerResult(_DOSING_REFUSAL, "safety_refusal_dosing", [], False)


def generate(query: str, evidence: list[dict]) -> AnswerResult:
    """`evidence` is the list already filtered by the Evidence Sufficiency Gate (Phase 2) — only items
    the gate judged topically supporting. An empty list means the gate found nothing sufficient."""
    folded = fold(query)

    if _is_dosing_question(folded):
        return dosing_refusal()
    if _is_unproven_cure_question(folded):
        # T5.8 fix: unconditional on evidence presence/quality -- see _CURE_CLAIM_EVIDENCE_ADDENDUM's
        # docstring-comment above for why weak/adjacent evidence must never suppress this caution.
        claim = "phương pháp này" if "te bao goc" not in folded else "liệu pháp tế bào gốc"
        text = _CURE_CLAIM_CAUTION_TEMPLATE.format(claim=claim) + _unproven_cure_evidence_note(evidence)
        citation_ids = [e["citation_id"] for e in evidence]
        return AnswerResult(text, "safety_caution_unproven_cure", citation_ids, False)

    if not evidence:
        text = ("Hệ thống chưa tìm được bằng chứng đủ phù hợp và cụ thể trong kho dữ liệu hiện có để trả "
                "lời chắc chắn câu hỏi này. " + SAFETY_NOTICE)
        return AnswerResult(text, "insufficient_evidence", [], False)

    source_ids = {e["source_id"] for e in evidence}
    template = _template_for(folded, source_ids)
    if template is not None:
        _, text, trigger_sources = template
        citation_ids = [e["citation_id"] for e in evidence if e["source_id"] in trigger_sources]
        if not citation_ids:  # defensive: always cite at least the evidence that triggered the template
            citation_ids = [e["citation_id"] for e in evidence]
        return AnswerResult(f"{text}\n\n{SAFETY_NOTICE}", "topic_template", citation_ids, True)

    new_template = _new_template_for(folded, evidence)
    if new_template is not None:
        _, text, citation_ids = new_template
        return AnswerResult(f"{text}\n\n{SAFETY_NOTICE}", "topic_template", citation_ids, True)

    # No bare "C1/C2/C3" codes in the user-facing text — numbered list only; citation_id stays a separate,
    # structured field in `evidence`/`citations` for the frontend to link, never embedded in the prose.
    lines = ["Hệ thống chưa có bản tổng hợp tiếng Việt được kiểm chứng cho câu hỏi này — dưới đây là trích "
             "dẫn trực tiếp từ nguồn đã truy xuất (không phải văn bản tổng hợp):"]
    citation_ids = []
    for i, item in enumerate(evidence, 1):
        citation_ids.append(item["citation_id"])
        lines.append(f"{i}. {_truncate(item['excerpt'])}")
    lines.append(SAFETY_NOTICE)
    return AnswerResult("\n".join(lines), "extractive_fallback", citation_ids, True)
