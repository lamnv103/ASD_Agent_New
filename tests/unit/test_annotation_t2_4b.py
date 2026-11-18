# ruff: noqa: E501
"""T2.4-B annotation pipeline: kappa maths, import validation, never-average finalization, blind-package leakage.
All label data here is SYNTHETIC test fixture data, never used as annotation."""

import importlib.util
import json

import pytest

from app.config import ROOT

_spec = importlib.util.spec_from_file_location("ann", ROOT / "scripts" / "annotation_t2_4b.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)


# ------------------------------------------------------------------ kappa
def test_kappa_perfect_and_perfectly_reversed():
    assert A.weighted_kappa([(0, 0), (1, 1), (2, 2), (3, 3)], A.ORDINAL, "quadratic") == 1.0
    assert A.weighted_kappa([(0, 3), (0, 3), (3, 0), (3, 0)], A.ORDINAL, "quadratic") == -1.0


def test_unweighted_kappa_textbook_2x2():
    pairs = [(1, 1)] * 20 + [(1, 0)] * 5 + [(0, 1)] * 10 + [(0, 0)] * 15  # po = .7, pe = .5 -> 0.4
    assert A.weighted_kappa(pairs, (0, 1), "none") == 0.4


def test_quadratic_penalises_distance_more_than_linear():
    pairs = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 3), (3, 0), (1, 2), (2, 1)]
    q, lin = A.weighted_kappa(pairs, A.ORDINAL, "quadratic"), A.weighted_kappa(pairs, A.ORDINAL, "linear")
    assert q is not None and lin is not None and q != lin


def test_kappa_undefined_when_no_variation():
    assert A.weighted_kappa([(2, 2), (2, 2)], A.ORDINAL, "quadratic") is None
    assert A.weighted_kappa([], A.ORDINAL, "linear") is None


# ------------------------------------------------------------------ agreement / disagreements
def lab(ann, q, c, g, needs=False):
    return {"annotator": ann, "annotation_code": f"{ann}{q}{c}", "question_id": q, "chunk_id": c, "item_id": f"i{q}{c}",
            "grade": g, "needs_review": needs, "rationale": "r", "evidence_span": "e", "confidence": "high", "review_note": "n" if needs else None}


def test_minus1_and_needs_review_are_kept_out_of_kappa_and_reported():
    la = [lab("a", "q1", "c1", 2), lab("a", "q1", "c2", -1), lab("a", "q1", "c3", None, True), lab("a", "q1", "c4", 0)]
    lb = [lab("b", "q1", "c1", 2), lab("b", "q1", "c2", 1), lab("b", "q1", "c3", 3), lab("b", "q1", "c4", 1)]
    m, dis = A.agreement(la, lb)
    assert m["pairs_in_kappa"] == 2  # c1, c4 only
    assert m["conflicting_minus1"]["pairs_with_any_minus1"] == 1
    assert m["needs_review_rate"]["a"] == 0.25
    assert {d["chunk_id"]: d["kind"] for d in dis} == {"c2": "conflicting_involved", "c3": "needs_review", "c4": "adjacent_or_other"}
    assert m["exact_agreement"] == 0.3333  # c1 agree; c2, c4 disagree (c3 excluded)


def test_disagreement_kinds():
    la = [lab("a", "q", "x", 1), lab("a", "q", "y", 3)]
    lb = [lab("b", "q", "x", 2), lab("b", "q", "y", 0)]
    _, dis = A.agreement(la, lb)
    assert {d["chunk_id"]: d["kind"] for d in dis} == {"x": "relevance_boundary_1_vs_2", "y": "relevant_vs_irrelevant"}


# ------------------------------------------------------------------ finalize: no averaging, no filling
def test_finalize_never_averages_and_keeps_pending():
    la = [lab("a", "q", "agree", 2), lab("a", "q", "dis", 1), lab("a", "q", "adj", 3), lab("a", "q", "onlya", 2)]
    lb = [lab("b", "q", "agree", 2), lab("b", "q", "dis", 3), lab("b", "q", "adj", 0)]
    adj = [{"question_id": "q", "chunk_id": "adj", "final_grade": 1, "adjudicator_id": "expert1", "reason": "why"}]
    out = {r["chunk_id"]: r for r in A.finalize(la, lb, adj)}
    assert out["agree"]["final_grade"] == 2 and out["agree"]["adjudication_status"] == "agreed"
    assert out["dis"]["final_grade"] is None and out["dis"]["adjudication_status"] == "pending_adjudication"  # never 2
    assert out["adj"]["final_grade"] == 1 and out["adj"]["adjudicator_id"] == "expert1"
    assert out["onlya"]["final_grade"] is None and out["onlya"]["adjudication_status"] == "single_annotator_only"
    assert all(r["provenance"]["ai_labels_used"] is None for r in out.values())  # unknown annotators: not claimed


def test_provenance_marks_ai_annotators_as_silver_never_human():
    ai = {"a": {"id": "agent_A", "type": "ai_model", "model": "m1"}, "b": {"id": "agent_B", "type": "ai_model", "model": "m2"},
          "adjudicator": {"id": "agent_C", "type": "ai_model", "model": "m1"}}
    hu = {k: {"id": k, "type": "human"} for k in ("a", "b", "adjudicator")}
    assert A.provenance(ai)["ai_labels_used"] is True and A.provenance(ai)["label_tier"] == "silver_ai_dual_annotation"
    assert A.provenance(hu)["label_tier"] == "gold_human_dual_annotation"
    assert A.annotator_ids(ai) >= {"agent_A", "agent_B"} and "agent_C" not in A.annotator_ids(ai)


@pytest.mark.parametrize("bad,msg", [
    ({"final_grade": 1.5}, "final_grade"),
    ({"reason": ""}, "required"),
    ({"adjudicator_id": "A"}, "must not be annotator"),
    ({"chunk_id": "nope"}, "not a disagreement"),
])
def test_adjudication_validation(bad, msg):
    rec = {"question_id": "q", "chunk_id": "c", "final_grade": 2, "adjudicator_id": "expert", "reason": "x"} | bad
    errs = A.validate_adjudication([rec], {("q", "c")}, {"A", "B"})
    assert any(msg in e for e in errs)


# ------------------------------------------------------------------ import validation
CMAP = {"C1": {"annotator": "a", "question_id": "q", "chunk_id": "c1", "item_id": "i1"},
        "C2": {"annotator": "a", "question_id": "q", "chunk_id": "c2", "item_id": "i2"},
        "B1": {"annotator": "b", "question_id": "q", "chunk_id": "c1", "item_id": "i1"}}


def row(code="C1", grade="2", **kw):
    return {"annotation_code": code, "content": "the child has epilepsy", "grade": grade, "rationale": "r",
            "evidence_span": "has epilepsy", "confidence": "high", "needs_review": "", "review_note": ""} | kw


def test_blank_grade_stays_unjudged_never_zero():
    labels, errors = A.parse_returned([row(grade="")], CMAP, "a")
    assert labels == [] and errors == []


@pytest.mark.parametrize("r,msg", [
    (row(code="B1"), "foreign"), (row(code="ZZ"), "unknown"), (row(grade="5"), "not in -1..3"),
    (row(grade="two"), "not a number"), (row(rationale=""), "without rationale"),
    (row(evidence_span=""), "without evidence_span"), (row(confidence="sure"), "confidence"),
    (row(evidence_span="not in text"), "not a substring"),
    (row(grade="", needs_review="yes", review_note=""), "needs_review without review_note"),
])
def test_import_rejects_bad_rows(r, msg):
    _, errors = A.parse_returned([r], CMAP, "a")
    assert any(msg in e for e in errors), errors


def test_import_rejects_duplicate_codes_and_accepts_needs_review():
    _, errors = A.parse_returned([row(), row()], CMAP, "a")
    assert any("duplicate" in e for e in errors)
    labels, errors = A.parse_returned([row(code="C2", grade="", needs_review="yes", review_note="unsure term")], CMAP, "a")
    assert not errors and labels[0]["needs_review"] and labels[0]["grade"] is None


# ------------------------------------------------------------------ blind packages (real files)
PKG = {a: ROOT / "eval" / "annotation" / "t2_4b" / f"annotator_{a}" / f"fts_blind_annotation_package_annotator_{a}_2026-11-15.jsonl" for a in "ab"}
KEY = ROOT / "eval" / "reports" / "fts_candidate_pool_key_2026-11-15.jsonl"


@pytest.mark.skipif(not all(p.exists() for p in PKG.values()), reason="packages not generated")
def test_packages_have_no_leaking_fields_or_ids_and_independent_codes():
    key = [json.loads(x) for x in KEY.read_text(encoding="utf-8").splitlines()]
    internal = {k["chunk_id"] for k in key} | {k["item_id"] for k in key}
    codes = {}
    for a, p in PKG.items():
        rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()]
        assert len(rows) == 2791
        for r in rows:
            assert list(r) == A.PACKAGE_FIELDS and not set(r) & A.FORBIDDEN_IN_PACKAGE
            assert r["annotation_code"] not in internal
            assert not any(r[f] for f in ("grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"))
        codes[a] = [r["annotation_code"] for r in rows]
        assert len(set(codes[a])) == 2791
    assert not set(codes["a"]) & set(codes["b"])
    assert codes["a"] != codes["b"]  # independent orders and codes
    # annotator folders contain only blind material (package, guideline, agent instructions, batches, helper, own work/output)
    allowed = ("fts_blind_annotation_package_annotator_", "annotation_guidelines_", "AGENT_INSTRUCTIONS_", "batches", "tools",
               "work", "returned", "returned_pilot_discarded", "returned_merged_annotator_")
    for a in "ab":
        names = sorted(p.name for p in PKG[a].parent.iterdir())
        assert all(n.startswith(allowed) for n in names), names
        for b in sorted((PKG[a].parent / "batches").glob("batch_*.jsonl")):
            for line in b.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                assert list(r) == A.BATCH_FIELDS and r["annotation_code"] not in internal
