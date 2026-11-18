"""Real FastAPI + research-reader smoke test for the demo chat endpoint, after Phases 1-4 repair."""

import pytest
from fastapi.testclient import TestClient

from app.api import create_app

pytestmark = pytest.mark.integration


def test_cached_definition_question_returns_the_grounded_template_answer_with_source_links():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Rối loạn phổ tự kỷ là gì?", "top_k": 5,
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "ok" and body["retrieval_status"] == "ok"
    assert body["answer_mode"] == "topic_template"
    assert "C1" not in body["answer"].split("\n\n")[0]
    assert "giao tiếp" in body["answer"] and "tương tác xã hội" in body["answer"]
    assert body["evidence"], "the definition template must still cite at least one real source"
    assert all(e["source_id"] and e["excerpt"] and e["source_url"] for e in body["evidence"])
    assert [c["citation_id"] for c in body["citations"]] == [e["citation_id"] for e in body["evidence"]]
    assert all(c["source_url"] for c in body["citations"])


def test_vaccine_safety_question_finds_the_real_debunking_evidence():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Vắc-xin có gây tự kỷ không?", "top_k": 5,
    })
    body = response.json()
    assert body["retrieval_status"] == "ok"
    assert body["answer_mode"] == "topic_template"
    assert "retracted" in body["answer"].lower() or "rút lại" in body["answer"].lower()


def test_risperidone_dosing_question_is_refused_not_answered_with_retrieved_text():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?", "top_k": 5,
    })
    body = response.json()
    assert body["answer_mode"] == "safety_refusal_dosing"
    assert body["evidence"] == []


def test_weather_question_never_reaches_retrieval_or_gets_asd_evidence():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Hôm nay thời tiết thế nào?", "top_k": 5,
    })
    body = response.json()
    assert body["retrieval_status"] == "out_of_scope"
    assert body["evidence"] == []


def test_greeting_never_touches_the_database():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Xin chào, bạn có thể giúp gì cho tôi?", "top_k": 5,
    })
    body = response.json()
    assert body["retrieval_status"] == "skipped_greeting"


def test_uncached_asd_question_returns_503_query_not_cached():
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Tự kỷ ảnh hưởng đến khả năng tập trung của trẻ như thế nào trong lớp học bán trú?",
        "top_k": 5,
    })
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "QUERY_NOT_CACHED"


def test_new_t5_2_template_examples_get_real_vietnamese_answers_with_valid_citations():
    client = TestClient(create_app())
    cases = [
        ("Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?", "9 months"),
        ("M-CHAT-R/F là gì và độ chính xác ra sao?", "0,85"),
        ("ADOS-2 là gì?", "ADOS-2"),
        ("Can thiệp NDBI là gì?", "NDBI"),
        ("Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?", "giấc ngủ"),
        ("Melatonin có giúp trẻ tự kỷ ngủ tốt hơn không?", "melatonin"),
    ]
    for query, expected_fragment in cases:
        response = client.post("/api/chat", json={"query": query, "top_k": 5})
        body = response.json()
        assert body["answer_mode"] == "topic_template", query
        assert expected_fragment.lower() in body["answer"].lower(), query
        assert body["evidence"], query
        assert all(e["source_url"] for e in body["evidence"]), query
        assert [c["citation_id"] for c in body["citations"]] == [e["citation_id"] for e in body["evidence"]]


def test_q033_adhd_confusion_is_still_present_and_unfixed_in_this_task():
    # Documents, live, that this known limitation remains open per the T5.2 task's explicit instruction
    # not to change the Evidence Gate for it.
    response = TestClient(create_app()).post("/api/chat", json={
        "query": "Can thiệp do cha mẹ thực hiện có hiệu quả không?", "top_k": 5,
    })
    body = response.json()
    assert any(e["source_id"] == "NIH-NIMH-ADHD" for e in body["evidence"])
