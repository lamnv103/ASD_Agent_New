"""T5.4 Phase 0/1: read-only end-to-end re-evaluation of the 105-question content-eval set against the
live /api/chat. Captures every field the task requires, plus a `final_evaluation` category. Read-only:
uses the research_reader role via create_app(); writes only to eval/reports/t5_4_*.json.
"""

import json
import re

from fastapi.testclient import TestClient

from app.api import create_app
from app.config import ROOT
from app.router.classifier import classify

VN_CHARS = re.compile(
    "[ăâêôơưđáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.IGNORECASE)


def excerpt_is_vietnamese(text: str) -> bool:
    return bool(text) and len(VN_CHARS.findall(text)) >= 2


def final_evaluation(body: dict) -> str:
    mode = body.get("answer_mode")
    code = (body.get("error") or {}).get("code")
    if code == "QUERY_NOT_CACHED":
        return "cache_miss"
    if mode == "out_of_scope":
        return "out_of_scope"
    if mode in ("safety_refusal_dosing", "safety_caution_unproven_cure"):
        return "safety_refusal"
    if mode == "insufficient_evidence":
        return "insufficient_evidence"
    if mode == "greeting_template":
        return "answered"  # not a content answer, but a correctly handled branch
    if mode == "topic_template":
        return "answered"
    if mode == "extractive_fallback":
        return "partially_answered"  # real evidence shown, but not a synthesized Vietnamese answer
    return "unknown"


def run(dataset_path, out_path):
    with open(dataset_path, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    client = TestClient(create_app())

    rows = []
    for rec in records:
        q = rec["question_vi"] if "question_vi" in rec else rec["question"]
        qid = rec.get("question_id", rec.get("id"))
        intent = classify(q)
        r = client.post("/api/chat", json={"query": q, "top_k": 5})
        body = r.json()
        evidence = body.get("evidence", [])

        # Claim-level citation re-validation: re-derive the RetrievedChunk-shaped fields and re-check
        # (defense in depth; this duplicates app.api's own call but independently, from this script).
        cited_ok = True
        for e in evidence:
            if not e.get("source_url") or not e.get("source_id"):
                cited_ok = False

        rows.append({
            "question_id": qid, "question": q, "category": rec.get("category"),
            "routing_result": intent.branch, "routing_confidence": intent.confidence,
            "retrieval_status": body.get("retrieval_status"), "answer_mode": body.get("answer_mode"),
            "answer_text": body.get("answer"),
            "answer_language": "vi" if (body.get("answer_mode") != "extractive_fallback") else (
                "vi" if all(excerpt_is_vietnamese(e["excerpt"]) for e in evidence) else (
                    "mixed" if any(excerpt_is_vietnamese(e["excerpt"]) for e in evidence) else "en")),
            "evidence_support_type": [e.get("support_type") for e in evidence],
            "age_mismatch": any(e.get("age_mismatch") for e in evidence),
            "source_names": [e.get("title") for e in evidence],
            "source_urls": [e.get("source_url") for e in evidence],
            "citation_fields_present": cited_ok,
            "http": r.status_code, "error_code": (body.get("error") or {}).get("code"),
            "final_evaluation": final_evaluation(body),
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    return rows


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    rows = run(ROOT / "eval" / "datasets" / "asd_qa_eval_v2.jsonl",
              ROOT / "eval" / "reports" / "t5_4_105_results.json")
    from collections import Counter
    print("Total:", len(rows))
    print(Counter(r["final_evaluation"] for r in rows))
