"""Map the generated catalog/manifest to database rows (pure functions) and load them (one transaction).

Inputs (all produced by scripts/build_corpus.py from data/raw):
  data/raw/source_library/catalog.jsonl   full raw records  -> sources.catalog_payload
  data/catalog/sources.jsonl              tier per source   -> sources.corpus_role
  data/corpus/manifest.jsonl              73 documents      -> documents

Never sets approvals, review decisions or processing permissions: those columns are not even
granted to the ingest role.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg
from psycopg.types.json import Jsonb

from app.config import CORPUS_MANIFEST, RAW_CATALOG, ROOT, SOURCE_CATALOG

# Documents whose converted text has an unresolved fidelity problem: imported, but quarantined.
TEXT_FIDELITY_WARNING = "text_fidelity_needs_conversion_review"
QUALITY_HOLD_WARNING = "catalog_quality_hold"
PDF_PAGE_MARKER = re.compile(r"<!-- SOURCE_PDF_PAGE (\d+) -->")
CC_LICENSE_URL = re.compile(r"creativecommons\.org/licenses/([a-z-]+)/(\d\.\d)", re.I)
DOI_IN_URL = re.compile(r"doi\.org/(10\.\d{4,9}/\S+)", re.I)
YEAR = re.compile(r"^(\d{4})")


class ImportError_(RuntimeError):
    """Input files are inconsistent; nothing was written."""


@dataclass(frozen=True)
class ImportInputs:
    raw: dict[str, dict[str, Any]]
    catalog: dict[str, dict[str, Any]]
    manifest: dict[str, dict[str, Any]]
    fingerprint: str


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8-sig") as f:
        return [json.loads(line) for line in f if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_inputs() -> ImportInputs:
    raw = {r["source_id"]: r for r in _read_jsonl(RAW_CATALOG)}
    catalog = {r["source_id"]: r for r in _read_jsonl(SOURCE_CATALOG)}
    manifest = {r["source_id"]: r for r in _read_jsonl(CORPUS_MANIFEST)}
    if set(raw) != set(catalog):
        raise ImportError_("data/catalog/sources.jsonl is out of sync with the raw catalog; rerun build_corpus.py")
    if not set(manifest) <= set(catalog):
        raise ImportError_("manifest lists sources missing from the catalog")
    fingerprint = hashlib.sha256(
        "".join(sha256_file(p) for p in (RAW_CATALOG, SOURCE_CATALOG, CORPUS_MANIFEST)).encode()
    ).hexdigest()
    return ImportInputs(raw, catalog, manifest, fingerprint)


# ---------------------------------------------------------------- pure mappings


def publication_year(value: str | None) -> int | None:
    match = YEAR.match(value or "")
    return int(match.group(1)) if match else None


def doi_from_url(url: str | None) -> str | None:
    match = DOI_IN_URL.search(url or "")
    return match.group(1).rstrip(".") if match else None


def license_fields(license_value: str | None, license_url: str | None) -> tuple[str | None, str | None]:
    """Return (license_name, license_url). Only CC URLs are named; free text is kept verbatim."""
    if license_value and license_value.lower().startswith("http"):
        match = CC_LICENSE_URL.search(license_value)
        name = f"CC {match.group(1).upper()} {match.group(2)}" if match else None
        return name, license_value
    return license_value, license_url


def content_warning(raw_record: dict[str, Any]) -> str | None:
    gaps = (raw_record.get("conversion") or {}).get("gaps") or []
    if any(g.get("type") == "text_fidelity" for g in gaps):
        return TEXT_FIDELITY_WARNING
    if raw_record.get("quality_hold"):
        return QUALITY_HOLD_WARNING
    return None


def source_row(raw_record: dict[str, Any], catalog_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": raw_record["source_id"],
        "title": raw_record.get("title") or raw_record["source_id"],
        "authors": raw_record.get("authors") or [],
        "publisher": raw_record.get("organization"),
        "publication_year": publication_year(raw_record.get("publication_date")),
        "doi": doi_from_url(raw_record.get("source_url")),
        "source_url": raw_record.get("source_url"),
        "source_type": raw_record.get("source_type"),
        "subject_areas": raw_record.get("topics") or [],
        "corpus_role": catalog_row["tier"],
        "scope_status": raw_record["status"],
        "content_warning": content_warning(raw_record),
        "catalog_payload": Jsonb(raw_record),
    }


def rights_row(raw_record: dict[str, Any], catalog_row: dict[str, Any] | None = None) -> dict[str, Any]:
    """Descriptive rights facts. The status and licence facts come from the generated catalog, which
    already applies curated corrections; permissions (*_allowed) are never part of this row."""
    rights = raw_record.get("rights") or {}
    catalog_row = catalog_row or {}
    name, url = license_fields(rights.get("license"), rights.get("license_url"))
    notes = [
        f"Catalog rights review ({raw_record.get('checked_at') or 'date unknown'}): status={rights.get('status')}.",
        *(f"{label}: {rights[key]}" for key, label in (
            ("conditions", "Conditions"), ("attribution", "Attribution"),
            ("third_party_exceptions", "Third-party exceptions"),
        ) if rights.get(key)),
    ]
    if correction := catalog_row.get("license_correction_id"):
        notes.append(f"Classification corrected by {correction}: {catalog_row['rights_status_original']} -> "
                     f"{catalog_row['rights_status']} (licence read from the original document).")
    notes.append("Text mining / embedding / Cohere / external LLM processing: not verified.")
    return {
        "source_id": raw_record["source_id"],
        "rights_status": catalog_row.get("rights_status") or rights.get("status") or "unknown",
        "license_name": name,
        "license_url": url,
        "license_type": catalog_row.get("license_type"),
        "license_version": catalog_row.get("license_version"),
        "rights_holder": catalog_row.get("rights_holder"),
        "permitted_use_notes": " ".join(notes),
        "evidence_url": rights.get("evidence_url"),
    }


def page_count(text: str) -> int | None:
    pages = [int(p) for p in PDF_PAGE_MARKER.findall(text)]
    return max(pages) if pages else None


def document_row(manifest_row: dict[str, Any], raw_record: dict[str, Any], text: str) -> dict[str, Any]:
    conversion = raw_record.get("conversion") or {}
    warning = content_warning(raw_record)
    original = manifest_row.get("raw_original_path")
    return {
        "document_id": f"{manifest_row['source_id']}@{manifest_row['version']}",
        "source_id": manifest_row["source_id"],
        "document_version": manifest_row["version"],
        "raw_relative_path": manifest_row["raw_document_path"],
        "corpus_relative_path": manifest_row["path"],
        "original_file_name": Path(original).name if original else None,
        "file_format": raw_record.get("original_format"),
        "file_sha256": manifest_row["sha256"],
        "original_sha256": raw_record.get("original_sha256"),
        "character_count": manifest_row["characters"],
        "page_count": page_count(text),
        "text_completeness": "complete" if manifest_row["tier"] == "core" else "partial",
        "missing_components": Jsonb(manifest_row.get("conversion_gaps") or {}),
        "extraction_status": conversion.get("status") or "unknown",
        "content_review_status": "quarantined" if warning else "pending",
        "content_warning": warning,
        "extraction_tool": conversion.get("method"),
        "extraction_version": conversion.get("conversion_revision"),
        "is_current": True,
    }


# ---------------------------------------------------------------- database load


def _upsert(conn: psycopg.Connection, table: str, row: dict[str, Any], key: str, update: list[str]) -> None:
    cols = list(row)
    assignments = ", ".join(f"{c} = EXCLUDED.{c}" for c in update)
    if "updated_at" not in update and table in {"sources", "source_rights", "documents"}:
        assignments += ", updated_at = now()"
    conn.execute(
        f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('%(' + c + ')s' for c in cols)}) "
        f"ON CONFLICT ({key}) DO UPDATE SET {assignments}",
        row,
    )


DOCUMENT_REFRESHABLE = [
    "raw_relative_path", "corpus_relative_path", "original_file_name", "file_format", "file_sha256",
    "original_sha256", "character_count", "page_count", "text_completeness", "missing_components",
    "extraction_status", "extraction_tool", "extraction_version", "is_current",
]


def import_all(conn: psycopg.Connection, inputs: ImportInputs, code_version: str) -> dict[str, Any]:
    """Load sources, rights and documents in the caller's transaction. Returns run stats."""
    run_id = conn.execute(
        "INSERT INTO ingestion_runs (run_type, code_version, input_fingerprint, configuration) "
        "VALUES ('catalog_import', %s, %s, %s) RETURNING run_id",
        (code_version, inputs.fingerprint, Jsonb({"inputs": ["raw catalog", "sources.jsonl", "manifest.jsonl"]})),
    ).fetchone()[0]

    for source_id in sorted(inputs.raw):
        raw_record = inputs.raw[source_id]
        src = source_row(raw_record, inputs.catalog[source_id])
        _upsert(conn, "sources", src, "source_id", [c for c in src if c != "source_id"])
        rights = rights_row(raw_record, inputs.catalog[source_id])
        _upsert(conn, "source_rights", rights, "source_id", [c for c in rights if c != "source_id"])

    for source_id in sorted(inputs.manifest):
        m = inputs.manifest[source_id]
        corpus_file = ROOT / m["path"]
        if sha256_file(corpus_file) != m["sha256"]:
            raise ImportError_(f"{source_id}: corpus file hash differs from manifest")
        doc = document_row(m, inputs.raw[source_id], corpus_file.read_text(encoding="utf-8-sig"))
        conn.execute("UPDATE documents SET is_current = false, updated_at = now() "
                     "WHERE source_id = %s AND document_id <> %s AND is_current",
                     (source_id, doc["document_id"]))
        _upsert(conn, "documents", doc, "document_id", DOCUMENT_REFRESHABLE)
        conn.execute("INSERT INTO ingestion_run_documents (run_id, document_id, status) VALUES (%s, %s, 'succeeded')",
                     (run_id, doc["document_id"]))

    stats = {"sources": len(inputs.raw), "documents": len(inputs.manifest)}
    conn.execute("UPDATE ingestion_runs SET status = 'succeeded', finished_at = now(), stats = %s WHERE run_id = %s",
                 (Jsonb(stats), run_id))
    return {"run_id": str(run_id), **stats}
