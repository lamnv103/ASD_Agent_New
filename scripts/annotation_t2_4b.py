# ruff: noqa: E501  -- report assembly lines are kept whole for readability
"""Phase 6.2 T2.4-B — blind human annotation of the Dense + FTS union pool: verify, package, import, agree, finalize.

This script never produces a relevance label. Labels come only from the two human annotators' returned files and
from a named adjudicator. AI-generated labels are never used as annotations or as hints.

Subcommands
  verify     R1 integrity of the T2.4 pool (+ live content check via the research reader view, read-only)
  package    R2 two independent blind packages (random HMAC codes, independent shuffles) + coordinator code map
  import     validate a returned annotator file and map codes back to (question_id, chunk_id) → annotator_{a,b} file
  agreement  R5 agreement (exact, per-grade, confusion, linear/quadratic weighted kappa on 0..3, -1 and needs_review
             reported separately) + R6 disagreement list
  finalize   R9 final labels: agreed pairs + adjudicated pairs only; never averages; others stay pending

Files: eval/annotation/t2_4b/{annotator_a,annotator_b,coordinator}/ and eval/reports/fts_*_2026-11-15.*
The coordinator folder and eval/reports/fts_candidate_pool_key_2026-11-15.jsonl must never be given to annotators.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import io
import json
import random
import secrets
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT

TAG = "2026-11-15"
POOL = REPORTS / f"fts_candidate_pool_{TAG}.jsonl"
KEY = REPORTS / f"fts_candidate_pool_key_{TAG}.jsonl"
MANIFEST = REPORTS / f"fts_candidate_pool_manifest_{TAG}.csv"
OVERLAP = REPORTS / f"fts_candidate_overlap_{TAG}.csv"
RECORD = REPORTS / f"fts_run_record_{TAG}.json"
ORIGINAL = ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl"
MERGED = ROOT / "eval" / "datasets" / "retrieval_eval_v1_merged_2026-11-14.jsonl"
EMB_MANIFEST = REPORTS / "embedding_manifest.csv"
ALLOWLIST = REPORTS / "research_authorization_allowlist_rev_d1_2026-11-14.csv"
ANN = ROOT / "eval" / "annotation" / "t2_4b"
COORD = ANN / "coordinator"
EXPECTED = {POOL.name: "851dc4710eef4ec3", KEY.name: "0de3cc6c65753221", MANIFEST.name: "e9e7c072b501778a",
            OVERLAP.name: "0da42455798b875b", ORIGINAL.name: "7704bb510c9ab4a5", MERGED.name: "6bd3ad7868f9fc2a"}
FROZEN = ["config/query_glossary_vi_en_v1.json", "config/fts_profiles.json", "config/retrieval_profiles.json",
          "app/retrieval/fts.py", "app/retrieval/dense.py", "app/retrieval/research_reader.py"]
GRADES = (-1, 0, 1, 2, 3)
ORDINAL = (0, 1, 2, 3)
CONFIDENCE = ("high", "medium", "low")
PACKAGE_FIELDS = ["annotation_code", "question_id", "question_vi", "document_title", "section", "page", "content",
                  "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]
FORBIDDEN_IN_PACKAGE = {"chunk_id", "item_id", "source_id", "document_id", "in_dense", "in_fts_a", "in_fts_b", "in_fts_c",
                        "ranks", "scores", "rank", "score", "grade_original", "grade_merged", "t2_3_2_status",
                        "expected_answer_scope", "content_sha256", "char_range"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def write_new(p: Path, text: str) -> None:
    if p.exists():
        raise SystemExit(f"{p} exists; refusing to overwrite")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def jsonl_text(rows: list[dict]) -> str:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def csv_text(rows: list[dict], cols: list[str], bom: bool = False) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore", lineterminator="\r\n" if bom else "\n")
    w.writeheader()
    w.writerows(rows)
    return ("﻿" if bom else "") + buf.getvalue()


# ============================================================================================ R1 verify
def verify(live: bool = True) -> dict:
    checks: dict[str, object] = {}
    problems: list[str] = []
    files = {p.name: sha(p) for p in (POOL, KEY, MANIFEST, OVERLAP, ORIGINAL, MERGED)}
    for n, prefix in EXPECTED.items():
        if not files[n].startswith(prefix):
            problems.append(f"{n}: hash {files[n][:16]} != recorded {prefix}")
    pool, key = read_jsonl(POOL), read_jsonl(KEY)
    ds = {r["question_id"]: r for r in read_jsonl(ORIGINAL)}
    emb = {r["chunk_id"]: r for r in csv.DictReader(io.StringIO(EMB_MANIFEST.read_text(encoding="utf-8-sig")))}
    allow = {r["chunk_id"] for r in csv.DictReader(io.StringIO(ALLOWLIST.read_text(encoding="utf-8-sig")))}
    pairs = [(p["question_id"], p["chunk_id"]) for p in pool]
    kpairs = [(k["question_id"], k["chunk_id"]) for k in key]
    checks["questions"] = len({q for q, _ in pairs})
    checks["pairs"] = len(pairs)
    checks["unique_chunks"] = len({c for _, c in pairs})
    checks["duplicate_pairs"] = len(pairs) - len(set(pairs))
    checks["duplicate_item_ids"] = len(pool) - len({p["item_id"] for p in pool})
    checks["pool_pairs_equal_key_pairs"] = set(pairs) == set(kpairs) and len(kpairs) == len(set(kpairs))
    checks["pool_item_ids_equal_key_item_ids"] = {(p["item_id"], p["question_id"], p["chunk_id"]) for p in pool} == {(k["item_id"], k["question_id"], k["chunk_id"]) for k in key}
    for name, want in (("questions", 66), ("pairs", 2791), ("unique_chunks", 1218), ("duplicate_pairs", 0), ("duplicate_item_ids", 0)):
        if checks[name] != want:
            problems.append(f"{name} = {checks[name]} (expected {want})")
    for name in ("pool_pairs_equal_key_pairs", "pool_item_ids_equal_key_item_ids"):
        if not checks[name]:
            problems.append(name)
    # question mapping, provenance, content
    bad_q = [p["item_id"] for p in pool if p["question_id"] not in ds or ds[p["question_id"]]["question_vi"] != p["question_vi"]]
    bad_hash = [p["item_id"] for p in pool if hashlib.sha256(p["content"].encode("utf-8")).hexdigest() != p["content_sha256"]]
    bad_emb = [p["item_id"] for p in pool if p["chunk_id"] not in emb or emb[p["chunk_id"]]["content_hash"] != p["content_sha256"]
               or emb[p["chunk_id"]]["source_id"] != p["source_id"] or emb[p["chunk_id"]]["document_id"] != p["document_id"]]
    bad_prov = [p["item_id"] for p in pool if not p["source_id"] or not p["document_id"] or not p["title"] or (p["page"] is None and p["char_range"] is None)]
    bad_allow = [p["item_id"] for p in pool if p["chunk_id"] not in allow]
    for name, lst in (("question_mapping_errors", bad_q), ("content_hash_errors", bad_hash), ("manifest_mismatch", bad_emb),
                      ("provenance_missing", bad_prov), ("outside_authorization_2", bad_allow)):
        checks[name] = len(lst)
        if lst:
            problems.append(f"{name}: {len(lst)}")
    # manifest per question = pool per question; key origins = run-record ranked lists
    man = {r["question_id"]: r for r in csv.DictReader(io.StringIO(MANIFEST.read_text(encoding="utf-8")))}
    per_q = Counter(q for q, _ in pairs)
    checks["manifest_union_matches_pool"] = all(int(man[q]["union"]) == per_q[q] for q in man) and set(man) == set(per_q)
    ranked = json.loads(RECORD.read_text(encoding="utf-8"))["ranked"]
    origin_err = 0
    for k in key:
        for s in ("dense", "fts_a", "fts_b", "fts_c"):
            rank = next((x["rank"] for x in ranked[s][k["question_id"]] if x["chunk_id"] == k["chunk_id"]), None)
            if (rank is not None) != k[f"in_{s}"] or (rank is not None and k["ranks"].get(s) != rank):
                origin_err += 1
    checks["key_origin_errors_vs_run_record"] = origin_err
    if not checks["manifest_union_matches_pool"]:
        problems.append("manifest union != pool count")
    if origin_err:
        problems.append(f"key origin errors: {origin_err}")
    by_origin = Counter("+".join(s for s in ("dense", "fts_a", "fts_b", "fts_c") if k[f"in_{s}"]) for k in key)
    checks["pairs_by_origin"] = dict(sorted(by_origin.items()))
    checks["pairs_dense_only"] = by_origin.get("dense", 0)
    checks["pairs_fts_only"] = sum(v for o, v in by_origin.items() if "dense" not in o)
    checks["pairs_both"] = sum(v for o, v in by_origin.items() if "dense" in o and o != "dense")
    if live:  # content in the live research view (reader role, read-only) is unchanged
        from app.db import connect
        with connect("research_reader", "t2_4b_verify") as conn:
            conn.read_only = True
            live_hash = {r[0]: (r[1], r[2]) for r in conn.execute(
                "SELECT chunk_id, content_sha256, authorization_id FROM asd_rag.v_research_retrieval_chunks WHERE chunk_id = ANY(%(i)s)",
                {"i": sorted({c for _, c in pairs})})}
            conn.rollback()
        live_bad = [p["item_id"] for p in pool if live_hash.get(p["chunk_id"], (None, None))[0] != p["content_sha256"]
                    or live_hash[p["chunk_id"]][1] != 2]
        checks["live_view_content_or_authorization_mismatch"] = len(live_bad)
        if live_bad:
            problems.append(f"live view mismatch: {len(live_bad)}")
    checks["frozen_files_sha256"] = {f: sha(ROOT / f) for f in FROZEN}
    return {"ok": not problems, "problems": problems, "files_sha256": files, "checks": checks,
            "verified_at": datetime.now(UTC).isoformat(timespec="seconds")}


# =========================================================================================== R2 package
def annotation_code(secret: bytes, annotator: str, qid: str, chunk_id: str) -> str:
    return hmac.new(secret, f"{annotator}|{qid}|{chunk_id}".encode(), hashlib.sha256).hexdigest()[:10].upper()


def build_package(pool: list[dict], annotator: str, secret: bytes) -> tuple[list[dict], list[dict]]:
    """Returns (package rows for the annotator, coordinator map rows). Order: questions shuffled and candidates
    shuffled per annotator with an RNG seeded from the secret — unrelated to rank or retrieval system."""
    rng = random.Random(hmac.new(secret, f"order|{annotator}".encode(), hashlib.sha256).digest())
    by_q: dict[str, list[dict]] = defaultdict(list)
    for p in pool:
        by_q[p["question_id"]].append(p)
    qids = sorted(by_q)
    rng.shuffle(qids)
    rows, cmap = [], []
    for qpos, q in enumerate(qids, 1):
        items = sorted(by_q[q], key=lambda p: p["chunk_id"])
        rng.shuffle(items)
        for ipos, p in enumerate(items, 1):
            code = annotation_code(secret, annotator, q, p["chunk_id"])
            rows.append({"annotation_code": code, "question_id": q, "question_vi": p["question_vi"], "document_title": p["title"],
                         "section": p["section"] or "", "page": p["page"] or "", "content": p["content"], "grade": "", "rationale": "",
                         "evidence_span": "", "confidence": "", "needs_review": "", "review_note": ""})
            cmap.append({"annotator": annotator, "annotation_code": code, "position": f"{qpos}.{ipos}", "question_id": q,
                         "chunk_id": p["chunk_id"], "item_id": p["item_id"], "content_sha256": p["content_sha256"]})
    return rows, cmap


def package(check_only: bool = False) -> dict:
    v = verify()
    if not v["ok"]:
        raise SystemExit(f"R1 integrity failed, packages not created: {v['problems']}")
    pool = read_jsonl(POOL)
    secret_file = COORD / "hmac_secret.txt"
    if check_only:
        secret = bytes.fromhex(secret_file.read_text().strip())
    else:
        if secret_file.exists():
            raise SystemExit("coordinator secret exists; packages were already created (refusing to regenerate)")
        secret = secrets.token_bytes(32)
        write_new(secret_file, secret.hex() + "\n")
    out, maps = {}, []
    for a in ("a", "b"):
        rows, cmap = build_package(pool, a, secret)
        maps += cmap
        out[f"annotator_{a}/fts_blind_annotation_package_annotator_{a}_{TAG}.jsonl"] = jsonl_text(rows)
        out[f"annotator_{a}/fts_blind_annotation_package_annotator_{a}_{TAG}.csv"] = csv_text(rows, PACKAGE_FIELDS, bom=True)
    out[f"coordinator/annotation_code_map_{TAG}.jsonl"] = jsonl_text(maps)
    out["coordinator/annotators.json"] = json.dumps({"a": None, "b": None, "adjudicator": None, "note": "coordinator fills real ids; never given to annotators"}, indent=1) + "\n"
    guide = (ANN / f"annotation_guidelines_t2_4b_{TAG}.md")
    if guide.exists():
        for a in ("a", "b"):
            out[f"annotator_{a}/annotation_guidelines_t2_4b_{TAG}.md"] = guide.read_text(encoding="utf-8")
    leak = leakage_check(out, pool)
    if check_only:
        diffs = [n for n, t in out.items() if (ANN / n).read_bytes().decode("utf-8") != t]
        return {"reproducible": not diffs, "differs": diffs, "leakage": leak}
    if not leak["ok"]:
        raise SystemExit(f"leakage check failed: {leak}")
    for n, t in out.items():
        write_new(ANN / n, t)
    return {"written": sorted(out), "leakage": leak, "sha256": {n: hashlib.sha256(t.encode("utf-8")).hexdigest() for n, t in out.items()}}


def leakage_check(out: dict[str, str], pool: list[dict]) -> dict:
    problems = []
    key_values = set()
    for k in read_jsonl(KEY):
        key_values |= {k["chunk_id"], k["item_id"]}
    for n, text in out.items():
        if not n.startswith("annotator_") or not n.endswith(".jsonl"):
            continue
        rows = read_jsonl_text(text)
        for r in rows:
            bad = set(r) & FORBIDDEN_IN_PACKAGE
            if bad or set(r) != set(PACKAGE_FIELDS):
                problems.append(f"{n}: fields {sorted(bad) or sorted(set(r) ^ set(PACKAGE_FIELDS))}")
                break
            if r["annotation_code"] in key_values or any(v in key_values for k_, v in r.items() if k_ != "content"):
                problems.append(f"{n}: internal id exposed")
                break
            if any(r[f] for f in ("grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note")):
                problems.append(f"{n}: pre-filled annotation fields")
                break
    a = [r["annotation_code"] for r in read_jsonl_text(out[f"annotator_a/fts_blind_annotation_package_annotator_a_{TAG}.jsonl"])]
    b = [r["annotation_code"] for r in read_jsonl_text(out[f"annotator_b/fts_blind_annotation_package_annotator_b_{TAG}.jsonl"])]
    if set(a) & set(b):
        problems.append("annotator codes overlap between A and B")
    if len(set(a)) != len(pool) or len(set(b)) != len(pool):
        problems.append("codes not unique / pairs missing")
    # order independence from retrieval: Spearman between package position and best rank across systems (coordinator-only check)
    key = {(k["question_id"], k["chunk_id"]): min(k["ranks"].values()) for k in read_jsonl(KEY)}
    corr = {}
    for ann in ("a", "b"):
        rows = read_jsonl_text(out[f"annotator_{ann}/fts_blind_annotation_package_annotator_{ann}_{TAG}.jsonl"])
        cmap = {m["annotation_code"]: m for m in read_jsonl_text(out[f"coordinator/annotation_code_map_{TAG}.jsonl"]) if m["annotator"] == ann}
        rho = []
        by_q = defaultdict(list)
        for pos, r in enumerate(rows):
            m = cmap[r["annotation_code"]]
            by_q[m["question_id"]].append((pos, key[(m["question_id"], m["chunk_id"])]))
        for v in by_q.values():
            if len(v) > 2:
                rho.append(spearman([x for x, _ in v], [y for _, y in v]))
        corr[ann] = round(sum(rho) / len(rho), 4)
    return {"ok": not problems, "problems": problems, "mean_spearman_position_vs_best_rank": corr}


def read_jsonl_text(text: str) -> list[dict]:
    return [json.loads(x) for x in text.splitlines() if x.strip()]


def spearman(x: list[float], y: list[float]) -> float:
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


# ============================================================================================ import
def parse_returned(rows: list[dict], code_map: dict[str, dict], annotator: str) -> tuple[list[dict], list[str]]:
    """Validate one annotator's returned rows (csv or jsonl, same fields). Returns (labels, errors)."""
    errors, labels, seen = [], [], set()
    expected = {c for c, m in code_map.items() if m["annotator"] == annotator}
    for i, r in enumerate(rows, 1):
        code = str(r.get("annotation_code", "")).strip()
        if code not in expected:
            errors.append(f"row {i}: unknown or foreign annotation_code {code!r}")
            continue
        if code in seen:
            errors.append(f"row {i}: duplicate code {code}")
            continue
        seen.add(code)
        needs = str(r.get("needs_review", "")).strip().lower() in ("1", "true", "yes", "x", "needs_review")
        g_raw = str(r.get("grade", "")).strip()
        if g_raw == "" and not needs:
            continue  # not yet annotated: stays UNJUDGED, never 0
        grade = None
        if g_raw != "":
            try:
                grade = int(float(g_raw))
            except ValueError:
                errors.append(f"row {i}: grade {g_raw!r} not a number")
                continue
            if grade not in GRADES or str(grade) != g_raw.split(".")[0].strip():
                errors.append(f"row {i}: grade {g_raw!r} not in -1..3")
                continue
        rationale = str(r.get("rationale", "")).strip()
        span = str(r.get("evidence_span", "")).strip()
        conf = str(r.get("confidence", "")).strip().lower()
        if grade is not None and not rationale:
            errors.append(f"row {i}: grade without rationale")
        if grade is not None and grade >= 1 and not span:
            errors.append(f"row {i}: grade {grade} without evidence_span")
        if grade is not None and conf not in CONFIDENCE:
            errors.append(f"row {i}: confidence must be high/medium/low")
        if needs and not str(r.get("review_note", "")).strip():
            errors.append(f"row {i}: needs_review without review_note")
        m = code_map[code]
        if span and span not in r.get("content", span) and span.replace("…", "") not in r.get("content", span):
            errors.append(f"row {i}: evidence_span is not a substring of the chunk content")
        labels.append({"annotator": annotator, "annotation_code": code, "question_id": m["question_id"], "chunk_id": m["chunk_id"],
                       "item_id": m["item_id"], "grade": grade, "needs_review": needs, "rationale": rationale, "evidence_span": span,
                       "confidence": conf or None, "review_note": str(r.get("review_note", "")).strip() or None})
    return labels, errors


# ========================================================================================= agreement
def weighted_kappa(pairs: list[tuple[int, int]], cats: tuple[int, ...], weights: str) -> float | None:
    if not pairs:
        return None
    k = len(cats)
    idx = {c: i for i, c in enumerate(cats)}
    n = len(pairs)
    obs = [[0.0] * k for _ in range(k)]
    for a, b in pairs:
        obs[idx[a]][idx[b]] += 1 / n
    ra = [sum(row) for row in obs]
    rb = [sum(obs[i][j] for i in range(k)) for j in range(k)]

    def w(i, j):
        if weights == "none":
            return 0.0 if i == j else 1.0
        d = abs(i - j) / (k - 1)
        return d * d if weights == "quadratic" else d
    num = sum(w(i, j) * obs[i][j] for i in range(k) for j in range(k))
    den = sum(w(i, j) * ra[i] * rb[j] for i in range(k) for j in range(k))
    return None if den == 0 else round(1 - num / den, 4)


def agreement(labels_a: list[dict], labels_b: list[dict]) -> tuple[dict, list[dict]]:
    A = {(x["question_id"], x["chunk_id"]): x for x in labels_a}
    B = {(x["question_id"], x["chunk_id"]): x for x in labels_b}
    both = sorted(set(A) & set(B))
    graded = [(k, A[k]["grade"], B[k]["grade"]) for k in both if A[k]["grade"] is not None and B[k]["grade"] is not None
              and not A[k]["needs_review"] and not B[k]["needs_review"]]
    cats = ("needs_review", *GRADES)

    def cat(x):
        return "needs_review" if x["needs_review"] or x["grade"] is None else x["grade"]
    conf = {str(a): {str(b): 0 for b in cats} for a in cats}
    for k in both:
        conf[str(cat(A[k]))][str(cat(B[k]))] += 1
    ordinal = [(a, b) for _, a, b in graded if a in ORDINAL and b in ORDINAL]
    exact = sum(a == b for _, a, b in graded)
    per_grade = {}
    for g in GRADES:
        na, nb, nab = sum(a == g for _, a, _ in graded), sum(b == g for _, _, b in graded), sum(a == b == g for _, a, b in graded)
        per_grade[str(g)] = {"a": na, "b": nb, "both": nab, "specific_agreement": round(2 * nab / (na + nb), 4) if na + nb else None}
    conflict_pairs = [(a, b) for _, a, b in graded if -1 in (a, b)]
    binary = [(int(a >= 2), int(b >= 2)) for a, b in ordinal]
    metrics = {
        "pairs_labelled_by_a": len(A), "pairs_labelled_by_b": len(B), "pairs_labelled_by_both": len(both),
        "pairs_graded_by_both_excluding_needs_review": len(graded),
        "exact_agreement": round(exact / len(graded), 4) if graded else None,
        "per_grade": per_grade, "confusion_matrix_a_rows_b_cols": conf,
        "kappa_scale": "ordinal grades 0..3 only; pairs where either annotator gave -1 or needs_review are excluded and reported separately",
        "weighted_kappa_quadratic_0_3": weighted_kappa(ordinal, ORDINAL, "quadratic"),
        "weighted_kappa_linear_0_3": weighted_kappa(ordinal, ORDINAL, "linear"),
        "unweighted_kappa_0_3": weighted_kappa(ordinal, ORDINAL, "none"),
        "binary_relevant_kappa_ge2": weighted_kappa(binary, (0, 1), "none"),
        "pairs_in_kappa": len(ordinal),
        "conflicting_minus1": {"a": sum(a == -1 for _, a, _ in graded), "b": sum(b == -1 for _, _, b in graded),
                               "both": sum(a == b == -1 for _, a, b in graded), "pairs_with_any_minus1": len(conflict_pairs)},
        "needs_review_rate": {"a": round(sum(x["needs_review"] for x in A.values()) / len(A), 4) if A else None,
                              "b": round(sum(x["needs_review"] for x in B.values()) / len(B), 4) if B else None},
        "disagreement_rate_by_grade_of_a": {str(g): (round(sum(a == g and a != b for _, a, b in graded) / max(1, sum(a == g for _, a, _ in graded)), 4)) for g in GRADES},
        "grade_distribution": {"a": dict(Counter(str(a) for _, a, _ in graded)), "b": dict(Counter(str(b) for _, _, b in graded))},
    }
    dis = []
    for k in both:
        a, b = A[k], B[k]
        if a["needs_review"] or b["needs_review"] or a["grade"] != b["grade"]:
            kind = "needs_review" if (a["needs_review"] or b["needs_review"]) else (
                "conflicting_involved" if -1 in (a["grade"], b["grade"]) else
                "relevance_boundary_1_vs_2" if {a["grade"], b["grade"]} == {1, 2} else
                "relevant_vs_irrelevant" if (a["grade"] >= 2) != (b["grade"] >= 2) else "adjacent_or_other")
            dis.append({"question_id": k[0], "chunk_id": k[1], "item_id": a["item_id"], "kind": kind,
                        "grade_a": a["grade"], "grade_b": b["grade"], "needs_review_a": a["needs_review"], "needs_review_b": b["needs_review"],
                        "rationale_a": a["rationale"], "rationale_b": b["rationale"], "evidence_span_a": a["evidence_span"],
                        "evidence_span_b": b["evidence_span"], "review_note_a": a["review_note"], "review_note_b": b["review_note"]})
    metrics["disagreements"] = len(dis)
    metrics["disagreement_kinds"] = dict(Counter(d["kind"] for d in dis))
    return metrics, dis


# ========================================================================================== finalize
def validate_adjudication(adj: list[dict], dis_keys: set[tuple[str, str]], annotator_ids: set[str]) -> list[str]:
    errs, seen = [], set()
    for i, r in enumerate(adj, 1):
        k = (r.get("question_id"), r.get("chunk_id"))
        if k in seen:
            errs.append(f"adjudication {i}: duplicate decision for {k}")
        seen.add(k)
        if k not in dis_keys:
            errs.append(f"adjudication {i}: {k} is not a disagreement")
        if r.get("final_grade") not in GRADES:
            errs.append(f"adjudication {i}: final_grade must be in -1..3 (use status 'pending' instead of guessing)")
        if not str(r.get("reason", "")).strip() or not str(r.get("adjudicator_id", "")).strip():
            errs.append(f"adjudication {i}: reason and adjudicator_id are required")
        if r.get("adjudicator_id") in annotator_ids:
            errs.append(f"adjudication {i}: adjudicator must not be annotator A or B")
    return errs


def finalize(labels_a: list[dict], labels_b: list[dict], adj: list[dict], annotators: dict | None = None) -> list[dict]:
    """Agreed grade if A == B (neither needs_review); adjudicated grade if decided; otherwise pending (grade None).
    Never averages; never fills unlabelled pairs."""
    A = {(x["question_id"], x["chunk_id"]): x for x in labels_a}
    B = {(x["question_id"], x["chunk_id"]): x for x in labels_b}
    D = {(r["question_id"], r["chunk_id"]): r for r in adj}
    out = []
    for k in sorted(set(A) | set(B)):
        a, b = A.get(k), B.get(k)
        rec = {"question_id": k[0], "chunk_id": k[1], "item_id": (a or b)["item_id"],
               "annotation_code_a": a and a["annotation_code"], "annotation_code_b": b and b["annotation_code"],
               "grade_a": a and a["grade"], "grade_b": b and b["grade"],
               "needs_review_a": bool(a and a["needs_review"]), "needs_review_b": bool(b and b["needs_review"]),
               "rationale_a": a and a["rationale"], "rationale_b": b and b["rationale"],
               "evidence_span_a": a and a["evidence_span"], "evidence_span_b": b and b["evidence_span"]}
        if a and b and not a["needs_review"] and not b["needs_review"] and a["grade"] == b["grade"] and a["grade"] is not None:
            rec.update(final_grade=a["grade"], adjudication_status="agreed", adjudicator_id=None, adjudication_reason=None)
        elif k in D:
            d = D[k]
            rec.update(final_grade=d["final_grade"], adjudication_status="adjudicated", adjudicator_id=d["adjudicator_id"],
                       adjudication_reason=d["reason"])
        elif a and b:
            rec.update(final_grade=None, adjudication_status="pending_adjudication", adjudicator_id=None, adjudication_reason=None)
        else:
            rec.update(final_grade=None, adjudication_status="single_annotator_only", adjudicator_id=None, adjudication_reason=None)
        rec["provenance"] = provenance(annotators)
        out.append(rec)
    return out


def provenance(annotators: dict | None) -> dict:
    """Who produced the labels. AI annotators are recorded as such; never presented as human labels."""
    people = {r: (annotators or {}).get(r) for r in ("a", "b", "adjudicator")}
    types = {v.get("type") for v in people.values() if isinstance(v, dict)}
    return {"pool": POOL.name, "pool_sha256_prefix": EXPECTED[POOL.name],
            "annotator_a": people["a"], "annotator_b": people["b"], "adjudicator": people["adjudicator"],
            "ai_labels_used": None if not types else "ai_model" in types,
            "label_tier": None if not types else ("silver_ai_dual_annotation" if "ai_model" in types else "gold_human_dual_annotation")}


def annotator_ids(people: dict) -> set[str]:
    return {"A", "B", "a", "b"} | {v["id"] for k, v in people.items() if k in ("a", "b") and isinstance(v, dict) and v.get("id")}


# ======================================================================================= agent batches
BATCH_FIELDS = ["annotation_code", "question_id", "question_vi", "document_title", "section", "page", "content"]
SHOW_TOOL_PATH = ROOT / "scripts" / "annotation_show_question.py"


def make_batches(annotator: str, max_pairs: int = 160) -> dict:
    """Split one annotator's package into batches of whole questions (package order kept) for annotator agents."""
    pkg = read_jsonl(ANN / f"annotator_{annotator}" / f"fts_blind_annotation_package_annotator_{annotator}_{TAG}.jsonl")
    order: list[str] = []
    for r in pkg:
        if r["question_id"] not in order:
            order.append(r["question_id"])
    n = Counter(r["question_id"] for r in pkg)
    batches, cur, size = [], [], 0
    for q in order:
        if cur and size + n[q] > max_pairs:
            batches.append(cur)
            cur, size = [], 0
        cur.append(q)
        size += n[q]
    batches.append(cur)
    base = ANN / f"annotator_{annotator}"
    index = {}
    for i, qs in enumerate(batches, 1):
        name = f"batch_{i:02d}"
        rows = [{f: r[f] for f in BATCH_FIELDS} for r in pkg if r["question_id"] in qs]
        write_new(base / "batches" / f"{name}.jsonl", jsonl_text(rows))
        index[name] = {"questions": qs, "pairs": len(rows)}
    write_new(base / "batches" / "index.json", json.dumps(index, ensure_ascii=False, indent=1) + "\n")
    write_new(base / "tools" / "show_question.py", SHOW_TOOL_PATH.read_text(encoding="utf-8"))
    return index


def collect(annotator: str) -> dict:
    """Merge the per-question label files an annotator agent wrote back onto its package rows (content kept for the
    evidence-span check). Missing codes stay unlabelled (never 0)."""
    base = ANN / f"annotator_{annotator}"
    pkg = {r["annotation_code"]: r for r in read_jsonl(base / f"fts_blind_annotation_package_annotator_{annotator}_{TAG}.jsonl")}
    got, problems = {}, []
    for f in sorted((base / "returned").glob("batch_*/*.jsonl")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{f.parent.name}/{f.name}:{i} invalid JSON")
                continue
            c = str(r.get("annotation_code", "")).strip()
            if c not in pkg:
                problems.append(f"{f.parent.name}/{f.name}:{i} unknown code {c!r}")
            elif c in got:
                problems.append(f"{f.parent.name}/{f.name}:{i} duplicate code {c}")
            else:
                got[c] = r
    merged = []
    for c, row in pkg.items():
        out = dict(row)
        if c in got:
            r = got[c]
            g = r.get("grade")
            out.update(grade="" if g is None else str(g), rationale=r.get("rationale") or "", evidence_span=r.get("evidence_span") or "",
                       confidence=r.get("confidence") or "", needs_review="yes" if r.get("needs_review") else "",
                       review_note=r.get("review_note") or "")
        merged.append(out)
    path = base / f"returned_merged_annotator_{annotator}_{TAG}.jsonl"
    path.write_text(jsonl_text(merged), encoding="utf-8", newline="\n")  # working file, regenerated on every collect
    return {"labelled_codes": len(got), "package_codes": len(pkg), "missing": len(pkg) - len(got), "problems": problems[:50],
            "problem_count": len(problems), "merged_file": str(path.relative_to(ROOT))}


# ================================================================================================ CLI
def load_returned(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        return read_jsonl(path)
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("verify", "package", "batches", "collect", "import", "agreement", "finalize"))
    ap.add_argument("--annotator", choices=("a", "b"))
    ap.add_argument("--returned", type=Path, help="import: the annotator's filled package (csv or jsonl)")
    ap.add_argument("--adjudication", type=Path, default=REPORTS / f"fts_annotation_adjudication_{TAG}.jsonl")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-live", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.command == "verify":
        res = verify(live=not args.no_live)
        if not args.check:
            write_new(REPORTS / f"fts_annotation_pool_integrity_{TAG}.json", json.dumps(res, ensure_ascii=False, indent=1) + "\n")
        print(json.dumps({k: res[k] for k in ("ok", "problems")} | {"checks": {k: v for k, v in res["checks"].items() if k != "frozen_files_sha256"}}, ensure_ascii=False, indent=1))
        return 0 if res["ok"] else 1
    if args.command == "package":
        res = package(check_only=args.check)
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if args.command == "batches":
        print(json.dumps({a: {k: v["pairs"] for k, v in make_batches(a).items()} for a in ("a", "b")}, indent=1))
        return 0
    if args.command == "collect":
        print(json.dumps(collect(args.annotator), ensure_ascii=False, indent=1))
        return 0
    code_map = {m["annotation_code"]: m for m in read_jsonl(next(COORD.glob("annotation_code_map_*.jsonl")))}
    if args.command == "import":
        labels, errors = parse_returned(load_returned(args.returned), code_map, args.annotator)
        print(json.dumps({"labels": len(labels), "errors": errors[:50], "error_count": len(errors)}, ensure_ascii=False, indent=1))
        if errors:
            return 1
        write_new(REPORTS / f"fts_blind_annotation_annotator_{args.annotator}_{TAG}.jsonl", jsonl_text(labels))
        return 0
    la = read_jsonl(REPORTS / f"fts_blind_annotation_annotator_a_{TAG}.jsonl")
    lb = read_jsonl(REPORTS / f"fts_blind_annotation_annotator_b_{TAG}.jsonl")
    metrics, dis = agreement(la, lb)
    if args.command == "agreement":
        write_new(REPORTS / f"fts_annotation_agreement_{TAG}.json", json.dumps(metrics, ensure_ascii=False, indent=1) + "\n")
        write_new(REPORTS / f"fts_annotation_disagreement_{TAG}.csv", csv_text(dis, list(dis[0]) if dis else ["question_id"], bom=True))
        print(json.dumps({k: v for k, v in metrics.items() if k != "confusion_matrix_a_rows_b_cols"}, ensure_ascii=False, indent=1))
        return 0
    adj = read_jsonl(args.adjudication) if args.adjudication.exists() else []
    people = json.loads((COORD / "annotators.json").read_text(encoding="utf-8")) if (COORD / "annotators.json").exists() else {}
    errs = validate_adjudication(adj, {(d["question_id"], d["chunk_id"]) for d in dis}, annotator_ids(people))
    if errs:
        print(json.dumps({"adjudication_errors": errs}, ensure_ascii=False, indent=1))
        return 1
    final = finalize(la, lb, adj, people)
    write_new(REPORTS / f"fts_blind_annotation_final_{TAG}.jsonl", jsonl_text(final))
    print(json.dumps(dict(Counter(r["adjudication_status"] for r in final)), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
