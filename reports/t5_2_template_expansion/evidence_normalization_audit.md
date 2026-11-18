# T5.2 Phase C — Evidence Normalization Audit

New module: `app/answer/evidence_normalization.py`, read-only over the string the database already
returns; never touches the corpus. 10 unit tests (`tests/unit/test_evidence_normalization.py`), all
built from the actual markdown-pipe-table and bulleted-list shapes observed in this corpus, not
synthetic formats invented for convenience.

## Paragraph evidence

Default classification for anything not recognized as a table or list. No special handling needed
beyond trailing-boilerplate stripping (below).

## Heading evidence

Not emitted as a standalone kind by `classify()` — title/section are already passed to callers
separately by `RetrievedChunk`, so there was nothing additional to normalize here. Named in the module
docstring for completeness, per the task's explicit list, not implemented as dead code.

## List evidence

Bulleted lists (`* item`) are split into an `intro` sentence (the text before the first bullet, if any)
and `items`. Each item's mentioned age(s) are extracted and kept alongside it (`item_ages`), never
discarded — this is what lets `signs_by_age` show exactly the sign tied to the age actually asked about,
unlike the T3/T4-era behavior that mixed age-tagged signs with unrelated generic milestone chunks (the
"Lỗi 7" finding). Verified against the real `CDC-ASD-SIGNS` excerpt live during this task (re-produced
in `template_specifications.md`).

**Real bug found and fixed while building this**: the raw excerpt ends with a boilerplate footer ("Keep
Reading: Screening for Autism Spectrum Disorder") that would otherwise be glued onto the last bullet
item's text. Fixed with `strip_boilerplate()`, which removes trailing lines matching known CDC footer
patterns **from the end only** — verified by a dedicated test
(`test_boilerplate_marker_in_the_middle_of_real_content_is_not_destroyed`) that an "Image:" marker
appearing mid-document, followed by real content (as seen in `CDC-MILESTONES-18` excerpts), is never
stripped — only genuine trailing footers are.

## Table evidence

Markdown pipe tables (`| a | b | c |` header, `|---|---|---|` separator, data rows) are parsed into a
`TableEvidence` with `columns` and `rows` (each row a column-name → cell-value dict). Checked directly
against the real sleep-recommendation table in `ASD-OA-PMC7407189` (the "ABCs of SLEEPING" mnemonic,
14 practice recommendations across 3 columns).

**Real finding**: this table uses merged/continuation rows in its markdown source — e.g. the first
practice area ("Age-appropriate Bedtime...") is followed by two more rows that have only 2 cells
instead of 3, implicitly continuing the same practice area. Per the task's explicit rule ("Không tách
một hàng khỏi tiêu đề cột... không làm thay đổi quan hệ giữa cột và giá trị"), the parser **stops at the
first row whose cell count doesn't match the header** rather than guessing which column the 2 cells
belong to. Result: only 1 of the 14 recommendations could be safely extracted from this table. This is
disclosed as a real, bounded limitation (not silently worked around) in
`template_specifications.md`'s `sleep_nonpharma` spec and in `remaining_limitations.md` — the
`sleep_nonpharma` template cites only that one safely-extracted row and says so explicitly in its text
("Đây chỉ là một trong nhiều khuyến nghị được tổng quan...").

A second table test (`test_table_cell_lookup_preserves_units_and_does_not_mix_rows`) confirms a cell
value with a unit ("0.5 mg/kg up to 50mg") is returned verbatim, not reduced to a bare number, and that
two rows' values are never conflated — directly testing the task's "không mất đơn vị đo" and "không làm
thay đổi quan hệ giữa cột và giá trị" rules. This lookup function (`table_cell`) was not needed by any
of the 10 implemented templates in the end (the sleep table only needed the single safely-parsed row
directly), but is tested and available for future table-based templates.

## Age-context evidence

`extract_ages()` recognizes both Vietnamese ("18 tháng," "3 tuổi") and English ("18 months," "3 years")
age mentions via one regex — tested with both. Used by `signs_by_age` (per-item) and by the existing
`evidence_gate.py`'s `age_mismatch` flag (T4, unchanged, reused here, not duplicated).

## Multiple-audience evidence

Not implemented as a distinct normalization step. The closest real case found was `adolescence_asd`'s
source, which discusses ASD, ADHD, and intellectual disability together as a group of "neurodevelopmental
disorders" — handled at the template-authoring level (the Vietnamese text names ASD specifically and
does not generalize claims to the other conditions), not by a generic code mechanism. Building a general
"multiple audience" detector was considered out of scope for the 10 templates actually needed in this
task; flagged in `remaining_limitations.md` as unimplemented, not silently assumed unnecessary.

## Corpus integrity

No corpus file, raw document, or database row was modified by this module or its tests — it operates
entirely on strings already returned by the existing read-only retrieval pipeline.
