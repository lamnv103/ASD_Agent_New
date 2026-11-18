"""T5.2 Phase F: negative tests using queries and source combinations NOT among the 18 questions used to
build the new templates — per the task's explicit instruction not to use the same 18 questions to claim
generalization. These check that a template never fires just because a keyword appears somewhere, or
just because a source appears somewhere, without both the right source AND (where required) the right
query wording together."""

from app.answer.answer_generator import generate


def ev(citation_id="C1", source_id="S1", excerpt="Some excerpt.", **changes):
    item = {"citation_id": citation_id, "source_id": source_id, "title": "T", "section": "Sec",
            "page": None, "char_range": None, "source_url": "u", "excerpt": excerpt, "rank": 1}
    return item | changes


def test_mentioning_ados_with_the_wrong_source_does_not_fire_the_ados_template():
    # A question that happens to mention "ADOS" but whose actual evidence is from an unrelated source.
    result = generate("So sánh ADOS với các công cụ quan sát hành vi khác trong nghiên cứu này",
                       [ev(source_id="ASD-CSV-091")])
    assert "gold standard" not in result.text and "Autism Diagnostic Observation Schedule" not in result.text


def test_mentioning_melatonin_with_an_unrelated_source_does_not_fire_the_melatonin_template():
    result = generate("Con tôi nhắc đến từ melatonin trên quảng cáo TV, đó là gì?",
                       [ev(source_id="CDC-ASD-SIGNS")])
    assert "liều lượng cụ thể phải do bác sĩ quyết định" not in result.text


def test_t5_3_fix_vague_question_with_the_ndbi_source_present_but_no_ndbi_wording_now_declines():
    # T5.3 found this was a real bug: before this fix, NDBI's template fired on source presence alone,
    # so a vague question whose evidence merely included the NDBI source got an NDBI-specific answer it
    # never asked for. Now requires the query to actually say "NDBI" — correctly declines here.
    result = generate("Cái này là phương pháp gì vậy?", [ev(source_id="ASD-SUP-PMC4513196")])
    assert result.mode == "extractive_fallback"


def test_who_caregiver_training_does_not_fire_for_an_unrelated_caregiver_source():
    result = generate("Người chăm sóc cần làm gì khi mệt mỏi?", [ev(source_id="SOME-OTHER-CAREGIVER-DOC")])
    assert result.mode != "topic_template"


def test_t5_3_fix_signs_by_age_declines_for_a_vague_question_even_with_age_tagged_evidence_present():
    # T5.3 found this was a real bug: a sleep-focused question whose gate-filtered evidence happened to
    # also include a CDC-ASD-SIGNS chunk got the signs-by-age answer instead of answering the real
    # question, because signs_by_age had no query-side gate. Now requires the query to mention "dấu
    # hiệu" AND a specific age — a vague, topic-less question correctly declines and falls back.
    excerpt = ("Signs include * Does not respond to name by 9 months of age "
               "* Does not point by 18 months of age")
    result = generate("Con tôi thế nào rồi?", [ev(source_id="CDC-ASD-SIGNS", excerpt=excerpt)])
    assert result.mode == "extractive_fallback"


def test_ayres_si_template_does_not_fire_for_a_different_sensory_source():
    result = generate("Liệu pháp cảm giác nào tốt nhất?", [ev(source_id="NIHR-SENITA-2022")])
    assert "A. Jean Ayres" not in result.text


def test_adolescence_template_does_not_fire_for_a_childhood_development_source():
    result = generate("Trẻ nhỏ phát triển thế nào?", [ev(source_id="CDC-MILESTONES-18")])
    assert "camouflaging" not in result.text


def test_school_inclusion_does_not_fire_for_a_generic_education_source():
    result = generate("Giáo dục đặc biệt là gì?", [ev(source_id="SOME-OTHER-EDU-SOURCE")])
    assert result.mode != "topic_template"


def test_new_templates_fire_the_same_with_or_without_diacritics_in_the_query():
    with_diacritics = generate("ADOS-2 là gì?", [ev(source_id="ASD-CSV-062")])
    without_diacritics = generate("ADOS-2 la gi?", [ev(source_id="ASD-CSV-062")])
    assert with_diacritics.mode == without_diacritics.mode == "topic_template"
    assert with_diacritics.text == without_diacritics.text


def test_melatonin_template_fires_regardless_of_diacritics():
    with_diacritics = generate("Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không?",
                                [ev(source_id="ASD-OA-PMC7407189")])
    without_diacritics = generate("Melatonin co giup tre tu ky ngu tot hon khong?",
                                   [ev(source_id="ASD-OA-PMC7407189")])
    assert with_diacritics.mode == without_diacritics.mode == "topic_template"
    assert "melatonin" in with_diacritics.text.lower() and "melatonin" in without_diacritics.text.lower()


# -- T5.3 regression: cross-topic co-occurrence must not let an ungated template hijack the answer -------

def test_sleep_question_with_a_co_occurring_signs_chunk_gets_the_sleep_answer_not_signs_by_age():
    signs_excerpt = ("Examples can include * Does not respond to name by 9 months of age "
                     "* Does not point by 18 months of age")
    sleep_excerpt = "Sleep disturbances are common in children with ASD, affecting 50-80 percent."
    evidence = [
        ev("C1", "CDC-ASD-SIGNS", signs_excerpt),
        ev("C2", "ASD-OA-PMC7407189", sleep_excerpt),
    ]
    result = generate("Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?", evidence)
    assert result.mode == "topic_template"
    assert "giấc ngủ" in result.text or "ngủ" in result.text.lower()
    assert "9 months" not in result.text


def test_generic_intervention_question_with_a_co_occurring_ndbi_source_gets_the_aba_answer_not_ndbi():
    aba_excerpt = "Behavioral approaches have the most evidence for treating ASD symptoms."
    ndbi_excerpt = "NDBI are implemented in natural settings with shared control."
    evidence = [
        ev("C1", "CDC-ASD-TREATMENT", aba_excerpt),
        ev("C2", "ASD-SUP-PMC4513196", ndbi_excerpt),
    ]
    result = generate("Can thiệp hành vi (ABA) nào cho trẻ tự kỷ hiệu quả nhất?", evidence)
    assert result.mode == "topic_template"
    assert "Applied Behavior Analysis" in result.text
    assert "NDBI" not in result.text


def test_generic_intervention_question_with_no_specific_term_at_all_falls_back_honestly():
    aba_excerpt = "Behavioral approaches have the most evidence for treating ASD symptoms."
    ndbi_excerpt = "NDBI are implemented in natural settings with shared control."
    evidence = [
        ev("C1", "CDC-ASD-TREATMENT", aba_excerpt),
        ev("C2", "ASD-SUP-PMC4513196", ndbi_excerpt),
    ]
    # No "ABA"/"hành vi"/"NDBI" wording at all -> neither template should claim this question.
    result = generate("Can thiệp nào cho trẻ tự kỷ hiệu quả nhất?", evidence)
    assert result.mode == "extractive_fallback"
