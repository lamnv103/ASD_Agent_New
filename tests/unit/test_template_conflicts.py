"""T5.3 Phase 3 — the 8 template-conflict categories named in the task brief, each as its own named
test for direct traceability. Several of these reproduce bugs found and fixed during T5.2/T5.3; the
assertions check the FIXED (current, correct) behavior and the comments say what used to happen."""

from app.answer.answer_generator import generate


def ev(citation_id="C1", source_id="S1", excerpt="Some excerpt.", **changes):
    item = {"citation_id": citation_id, "source_id": source_id, "title": "T", "section": "Sec",
            "page": None, "char_range": None, "source_url": "u", "excerpt": excerpt, "rank": 1}
    return item | changes


def test_1_dsm5_vs_asd_definition():
    # Pre-existing bug, fixed in T5.2: asd_definition used to hijack this whenever CDC-ASD-CLINICAL
    # (shared by both templates) was present, because it was checked first with no query gate.
    result = generate("Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?", [ev(source_id="CDC-ASD-CLINICAL")])
    assert "DSM-5" in result.text
    assert "khác nhau ở mỗi người" not in result.text  # the asd_definition-only fragment


def test_2_ados2_vs_mchat():
    # Bug found and fixed within T5.2: both share ASD-CSV-002.
    ados = generate("ADOS-2 là gì?", [ev(source_id="ASD-CSV-002")])
    mchat = generate("M-CHAT-R/F là gì?", [ev(source_id="ASD-CSV-002")])
    assert "ADOS-2" in ados.text and "M-CHAT" not in ados.text
    assert "M-CHAT" in mchat.text and "ADOS-2" not in mchat.text


def test_3_sleep_vs_developmental_signs():
    # Bug found and fixed in T5.3: signs_by_age had no query gate, so a sleep question whose
    # gate-filtered evidence happened to include a CDC-ASD-SIGNS chunk got the wrong answer.
    evidence = [
        ev("C1", "CDC-ASD-SIGNS", "Signs include * Does not respond to name by 9 months of age "
                                  "* Does not point by 18 months of age"),
        ev("C2", "ASD-OA-PMC7407189", "Sleep disturbances are common in children with ASD."),
    ]
    result = generate("Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?", evidence)
    assert result.mode == "topic_template"
    assert "9 months" not in result.text


def test_4_asd_vs_adhd_parent_education():
    # The still-open q033 limitation (NOT fixed in T5.3, by instruction) — see special_case_review.md.
    # This test documents the current, unfixed state so a future change is visible as a diff here.
    from app.retrieval.evidence_gate import assess
    from app.retrieval.types import RetrievedChunk

    base = RetrievedChunk(rank=1, chunk_id="c1", source_id="NIH-NIMH-ADHD", document_id="D1",
                          title="Attention-Deficit/Hyperactivity Disorder: What You Need to Know",
                          source_url="u", content="Mental health professionals can educate parents "
                          "about the disorder and how it affects a family.",
                          content_sha256="h", section="How is ADHD treated? > Parent education and support",
                          page=None, char_range=None, score_type="cosine_distance", score=0.5,
                          cosine_similarity=0.5, authorization_version=1, embedding_profile="p",
                          model_id="m", corpus_version="v1")
    a = assess("Can thiệp do cha mẹ thực hiện có hiệu quả không?", [base])
    assert a.sufficient  # reproduces the known, documented, unfixed false positive


def test_5_multiple_templates_sharing_one_source():
    # NIH-NIMH-ASD-2025 is shared by 4 templates (risk_factors, screening_age, diagnosis_process,
    # asd_definition) — each of the 3 specific ones must win over the generic catch-all.
    cases = [
        ("Những yếu tố nào làm tăng nguy cơ tự kỷ?", "nguyên nhân duy nhất"),
        ("Nên sàng lọc tự kỷ cho trẻ vào độ tuổi nào?", "AAP"),
        ("Tự kỷ được chẩn đoán như thế nào?", "xét nghiệm y khoa đơn lẻ"),
    ]
    for query, expected_fragment in cases:
        result = generate(query, [ev(source_id="NIH-NIMH-ASD-2025")])
        assert expected_fragment in result.text, query


def test_6_generic_template_vs_specific_template():
    result = generate("Rối loạn phổ tự kỷ là gì?", [ev(source_id="CDC-ASD-CLINICAL")])
    assert "rối loạn phát triển thần kinh" in result.text  # generic wins only when nothing specific matches


def test_7_multi_intent_question():
    # A question naming two topics at once resolves deterministically to the first-priority match
    # (risk_factors before diagnosis_process) rather than arbitrarily/randomly — documented, not fixed
    # to pick "the right one" since there is no reliable way to know which the user meant more.
    result = generate("Những yếu tố nguy cơ nào liên quan đến chẩn đoán sớm tự kỷ?",
                      [ev(source_id="NIH-NIMH-ASD-2025")])
    assert "nguyên nhân duy nhất" in result.text  # risk_factors, checked first


def test_8_template_candidate_with_insufficient_evidence_never_reaches_the_template_at_all():
    # A template's trigger source can only reach `generate()` via evidence already filtered by the
    # Evidence Sufficiency Gate. If the gate found nothing sufficient, `generate()` is called with an
    # empty evidence list — no template can ever fire, regardless of what the question was "about."
    result = generate("Tiêu chuẩn DSM-5 cho tự kỷ gồm những gì?", [])
    assert result.mode == "insufficient_evidence"
    assert result.citation_ids == []
