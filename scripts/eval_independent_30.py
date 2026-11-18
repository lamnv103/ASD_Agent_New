"""T5.4 Phase 5: read-only run of the frozen, independent 32-question set
(eval/datasets/independent_eval_v1.jsonl) against the live /api/chat. Run once; results are reported
honestly, not used to retune any template (see independent_30_question_results.md for the disclosure
rule this script's output is subject to)."""

import json

from fastapi.testclient import TestClient

from app.api import create_app
from app.config import ROOT
from app.router.classifier import classify

DATASET = ROOT / "eval" / "datasets" / "independent_eval_v1.jsonl"
OUT = ROOT / "eval" / "reports" / "independent_30_results.json"


def main() -> int:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    with open(DATASET, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    client = TestClient(create_app())

    rows = []
    for rec in records:
        q = rec["question"]
        intent = classify(q)
        r = client.post("/api/chat", json={"query": q, "top_k": 5})
        body = r.json()
        rows.append({
            "id": rec["id"], "question": q, "category": rec["category"], "notes": rec.get("notes"),
            "routing_result": intent.branch, "routing_confidence": intent.confidence,
            "http": r.status_code, "answer_mode": body.get("answer_mode"),
            "retrieval_status": body.get("retrieval_status"), "answer_text": body.get("answer"),
            "evidence_sources": [e["source_id"] for e in body.get("evidence", [])],
            "support_types": [e.get("support_type") for e in body.get("evidence", [])],
            "error_code": (body.get("error") or {}).get("code"),
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    from collections import Counter
    print("Total:", len(rows))
    print("Routing:", Counter(r["routing_result"] for r in rows))
    print("Answer mode:", Counter(r["answer_mode"] for r in rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
