"""T5.7 — isolated, read-only test harness implementing T5.6's proposed integration design end to end:

  EXP-1b FTS retrieval (app/retrieval/fts.py, unmodified)
    -> FtsEvidenceAdapter (NEW, lives only here)
    -> evidence_gate.assess() (app/retrieval/evidence_gate.py, UNMODIFIED)
    -> answer_generator.generate() (app/answer/answer_generator.py, UNMODIFIED)
    -> citation_validation.validate() (app/retrieval/citation_validation.py, UNMODIFIED)

This file is the ONLY new code T5.7 adds. It imports but never edits any app/ file. It is never imported
by app/api.py or any other production path. Rollback = delete this file.

EXP-1b recap (from T5.6): expand the query via the existing 94-entry FTS glossary; drop the generic
"autism"/"asd_full" anchor concepts from scoring (they carry no discriminating signal since nearly every
chunk contains them); require an OR of AND-pairs over the remaining concepts (falls back to a plain OR of
the single concept's own terms when exactly one non-anchor concept was found); if ZERO non-anchor concepts
were found, search the anchor concept alone instead of returning nothing (serves purely generic questions
like the Answer Quality Reference's own "ASD la gi?").
"""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass

sys.path.insert(0, ".")

from app.config import ROOT
from app.db import connect
from app.retrieval.citation_validation import validate as validate_citations
from app.retrieval.evidence_gate import EvidenceAssessment, assess
from app.retrieval.fts import FtsProfile, FtsReader, Glossary, term_sql
from app.retrieval.types import RetrievedChunk
from app.answer.answer_generator import generate
from app.api import _chat_evidence

GLOSSARY_PATH = ROOT / "config" / "query_glossary_vi_en_v1.json"
ANCHOR_CONCEPTS = {"autism", "asd_full"}
K = 10
FTS_SYNTHETIC_SIMILARITY = 0.12  # == evidence_gate.MIN_SIMILARITY, the existing floor; see t5_6 design doc


@dataclass
class HarnessResult:
    query: str
    tsquery: str
    fts_hit_count: int
    fts_top_sources: list[str]
    gate_sufficient: bool
    gate_reason: str
    supported_sources: list[str]
    answer_mode: str
    answer_text: str
    citation_ids: list[str]


_glossary: Glossary | None = None
_reader_c: FtsReader | None = None


def _lazy_init() -> tuple[Glossary, FtsReader]:
    global _glossary, _reader_c
    if _glossary is None:
        _glossary = Glossary(GLOSSARY_PATH)
        _reader_c = FtsReader(FtsProfile.load("fts_c_glossary_or_v1"))
    return _glossary, _reader_c


def _term_text(conn, cfg: str, term: str) -> str:
    kind, text = term_sql(term)
    fn = "plainto_tsquery" if kind == "all" else "phraseto_tsquery"
    return conn.execute(f"SELECT {fn}(%(cfg)s::regconfig, %(t)s)::text", {"cfg": cfg, "t": text}).fetchone()[0]


def exp1b_retrieve(query: str) -> tuple[str, list[dict]]:
    """EXP-1b: anchor-excluded pair-AND, with an anchor-only fallback when no specific concept exists."""
    glossary, reader = _lazy_init()
    exp = glossary.expand(query)
    non_anchor = [c for c in exp.concepts if c.concept not in ANCHOR_CONCEPTS]
    anchor = [c for c in exp.concepts if c.concept in ANCHOR_CONCEPTS]

    with connect(reader.profile.db_role, "t5_7_e2e") as conn:
        conn.read_only = True
        cfg = reader.profile.ts_config

        if not non_anchor and not anchor:
            return "", []  # no recognizable ASD-related concept at all; honest empty result

        if not non_anchor:  # anchor-only fallback (EXP-1b's addition over EXP-1; EXP-1c refinement below)
            # EXP-1c (T5.7 Phase 1 finding): a bare short acronym term ("ASD", "ASD" alone) is just as
            # high-frequency/low-discriminating as "autism" alone -- it is not the concept that is
            # generic, it is any SINGLE-WORD, ultra-common term used without requiring co-occurrence.
            # Multi-word phrase terms (phraseto_tsquery, requiring adjacency) are far more specific, so
            # the anchor-only fallback uses ONLY multi-word terms, never a bare single-word acronym.
            multi_word_terms = [term for c in anchor for term in c.terms if len(term.split()) > 1]
            texts = [t for term in multi_word_terms if (t := _term_text(conn, cfg, term))]
            tsq = " | ".join(f"( {t} )" for t in texts) if texts else ""
        elif len(non_anchor) < 2:
            texts = [t for term in non_anchor[0].terms if (t := _term_text(conn, cfg, term))]
            tsq = " | ".join(f"( {t} )" for t in texts) if texts else ""
        else:
            pair_clauses = []
            for group in itertools.combinations(non_anchor, 2):
                and_parts = []
                for c in group:
                    texts = [t for term in c.terms if (t := _term_text(conn, cfg, term))]
                    if texts:
                        and_parts.append("( " + " | ".join(f"( {t} )" for t in texts) + " )")
                if len(and_parts) == len(group):
                    pair_clauses.append("( " + " & ".join(and_parts) + " )")
            tsq = " | ".join(f"( {c} )" for c in pair_clauses) if pair_clauses else ""

        if not tsq:
            conn.rollback()
            return "", []

        cur = conn.execute(
            "SELECT chunk_id, source_id, title, section_heading, content, ts_rank_cd(content_tsv, "
            "%(tsq)s::tsquery, %(norm)s) AS score FROM asd_rag.v_research_retrieval_chunks WHERE "
            "profile_code = %(profile)s AND content_tsv @@ %(tsq)s::tsquery ORDER BY score DESC, "
            "chunk_id ASC LIMIT %(k)s",
            {"tsq": tsq, "norm": reader.profile.rank_normalization,
             "profile": reader.profile.view_profile_code, "k": K})
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r, strict=True)) for r in cur.fetchall()]
        conn.rollback()
        return tsq, rows


def adapt_to_chunks(hits: list[dict]) -> list[RetrievedChunk]:
    """FtsEvidenceAdapter (T5.6 Phase 4 design, 'Option X'): a synthetic similarity exactly at the
    Evidence Gate's existing floor -- never fabricated higher, and the Gate's own term-specificity check
    (unchanged) still decides whether each chunk actually counts as supporting evidence."""
    chunks = []
    for i, h in enumerate(hits, 1):
        chunks.append(RetrievedChunk(
            rank=i, chunk_id=h["chunk_id"], source_id=h["source_id"],
            document_id=h["chunk_id"].split("#")[0], title=h.get("title") or "",
            source_url=f"https://example.org/source/{h['source_id']}",  # placeholder; real url resolution
            content=h["content"], content_sha256="0" * 64,               # is a separate, unimplemented step
            section=h.get("section_heading") or "", page=None, char_range=None,
            score_type="fts_adapted_experimental", score=0.0, cosine_similarity=FTS_SYNTHETIC_SIMILARITY,
            authorization_version=2, embedding_profile="fts_adapted_experimental", model_id="n/a",
            corpus_version="n/a"))
    return chunks


def run(query: str) -> HarnessResult:
    tsq, hits = exp1b_retrieve(query)
    chunks = adapt_to_chunks(hits)
    ga: EvidenceAssessment = assess(query, chunks) if chunks else EvidenceAssessment(False, "no_results", [], 0, [])
    ev = validate_citations(_chat_evidence(ga.details), ga.supported) if ga.supported else []
    result = generate(query, ev)
    return HarnessResult(
        query=query, tsquery=tsq, fts_hit_count=len(hits),
        fts_top_sources=[h["source_id"] for h in hits[:3]],
        gate_sufficient=ga.sufficient, gate_reason=ga.reason,
        supported_sources=[c.source_id for c in ga.supported],
        answer_mode=result.mode, answer_text=result.text, citation_ids=list(result.citation_ids))
