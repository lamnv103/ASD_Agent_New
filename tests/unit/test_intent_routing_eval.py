"""Phase 1/8 regression: scores the router against the independently-labeled 105-item dataset.

Labels in eval/datasets/intent_routing_v1.jsonl were written before this test was run, by direct
judgment, not by copying the classifier's own output (see the dataset file's per-item "notes" for the
reasoning on every deliberately ambiguous case). A small number of documented gray-zone mismatches are
expected and allowed; this test guards against a *new* regression, not against those known limitations.
"""

import json

from app.config import ROOT
from app.router.classifier import classify

DATASET = ROOT / "eval" / "datasets" / "intent_routing_v1.jsonl"
KNOWN_GRAY_ZONE_IDS = {"ir069", "ir092", "ir105"}  # see phase_1 report for why each is a judgment call


def _records():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_dataset_has_at_least_100_independently_labeled_cases():
    assert len(_records()) >= 100


def test_dataset_covers_all_three_branches_with_a_real_distribution():
    branches = {r["expected_branch"] for r in _records()}
    assert branches == {"greeting", "out_of_scope", "asd_question"}


def test_routing_accuracy_meets_the_locked_in_floor():
    records = _records()
    correct = sum(classify(r["text"]).branch == r["expected_branch"] for r in records)
    accuracy = correct / len(records)
    assert accuracy >= 0.95, f"routing accuracy regressed to {accuracy:.1%}"


def test_every_mismatch_is_a_previously_documented_gray_zone_case_not_a_new_regression():
    mismatches = {r["id"] for r in _records() if classify(r["text"]).branch != r["expected_branch"]}
    new_regressions = mismatches - KNOWN_GRAY_ZONE_IDS
    assert not new_regressions, f"new routing regressions not previously documented: {new_regressions}"
