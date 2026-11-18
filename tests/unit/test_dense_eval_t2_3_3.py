"""T2.3.3 metric rules: unjudged never counts as grade 0, -1 has no nDCG gain, sources are deduplicated."""

import importlib.util

import pytest

from app.config import ROOT


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E = _load("dense_eval_t2_3_3", "scripts/dense_eval_t2_3_3.py")
T231 = _load("dense_retrieval_eval", "scripts/dense_retrieval_eval.py")


def rec(grades):
    return {"judgments": [{"chunk_id": c, "grade": g, "source_id": c.split("#")[0], "document_id": c.split("#")[0]}
                          for c, g in grades.items()]}


def ranked(ids):
    return [{"rank": i + 1, "chunk_id": c, "source_id": c.split("#")[0], "document_id": c.split("#")[0],
             "cosine_distance": 0.5} for i, c in enumerate(ids)]


IDS = [f"S{i % 3}#{i:02d}" for i in range(20)]  # 3 sources, 20 chunks
RETR = set(IDS)


def test_unjudged_bounds_and_coverage():
    m = E.question_metrics(ranked(IDS), rec({IDS[2]: 3, IDS[0]: 0}), RETR, T231)
    assert m["judged@5"] == 2 and m["unjudged@5"] == 3
    assert m["judged_coverage@5"] == pytest.approx(0.4)
    assert m["precision_lb@5"] == pytest.approx(0.2)          # unjudged treated as non-relevant only in the LOWER bound
    assert m["precision_ub@5"] == pytest.approx(0.8)          # 1 relevant + 3 unjudged
    assert m["judged_precision@5"] == pytest.approx(0.5)
    assert m["mrr"] == pytest.approx(1 / 3) and m["mrr_ub"] == pytest.approx(1 / 2)
    assert m["unjudged_before_first_relevant"] == 1


def test_conflicting_grade_has_no_gain_and_is_not_relevant():
    m = E.question_metrics(ranked(IDS), rec({IDS[0]: -1, IDS[1]: 2}), RETR, T231)
    assert m["relevant_known"] == 1 and m["conflict_known"] == 1
    assert m["first_relevant_rank"] == 2
    ideal = T231.dcg([3])
    assert m["ndcg@5"] == pytest.approx(T231.dcg([0, 3]) / ideal)  # -1 at rank 1 contributes nothing
    assert m["conflict_coverage@20"] == 1.0


def test_source_recall_is_deduplicated():
    # two relevant chunks from the same source S0 count as ONE source
    m = E.question_metrics(ranked(IDS), rec({IDS[0]: 3, IDS[3]: 2, IDS[1]: 2}), RETR, T231)
    assert m["relevant_sources"] == 2
    assert m["source_recall@5"] == 1.0


def test_no_relevant_gives_none_not_zero():
    m = E.question_metrics(ranked(IDS), rec({IDS[0]: 0}), RETR, T231)
    assert m["recall@10"] is None and m["hit@10"] is None and m["ndcg@10"] is None
    assert m["mrr"] == 0.0


def test_relevant_but_not_retrievable_is_excluded_from_denominator():
    m = E.question_metrics(ranked(IDS), rec({IDS[0]: 3, "GONE#99": 3}), RETR, T231)
    assert m["relevant_known"] == 1 and m["relevant_not_retrievable"] == 1
    assert m["recall@5"] == 1.0
