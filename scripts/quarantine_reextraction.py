"""Build review dossiers for the two quarantined documents (no DB writes, no network, corpus untouched).

ASD-CSV-077: every table cell of the JATS original that contains <break/> is re-extracted with the
  line breaks kept as separators, compared with the run-together text in the corpus, and checked
  number-for-number. Output: data/extractions/ASD-CSV-077/table_cells.jats-breaks.v1.json
NIH-NIMH-CHILDREN: the list items of the 2-column table are compared with the original HTML and with
  the section_v2_1 table chunk. Output: data/extractions/NIH-NIMH-CHILDREN/table_list_items.v1.json

These are PROPOSALS for a human reviewer. Quarantine is not lifted and nothing is approved here.

Usage:
  python -B scripts/quarantine_reextraction.py
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import itertools

from app.config import CORPUS_MANIFEST, ROOT
from app.ingest.chunking import ChunkingProfile, DocumentInfo, HFTokenCounter, chunk_document

OUT = ROOT / "data" / "extractions"
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def plain(fragment: str) -> str:
    fragment = re.sub(r"<xref[^>]*>(.*?)</xref>", r"\1", fragment, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def with_breaks(cell: str) -> tuple[str, int]:
    """A JATS <break/> is a line break: it may be a visual wrap ("40<break/>(98th)" = "40 (98th)") or separate
    list items. Its faithful text form is whitespace — adding "; " would turn "40 (98th)" into two values.
    Returns (text, ambiguous) where `ambiguous` counts breaks that may separate items with no punctuation
    (previous part ends without punctuation and the next starts with a capital) — for the human reviewer."""
    parts = [p for p in (plain(p) for p in re.split(r"<break\s*/>", cell)) if p]
    ambiguous = sum(1 for a, b in itertools.pairwise(parts)
                    if not a.endswith((";", ":", ",", ".", "-")) and b[:1].isupper())
    return " ".join(parts), ambiguous


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asd_csv_077(m: dict) -> dict:
    xml_path = ROOT / m["raw_original_path"]
    xml = xml_path.read_text(encoding="utf-8")
    corpus_plain = plain((ROOT / m["path"]).read_text(encoding="utf-8"))  # compare tag-free text on both sides
    cells = []
    for t_index, wrap in enumerate(re.findall(r"<table-wrap\b.*?</table-wrap>", xml, re.S)):
        label = plain((re.search(r"<label>(.*?)</label>", wrap, re.S) or [None, ""])[1])
        for r_index, row in enumerate(re.findall(r"<tr\b.*?</tr>", wrap, re.S)):
            for c_index, cell in enumerate(re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, re.S)):
                if "<break" not in cell:
                    continue
                current = re.sub(r"<break\s*/>", "", cell)
                current_text = plain(current)
                proposed, ambiguous = with_breaks(cell)
                cells.append({
                    "table": label, "table_index": t_index, "row": r_index, "column": c_index,
                    "current_extraction": current_text, "proposed_extraction": proposed,
                    "ambiguous_item_boundaries": ambiguous,
                    "current_found_in_corpus": current_text.replace(" ", "") in corpus_plain.replace(" ", ""),
                    "numbers_identical": sorted(NUMBER.findall(current_text)) == sorted(NUMBER.findall(proposed)),
                })
    return {"source_id": m["source_id"], "status": "proposal_pending_human_review_quarantine_kept",
            "original_file": m["raw_original_path"], "original_sha256": sha(xml_path),
            "corpus_file": m["path"], "corpus_sha256": sha(ROOT / m["path"]),
            "defect": "JATS <break/> inside table cells was dropped during XML-to-Markdown conversion",
            "cells_with_breaks": len(cells), "cells": cells,
            "proposal_rule": "replace each <break/> with one space (no separator is inferred)",
            "cells_with_ambiguous_item_boundaries": sum(c["ambiguous_item_boundaries"] > 0 for c in cells),
            "all_numbers_identical": all(c["numbers_identical"] for c in cells),
            "all_current_text_in_corpus": all(c["current_found_in_corpus"] for c in cells)}


def nimh_children(m: dict) -> dict:
    original = ROOT / m["raw_original_path"]
    page = original.read_text(encoding="utf-8")
    corpus = (ROOT / m["path"]).read_text(encoding="utf-8")
    squash = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()  # noqa: E731
    items = [squash(i) for i in re.findall(r"<li[^>]*>(.*?)</li>", corpus, re.S)]
    original_text = squash(page)
    profile = ChunkingProfile.load("section_v2_1")
    counter = HFTokenCounter(profile.tokenizer_path, profile.tokenizer_sha256)
    info = DocumentInfo(m["source_id"], m["source_id"], m["title"], m["tier"], m["source_type"], "en",
                        m["conversion_gaps"])
    chunks = chunk_document(corpus, info, profile, counter).chunks
    table = next(c for c in chunks if c.content_kind == "table" and "Younger children" in c.content)
    separated = sum(item in table.content for item in items)
    return {"source_id": m["source_id"], "status": "proposal_pending_human_review_quarantine_kept",
            "original_file": m["raw_original_path"], "original_sha256": sha(original),
            "corpus_file": m["path"], "corpus_sha256": sha(ROOT / m["path"]),
            "defect": "list items inside a 2-column HTML table were run together when tags were stripped",
            "list_items": len(items), "items_verbatim_in_original": sum(i in original_text for i in items),
            "items_present_in_v2_1_table_chunk": separated,
            "v2_1_table_chunk": {"chunk_index": table.chunk_index, "content_sha256": table.content_sha256,
                                 "tokens": table.token_count, "content": table.content},
            "sensitive_content": "older-children list includes self-harm and suicidal thoughts: route to safety branch"}


def main() -> int:
    manifest = {(m := json.loads(x))["source_id"]: m for x in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines()
                if x.strip()}
    summary = {}
    for sid, build in (("ASD-CSV-077", asd_csv_077), ("NIH-NIMH-CHILDREN", nimh_children)):
        dossier = build(manifest[sid])
        name = "table_cells.jats-breaks.v1.json" if sid == "ASD-CSV-077" else "table_list_items.v1.json"
        out = OUT / sid / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(dossier, ensure_ascii=False, indent=1), encoding="utf-8")
        summary[sid] = {k: v for k, v in dossier.items() if k not in ("cells", "v2_1_table_chunk")} | {
            "file": out.relative_to(ROOT).as_posix(), "sha256": sha(out)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
