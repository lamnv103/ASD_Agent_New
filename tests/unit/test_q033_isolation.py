"""T5.2 Phase E — q033 (ADHD/ASD confusion) isolation tests.

Characterizes current Evidence Gate behavior on four scenarios, WITHOUT changing
`app/retrieval/evidence_gate.py` (forbidden by the T5.2 task brief for this phase). These are
false-positive/false-negative documentation tests, not a fix — see
`reports/t5_2_template_expansion/remaining_limitations.md` for the decision this is meant to inform.
"""

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


ASD_PARENT_QUERY = "Can thiệp do cha mẹ thực hiện có hiệu quả không?"


def test_asd_parent_intervention_direct_asd_evidence_is_accepted():
    """The clean positive case: evidence is genuinely about ASD parent-delivered intervention."""
    c = chunk(title="Parenting interventions to promote early child development",
              section="Results > Parent-delivered intervention for autism spectrum disorder",
              content="Parent-delivered intervention for children with autism spectrum disorder showed "
                      "measurable gains in social communication skills.")
    a = assess(ASD_PARENT_QUERY, [c])
    assert a.sufficient and a.details[0].support_type == "direct"


def test_adhd_parent_education_false_positive_is_reproduced_and_documented():
    """THE q033 BUG, reproduced exactly from the live chunk's real title/section (not invented): the
    section heading literally contains "parent", which is the query's only specific term, with no ASD
    anchor anywhere in the chunk. Evidence Gate currently accepts this as `direct` support — a known,
    documented false positive, NOT fixed here per the task's explicit instruction not to touch the gate
    in this phase."""
    c = chunk(title="Attention-Deficit/Hyperactivity Disorder: What You Need to Know",
              section="How is ADHD treated? > Parent education and support",
              content="Mental health professionals can educate parents about the disorder and how it "
                      "affects a family... parenting skills training, stress management techniques for "
                      "parents, and support groups.")
    a = assess(ASD_PARENT_QUERY, [c])
    assert a.sufficient  # reproduces the bug
    assert a.details[0].support_type == "direct"  # the strongest label, not even "indirect"
    assert "autism" not in c.content.lower() and "asd" not in c.content.lower()  # confirms: no ASD anchor anywhere


def test_asd_plus_adhd_comorbidity_evidence_is_legitimately_relevant_not_a_false_positive():
    """The trade-off case named in `q033_context_analysis.md`: a chunk that legitimately discusses ADHD
    IN THE CONTEXT of ASD comorbidity must stay accepted — a blanket "reject anything ADHD-labeled" rule
    would create a new false negative here."""
    comorbid_query = "Trẻ tự kỷ kèm ADHD lại hay mất ngủ thì hỗ trợ thế nào?"
    c = chunk(title="Attention-Deficit/Hyperactivity Disorder: What You Need to Know",
              section="How is ADHD treated? > Parent education and support",
              content="For children with co-occurring autism spectrum disorder (ASD) and ADHD, parent "
                      "education addressing both conditions together is recommended.")
    a = assess(comorbid_query, [c])
    assert a.sufficient  # correctly relevant — "mat ngu"/"ho tro" aren't glossary terms here, but the
    # comorbidity question's only specific term is still "cha me"-adjacent support context; what matters
    # for this test is only that comorbid ASD+ADHD content is not blanket-excluded by content inspection


def test_parent_question_with_no_asd_context_at_all_is_routed_as_low_confidence_not_rejected():
    """A related finding, not the main q033 bug but worth recording alongside it: a purely generic
    parenting question with NO ASD content at all ("how can I be a better parent?") still routes to
    `asd_question` (not `out_of_scope`) because "cha mẹ"/"parent" alone is a glossary term (Phase 1's
    design: any glossary term triggers low-confidence `asd_question`, never outright rejection). This
    query would then reach the Evidence Gate exactly like the real q033 case — i.e. this is the same
    root cause (a generic word used as the query's only specific term) showing up one layer earlier."""
    from app.router.classifier import classify
    result = classify("Làm sao để làm cha mẹ tốt hơn?")  # "how to be a better parent" — no ASD content
    assert result.branch == "asd_question" and result.confidence == "low"


def test_mitigation_option_require_asd_anchor_in_chunk_would_fix_the_false_positive():
    """Documents (does not implement) the lexical mitigation from `q033_context_analysis.md`: requiring
    the ASD anchor phrase somewhere in the chunk text would correctly reject the ADHD false positive
    while still accepting the genuine ASD-parent-intervention case — characterized here with a plain
    substring check, not wired into the Evidence Gate."""
    from app.nlp.text_match import ASD_ANCHOR_PHRASES, contains_any, fold

    adhd_chunk_text = ("Mental health professionals can educate parents about the disorder and how it "
                       "affects a family... parenting skills training, stress management.")
    asd_chunk_text = ("Parent-delivered intervention for children with autism spectrum disorder showed "
                      "measurable gains in social communication skills.")
    assert not contains_any(fold(adhd_chunk_text), ASD_ANCHOR_PHRASES)  # would be correctly rejected
    assert contains_any(fold(asd_chunk_text), ASD_ANCHOR_PHRASES)  # would be correctly kept
