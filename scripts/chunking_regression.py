"""Compare two chunking profiles on every non-quarantined corpus document (no DB writes, no network).

Metrics per profile: chunks, eligible chunks, tokens, text coverage, noise (retrievable chunks that
contain removed header/footer lines or look like reference/contributor lists), table integrity,
page provenance, and hash stability (the candidate profile is run twice).

Usage:
  python -B scripts/chunking_regression.py --base section_v1 --candidate section_v2
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

from app.config import CORPUS_MANIFEST, REPORTS, ROOT
from app.ingest.chunking import (
    NOT_RETRIEVABLE,
    TABLE_CAPTION,
    ChunkingProfile,
    ChunkingResult,
    DocumentInfo,
    HFTokenCounter,
    chunk_document,
    classify_section,
    detect_list_type,
)


def run(profile: ChunkingProfile, counter: HFTokenCounter, docs: list[dict]) -> dict[str, ChunkingResult]:
    out = {}
    for m in docs:
        info = DocumentInfo(m["source_id"], m["source_id"], m["title"], m["tier"], m["source_type"], "en",
                            m["conversion_gaps"])
        out[m["source_id"]] = chunk_document((ROOT / m["path"]).read_text(encoding="utf-8-sig"), info, profile, counter)
    return out


def fingerprint(results: dict[str, ChunkingResult]) -> str:
    h = hashlib.sha256()
    for sid in sorted(results):
        for c in results[sid].chunks:
            h.update(f"{sid}|{c.chunk_index}|{c.content_sha256}|{c.section_type}|{c.retrieval_eligible}\n".encode())
    return h.hexdigest()


def metrics(results: dict[str, ChunkingResult], boilerplate: set[str], paged: set[str]) -> dict:
    chunks = [c for r in results.values() for c in r.chunks]
    eligible = [c for c in chunks if c.retrieval_eligible]
    tokens = [c.token_count for c in chunks]
    tables = [c for c in chunks if c.content_kind == "table"]
    paged_chunks = [c for sid in paged for c in results[sid].chunks]
    body = sum(r.body_chars for r in results.values())
    return {
        "documents": len(results), "chunks": len(chunks), "eligible": len(eligible),
        "tokens": {"min": min(tokens), "median": int(statistics.median(tokens)), "max": max(tokens),
                   "over_600": sum(t > 600 for t in tokens), "over_700": sum(t > 700 for t in tokens),
                   "under_60": sum(t < 60 for t in tokens),
                   "under_60_eligible": sum(c.token_count < 60 for c in eligible)},
        "text_kept_pct": round(100 * sum(r.kept_chars for r in results.values()) / body, 2),
        "dropped_chars": dict(sum((r.dropped for r in results.values()), Counter())),
        "noise": {
            "eligible_with_header_footer": sum(any(b in c.content for b in boilerplate) for c in eligible),
            "eligible_reference_like": sum(detect_list_type(c.content) == "references_detected" for c in eligible
                                           if c.content_kind == "text"),
            "eligible_contributor_like": sum(detect_list_type(c.content) == "contributors_detected" for c in eligible
                                             if c.content_kind == "text"),
        },
        "tables": {"chunks": len(tables), "with_caption": sum(bool(TABLE_CAPTION.match(c.content)) for c in tables),
                   "with_header_separator": sum("|---|" in c.content for c in tables),
                   "floating": sum(c.section_type == "floating_table" for c in tables)},
        "section_types": dict(Counter(c.section_type for c in chunks).most_common()),
        "completeness": dict(Counter(c.completeness_status for c in chunks)),
        "page_provenance_paged_docs_pct": round(100 * sum(c.page_start is not None for c in paged_chunks)
                                                / max(1, len(paged_chunks)), 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="section_v1")
    parser.add_argument("--candidate", default="section_v2")
    args = parser.parse_args()
    base, cand = ChunkingProfile.load(args.base), ChunkingProfile.load(args.candidate)
    counter = HFTokenCounter(cand.tokenizer_path, cand.tokenizer_sha256)
    manifest = [json.loads(x) for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]
    docs = [m for m in manifest if not m["text_fidelity_warning"]]  # quarantined documents are not chunked

    base_res = run(base, counter, docs)
    cand_res = run(cand, counter, docs)
    cand_again = run(cand, counter, docs)
    boilerplate = {ex for r in cand_res.values() if r.layout
                   for reason, examples in r.layout.removed_examples.items() if reason == "header_footer"
                   for ex in examples if len(ex) >= 40}  # shorter fragments occur in real prose
    paged = {m["source_id"] for m in docs if "<!-- SOURCE_PDF_PAGE" in (ROOT / m["path"]).read_text(encoding="utf-8")}
    layout_docs = sorted(sid for sid, r in cand_res.items() if r.layout)

    # Chunks of non-PDF documents that the base profile would have retrieved but the candidate excludes
    # (judged by the base profile's section rules on the same section path): candidates for false positives.
    newly_excluded = []
    for sid, r in cand_res.items():
        if sid in layout_docs:
            continue
        for c in r.chunks:
            base_type = classify_section(c.section_path, "body")
            if not c.retrieval_eligible and base_type not in NOT_RETRIEVABLE and c.section_type != "floating_table":
                newly_excluded.append({"source_id": sid, "chunk_index": c.chunk_index, "section_type": c.section_type,
                                       "base_section_type": base_type, "section_path": list(c.section_path),
                                       "content": c.content[:300]})

    per_doc = {sid: {"base_chunks": len(base_res[sid].chunks), "cand_chunks": len(cand_res[sid].chunks),
                     "base_eligible": sum(c.retrieval_eligible for c in base_res[sid].chunks),
                     "cand_eligible": sum(c.retrieval_eligible for c in cand_res[sid].chunks)}
               for sid in sorted(cand_res)}
    report = {
        "date": date.today().isoformat(), "base": args.base, "candidate": args.candidate,
        "quarantined_excluded": sorted(m["source_id"] for m in manifest if m["text_fidelity_warning"]),
        "layout_documents": layout_docs, "paged_documents": sorted(paged),
        "boilerplate_probe_strings": sorted(boilerplate),
        "base_metrics": metrics(base_res, boilerplate, paged),
        "candidate_metrics": metrics(cand_res, boilerplate, paged),
        "candidate_hash_run1": fingerprint(cand_res), "candidate_hash_run2": fingerprint(cand_again),
        "candidate_deterministic": fingerprint(cand_res) == fingerprint(cand_again),
        "non_layout_chunks_newly_excluded": newly_excluded,
        "per_document": per_doc,
        "layout_headings": {sid: [{"level": lv, "text": t, "signal": s} for lv, t, s in cand_res[sid].layout.headings]
                            for sid in layout_docs},
        "layout_running_titles": {sid: cand_res[sid].layout.running_titles for sid in layout_docs},
    }
    out = REPORTS / f"{report['date']}_chunking_regression_{args.base}_vs_{args.candidate}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {k: report[k] for k in ("candidate_deterministic",)}
    summary |= {"base": report["base_metrics"], "candidate": report["candidate_metrics"],
                "non_layout_newly_excluded": len(newly_excluded), "report": out.relative_to(ROOT).as_posix()}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
