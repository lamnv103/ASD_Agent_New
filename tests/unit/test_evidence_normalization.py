"""T5.2 Phase C: evidence normalization. Table fixtures use the real markdown-pipe-table shape observed
in this corpus (caption glued to an asset id, header row, '|---|---|' separator, data rows) — not a
synthetic format invented for the test."""

from app.answer.evidence_normalization import classify, extract_ages, table_cell


def test_paragraph_is_the_default_for_plain_prose():
    text = "Autism spectrum disorder is a developmental disability affecting communication."
    result = classify(text)
    assert result.kind == "paragraph"
    assert result.paragraph.text == text


def test_list_items_are_split_and_kept_verbatim():
    text = ("Examples of social communication characteristics can include * Avoids or does not keep "
            "eye contact * Does not respond to name by 9 months of age * Does not point to show you "
            "something interesting by 18 months of age")
    result = classify(text)
    assert result.kind == "list"
    assert "can include" in result.list_.intro
    assert len(result.list_.items) == 3
    assert "eye contact" in result.list_.items[0]
    assert result.list_.item_ages[1] == ["9"]
    assert result.list_.item_ages[2] == ["18"]


def test_table_header_and_rows_are_kept_aligned_not_separated():
    text = (
        "brainsci-10-00441-t002_Table 2Table 2 Evidence-based pediatric sleep practice recommendations "
        "of the 'ABCs of SLEEPING' mnemonic.\n"
        "| Practice Area | Recommendation | Level of Empirical Support |\n"
        "|---|---|---|\n"
        "| Age-appropriate Bedtime | Set a consistent bedtime of 8-9pm | High |\n"
        "| Avoid screens before bed | No screens for 1 hour before bedtime | Moderate |\n"
    )
    result = classify(text)
    assert result.kind == "table"
    assert result.table.columns == ["Practice Area", "Recommendation", "Level of Empirical Support"]
    assert len(result.table.rows) == 2
    assert result.table.rows[0]["Practice Area"] == "Age-appropriate Bedtime"
    assert result.table.rows[0]["Recommendation"] == "Set a consistent bedtime of 8-9pm"
    assert result.table.rows[0]["Level of Empirical Support"] == "High"


def test_table_cell_lookup_preserves_units_and_does_not_mix_rows():
    text = (
        "Dosage table.\n"
        "| Antihistamine | Dosage | Effects on Sleep |\n"
        "|---|---|---|\n"
        "| Diphenhydramine | 0.5 mg/kg up to 50mg | Sedating |\n"
        "| Hydroxyzine | 0.5-1 mg/kg | Sedating |\n"
    )
    result = classify(text)
    dose = table_cell(result.table, "Dosage", {"Antihistamine": "Diphenhydramine"})
    assert dose == "0.5 mg/kg up to 50mg"  # unit preserved verbatim, not reduced to a bare number
    other = table_cell(result.table, "Dosage", {"Antihistamine": "Hydroxyzine"})
    assert other == "0.5-1 mg/kg" and other != dose  # rows are not conflated


def test_a_row_with_a_different_cell_count_than_the_header_is_not_force_fit():
    text = (
        "| A | B | C |\n"
        "|---|---|---|\n"
        "| 1 | 2 | 3 |\n"
        "| only two cells |\n"
    )
    result = classify(text)
    assert result.kind == "table"
    assert len(result.table.rows) == 1  # the malformed second row is dropped, not guessed


def test_malformed_table_falls_back_to_paragraph_not_a_guessed_table():
    text = "This mentions a | pipe | character but is not a real table at all."
    result = classify(text)
    assert result.kind == "paragraph"


def test_extract_ages_handles_vietnamese_and_english_units():
    assert extract_ages("by 18 months of age") == ["18"]
    assert extract_ages("ở trẻ 18 tháng") == ["18"]
    assert extract_ages("no age mentioned here") == []


def test_classify_also_reports_all_ages_found_anywhere_in_the_excerpt():
    text = "Signs at 9 months include X. By 18 months, Y should appear."
    result = classify(text)
    assert result.source_ages == ["9", "18"]


def test_trailing_keep_reading_boilerplate_is_stripped_not_glued_to_the_last_item():
    text = ("Examples can include * First sign * Second sign by 18 months of age\n\n"
            "Keep Reading: Screening for Autism Spectrum Disorder")
    result = classify(text)
    assert result.kind == "list"
    assert "Keep Reading" not in result.list_.items[-1]


def test_boilerplate_marker_in_the_middle_of_real_content_is_not_destroyed():
    text = "Image: mom holding baby on lap and reading a book\n\nReal tip: read with your child daily."
    result = classify(text)
    assert "Real tip" in result.paragraph.text
