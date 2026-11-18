"""License evidence audit for the 73 corpus documents (read-only: writes reports, never the database).

For every source the audit reads the licence statement from the ORIGINAL file (JATS <license> for
PMC XML, the public-domain statement in NIH HTML, the licence page text in PDFs, the agency reuse
policy for CDC pages), compares it with the catalog label, and assesses each action strictly from
the licence wording. Assessments are evidence, not permissions: the effective *_allowed flags in
the database are set only by the project owner.

Assessment vocabulary (per action):
  yes_by_license      the licence text grants it
  nc_only_by_license  granted for non-commercial purposes only
  no_by_license       the licence excludes it
  conditional         granted with conditions that need a decision (e.g. agency "most content")
  pending_decision    depends on provider terms / owner decision, not on the licence alone
  blocked             a known conflict prevents it under current conditions
  unknown             no evidence
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

ACTIONS = (
    "archive_allowed", "text_mining_allowed", "chunking_allowed", "embedding_allowed", "cohere_processing_allowed",
    "external_llm_processing_allowed", "commercial_use_allowed", "attribution_required", "share_alike_required",
)
CC_URL = re.compile(r"creativecommons\.org/licenses/([a-z-]+)/(\d\.\d)(/igo)?", re.I)
CC_TEXT = re.compile(r"\bCC (BY(?:-NC)?(?:-SA)?(?:-ND)?) (\d\.\d)( IGO)?\b")
PD_STATEMENT = re.compile(r"[^.<>]{0,120}\bpublic domain\b[^.<>]{0,160}\.", re.I)
TAG = re.compile(r"<[^>]+>")

# Agency reuse policies cached during the October 2026 source review (Carobud_ASD_2026, read-only).
AGENCY_POLICIES = {
    "cdc.gov": ("https://www.cdc.gov/other/agencymaterials.html",
                "Most of the information on the CDC and ATSDR websites is not subject to copyright, is in the public "
                "domain, and may be freely used or reproduced without obtaining copyright permission. ... A federal "
                "government website may have a mix of public domain and copyright-protected materials."),
    "nidcd.nih.gov": ("https://www.nidcd.nih.gov/policies",
                      "Unless otherwise stated, the information on this site is not copyrighted and is in the public "
                      "domain."),
}


@dataclass
class Evidence:
    source_id: str
    title: str
    original_format: str
    source_url: str
    license_name: str = "Unknown"
    license_version: str = ""
    license_url: str = ""
    rights_holder: str = ""
    statement: str = ""
    evidence_url: str = ""
    evidence_location: str = ""
    verification_status: str = "unknown"
    notes: list[str] = field(default_factory=list)


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", text))).strip()


def classify_cc(url_or_text: str) -> tuple[str, str] | None:
    """('CC BY-NC-SA', '3.0 IGO') from a CC licence URL or a 'CC BY-NC-SA 3.0 IGO' string."""
    if m := CC_URL.search(url_or_text):
        return "CC " + m.group(1).upper(), m.group(2) + (" IGO" if m.group(3) else "")
    if m := CC_TEXT.search(url_or_text):
        return "CC " + m.group(1), m.group(2) + (m.group(3) or "")
    return None


def from_jats(ev: Evidence, xml: str) -> None:
    hrefs = re.findall(r'<license[^>]*xlink:href="([^"]+)"', xml) + \
        re.findall(r"<ali:license_ref[^>]*>([^<]+)</ali:license_ref>", xml)
    license_p = re.search(r"<license\b.*?</license>", xml, re.S)
    holder = re.search(r"<copyright-holder>(.*?)</copyright-holder>", xml, re.S)
    statement = re.search(r"<copyright-statement>(.*?)</copyright-statement>", xml, re.S)
    ev.evidence_location = "original JATS XML <license>"
    if hrefs and (cc := classify_cc(hrefs[0])):
        ev.license_name, ev.license_version = cc
        ev.license_url = hrefs[0]
        ev.verification_status = "evidence_in_original_document"
        if len(set(hrefs)) > 1:
            ev.notes.append(f"multiple licence refs in XML: {sorted(set(hrefs))}")
    ev.statement = _clean(license_p.group(0))[:400] if license_p else ""
    ev.rights_holder = _clean(holder.group(1)) if holder else (_clean(statement.group(1))[:160] if statement else "")


def from_public_domain_html(ev: Evidence, page: str) -> None:
    ev.evidence_location = "original HTML"
    if m := PD_STATEMENT.search(_clean(page)):
        ev.license_name, ev.statement = "Public Domain", m.group(0).strip()
        ev.verification_status = "evidence_in_original_document"
        ev.rights_holder = "U.S. Government (NIH)"


def from_pdf_text(ev: Evidence, text: str) -> None:
    pattern = r"[^\n]{0,200}(?:creativecommons\.org/licenses/[^\s);]+|CC BY[-A-Z]* \d\.\d(?: IGO)?)[^\n]{0,160}"
    for m in re.finditer(pattern, text):
        if "Giấy phép:" in m.group(0):  # skip the Vietnamese metadata header added during conversion
            continue
        if cc := classify_cc(m.group(0)):
            page = re.findall(r"<!-- SOURCE_PDF_PAGE (\d+) -->", text[: m.start()])
            ev.license_name, ev.license_version = cc
            ev.statement = m.group(0).strip()[:400]
            where = f" page {page[-1]}" if page else ""
            ev.evidence_location = f"PDF text{where} (converted corpus text; PDF not re-parsed)"
            ev.verification_status = "evidence_in_original_document"
            break
    holder = re.search(r"(©|Copyright ©)\s*([^.\n]{3,80})", text)
    ev.rights_holder = holder.group(2).strip() if holder else ""


def from_agency_policy(ev: Evidence) -> None:
    for domain, (url, quote) in AGENCY_POLICIES.items():
        if domain in ev.source_url:
            ev.license_name, ev.statement, ev.evidence_url = "Public Domain", quote, url
            ev.evidence_location = "agency reuse policy (no statement on the captured page)"
            ev.verification_status = "agency_policy_only"
            agency = domain.split(".")[0].upper()
            ev.rights_holder = f"U.S. Government ({agency})"
            ev.notes.append(f"{agency} site-wide policy only (no statement on the captured page); "
                            "page-level third-party content not checked")


def collect(record: dict, manifest_row: dict, root: Path) -> Evidence:
    rights = record.get("rights") or {}
    ev = Evidence(record["source_id"], record.get("title") or "", record.get("original_format") or "",
                  record.get("source_url") or "", evidence_url=rights.get("evidence_url") or "")
    original = root / manifest_row["raw_original_path"]
    if original.suffix == ".xml":
        from_jats(ev, original.read_text(encoding="utf-8", errors="replace"))
    elif original.suffix == ".html":
        from_public_domain_html(ev, original.read_text(encoding="utf-8", errors="replace"))
        if ev.verification_status == "unknown":
            from_agency_policy(ev)
    elif original.suffix == ".pdf":
        from_pdf_text(ev, (root / manifest_row["path"]).read_text(encoding="utf-8"))
    else:
        from_agency_policy(ev)
    if ev.license_url == "" and ev.license_name.startswith("CC"):
        ev.license_url = rights.get("license_url") or rights.get("license") or ""
    if not ev.rights_holder:
        ev.notes.append("rights holder not stated in the original")
    if third := rights.get("third_party_exceptions"):
        ev.notes.append(f"third-party material: {third}")
    catalog_cc = classify_cc(rights.get("license") or "")
    if catalog_cc and catalog_cc[0] != ev.license_name:
        ev.verification_status = "conflict"
        ev.notes.append(f"catalog licence {catalog_cc} differs from original {ev.license_name}")
    return ev


def assess(ev: Evidence, cohere_blocks_nc: bool) -> dict[str, str]:
    """Licence-level assessment per action. Never returns a permission for provider/LLM processing."""
    name = ev.license_name
    if name == "CC BY":
        base = commercial = attribution = "yes_by_license"
        share_alike = "no_by_license"
    elif name in ("CC BY-NC", "CC BY-NC-SA"):
        base, commercial, attribution = "nc_only_by_license", "no_by_license", "yes_by_license"
        share_alike = "yes_by_license" if name.endswith("SA") else "no_by_license"
    elif name == "Public Domain":
        conditional = ev.verification_status == "agency_policy_only"
        base = "conditional" if conditional else "yes_by_license"
        commercial = "conditional" if conditional else "yes_by_license"
        attribution, share_alike = "conditional", "no_by_license"  # agencies request credit, not a licence term
    else:
        return dict.fromkeys(ACTIONS, "unknown")
    cohere = "blocked" if (cohere_blocks_nc and base == "nc_only_by_license") else "pending_decision"
    return {
        "archive_allowed": base, "text_mining_allowed": base, "chunking_allowed": base, "embedding_allowed": base,
        "cohere_processing_allowed": cohere, "external_llm_processing_allowed": "pending_decision",
        "commercial_use_allowed": commercial, "attribution_required": attribution,
        "share_alike_required": share_alike,
    }
