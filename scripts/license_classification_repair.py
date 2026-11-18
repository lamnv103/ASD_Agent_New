"""Write the curated licence-classification corrections (data/curation/license_corrections.jsonl).

A correction is written ONLY when the licence statement read from the ORIGINAL file is CC BY, the
evidence sits in the document itself (not an agency-wide policy), there is no conflict with the
catalog, and the catalog label is the stricter `verified_noncommercial_research`. Each row carries
the original file's SHA-256, so build_corpus.py can refuse a correction whose evidence changed.

What is corrected: the classification label and licence facts (type, version, URL, holder).
What is NOT touched: any permission (`*_allowed`), project usage policy, quarantine, approvals.
data/raw is never modified. Rollback = delete the curation file and rebuild.

Usage:
  python -B scripts/license_classification_repair.py            # write the curation file
  python -B scripts/license_classification_repair.py --dry-run  # print what would be written
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import CORPUS_MANIFEST, RAW_CATALOG, ROOT
from app.rights.license_audit import collect

CURATION = ROOT / "data" / "curation" / "license_corrections.jsonl"
FROM_STATUS = "verified_noncommercial_research"
TO_STATUS = "verified_cc_by"
AUTHORIZATION = "Project owner instruction: MASTER PROMPT Phase 5, Task A (2026-11-14) — correct CC BY classification"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    raw = {json.loads(x)["source_id"]: json.loads(x)
           for x in RAW_CATALOG.read_text(encoding="utf-8-sig").splitlines() if x.strip()}
    manifest = [json.loads(x) for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows, skipped = [], Counter()
    for m in sorted(manifest, key=lambda r: r["source_id"]):
        record = raw[m["source_id"]]
        if (record.get("rights") or {}).get("status") != FROM_STATUS:
            continue
        ev = collect(record, m, ROOT)
        if ev.license_name != "CC BY":
            skipped[f"licence is {ev.license_name}"] += 1
            continue
        if ev.verification_status != "evidence_in_original_document":
            skipped[f"evidence {ev.verification_status}"] += 1
            continue
        original = ROOT / m["raw_original_path"]
        rows.append({
            "correction_id": f"LC-2026-11-14-{m['source_id']}",
            "source_id": m["source_id"],
            "rights_status_from": FROM_STATUS,
            "rights_status_to": TO_STATUS,
            "license_type": "CC BY",
            "license_version": ev.license_version,
            "license_url": ev.license_url,
            "rights_holder": ev.rights_holder or None,
            "evidence_file": m["raw_original_path"],
            "evidence_file_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "evidence_location": ev.evidence_location,
            "evidence_excerpt": ev.statement[:300],
            "caveats": "; ".join(ev.notes) or None,
            "permissions_changed": False,
            "project_usage_policy": None,
            "authorized_by": AUTHORIZATION,
            "prepared_by": "scripts/license_classification_repair.py",
            "prepared_at": date.today().isoformat(),
        })
    summary = {"corrections": len(rows), "skipped": dict(skipped),
               "by_version": dict(Counter(r["license_version"] for r in rows)),
               "file": CURATION.relative_to(ROOT).as_posix(), "dry_run": args.dry_run}
    if not args.dry_run:
        CURATION.parent.mkdir(parents=True, exist_ok=True)
        with open(CURATION, "w", encoding="utf-8", newline="\n") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        summary["sha256"] = hashlib.sha256(CURATION.read_bytes()).hexdigest()
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
