from app.answer.mock_answer import SAFETY_NOTICE, MockAnswerGenerator


def evidence_item(citation_id="C1", excerpt="Evidence text."):
    return {"citation_id": citation_id, "source_id": "S1", "title": "T", "section": "Sec",
            "page": "1", "char_range": None, "excerpt": excerpt, "rank": 1}


def test_mock_answer_is_labeled_and_carries_safety_notice():
    answer = MockAnswerGenerator().generate("q", [evidence_item()])
    assert answer.mode == "mock"
    assert "[MOCK" in answer.text
    assert SAFETY_NOTICE in answer.text


def test_mock_answer_never_invents_citations_beyond_given_evidence():
    items = [evidence_item("C1"), evidence_item("C2")]
    answer = MockAnswerGenerator().generate("q", items)
    assert answer.citation_ids == ["C1", "C2"]
    assert "C3" not in answer.text


def test_mock_answer_states_insufficient_evidence_explicitly():
    answer = MockAnswerGenerator().generate("q", [])
    assert answer.sufficient_evidence is False
    assert answer.citation_ids == []
    assert "Không tìm thấy đủ bằng chứng" in answer.text
    assert SAFETY_NOTICE in answer.text


def test_mock_answer_truncates_long_excerpts_without_losing_citation():
    long_excerpt = "x" * 1000
    answer = MockAnswerGenerator().generate("q", [evidence_item(excerpt=long_excerpt)])
    assert "C1" in answer.text
    assert len(answer.text) < 1000 + 200  # truncated, not the full 1000-char excerpt verbatim
