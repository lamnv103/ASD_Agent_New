"""T5.5 Phase 1/2 — read-only FTS diagnostics for the 31 independent-set cache-miss questions.

Dense retrieval cannot be run live for these queries (no cached query vector, and live Cohere embedding
is APPROVAL_REQUIRED per T2.6 — never attempted here). FTS (app/retrieval/fts.py) needs no embedding at
all, so it is used here as the only cache-only-compliant tool to check whether the corpus actually
contains relevant content for each cache-missed question.

Read-only: research_reader role only, no writes to the DB, no API calls. Output written only to
eval/reports/t5_5_fts_diagnostics.json.
"""

import json
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

from app.config import ROOT
from app.nlp.text_match import chunk_matches_terms, fold, specific_terms
from app.retrieval.fts import FtsProfile, FtsRetriever, Glossary

INDEPENDENT = ROOT / "eval" / "datasets" / "independent_eval_v1.jsonl"
RESULTS = ROOT / "eval" / "reports" / "independent_30_results.json"
OUT = ROOT / "eval" / "reports" / "t5_5_fts_diagnostics.json"
K = 10

PROFILES = ["fts_a_baseline_v1", "fts_b_glossary_and_v1", "fts_c_glossary_or_v1"]


def classify_chunk(query: str, title: str, section: str, content: str) -> str:
    """Reuse the Evidence-Gate-style term check (app.nlp.text_match), not the gate itself (gate needs a
    cosine_similarity field FTS hits do not have). direct/indirect/generic/none."""
    terms = specific_terms(query)
    heading = f"{title} {section}"
    searchable = f"{heading} {content}"
    if not terms:
        return "generic"
    if chunk_matches_terms(heading, terms):
        return "direct"
    if chunk_matches_terms(searchable, terms):
        return "indirect"
    return "none"


def main() -> int:
    with open(INDEPENDENT, encoding="utf-8") as f:
        records = {r["id"]: r for r in (json.loads(x) for x in f if x.strip())}
    with open(RESULTS, encoding="utf-8") as f:
        results = {r["id"]: r for r in json.load(f)}
    cache_miss_ids = [i for i, r in results.items() if r.get("error_code") == "QUERY_NOT_CACHED"]

    glossary = Glossary(ROOT / "config" / "query_glossary_vi_en_v1.json")
    retrievers = {}
    for code in PROFILES:
        prof = FtsProfile.load(code)
        retrievers[code] = FtsRetriever(prof, glossary=glossary if prof.query_mode != "plain_and" else None)

    out = []
    for qid in sorted(cache_miss_ids, key=lambda x: int(x[2:])):
        rec = records[qid]
        q = rec["question"]
        row = {"id": qid, "question": q, "category": rec["category"], "notes": rec.get("notes"),
               "folded_query": fold(q), "glossary_concepts_matched_answergen": specific_terms(q),
               "systems": {}}
        for code, ret in retrievers.items():
            resp = ret.retrieve(q, k=K, question_id=qid)
            hits = []
            for h in resp.results:
                hits.append({
                    "rank": h.rank, "chunk_id": h.chunk_id, "source_id": h.source_id, "title": h.title,
                    "section": h.section, "score": round(h.score, 6),
                    "classification": classify_chunk(q, h.title, h.section, h.content),
                    "content_preview": h.content[:220].replace("\n", " "),
                })
            row["systems"][code] = {
                "status": resp.status, "returned": len(hits),
                "expansion_concepts": [c["concept"] for c in resp.expansion.get("concepts", [])],
                "unmapped_words": resp.expansion.get("unmapped_words", []),
                "tsquery": resp.tsquery, "hits": hits,
            }
        out.append(row)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"Total cache-miss questions diagnosed: {len(out)}")
    for row in out:
        best = "none"
        for code in PROFILES:
            classes = [h["classification"] for h in row["systems"][code]["hits"]]
            if "direct" in classes:
                best = "direct"
                break
            if "indirect" in classes and best == "none":
                best = "indirect"
            if "generic" in classes and best == "none":
                best = "generic"
        print(f"{row['id']:6s} {row['category']:25s} best={best:8s} "
              f"A={row['systems']['fts_a_baseline_v1']['returned']:2d} "
              f"B={row['systems']['fts_b_glossary_and_v1']['returned']:2d} "
              f"C={row['systems']['fts_c_glossary_or_v1']['returned']:2d} "
              f"concepts={row['glossary_concepts_matched_answergen']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
