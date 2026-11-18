"""Candidate-pool judgments (Phase 6.2 T2.3.2): merge into retrieval_eval_v1 and validate. Reads files only:
no database connection, no network, no provider API.

The judgments file is an *extension* of the original dataset, never an in-place edit. One JSONL row per
(question_id, chunk_id, annotator) for every row of the T2.3.1 dense candidate pool, with a status:

  judged              grade -1..3 + rationale; merged into the v1 record's `judgments`
  needs_adjudication  provisional grade + rationale; NOT merged (stays in `candidate_chunk_ids`)
  excluded            no grade, has exclusion_reason; NOT merged, not a candidate (e.g. out-of-scope question)
  unjudged            no grade; NOT merged (stays in `candidate_chunk_ids`) — never read as grade 0

merge(original, rows) is deterministic, so the merged dataset is reproducible from the original file plus the
judgments file (`merge --check` re-derives it and compares bytes).

Usage:
  python -B scripts/candidate_judgments.py merge    [--original P] [--judgments P] [--out P] [--check]
  python -B scripts/candidate_judgments.py validate [--original P] [--judgments P] [--merged P] [--report P]
Exit code 0 = valid, 1 = errors.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "eval" / "datasets"
REPORTS = ROOT / "eval" / "reports"
ORIGINAL = DS / "retrieval_eval_v1.jsonl"
JUDGMENTS = DS / "retrieval_eval_v1_candidate_judgments_2026-11-14.jsonl"
JUDGMENTS_SCHEMA = DS / "retrieval_eval_v1_candidate_judgments_schema.json"
MERGED = DS / "retrieval_eval_v1_merged_2026-11-14.jsonl"
SCHEMA = DS / "retrieval_eval_v1_schema.json"
MANIFEST = REPORTS / "embedding_manifest.csv"
ALLOWLIST = REPORTS / "research_authorization_allowlist_rev_d1_2026-11-14.csv"
EXCLUSIONS = REPORTS / "research_authorization_d1_exclusions_2026-11-14.csv"
POOL = REPORTS / "phase_6_2_t2_3_1_candidate_pool_expansion_2026-11-14.csv"

STATUSES = ("judged", "needs_adjudication", "excluded", "unjudged")
GRADE_CLASS = {3: "relevant", 2: "relevant", 1: "partial", 0: "negative", -1: "conflicting"}
JUDGMENT_KEYS = ("chunk_id", "document_id", "source_id", "content_sha256", "grade", "evidence_class", "aspect",
                 "rationale_vi")
PENDING = ("unjudged", "needs_adjudication")


class MergeError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_jsonl(records: list[dict]) -> str:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def judgment_id(question_id: str, chunk_id: str, annotator_id: str | None) -> str:
    return hashlib.sha256(f"{question_id}|{chunk_id}|{annotator_id or '-'}".encode()).hexdigest()[:20]


def merge(original: list[dict], rows: list[dict], judgments_name: str, judgments_sha: str) -> list[dict]:
    """Original records + judged rows -> merged records. Original judgments are kept untouched and first."""
    by_q: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_q[row["question_id"]].append(row)
    unknown = set(by_q) - {r["question_id"] for r in original}
    if unknown:
        raise MergeError(f"judgments for unknown questions: {sorted(unknown)}")
    merged = []
    for rec in original:
        r = copy.deepcopy(rec)
        qrows = sorted(by_q.get(r["question_id"], []), key=lambda x: x["chunk_id"])
        before = {j["chunk_id"] for j in r["judgments"]}
        new = [row for row in qrows if row["status"] == "judged"]
        for row in new:
            if row["chunk_id"] in before:
                raise MergeError(f"{r['question_id']}: {row['chunk_id']} already judged in the original dataset")
            r["judgments"].append({k: row[k] for k in JUDGMENT_KEYS})
        judged = {j["chunk_id"]: j["grade"] for j in r["judgments"]}
        rel = [j for j in r["judgments"] if j["grade"] >= 2]
        r["relevance_grade"] = judged
        r["relevant_chunk_ids"] = [j["chunk_id"] for j in rel]
        r["relevant_document_ids"] = sorted({j["document_id"] for j in rel})
        r["expected_sources"] = sorted({j["source_id"] for j in rel})
        cands = [c for c in r["candidate_chunk_ids"] if c not in judged]
        cands += [row["chunk_id"] for row in qrows
                  if row["status"] in PENDING and row["chunk_id"] not in judged and row["chunk_id"] not in cands]
        r["candidate_chunk_ids"] = cands
        if cands and r["annotation_completeness"] == "complete_for_judged_pool":
            r["annotation_completeness"] = "partial"
        n = Counter(row["status"] for row in qrows)
        if qrows:
            r["search_log"] = r["search_log"] + [
                f"T2.3.2: pool dense top-20 (T2.3.1) — judged {n['judged']}, needs_adjudication "
                f"{n['needs_adjudication']}, unjudged {n['unjudged']}, excluded {n['excluded']}; "
                f"nguồn {judgments_name} sha256 {judgments_sha[:16]}"]
        if new:
            r["annotation_method"] += (" + T2.3.2: chấm mù toàn văn các ứng viên pool dense (ẩn rank/điểm cosine), "
                                       "cùng annotator A1")
        adj = [row for row in qrows if row["status"] == "needs_adjudication"]
        if adj:
            r["annotation_notes"] = (r["annotation_notes"] + " " if r["annotation_notes"] else "") + " ".join(
                f"[T2.3.2 cần phân xử: {row['source_id']}#{row['chunk_id'][-4:]} tạm {row['grade']} — "
                f"{row['rationale_vi']}]" for row in adj)
        merged.append(r)
    return merged


def _load_v1_validator():
    spec = importlib.util.spec_from_file_location("validate_retrieval_eval", ROOT / "scripts" /
                                                  "validate_retrieval_eval.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_rows(rows: list[dict], schema: dict, original: list[dict], manifest: dict[str, dict],
                  allowlist: set[str], excluded_d1: set[str], pool: dict[tuple[str, str], dict],
                  corpus_pin: dict) -> list[str]:
    """Checks 1–6 and 9–13 on the judgments file itself."""
    errors: list[str] = []
    props, required = schema["properties"], schema["required"]
    qids = {r["question_id"] for r in original}
    seen: Counter = Counter()
    for n, row in enumerate(rows, 1):
        tag = f"row {n} {row.get('question_id', '?')}/{str(row.get('chunk_id', '?'))[-24:]}"
        missing = [k for k in required if k not in row]
        extra = [k for k in row if k not in props]
        if missing or extra:  # 1 schema
            errors.append(f"{tag}: schema (missing {missing}, unexpected {extra})")
            continue
        st, g = row["status"], row["grade"]
        if row["question_id"] not in qids:  # 2
            errors.append(f"{tag}: unknown question_id")
        m = manifest.get(row["chunk_id"])
        if m is None:  # 3
            errors.append(f"{tag}: chunk not in the embedded set")
        elif (m["document_id"], m["source_id"], m["content_hash"]) != (row["document_id"], row["source_id"],
                                                                       row["content_sha256"]):  # 11
            errors.append(f"{tag}: source/document/content hash mismatch with the manifest")
        if st not in STATUSES:  # 5
            errors.append(f"{tag}: status {st!r} not allowed")
        if st in ("judged", "needs_adjudication"):  # 4
            if g not in GRADE_CLASS:
                errors.append(f"{tag}: grade {g!r} not in {{-1,0,1,2,3}}")
            elif row["evidence_class"] != GRADE_CLASS[g]:
                errors.append(f"{tag}: evidence_class does not match grade")
            if not row["annotator"] or not row["annotated_at"]:  # 10
                errors.append(f"{tag}: judged row without annotator/timestamp")
        elif g is not None or row["evidence_class"] is not None:  # 4/8: unjudged/excluded carry no grade
            errors.append(f"{tag}: {st} row must not carry a grade")
        if st in ("judged", "needs_adjudication", "excluded") and not (row["rationale_vi"] or "").strip():  # 12
            errors.append(f"{tag}: missing rationale")
        if st == "excluded" and not (row["exclusion_reason"] or "").strip():
            errors.append(f"{tag}: excluded without exclusion_reason")
        key = (row["question_id"], row["chunk_id"], (row["annotator"] or {}).get("annotator_id"))
        seen[key] += 1
        if seen[key] == 2:  # 6
            errors.append(f"{tag}: duplicate judgment for (question, chunk, annotator)")
        if row["chunk_id"] in excluded_d1:  # 9
            errors.append(f"{tag}: D-1 excluded (reference-list) chunk brought back")
        if row["chunk_id"] not in allowlist:  # 13
            errors.append(f"{tag}: chunk outside the active research authorization allowlist")
        p = pool.get((row["question_id"], row["chunk_id"]))
        if p is None or p["source_id"] != row["source_id"]:  # 10 provenance
            errors.append(f"{tag}: not traceable to the T2.3.1 candidate pool")
        elif (row["origin"].get("rank") != int(p["rank"]) or row["origin"].get("suggested_review_priority")
              != p["suggested_review_priority"]):
            errors.append(f"{tag}: origin rank/priority differs from the pool file")
        if row["corpus"] != corpus_pin:  # 10
            errors.append(f"{tag}: corpus/authorization pin differs")
    pairs = Counter((r.get("question_id"), r.get("chunk_id")) for r in rows)
    errors += [f"{q}/{c[-24:]}: more than one row for the pair" for (q, c), v in pairs.items() if v > 1]
    return errors


def validate_merge(original: list[dict], rows: list[dict], merged: list[dict], merged_text: str,
                   judgments_name: str, judgments_sha: str) -> list[str]:
    """Checks 7, 8 and 14 (old labels kept, unjudged never becomes 0, merge reproducible)."""
    errors: list[str] = []
    try:
        rebuilt = merge(original, rows, judgments_name, judgments_sha)
    except MergeError as exc:
        return [f"merge failed: {exc}"]
    if dump_jsonl(rebuilt) != merged_text:  # 14
        errors.append("merged file is not reproducible from original + judgments")
    mq = {r["question_id"]: r for r in merged}
    if [r["question_id"] for r in original] != [r["question_id"] for r in merged]:
        errors.append("merged question list differs from the original")
    judged_rows = {(r["question_id"], r["chunk_id"]): r for r in rows if r["status"] == "judged"}
    other = {(r["question_id"], r["chunk_id"]) for r in rows if r["status"] != "judged"}
    for rec in original:
        m = mq.get(rec["question_id"])
        if m is None:
            continue
        n0 = len(rec["judgments"])
        if m["judgments"][:n0] != rec["judgments"]:  # 7
            errors.append(f"{rec['question_id']}: original judgments changed or lost")
        for j in m["judgments"][n0:]:
            k = (rec["question_id"], j["chunk_id"])
            if k in other:  # 8
                errors.append(f"{k[0]}: non-judged candidate {k[1][-24:]} appears as a judgment (grade {j['grade']})")
            elif k not in judged_rows or {x: judged_rows[k][x] for x in JUDGMENT_KEYS} != j:
                errors.append(f"{k[0]}: merged judgment {k[1][-24:]} has no matching judged row")
        lost = set(rec["candidate_chunk_ids"]) - set(m["candidate_chunk_ids"]) - set(m["relevance_grade"])
        if lost:
            errors.append(f"{rec['question_id']}: original candidates dropped without a judgment: {len(lost)}")
        for (q, c) in other:
            if q == rec["question_id"] and c in m["relevance_grade"] and c not in rec["relevance_grade"]:
                errors.append(f"{q}: unjudged/adjudication/excluded chunk {c[-24:]} has a grade")
    return errors


def corpus_pin() -> dict:
    return {"chunking_profile": "section_v2_1", "embedding_profile": "cohere_embed_v4_1536_v1",
            "embedding_manifest_sha256": sha256_file(MANIFEST), "authorization_id": 2,
            "authorization_allowlist": ALLOWLIST.name, "authorization_allowlist_sha256": sha256_file(ALLOWLIST)}


def run_validate(original_p: Path, judgments_p: Path, merged_p: Path) -> dict:
    original, rows = read_jsonl(original_p), read_jsonl(judgments_p)
    merged_text = merged_p.read_text(encoding="utf-8")
    merged = [json.loads(x) for x in merged_text.splitlines() if x.strip()]
    v1 = _load_v1_validator()
    manifest = v1.load_manifest(MANIFEST)
    allowlist = {r["chunk_id"] for r in read_csv(ALLOWLIST)}
    excluded_d1 = {r["chunk_id"] for r in read_csv(EXCLUSIONS)}
    pool = {(r["question_id"], r["chunk_id"]): r for r in read_csv(POOL)}
    jschema = json.loads(JUDGMENTS_SCHEMA.read_text(encoding="utf-8"))
    j_sha = sha256_file(judgments_p)
    errors = validate_rows(rows, jschema, original, manifest, allowlist, excluded_d1, pool, corpus_pin())
    errors += validate_merge(original, rows, merged, merged_text, judgments_p.name, j_sha)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    manifest_sha = sha256_file(MANIFEST)
    v_orig = v1.validate(original_p.read_text(encoding="utf-8").splitlines(), schema, manifest, manifest_sha)
    v_merged = v1.validate(merged_text.splitlines(), schema, manifest, manifest_sha)
    errors += [f"original: {e}" for e in v_orig["errors"]] + [f"merged: {e}" for e in v_merged["errors"]]
    covered = {(r["question_id"], r["chunk_id"]) for r in rows}
    missing_pool = set(pool) - covered
    if missing_pool:
        errors.append(f"{len(missing_pool)} pool rows have no status row (every pool row must be accounted for)")
    return {"ok": not errors, "errors": errors, "warnings": v_merged["warnings"],
            "files": {"original": [original_p.name, sha256_file(original_p)],
                      "judgments": [judgments_p.name, j_sha], "merged": [merged_p.name, sha256_file(merged_p)],
                      "pool": [POOL.name, sha256_file(POOL)], "manifest": [MANIFEST.name, manifest_sha],
                      "allowlist": [ALLOWLIST.name, sha256_file(ALLOWLIST)]},
            "status_counts": dict(Counter(r["status"] for r in rows)),
            "grade_counts_judged": {str(k): v for k, v in sorted(Counter(
                r["grade"] for r in rows if r["status"] == "judged").items())},
            "stats_original": v_orig["stats"], "stats_merged": v_merged["stats"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("merge", "validate"))
    parser.add_argument("--original", type=Path, default=ORIGINAL)
    parser.add_argument("--judgments", type=Path, default=JUDGMENTS)
    parser.add_argument("--out", "--merged", dest="merged", type=Path, default=MERGED)
    parser.add_argument("--check", action="store_true", help="merge: compare with the existing file, write nothing")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.command == "merge":
        text = dump_jsonl(merge(read_jsonl(args.original), read_jsonl(args.judgments), args.judgments.name,
                                sha256_file(args.judgments)))
        if args.check:
            same = args.merged.exists() and args.merged.read_text(encoding="utf-8") == text
            print(json.dumps({"reproducible": same, "sha256": hashlib.sha256(text.encode()).hexdigest()}))
            return 0 if same else 1
        if args.merged.exists() and args.merged.read_text(encoding="utf-8") != text:
            print(f"refusing to overwrite a different {args.merged.name}; use a new --out path", file=sys.stderr)
            return 1
        args.merged.write_text(text, encoding="utf-8", newline="\n")
        print(json.dumps({"written": str(args.merged), "sha256": sha256_file(args.merged)}))
        return 0
    result = run_validate(args.original, args.judgments, args.merged)
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
