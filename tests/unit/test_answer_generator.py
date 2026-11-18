"""Phase 3: non-LLM answer generation. Templates must only fire when their trigger source is actually
present; everything else falls back to an honestly-labeled extractive presentation or an explicit
insufficient-evidence / safety message. Never claims to be an LLM; never prints bare C1/C2/C3 in prose."""

import pytest

from app.answer.answer_generator import MODES, generate


def ev(citation_id="C1", source_id="S1", excerpt="Some excerpt.", **changes):
    item = {"citation_id": citation_id, "source_id": source_id, "title": "T", "section": "Sec",
            "page": None, "char_range": None, "source_url": "u", "excerpt": excerpt, "rank": 1}
    return item | changes


def test_definition_template_fires_and_matches_the_task_example_wording():
    result = generate("Rối loạn phổ tự kỷ là gì?", [ev(source_id="NIH-NIMH-ASD-2025")])
    assert result.mode == "topic_template"
    assert "Autism Spectrum Disorder" in result.text or "ASD" in result.text
    assert "giao tiếp" in result.text and "tương tác xã hội" in result.text
    assert "C1" not in result.text.split("\n\n")[0]  # the templated paragraph itself has no bare citation code


def test_no_template_matches_falls_back_to_labeled_extractive_presentation():
    result = generate("Một câu hỏi không có mẫu nào khớp", [ev(source_id="SOME-OTHER-SOURCE")])
    assert result.mode == "extractive_fallback"
    assert "chưa có bản tổng hợp" in result.text
    assert "1." in result.text  # numbered, not "C1"
    assert "C1" not in result.text


def test_empty_evidence_states_insufficient_evidence_explicitly():
    result = generate("Trẻ tự kỷ có hay bị động kinh không?", [])
    assert result.mode == "insufficient_evidence"
    assert result.sufficient_evidence is False
    assert result.citation_ids == []
    assert "chưa tìm được bằng chứng" in result.text or "chưa đủ" in result.text.lower()


def test_dosing_question_is_refused_regardless_of_evidence_quality():
    result = generate("Liều risperidone cho trẻ 5 tuổi là bao nhiêu?", [ev()])
    assert result.mode == "safety_refusal_dosing"
    assert result.citation_ids == []
    assert "risperidone" in result.text.lower()
    assert "bác sĩ" in result.text


@pytest.mark.parametrize("query", [
    "Tôi nên tự tăng liều thuốc cho con nếu thấy chưa đỡ không?",
    "Có thể ngừng thuốc tâm thần cho con mà không hỏi bác sĩ không?",
    "Melatonin liều bao nhiêu mg là an toàn cho trẻ 6 tuổi?",
])
def test_self_medication_adjustment_questions_are_refused_even_with_no_drug_named(query):
    # Found live during the Phase 5/6 100-question eval run (qe069, qe071, qe072): these previously fell
    # through to a generic "out of scope" or "not cached" response instead of a safety refusal.
    result = generate(query, [])
    assert result.mode == "safety_refusal_dosing"
    assert result.citation_ids == []


@pytest.mark.parametrize("query", [
    "Tôi có thể tự điều chỉnh liều thuốc cho con không?",  # T5.8 adversarial case B2
    "Con em uống melatonin 10mg mỗi tối có an toàn không?",  # T5.8 case B6
    "Con em đang uống risperidone, em có thể tự đổi sang thuốc khác không cần hỏi bác sĩ không?",  # B9
])
def test_t5_8_self_directed_medication_safety_phrasings_are_refused(query):
    # Found via T5.8 Phase 3's 31-case adversarial sweep: each of these phrasings is just as risky as the
    # already-covered self-adjustment phrasings but used different wording the original term lists did
    # not recognize ("điều chỉnh" instead of "tăng/giảm", a drug-to-drug "chuyển...sang" switch instead of
    # the fixed phrase "đổi thuốc", and a stated mg dose with no word "liều" at all).
    result = generate(query, [])
    assert result.mode == "safety_refusal_dosing"
    assert result.citation_ids == []


def test_clinician_supervised_switch_question_is_not_automatically_refused():
    result = generate("Chuyển từ risperidone sang aripiprazole có cần hỏi bác sĩ không?", [])
    assert result.mode != "safety_refusal_dosing"


def test_t5_8_cure_dut_diem_phrasing_is_cautioned():
    # T5.8 adversarial case A5: "chữa dứt điểm" (a definitive/complete cure) is a distinct phrasing from
    # "chữa khỏi" that _CURE_CLAIM_TERMS did not previously recognize.
    result = generate("Có phương pháp nào chữa dứt điểm tự kỷ chưa ạ?", [])
    assert result.mode == "safety_caution_unproven_cure"


@pytest.mark.parametrize("query", [
    "Risperidone có giúp giảm hành vi hung hăng ở trẻ tự kỷ không?",  # named drug, efficacy question
    "Melatonin có tác dụng phụ gì không?",  # named drug, side-effect question
    "Nguy cơ dùng liều cao vitamin B6 là gì?",  # "liều cao" present, but no named _DRUG_TERMS drug
])
def test_t5_8_ordinary_medication_evidence_questions_are_not_swept_into_dosing_refusal(query):
    # Guards against the T5.8 B6/B9 fixes over-triggering: naming a drug alongside an efficacy or
    # side-effect question (not a dose/switch/adjustment request) must still be answered normally.
    result = generate(query, [])
    assert result.mode != "safety_refusal_dosing"


def test_unproven_cure_claim_with_no_evidence_gets_a_caution_message_not_silence():
    result = generate("Tế bào gốc có chữa được tự kỷ không?", [])
    assert result.mode == "safety_caution_unproven_cure"
    assert "chưa có bằng chứng" in result.text.lower()
    assert result.citation_ids == []


def test_unproven_cure_claim_still_cautions_when_weak_topically_adjacent_evidence_exists():
    # T5.7 finding, fixed in T5.8: the caution used to be conditioned on "and not evidence", so any
    # non-empty evidence list -- even weak, topically-adjacent, substantively irrelevant evidence --
    # silently skipped the caution and fell through to a neutral extractive_fallback. Reproduced live
    # with "Nghe nói uống vitamin B6 liều cao chữa được tự kỷ, có đúng không?": FTS evidence surfaced a
    # sleep-disorder paper mentioning B6 as a supplement ingredient, which is NOT evidence B6 cures
    # autism, yet the caution was skipped. Minimal fix: the caution now fires unconditionally whenever
    # the query is recognized as an unproven-cure claim, regardless of evidence presence/quality.
    weak_evidence = [ev(source_id="ASD-OA-PMC7407189", excerpt="A solution containing melatonin, Trp and "
                         "vitamin B6 proved effective in reducing the number of tests repeated due to "
                         "awakening of the child.")]
    result = generate("Nghe nói uống vitamin B6 liều cao chữa được tự kỷ, có đúng không?", weak_evidence)
    assert result.mode == "safety_caution_unproven_cure"
    assert "chưa có bằng chứng" in result.text.lower()
    assert "chữa khỏi" in result.text.lower()
    # the found-but-insufficient evidence is disclosed, not silently cited as if it supported the claim
    assert result.citation_ids == ["C1"]
    assert "không" in result.text.lower() and "xác nhận hiệu quả" in result.text.lower()


def test_unproven_cure_claim_with_no_evidence_has_no_evidence_addendum_text():
    # The addendum sentence (naming how many documents were found) must only appear when evidence
    # actually exists -- otherwise it would falsely imply something was found.
    result = generate("Tế bào gốc có chữa được tự kỷ không?", [])
    assert "tài liệu đề cập" not in result.text.lower()


def test_template_citations_only_include_the_triggering_source_not_unrelated_extra_evidence():
    evidence = [ev("C1", "NIH-NIMH-ASD-2025"), ev("C2", "SOME-UNRELATED-SOURCE")]
    result = generate("Rối loạn phổ tự kỷ là gì?", evidence)
    assert result.mode == "topic_template"
    assert "C2" not in result.citation_ids


def test_all_modes_are_in_the_declared_set():
    for query, evidence in [
        ("Rối loạn phổ tự kỷ là gì?", [ev(source_id="NIH-NIMH-ASD-2025")]),
        ("câu hỏi khác", [ev(source_id="X")]),
        ("câu hỏi khác", []),
        ("Liều risperidone", [ev()]),
    ]:
        assert generate(query, evidence).mode in MODES


# -- T5.2 regression: templates sharing a source must not hijack each other -----------------------------

def test_risk_factors_template_fires_not_the_generic_definition_despite_shared_source():
    # Found live during T5.2: NIH-NIMH-ASD-2025 is cited by both asd_definition and risk_factors; the
    # risk-factors question must get the risk-factors text, not the generic "what is ASD" paragraph.
    result = generate("Những yếu tố nào làm tăng nguy cơ tự kỷ?", [ev(source_id="NIH-NIMH-ASD-2025")])
    assert "nguyên nhân duy nhất" in result.text
    assert "giao tiếp" not in result.text  # that phrase is unique to the definition template


def test_dsm5_template_fires_not_the_generic_definition_despite_shared_source():
    result = generate("Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?", [ev(source_id="CDC-ASD-CLINICAL")])
    assert "DSM-5" in result.text
    assert "khác nhau ở mỗi người" not in result.text  # fragment unique to the definition template


def test_diagnosis_process_template_fires_not_the_generic_definition():
    result = generate("Tự kỷ được chẩn đoán như thế nào?", [ev(source_id="NIH-NIMH-ASD-2025")])
    assert "xét nghiệm y khoa đơn lẻ" in result.text


def test_screening_age_template_fires_not_the_generic_definition():
    result = generate("Nên sàng lọc tự kỷ cho trẻ vào độ tuổi nào?", [ev(source_id="NIH-NIMH-ASD-2025")])
    assert "AAP" in result.text


def test_generic_definition_still_fires_when_no_specific_term_is_present():
    result = generate("Rối loạn phổ tự kỷ là gì?", [ev(source_id="CDC-ASD-CLINICAL")])
    assert "rối loạn phát triển thần kinh" in result.text


# -- T5.2 new templates ------------------------------------------------------------------------------------

def test_ados2_and_mchat_disambiguate_despite_sharing_a_source():
    mchat = generate("M-CHAT-R/F là gì và độ chính xác ra sao?", [ev(source_id="ASD-CSV-002")])
    ados = generate("ADOS-2 là gì?", [ev(source_id="ASD-CSV-002")])
    assert "M-CHAT" in mchat.text and "ADOS" not in mchat.text
    assert "ADOS-2" in ados.text and "M-CHAT" not in ados.text


def test_melatonin_and_general_sleep_template_disambiguate_despite_sharing_a_source():
    sleep = generate("Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?",
                      [ev(source_id="ASD-OA-PMC7407189")])
    mel = generate("Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không?", [ev(source_id="ASD-OA-PMC7407189")])
    assert "melatonin" not in sleep.text.lower()
    assert "melatonin" in mel.text.lower()
    assert "liều lượng cụ thể phải do bác sĩ quyết định" in mel.text  # no dose number ever stated


def test_signs_by_age_template_lists_only_age_tagged_items_and_adds_the_single_sign_caveat():
    excerpt = ("Examples can include * Avoids eye contact * Does not respond to name by 9 months of "
               "age * Does not point by 18 months of age")
    result = generate("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?",
                       [ev(source_id="CDC-ASD-SIGNS", excerpt=excerpt)])
    assert "9 months" in result.text and "18 months" in result.text
    assert "Avoids eye contact" not in result.text  # no age tag -> not included
    assert "Một dấu hiệu đơn lẻ không đủ để kết luận" in result.text


def test_signs_by_age_declines_and_falls_back_when_the_excerpt_has_no_age_tagged_items():
    excerpt = "Social communication is challenging for people with ASD in general."
    result = generate("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?",
                       [ev(source_id="CDC-ASD-SIGNS", excerpt=excerpt)])
    assert result.mode == "extractive_fallback"  # template declined, no guessed content


def test_ndbi_school_inclusion_who_caregiver_ayres_si_and_adolescence_templates_fire():
    cases = [
        ("Can thiệp NDBI là gì?", "ASD-SUP-PMC4513196", "NDBI"),
        ("Làm sao hỗ trợ trẻ tự kỷ hòa nhập ở trường phổ thông?", "ASD-CSV-019", "hòa nhập"),
        ("Chương trình huấn luyện kỹ năng cho người chăm sóc của WHO gồm những gì?",
         "WHO-CST-PARTICIPANTS-2022", "WHO"),
        ("Ayres Sensory Integration khác các can thiệp cảm giác khác thế nào?",
         "ASD-SUP-PMC7726187", "Ayres"),
        ("Tự kỷ ở tuổi dậy thì có những thách thức gì?", "ASD-OA-PMC12593641", "dậy thì"),
    ]
    for query, source_id, expected_fragment in cases:
        result = generate(query, [ev(source_id=source_id)])
        assert result.mode == "topic_template", query
        assert expected_fragment in result.text, query
