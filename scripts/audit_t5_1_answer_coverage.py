"""T5.1: read-only audit of the 105-question content-eval set against the live /api/chat.

Captures, per question: routing branch/confidence, cache status, evidence sources, Evidence Gate
support_type/age_mismatch, and an excerpt-level language guess (Vietnamese-diacritic count), to quantify
exactly how often a cached ASD question gets a real Vietnamese template answer vs. an English-heavy
extractive fallback. Read-only: uses the research_reader role via create_app(); writes only to
eval/reports/t5_1_audit_raw.json, never to the database.
"""

import json
import re

from fastapi.testclient import TestClient

from app.api import create_app
from app.router.classifier import classify

client = TestClient(create_app())
DATASET = "eval/datasets/asd_qa_eval_v2.jsonl"
with open(DATASET, encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

VN_CHARS = re.compile(
    "[ăâêôơưđáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.IGNORECASE)


def excerpt_is_vietnamese(text: str) -> bool:
    if not text:
        return False
    return len(VN_CHARS.findall(text)) >= 2  # at least 2 VN-specific diacritic chars


rows = []
for rec in records:
    intent = classify(rec["question_vi"])
    r = client.post("/api/chat", json={"query": rec["question_vi"], "top_k": 5})
    body = r.json()
    evidence = body.get("evidence", [])
    mode = body.get("answer_mode")

    excerpt_langs = [("vi" if excerpt_is_vietnamese(e["excerpt"]) else "en") for e in evidence]
    if mode == "topic_template":
        answer_lang = "vi"  # hand-authored Vietnamese template text, independent of excerpt language
    elif mode == "extractive_fallback":
        answer_lang = "vi" if all(lang == "vi" for lang in excerpt_langs) else (
            "mixed" if any(lang == "vi" for lang in excerpt_langs) else "en")
    elif mode in ("greeting_template", "out_of_scope", "insufficient_evidence",
                  "safety_refusal_dosing", "safety_caution_unproven_cure"):
        answer_lang = "vi"  # these are fixed Vietnamese messages regardless of evidence
    else:
        answer_lang = "n/a"

    rows.append({
        "question_id": rec["question_id"], "question_vi": rec["question_vi"], "category": rec["category"],
        "expected_behavior": rec["expected_behavior"], "safety_level": rec["safety_level"],
        "intent_branch": intent.branch, "intent_confidence": intent.confidence,
        "http": r.status_code, "answer_mode": mode, "retrieval_status": body.get("retrieval_status"),
        "evidence_count": len(evidence),
        "evidence_sources": [e["source_id"] for e in evidence],
        "support_types": [e.get("support_type") for e in evidence],
        "age_mismatch_any": any(e.get("age_mismatch") for e in evidence),
        "excerpt_langs": excerpt_langs,
        "answer_lang": answer_lang,
        "error_code": (body.get("error") or {}).get("code"),
    })

with open("eval/reports/t5_1_audit_raw.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print("done", len(rows))
