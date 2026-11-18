"""Phase 1: intent routing. Covers the edge cases the task brief explicitly requires."""

import pytest

from app.router.classifier import classify


@pytest.mark.parametrize("query", ["Xin chào!", "Chào bạn", "Hello", "Hi there"])
def test_pure_greeting_routes_to_greeting(query):
    assert classify(query).branch == "greeting"


@pytest.mark.parametrize("query", ["Cảm ơn bạn nhiều!", "Thank you so much"])
def test_thanks_routes_to_greeting(query):
    r = classify(query)
    assert r.branch == "greeting" and r.greeting_kind == "thanks"


@pytest.mark.parametrize("query", ["Tạm biệt nhé", "Goodbye"])
def test_farewell_routes_to_greeting(query):
    r = classify(query)
    assert r.branch == "greeting" and r.greeting_kind == "farewell"


@pytest.mark.parametrize("query", [
    "Hôm nay thời tiết thế nào?", "Giá vàng hôm nay là bao nhiêu?", "Bạn thích ăn món gì?",
])
def test_unrelated_topics_route_to_out_of_scope(query):
    assert classify(query).branch == "out_of_scope"


def test_empty_message_routes_to_out_of_scope():
    assert classify("").branch == "out_of_scope"
    assert classify("   ").branch == "out_of_scope"


@pytest.mark.parametrize("query", [
    "Rối loạn phổ tự kỷ là gì?",
    "What is autism spectrum disorder?",
    "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?",
    "Liều risperidone cho trẻ 5 tuổi là bao nhiêu?",  # no literal "tự kỷ"/"autism", but a clinical/ASD-adjacent term
    "Tieu chuan DSM-5 cho tu ky gom nhung gi?",  # no diacritics at all
    "Con tôi 3 tuổi hay xếp đồ thành hàng, có phải bị asd không ạ?",  # typo-tolerant-ish, mixed case
])
def test_asd_related_questions_route_to_asd_question(query):
    assert classify(query).branch == "asd_question"


def test_mixed_intent_greeting_and_asd_question_prefers_the_real_question():
    r = classify("Chào bạn, tự kỷ là gì?")
    assert r.branch == "asd_question"


def test_long_multi_clause_question_routes_to_asd_question():
    q = ("Con tôi 2 tuổi chưa nói, không chỉ tay, hay xếp đồ thành hàng, và gần đây hay thoái lui kỹ năng "
         "đã có — liệu đây có phải dấu hiệu của rối loạn phổ tự kỷ không, và tôi nên làm gì tiếp theo?")
    assert classify(q).branch == "asd_question"


def test_short_single_word_asd_term_routes_to_asd_question():
    assert classify("ASD?").branch == "asd_question"
