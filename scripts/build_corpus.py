"""Build the expert-QA corpus and the source catalog from data/raw/source_library.

Outputs (fully regenerated on every run; never edit them by hand):
  data/corpus/core/<source_id>.md    33 accepted complete-text documents
  data/corpus/gaps/<source_id>.md    40 full-text documents with conversion gaps
  data/corpus/manifest.jsonl         one row per corpus document (73)
  data/catalog/sources.jsonl         one row per source (174), for the info-lookup branch

Usage:
  python -B scripts/build_corpus.py          # build
  python -B scripts/build_corpus.py --check  # verify outputs against raw hashes, no writes
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "source_library"
CORPUS = ROOT / "data" / "corpus"
CATALOG = ROOT / "data" / "catalog"
RAW_PREFIX = "knowledge/rag/source_library/"  # catalog paths are relative to the old project root
# Curated, versioned corrections layered over the immutable raw catalog (see
# scripts/license_classification_repair.py). Optional: without it the build reproduces the raw labels.
CURATION = ROOT / "data" / "curation" / "license_corrections.jsonl"
CORRECTED_FIELDS = ("license_type", "license_version", "rights_holder", "rights_status_original",
                    "license_correction_id")

TIER_BY_STATUS = {
    "accepted_complete_text": "core",
    "full_text_with_conversion_gaps": "gaps",
    "outside_scope": "excluded",
    "excluded_quality_and_uncleared_rights": "excluded",
}
CORPUS_TIERS = ("core", "gaps")


def tier_of(status: str) -> str:
    return TIER_BY_STATUS.get(status, "metadata_only")


def raw_path(catalog_path: str | None) -> Path | None:
    if not catalog_path or not catalog_path.startswith(RAW_PREFIX):
        return None
    return RAW / catalog_path[len(RAW_PREFIX):]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_catalog() -> list[dict]:
    with open(RAW / "catalog.jsonl", encoding="utf-8-sig") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    ids = [r["source_id"] for r in rows]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dupes:
        sys.exit(f"duplicate source_id in catalog: {dupes}")
    return rows


def load_corrections(catalog: list[dict]) -> dict[str, dict]:
    """Validated licence-classification corrections keyed by source_id ({} when the file is absent)."""
    if not CURATION.exists():
        return {}
    by_id = {r["source_id"]: r for r in catalog}
    corrections: dict[str, dict] = {}
    for line in CURATION.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        sid = c["source_id"]
        if sid not in by_id:
            sys.exit(f"correction for unknown source {sid}")
        if sid in corrections:
            sys.exit(f"duplicate correction for {sid}")
        if any(k.endswith("_allowed") for k in c) or c.get("permissions_changed") is not False:
            sys.exit(f"{sid}: a classification correction may not carry permissions")
        raw_status = (by_id[sid].get("rights") or {}).get("status")
        if raw_status != c["rights_status_from"]:
            sys.exit(f"{sid}: raw status {raw_status!r} != correction's from-status {c['rights_status_from']!r}")
        evidence = ROOT / c["evidence_file"]
        if not evidence.is_file() or sha256(evidence) != c["evidence_file_sha256"]:
            sys.exit(f"{sid}: evidence file missing or changed since the correction was prepared")
        corrections[sid] = c
    return corrections


def rights_fields(r: dict, correction: dict | None) -> dict:
    rights = r.get("rights") or {}
    fields = {
        "rights_status": rights.get("status"),
        "license": rights.get("license"),
        "rights_conditions": rights.get("conditions") or rights.get("attribution"),
        **dict.fromkeys(CORRECTED_FIELDS),
    }
    if correction:
        fields |= {
            "rights_status": correction["rights_status_to"],
            "license_type": correction["license_type"],
            "license_version": correction["license_version"],
            "rights_holder": correction["rights_holder"],
            "rights_status_original": correction["rights_status_from"],
            "license_correction_id": correction["correction_id"],
        }
    return fields


def common_fields(r: dict, corrections: dict[str, dict]) -> dict:
    return {
        "source_id": r["source_id"],
        "tier": tier_of(r["status"]),
        "status": r["status"],
        "title": r.get("title"),
        "authors": r.get("authors") or [],
        "organization": r.get("organization"),
        "publication_date": r.get("publication_date"),
        "source_type": r.get("source_type"),
        "language": r.get("language"),
        "topics": r.get("topics") or [],
        "source_url": r.get("source_url"),
        "full_text_url": r.get("full_text_url"),
        **rights_fields(r, corrections.get(r["source_id"])),
        "applicability_0_18_years": r.get("applicability_0_18_years"),
        "original_age_scope": r.get("original_age_scope"),
    }


def manifest_row(r: dict, out: Path, corrections: dict[str, dict]) -> dict:
    gaps = (r.get("conversion") or {}).get("gaps") or []
    gap_types = collections.Counter(g.get("type") or "unspecified" for g in gaps)
    return {
        **common_fields(r, corrections),
        "path": out.relative_to(ROOT).as_posix(),
        "sha256": r["document_sha256"],
        "characters": len(out.read_text(encoding="utf-8-sig")),
        "version": r.get("version"),
        "limits": r.get("limits") or [],
        "conversion_gaps": dict(sorted(gap_types.items())),
        "text_fidelity_warning": "text_fidelity" in gap_types,
        "raw_document_path": raw_path(r["document_path"]).relative_to(ROOT).as_posix(),
        "raw_original_path": (p.relative_to(ROOT).as_posix() if (p := raw_path(r.get("original_path"))) else None),
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")


def build() -> None:
    catalog = load_catalog()
    corrections = load_corrections(catalog)  # validated before anything is deleted
    for d in (CORPUS, CATALOG):
        if d.exists():
            shutil.rmtree(d)

    manifest = []
    for r in sorted(catalog, key=lambda r: r["source_id"]):
        tier = tier_of(r["status"])
        if tier not in CORPUS_TIERS:
            continue
        src = raw_path(r.get("document_path"))
        if src is None or not src.is_file():
            sys.exit(f"{r['source_id']}: document missing in raw library ({r.get('document_path')})")
        if sha256(src) != r["document_sha256"]:
            sys.exit(f"{r['source_id']}: raw document hash does not match catalog")
        out = CORPUS / tier / f"{r['source_id']}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        manifest.append(manifest_row(r, out, corrections))

    sources = []
    for r in sorted(catalog, key=lambda r: r["source_id"]):
        row = common_fields(r, corrections)
        row["in_corpus"] = row["tier"] in CORPUS_TIERS
        row["corpus_path"] = f"data/corpus/{row['tier']}/{r['source_id']}.md" if row["in_corpus"] else None
        row["audit_conclusion"] = r.get("audit_conclusion")
        sources.append(row)

    write_jsonl(CORPUS / "manifest.jsonl", manifest)
    write_jsonl(CATALOG / "sources.jsonl", sources)
    report(manifest, sources)


def check() -> None:
    with open(CORPUS / "manifest.jsonl", encoding="utf-8") as f:
        manifest = [json.loads(line) for line in f if line.strip()]
    with open(CATALOG / "sources.jsonl", encoding="utf-8") as f:
        sources = [json.loads(line) for line in f if line.strip()]
    errors = []
    for m in manifest:
        for key in ("path", "raw_document_path"):
            p = ROOT / m[key]
            if not p.is_file():
                errors.append(f"{m['source_id']}: missing {m[key]}")
            elif sha256(p) != m["sha256"]:
                errors.append(f"{m['source_id']}: hash mismatch {m[key]}")
    on_disk = {p.relative_to(ROOT).as_posix() for t in CORPUS_TIERS for p in (CORPUS / t).glob("*.md")}
    extra = on_disk - {m["path"] for m in manifest}
    errors += [f"unlisted corpus file: {p}" for p in sorted(extra)]
    # Generated rights fields must equal raw catalog + current curation (catches a stale build).
    catalog = load_catalog()
    corrections = load_corrections(catalog)
    expected = {r["source_id"]: rights_fields(r, corrections.get(r["source_id"])) for r in catalog}
    for row in [*manifest, *sources]:
        want = expected[row["source_id"]]
        if any(row.get(k) != v for k, v in want.items()):
            errors.append(f"{row['source_id']}: rights fields differ from raw catalog + curation (rebuild needed)")
    if corrections:
        print(f"curation: {len(corrections)} licence corrections applied ({CURATION.relative_to(ROOT).as_posix()})")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    report(manifest, sources)
    print("check: OK")


def report(manifest: list[dict], sources: list[dict]) -> None:
    by_tier = collections.Counter(m["tier"] for m in manifest)
    chars = collections.Counter()
    for m in manifest:
        chars[m["tier"]] += m["characters"]
    print(f"corpus: {len(manifest)} documents {dict(by_tier)}, characters {dict(chars)}")
    print(f"catalog: {len(sources)} sources {dict(collections.Counter(s['tier'] for s in sources))}")
    flagged = [m["source_id"] for m in manifest if m["text_fidelity_warning"]]
    if flagged:
        print(f"text_fidelity warnings: {flagged}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verify existing outputs without writing")
    check() if parser.parse_args().check else build()
