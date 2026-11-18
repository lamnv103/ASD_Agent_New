# ruff: noqa: E501  -- report assembly lines are kept whole for readability
"""Phase 6.2 T2.4 — FTS (sparse) baseline: runs, fair candidate pool, overlap, EXPLORATORY metrics. Read-only.

  1. preconditions: dataset / cohort-manifest / glossary / profile hashes
  2. reader-only DB fingerprint before (same function as T2.3.3)
  3. glossary corpus check: every English term instantiated for the 66 questions → chunk count in the view
  4. dense top-20 with the T2.3.1 configuration (cache only, no API) — must equal the T2.3.3 ranked lists
  5. FTS-A / FTS-B / FTS-C top-20 for the 66 questions
  6. independent SQL verification of every FTS ranking + authorization check (allowlist, D-1 exclusions)
  7. union pool per question (dedup by chunk_id) → BLIND export (no system, rank, score or prior label) +
     sealed key file (origins, ranks, scores, prior labels) + manifest + overlap
  8. exploratory metrics (original and merged labels kept separate; frozen T2.3.1 cohort)
  9. fingerprint after; --check recomputes and compares (ignoring timestamps/latency)
No annotation is performed here: the pool is PENDING ANNOTATION.

Usage: python -B scripts/fts_eval_t2_4.py [--tag 2026-11-15] [--check]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect
from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.fts import FTS_PROFILES_FILE, FtsProfile, FtsRetriever, Glossary, term_sql
from app.retrieval.types import RetrievalProfile

DS = ROOT / "eval" / "datasets"
ORIGINAL = DS / "retrieval_eval_v1.jsonl"
MERGED = DS / "retrieval_eval_v1_merged_2026-11-14.jsonl"
JUDGMENTS = DS / "retrieval_eval_v1_candidate_judgments_2026-11-14.jsonl"
COHORT = REPORTS / "dense_eval_frozen_cohort_manifest_2026-11-15.csv"
T233_RECORD = REPORTS / "dense_eval_run_record_2026-11-15.json"
ALLOWLIST = REPORTS / "research_authorization_allowlist_rev_d1_2026-11-14.csv"
EXCLUSIONS = REPORTS / "research_authorization_d1_exclusions_2026-11-14.csv"
GLOSSARY = ROOT / "config" / "query_glossary_vi_en_v1.json"
EXPECTED = {ORIGINAL.name: "7704bb510c9ab4a545d9195b18ffa2dc32f10b705df909a9201e11c96f104c2b",
            MERGED.name: "6bd3ad7868f9fc2aa5c8079c4d7d14116a06c721ec55537b466a9960a3eae7ab",
            COHORT.name: "0d88846ea299c57cf060d0a9278b96c361c2b13df3aff0162f326b8588be380c"}
SYSTEMS = {"dense": None, "fts_a": "fts_a_baseline_v1", "fts_b": "fts_b_glossary_and_v1", "fts_c": "fts_c_glossary_or_v1"}
KS = (5, 10, 20)
K = 20
POOL_SALT = "t2_4_pool_v1"
CASES = ("q066", "q033", "q063", "q054")
CODE = ["app/retrieval/fts.py", "config/fts_profiles.json", "config/query_glossary_vi_en_v1.json",
        "scripts/fts_eval_t2_4.py", "app/retrieval/dense.py", "app/retrieval/research_reader.py",
        "config/retrieval_profiles.json"]
VOLATILE = {"generated_at", "latency", "fingerprint_before", "fingerprint_after"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_mod(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def jsonl(path: Path) -> dict[str, dict]:
    return {r["question_id"]: r for r in (json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip())}


def csv_text(rows: list[dict], cols: list[str]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def item_id(qid: str, chunk_id: str) -> str:
    return hashlib.sha256(f"{POOL_SALT}|{qid}|{chunk_id}".encode()).hexdigest()[:16]


def glossary_corpus_check(glossary: Glossary, questions: dict[str, dict]) -> dict:
    """Count chunks in the view matching each English term the glossary produces for the 66 questions (+ all entries)."""
    terms = sorted({t for e in glossary.entries for t in e["en"]} |
                   {t for q in questions.values() for c in glossary.expand(q["question_vi"]).concepts for t in c.terms})
    out = {}
    with connect("research_reader", "t2_4_glossary_check") as conn:
        conn.read_only = True
        for t in terms:
            kind, text = term_sql(t)
            fn = "plainto_tsquery" if kind == "all" else "phraseto_tsquery"
            n = conn.execute(f"SELECT count(*) FROM asd_rag.v_research_retrieval_chunks WHERE content_tsv @@ {fn}('english', %(t)s)",
                             {"t": text}).fetchone()[0]
            out[t] = n
        conn.rollback()
    return out


def verify_independently(tsq: str, profile_code: str, k: int) -> list[str]:
    """Independent check: all matches with their ts_rank_cd, ordered in Python (no SQL ORDER BY / LIMIT)."""
    if not tsq:
        return []
    with connect("research_reader", "t2_4_verify") as conn:
        conn.read_only = True
        rows = conn.execute("SELECT chunk_id, ts_rank_cd(content_tsv, %(q)s::tsquery, 0) FROM asd_rag.v_research_retrieval_chunks "
                            "WHERE profile_code = %(p)s AND content_tsv @@ %(q)s::tsquery", {"q": tsq, "p": profile_code}).fetchall()
        conn.rollback()
    return [c for c, _ in sorted(rows, key=lambda r: (-r[1], r[0]))][:k]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default="2026-11-15")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    E = load_mod("dense_eval_t2_3_3", "scripts/dense_eval_t2_3_3.py")
    T231 = load_mod("dense_retrieval_eval", "scripts/dense_retrieval_eval.py")
    names = {"pool": ("fts_candidate_pool", "jsonl"), "key": ("fts_candidate_pool_key", "jsonl"),
             "manifest": ("fts_candidate_pool_manifest", "csv"), "overlap": ("fts_candidate_overlap", "csv"),
             "metrics": ("fts_retrieval_metrics", "json"), "glossary": ("fts_query_glossary", "json"),
             "record": ("fts_run_record", "json")}
    out = {k: REPORTS / f"{n}_{args.tag}.{ext}" for k, (n, ext) in names.items()}
    if not args.check and any(p.exists() for p in out.values()):
        raise SystemExit("output files exist; refusing to overwrite (use --check or a new --tag)")

    inputs = {p.name: sha(p) for p in (ORIGINAL, MERGED, JUDGMENTS, COHORT, T233_RECORD, ALLOWLIST, EXCLUSIONS, GLOSSARY, FTS_PROFILES_FILE)}
    for n, exp in EXPECTED.items():
        if inputs[n] != exp:
            raise SystemExit(f"{n} changed ({inputs[n][:12]} != {exp[:12]}); stop")
    code = {c: sha(ROOT / c) for c in CODE}
    original, merged = jsonl(ORIGINAL), jsonl(MERGED)
    with open(COHORT, encoding="utf-8") as f:
        cohorts = {r["question_id"]: r["cohort_t2_3_1"] for r in csv.DictReader(f)}
    if set(cohorts) != set(original) or len(cohorts) != 66:
        raise SystemExit("cohort manifest does not cover the 66 questions; stop")
    allow = {r["chunk_id"] for r in csv.DictReader(io.StringIO(ALLOWLIST.read_text(encoding="utf-8-sig")))}
    excluded = {r["chunk_id"] for r in csv.DictReader(io.StringIO(EXCLUSIONS.read_text(encoding="utf-8-sig")))}
    t232 = {(r["question_id"], r["chunk_id"]): r["status"] for r in (json.loads(x) for x in JUDGMENTS.read_text(encoding="utf-8").splitlines())}

    fp_before = E.reader_fingerprint()
    rp = RetrievalProfile.load("dense_baseline_v1")
    cache_before = E.dir_sha(ROOT / rp.query_cache_dir)
    glossary = Glossary(GLOSSARY)
    term_counts = glossary_corpus_check(glossary, original)

    # ---- dense (T2.3.1 configuration, cache only)
    dense_ranked, dense_api, dense_info = E.ranked_lists(rp, original, f"t2_4_dense_{datetime.now(UTC):%Y%m%dT%H%M%S}.jsonl")
    t233 = json.loads(T233_RECORD.read_text(encoding="utf-8"))["ranked"]
    dense_same = sum([x["chunk_id"] for x in dense_ranked[q]] == [x["chunk_id"] for x in t233[q]] for q in original)
    if dense_api["cache_misses"] or dense_api["calls"]:
        raise SystemExit("dense run needed the API; stop")

    # ---- FTS runs
    log = JsonlRetrievalLog(ROOT / "logs" / "retrieval", f"t2_4_fts_{datetime.now(UTC):%Y%m%dT%H%M%S}.jsonl")
    ranked = {"dense": dense_ranked}
    runs: dict[str, dict] = {}
    problems = []
    for sysname, code_ in SYSTEMS.items():
        if code_ is None:
            continue
        prof = FtsProfile.load(code_)
        ret = FtsRetriever(prof, glossary=glossary if prof.query_mode != "plain_and" else None, log=log)
        ranked[sysname], runs[sysname] = {}, {}
        for q in sorted(original):
            resp = ret.retrieve(original[q]["question_vi"], k=K, question_id=q)
            hits = resp.results
            ranked[sysname][q] = [{"rank": h.rank, "chunk_id": h.chunk_id, "source_id": h.source_id, "document_id": h.document_id,
                                   "score": round(h.score, 6), "authorization_version": h.authorization_version} for h in hits]
            runs[sysname][q] = {"normalized_query": resp.normalized_query, "expansion": resp.expansion, "tsquery": resp.tsquery,
                                "ts_config": resp.ts_config, "ranker": resp.ranker, "profile_version": resp.profile_version,
                                "status": resp.status, "returned": len(hits)}
            indep = verify_independently(resp.tsquery, prof.view_profile_code, K)
            if indep != [h.chunk_id for h in hits]:
                problems.append(f"{sysname}/{q}: retriever ranking differs from independent SQL")
            for h in hits:
                if h.chunk_id not in allow or h.chunk_id in excluded or h.authorization_version != 2:
                    problems.append(f"{sysname}/{q}: {h.chunk_id[-30:]} outside the active authorization")
    verification = {"independent_sql_rankings_identical": not any("independent" in p for p in problems),
                    "authorization_violations": sum("authorization" in p for p in problems), "problems": problems,
                    "dense_identical_to_t2_3_3": f"{dense_same}/{len(original)}"}

    # ---- pool
    pool_items, key_items, manifest_rows, overlap_rows = [], [], [], []
    for q in sorted(original):
        origin: dict[str, dict] = {}
        for s in SYSTEMS:
            for x in ranked[s][q][:K]:
                o = origin.setdefault(x["chunk_id"], {"source_id": x["source_id"], "document_id": x["document_id"], "ranks": {}, "scores": {}})
                o["ranks"][s] = x["rank"]
                if "score" in x:
                    o["scores"][s] = x["score"]
                elif "cosine_distance" in x:
                    o["scores"][s] = x["cosine_distance"]
        g_o = {j["chunk_id"]: j["grade"] for j in original[q]["judgments"]}
        g_m = {j["chunk_id"]: j["grade"] for j in merged[q]["judgments"]}
        for cid, o in origin.items():
            iid = item_id(q, cid)
            key_items.append({"item_id": iid, "question_id": q, "chunk_id": cid, "source_id": o["source_id"],
                              "in_dense": "dense" in o["ranks"], "in_fts_a": "fts_a" in o["ranks"], "in_fts_b": "fts_b" in o["ranks"],
                              "in_fts_c": "fts_c" in o["ranks"], "ranks": o["ranks"], "scores": o["scores"],
                              "grade_original": g_o.get(cid), "grade_merged": g_m.get(cid), "t2_3_2_status": t232.get((q, cid))})
            pool_items.append({"item_id": iid, "question_id": q, "chunk_id": cid, "source_id": o["source_id"], "document_id": o["document_id"]})
        dense_set = {x["chunk_id"] for x in ranked["dense"][q]}
        fts_any = set().union(*({x["chunk_id"] for x in ranked[s][q]} for s in ("fts_a", "fts_b", "fts_c")))
        manifest_rows.append({"question_id": q, "cohort_t2_3_1": cohorts[q], "dense": len(dense_set),
                              **{s: len(ranked[s][q]) for s in ("fts_a", "fts_b", "fts_c")}, "union": len(origin),
                              "dense_only": len(dense_set - fts_any), "fts_only": len(fts_any - dense_set), "both": len(dense_set & fts_any),
                              "labelled_original": sum(c in g_o for c in origin), "labelled_merged": sum(c in g_m for c in origin),
                              "unlabelled_in_both_sets": sum(c not in g_m and c not in g_o for c in origin),
                              "to_annotate_blind": len(origin)})
        for a, b in (("dense", "fts_a"), ("dense", "fts_b"), ("dense", "fts_c"), ("fts_b", "fts_c")):
            for k in (10, 20):
                A = {x["chunk_id"] for x in ranked[a][q][:k]}
                B = {x["chunk_id"] for x in ranked[b][q][:k]}
                overlap_rows.append({"question_id": q, "cohort_t2_3_1": cohorts[q], "pair": f"{a}|{b}", "k": k, "n_a": len(A), "n_b": len(B),
                                     "intersection": len(A & B), "a_only": len(A - B), "b_only": len(B - A),
                                     "jaccard": round(len(A & B) / len(A | B), 4) if A | B else None})
    # blind export: content + provenance needed to judge; ordered by item_id (independent of rank/system)
    content = {}
    with connect("research_reader", "t2_4_pool_content") as conn:
        conn.read_only = True
        ids = sorted({p["chunk_id"] for p in pool_items})
        for row in conn.execute("SELECT chunk_id, title, section_heading, page_start, page_end, char_start, char_end, content, content_sha256 "
                                "FROM asd_rag.v_research_retrieval_chunks WHERE chunk_id = ANY(%(ids)s)", {"ids": ids}):
            content[row[0]] = row
        conn.rollback()
    blind = []
    for p in sorted(pool_items, key=lambda x: (x["question_id"], x["item_id"])):
        c = content[p["chunk_id"]]
        r = original[p["question_id"]]
        blind.append({"item_id": p["item_id"], "question_id": p["question_id"], "question_vi": r["question_vi"],
                      "expected_answer_scope": r["expected_answer_scope"], "chunk_id": p["chunk_id"], "source_id": p["source_id"],
                      "document_id": p["document_id"], "title": c[1], "section": c[2],
                      "page": None if c[3] is None else (str(c[3]) if c[4] in (None, c[3]) else f"{c[3]}-{c[4]}"),
                      "char_range": None if c[5] is None else f"{c[5]}-{c[6]}", "content": c[7], "content_sha256": c[8],
                      "grade": None, "rationale_vi": None, "annotator_id": None, "annotated_at": None})
    pool_stats = {"pairs_union": len(pool_items), "unique_chunks": len({p["chunk_id"] for p in pool_items}),
                  "pairs_dense_only": sum(r["dense_only"] for r in manifest_rows), "pairs_fts_only": sum(r["fts_only"] for r in manifest_rows),
                  "pairs_both": sum(r["both"] for r in manifest_rows),
                  "pairs_labelled_original": sum(r["labelled_original"] for r in manifest_rows),
                  "pairs_labelled_merged": sum(r["labelled_merged"] for r in manifest_rows),
                  "pairs_unlabelled": sum(r["unlabelled_in_both_sets"] for r in manifest_rows),
                  "pairs_by_origin": dict(Counter("+".join(s for s in SYSTEMS if k[f"in_{s}"]) for k in key_items)),
                  "annotation_status": "PENDING ANNOTATION (no blind human annotation performed; no AI labels used)"}
    dense_chunks = {k["chunk_id"] for k in key_items if k["in_dense"]}
    fts_chunks = {k["chunk_id"] for k in key_items if k["in_fts_a"] or k["in_fts_b"] or k["in_fts_c"]}
    pool_stats.update({"unique_chunks_dense": len(dense_chunks), "unique_chunks_fts": len(fts_chunks),
                       "unique_chunks_only_dense": len(dense_chunks - fts_chunks), "unique_chunks_only_fts": len(fts_chunks - dense_chunks)})

    # ---- exploratory metrics
    with connect("research_reader", "t2_4_retrievable") as conn:
        conn.read_only = True
        retrievable = {r[0] for r in conn.execute("SELECT chunk_id FROM asd_rag.v_research_retrieval_chunks")}
        conn.rollback()
    metrics = {"status": "EXPLORATORY ONLY — not a fair comparison. Original labels: low judged coverage, pooled by a T1 search; merged labels: +95 relevant labels from the dense top-20 only (biased to dense). A fair comparison needs blind annotation of the union pool.",
               "label_sets": {}, "definitions": E.METRIC_DEFINITIONS}
    per_q_rows = []
    for label_name, records in (("original", original), ("merged", merged)):
        metrics["label_sets"][label_name] = {}
        for s in SYSTEMS:
            per_q = []
            for q in sorted(records):
                m = E.question_metrics(ranked[s][q], records[q], retrievable, T231)
                m.pop("_t231")
                per_q.append({"question_id": q, "cohort": cohorts[q], **m})
                per_q_rows.append({"label_set": label_name, "system": s, "question_id": q, "cohort": cohorts[q],
                                   **{k_: m[k_] for k_ in ("relevant_known", "first_relevant_rank", "mrr", "recall@10", "recall@20", "hit@10", "judged_coverage@10", "judged_coverage@20", "returned")}})
            summ = {}
            for g in ("answerable", "answerable_partial_pool", "conflicting"):
                summ[g] = E.summarize(per_q, [q for q in sorted(records) if cohorts[q] == g], T231)
            summ["returned_lt_20"] = sum(1 for p in per_q if p["returned"] < K)
            summ["returned_zero"] = sorted(p["question_id"] for p in per_q if p["returned"] == 0)
            metrics["label_sets"][label_name][s] = summ
    # mandatory cases
    cases = {}
    for q in CASES:
        g_o = {j["chunk_id"]: j["grade"] for j in original[q]["judgments"]}
        g_m = {j["chunk_id"]: j["grade"] for j in merged[q]["judgments"]}
        cases[q] = {s: [{"rank": x["rank"], "chunk_id": x["chunk_id"], "source_id": x["source_id"], "grade_original": g_o.get(x["chunk_id"]),
                         "grade_merged": g_m.get(x["chunk_id"]), "t2_3_2_status": t232.get((q, x["chunk_id"]))} for x in ranked[s][q][:10]]
                    for s in SYSTEMS}
        cases[q]["expansion"] = runs["fts_b"][q]["expansion"]
        cases[q]["tsquery_b"] = runs["fts_b"][q]["tsquery"]
        cases[q]["tsquery_c"] = runs["fts_c"][q]["tsquery"]
    fp_after = E.reader_fingerprint()
    cache_after = E.dir_sha(ROOT / rp.query_cache_dir)
    unchanged = {"db_fingerprint_identical": fp_before == fp_after, "query_cache_identical": cache_before == cache_after,
                 "original_unchanged": sha(ORIGINAL) == EXPECTED[ORIGINAL.name], "merged_unchanged": sha(MERGED) == EXPECTED[MERGED.name]}
    zero_terms = sorted(t for t, n in term_counts.items() if n == 0)
    glossary_doc = {"version": glossary.version, "sha256": glossary.sha256, "file": str(GLOSSARY.relative_to(ROOT)).replace("\\", "/"),
                    "glossary": json.loads(GLOSSARY.read_text(encoding="utf-8")),
                    "corpus_check": {"terms_checked": len(term_counts), "terms_with_zero_chunks": zero_terms, "chunk_counts": term_counts},
                    "expansions_for_eval_questions": {q: runs["fts_b"][q]["expansion"] for q in sorted(original)}}
    common = {"task": "T2.4 FTS baseline (exploratory evaluation + fair pool)", "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
              "inputs_sha256": inputs, "code_sha256": code, "k": K, "api": {"dense": dense_api, "fts": "no external API (PostgreSQL only)"}}
    metrics.update(common)
    metrics["pool"] = pool_stats
    record = {**common, "verification": verification, "pool": pool_stats, "unchanged": unchanged, "fingerprint_before": fp_before,
              "fingerprint_after": fp_after, "query_cache": cache_before, "latency": dense_info, "runs": runs, "ranked": ranked, "cases": cases}
    texts = {"pool": "".join(json.dumps(b, ensure_ascii=False) + "\n" for b in blind),
             "key": "".join(json.dumps(k_, ensure_ascii=False) + "\n" for k_ in sorted(key_items, key=lambda x: (x["question_id"], x["item_id"]))),
             "manifest": csv_text(manifest_rows, list(manifest_rows[0])),
             "overlap": csv_text(overlap_rows, list(overlap_rows[0])),
             "metrics": json.dumps(metrics, ensure_ascii=False, indent=1) + "\n",
             "glossary": json.dumps(glossary_doc, ensure_ascii=False, indent=1) + "\n",
             "record": json.dumps(record, ensure_ascii=False, indent=1) + "\n"}
    summary = {"verification": {k_: v for k_, v in verification.items() if k_ != "problems"}, "problems": problems[:10],
               "unchanged": unchanged, "pool": pool_stats, "zero_count_glossary_terms": zero_terms}
    if args.check:
        diffs = []
        for n, text in texts.items():
            old = out[n].read_text(encoding="utf-8")
            if out[n].suffix == ".json":
                strip = lambda d: {k_: v for k_, v in d.items() if k_ not in VOLATILE}  # noqa: E731
                if strip(json.loads(old)) != strip(json.loads(text)):
                    diffs.append(n)
            elif old != text:
                diffs.append(n)
        print(json.dumps({"reproducible": not diffs, "differs": diffs, **summary}, ensure_ascii=False, indent=1))
        return 0 if not diffs and not problems else 1
    for n, text in texts.items():
        out[n].write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"written": [p.name for p in out.values()], **summary}, ensure_ascii=False, indent=1))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
