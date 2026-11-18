"""Validator for the retrieval evaluation dataset: each rule has a positive and a negative case."""

import importlib.util
import json

import pytest

from app.config import ROOT

_spec = importlib.util.spec_from_file_location("validate_retrieval_eval",
                                               ROOT / "scripts" / "validate_retrieval_eval.py")
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

SCHEMA = json.loads((ROOT / "eval" / "datasets" / "retrieval_eval_v1_schema.json").read_text(encoding="utf-8"))
SHA = "a" * 64
MANIFEST = {
    "D1#p#0001": {"chunk_id": "D1#p#0001", "document_id": "D1", "source_id": "S1", "content_hash": "1" * 64},
    "D1#p#0002": {"chunk_id": "D1#p#0002", "document_id": "D1", "source_id": "S1", "content_hash": "2" * 64},
    "D2#p#0001": {"chunk_id": "D2#p#0001", "document_id": "D2", "source_id": "S2", "content_hash": "3" * 64},
}


def judgment(cid, grade):
    m = MANIFEST[cid]
    return {"chunk_id": cid, "document_id": m["document_id"], "source_id": m["source_id"],
            "content_sha256": m["content_hash"], "grade": grade,
            "evidence_class": {3: "relevant", 2: "relevant", 1: "partial", 0: "negative", -1: "conflicting"}[grade],
            "aspect": "a", "rationale_vi": "lý do"}


def record(qid="q001", question="Rối loạn phổ tự kỷ là gì?", grades=(("D1#p#0001", 3), ("D2#p#0001", 0)), **kw):
    js = [judgment(c, g) for c, g in grades]
    rel = [j["chunk_id"] for j in js if j["grade"] >= 2]
    base = {
        "dataset_version": "retrieval_eval_v1", "question_id": qid, "question_vi": question,
        "reference_query_en": "What is autism?", "query_category": "basic_knowledge", "query_style": ["short"],
        "query_complexity": "simple", "expected_route": "expert_qa", "answerability": "answerable",
        "expected_evidence_status": "sufficient", "expected_answer_scope": "x",
        "expected_sources": sorted({MANIFEST[c]["source_id"] for c in rel}),
        "relevant_document_ids": sorted({MANIFEST[c]["document_id"] for c in rel}),
        "relevant_chunk_ids": rel, "relevance_grade": {j["chunk_id"]: j["grade"] for j in js}, "judgments": js,
        "candidate_chunk_ids": [], "evidence_requirements": ["định nghĩa"], "requires_multiple_chunks": False,
        "requires_multiple_sources": False, "annotation_status": "annotated_single",
        "label_tier": "silver_single_annotator", "annotation_completeness": "complete_for_judged_pool",
        "annotators": [{"annotator_id": "A1", "annotator_type": "ai_model"}], "annotation_method": "m",
        "search_log": [], "annotation_notes": "", "corpus": {"chunking_profile": "section_v2_1",
        "embedding_profile": "p", "embedding_manifest_sha256": SHA}}
    return base | kw


def run(*records):
    return V.validate([json.dumps(r, ensure_ascii=False) for r in records], SCHEMA, MANIFEST, SHA)


def test_valid_record_passes():
    assert run(record())["ok"]


def test_invalid_json_and_duplicate_ids_fail():
    res = V.validate(["{not json"], SCHEMA, MANIFEST, SHA)
    assert not res["ok"] and "invalid JSON" in res["errors"][0]
    assert any("duplicate question_id" in e for e in run(record(), record(question="Khác hẳn câu kia?"))["errors"])


def test_unknown_chunk_is_rejected():
    r = record()
    r["judgments"][0]["chunk_id"] = "FAKE#p#9999"
    assert any("not in the embedded set" in e for e in run(r)["errors"])


def test_relevant_ids_must_equal_judged_grade_2_plus():
    r = record()
    r["relevant_chunk_ids"] = ["D1#p#0001", "D1#p#0002"]  # D1#p#0002 was never judged
    assert any("relevant_chunk_ids" in e for e in run(r)["errors"])


def test_grade_outside_scale_is_rejected():
    r = record()
    r["judgments"][0]["grade"] = 4
    r["relevance_grade"]["D1#p#0001"] = 4
    assert any("grade" in e for e in run(r)["errors"])


def test_content_hash_drift_is_detected():
    r = record()
    r["judgments"][0]["content_sha256"] = "f" * 64
    assert any("hash drift" in e for e in run(r)["errors"])


def test_gold_requires_a_human():
    assert any("gold tier" in e for e in run(record(label_tier="gold_human_verified"))["errors"])
    human = [{"annotator_id": "H1", "annotator_type": "human"}]
    assert run(record(label_tier="gold_human_verified", annotators=human))["ok"]


def test_pending_records_cannot_carry_gold():
    bad = record(annotation_status="pending_annotation", label_tier="candidate")
    assert any("pending" in e for e in run(bad)["errors"])
    ok = record(annotation_status="pending_annotation", label_tier="candidate", grades=())
    assert run(ok)["ok"]


def test_unanswerable_records_carry_no_relevant_chunks():
    bad = record(answerability="unanswerable", expected_evidence_status="insufficient")
    assert any("must not carry relevant" in e for e in run(bad)["errors"])
    ok = record(answerability="unanswerable", expected_evidence_status="insufficient",
                annotation_status="verified_unanswerable", grades=(("D2#p#0001", 0),))
    assert run(ok)["ok"]


def test_answerable_needs_evidence():
    assert any("without relevant" in e for e in run(record(grades=(("D2#p#0001", 0),)))["errors"])


def test_empty_duplicate_and_sensitive_questions():
    assert not run(record(question="   "))["ok"]
    dup = run(record(), record(qid="q002", question="rối loạn phổ tự kỷ là gì"))
    assert any("duplicate question text" in e for e in dup["errors"])
    assert not run(record(question="Liên hệ test@example.com về tự kỷ?"))["ok"]


def test_corpus_pin_must_match_manifest():
    r = record()
    r["corpus"]["embedding_manifest_sha256"] = "b" * 64
    assert any("corpus pin" in e for e in run(r)["errors"])


def test_unexpected_field_and_bad_enum():
    assert any("unexpected fields" in e for e in run(record(extra_field=1))["errors"])
    assert any("query_category" in e for e in run(record(query_category="random"))["errors"])


def test_statistics_split_pending_from_annotated():
    stats = run(record(), record(qid="q002", question="Một câu khác hẳn?", annotation_status="pending_annotation",
                                 label_tier="candidate", grades=()))["stats"]
    assert stats["pending"] == 1 and stats["fully_annotated_single_pass"] == 1 and stats["human_verified"] == 0


@pytest.mark.parametrize("grade", [-1, 0, 1, 2, 3])
def test_every_grade_on_the_scale_is_accepted(grade):
    rel = (("D1#p#0001", 3),) if grade < 2 else ()
    assert run(record(grades=(*rel, ("D1#p#0002", grade))))["ok"]
