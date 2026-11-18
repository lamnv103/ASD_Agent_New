"""Apply versioned SQL migrations (migrations/NNN_name.sql) as the owner role.

Each file runs in its own transaction and is recorded in asd_rag.schema_migrations with its
SHA-256. A file that was already applied and has since changed is a hard error: write a new
migration instead of editing an old one.

Usage:
  python -B scripts/db_migrate.py            # apply pending migrations
  python -B scripts/db_migrate.py --status   # show applied / pending, change nothing
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import migrations
from app.db import connect


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    found = migrations.discover()
    with connect("owner", "db_migrate") as conn:
        conn.autocommit = True  # each migrations.apply() is then a real, separate transaction
        applied = migrations.applied_migrations(conn)
        pending = migrations.plan(found, applied)
        for m in found:
            print(f"{m.version}  {'applied' if m.version in applied else 'pending':8} {m.path.name}")
        if args.status or not pending:
            print("nothing to apply" if not pending else f"{len(pending)} pending")
            return 0
        for m in pending:
            migrations.apply(conn, m)
            print(f"applied {m.path.name}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except migrations.MigrationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
