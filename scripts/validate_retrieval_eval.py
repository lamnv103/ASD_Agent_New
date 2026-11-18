"""Validate the retrieval evaluation dataset (eval/datasets/retrieval_eval_v1.jsonl). Reads files only:
no database connection, no network, no provider API.

Checks: JSONL parses; unique question_id; required fields/enums from the schema; grades in {-1..3};
every judged chunk exists in the embedded set (embedding_manifest.csv) with the same document/source and
content hash; relevant_chunk_ids == judged chunks with grade >= 2 (nothing unjudged, nothing invented);
gold tier only with a human annotator; pending records carry no relevant ids; unanswerable/blocked/out-of-scope
records carry no relevant ids; answerable records have >= 1; no empty or near-duplicate questions; no
email/phone/secret-looking strings; corpus pin matches the manifest.

Usage: python -B scripts/validate_retrieval_eval.py [--dataset PATH] [--report PATH]
Exit code 0 = valid (warnings allowed), 1 = errors.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl"
SCHEMA = ROOT / "eval" / "datasets" / "retrieval_eval_v1_schema.json"
MANIFEST = ROOT / "eval" / "reports" / "embedding_manifest.csv"

NO_EVIDENCE = {"unanswerable", "out_of_scope"}
SENSITIVE = [re.compile(p) for p in (r"[\w.+-]+@[\w-]+\.[\w.]+", r"\b(?:\+?84|0)\d{9,10}\b",
                                     r"(?i)\b(api[_-]?key|secret|password|token)\b\s*[:=]", r"\b[A-Za-z0-9]{40,}\b")]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text.lower())
    return re.sub(r"[^\w\s]", "", re.sub(r"\s+", " ", text)).strip()


def jaccard(a: str, b: str) -> float:
    x, y = set(normalize(a).split()), set(normalize(b).split())
    return len(x & y) / max(1, len(x | y))


def load_manifest(path: Path) -> dict[str, dict]:
    with open(path, encoding="utf-8-sig") as f:
        return {r["chunk_id"]: r for r in csv.DictReader(f)}


def validate(lines: list[str], schema: dict, manifest: dict[str, dict], manifest_sha: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    records = []
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"line {n}: invalid JSON ({exc.msg})")
    props = schema["properties"]
    required = schema["required"]
    jprops = props["judgments"]["items"]
    ids = Counter(r.get("question_id") for r in records)
    errors += [f"duplicate question_id {k}" for k, v in ids.items() if v > 1]

    for r in records:
        qid = r.get("question_id", "?")
        missing = [k for k in required if k not in r]
        extra = [k for k in r if k not in props]
        if missing:
            errors.append(f"{qid}: missing fields {missing}")
        if extra:
            errors.append(f"{qid}: unexpected fields {extra}")
        for key, spec in props.items():
            if key in r and "enum" in spec and r[key] not in spec["enum"]:
                errors.append(f"{qid}: {key}={r[key]!r} not allowed")
            if key in r and "const" in spec and r[key] != spec["const"]:
                errors.append(f"{qid}: {key} must be {spec['const']!r}")
        if not re.fullmatch(props["question_id"]["pattern"], str(qid)):
            errors.append(f"{qid}: bad question_id format")
        if not str(r.get("question_vi", "")).strip():
            errors.append(f"{qid}: empty question")
        for style in r.get("query_style", []):
            if style not in props["query_style"]["items"]["enum"]:
                errors.append(f"{qid}: query_style {style!r} not allowed")

        judged = {}
        for j in r.get("judgments", []):
            jm = [k for k in jprops["required"] if k not in j]
            if jm:
                errors.append(f"{qid}: judgment missing {jm}")
                continue
            cid = j["chunk_id"]
            if cid in judged:
                errors.append(f"{qid}: chunk judged twice {cid}")
            judged[cid] = j["grade"]
            if j["grade"] not in jprops["properties"]["grade"]["enum"]:
                errors.append(f"{qid}: grade {j['grade']!r} not in {{-1,0,1,2,3}}")
            m = manifest.get(cid)
            if m is None:
                errors.append(f"{qid}: chunk not in the embedded set: {cid}")
                continue
            if m["document_id"] != j["document_id"] or m["source_id"] != j["source_id"]:
                errors.append(f"{qid}: document/source mismatch for {cid}")
            if m["content_hash"] != j["content_sha256"]:
                errors.append(f"{qid}: content hash drift for {cid}")
        expected_rel = [c for c, g in judged.items() if g >= 2]
        if r.get("relevant_chunk_ids") != expected_rel:
            errors.append(f"{qid}: relevant_chunk_ids must equal judged chunks with grade >= 2")
        if r.get("relevance_grade") != judged:
            errors.append(f"{qid}: relevance_grade does not match judgments")
        rel_docs = sorted({manifest[c]["document_id"] for c in expected_rel if c in manifest})
        if r.get("relevant_document_ids") != rel_docs:
            errors.append(f"{qid}: relevant_document_ids must be the documents of relevant chunks")
        if set(r.get("candidate_chunk_ids", [])) & set(r.get("relevant_chunk_ids", [])):
            errors.append(f"{qid}: candidate (unjudged) chunks inside relevant_chunk_ids")

        status, tier, ans = r.get("annotation_status"), r.get("label_tier"), r.get("answerability")
        humans = [a for a in r.get("annotators", []) if a.get("annotator_type") == "human"]
        if tier == "gold_human_verified" and not humans:
            errors.append(f"{qid}: gold tier without a human annotator")
        if status == "adjudicated" and len(r.get("annotators", [])) < 2:
            errors.append(f"{qid}: adjudicated needs >= 2 annotators")
        if status == "pending_annotation" and (expected_rel or tier not in ("candidate",)):
            errors.append(f"{qid}: pending record must have no relevant ids and tier 'candidate'")
        if ans in NO_EVIDENCE and expected_rel:
            errors.append(f"{qid}: {ans} record must not carry relevant chunks")
        if ans == "answerable" and status != "pending_annotation" and not expected_rel:
            errors.append(f"{qid}: answerable record without relevant chunks")
        if r.get("corpus", {}).get("embedding_manifest_sha256") != manifest_sha:
            errors.append(f"{qid}: corpus pin does not match embedding_manifest.csv")
        # identifiers (document/chunk ids contain '@' and long hashes) are checked against the manifest above
        blob = json.dumps({k: v for k, v in r.items() if k not in ("judgments", "relevance_grade", "corpus",
                                                                   "relevant_chunk_ids", "candidate_chunk_ids",
                                                                   "relevant_document_ids")},
                          ensure_ascii=False)
        for pat in SENSITIVE:
            if pat.search(blob):
                errors.append(f"{qid}: sensitive-looking string ({pat.pattern[:20]}…)")

    qs = [(r.get("question_id"), r.get("question_vi", "")) for r in records]
    norm = Counter(normalize(q) for _, q in qs)
    errors += [f"duplicate question text: {k!r}" for k, v in norm.items() if v > 1]
    for i, (a, qa) in enumerate(qs):
        for b, qb in qs[i + 1:]:
            if jaccard(qa, qb) >= 0.8:
                warnings.append(f"near-duplicate questions {a} / {b}")

    stats = statistics(records)
    return {"ok": not errors, "errors": errors, "warnings": warnings, "stats": stats}


def statistics(records: list[dict]) -> dict:
    rel = [r for r in records if r["relevant_chunk_ids"]]
    grades = Counter(j["grade"] for r in records for j in r["judgments"])
    return {
        "total_questions": len(records),
        "annotation_status": dict(Counter(r["annotation_status"] for r in records)),
        "label_tier": dict(Counter(r["label_tier"] for r in records)),
        "fully_annotated_single_pass": sum(r["annotation_status"] in ("annotated_single", "verified_unanswerable")
                                           for r in records),
        "human_verified": sum(r["label_tier"] == "gold_human_verified" for r in records),
        "pending": sum(r["annotation_status"] == "pending_annotation" for r in records),
        "partially_annotated": sum(r["annotation_completeness"] == "partial" for r in records),
        "partially_answerable": sum(r["answerability"] == "partially_answerable" for r in records),
        "unanswerable": sum(r["answerability"] == "unanswerable" for r in records),
        "blocked": sum(r["answerability"] == "blocked" for r in records),
        "out_of_scope": sum(r["answerability"] == "out_of_scope" for r in records),
        "conflicting_questions": sum(any(j["grade"] == -1 for j in r["judgments"]) for r in records),
        "multi_evidence_questions": sum(r["requires_multiple_chunks"] for r in records),
        "multi_source_questions": sum(len({j["source_id"] for j in r["judgments"] if j["grade"] >= 2}) >= 2
                                      for r in records),
        "questions_with_relevant": len(rel),
        "judgments": sum(len(r["judgments"]) for r in records),
        "relevant_judgments": sum(len(r["relevant_chunk_ids"]) for r in records),
        "unique_relevant_chunks": len({c for r in records for c in r["relevant_chunk_ids"]}),
        "unique_judged_chunks": len({j["chunk_id"] for r in records for j in r["judgments"]}),
        "unique_relevant_sources": len({s for r in records for s in r["expected_sources"]}),
        "grade_distribution": {str(k): grades[k] for k in sorted(grades)},
        "by_category": dict(Counter(r["query_category"] for r in records)),
        "by_complexity": dict(Counter(r["query_complexity"] for r in records)),
        "query_style": dict(Counter(s for r in records for s in r["query_style"])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    manifest_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    result = validate(args.dataset.read_text(encoding="utf-8").splitlines(), schema, load_manifest(MANIFEST),
                      manifest_sha)
    result["dataset_sha256"] = hashlib.sha256(args.dataset.read_bytes()).hexdigest()
    result["manifest_sha256"] = manifest_sha
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
