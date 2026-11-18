"""Write the CSV evidence for the 2026-11-14 follow-up (read-only: DB reads and existing report JSON).

  eval/reports/pdf_extraction_diff.csv    every section_v2_1 chunk of the 4 PDFs that is not plain retrievable
                                          text (flattened/unrecoverable tables, recovered-pending-review, glyph
                                          encoding), with pages, reason and the extraction sidecar consulted
  eval/reports/section_v2_regression.csv  per document: chunks / eligible chunks for v1, v2, v2_1

Usage:
  python -B scripts/acceptance_artifacts.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect

PDF_SOURCES = ["NIHR-SENITA-2022", "WHO-CST-INTRO-2022", "WHO-CST-PARTICIPANTS-2022", "WHO-ECD-GUIDELINE-2020"]
REASONS = {
    "table_structure_unrecoverable": "flattened PDF table; no candidate passed automated structure checks",
    "table_recovered_pending_review": "structured candidate in tables sidecar passed checks; awaiting human review",
    "text_encoding_lost": "glyph ids (/gidNNNNN) instead of characters; pdfium re-extraction proposal in sidecar",
    "page_provenance_incomplete": "no verified page map",
}


def latest(pattern: str) -> Path:
    files = sorted(REPORTS.glob(pattern))
    if not files:
        raise SystemExit(f"missing {pattern}; run scripts/chunking_regression.py first")
    return files[-1]


def main() -> int:
    with connect("ingest", "acceptance_artifacts") as conn:
        rows = conn.execute("""SELECT source_id, document_id, chunk_id, chunk_index, page_start, page_end,
                                      section_type, completeness_status, retrieval_eligible, token_count
                               FROM v_chunk_provenance
                               WHERE chunking_profile = 'section_v2_1' AND source_id = ANY(%s)
                                 AND completeness_status = ANY(%s)
                               ORDER BY source_id, chunk_index""", (PDF_SOURCES, list(REASONS))).fetchall()
    sidecars = {sid: [p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "data" / "extractions" / sid).glob("*"))]
                for sid in PDF_SOURCES}
    diff = REPORTS / "pdf_extraction_diff.csv"
    with open(diff, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "document_id", "chunk_id", "chunk_index", "page_start", "page_end", "section_type",
                    "status_v2_1", "retrieval_eligible", "tokens", "reason", "extraction_sidecars"])
        for r in rows:
            w.writerow([*r, REASONS[r[7]], " | ".join(sidecars[r[0]])])

    v1v21 = json.loads(latest("*_chunking_regression_section_v1_vs_section_v2_1.json").read_text(encoding="utf-8"))
    v2v21 = json.loads(latest("*_chunking_regression_section_v2_vs_section_v2_1.json").read_text(encoding="utf-8"))
    reg = REPORTS / "section_v2_regression.csv"
    with open(reg, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "pdf_layout", "v1_chunks", "v1_eligible", "v2_chunks", "v2_eligible",
                    "v2_1_chunks", "v2_1_eligible"])
        for sid, a in sorted(v1v21["per_document"].items()):
            b = v2v21["per_document"][sid]
            w.writerow([sid, sid in v1v21["layout_documents"], a["base_chunks"], a["base_eligible"], b["base_chunks"],
                        b["base_eligible"], a["cand_chunks"], a["cand_eligible"]])
    print(json.dumps({"pdf_extraction_diff_rows": len(rows), "regression_rows": len(v1v21["per_document"]),
                      "files": [diff.relative_to(ROOT).as_posix(), reg.relative_to(ROOT).as_posix()]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
