"""Write verified page maps for PDF-derived documents without page markers (no network, no DB).

Output (versioned, never overwritten silently):
  data/extractions/<source_id>/page_map.pypdf-6.11.0.v1.json

Usage:
  python -B scripts/pdf_page_map.py WHO-CST-INTRO-2022 WHO-CST-PARTICIPANTS-2022 WHO-ECD-GUIDELINE-2020
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import CORPUS_MANIFEST, ROOT
from app.ingest.pdf_page_map import EXTRACTOR, EXTRACTOR_VERSION, MAP_VERSION, build_page_map

OUT_DIR = ROOT / "data" / "extractions"


def map_path(source_id: str) -> Path:
    return OUT_DIR / source_id / f"page_map.{EXTRACTOR}-{EXTRACTOR_VERSION}.{MAP_VERSION}.json"


def main() -> int:
    manifest = {(m := json.loads(x))["source_id"]: m for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines()
                if x.strip()}
    results = []
    for sid in sys.argv[1:]:
        m = manifest[sid]
        pm = build_page_map(sid, ROOT / m["raw_original_path"], ROOT / m["path"])
        out = map_path(sid)
        if out.exists():
            existing = json.loads(out.read_text(encoding="utf-8"))
            if existing["corpus_sha256"] != pm.corpus_sha256 or existing["original_sha256"] != pm.original_sha256:
                raise SystemExit(f"{out} exists for different inputs; bump MAP_VERSION instead of overwriting")
        if pm.verified:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(pm.to_json(), ensure_ascii=False, indent=1), encoding="utf-8")
        results.append({"source_id": sid, "verified": pm.verified, "pages": len(pm.pages),
                        "empty_pages": sum(not p.chars for p in pm.pages),
                        "labels": [p.label for p in pm.pages[:6]], "failures": pm.failures[:3],
                        "file": out.relative_to(ROOT).as_posix() if pm.verified else None})
    print(json.dumps(results, ensure_ascii=False, indent=1))
    return 0 if all(r["verified"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
