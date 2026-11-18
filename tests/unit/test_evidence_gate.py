"""Phase 2: Evidence Sufficiency Gate. Built from the four confirmed failure cases in the independent
expert evaluation (vaccine, risperidone dosing, stem cells, epilepsy) plus the q062 "weather" case and
the generic-definition case that must still pass."""

from dataclasses import replace

from app.retrieval.evidence_gate import assess
from app.retrieval.types import RetrievedChunk

BASE = RetrievedChunk(
    rank=1, chunk_id="c1", source_id="S1", document_id="D1", title="T", source_url="u", content="",
    content_sha256="h", section="Sec", page=None, char_range=None, score_type="cosine_distance",
    score=0.5, cosine_similarity=0.5, authorization_version=1, embedding_profile="p", model_id="m",
    corpus_version="v1",
)


def chunk(**changes) -> RetrievedChunk:
    return replace(BASE, **changes)


def test_generic_definition_question_is_sufficient_from_similarity_alone():
    results = [chunk(content="Autism spectrum disorder is a developmental disorder affecting communication.")]
    a = assess("Rối loạn phổ tự kỷ là gì?", results)
    assert a.sufficient and len(a.supported) == 1


def test_vaccine_question_rejects_evidence_with_no_vaccine_mention():
    results = [chunk(content="Autism is a lifelong neurodevelopmental condition.", title="Autism overview")]
    a = assess("Vắc-xin có gây tự kỷ không?", results)
    assert not a.sufficient and a.reason == "no_topic_specific_evidence"


def test_vaccine_question_accepts_evidence_that_actually_discusses_vaccination():
    results = [chunk(content="The alleged link between routine childhood vaccination and autism came from "
                              "a now-retracted study.")]
    a = assess("Vắc-xin có gây tự kỷ không?", results)
    assert a.sufficient and len(a.supported) == 1


def test_risperidone_dosing_question_rejects_unrelated_sleep_medication_evidence():
    results = [chunk(content="Melatonin dosing for sleep-onset insomnia in children is typically 1-3mg.")]
    a = assess("Liều risperidone cho trẻ 5 tuổi là bao nhiêu?", results)
    assert not a.sufficient


def test_stem_cell_question_rejects_unrelated_genetic_evidence():
    results = [chunk(content="A genetic workup should be performed to identify a possible genetic cause.")]
    a = assess("Tế bào gốc có chữa được tự kỷ không?", results)
    assert not a.sufficient


def test_epilepsy_question_rejects_anxiety_and_adhd_comorbidity_evidence():
    results = [chunk(content="Anxiety disorders and ADHD are common psychiatric comorbidities in ASD.")]
    a = assess("Trẻ tự kỷ có hay bị động kinh không?", results)
    assert not a.sufficient


def test_epilepsy_question_accepts_evidence_that_mentions_seizures():
    results = [chunk(content="Seizure disorders are more prevalent in autistic children than in the "
                              "general pediatric population.")]
    a = assess("Trẻ tự kỷ có hay bị động kinh không?", results)
    assert a.sufficient


def test_title_and_section_signal_counts_even_when_body_excerpt_does_not_repeat_the_word():
    # Regression for a real bug found during this task: "CDC-ASD-SIGNS" / "Signs and Symptoms of ASD" is
    # the right source for an early-signs question, but its excerpt body may not literally repeat "sign".
    results = [chunk(title="Signs and Symptoms of Autism Spectrum Disorder", section="Signs and symptoms",
                      content="Avoids or does not keep eye contact. Does not respond to name by 9 months.")]
    a = assess("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?", results)
    assert a.sufficient


def test_no_results_is_insufficient():
    a = assess("Bất kỳ câu hỏi nào", [])
    assert not a.sufficient and a.reason == "no_results"


def test_below_similarity_floor_is_insufficient_even_for_a_generic_question():
    results = [chunk(cosine_similarity=0.01, content="Autism spectrum disorder overview.")]
    a = assess("Rối loạn phổ tự kỷ là gì?", results)
    assert not a.sufficient and a.reason == "below_similarity_floor"


def test_mixed_results_keep_only_the_supporting_ones():
    good = chunk(content="Routine vaccination has no established link to autism; the original claim came "
                          "from a retracted study.")
    bad = chunk(content="Autism community stigma varies across cultures.", rank=2)
    a = assess("Vắc-xin có gây tự kỷ không?", [good, bad])
    assert a.sufficient and a.supported == [good] and a.unsupported_dropped == 1


def test_direct_support_when_the_specific_term_is_in_the_title_or_section():
    results = [chunk(title="Vaccine Safety and Autism", section="Overview",
                      content="There is no causal link established.")]
    a = assess("Vắc-xin có gây tự kỷ không?", results)
    assert a.sufficient and a.details[0].support_type == "direct"


def test_indirect_support_when_the_specific_term_is_only_in_the_body():
    results = [chunk(title="General health topics", section="Misc",
                      content="Routine vaccination has no established link to autism.")]
    a = assess("Vắc-xin có gây tự kỷ không?", results)
    assert a.sufficient and a.details[0].support_type == "indirect"


def test_generic_support_type_for_a_question_with_no_specific_term():
    results = [chunk(content="Autism spectrum disorder overview.")]
    a = assess("Rối loạn phổ tự kỷ là gì?", results)
    assert a.sufficient and a.details[0].support_type == "generic"


def test_age_mismatch_flagged_when_query_names_an_age_the_chunk_does_not_mention():
    results = [chunk(title="Signs and Symptoms of Autism Spectrum Disorder",
                      content="Signs and symptoms of autism can appear in early childhood.")]
    a = assess("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?", results)
    assert a.sufficient and a.details[0].age_mismatch is True


def test_age_mismatch_false_when_the_chunk_actually_mentions_the_same_age():
    results = [chunk(title="Signs and Symptoms of Autism Spectrum Disorder",
                      content="Does not point to show you something interesting by 18 months of age.")]
    a = assess("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?", results)
    assert a.sufficient and a.details[0].age_mismatch is False


def test_age_mismatch_is_false_when_the_query_names_no_age_at_all():
    results = [chunk(content="Autism spectrum disorder overview.")]
    a = assess("Rối loạn phổ tự kỷ là gì?", results)
    assert a.details[0].age_mismatch is False
