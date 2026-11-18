"""Draft embedding candidate matrix — every row is NOT_APPROVED (read-only: DB reads, no network).

One row per source (174): technical readiness (current document, quarantine, chunks of the embedding
profile's chunking profile, unverified structure, provenance) next to what still blocks it (rights
decisions, provider terms, expert review). It is a worksheet for the owner, not an allowlist.

Usage:
  python -B scripts/embedding_candidates.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect
from app.retrieval.embeddings import EmbeddingProfile

PROFILE = "cohere_embed_v4_1536_v1"
RIGHT_FLAGS = ("archive_allowed", "text_mining_allowed", "chunking_allowed", "embedding_allowed",
               "cohere_processing_allowed", "external_llm_processing_allowed")
FIELDS = ["source_id", "title", "corpus_role", "license_type", "license_version", "rights_status",
          "category", "content_review_status", "quarantined", "chunks", "eligible_chunks", "eligible_tokens",
          "unverified_chunks", "page_provenance", "technically_eligible", "rights_blockers", "cohere_assessment",
          "external_llm_assessment", "expert_review_required", "approval_status", "notes"]

QUERY = """
SELECT s.source_id, s.title, s.corpus_role, r.license_type, r.license_version, r.rights_status,
       d.document_id, d.content_review_status, d.file_format,
       count(c.chunk_id) AS chunks,
       count(c.chunk_id) FILTER (WHERE c.retrieval_eligible) AS eligible_chunks,
       coalesce(sum(c.token_count) FILTER (WHERE c.retrieval_eligible), 0) AS eligible_tokens,
       count(c.chunk_id) FILTER (WHERE c.completeness_status IN ('table_structure_unrecoverable',
           'table_recovered_pending_review', 'text_encoding_lost', 'page_provenance_incomplete')) AS unverified,
       count(c.chunk_id) FILTER (WHERE c.page_start IS NULL) AS no_page,
       r.archive_allowed, r.text_mining_allowed, r.chunking_allowed, r.embedding_allowed,
       r.cohere_processing_allowed, r.external_llm_processing_allowed
FROM sources s
JOIN source_rights r ON r.source_id = s.source_id
LEFT JOIN documents d ON d.source_id = s.source_id AND d.is_current
LEFT JOIN chunks c ON c.document_id = d.document_id AND c.chunking_profile = %(chunking)s
GROUP BY s.source_id, s.title, s.corpus_role, r.license_type, r.license_version, r.rights_status, d.document_id,
         d.content_review_status, d.file_format, r.archive_allowed, r.text_mining_allowed, r.chunking_allowed,
         r.embedding_allowed, r.cohere_processing_allowed, r.external_llm_processing_allowed
ORDER BY s.source_id
"""


def main() -> int:
    profile = EmbeddingProfile.load(PROFILE)
    with open(REPORTS / "license_review_matrix.csv", encoding="utf-8-sig") as f:
        audit = {r["source_id"]: r for r in csv.DictReader(f)}
    with connect("ingest", "embedding_candidates") as conn:
        cur = conn.execute(QUERY, {"chunking": profile.chunking_profile})
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r, strict=True)) for r in cur.fetchall()]

    out = []
    for r in rows:
        sid, has_doc = r["source_id"], r["document_id"] is not None
        quarantined = r["content_review_status"] == "quarantined"
        if not has_doc:
            category = "metadata_retrieval_only" if r["corpus_role"] == "metadata_only" else "excluded_from_answers"
        elif quarantined:
            category = "quarantined"
        else:
            category = "full_text"
        pdf = (r["file_format"] or "") == "pdf"
        provenance = ("n/a" if not has_doc or quarantined else
                      ("pdf_pages_complete" if r["no_page"] == 0 else "pdf_pages_incomplete") if pdf
                      else "char_offsets (source has no pages)")
        technically = (category == "full_text" and r["eligible_chunks"] > 0
                       and provenance in ("pdf_pages_complete", "char_offsets (source has no pages)"))
        blockers = [f"{k}=NULL" if r[k] is None else f"{k}={r[k]}" for k in RIGHT_FLAGS if r[k] is not True]
        a = audit.get(sid, {})
        notes = []
        if r["unverified"]:
            notes.append(f"{r['unverified']} chunk(s) with unverified table/encoding structure excluded")
        if a.get("verification_status") == "agency_policy_only":
            notes.append("licence evidence is agency-wide policy only")
        out.append({
            "source_id": sid, "title": r["title"], "corpus_role": r["corpus_role"],
            "license_type": r["license_type"] or "", "license_version": r["license_version"] or "",
            "rights_status": r["rights_status"], "category": category,
            "content_review_status": r["content_review_status"] or "", "quarantined": quarantined,
            "chunks": r["chunks"], "eligible_chunks": r["eligible_chunks"], "eligible_tokens": r["eligible_tokens"],
            "unverified_chunks": r["unverified"], "page_provenance": provenance, "technically_eligible": technically,
            "rights_blockers": "; ".join(blockers) if has_doc else "n/a (no full text)",
            "cohere_assessment": a.get("cohere_processing_allowed", "n/a"),
            "external_llm_assessment": a.get("external_llm_processing_allowed", "n/a"),
            "expert_review_required": has_doc, "approval_status": "NOT_APPROVED", "notes": "; ".join(notes),
        })

    path = REPORTS / "embedding_candidate_matrix.csv"
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)
    tech = [o for o in out if o["technically_eligible"]]
    summary = {
        "date": date.today().isoformat(), "embedding_profile": PROFILE, "chunking_profile": profile.chunking_profile,
        "sources": len(out), "by_category": dict(Counter(o["category"] for o in out)),
        "technically_eligible": len(tech), "technically_eligible_chunks": sum(o["eligible_chunks"] for o in tech),
        "technically_eligible_tokens": sum(o["eligible_tokens"] for o in tech),
        "technically_eligible_by_cohere_assessment": dict(Counter(o["cohere_assessment"] for o in tech)),
        "approved": sum(o["approval_status"] != "NOT_APPROVED" for o in out),
        "file": path.relative_to(ROOT).as_posix(),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
