"""Phase 1/8: score the router against the independently-labeled eval/datasets/intent_routing_v1.jsonl.

Labels in that file were written by direct judgment BEFORE this script was run, not derived from the
classifier's own output (per the task's explicit prohibition on using the system under test to produce
its own ground truth). This script only reads the dataset and the classifier; it writes no labels.
"""

from __future__ import annotations

import json
import sys
from collections import Counter

from app.config import ROOT
from app.router.classifier import classify

DATASET = ROOT / "eval" / "datasets" / "intent_routing_v1.jsonl"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    records = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]

    total = len(records)
    correct = 0
    by_category: dict[str, list[int]] = {}
    mismatches = []

    for rec in records:
        result = classify(rec["text"])
        is_correct = result.branch == rec["expected_branch"]
        correct += is_correct
        cat = rec.get("category", "uncategorized")
        by_category.setdefault(cat, [0, 0])
        by_category[cat][0] += is_correct
        by_category[cat][1] += 1
        if not is_correct:
            mismatches.append((rec["id"], rec["category"], rec["text"], rec["expected_branch"], result.branch,
                              rec.get("notes", "")))

    print(f"Overall: {correct}/{total} = {correct / total:.1%}\n")
    print("By category:")
    for cat, (c, n) in sorted(by_category.items()):
        print(f"  {cat:24s} {c:3d}/{n:3d} = {c / n:.0%}")

    print(f"\nMismatches ({len(mismatches)}):")
    for id_, cat, text, expected, actual, notes in mismatches:
        print(f"  [{id_}] ({cat}) {text!r} -> expected={expected} actual={actual}" +
              (f"  note: {notes}" if notes else ""))

    branch_counts = Counter(r["expected_branch"] for r in records)
    print(f"\nExpected-branch distribution: {dict(branch_counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
