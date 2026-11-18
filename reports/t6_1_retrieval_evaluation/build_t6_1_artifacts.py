"""Build T6.1 blinded annotation pools and unjudged offline fusion lists.

Reads only the frozen 66-query text, the T6.0 comparison CSV, and the authorized
research retrieval view. It deliberately does not read relevance/judgment fields.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

from app.db import connect

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "t6_1_retrieval_evaluation"
COMPARISON = ROOT / "reports" / "t6_0_hybrid_readiness" / "phase_3_retrieval_comparison.csv"
DATASET = ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl"
EXPECTED_USER = "asd_rag_v2_research_reader"
PROFILES = ("dense_baseline_v1", "fts_a_baseline_v1", "fts_b_glossary_and_v1",
            "fts_c_glossary_or_v1", "t5_7_exp1c_isolated")
FTS_PROFILES = PROFILES[1:]
K_VALUES = (20, 60, 100)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Select only query_id and question_vi; do not load benchmark judgment fields.
    questions = {}
    with DATASET.open(encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            questions[obj["question_id"]] = obj["question_vi"]

    with COMPARISON.open(encoding="utf-8-sig", newline="") as f:
        source_rows = list(csv.DictReader(f))
    for row in source_rows:
        row["candidate_k"] = int(row["candidate_k"])
        row["result_rank"] = int(row["result_rank"]) if row["result_rank"] else None
        row["score"] = float(row["score"]) if row["score"] else None

    # Keep core queries and the 12 accent variants separate.
    core = lambda qid: len(qid) == 4 and qid.startswith("q") and qid[1:].isdigit()
    core_rows = [r for r in source_rows if core(r["question_id"])]
    variant_rows = [r for r in source_rows if not core(r["question_id"])]
    if len({r["question_id"] for r in core_rows}) != 66:
        raise RuntimeError("Expected exactly 66 core query IDs")

    # Candidate provenance for the evaluator stays separate from the blinded sheet.
    grouped: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for r in core_rows:
        if r["status"] != "ok":
            continue
        qid, cid, profile = r["question_id"], r["chunk_id"], r["profile"]
        if profile not in PROFILES:
            continue
        rec = {"rank": r["result_rank"], "score_type": r["score_type"], "score": r["score"]}
        if cid in grouped[(qid, profile)]:
            raise RuntimeError(f"Duplicate {qid}/{profile}/{cid} in source results")
        grouped[(qid, profile)][cid] = rec
    all_pairs = sorted({(r["question_id"], r["chunk_id"]) for r in core_rows if r["status"] == "ok"})
    all_variant_pairs = sorted({(r["question_id"], r["chunk_id"]) for r in variant_rows if r["status"] == "ok"})
    all_ids = sorted({cid for _, cid in all_pairs + all_variant_pairs})

    sql = """SELECT chunk_id, source_id, document_id, title, source_url,
                     section_heading, section_path, page_start, page_end,
                     char_start, char_end, content, content_sha256,
                     chunking_profile, document_version, authorization_id, profile_code
              FROM asd_rag.v_research_retrieval_chunks
              WHERE chunk_id = ANY(%s)"""
    with connect("research_reader", "t6.1:read_candidate_metadata") as conn:
        conn.read_only = True
        user = conn.execute("SELECT current_user").fetchone()[0]
        if user != EXPECTED_USER:
            raise RuntimeError("Research reader identity mismatch")
        records = conn.execute(sql, (all_ids,)).fetchall()
    fields = ["chunk_id", "source_id", "document_id", "title", "source_url", "section_heading",
              "section_path", "page_start", "page_end", "char_start", "char_end", "content",
              "content_sha256", "chunking_profile", "document_version", "authorization_id", "profile_code"]
    metadata = {row[0]: dict(zip(fields, row, strict=True)) for row in records}
    missing = sorted(set(all_ids) - metadata.keys())
    if missing:
        raise RuntimeError(f"{len(missing)} candidate IDs are not visible in authorized view")
    for cid, rec in metadata.items():
        if not rec["content"] or hashlib.sha256(rec["content"].encode("utf-8")).hexdigest() != rec["content_sha256"]:
            raise RuntimeError(f"Content/hash validation failed for candidate {cid}")

    def annotation_rows(pairs: list[tuple[str, str]], seed: int) -> list[dict]:
        out = []
        for qid, cid in pairs:
            md = metadata[cid]
            qtext = questions.get(qid)
            if qtext is None:
                # Variant texts are sourced from the comparison artifact, not transformed here.
                qtext = next((r["query"] for r in source_rows if r["question_id"] == qid), None)
            if qtext is None:
                raise RuntimeError(f"Missing exact query text for {qid}")
            anon = "ann_" + hashlib.sha256((qid + "\0" + cid).encode()).hexdigest()[:16]
            out.append({
                "annotation_id": anon, "query_id": qid, "query_text": qtext,
                "chunk_id": cid, "source_id": md["source_id"], "document_title": md["title"],
                "section": md["section_heading"] or " > ".join(md["section_path"] or []),
                "page_start": md["page_start"], "page_end": md["page_end"],
                "content": md["content"], "content_sha256": md["content_sha256"],
                "relevance_grade": "", "evidence_type": "", "evidence_span": "", "rationale": "",
                "annotator_id": "", "review_status": "PENDING_HUMAN_REVIEW",
                "disagreement_reason": "", "contradiction_flag": "", "context_limitation": "",
                "adjudication_grade": "",
            })
        rng = random.Random(seed)
        by_query: dict[str, list[dict]] = defaultdict(list)
        for item in out:
            by_query[item["query_id"]].append(item)
        query_ids = sorted(by_query)
        rng.shuffle(query_ids)
        ordered = []
        for qid in query_ids:
            rng.shuffle(by_query[qid])
            ordered.extend(by_query[qid])
        return ordered

    ann_fields = ["annotation_id", "query_id", "query_text", "chunk_id", "source_id", "document_title",
                  "section", "page_start", "page_end", "content", "content_sha256", "relevance_grade",
                  "evidence_type", "evidence_span", "rationale", "annotator_id", "review_status",
                  "disagreement_reason", "contradiction_flag", "context_limitation", "adjudication_grade"]
    core_pool = annotation_rows(all_pairs, 6101)
    variant_pool = annotation_rows(all_variant_pairs, 6101)
    write_csv(OUT / "human_annotation_pool_core.csv", ann_fields, core_pool)
    write_csv(OUT / "human_annotation_pool_diacritic_variants.csv", ann_fields, variant_pool)
    for label, seed in (("annotator_1", 6101), ("annotator_2", 6102)):
        write_csv(OUT / f"human_annotation_sheet_{label}_core.csv", ann_fields,
                  annotation_rows(all_pairs, seed))
        write_csv(OUT / f"human_annotation_sheet_{label}_diacritic_variants.csv", ann_fields,
                  annotation_rows(all_variant_pairs, seed))

    # Evaluator-only mapping; do not give to annotators. No relevance values are read or produced.
    provenance = []
    for qid, cid in all_pairs:
        md = metadata[cid]
        hit_profiles = [p for p in PROFILES if cid in grouped[(qid, p)]]
        ranks = {p: grouped[(qid, p)][cid]["rank"] for p in hit_profiles}
        scores = {p: {"type": grouped[(qid, p)][cid]["score_type"],
                      "value": grouped[(qid, p)][cid]["score"]} for p in hit_profiles}
        provenance.append({"query_id": qid, "chunk_id": cid, "retrievers": hit_profiles,
                           "ranks": ranks, "raw_scores": scores, "source_id": md["source_id"],
                           "content_sha256": md["content_sha256"]})
    (OUT / "candidate_pool_provenance_map.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")

    # Per-combination, rank-only RRF; profile and c are explicit. No labeled metric is computed.
    fused = []
    for fts in FTS_PROFILES:
        for c in K_VALUES:
            for qid in sorted({r["question_id"] for r in core_rows}):
                dense = grouped[(qid, "dense_baseline_v1")]
                sparse = grouped[(qid, fts)]
                union = set(dense) | set(sparse)
                scored = []
                for cid in union:
                    score = (1 / (c + dense[cid]["rank"]) if cid in dense else 0.0) + \
                            (1 / (c + sparse[cid]["rank"]) if cid in sparse else 0.0)
                    scored.append((score, cid))
                scored.sort(key=lambda x: (-x[0], x[1]))
                for rank, (score, cid) in enumerate(scored[:10], 1):
                    fused.append({"query_id": qid, "dense_profile": "dense_baseline_v1",
                                  "fts_profile": fts, "rrf_c": c, "rank": rank,
                                  "chunk_id": cid, "rrf_score": f"{score:.12f}",
                                  "dense_rank": dense.get(cid, {}).get("rank", ""),
                                  "fts_rank": sparse.get(cid, {}).get("rank", ""),
                                  "source_id": metadata[cid]["source_id"]})
    write_csv(OUT / "offline_rrf_top10.csv",
              ["query_id", "dense_profile", "fts_profile", "rrf_c", "rank", "chunk_id", "rrf_score",
               "dense_rank", "fts_rank", "source_id"], fused)

    variants = []
    for r in variant_rows:
        variants.append({"query_id": r["question_id"], "retriever": r["profile"],
                         "rank": r["result_rank"] or "", "chunk_id": r["chunk_id"],
                         "score_type": r["score_type"], "score": r["score"] or "",
                         "status": r["status"], "query": r["query"]})
    write_csv(OUT / "diacritic_variant_candidates.csv",
              ["query_id", "retriever", "rank", "chunk_id", "score_type", "score", "status", "query"], variants)

    summary = {
        "status": "PENDING_HUMAN_REVIEW",
        "core_queries": len({q for q, _ in all_pairs}),
        "core_query_chunk_pairs": len(all_pairs),
        "unique_core_chunks": len({cid for _, cid in all_pairs}),
        "diacritic_variant_query_ids": len({q for q, _ in all_variant_pairs}),
        "diacritic_variant_query_chunk_pairs": len(all_variant_pairs),
        "diacritic_variant_unique_chunks": len({cid for _, cid in all_variant_pairs}),
        "unique_chunks_fetched_from_authorized_view": len(metadata),
        "candidate_ids_missing_from_authorized_view": len(missing),
        "core_candidate_occurrences_by_retriever": {p: sum(len(grouped[(q, p)]) for q in questions)
                                                     for p in PROFILES},
        "dense_queries_with_cached_vectors": 66,
        "external_embedding_calls": 0,
        "database_writes": 0,
        "benchmark_relevance_fields_used": False,
        "retrieval_relevance_metrics_computed": False,
        "rrf_runs": len({r["query_id"] for r in fused}) * len(FTS_PROFILES) * len(K_VALUES),
        "provenance_map_is_annotator_facing": False,
        "builder_script_sha256": sha(Path(__file__)),
        "input_sha256": {"retrieval_eval_v1.jsonl": sha(DATASET),
                         "phase_3_retrieval_comparison.csv": sha(COMPARISON)},
    }
    (OUT / "artifact_build_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
