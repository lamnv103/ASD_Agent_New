"""Structured retrieval log (JSONL, local research environment).

Interim by design: the research reader role may not write `retrieval_logs` (only the app role can), and
read-only access is not widened for logging. One JSON object per line; the query text is never written
(only its SHA-256), nor any secret. Records are append-only on local disk (logs/ is git-ignored); they are
neither centralised nor tamper-evident — see the T2.3.1 report for the proposed database logging path.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

FORBIDDEN_KEYS = {"query", "query_text", "question", "question_vi", "password", "api_key", "content"}


class JsonlRetrievalLog:
    def __init__(self, log_dir: Path, name: str | None = None) -> None:
        log_dir.mkdir(parents=True, exist_ok=True)
        self.path = log_dir / (name or f"dense_{datetime.now(UTC):%Y%m%d}.jsonl")

    def write(self, record: dict) -> None:
        leaked = FORBIDDEN_KEYS & set(record)
        if leaked:
            raise ValueError(f"refusing to log fields {sorted(leaked)}")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
