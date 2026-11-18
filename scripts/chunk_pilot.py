"""Chunk a pilot set of documents, store the chunks, and write a review report.

No external API is called. Chunks are stored with the documents' current (unapproved) status,
so none of them can reach retrieval until a reviewer approves the document and its rights.

Usage:
  python -B scripts/chunk_pilot.py                       # default pilot set, profile section_v1
  python -B scripts/chunk_pilot.py --profile section_v2  # v1 set + the two other PDF-derived documents
  python -B scripts/chunk_pilot.py --sources A B C       # custom set
  python -B scripts/chunk_pilot.py --no-db               # report only
  python -B scripts/chunk_pilot.py --review-quarantined  # chunk the quarantined documents for human review
                                                         # (report only; never written to the database)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from psycopg.types.json import Jsonb

from app.config import CORPUS_MANIFEST, REPORTS, ROOT
from app.db import connect
from app.ingest.chunk_store import chunk_id, replace_document_chunks
from app.ingest.chunking import ChunkingProfile, ChunkingResult, DocumentInfo, HFTokenCounter, chunk_document

# Chosen to cover each structural variant seen in the Phase 0 audit.
DEFAULT_PILOT = {
    "ASD-CSV-002": "core · review, deep heading hierarchy (5 levels)",
    "ASD-CSV-062": "core · research article with HTML tables and MathML",
    "ASD-OA-PMC7407189": "core · long review (sleep), many sections",
    "CDC-EARLY-INTERVENTION": "core · short public-health web page",
    "NIH-NIMH-MEDICATIONS": "core · patient information on medications (safety-relevant)",
    "ASD-CSV-007": "gaps · meta-analysis, unlabeled abstract in front matter, figures missing",
    "NIHR-SENITA-2022": "gaps · 172-page PDF report without Markdown headings",
    "WHO-CST-INTRO-2022": "gaps · PDF-derived training manual without headings",
}
# section_v2 targets PDF-derived text, so its pilot adds the remaining two PDF documents.
DEFAULT_PILOT_V2 = DEFAULT_PILOT | {
    "WHO-CST-PARTICIPANTS-2022": "gaps · PDF workbook: session running headers, repeated form labels",
    "WHO-ECD-GUIDELINE-2020": "gaps · PDF guideline: ALL CAPS headings, flattened GRADE tables",
}
QUARANTINED_REVIEW = {
    "ASD-CSV-077": "quarantined · FYI cut-off cell lost <break/> separators",
    "NIH-NIMH-CHILDREN": "quarantined · list items inside a 2-column table",
}
REVIEW_SAMPLES_PER_PDF = 4


def load_documents(conn, source_ids: list[str], allow_quarantined: bool = False) -> list[tuple[DocumentInfo, Path]]:
    rows = conn.execute(
        """SELECT d.document_id, d.source_id, s.title, s.corpus_role, s.source_type, d.corpus_relative_path,
                  d.missing_components, d.file_sha256, d.content_review_status
           FROM documents d JOIN sources s USING (source_id)
           WHERE d.is_current AND d.source_id = ANY(%s)""", (source_ids,)).fetchall()
    found = {r[1] for r in rows}
    if missing := sorted(set(source_ids) - found):
        raise SystemExit(f"Unknown or non-current documents: {missing}")
    out = []
    for doc_id, sid, title, role, stype, rel, missing_components, sha, review in rows:
        if review == "quarantined" and not allow_quarantined:
            raise SystemExit(f"{sid} is quarantined; it is excluded from chunking until reviewed")
        path = ROOT / rel
        if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            raise SystemExit(f"{sid}: corpus file hash differs from documents.file_sha256")
        out.append((DocumentInfo(sid, doc_id, title, role, stype, "en", missing_components or {}), path))
    return sorted(out, key=lambda x: source_ids.index(x[0].source_id))


def doc_summary(info: DocumentInfo, result: ChunkingResult, purpose: str) -> dict:
    tokens = [c.token_count for c in result.chunks]
    pages = [p for c in result.chunks for p in (c.page_start, c.page_end) if p]
    return {
        "source_id": info.source_id, "title": info.title, "corpus_role": info.corpus_role, "why_selected": purpose,
        "chunks": len(result.chunks),
        "retrieval_eligible": sum(c.retrieval_eligible for c in result.chunks),
        "tables": sum(c.content_kind == "table" for c in result.chunks),
        "with_overlap": sum(c.has_overlap for c in result.chunks),
        "tokens": {"min": min(tokens), "median": int(statistics.median(tokens)), "max": max(tokens),
                   "total": sum(tokens)} if tokens else {},
        "token_bands": dict(Counter("<100" if t < 100 else "100-349" if t < 350 else "350-600" if t <= 600
                                    else ">600" for t in tokens)),
        "section_types": dict(Counter(c.section_type for c in result.chunks).most_common()),
        "distinct_sections": len({c.section_path for c in result.chunks}),
        "completeness": dict(Counter(c.completeness_status for c in result.chunks)),
        "body_chars": result.body_chars, "kept_chars": result.kept_chars,
        "kept_pct": round(100 * result.kept_chars / result.body_chars, 1) if result.body_chars else None,
        "dropped_chars": dict(result.dropped),
        "missing_components": info.missing_components,
        "page_range": [min(pages), max(pages)] if pages else None,
    }


def pick_samples(info: DocumentInfo, result: ChunkingResult, profile: str) -> list[dict]:
    """Non-PDF documents: one body chunk and the first table. PDF-derived documents (layout pass): a spread
    for manual review — a retrievable chunk of each kind of section, an excluded chunk, a flattened table."""
    picks: dict[int, str] = {}
    eligible = [c for c in result.chunks if c.retrieval_eligible]
    if result.layout is None:
        if eligible:
            picks[eligible[len(eligible) // 3].chunk_index] = "retrievable body chunk"
        if tables := [c for c in eligible if c.content_kind == "table"]:
            picks[tables[0].chunk_index] = "first retrievable table"
    else:
        seen_types: set[str] = set()
        for c in sorted(eligible, key=lambda c: (c.section_type in ("body", "unclassified"), c.chunk_index)):
            if c.section_type not in seen_types and len(picks) < REVIEW_SAMPLES_PER_PDF - 2:
                seen_types.add(c.section_type)
                picks[c.chunk_index] = f"retrievable · {c.section_type} · section recovered by layout pass"
        excluded = [c for c in result.chunks
                    if not c.retrieval_eligible and c.completeness_status != "table_structure_lost"]
        if excluded:
            c = excluded[len(excluded) // 2]
            picks[c.chunk_index] = f"excluded from retrieval · {c.section_type}"
        if flat := [c for c in result.chunks if c.completeness_status == "table_structure_lost"]:
            picks[flat[0].chunk_index] = "excluded · flattened PDF table (table_structure_lost)"
    return [{
        "chunk_id": chunk_id(info.document_id, profile, c.chunk_index), "selection_reason": picks[c.chunk_index],
        "section_path": list(c.section_path), "section_type": c.section_type, "content_kind": c.content_kind,
        "pages": [c.page_start, c.page_end], "tokens": c.token_count, "retrieval_eligible": c.retrieval_eligible,
        "completeness_status": c.completeness_status, "missing_context": c.missing_context, "content": c.content,
    } for c in result.chunks if c.chunk_index in picks]


def write_markdown(path: Path, report: dict) -> None:
    lines = [
        f"# Chunking pilot — {report['profile']['name']} — {report['date']}", "",
        "Chưa gọi API bên ngoài. Chunk lưu trong DB nhưng tài liệu chưa được phê duyệt nên không truy xuất được.",
        "",
        "| source_id | vai trò | chunk | eligible | bảng | token min/median/max | % giữ | trang | đầy đủ |",
        "|---|---|---:|---:|---:|---|---:|---|---|",
    ]
    for d in report["documents"]:
        t = d["tokens"]
        completeness = ", ".join(f"{k}:{v}" for k, v in d["completeness"].items())
        lines.append(
            f"| {d['source_id']} | {d['corpus_role']} | {d['chunks']} | {d['retrieval_eligible']} | {d['tables']} "
            f"| {t.get('min')}/{t.get('median')}/{t.get('max')} | {d['kept_pct']} | {d['page_range'] or '—'} "
            f"| {completeness} |")
    lines += ["", "## Ví dụ chunk", ""]
    for s in report["samples"]:
        missing = f" — {s['missing_context']}" if s["missing_context"] else ""
        lines += [f"### {s['chunk_id']}",
                  f"- lý do chọn: {s['selection_reason']} · retrieval_eligible: {s['retrieval_eligible']}",
                  f"- section: {' > '.join(s['section_path']) or '(không có heading)'} · {s['section_type']} · "
                  f"{s['content_kind']} · {s['tokens']} tokens · trang {s['pages']}",
                  f"- completeness: {s['completeness_status']}{missing}",
                  "", "```text", s["content"], "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", default="section_v1")
    parser.add_argument("--sources", nargs="+")
    parser.add_argument("--no-db", action="store_true")
    parser.add_argument("--review-quarantined", action="store_true",
                        help="chunk the quarantined documents for review; implies --no-db")
    parser.add_argument("--all", action="store_true", help="every non-quarantined corpus document")
    args = parser.parse_args()

    profile = ChunkingProfile.load(args.profile)
    counter = HFTokenCounter(profile.tokenizer_path, profile.tokenizer_sha256)
    if args.review_quarantined:
        purposes, args.no_db = QUARANTINED_REVIEW, True
    elif args.all:
        manifest = [json.loads(x) for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]
        purposes = {m["source_id"]: "full corpus run" for m in manifest if not m["text_fidelity_warning"]}
    elif args.sources:
        purposes = dict.fromkeys(args.sources, "custom")
    else:
        purposes = DEFAULT_PILOT if profile.name == "section_v1" else DEFAULT_PILOT_V2
    source_ids = list(purposes)

    with connect("ingest", "chunk_pilot") as conn:
        documents = load_documents(conn, source_ids, allow_quarantined=args.review_quarantined)
        results = [(info, chunk_document(path.read_text(encoding="utf-8-sig"), info, profile, counter))
                   for info, path in documents]
        run_id = None
        if not args.no_db:
            run_id = conn.execute(
                "INSERT INTO ingestion_runs (run_type, code_version, configuration) VALUES ('chunking_pilot', %s, %s) "
                "RETURNING run_id", (f"chunking:{profile.name}", Jsonb(profile.as_config()))).fetchone()[0]
            for info, result in results:
                n = replace_document_chunks(conn, info, profile.name, result.chunks)
                conn.execute("INSERT INTO ingestion_run_documents (run_id, document_id, status, chunk_count) "
                             "VALUES (%s, %s, 'succeeded', %s)", (run_id, info.document_id, n))
            conn.execute("UPDATE ingestion_runs SET status='succeeded', finished_at=now(), stats=%s WHERE run_id=%s",
                         (Jsonb({"documents": len(results), "chunks": sum(len(r.chunks) for _, r in results)}), run_id))

    report = {
        "date": date.today().isoformat(), "profile": profile.as_config() | {"name": profile.name},
        "run_id": str(run_id) if run_id else None, "external_api_called": False,
        "documents": [doc_summary(info, r, purposes[info.source_id]) for info, r in results],
        "samples": [s for info, r in results for s in pick_samples(info, r, profile.name)],
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    kind = "quarantine_chunks" if args.review_quarantined else ("chunking_full" if args.all else "chunking_pilot")
    stem = REPORTS / f"{report['date']}_{kind}_{profile.name}"
    stem.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(stem.with_suffix(".md"), report)
    print(json.dumps({"run_id": report["run_id"], "report": stem.relative_to(ROOT).as_posix() + ".{json,md}",
                      "documents": [{k: d[k] for k in ("source_id", "chunks", "retrieval_eligible", "kept_pct")}
                                    | {"tokens": d["tokens"]} for d in report["documents"]]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
