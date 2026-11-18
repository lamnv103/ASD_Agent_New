"""Import 174 sources, their rights records and the 73 corpus documents into asd_rag_v2.

Idempotent: rerunning with unchanged inputs updates rows in place and adds one audit run.
Runs as the ingest role, which cannot set approvals or processing permissions.

Usage:
  python -B scripts/import_sources.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import connect
from app.ingest import catalog_import


def main() -> int:
    inputs = catalog_import.load_inputs()
    module_file = Path(catalog_import.__file__)
    code_version = f"catalog_import@{hashlib.sha256(module_file.read_bytes()).hexdigest()[:12]}"
    with connect("ingest", "import_sources") as conn:  # commits on success, rolls back on error
        result = catalog_import.import_all(conn, inputs, code_version)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except catalog_import.ImportError_ as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
