"""T5.6 Phase 2 — isolated, read-only FTS improvement experiments.

Does NOT modify app/retrieval/fts.py, config/fts_profiles.json, or any glossary file. Reuses their
classes (Glossary, FtsProfile, FtsReader) exactly as built; only the QUERY-COMPOSITION and POST-FILTER
logic here is new, and it lives entirely in this standalone script so it is trivially removable
(rollback = delete this file; nothing else references it).

Two experimental strategies, both testable against the EXISTING glossary (no new glossary content):

  EXP-1 "anchor-excluded, min-2-concept OR" — drop the generic ASD-anchor concepts ("autism", "asd_full")
    from the OR expression entirely (every row in an ASD corpus already satisfies them, so they add zero
    discriminating signal and are the main driver of OR-dilution observed in T5.5), and require the
    tsquery to match at least 2 of the *remaining* concept groups when 2+ exist (falls back to 1 when
    only 1 non-anchor concept was found) -- an OR-of-ANDs over concept pairs, not a flat OR.

  EXP-2 "post-hoc term-specificity filter" — run the existing FTS-B/FTS-C profiles unchanged, then drop
    any hit the app.nlp.text_match classifier would call "generic" or "none" (i.e. keep only hits that
    actually contain the query's specific glossary term in their own text, not just because the query had
    no specific term to check). This directly targets the Case F false-positive (T5.5) where a generic
    word like "treatment" let an off-topic chunk through.

Evaluated on: the 31 T5.5 cache-miss questions, plus a spot-check against 6 of the frozen 66-question set
(q066, q033, q063, q054 -- T2.4's own mandatory test cases -- plus q016, q057) to catch any regression on
already-studied behavior. This script explicitly does NOT claim the 31-question result generalizes; see
t5_6_fts_experiments.md for that disclosure.
"""

import itertools
import json
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

from app.config import ROOT
from app.nlp.text_match import chunk_matches_terms, specific_terms
from app.retrieval.fts import FtsProfile, FtsReader, Glossary, compose_tsquery, term_sql

GLOSSARY_PATH = ROOT / "config" / "query_glossary_vi_en_v1.json"
ANCHOR_CONCEPTS = {"autism", "asd_full"}  # present in virtually every chunk; zero discriminating signal
K = 10


def exp1_tsquery(reader: FtsReader, glossary: Glossary, query: str) -> tuple[str, list[dict]]:
    """Anchor-excluded, min-2-concept-pair OR. Falls back to a single-concept OR if <2 non-anchor
    concepts were found (same permissiveness as FTS-C in that degenerate case, but never lets the
    anchor concept alone drive the match)."""
    exp = glossary.expand(query)
    vi = ""  # deliberately drop the raw-VI plainto branch too: it never matches English content anyway
    # (confirmed in T2.4/T5.5: 0/97 raw-Vietnamese FTS-A hits across both question sets) and including it
    # changes nothing but tsquery text length.
    non_anchor = [c for c in exp.concepts if c.concept not in ANCHOR_CONCEPTS]
    if len(non_anchor) < 2:
        groups_concepts = [non_anchor] if non_anchor else []
    else:
        groups_concepts = list(itertools.combinations(non_anchor, 2))
    if not groups_concepts:
        return "", []
    # Build one OR-of-(AND-pairs) tsquery via raw SQL term lookup (mirrors fts.py's own TERMS_SQL path).
    import psycopg

    from app.db import connect
    with connect(reader.profile.db_role, "t5_6_exp1") as conn:
        conn.read_only = True
        def term_text(term: str) -> str:
            kind, text = term_sql(term)
            fn = "plainto_tsquery" if kind == "all" else "phraseto_tsquery"
            return conn.execute(f"SELECT {fn}(%(cfg)s::regconfig, %(t)s)::text",
                                 {"cfg": reader.profile.ts_config, "t": text}).fetchone()[0]
        pair_clauses = []
        for group in groups_concepts:
            if isinstance(group[0], str):  # the <2-concept fallback: group is one ConceptMatch
                concept_list = groups_concepts  # list[ConceptMatch]
                texts = [t for c in concept_list for t in (term_text(x) for x in c.terms) if t]
                if texts:
                    pair_clauses.append("( " + " | ".join(f"( {t} )" for t in texts) + " )")
                break
            and_parts = []
            for c in group:
                texts = [t for t in (term_text(x) for x in c.terms) if t]
                if texts:
                    and_parts.append("( " + " | ".join(f"( {t} )" for t in texts) + " )")
            if len(and_parts) == len(group):
                pair_clauses.append("( " + " & ".join(and_parts) + " )")
        conn.rollback()
    if not pair_clauses:
        return "", []
    tsq = " | ".join(f"( {c} )" for c in pair_clauses) if len(pair_clauses) > 1 else pair_clauses[0]
    rows = reader._connect()
    try:
        with rows:
            rows.read_only = True
            cur = rows.execute(
                "SELECT chunk_id, source_id, title, section_heading, content, score FROM "
                "(SELECT v.*, ts_rank_cd(v.content_tsv, q.query, %(norm)s) AS score FROM "
                "asd_rag.v_research_retrieval_chunks v CROSS JOIN (SELECT %(tsq)s::tsquery AS query) q "
                "WHERE v.profile_code = %(profile)s AND v.content_tsv @@ q.query) sub "
                "ORDER BY score DESC, chunk_id ASC LIMIT %(k)s",
                {"tsq": tsq, "norm": reader.profile.rank_normalization,
                 "profile": reader.profile.view_profile_code, "k": K})
            names = [d.name for d in cur.description]
            return tsq, [dict(zip(names, r, strict=True)) for r in cur.fetchall()]
    finally:
        rows.close()


def exp2_filter(query: str, hits: list[dict]) -> list[dict]:
    """Keep only hits whose evidence is direct/indirect per app.nlp.text_match -- drop generic/none."""
    terms = specific_terms(query)
    if not terms:
        return []  # no specific term at all: a post-hoc filter cannot rescue this query; be honest
    out = []
    for h in hits:
        heading = f"{h.get('title', '')} {h.get('section_heading', '')}"
        if chunk_matches_terms(heading, terms) or chunk_matches_terms(f"{heading} {h['content']}", terms):
            out.append(h)
    return out


def run_fts_bc(reader: FtsReader, glossary: Glossary, profile: FtsProfile, query: str) -> list[dict]:
    exp = glossary.expand(query)
    rows = reader.search(exp, K)[1]
    return rows


def main() -> int:
    independent = ROOT / "eval" / "datasets" / "independent_eval_v1.jsonl"
    results = ROOT / "eval" / "reports" / "independent_30_results.json"
    with open(independent, encoding="utf-8") as f:
        records = {r["id"]: r for r in (json.loads(x) for x in f if x.strip())}
    with open(results, encoding="utf-8") as f:
        res = {r["id"]: r for r in json.load(f)}
    cache_miss_ids = sorted((i for i, r in res.items() if r.get("error_code") == "QUERY_NOT_CACHED"),
                            key=lambda x: int(x[2:]))

    glossary = Glossary(GLOSSARY_PATH)
    prof_b = FtsProfile.load("fts_b_glossary_and_v1")
    prof_c = FtsProfile.load("fts_c_glossary_or_v1")
    reader_b, reader_c = FtsReader(prof_b), FtsReader(prof_c)

    out = []
    for qid in cache_miss_ids:
        q = records[qid]["question"]
        baseline_c = run_fts_bc(reader_c, glossary, prof_c, q)
        exp2_hits = exp2_filter(q, baseline_c)
        tsq1, exp1_hits = exp1_tsquery(reader_c, glossary, q)
        out.append({
            "id": qid, "category": records[qid]["category"],
            "baseline_c_n": len(baseline_c),
            "baseline_c_top2_sources": [h["source_id"] for h in baseline_c[:2]],
            "exp2_post_filter_n": len(exp2_hits),
            "exp2_top2_sources": [h["source_id"] for h in exp2_hits[:2]],
            "exp1_tsquery": tsq1, "exp1_n": len(exp1_hits),
            "exp1_top2_sources": [h["source_id"] for h in exp1_hits[:2]],
        })
        print(f"{qid:6s} baseline_C n={len(baseline_c):2d} top={out[-1]['baseline_c_top2_sources']}  "
              f"| EXP2(filter) n={len(exp2_hits):2d} top={out[-1]['exp2_top2_sources']}  "
              f"| EXP1(pair-AND) n={len(exp1_hits):2d} top={out[-1]['exp1_top2_sources']}")

    out_path = ROOT / "eval" / "reports" / "t5_6_fts_experiments.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
