# ruff: noqa: E501  -- metric/report assembly lines are kept whole for readability of the evaluation rules
"""Exploratory dense-retrieval baseline on eval/datasets/retrieval_eval_v1.jsonl (SILVER labels).

OFFLINE by default: query vectors come only from the local cache (data/index/query_embeddings/). With
--allow-api, cache misses are embedded with Cohere (search_query) in ONE batch — only the Vietnamese
question texts are sent, never document content — and the call count is capped by --max-api-inputs.
Retrieval runs as the research reader through the authorized view (k = max k_probe = 20, sliced to 5/10/20).

Metric rules (see the T2.3.1 report):
  gold        = judged chunks with grade >= 2 that are retrievable now (authorization 2)
  unjudged    = never counted as irrelevant: precision and nDCG are reported as LOWER BOUNDS, plus
                judged-precision and judged-coverage
  groups      = answerable (main) | answerable_partial_pool | conflicting | unanswerable | refusal | out_of_scope
  main metrics only on the 'answerable' group; 95% bootstrap CI (seeded)

Outputs: metrics JSON, candidate-pool CSV (unjudged top-20 chunks), per-question JSONL in logs/retrieval/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import statistics
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect
from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import CohereEmbedder, EmbeddingProfile
from app.retrieval.query_embedding import CachedQueryEmbedder, CohereQueryEmbedder, cache_key
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalProfile

DATASET = ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl"
GAIN = {3: 3, 2: 2, 1: 1, 0: 0, -1: 2}  # schema x-metric-gain
KS = (5, 10, 20)


def group_of(r: dict) -> str:
    if r["answerability"] == "out_of_scope":
        return "out_of_scope"
    if r["answerability"] == "blocked":
        return "refusal"
    if r["answerability"] == "unanswerable":
        return "unanswerable"
    if any(j["grade"] == -1 for j in r["judgments"]):
        return "conflicting"
    if r["annotation_completeness"] == "partial":
        return "answerable_partial_pool"
    return "answerable"


def dcg(gains: list[float]) -> float:
    return sum(g / math.log2(i + 2) for i, g in enumerate(gains))


def question_metrics(ranked: list[str], judged: dict[str, int], retrievable: set[str],
                     ranked_sources: list[str] | None = None, gold_sources: set[str] | None = None) -> dict:
    gold = {c for c, g in judged.items() if g >= 2 and c in retrievable}
    ideal = sorted((GAIN[g] for c, g in judged.items() if c in retrievable and GAIN[g] > 0), reverse=True)
    out = {"gold": len(gold), "gold_not_retrievable": sum(1 for c, g in judged.items() if g >= 2 and c not in retrievable)}
    first = next((i + 1 for i, c in enumerate(ranked) if c in gold), None)
    out["mrr@20"] = 1 / first if first else 0.0
    out["first_relevant_rank"] = first
    for k in KS:
        top = ranked[:k]
        hits = sum(1 for c in top if c in gold)
        judged_in = sum(1 for c in top if c in judged)
        out[f"recall@{k}"] = hits / len(gold) if gold else None
        out[f"hit@{k}"] = 1.0 if hits else 0.0
        out[f"precision_lb@{k}"] = hits / k
        out[f"judged_precision@{k}"] = hits / judged_in if judged_in else None
        out[f"judged_coverage@{k}"] = judged_in / k
        idcg = dcg(ideal[:k])
        out[f"ndcg_lb@{k}"] = dcg([GAIN.get(judged.get(c), 0) if c in judged else 0 for c in top]) / idcg if idcg else None
    if ranked_sources is not None and gold_sources:
        for k in KS:  # source level: less sensitive to unjudged chunks of an already-relevant source
            got = set(ranked_sources[:k])
            out[f"source_hit@{k}"] = 1.0 if got & gold_sources else 0.0
            out[f"source_recall@{k}"] = len(got & gold_sources) / len(gold_sources)
    conflict = {c for c, g in judged.items() if g == -1 and c in retrievable}
    if conflict:
        out["conflict_coverage@20"] = sum(1 for c in ranked[:20] if c in conflict) / len(conflict)
    return out


def mean_ci(values: list[float], seed: int = 20261114, n: int = 2000) -> dict:
    vals = [v for v in values if v is not None]
    if not vals:
        return {"mean": None, "n": 0}
    rng = random.Random(seed)
    boots = sorted(statistics.fmean(rng.choices(vals, k=len(vals))) for _ in range(n))
    return {"mean": round(statistics.fmean(vals), 4), "ci95": [round(boots[int(0.025 * n)], 4),
                                                              round(boots[int(0.975 * n) - 1], 4)], "n": len(vals)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--allow-api", action="store_true")
    parser.add_argument("--max-api-inputs", type=int, default=0)
    parser.add_argument("--metrics-out", type=Path, default=REPORTS / "phase_6_2_t2_3_1_dense_retrieval_metrics_2026-11-14.json")
    parser.add_argument("--pool-out", type=Path, default=REPORTS / "phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    for p in (args.metrics_out, args.pool_out):
        if p.exists():
            raise SystemExit(f"{p} exists; refusing to overwrite (choose a new --*-out path)")

    rp = RetrievalProfile.load("dense_baseline_v1")
    ep = EmbeddingProfile.load(rp.embedding_profile)
    records = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]
    dataset_sha = hashlib.sha256(DATASET.read_bytes()).hexdigest()
    texts = [r["question_vi"].strip() for r in records]

    inner, client = None, None
    cache = CachedQueryEmbedder(ep, rp.query_cache_dir)
    missing = sorted({cache_key(ep, t) for t in texts if not (rp.query_cache_dir / f"{cache_key(ep, t)}.json").exists()})
    if missing:
        if not args.allow_api:
            raise SystemExit(f"{len(missing)} query vectors are not cached; re-run with --allow-api after approval")
        if len(missing) > args.max_api_inputs:
            raise SystemExit(f"{len(missing)} inputs would be sent, above --max-api-inputs={args.max_api_inputs}")
        client = CohereEmbedder(ep, os.environ.get("COHERE_API_KEY", ""))
        inner = CohereQueryEmbedder(ep, client)
        cache = CachedQueryEmbedder(ep, rp.query_cache_dir, inner)
    t0 = time.perf_counter()
    vectors = cache.embed_queries(texts)  # one batch for all cache misses
    embed_ms = (time.perf_counter() - t0) * 1000
    api_calls = client.calls if client else 0
    billed = client.billed_input_tokens if client else 0
    if client:
        client.close()

    with connect(rp.db_role, "dense_eval") as conn:  # type: ignore[arg-type]
        retrievable = {r[0] for r in conn.execute("SELECT chunk_id FROM v_research_retrieval_chunks")}
        conn.rollback()
    log = JsonlRetrievalLog(rp.log_dir, f"dense_eval_{datetime.now(UTC):%Y%m%dT%H%M%S}.jsonl")
    dense = DenseRetriever(rp, cache, ResearchVectorReader(rp), log=log)
    kmax = max(rp.k_probe)

    per_q, pool, db_ms, norms = [], [], [], []
    for r, text, vec in zip(records, texts, vectors, strict=True):
        qhash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        resp = dense.retrieve_by_vector(vec, k=kmax, question_id=r["question_id"], query_hash=qhash)
        db_ms.append(resp.latency_ms["db"])
        norms.append(math.sqrt(sum(x * x for x in vec)))
        ranked = [c.chunk_id for c in resp.results]
        judged = {j["chunk_id"]: j["grade"] for j in r["judgments"]}
        g = group_of(r)
        gold_sources = {j["source_id"] for j in r["judgments"] if j["grade"] >= 2 and j["chunk_id"] in retrievable}
        m = question_metrics(ranked, judged, retrievable, [c.source_id for c in resp.results], gold_sources)
        per_q.append({"question_id": r["question_id"], "group": g, "category": r["query_category"],
                      "authorization_version": resp.authorization_version,
                      "top1_cosine_similarity": round(resp.results[0].cosine_similarity, 4) if resp.results else None,
                      **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}})
        for c in resp.results:
            if c.chunk_id not in judged:
                prio = ("high" if c.rank <= 5 or (g in ("unanswerable", "refusal") and c.rank <= 10)
                        else "medium" if c.rank <= 10 else "low")
                pool.append({"question_id": r["question_id"], "question_group": g, "chunk_id": c.chunk_id,
                             "source_id": c.source_id, "rank": c.rank, "cosine_distance": round(c.score, 6),
                             "cosine_similarity": round(c.cosine_similarity, 6),
                             "current_annotation_status": "unjudged", "suggested_review_priority": prio})

    groups = Counter(q["group"] for q in per_q)
    metric_names = [f"{m}@{k}" for k in KS for m in ("recall", "hit", "precision_lb", "judged_precision",
                                                     "judged_coverage", "ndcg_lb", "source_hit",
                                                     "source_recall")] + ["mrr@20"]
    summary = {}
    for gname in ("answerable", "answerable_partial_pool", "conflicting"):
        qs = [q for q in per_q if q["group"] == gname]
        summary[gname] = {"questions": len(qs), **{m: mean_ci([q.get(m) for q in qs]) for m in metric_names}}
        if gname == "conflicting":
            summary[gname]["conflict_coverage@20"] = mean_ci([q.get("conflict_coverage@20") for q in qs])
    for gname in ("unanswerable", "refusal", "out_of_scope"):
        qs = [q for q in per_q if q["group"] == gname]
        summary[gname] = {"questions": len(qs), "top1_cosine_similarity": [q["top1_cosine_similarity"] for q in qs],
                          "question_ids": [q["question_id"] for q in qs]}
    ans_top1 = [q["top1_cosine_similarity"] for q in per_q if q["group"] == "answerable"]
    out = {
        "status": "exploratory_silver_baseline", "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "retrieval_profile": rp.code, "embedding_profile": ep.profile_code, "model_id": ep.model_id,
        "query_input_type": ep.query_input_type, "metric": "cosine (pgvector <=>), exact search, no ANN index",
        "query_expansion": False, "k_probe": list(KS), "dataset": DATASET.name, "dataset_sha256": dataset_sha,
        "label_tier": "silver_single_annotator (0 human-verified)", "authorization_version": per_q[0]["authorization_version"],
        "retrievable_chunks": len(retrievable), "questions_total": len(per_q), "groups": dict(groups),
        "api": {"calls": api_calls, "inputs_sent": len(missing) if inner else 0, "billed_input_tokens": billed,
                "cache_hits": cache.hits, "cache_misses": cache.misses},
        "query_vector_l2_norm": {"min": round(min(norms), 6), "max": round(max(norms), 6)},
        "latency_ms": {"embed_batch_total": round(embed_ms, 1), "db_per_query_median": round(statistics.median(db_ms), 1),
                       "db_per_query_p95": round(sorted(db_ms)[int(0.95 * len(db_ms)) - 1], 1),
                       "db_per_query_max": round(max(db_ms), 1)},
        "top1_similarity_answerable": {"median": round(statistics.median(ans_top1), 4), "min": min(ans_top1),
                                       "max": max(ans_top1)},
        "summary": summary, "per_question": per_q, "candidate_pool_rows": len(pool),
        "candidate_pool_by_priority": dict(Counter(p["suggested_review_priority"] for p in pool)),
        "log_file": str(log.path.relative_to(ROOT)),
    }
    args.metrics_out.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(args.pool_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pool[0]) if pool else ["question_id"])
        w.writeheader()
        w.writerows(pool)
    print(json.dumps({k: out[k] for k in ("groups", "api", "latency_ms", "candidate_pool_rows",
                                          "candidate_pool_by_priority", "query_vector_l2_norm")}, indent=1))
    print(json.dumps({g: {m: v for m, v in s.items() if m in ("questions", "recall@5", "recall@10", "recall@20",
                                                            "mrr@20", "ndcg_lb@10", "precision_lb@5")}
                      for g, s in summary.items() if g in ("answerable", "answerable_partial_pool", "conflicting")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
