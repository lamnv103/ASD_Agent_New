"""PostgreSQL connections, one login role per responsibility (owner / ingest / app)."""

from __future__ import annotations

import psycopg

from app.config import Role, db_settings


def connect(role: Role, application_name: str) -> psycopg.Connection:
    """Open a connection as the given role. Autocommit is off: callers own the transaction."""
    return psycopg.connect(**db_settings(role).conninfo(application_name))
