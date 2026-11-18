"""Look for ruled tables in the ORIGINAL PDF on the pages of flattened-table chunks (no network, no DB).

For each page that holds a chunk flagged as a flattened table (profile section_v2_1), pdfplumber's
line-based table finder is run on the original PDF. A candidate passes the automated checks only if:
  * it is rectangular with >= 2 rows and >= 2 columns, and <= 50% of cells are empty;
  * >= 90% of its alphanumeric tokens occur in the already-extracted text of the same page
    (so no value is introduced that the corpus text does not contain).
Passing candidates are written for HUMAN REVIEW; they are never made retrievable here. Cells are kept
verbatim (no value is inferred, no unit or footnote dropped); empty cells stay empty.

Output: data/extractions/<source_id>/tables.pdfplumber-<version>.v1.jsonl  (+ a run summary on stdout)

Usage:
  python -u -B scripts/pdf_table_recovery.py
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import CORPUS_MANIFEST, ROOT
from app.ingest.chunking import ChunkingProfile, DocumentInfo, HFTokenCounter, chunk_document

PROFILE = "section_v2_1"
TOKEN = re.compile(r"[A-Za-z0-9]+(?:[.,][0-9]+)?")
MIN_COVERAGE, MAX_EMPTY = 0.9, 0.5


def tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text or "")]


def check(rows: list[list[str | None]], page_text: str) -> dict:
    n_rows, widths = len(rows), {len(r) for r in rows}
    cells = [c for r in rows for c in r]
    empty = sum(not (c or "").strip() for c in cells) / max(1, len(cells))
    table_tokens = [t for c in cells for t in tokens(c)]
    page_tokens = set(tokens(page_text))
    coverage = sum(t in page_tokens for t in table_tokens) / max(1, len(table_tokens))
    # Header words must be readable too: rotated header text comes out reversed ("seiduts fo .oN") while the
    # numbers still match, which would pass a whole-table coverage check.
    header_tokens = [t for c in (rows[0] if rows else []) for t in tokens(c)]
    header_coverage = sum(t in page_tokens for t in header_tokens) / max(1, len(header_tokens))
    # Words alone (>= 3 letters) must also be found: reversed or garbled words fail even when numbers match.
    words = [t for t in table_tokens if t.isalpha() and len(t) >= 3]
    word_coverage = sum(t in page_tokens for t in words) / max(1, len(words))
    checks = {"rows_ge_2": n_rows >= 2, "cols_ge_2": max(widths, default=0) >= 2, "rectangular": len(widths) == 1,
              "word_coverage_ok": word_coverage >= MIN_COVERAGE,
              "empty_ratio_ok": empty <= MAX_EMPTY, "token_coverage_ok": coverage >= MIN_COVERAGE,
              "header_tokens_ok": bool(header_tokens) and header_coverage >= MIN_COVERAGE,
              "has_tokens": bool(table_tokens)}
    # Rotated column headers are often read right-to-left: a word that is only on the page when reversed.
    reversed_cells = sorted({(r_i, c_i) for r_i, row in enumerate(rows) for c_i, cell in enumerate(row)
                             for t in tokens(cell) if t.isalpha() and len(t) >= 4
                             and t not in page_tokens and t[::-1] in page_tokens})
    defects = [f"text read reversed (rotated header?) in {len(reversed_cells)} cell(s), rows "
               f"{sorted({r for r, _ in reversed_cells})}"] if reversed_cells else []
    return {"checks": checks, "empty_ratio": round(empty, 3), "token_coverage": round(coverage, 3),
            "header_token_coverage": round(header_coverage, 3), "word_coverage": round(word_coverage, 3),
            "defects": defects, "auto_checks_passed": all(checks.values())}


def main() -> int:
    import pdfplumber

    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    profile = ChunkingProfile.load(PROFILE)
    counter = HFTokenCounter(profile.tokenizer_path, profile.tokenizer_sha256)
    manifest = [json.loads(x) for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]
    summary = {}
    for m in manifest:
        if m["text_fidelity_warning"] or not (m.get("raw_original_path") or "").endswith(".pdf"):
            continue
        sid = m["source_id"]
        document = (ROOT / m["path"]).read_text(encoding="utf-8-sig")
        info = DocumentInfo(sid, sid, m["title"], m["tier"], m["source_type"], "en", m["conversion_gaps"])
        result = chunk_document(document, info, profile, counter)
        flat = [c for c in result.chunks if c.completeness_status.startswith("table_")]
        pages = sorted({p for c in flat if c.page_start for p in range(c.page_start, c.page_end + 1)})
        page_text: dict[int, str] = defaultdict(str)
        for block in result.layout.blocks if result.layout else []:
            if block.page_start:
                page_text[block.page_start] += " " + block.text
        pdf_path = ROOT / m["raw_original_path"]
        out_rows = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_no in pages:
                for t_index, table in enumerate(pdf.pages[page_no - 1].find_tables()):
                    rows = table.extract()
                    verdict = check(rows, page_text[page_no])
                    out_rows.append({
                        "source_id": sid, "page": page_no, "table_index": t_index,
                        "bbox": [round(v, 1) for v in table.bbox], "n_rows": len(rows),
                        "n_cols": max((len(r) for r in rows), default=0), "rows": rows, **verdict,
                        "status": "recovered_pending_human_review" if verdict["auto_checks_passed"]
                        else "candidate_failed_auto_checks",
                        "extractor": f"pdfplumber {pdfplumber.__version__} find_tables(lines strategy)",
                        "original_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                    })
                print(f"{sid} page {page_no}: {sum(r['page'] == page_no for r in out_rows)} table(s)", flush=True)
        out = ROOT / "data" / "extractions" / sid / f"tables.pdfplumber-{pdfplumber.__version__}.v1.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out_rows), encoding="utf-8")
        summary[sid] = {"flattened_chunks": len(flat), "pages_scanned": len(pages), "candidates": len(out_rows),
                        "passed_auto_checks": sum(r["auto_checks_passed"] for r in out_rows),
                        "file": out.relative_to(ROOT).as_posix()}
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
