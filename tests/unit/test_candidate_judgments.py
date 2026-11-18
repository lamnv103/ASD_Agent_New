"""T2.3.2 candidate judgments: merge rules and validator checks (positive + negative case per rule)."""

import copy
import importlib.util
import json

import pytest

from app.config import ROOT

_spec = importlib.util.spec_from_file_location("candidate_judgments", ROOT / "scripts" / "candidate_judgments.py")
CJ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CJ)

SCHEMA = json.loads(CJ.JUDGMENTS_SCHEMA.read_text(encoding="utf-8"))
PIN = {"chunking_profile": "p", "embedding_profile": "e", "embedding_manifest_sha256": "m" * 64,
       "authorization_id": 2, "authorization_allowlist": "a.csv", "authorization_allowlist_sha256": "a" * 64}
MANIFEST = {f"D1#p#000{i}": {"chunk_id": f"D1#p#000{i}", "document_id": "D1", "source_id": "S1",
                             "content_hash": str(i) * 64} for i in range(1, 6)}
ALLOW = set(MANIFEST) - {"D1#p#0005"}
D1_EXCLUDED = {"D1#p#0004"}
POOL = {("q001", c): {"question_id": "q001", "chunk_id": c, "source_id": "S1", "rank": str(i),
                      "suggested_review_priority": "high"} for i, c in enumerate(sorted(MANIFEST), 1)}


def original():
    return [{"question_id": "q001", "judgments": [
        {"chunk_id": "D1#p#0001", "document_id": "D1", "source_id": "S1", "content_sha256": "1" * 64, "grade": 3,
         "evidence_class": "relevant", "aspect": "a", "rationale_vi": "cũ"}],
        "relevance_grade": {"D1#p#0001": 3}, "relevant_chunk_ids": ["D1#p#0001"], "relevant_document_ids": ["D1"],
        "expected_sources": ["S1"], "candidate_chunk_ids": [], "annotation_completeness": "complete_for_judged_pool",
        "search_log": [], "annotation_method": "m", "annotation_notes": ""}]


def row(chunk, status="judged", grade=2, **kw):
    m = MANIFEST[chunk]
    judged = status in ("judged", "needs_adjudication")
    base = {"judgment_version": "t2_3_2_v1", "judgment_id": "0" * 20, "question_id": "q001", "chunk_id": chunk,
            "document_id": m["document_id"], "source_id": m["source_id"], "content_sha256": m["content_hash"],
            "status": status, "grade": grade if judged else None,
            "evidence_class": CJ.GRADE_CLASS[grade] if judged else None, "aspect": "x" if judged else None,
            "rationale_vi": "lý do" if status != "unjudged" else None,
            "exclusion_reason": "question_out_of_scope" if status == "excluded" else None,
            "annotator": {"annotator_id": "A1", "annotator_type": "ai_model"} if status != "unjudged" else None,
            "annotated_at": "2026-11-15T00:00:00+07:00" if status != "unjudged" else None,
            "judging_protocol": "blind", "corpus": dict(PIN), "base_dataset": {"file": "f", "sha256": "s"},
            "origin": {"pool": "p.csv", "pool_sha256": "p", "question_group": "answerable",
                       "rank": int(POOL[("q001", chunk)]["rank"]), "suggested_review_priority": "high"}}
    base.update(kw)
    return base


def check_rows(rows):
    return CJ.validate_rows(rows, SCHEMA, original(), MANIFEST, ALLOW, D1_EXCLUDED, POOL, PIN)


def check_merge(rows, merged=None):
    m = merged if merged is not None else CJ.merge(original(), rows, "j.jsonl", "s" * 64)
    return CJ.validate_merge(original(), rows, m, CJ.dump_jsonl(m), "j.jsonl", "s" * 64)


GOOD = [row("D1#p#0002", grade=2), row("D1#p#0003", "unjudged")]


def test_valid_rows_and_merge_pass():
    assert check_rows(GOOD) == []
    assert check_merge(GOOD) == []


def test_merge_keeps_old_labels_and_derives_relevant_ids():
    m = CJ.merge(original(), [*GOOD, row("D1#p#0004", "needs_adjudication", grade=-1)], "j", "s" * 64)[0]
    assert m["judgments"][0] == original()[0]["judgments"][0]
    assert m["relevant_chunk_ids"] == ["D1#p#0001", "D1#p#0002"]
    assert m["candidate_chunk_ids"] == ["D1#p#0003", "D1#p#0004"]  # unjudged + needs_adjudication, never graded
    assert "D1#p#0003" not in m["relevance_grade"] and "D1#p#0004" not in m["relevance_grade"]
    assert m["annotation_completeness"] == "partial"
    assert "cần phân xử" in m["annotation_notes"]


def test_merge_is_deterministic():
    a = CJ.dump_jsonl(CJ.merge(original(), GOOD, "j", "s" * 64))
    assert a == CJ.dump_jsonl(CJ.merge(original(), list(reversed(GOOD)), "j", "s" * 64))


def test_excluded_rows_are_neither_judged_nor_candidates():
    m = CJ.merge(original(), [row("D1#p#0002", "excluded")], "j", "s" * 64)[0]
    assert m["candidate_chunk_ids"] == [] and "D1#p#0002" not in m["relevance_grade"]


def test_merge_refuses_rejudging_an_original_label():
    with pytest.raises(CJ.MergeError):
        CJ.merge(original(), [row("D1#p#0001", grade=0)], "j", "s" * 64)


@pytest.mark.parametrize("mutate,needle", [
    (lambda r: r.pop("rationale_vi"), "schema"),                                   # 1
    (lambda r: r.update(question_id="q999"), "unknown question_id"),               # 2
    (lambda r: r.update(chunk_id="D9#p#0001"), "not in the embedded set"),         # 3
    (lambda r: r.update(grade=5), "grade 5"),                                      # 4
    (lambda r: r.update(evidence_class="negative"), "evidence_class"),             # 4
    (lambda r: r.update(status="maybe"), "status 'maybe'"),                        # 5
    (lambda r: r.update(content_sha256="f" * 64), "hash mismatch"),                # 11
    (lambda r: r.update(source_id="S9"), "mismatch"),                              # 11
    (lambda r: r.update(rationale_vi="  "), "missing rationale"),                  # 12
    (lambda r: r.update(annotator=None), "annotator"),                             # 10
    (lambda r: r.update(corpus={**PIN, "authorization_id": 1}), "pin differs"),    # 10/13
    (lambda r: r["origin"].update(rank=99), "rank/priority"),                      # 10
])
def test_row_checks_reject(mutate, needle):
    r = copy.deepcopy(GOOD[0])
    mutate(r)
    errs = check_rows([r])
    assert any(needle in e for e in errs), errs


def test_unjudged_row_may_not_carry_a_grade():  # 8
    assert any("must not carry a grade" in e for e in check_rows([row("D1#p#0003", "unjudged") | {"grade": 0}]))


def test_duplicate_judgment_rejected():  # 6
    assert any("duplicate" in e for e in check_rows([GOOD[0], copy.deepcopy(GOOD[0])]))


def test_d1_excluded_chunk_rejected():  # 9
    assert any("D-1" in e for e in check_rows([row("D1#p#0004")]))


def test_chunk_outside_authorization_rejected():  # 13
    pool = dict(POOL)
    errs = CJ.validate_rows([row("D1#p#0005")], SCHEMA, original(), MANIFEST, ALLOW, D1_EXCLUDED, pool, PIN)
    assert any("allowlist" in e for e in errs)


def test_excluded_requires_reason():
    assert any("exclusion_reason" in e for e in check_rows([row("D1#p#0002", "excluded", exclusion_reason="")]))


def test_lost_old_label_detected():  # 7
    m = CJ.merge(original(), GOOD, "j", "s" * 64)
    m[0]["judgments"][0]["grade"] = 1
    assert any("original judgments changed" in e for e in check_merge(GOOD, m))


def test_unjudged_turned_into_zero_detected():  # 8
    m = CJ.merge(original(), GOOD, "j", "s" * 64)
    m[0]["judgments"].append({**{k: GOOD[0][k] for k in CJ.JUDGMENT_KEYS}, "chunk_id": "D1#p#0003",
                              "content_sha256": "3" * 64, "grade": 0, "evidence_class": "negative"})
    m[0]["relevance_grade"]["D1#p#0003"] = 0
    assert any("non-judged candidate" in e for e in check_merge(GOOD, m))


def test_merge_not_reproducible_detected():  # 14
    m = CJ.merge(original(), GOOD, "j", "s" * 64)
    m[0]["annotation_notes"] = "sửa tay"
    assert any("not reproducible" in e for e in check_merge(GOOD, m))
