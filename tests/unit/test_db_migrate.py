from pathlib import Path

import pytest

from app.migrations import Migration, MigrationError, discover, plan


def m(version: str, sha: str = "x") -> Migration:
    return Migration(version, Path(f"{version}_step.sql"), sha)


def test_pending_are_returned_in_order():
    assert [p.version for p in plan([m("001"), m("002"), m("003")], {"001": ("001_step.sql", "x")})] == ["002", "003"]


def test_edited_applied_migration_is_rejected():
    with pytest.raises(MigrationError, match="changed on disk"):
        plan([m("001", "new")], {"001": ("001_step.sql", "old")})


def test_unknown_applied_migration_is_rejected():
    with pytest.raises(MigrationError, match="not present on disk"):
        plan([m("001")], {"001": ("001_step.sql", "x"), "002": ("002_step.sql", "y")})


def test_out_of_order_pending_is_rejected():
    with pytest.raises(MigrationError, match="older than applied"):
        plan([m("001"), m("002")], {"002": ("002_step.sql", "x")})


def test_repository_migrations_are_well_formed():
    versions = [x.version for x in discover()]
    assert versions == sorted(versions) and versions[:3] == ["001", "002", "003"]
