"""Sparse retrieval: PostgreSQL full-text search over the authorized research view (Phase 6.2 T2.4).

Independent of the dense retriever (no import of dense.py / research_reader.py, no vectors read).

Safety
- Connects only as the research reader role; `current_user` is asserted; read-only session; fail-closed.
- Reads only `asd_rag.v_research_retrieval_chunks` (authorization + C5 eligibility filters live in the view, so
  ORDER BY … LIMIT k runs on already-filtered rows). The SQL text is fixed; every value is a bound parameter.
- User text is NEVER parsed as tsquery syntax: it only reaches plainto_tsquery / phraseto_tsquery (which ignore
  operators). The combined query is assembled from the tsquery texts PostgreSQL returned for each term, so all
  lexemes are quoted by PostgreSQL itself; Python adds only parentheses and & / | between them.

Ranking: ts_rank_cd (cover density) over `content_tsv` (english config; heading weight B, content weight A).
It is NOT BM25 and the score is NOT a probability of relevance or medical evidence — ordering only.
Ties are broken by chunk_id so the output is deterministic.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import unicodedata
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import psycopg

from app.config import ROOT
from app.db import connect
from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.types import RetrievalError

FTS_PROFILES_FILE = ROOT / "config" / "fts_profiles.json"
ALLOWED_VIEWS = {"asd_rag.v_research_retrieval_chunks"}
ALLOWED_TS_CONFIGS = {"english"}  # must equal the config that built content_tsv (migration 001)
QUERY_MODES = {"plain_and", "glossary_and_groups", "glossary_or_groups"}
RANKERS = {"ts_rank_cd"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
VI_DIACRITIC_RE = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]")
ACRONYM_RE = re.compile(r"(?<![\w-])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*(?:/[A-Z])?)(?![\w-])")
COLUMNS = ("chunk_id", "source_id", "document_id", "title", "source_url", "section_heading", "section_path",
           "page_start", "page_end", "char_start", "char_end", "content", "content_sha256", "chunking_profile",
           "document_version", "authorization_id", "profile_code")


# ------------------------------------------------------------------------------------------------ profile
@dataclass(frozen=True)
class FtsProfile:
    code: str
    version: str
    db_role: str
    expected_db_user: str
    view: str
    view_profile_code: str
    ts_config: str
    query_mode: str
    glossary: Path | None
    ranker: str
    rank_normalization: int
    k_default: int
    k_max: int
    max_query_chars: int
    log_dir: Path

    @classmethod
    def load(cls, code: str, path: Path = FTS_PROFILES_FILE) -> FtsProfile:
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))[code]
            prof = cls(code=code, version=cfg["version"], db_role=cfg["db_role"],
                       expected_db_user=cfg["expected_db_user"], view=cfg["view"],
                       view_profile_code=cfg["view_profile_code"], ts_config=cfg["ts_config"],
                       query_mode=cfg["query_mode"], glossary=ROOT / cfg["glossary"] if cfg.get("glossary") else None,
                       ranker=cfg["ranker"], rank_normalization=int(cfg["rank_normalization"]),
                       k_default=int(cfg["k_default"]), k_max=int(cfg["k_max"]),
                       max_query_chars=int(cfg["max_query_chars"]), log_dir=ROOT / cfg["log_dir"])
        except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
            raise RetrievalError("configuration_error", f"FTS profile {code!r} not loadable") from exc
        prof.check()
        return prof

    def check(self) -> None:
        if self.view not in ALLOWED_VIEWS:
            raise RetrievalError("configuration_error", "view is not an authorized retrieval view")
        if self.ts_config not in ALLOWED_TS_CONFIGS:
            raise RetrievalError("configuration_error", "text-search config must match the content_tsv config")
        if self.query_mode not in QUERY_MODES or self.ranker not in RANKERS:
            raise RetrievalError("configuration_error", "unknown query mode or ranker")
        if self.query_mode != "plain_and" and self.glossary is None:
            raise RetrievalError("configuration_error", "glossary modes need a glossary file")
        if self.db_role != "research_reader":
            raise RetrievalError("configuration_error", "FTS retrieval must use the research reader role")


# ----------------------------------------------------------------------------------------------- glossary
def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    return unicodedata.normalize("NFC", "".join(ch for ch in text if unicodedata.category(ch) != "Mn"))


def normalize_query(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


@dataclass(frozen=True)
class ConceptMatch:
    concept: str
    trigger: str
    terms: tuple[str, ...]


@dataclass(frozen=True)
class QueryExpansion:
    original: str
    normalized: str
    diacritics: bool
    glossary_version: str | None
    glossary_sha256: str | None
    concepts: tuple[ConceptMatch, ...]
    unmapped_words: tuple[str, ...]

    @property
    def english_terms(self) -> list[str]:
        return [t for c in self.concepts for t in c.terms]


class Glossary:
    def __init__(self, path: Path) -> None:
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        self.version: str = data["version"]
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self.entries = data["entries"]
        self.age_patterns = data.get("age_patterns", [])
        self.generic = {normalize_query(g).lower() for g in data.get("generic_not_expanded", [])}
        ids = [e["id"] for e in self.entries]
        if len(ids) != len(set(ids)):
            raise RetrievalError("configuration_error", "duplicate glossary ids")
        self.by_trigger: dict[str, dict] = {}
        self.by_trigger_plain: dict[str, dict] = {}
        for e in self.entries:
            if not e["en"] or not e["vi"]:
                raise RetrievalError("configuration_error", f"empty glossary entry {e['id']}")
            for v in e["vi"]:
                key = normalize_query(v).lower()
                self.by_trigger.setdefault(key, e)
                self.by_trigger_plain.setdefault(strip_accents(key), e)

    def expand(self, question: str) -> QueryExpansion:
        text = normalize_query(question)
        low = text.lower()
        diacritics = bool(VI_DIACRITIC_RE.search(low))
        target = low if diacritics else strip_accents(low)
        table = self.by_trigger if diacritics else self.by_trigger_plain
        taken = [False] * len(target)
        found: list[tuple[int, ConceptMatch]] = []

        def claim(start: int, end: int) -> bool:
            if any(taken[start:end]):
                return False
            taken[start:end] = [True] * (end - start)
            return True

        for trig in sorted(table, key=lambda t: (-len(t), t)):  # longest trigger first, deterministic
            for m in re.finditer(r"(?<![\w-])" + re.escape(trig) + r"(?![\w-])", target):
                if claim(m.start(), m.end()):
                    e = table[trig]
                    found.append((m.start(), ConceptMatch(e["id"], trig, tuple(e["en"]))))
        for pat in self.age_patterns:
            rx = pat["vi_regex"] if diacritics else strip_accents(pat["vi_regex"])
            for m in re.finditer(rx, target):
                if claim(m.start(), m.end()):
                    n = m.group(1)
                    found.append((m.start(), ConceptMatch(f"age:{m.group(0)}", m.group(0),
                                                          tuple(t.replace("{n}", n) for t in pat["en"]))))
        for m in ACRONYM_RE.finditer(text):  # case-sensitive on the original text
            if len(re.sub(r"[-/]", "", m.group(1))) >= 2 and claim(m.start(), m.end()):
                found.append((m.start(), ConceptMatch(f"acronym:{m.group(1)}", m.group(1), (m.group(1),))))
        # merge concepts with the same id (a trigger can occur twice) — keep first position
        seen, concepts = set(), []
        for _, c in sorted(found, key=lambda x: x[0]):
            if c.concept not in seen:
                seen.add(c.concept)
                concepts.append(c)
        rest = "".join(" " if taken[i] else ch for i, ch in enumerate(target))
        unmapped = tuple(w for w in re.findall(r"[\w-]+", rest) if w not in self.generic and not w.isdigit())
        return QueryExpansion(original=question, normalized=text, diacritics=diacritics,
                              glossary_version=self.version, glossary_sha256=self.sha256,
                              concepts=tuple(concepts), unmapped_words=unmapped)


def no_expansion(question: str) -> QueryExpansion:
    text = normalize_query(question)
    return QueryExpansion(original=question, normalized=text, diacritics=bool(VI_DIACRITIC_RE.search(text.lower())),
                          glossary_version=None, glossary_sha256=None, concepts=(), unmapped_words=())


# --------------------------------------------------------------------------------------------- tsquery
def term_sql(term: str) -> tuple[str, str]:
    """('phrase'|'all', text). 'all:' = every word, any order (plainto); otherwise an exact phrase."""
    return ("all", term[4:].strip()) if term.startswith("all:") else ("phrase", term.strip())


def compose_tsquery(mode: str, vi_part: str, groups: list[list[str]]) -> str:
    """Combine PostgreSQL-produced tsquery texts. groups = per concept, the normalized texts of its terms."""
    groups = [[t for t in g if t] for g in groups]
    groups = [g for g in groups if g]
    parts = [f"( {' | '.join(f'( {t} )' for t in g)} )" for g in groups]
    if mode == "plain_and":
        return vi_part
    if mode == "glossary_and_groups":
        expr = " & ".join(parts)
    elif mode == "glossary_or_groups":
        expr = " | ".join(parts)
    else:
        raise RetrievalError("configuration_error", "unknown query mode")
    if vi_part and expr:
        return f"( {vi_part} ) | ( {expr} )"
    return vi_part or expr


# ----------------------------------------------------------------------------------------------- reader
SEARCH_SQL = (
    f"SELECT {', '.join('v.' + c for c in COLUMNS)}, "
    "ts_rank_cd(v.content_tsv, q.query, %(norm)s) AS score "
    "FROM asd_rag.v_research_retrieval_chunks v CROSS JOIN (SELECT %(tsq)s::tsquery AS query) q "
    "WHERE v.profile_code = %(profile)s AND v.content_tsv @@ q.query "
    "ORDER BY score DESC, v.chunk_id ASC LIMIT %(k)s")
TERMS_SQL = ("SELECT i, CASE WHEN kind = 'all' THEN plainto_tsquery(%(cfg)s::regconfig, t)::text "
             "ELSE phraseto_tsquery(%(cfg)s::regconfig, t)::text END "
             "FROM unnest(%(terms)s::text[], %(kinds)s::text[]) WITH ORDINALITY AS u(t, kind, i) ORDER BY i")
VI_SQL = "SELECT plainto_tsquery(%(cfg)s::regconfig, %(q)s)::text"


class FtsReader:
    def __init__(self, profile: FtsProfile, connect_fn: Callable[[], psycopg.Connection] | None = None) -> None:
        self.profile = profile
        self._connect = connect_fn or (lambda: connect(profile.db_role, f"retrieval:{profile.code}"))  # type: ignore[arg-type]

    def search(self, expansion: QueryExpansion, k: int) -> tuple[str, list[dict]]:
        p = self.profile
        try:
            conn = self._connect()
        except psycopg.OperationalError:
            raise RetrievalError("database_unavailable", "cannot connect as the research reader") from None
        try:
            with conn:
                conn.read_only = True
                if conn.execute("SELECT current_user").fetchone()[0] != p.expected_db_user:
                    raise RetrievalError("wrong_role", "connection is not the research reader role")
                vi = conn.execute(VI_SQL, {"cfg": p.ts_config, "q": expansion.normalized}).fetchone()[0]
                groups: list[list[str]] = []
                if p.query_mode != "plain_and" and expansion.concepts:
                    flat = [(gi, *term_sql(t)) for gi, c in enumerate(expansion.concepts) for t in c.terms]
                    rows = conn.execute(TERMS_SQL, {"cfg": p.ts_config, "terms": [f[2] for f in flat],
                                                    "kinds": [f[1] for f in flat]}).fetchall()
                    groups = [[] for _ in expansion.concepts]
                    for (gi, _kind, _t), (_i, text) in zip(flat, rows, strict=True):
                        groups[gi].append(text)
                tsq = compose_tsquery(p.query_mode, vi, groups)
                if not tsq:
                    return "", []
                cur = conn.execute(SEARCH_SQL, {"tsq": tsq, "norm": p.rank_normalization,
                                                "profile": p.view_profile_code, "k": k})
                names = [d.name for d in cur.description]
                return tsq, [dict(zip(names, row, strict=True)) for row in cur.fetchall()]
        except RetrievalError:
            raise
        except psycopg.errors.InsufficientPrivilege:
            raise RetrievalError("permission_denied", "research reader lacks access to the retrieval view") from None
        except psycopg.errors.UndefinedTable:
            raise RetrievalError("view_missing", "retrieval view does not exist") from None
        except psycopg.errors.QueryCanceled:
            raise RetrievalError("query_timeout", "FTS query exceeded the statement timeout") from None
        except psycopg.OperationalError:
            raise RetrievalError("database_unavailable", "database connection failed during retrieval") from None
        except psycopg.Error as exc:
            raise RetrievalError("database_error", type(exc).__name__) from None


# -------------------------------------------------------------------------------------------- retriever
@dataclass(frozen=True)
class FtsHit:
    rank: int
    chunk_id: str
    source_id: str
    document_id: str
    title: str
    source_url: str
    section: str
    page: str | None
    char_range: str | None
    content: str
    content_sha256: str
    score_type: str
    score: float
    authorization_version: int
    corpus_version: str


@dataclass
class FtsResponse:
    request_id: str
    question_id: str | None
    retriever: str
    profile_version: str
    status: str
    k_requested: int
    query_sha256: str
    normalized_query: str
    expansion: dict
    ts_config: str
    tsquery: str
    ranker: str
    authorization_version: int | None
    results: list[FtsHit] = field(default_factory=list)
    latency_ms: dict[str, float] = field(default_factory=dict)
    timestamp: str = ""


def check_rows(rows: list[dict], k: int, profile: FtsProfile) -> list[FtsHit]:
    """Fail closed on any provenance problem, duplicate, ordering error or > k rows."""
    if len(rows) > k:
        raise RetrievalError("provenance_invalid", "database returned more rows than k")
    seen: set[str] = set()
    hits, auth = [], set()
    prev: tuple[float, str] | None = None
    for rank, row in enumerate(rows, 1):
        problems = [f"missing {key}" for key in ("chunk_id", "source_id", "document_id", "content",
                                                  "content_sha256", "chunking_profile", "document_version",
                                                  "authorization_id") if row.get(key) in (None, "")]
        if row.get("page_start") is None and (row.get("char_start") is None or row.get("char_end") is None):
            problems.append("no page and no character range")
        content = row.get("content")
        if not SHA_RE.match(str(row.get("content_sha256", ""))) or (
                content and hashlib.sha256(content.encode("utf-8")).hexdigest() != row.get("content_sha256")):
            problems.append("content hash mismatch")
        if row.get("profile_code") != profile.view_profile_code:
            problems.append("view profile mismatch")
        score = row.get("score")
        if not isinstance(score, int | float) or score < 0 or score != score:
            problems.append("invalid rank score")
        cid = row.get("chunk_id")
        if cid in seen:
            problems.append("duplicate chunk")
        if problems:
            raise RetrievalError("provenance_invalid", f"rank {rank}: " + "; ".join(problems))
        key = (-float(score), cid)
        if prev is not None and key < prev:
            raise RetrievalError("provenance_invalid", f"rank {rank}: results not ordered by score, chunk_id")
        prev = key
        seen.add(cid)
        auth.add(int(row["authorization_id"]))
        section = row.get("section_heading") or " > ".join(row.get("section_path") or [])
        page = None
        if row.get("page_start") is not None:
            page = str(row["page_start"]) if row.get("page_end") in (None, row["page_start"]) else \
                f"{row['page_start']}-{row['page_end']}"
        hits.append(FtsHit(rank=rank, chunk_id=cid, source_id=row["source_id"], document_id=row["document_id"],
                           title=row.get("title") or "", source_url=row.get("source_url") or "", section=section,
                           page=page, char_range=None if row.get("char_start") is None else
                           f"{row['char_start']}-{row['char_end']}", content=content,
                           content_sha256=row["content_sha256"], score_type=profile.ranker, score=float(score),
                           authorization_version=int(row["authorization_id"]),
                           corpus_version=f"{row['chunking_profile']}@{row['document_version']}"))
    if len(auth) > 1:
        raise RetrievalError("provenance_invalid", "results come from more than one authorization")
    return hits


class FtsRetriever:
    def __init__(self, profile: FtsProfile, reader: FtsReader | None = None, glossary: Glossary | None = None,
                 log: JsonlRetrievalLog | None = None, clock: Callable[[], float] = time.perf_counter) -> None:
        self.profile = profile
        self.reader = reader or FtsReader(profile)
        self.glossary = glossary if glossary is not None else (Glossary(profile.glossary) if profile.glossary else None)
        self.log = log
        self._clock = clock

    def validate(self, query: object, k: object) -> tuple[str, int]:
        if not isinstance(query, str) or not query.strip():
            raise RetrievalError("invalid_query", "query must be a non-empty string")
        if len(query) > self.profile.max_query_chars:
            raise RetrievalError("invalid_query", "query is too long")
        if k is None:
            k = self.profile.k_default
        if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= self.profile.k_max:
            raise RetrievalError("invalid_k", f"k must be an integer in [1, {self.profile.k_max}]")
        return query, k

    def expand(self, query: str) -> QueryExpansion:
        if self.profile.query_mode == "plain_and" or self.glossary is None:
            return no_expansion(query)
        return self.glossary.expand(query)

    def retrieve(self, query: str, k: int | None = None, question_id: str | None = None) -> FtsResponse:
        request_id, start = str(uuid.uuid4()), self._clock()
        qhash = hashlib.sha256(query.encode("utf-8")).hexdigest() if isinstance(query, str) else None
        try:
            query, k = self.validate(query, k)
            exp = self.expand(query)
            t0 = self._clock()
            tsq, rows = self.reader.search(exp, k)
            db_ms = (self._clock() - t0) * 1000
            hits = check_rows(rows, k, self.profile)
        except RetrievalError as exc:
            if self.log:
                self.log.write({"event": "retrieval", "status": "error", "error_category": exc.category,
                                "request_id": request_id, "question_id": question_id, "retriever": self.profile.code,
                                "query_sha256": qhash, "k": k, "returned": [],
                                "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds")})
            raise
        exp_d = {"glossary_version": exp.glossary_version, "glossary_sha256": exp.glossary_sha256,
                 "diacritics": exp.diacritics, "concepts": [asdict(c) for c in exp.concepts],
                 "unmapped_words": list(exp.unmapped_words)}
        auth = {h.authorization_version for h in hits}
        resp = FtsResponse(request_id=request_id, question_id=question_id, retriever=self.profile.code,
                           profile_version=self.profile.version, status="ok" if hits else "no_results",
                           k_requested=k, query_sha256=qhash or "", normalized_query=exp.normalized, expansion=exp_d,
                           ts_config=self.profile.ts_config, tsquery=tsq, ranker=self.profile.ranker,
                           authorization_version=next(iter(auth)) if auth else None, results=hits,
                           latency_ms={"db": round(db_ms, 2), "total": round((self._clock() - start) * 1000, 2)},
                           timestamp=datetime.now(UTC).isoformat(timespec="milliseconds"))
        if self.log:  # raw question text is not logged (hash only, as for dense); expansion = glossary terms
            self.log.write({"event": "retrieval", "status": resp.status, "request_id": request_id,
                            "question_id": question_id, "retriever": resp.retriever,
                            "profile_version": resp.profile_version, "query_sha256": resp.query_sha256,
                            "expansion": exp_d, "ts_config": resp.ts_config, "tsquery": resp.tsquery,
                            "ranker": resp.ranker, "authorization_version": resp.authorization_version, "k": k,
                            "returned": [{"rank": h.rank, "chunk_id": h.chunk_id, "score": round(h.score, 6)}
                                         for h in hits], "latency_ms": resp.latency_ms, "timestamp": resp.timestamp})
        return resp
