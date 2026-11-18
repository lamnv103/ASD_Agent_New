# ruff: noqa: E501  -- metric/report assembly lines are kept whole for readability of the evaluation rules
"""Phase 6.2 T2.3.3 — dense retrieval evaluation on a FROZEN cohort, original vs merged labels (evaluation only).

Reuses the T2.3.1 retriever unchanged (profile dense_baseline_v1, research reader role, authorized view,
k = 20) with query vectors from the local cache ONLY: the cached embedder has no API client, so a cache miss
aborts the run. Nothing is written to the database. Also reads (as the research reader, read-only):
a fingerprint of the view (+ catalog privileges/role attributes/table write counters) before and after.

Runs
  A = original labels  (eval/datasets/retrieval_eval_v1.jsonl)            — comparable with T2.3.1
  B = merged labels    (eval/datasets/retrieval_eval_v1_merged_2026-11-14.jsonl) — +95 relevant labels that ALL come
      from the dense top-20 pool → biased towards dense; never a fair basis for a dense-vs-FTS comparison.
Cohort = T2.3.1 groups (…_metrics_2026-11-14_r2.json), never re-derived from the merged file.

Metric definitions: see METRIC_DEFINITIONS below and the T2.3.3 report.
Usage: python -B scripts/dense_eval_t2_3_3.py [--tag 2026-11-15] [--check]
  --check  recompute everything and compare with the files already written (ignores timestamps/latency).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import statistics
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect
from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import EmbeddingProfile
from app.retrieval.query_embedding import CachedQueryEmbedder
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalProfile

DS = ROOT / "eval" / "datasets"
ORIGINAL = DS / "retrieval_eval_v1.jsonl"
MERGED = DS / "retrieval_eval_v1_merged_2026-11-14.jsonl"
JUDGMENTS = DS / "retrieval_eval_v1_candidate_judgments_2026-11-14.jsonl"
ADJUDICATIONS = REPORTS / "phase_6_2_t2_3_2_unresolved_adjudications_2026-11-14.csv"
T231_METRICS = REPORTS / "phase_6_2_t2_3_1_dense_retrieval_metrics_2026-11-14_r2.json"
EXPECTED_SHA = {ORIGINAL.name: "7704bb510c9ab4a545d9195b18ffa2dc32f10b705df909a9201e11c96f104c2b",
                MERGED.name: "6bd3ad7868f9fc2aa5c8079c4d7d14116a06c721ec55537b466a9960a3eae7ab"}
CODE = ["app/retrieval/dense.py", "app/retrieval/research_reader.py", "app/retrieval/query_embedding.py",
        "app/retrieval/types.py", "app/retrieval/embeddings.py", "config/retrieval_profiles.json",
        "config/embedding_profiles.json", "scripts/dense_retrieval_eval.py", "scripts/dense_eval_t2_3_3.py"]
KS = (5, 10, 20)
NDCG_GAIN = {3: 7, 2: 3, 1: 1, 0: 0}  # exponential 2^g - 1; grade -1 has NO gain (reported as conflict coverage)
ROLES = ("asd_rag_v2_owner", "asd_rag_v2_ingest", "asd_rag_v2_app", "asd_rag_v2_research_reader")
PRIVS = ("SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE")
VOLATILE = {"generated_at", "latency_ms", "log_file"}

METRIC_DEFINITIONS = {
    "relevant set R": "judged chunks with grade >= 2 that are retrievable now (authorization 2). Grade -1 is not in R; grade 1 is not in R",
    "recall@K": "|top-K ∩ R| / |R|; denominator = KNOWN relevant only (unpooled relevant chunks unknown) → recall w.r.t. the judged set, not a bound on true recall",
    "hit@K": "1 if top-K ∩ R ≠ ∅",
    "precision_lb@K": "|top-K ∩ R| / |top-K|; unjudged counted as not relevant → LOWER bound",
    "precision_ub@K": "(|top-K ∩ R| + unjudged in top-K) / |top-K|; every unjudged counted relevant → UPPER bound",
    "judged_precision@K": "|top-K ∩ R| / |judged in top-K| (judged-only precision; None if nothing judged)",
    "mrr": "1 / rank of first chunk in R within top-20 (0 if none) — LOWER bound; mrr_ub = 1 / rank of first chunk that is in R OR unjudged",
    "unjudged_before_first_relevant": "number of unjudged chunks ranked above the first relevant one (MRR sensitivity)",
    "ndcg@K": "DCG with gain 3→7, 2→3, 1→1, 0→0, unjudged→0, -1→0 (and excluded from the ideal); IDCG from all judged retrievable chunks; LOWER bound",
    "ndcg_t231_lb@K": "T2.3.1 definition (linear gain 3,2,1,0, -1→2) — kept only for comparability",
    "source_recall@K": "|distinct source_id in top-K ∩ S| / |S|, S = distinct source_id of R (deduplicated by source)",
    "document_recall@K": "same with document_id",
    "judged_coverage@K": "judged chunks in top-K / |top-K| (judged = any final grade -1..3 in that label set); micro = Σjudged/Σretrieved, macro = mean of per-question values",
    "unjudged_rate@K": "1 - judged_coverage@K",
    "conflict_coverage@20": "grade -1 chunks in top-20 / grade -1 retrievable chunks (conflict aspect only)",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dir_sha(path: Path) -> dict:
    files = sorted(p for p in path.iterdir() if p.is_file())
    h = hashlib.sha256()
    for p in files:
        h.update(p.name.encode() + b"\0" + p.read_bytes() + b"\0")
    return {"files": len(files), "sha256": h.hexdigest()}


def load_jsonl(path: Path) -> dict[str, dict]:
    return {r["question_id"]: r for r in (json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip())}


def t231_module():
    spec = importlib.util.spec_from_file_location("dense_retrieval_eval", ROOT / "scripts" / "dense_retrieval_eval.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reader_fingerprint() -> dict:
    """Read-only, research reader role only: view content/vector hash + catalog privileges + write counters."""
    with connect("research_reader", "t2_3_3_fingerprint") as conn:
        conn.read_only = True
        user = conn.execute("SELECT current_user").fetchone()[0]
        n, nd, auth, digest = conn.execute(
            "SELECT count(*), count(DISTINCT chunk_id), array_agg(DISTINCT authorization_id ORDER BY authorization_id), "
            "md5(string_agg(chunk_id || '|' || content_sha256 || '|' || authorization_id || '|' || profile_code || '|' "
            "|| model_id || '|' || vector_dimension || '|' || md5(embedding::text), ',' ORDER BY chunk_id)) "
            "FROM asd_rag.v_research_retrieval_chunks").fetchone()
        rels = conn.execute("SELECT c.oid, c.relname, c.relkind FROM pg_class c JOIN pg_namespace s ON s.oid = c.relnamespace "
                            "WHERE s.nspname = 'asd_rag' AND c.relkind IN ('r','v','m','p') ORDER BY c.relname").fetchall()
        privs = []
        for oid, name, _kind in rels:
            for role in ROLES:
                row = conn.execute("SELECT " + ", ".join(f"has_table_privilege(%(r)s, %(o)s::oid, '{p}')" for p in PRIVS),
                                   {"r": role, "o": oid}).fetchone()
                privs.append(f"{name}|{role}|" + "".join("1" if x else "0" for x in row))
        roles = conn.execute("SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin, rolconnlimit, "
                             "coalesce(array_to_string(rolconfig, ';'), '') FROM pg_roles WHERE rolname = ANY(%(r)s) "
                             "ORDER BY rolname", {"r": list(ROLES)}).fetchall()
        stats = conn.execute("SELECT relname, n_live_tup, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_all_tables "
                             "WHERE schemaname = 'asd_rag' ORDER BY relname").fetchall()
        conn.rollback()
    return {"session_user": user, "view_rows": n, "view_distinct_chunks": nd, "authorization_ids": list(auth),
            "view_content_vector_md5": digest, "relations": len(rels),
            "privilege_matrix_sha256": hashlib.sha256("\n".join(privs).encode()).hexdigest(), "privilege_entries": len(privs),
            "role_attributes": [list(map(str, r)) for r in roles],
            "table_write_counters": {r[0]: {"n_live_tup": r[1], "ins": r[2], "upd": r[3], "del": r[4]} for r in stats}}


def ranked_lists(rp: RetrievalProfile, records: dict[str, dict], log_name: str) -> tuple[dict, dict, dict]:
    ep = EmbeddingProfile.load(rp.embedding_profile)
    cache = CachedQueryEmbedder(ep, rp.query_cache_dir)  # no inner embedder → a cache miss raises, never calls an API
    qids = sorted(records)
    vectors = cache.embed_queries([records[q]["question_vi"].strip() for q in qids])
    log = JsonlRetrievalLog(rp.log_dir, log_name)
    dense = DenseRetriever(rp, cache, ResearchVectorReader(rp), log=log)
    ranked, db_ms = {}, []
    for q, vec in zip(qids, vectors, strict=True):
        qhash = hashlib.sha256(records[q]["question_vi"].strip().encode("utf-8")).hexdigest()
        resp = dense.retrieve_by_vector(vec, k=max(KS), question_id=q, query_hash=qhash)
        db_ms.append(resp.latency_ms["db"])
        ranked[q] = [{"rank": c.rank, "chunk_id": c.chunk_id, "source_id": c.source_id, "document_id": c.document_id,
                      "cosine_distance": round(c.score, 6), "authorization_version": resp.authorization_version}
                     for c in resp.results]
    api = {"api_client": None, "calls": 0, "cache_hits": cache.hits, "cache_misses": cache.misses}
    return ranked, api, {"db_per_query_median": round(statistics.median(db_ms), 1), "log_file": str(log.path.relative_to(ROOT))}


def question_metrics(ranked: list[dict], record: dict, retrievable: set[str], t231) -> dict:
    judged = {j["chunk_id"]: j for j in record["judgments"]}
    grade = {c: j["grade"] for c, j in judged.items()}
    R = {c for c, g in grade.items() if g >= 2 and c in retrievable}
    S = {judged[c]["source_id"] for c in R}
    D = {judged[c]["document_id"] for c in R}
    conflict = {c for c, g in grade.items() if g == -1 and c in retrievable}
    ideal = sorted((NDCG_GAIN[g] for c, g in grade.items() if c in retrievable and g >= 0 and NDCG_GAIN[g] > 0), reverse=True)
    ids = [x["chunk_id"] for x in ranked]
    out = {"relevant_known": len(R), "relevant_sources": len(S), "relevant_not_retrievable": sum(1 for c, g in grade.items() if g >= 2 and c not in retrievable),
           "conflict_known": len(conflict), "returned": len(ids)}
    first = next((i + 1 for i, c in enumerate(ids) if c in R), None)
    first_ub = next((i + 1 for i, c in enumerate(ids) if c in R or c not in grade), None)
    out["first_relevant_rank"] = first
    out["mrr"] = 1 / first if first else 0.0
    out["mrr_ub"] = 1 / first_ub if first_ub else 0.0
    out["unjudged_before_first_relevant"] = sum(1 for c in ids[: (first or len(ids) + 1) - 1] if c not in grade)
    for k in KS:
        top = ids[:k]
        n = len(top)
        hits = sum(1 for c in top if c in R)
        judged_in = sum(1 for c in top if c in grade)
        unj = n - judged_in
        out[f"retrieved@{k}"] = n
        out[f"judged@{k}"] = judged_in
        out[f"unjudged@{k}"] = unj
        out[f"judged_coverage@{k}"] = judged_in / n if n else None
        out[f"unjudged_rate@{k}"] = unj / n if n else None
        out[f"relevant_retrieved@{k}"] = hits
        out[f"grade1_retrieved@{k}"] = sum(1 for c in top if grade.get(c) == 1)
        out[f"grade0_retrieved@{k}"] = sum(1 for c in top if grade.get(c) == 0)
        out[f"conflict_retrieved@{k}"] = sum(1 for c in top if grade.get(c) == -1)
        out[f"recall@{k}"] = hits / len(R) if R else None
        out[f"hit@{k}"] = (1.0 if hits else 0.0) if R else None
        out[f"precision_lb@{k}"] = hits / n if n else None
        out[f"precision_ub@{k}"] = (hits + unj) / n if n else None
        out[f"judged_precision@{k}"] = hits / judged_in if judged_in else None
        idcg = t231.dcg(ideal[:k])
        out[f"ndcg@{k}"] = (t231.dcg([NDCG_GAIN.get(grade[c], 0) if c in grade and grade[c] >= 0 else 0 for c in top]) / idcg) if idcg else None
        srcs = {x["source_id"] for x in ranked[:k]}
        docs = {x["document_id"] for x in ranked[:k]}
        out[f"source_recall@{k}"] = len(srcs & S) / len(S) if S else None
        out[f"source_hit@{k}"] = (1.0 if srcs & S else 0.0) if S else None
        out[f"document_recall@{k}"] = len(docs & D) / len(D) if D else None
    out["conflict_coverage@20"] = (sum(1 for c in ids[:20] if c in conflict) / len(conflict)) if conflict else None
    # T2.3.1-identical computation (for the reproduction check and continuity)
    old = t231.question_metrics(ids, grade, retrievable, [x["source_id"] for x in ranked],
                                {judged[c]["source_id"] for c in grade if grade[c] >= 2 and c in retrievable})
    for k in KS:
        out[f"ndcg_t231_lb@{k}"] = old[f"ndcg_lb@{k}"]
    out["_t231"] = old
    return out


SUMMARY_METRICS = ([f"{m}@{k}" for k in KS for m in ("recall", "hit", "precision_lb", "precision_ub", "judged_precision", "ndcg",
                                                      "ndcg_t231_lb", "source_recall", "source_hit", "document_recall",
                                                      "judged_coverage", "unjudged_rate")] + ["mrr", "mrr_ub", "unjudged_before_first_relevant"])


def summarize(per_q: list[dict], cohort: list[str], t231) -> dict:
    rows = [p for p in per_q if p["question_id"] in cohort]
    out = {"questions": len(rows), "question_ids": [p["question_id"] for p in rows]}
    for m in SUMMARY_METRICS:
        out[m] = t231.mean_ci([p.get(m) for p in rows])
    for k in KS:
        tot, jud = sum(p[f"retrieved@{k}"] for p in rows), sum(p[f"judged@{k}"] for p in rows)
        out[f"judged_coverage_micro@{k}"] = round(jud / tot, 4) if tot else None
        out[f"retrieved_total@{k}"], out[f"judged_total@{k}"], out[f"unjudged_total@{k}"] = tot, jud, tot - jud
    cc = [p["conflict_coverage@20"] for p in rows if p["conflict_coverage@20"] is not None]
    if cc:
        out["conflict_coverage@20"] = t231.mean_ci(cc)
    return out


def evaluate(label: str, records: dict[str, dict], ranked: dict, retrievable: set[str], cohorts: dict[str, str], t231) -> tuple[dict, list[dict]]:
    per_q = []
    for q in sorted(records):
        m = question_metrics(ranked[q], records[q], retrievable, t231)
        m.pop("_t231")
        per_q.append({"question_id": q, "run": label, "cohort": cohorts[q], **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}})
    summary = {}
    for g in ("answerable", "answerable_partial_pool", "conflicting"):
        summary[g] = summarize(per_q, [q for q in sorted(records) if cohorts[q] == g], t231)
    summary["all_answerable_like"] = summarize(per_q, [q for q in sorted(records) if cohorts[q] in ("answerable", "answerable_partial_pool", "conflicting")], t231)
    for g in ("unanswerable", "refusal", "out_of_scope"):
        qs = [p for p in per_q if p["cohort"] == g]
        summary[g] = {"questions": len(qs), "question_ids": [p["question_id"] for p in qs],
                      "relevant_known": {p["question_id"]: p["relevant_known"] for p in qs},
                      "top1_cosine_similarity": {q: round(1 - ranked[q][0]["cosine_distance"], 4) for q in (p["question_id"] for p in qs)},
                      **{f"judged_coverage@{k}": {p["question_id"]: p[f"judged_coverage@{k}"] for p in qs} for k in KS}}
    return summary, per_q


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default="2026-11-15")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    t231 = t231_module()
    out = {n: REPORTS / f"{n}_{args.tag}.{ext}" for n, ext in (
        ("dense_eval_frozen_cohort_manifest", "csv"), ("dense_eval_original_metrics", "json"), ("dense_eval_merged_metrics", "json"),
        ("dense_eval_per_question_metrics", "csv"), ("dense_eval_judged_coverage", "csv"), ("dense_eval_run_record", "json"))}
    if not args.check and any(p.exists() for p in out.values()):
        raise SystemExit("output files exist; refusing to overwrite (use --check to compare, or a new --tag)")

    # ---- inputs + immutability preconditions
    inputs = {p.name: sha(p) for p in (ORIGINAL, MERGED, JUDGMENTS, ADJUDICATIONS, T231_METRICS)}
    for name, expected in EXPECTED_SHA.items():
        if inputs[name] != expected:
            raise SystemExit(f"{name} changed (sha {inputs[name][:12]} != {expected[:12]}); stop")
    code = {c: sha(ROOT / c) for c in CODE}
    rp = RetrievalProfile.load("dense_baseline_v1")
    cache_before = dir_sha(ROOT / rp.query_cache_dir)
    original, merged = load_jsonl(ORIGINAL), load_jsonl(MERGED)
    t231m = json.loads(T231_METRICS.read_text(encoding="utf-8"))
    cohorts = {p["question_id"]: p["group"] for p in t231m["per_question"]}

    # ---- R1 frozen cohort + consistency (stop on any mismatch)
    problems = []
    if set(cohorts) != set(original) or set(original) != set(merged) or len(cohorts) != 66:
        problems.append("question sets differ between T2.3.1, original and merged")
    for q, r in original.items():
        if t231.group_of(r) != cohorts.get(q):
            problems.append(f"{q}: group_of(original)={t231.group_of(r)} but T2.3.1 cohort={cohorts.get(q)}")
        if merged[q]["answerability"] != r["answerability"]:
            problems.append(f"{q}: answerability differs between original and merged")
    if Counter(cohorts.values()) != Counter(t231m["groups"]):
        problems.append("T2.3.1 per-question groups do not match its group counts")
    if problems:
        print(json.dumps({"stop": problems}, ensure_ascii=False, indent=1))
        return 1
    with open(ADJUDICATIONS, encoding="utf-8-sig") as f:
        adj = Counter(r["question_id"] for r in csv.DictReader(f) if r["item_type"] == "chunk_judgment")
    manifest_rows = [{"question_id": q, "cohort_t2_3_1": cohorts[q], "answerability": original[q]["answerability"],
                      "expected_evidence_status": original[q]["expected_evidence_status"],
                      "adjudication_status": (f"pending ({adj[q]} chunk)" + ("; answerability label pending" if q == "q057" else "")) if adj[q] else "none",
                      "group_if_rederived_from_merged": t231.group_of(merged[q]),
                      "dataset_version_original": f"retrieval_eval_v1@{inputs[ORIGINAL.name][:12]}",
                      "dataset_version_merged": f"retrieval_eval_v1_merged_2026-11-14@{inputs[MERGED.name][:12]}"} for q in sorted(original)]
    manifest_text = "".join(",".join(f'"{v}"' if "," in str(v) else str(v) for v in row.values()) + "\n" for row in manifest_rows)
    manifest_text = ",".join(manifest_rows[0]) + "\n" + manifest_text

    # ---- DB fingerprint before, retrieval, fingerprint after
    fp_before = reader_fingerprint()
    ranked, api, run_info = ranked_lists(rp, original, f"dense_eval_t2_3_3_{datetime.now(UTC):%Y%m%dT%H%M%S}.jsonl")
    with connect(rp.db_role, "t2_3_3_retrievable") as conn:
        conn.read_only = True
        retrievable = {r[0] for r in conn.execute("SELECT chunk_id FROM asd_rag.v_research_retrieval_chunks")}
        conn.rollback()
    fp_after = reader_fingerprint()
    cache_after = dir_sha(ROOT / rp.query_cache_dir)
    if api["cache_misses"] or api["cache_hits"] != 66:
        raise SystemExit(f"query cache not fully used: {api}")

    # ---- reproduction of T2.3.1 ranked lists + T2.3.1 metrics with original labels
    t231_log = [json.loads(x) for x in (ROOT / t231m["log_file"].replace("\\", "/")).read_text(encoding="utf-8").splitlines() if x.strip()]
    t231_rank = {r["question_id"]: [x["chunk_id"] for x in r["returned"]] for r in t231_log}
    t231_dist = {r["question_id"]: [x["cosine_distance"] for x in r["returned"]] for r in t231_log}
    same_lists = sum(t231_rank[q] == [x["chunk_id"] for x in ranked[q]] for q in ranked)
    max_dist_diff = max(abs(a - b["cosine_distance"]) for q in ranked for a, b in zip(t231_dist[q], ranked[q], strict=True))
    old_pq = {p["question_id"]: p for p in t231m["per_question"]}
    metric_mismatch = []
    for q in sorted(original):
        old = question_metrics(ranked[q], original[q], retrievable, t231)["_t231"]
        for k, v in old.items():
            if k in old_pq[q] and isinstance(v, float) and abs(round(v, 4) - old_pq[q][k]) > 1e-4:
                metric_mismatch.append(f"{q}:{k}")
    reproduction = {"t231_log": t231m["log_file"], "identical_ranked_lists": f"{same_lists}/{len(ranked)}",
                    "max_abs_cosine_distance_diff": round(max_dist_diff, 9), "t231_metric_mismatches": metric_mismatch}

    # ---- runs A and B
    sum_a, pq_a = evaluate("A_original", original, ranked, retrievable, cohorts, t231)
    sum_b, pq_b = evaluate("B_merged", merged, ranked, retrievable, cohorts, t231)

    # ---- q057 sensitivity (no dataset change: hypothetical label kept in memory only)
    q057_chunk = next(r["chunk_id"] for r in (json.loads(x) for x in JUDGMENTS.read_text(encoding="utf-8").splitlines())
                      if r["question_id"] == "q057" and r["status"] == "needs_adjudication")
    hyp = json.loads(json.dumps(merged["q057"]))
    m = next(r for r in (json.loads(x) for x in JUDGMENTS.read_text(encoding="utf-8").splitlines()) if r["chunk_id"] == q057_chunk and r["question_id"] == "q057")
    hyp["judgments"].append({k: m[k] for k in ("chunk_id", "document_id", "source_id", "content_sha256")} | {"grade": 2})
    q057_hyp = question_metrics(ranked["q057"], hyp, retrievable, t231)
    q057_hyp.pop("_t231")
    sens = {}
    for name, extra in (("H_unanswerable_as_labelled", None), ("H_answerable_hypothetical_grade2", q057_hyp)):
        for run, pq in (("A_original", pq_a), ("B_merged", pq_b)):
            rows = [p for p in pq if p["cohort"] == "answerable"] + ([{"question_id": "q057", **extra}] if extra else [])
            sens[f"{name}|{run}"] = {"questions": len(rows), **{m_: t231.mean_ci([p.get(m_) for p in rows])["mean"] for m_ in
                                     ("recall@5", "recall@10", "recall@20", "hit@5", "hit@10", "hit@20", "mrr", "ndcg@10", "judged_coverage@10")}}
    q057_info = {"chunk_id": q057_chunk, "rank_in_top20": next((x["rank"] for x in ranked["q057"] if x["chunk_id"] == q057_chunk), None),
                 "top1_cosine_similarity": round(1 - ranked["q057"][0]["cosine_distance"], 4), "hypothetical_metrics": {k: q057_hyp[k] for k in ("recall@5", "recall@10", "mrr", "ndcg@10", "judged_coverage@10")},
                 "sensitivity": sens}

    # ---- assemble outputs
    unchanged = {"query_cache_identical": cache_before == cache_after, "db_fingerprint_identical": fp_before == fp_after,
                 "original_dataset_sha_unchanged": sha(ORIGINAL) == EXPECTED_SHA[ORIGINAL.name],
                 "merged_dataset_sha_unchanged": sha(MERGED) == EXPECTED_SHA[MERGED.name]}
    common = {"task": "T2.3.3 dense evaluation (evaluation only)", "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
              "retrieval_profile": rp.code, "k": max(KS), "k_probe": list(KS), "query_expansion": False,
              "inputs_sha256": inputs, "code_sha256": code, "query_cache": cache_before, "api": api,
              "cohort_source": T231_METRICS.name, "cohort_counts": dict(Counter(cohorts.values())),
              "manifest_sha256": hashlib.sha256(manifest_text.encode()).hexdigest(),
              "metric_definitions": METRIC_DEFINITIONS, "ndcg_gain": {str(k): v for k, v in NDCG_GAIN.items()} | {"-1": "no gain; see conflict_coverage@20"},
              "bootstrap": "95% CI, 2000 resamples, seed 20261114 (as T2.3.1)", "retrievable_chunks": len(retrievable)}
    metrics_a = {**common, "run": "A_original", "label_file": ORIGINAL.name, "label_tier": "silver_single_annotator (0 human-verified)",
                 "reproduction_vs_t2_3_1": reproduction, "summary": sum_a}
    metrics_b = {**common, "run": "B_merged", "label_file": MERGED.name, "label_tier": "silver_single_annotator (0 human-verified)",
                 "bias_warning": "Merged labels add 95 relevant labels, ALL from the dense top-20 pool (81 at rank <= 5). Merged metrics are biased in favour of dense and must not be used as a fair comparison with FTS/hybrid unless their top-k are pooled and judged equally.",
                 "summary": sum_b}
    record = {**common, "latency": run_info, "reproduction_vs_t2_3_1": reproduction, "fingerprint_before": fp_before,
              "fingerprint_after": fp_after, "query_cache_after": cache_after, "unchanged": unchanged, "q057": q057_info,
              "ranked": ranked}
    pq_cols = ["question_id", "run", "cohort", "relevant_known", "relevant_sources", "relevant_not_retrievable", "conflict_known",
               "first_relevant_rank", "mrr", "mrr_ub", "unjudged_before_first_relevant"] + \
              [f"{m}@{k}" for k in KS for m in ("recall", "hit", "precision_lb", "precision_ub", "judged_precision", "ndcg", "ndcg_t231_lb",
                                                 "source_recall", "source_hit", "document_recall", "judged_coverage")] + ["conflict_coverage@20"]
    cov_cols = ["question_id", "run", "cohort", "k", "retrieved", "judged", "unjudged", "judged_coverage", "unjudged_rate",
                "relevant_retrieved", "grade1_retrieved", "grade0_retrieved", "conflict_retrieved", "low_confidence"]
    cov_rows = [{"question_id": p["question_id"], "run": p["run"], "cohort": p["cohort"], "k": k, "retrieved": p[f"retrieved@{k}"],
                 "judged": p[f"judged@{k}"], "unjudged": p[f"unjudged@{k}"], "judged_coverage": p[f"judged_coverage@{k}"],
                 "unjudged_rate": p[f"unjudged_rate@{k}"], "relevant_retrieved": p[f"relevant_retrieved@{k}"],
                 "grade1_retrieved": p[f"grade1_retrieved@{k}"], "grade0_retrieved": p[f"grade0_retrieved@{k}"],
                 "conflict_retrieved": p[f"conflict_retrieved@{k}"],
                 "low_confidence": "yes" if (p[f"judged_coverage@{k}"] or 0) < 0.5 else "no"}
                for p in pq_a + pq_b for k in KS]

    def csv_text(rows: list[dict], cols: list[str]) -> str:
        import io
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        return buf.getvalue()

    texts = {"dense_eval_frozen_cohort_manifest": manifest_text,
             "dense_eval_original_metrics": json.dumps(metrics_a, ensure_ascii=False, indent=1) + "\n",
             "dense_eval_merged_metrics": json.dumps(metrics_b, ensure_ascii=False, indent=1) + "\n",
             "dense_eval_per_question_metrics": csv_text(pq_a + pq_b, pq_cols),
             "dense_eval_judged_coverage": csv_text(cov_rows, cov_cols),
             "dense_eval_run_record": json.dumps(record, ensure_ascii=False, indent=1) + "\n"}
    if args.check:
        diffs = []
        for n, text in texts.items():
            old = out[n].read_text(encoding="utf-8")
            if out[n].suffix == ".json":
                a_, b_ = json.loads(old), json.loads(text)
                strip = lambda d: {k: v for k, v in d.items() if k not in VOLATILE | {"latency", "fingerprint_before", "fingerprint_after"}}  # noqa: E731
                if strip(a_) != strip(b_):
                    diffs.append(n)
            elif old != text:
                diffs.append(n)
        print(json.dumps({"reproducible": not diffs, "differs": diffs, "unchanged": unchanged, "api": api, "reproduction": reproduction}, indent=1))
        return 0 if not diffs else 1
    for n, text in texts.items():
        out[n].write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"written": [p.name for p in out.values()], "unchanged": unchanged, "api": api, "reproduction": reproduction,
                      "manifest_sha256": common["manifest_sha256"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
