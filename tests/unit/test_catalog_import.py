from app.ingest.catalog_import import (
    QUALITY_HOLD_WARNING,
    TEXT_FIDELITY_WARNING,
    content_warning,
    document_row,
    doi_from_url,
    license_fields,
    page_count,
    publication_year,
    rights_row,
)


def test_publication_year_and_doi():
    assert publication_year("2024-Jan") == 2024
    assert publication_year(None) is None
    assert doi_from_url("https://doi.org/10.1177/10731911231173089") == "10.1177/10731911231173089"
    assert doi_from_url("https://www.cdc.gov/autism") is None


def test_license_fields_names_cc_urls_and_keeps_free_text():
    assert license_fields("https://creativecommons.org/licenses/by-nc/4.0/", None) == (
        "CC BY-NC 4.0", "https://creativecommons.org/licenses/by-nc/4.0/")
    assert license_fields("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/") == (
        "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/")


def test_content_warning_priority():
    assert content_warning({"conversion": {"gaps": [{"type": "text_fidelity"}]}}) == TEXT_FIDELITY_WARNING
    assert content_warning({"quality_hold": True}) == QUALITY_HOLD_WARNING
    assert content_warning({"conversion": {"gaps": [{"type": "graphic"}]}}) is None


def test_rights_row_never_claims_processing_permission():
    row = rights_row({"source_id": "S", "checked_at": "2026-10-17",
                      "rights": {"status": "verified_noncommercial_research", "license": "CC BY 4.0"}})
    assert "not verified" in row["permitted_use_notes"]
    assert not {"embedding_allowed", "cohere_processing_allowed", "commercial_use_allowed"} & set(row)


def test_document_row_quarantines_fidelity_warnings_and_counts_pages():
    manifest = {"source_id": "S", "version": "v1", "raw_document_path": "data/raw/x.md",
                "path": "data/corpus/gaps/S.md",
                "raw_original_path": "data/raw/o/S.pdf", "sha256": "a" * 64, "characters": 10, "tier": "gaps",
                "conversion_gaps": {"text_fidelity": 1}}
    raw = {"conversion": {"status": "complete_text_with_gaps", "gaps": [{"type": "text_fidelity"}]},
           "original_format": "pdf", "original_sha256": "b" * 64}
    row = document_row(manifest, raw, "<!-- SOURCE_PDF_PAGE 1 -->\n<!-- SOURCE_PDF_PAGE 7 -->")
    assert row["content_review_status"] == "quarantined" and row["content_warning"] == TEXT_FIDELITY_WARNING
    assert row["document_id"] == "S@v1" and row["text_completeness"] == "partial"
    assert "approved_for_embedding" not in row
    assert page_count("no markers") is None


def test_rights_row_uses_curated_classification_but_never_permissions():
    raw = {"source_id": "S", "checked_at": "2026-10-17",
           "rights": {"status": "verified_noncommercial_research", "license": "https://creativecommons.org/licenses/by/4.0/"}}
    catalog = {"rights_status": "verified_cc_by", "license_type": "CC BY", "license_version": "4.0",
               "rights_holder": "Smith", "rights_status_original": "verified_noncommercial_research",
               "license_correction_id": "LC-2026-11-14-S"}
    row = rights_row(raw, catalog)
    assert (row["rights_status"], row["license_type"], row["license_version"]) == ("verified_cc_by", "CC BY", "4.0")
    assert "LC-2026-11-14-S" in row["permitted_use_notes"] and "not verified" in row["permitted_use_notes"]
    assert not any(k.endswith("_allowed") for k in row)
    assert rights_row(raw)["rights_status"] == "verified_noncommercial_research"  # no curation: raw label
