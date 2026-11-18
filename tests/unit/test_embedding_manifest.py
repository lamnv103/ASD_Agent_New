from app.ingest.embedding_manifest import ChunkRow, chunk_exclusion, classify, group_membership, valid_url

TEXT = "Early intervention improves social communication outcomes in young autistic children."


def row(chunk_id="D#p#0001", **kw) -> ChunkRow:
    base = dict(chunk_id=chunk_id, document_id="D", source_id="S", section_type="body",
                completeness_status="complete", retrieval_eligible=True, content=TEXT, content_sha256="h1",
                file_format="xml", page_start=None, page_end=None, char_start=0, char_end=90)
    return ChunkRow(**(base | kw))


def test_verified_content_chunk_is_eligible():
    assert chunk_exclusion(row()) is None


def test_unverified_structure_is_excluded_with_its_status():
    for status in ("table_structure_unrecoverable", "table_recovered_pending_review", "text_encoding_lost"):
        assert chunk_exclusion(row(completeness_status=status, retrieval_eligible=False)) == status


def test_non_content_sections_are_excluded():
    assert chunk_exclusion(row(section_type="references", retrieval_eligible=False)) == "non_content_section:references"


def test_glyph_garbage_is_excluded_even_if_flagged_eligible():
    assert chunk_exclusion(row(content=TEXT + " /gid00012/gid00034")) == "text_encoding_lost"


def test_provenance_rules_differ_for_pdf_and_text():
    assert chunk_exclusion(row(file_format="pdf", page_start=None, page_end=None)) == "missing_provenance"
    assert chunk_exclusion(row(file_format="pdf", page_start=3, page_end=4)) is None
    assert chunk_exclusion(row(char_start=None)) == "missing_provenance"


def test_undetermined_section_and_fragments_are_excluded():
    assert chunk_exclusion(row(section_type="unclassified")) == "undetermined_content_section"
    assert chunk_exclusion(row(content="HAZ 9 RCTs No serious")) == "fragment_too_short"
    assert chunk_exclusion(row(content="Plays games with you, like pat-a-cake")) is None


def test_empty_chunk_is_excluded():
    assert chunk_exclusion(row(content="  \n")) == "empty_chunk"


def test_exact_duplicates_keep_the_first_chunk_id_deterministically():
    rows = [row("B#p#0001"), row("A#p#0001"), row("C#p#0001", content_sha256="h2")]
    assert classify(rows) == {"A#p#0001": None, "B#p#0001": "duplicate_content_of:A#p#0001", "C#p#0001": None}
    assert classify(reversed(rows)) == classify(rows)


def test_excluded_duplicate_does_not_become_the_keeper():
    rows = [row("A#p#0001", completeness_status="text_encoding_lost", retrieval_eligible=False), row("B#p#0001")]
    assert classify(rows)["B#p#0001"] is None


def test_group_membership_and_urls():
    assert group_membership("core", "verified_noncommercial_research", "agency_policy_only") == ("A", "B", "C")
    assert group_membership("metadata_only", "unknown", "") == ()
    assert valid_url("https://www.cdc.gov/autism/index.html")
    assert not valid_url("www.cdc.gov") and not valid_url("https://x y.org") and not valid_url(None)
