"""Versioned SQL migrations (migrations/NNN_name.sql) recorded with their SHA-256.

An applied file that later changes on disk is a hard error: history is append-only, so a fix
goes into a new migration instead of an edit.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import psycopg

from app.config import DB_SCHEMA, MIGRATIONS

FILE_PATTERN = re.compile(r"^(\d{3})_[a-z0-9_]+\.sql$")


@dataclass(frozen=True)
class Migration:
    version: str
    path: Path
    sha256: str


class MigrationError(RuntimeError):
    pass


def discover(directory: Path = MIGRATIONS) -> list[Migration]:
    found = []
    for path in sorted(directory.glob("*.sql")):
        match = FILE_PATTERN.match(path.name)
        if not match:
            raise MigrationError(f"Unexpected file name in migrations/: {path.name}")
        found.append(Migration(match.group(1), path, hashlib.sha256(path.read_bytes()).hexdigest()))
    versions = [m.version for m in found]
    if len(versions) != len(set(versions)):
        raise MigrationError(f"Duplicate migration version in {versions}")
    return found


def plan(found: list[Migration], applied: dict[str, tuple[str, str]]) -> list[Migration]:
    """Return pending migrations; refuse if history was rewritten or would apply out of order."""
    for m in found:
        if m.version in applied and applied[m.version] != (m.path.name, m.sha256):
            raise MigrationError(f"Applied migration {m.version} changed on disk ({m.path.name}); "
                                 "add a new migration instead of editing it")
    unknown = set(applied) - {m.version for m in found}
    if unknown:
        raise MigrationError(f"Database has migrations not present on disk: {sorted(unknown)}")
    pending = [m for m in found if m.version not in applied]
    if pending and applied and pending[0].version < max(applied):
        raise MigrationError(f"Pending migration {pending[0].version} is older than applied {max(applied)}")
    return pending


def applied_migrations(conn: psycopg.Connection) -> dict[str, tuple[str, str]]:
    conn.execute(f"""CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.schema_migrations (
                        version text PRIMARY KEY, file_name text NOT NULL,
                        sha256 text NOT NULL, applied_at timestamptz NOT NULL DEFAULT now())""")
    rows = conn.execute(f"SELECT version, file_name, sha256 FROM {DB_SCHEMA}.schema_migrations").fetchall()
    return {v: (n, s) for v, n, s in rows}


def apply(conn: psycopg.Connection, migration: Migration) -> None:
    """Run one file and record it, in one transaction. `conn` must be in autocommit mode."""
    with conn.transaction():
        conn.execute(migration.path.read_text(encoding="utf-8"))
        conn.execute(f"INSERT INTO {DB_SCHEMA}.schema_migrations (version, file_name, sha256) VALUES (%s, %s, %s)",
                     (migration.version, migration.path.name, migration.sha256))
