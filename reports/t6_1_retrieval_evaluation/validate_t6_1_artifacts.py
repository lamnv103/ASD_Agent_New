"""Structural/integrity validation for T6.1 human pool and offline RRF artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "t6_1_retrieval_evaluation"
DATASET = ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl"
COMPARISON = ROOT / "reports" / "t6_0_hybrid_readiness" / "phase_3_retrieval_comparison.csv"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # Only select query ID/text from benchmark objects; no judgment fields are used.
    questions = {}
    for line in DATASET.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        questions[row["question_id"]] = row["question_vi"]
    source = read_csv(COMPARISON)
    core_ids = {r["question_id"] for r in source if re.fullmatch(r"q\d{3}", r["question_id"])}
    assert core_ids == set(questions) and len(core_ids) == 66
    assert all(next(r["query"] for r in source if r["question_id"] == q) == text
               for q, text in questions.items())

    core_pair_sets = []
    forbidden = ("retriever", "rank", "score", "stratum", "profile", "tsquery", "latency")
    for name in ("human_annotation_sheet_annotator_1_core.csv", "human_annotation_sheet_annotator_2_core.csv"):
        rows = read_csv(OUT / name)
        pairs = {(r["query_id"], r["chunk_id"]) for r in rows}
        core_pair_sets.append(pairs)
        assert len(rows) == len(pairs) == 1631
        assert {r["query_id"] for r in rows} == core_ids
        assert not any(any(term in field.lower() for term in forbidden) for field in rows[0])
        assert all(not r["relevance_grade"] and not r["evidence_span"] and not r["rationale"]
                   and not r["annotator_id"] and r["review_status"] == "PENDING_HUMAN_REVIEW" for r in rows)
        assert all(hashlib.sha256(r["content"].encode("utf-8")).hexdigest() == r["content_sha256"]
                   for r in rows)
    assert core_pair_sets[0] == core_pair_sets[1]

    variant_pair_sets = []
    for name in ("human_annotation_sheet_annotator_1_diacritic_variants.csv",
                 "human_annotation_sheet_annotator_2_diacritic_variants.csv"):
        rows = read_csv(OUT / name)
        pairs = {(r["query_id"], r["chunk_id"]) for r in rows}
        variant_pair_sets.append(pairs)
        assert len(rows) == len(pairs) == 230
        assert len({r["query_id"] for r in rows}) == 12
        assert not any(any(term in field.lower() for term in forbidden) for field in rows[0])
        assert all(not r["relevance_grade"] and r["review_status"] == "PENDING_HUMAN_REVIEW" for r in rows)
        assert all(hashlib.sha256(r["content"].encode("utf-8")).hexdigest() == r["content_sha256"]
                   for r in rows)
    assert variant_pair_sets[0] == variant_pair_sets[1]

    provenance = json.loads((OUT / "candidate_pool_provenance_map.json").read_text(encoding="utf-8"))
    assert {(r["query_id"], r["chunk_id"]) for r in provenance} == core_pair_sets[0]
    rrf = read_csv(OUT / "offline_rrf_top10.csv")
    assert len(rrf) == 7920
    combos = {(r["fts_profile"], r["rrf_c"], r["query_id"]) for r in rrf}
    assert len(combos) == 792
    for combo in combos:
        rows = [r for r in rrf if (r["fts_profile"], r["rrf_c"], r["query_id"]) == combo]
        assert [int(r["rank"]) for r in rows] == list(range(1, 11))

    manifest = json.loads((OUT / "phase_0_input_sha256.json").read_text(encoding="utf-8"))
    assert all(sha(ROOT / name) == digest for name, digest in manifest.items())
    result = {
        "status": "PASS_STRUCTURAL_VALIDATION",
        "core_query_ids": len(core_ids),
        "core_pairs_per_annotator": len(core_pair_sets[0]),
        "variant_query_ids": 12,
        "variant_pairs_per_annotator": len(variant_pair_sets[0]),
        "annotation_fields_blinded": True,
        "grades_and_evidence_blank": True,
        "content_hashes_match": True,
        "annotators_have_same_pair_sets": True,
        "rrf_top10_rows": len(rrf),
        "rrf_query_config_runs": len(combos),
        "input_hashes_match": True,
        "human_reviews_performed": False,
        "relevance_metrics_computed": False,
    }
    (OUT / "artifact_validation_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
