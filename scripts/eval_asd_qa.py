"""Phase 5/6: run eval/datasets/asd_qa_eval_v2.jsonl against the live /api/chat and report real behavior.

Labels (expected_behavior etc.) were written independently before this script ran (see the dataset
file). This script never edits the dataset; it only reports what the live system actually did next to
what was expected, including the (expected, disclosed) case where cache-only mode blocks a question.
"""

from __future__ import annotations

import json
import sys

from fastapi.testclient import TestClient

from app.api import create_app
from app.config import ROOT

DATASET = ROOT / "eval" / "datasets" / "asd_qa_eval_v2.jsonl"
OUT = ROOT / "eval" / "reports" / "asd_qa_eval_v2_results.json"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    records = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]
    client = TestClient(create_app())

    results = []
    for rec in records:
        resp = client.post("/api/chat", json={"query": rec["question_vi"], "top_k": 5})
        body = resp.json()
        results.append({
            "question_id": rec["question_id"], "category": rec["category"], "question_vi": rec["question_vi"],
            "expected_behavior": rec["expected_behavior"], "safety_level": rec["safety_level"],
            "http": resp.status_code, "actual_answer_mode": body.get("answer_mode"),
            "actual_retrieval_status": body.get("retrieval_status"),
            "error_code": (body.get("error") or {}).get("code"),
            "evidence_count": len(body.get("evidence", [])),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    cached = [r for r in results if r["error_code"] != "QUERY_NOT_CACHED"]
    blocked = [r for r in results if r["error_code"] == "QUERY_NOT_CACHED"]
    print(f"Total: {len(results)}  Answerable (cached): {len(cached)}  Blocked (uncached): {len(blocked)}")

    by_cat: dict[str, list[int]] = {}
    for r in results:
        c = r["category"]
        by_cat.setdefault(c, [0, 0])
        by_cat[c][1] += 1
        if r["error_code"] != "QUERY_NOT_CACHED":
            by_cat[c][0] += 1
    print("\nCache coverage by category (answerable/total):")
    for c, (a, n) in sorted(by_cat.items()):
        print(f"  {c:22s} {a:2d}/{n:2d}")

    print(f"\nFull results written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
