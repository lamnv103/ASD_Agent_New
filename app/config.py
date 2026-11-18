"""Project paths and environment-backed settings. Secrets are read from .env, never logged."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_LIBRARY = DATA / "raw" / "source_library"
RAW_CATALOG = RAW_LIBRARY / "catalog.jsonl"
CORPUS_MANIFEST = DATA / "corpus" / "manifest.jsonl"
SOURCE_CATALOG = DATA / "catalog" / "sources.jsonl"
MIGRATIONS = ROOT / "migrations"
REPORTS = ROOT / "eval" / "reports"

DB_SCHEMA = "asd_rag"
Role = Literal["owner", "ingest", "app", "research_reader"]
_ROLE_USERS: dict[str, tuple[str, str]] = {
    "owner": ("asd_rag_v2_owner", "ASD_RAG_OWNER_PASSWORD"),
    "ingest": ("asd_rag_v2_ingest", "ASD_RAG_INGEST_PASSWORD"),
    "app": ("asd_rag_v2_app", "ASD_RAG_APP_PASSWORD"),
    # read-only research retrieval role (migration 007): SELECT on v_research_retrieval_chunks only
    "research_reader": ("asd_rag_v2_research_reader", "ASD_RAG_RESEARCH_READER_PASSWORD"),
}

load_dotenv(ROOT / ".env", override=False)


class ConfigError(RuntimeError):
    """A required setting is missing. The message names the variable, never its value."""


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ConfigError(f"Missing environment variable {name} (set it in .env)")
    return value


def _flag(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# ---------------------------------------------------------------------------------- demo authorization gates
# T2.6 concluded APPROVAL_REQUIRED: no scenario authorizing live Cohere query embedding, live reranking, or
# any external LLM processing has been approved by the project owner. These flags default to disabled and
# stay disabled; setting one to true does not enable anything (no live adapter is wired to them) and instead
# fails loudly at startup, so a misconfigured environment can never silently send a live provider request.
DEMO_MODE = _flag("ASD_DEMO_MODE", True)
ENABLE_LIVE_QUERY_EMBEDDING = _flag("ASD_ENABLE_LIVE_QUERY_EMBEDDING", False)
ENABLE_LIVE_RERANKING = _flag("ASD_ENABLE_LIVE_RERANKING", False)
ENABLE_LIVE_LLM = _flag("ASD_ENABLE_LIVE_LLM", False)

if ENABLE_LIVE_QUERY_EMBEDDING or ENABLE_LIVE_RERANKING or ENABLE_LIVE_LLM:
    raise ConfigError(
        "ASD_ENABLE_LIVE_QUERY_EMBEDDING / ASD_ENABLE_LIVE_RERANKING / ASD_ENABLE_LIVE_LLM were set to true, "
        "but no scenario authorizing live Cohere/LLM processing has been approved (see "
        "reports/demo_mvp/t2_6_authorization_decision_matrix.md: APPROVAL_REQUIRED). Leave these unset or "
        "false until the project owner approves Scenario B and the code implementing it is added.")


@dataclass(frozen=True)
class DbSettings:
    host: str
    port: int
    name: str
    user: str
    password: str

    def conninfo(self, application_name: str) -> dict[str, str | int]:
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.name,
            "user": self.user,
            "password": self.password,
            "application_name": application_name,
            "connect_timeout": 10,
        }


def db_settings(role: Role) -> DbSettings:
    user, password_var = _ROLE_USERS[role]
    return DbSettings(
        host=_require("ASD_RAG_DB_HOST"),
        port=int(_require("ASD_RAG_DB_PORT")),
        name=_require("ASD_RAG_DB_NAME"),
        user=user,
        password=_require(password_var),
    )
