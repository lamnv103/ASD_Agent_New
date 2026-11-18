# ruff: noqa: E501
"""FTS retriever (T2.4): glossary expansion, tsquery construction, SQL safety, provenance and blind-pool rules."""

import hashlib
import json
import re

import pytest

from app.config import ROOT
from app.retrieval import fts as F
from app.retrieval.types import RetrievalError

GLOSSARY = F.Glossary(ROOT / "config" / "query_glossary_vi_en_v1.json")
PROF_A = F.FtsProfile.load("fts_a_baseline_v1")
PROF_B = F.FtsProfile.load("fts_b_glossary_and_v1")
PROF_C = F.FtsProfile.load("fts_c_glossary_or_v1")
QUESTIONS = [json.loads(x)["question_vi"] for x in
             (ROOT / "eval" / "datasets" / "retrieval_eval_v1.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]


def concepts(q):
    return [c.concept for c in GLOSSARY.expand(q).concepts]


# ------------------------------------------------------------------ glossary / Vietnamese handling
def test_vietnamese_with_and_without_diacritics_expand_identically():
    assert concepts("Trẻ tự kỷ có hay bị động kinh không?") == concepts("Tre tu ky co hay bi dong kinh khong?") \
        == ["autism", "epilepsy"]


def test_accent_stripped_matching_only_when_query_has_no_diacritics():
    assert GLOSSARY.expand("dong kinh").diacritics is False
    assert GLOSSARY.expand("động kinh").diacritics is True
    assert concepts("đồng kính") == []  # different words once diacritics are present: no accidental match


def test_british_and_american_spellings_are_both_expanded():
    terms = [t for c in GLOSSARY.expand("Cha mẹ làm gì khi trẻ có hành vi thách thức ở nhà?").concepts for t in c.terms]
    assert "challenging behaviour" in terms and "challenging behavior" in terms


@pytest.mark.parametrize("q,expected", [("Tiêu chuẩn DSM-5 cho tự kỷ", "dsm5"), ("Trẻ ASD là gì", "asd_full"),
                                        ("AAC có tốt không", "aac"), ("Trẻ kèm ADHD", "adhd"),
                                        ("ADOS-2 là gì?", "ados"), ("M-CHAT-R/F là gì", "mchat")])
def test_acronyms_map_to_their_entries(q, expected):
    assert expected in concepts(q)


def test_unknown_acronym_is_passed_through_unchanged():
    exp = GLOSSARY.expand("PECS là gì?")
    assert [c.terms for c in exp.concepts] == [("PECS",)]


def test_longest_trigger_wins_and_consumes_words():
    c = concepts("Can thiệp do cha mẹ thực hiện có hiệu quả không?")
    assert c == ["parent_mediated", "effectiveness"]  # not also 'intervention' or 'parents'


def test_expansion_never_adds_a_concept_absent_from_the_question():
    for q in QUESTIONS:
        exp = GLOSSARY.expand(q)
        text = exp.normalized.lower() if exp.diacritics else F.strip_accents(exp.normalized.lower())
        for c in exp.concepts:
            assert c.trigger.lower() in text or c.trigger in exp.normalized, (q, c)


def test_expansion_is_deterministic_and_keeps_the_original():
    q = QUESTIONS[52]
    a, b = GLOSSARY.expand(q), GLOSSARY.expand(q)
    assert a == b and a.original == q


def test_out_of_scope_question_gets_no_expansion():
    assert concepts("Hôm nay thời tiết thế nào?") == []


def test_glossary_has_version_hash_and_unique_ids():
    assert GLOSSARY.version == "query_glossary_vi_en_v1"
    assert GLOSSARY.sha256 == hashlib.sha256((ROOT / "config" / "query_glossary_vi_en_v1.json").read_bytes()).hexdigest()


# ------------------------------------------------------------------ tsquery construction (AND / OR)
def test_and_mode_requires_every_concept_or_mode_any():
    groups = [["'autism'", "'asd'"], ["'epilepsi'"]]
    b = F.compose_tsquery("glossary_and_groups", "'trẻ' & 'kỷ'", groups)
    c = F.compose_tsquery("glossary_or_groups", "'trẻ' & 'kỷ'", groups)
    assert b == "( 'trẻ' & 'kỷ' ) | ( ( ( 'autism' ) | ( 'asd' ) ) & ( ( 'epilepsi' ) ) )"
    assert c == "( 'trẻ' & 'kỷ' ) | ( ( ( 'autism' ) | ( 'asd' ) ) | ( ( 'epilepsi' ) ) )"


def test_plain_mode_uses_only_the_vietnamese_query_and_empty_groups_are_dropped():
    assert F.compose_tsquery("plain_and", "'a' & 'b'", [["'x'"]]) == "'a' & 'b'"
    assert F.compose_tsquery("glossary_and_groups", "", [[""], ["'x'"]]) == "( ( 'x' ) )"
    assert F.compose_tsquery("glossary_or_groups", "", []) == ""


def test_term_kinds():
    assert F.term_sql("all:respond name") == ("all", "respond name")
    assert F.term_sql("joint attention") == ("phrase", "joint attention")


# ------------------------------------------------------------------ SQL safety with a fake connection
class FakeCursor:
    def __init__(self, rows, names=()):
        self._rows, self.description = rows, [type("D", (), {"name": n}) for n in names]

    def fetchone(self):
        return self._rows[0]

    def fetchall(self):
        return self._rows


class FakeConn:
    def __init__(self, user="asd_rag_v2_research_reader", rows=()):
        self.user, self.rows, self.calls, self.read_only = user, list(rows), [], False

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, sql, params=None):
        self.calls.append((sql, params))
        if sql.startswith("SELECT current_user"):
            return FakeCursor([(self.user,)])
        if sql == F.VI_SQL:
            return FakeCursor([("'x'",)])
        if sql == F.TERMS_SQL:
            return FakeCursor([(i + 1, f"'t{i}'") for i in range(len(params["terms"]))])
        names = [*F.COLUMNS, "score"]
        return FakeCursor([tuple(r.get(n) for n in names) for r in self.rows], names)


EVIL = "x'); DROP TABLE asd_rag.chunks; -- & !a | b:* <-> \\"


def test_user_text_only_travels_as_bound_parameters():
    conn = FakeConn()
    reader = F.FtsReader(PROF_B, connect_fn=lambda: conn)
    reader.search(GLOSSARY.expand(EVIL), 5)
    for sql, _params in conn.calls:
        assert EVIL not in sql and "DROP" not in sql
    assert conn.calls[1][0] == F.VI_SQL and conn.calls[1][1]["q"] == F.normalize_query(EVIL)
    assert conn.read_only is True
    assert "asd_rag.v_research_retrieval_chunks" in F.SEARCH_SQL and "chunks c" not in F.SEARCH_SQL
    assert not re.search(r"(?<![a-z_])to_tsquery\(", F.SEARCH_SQL + F.TERMS_SQL + F.VI_SQL)  # never parse raw text as tsquery


def test_wrong_role_fails_closed():
    reader = F.FtsReader(PROF_A, connect_fn=lambda: FakeConn(user="asd_rag_v2_owner"))
    with pytest.raises(RetrievalError) as e:
        reader.search(F.no_expansion("autism"), 5)
    assert e.value.category == "wrong_role"


def test_profiles_are_reader_only_and_english_config():
    for p in (PROF_A, PROF_B, PROF_C):
        assert p.db_role == "research_reader" and p.view == "asd_rag.v_research_retrieval_chunks"
        assert p.ts_config == "english" and p.ranker == "ts_rank_cd"


def test_owner_profile_is_rejected(tmp_path):
    cfg = json.loads((ROOT / "config" / "fts_profiles.json").read_text(encoding="utf-8"))
    cfg["fts_a_baseline_v1"]["db_role"] = "owner"
    p = tmp_path / "p.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")
    with pytest.raises(RetrievalError):
        F.FtsProfile.load("fts_a_baseline_v1", p)


# ------------------------------------------------------------------ validation / provenance / top-k
def row(cid="D#c#0001", score=1.0, **kw):
    content = kw.pop("content", "text " + cid)
    base = {"chunk_id": cid, "source_id": "S", "document_id": "D", "title": "t", "source_url": "u",
            "section_heading": "h", "section_path": None, "page_start": 1, "page_end": 1, "char_start": None,
            "char_end": None, "content": content, "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "chunking_profile": "section_v2_1", "document_version": "v", "authorization_id": 2,
            "profile_code": PROF_A.view_profile_code, "score": score}
    base.update(kw)
    return base


@pytest.mark.parametrize("q", ["", "   ", None, 12, "x" * 1001])
def test_invalid_query_rejected(q):
    with pytest.raises(RetrievalError) as e:
        F.FtsRetriever(PROF_A, reader=object(), glossary=None).validate(q, 5)
    assert e.value.category == "invalid_query"


@pytest.mark.parametrize("k", [0, -1, 51, 2.5, True, "5"])
def test_invalid_k_rejected(k):
    with pytest.raises(RetrievalError) as e:
        F.FtsRetriever(PROF_A, reader=object(), glossary=None).validate("autism", k)
    assert e.value.category == "invalid_k"


def test_check_rows_accepts_good_ordered_rows():
    hits = F.check_rows([row("D#c#0002", 2.0), row("D#c#0001", 1.0), row("D#c#0003", 1.0)], 5, PROF_A)
    assert [h.rank for h in hits] == [1, 2, 3] and hits[0].score_type == "ts_rank_cd"


@pytest.mark.parametrize("rows,reason", [
    ([row("D#c#0001"), row("D#c#0001")], "duplicate"),
    ([row(content_sha256="0" * 64)], "hash"),
    ([row(content_sha256="nothex")], "hash"),
    ([row(profile_code="other")], "profile"),
    ([row(authorization_id=None)], "missing authorization_id"),
    ([row(page_start=None)], "no page"),
    ([row("D#c#0001", 1.0), row("D#c#0002", 2.0)], "ordered"),
    ([row("D#c#0002", 1.0), row("D#c#0001", 1.0)], "ordered"),       # ties must be by chunk_id
    ([row(score=-1.0)], "score"),
    ([row("D#c#0001"), row("D#c#0002", authorization_id=1)], "more than one authorization"),
])
def test_check_rows_rejects_invalid_provenance(rows, reason):
    with pytest.raises(RetrievalError) as e:
        F.check_rows(rows, 5, PROF_A)
    assert e.value.category == "provenance_invalid" and reason in str(e.value)


def test_more_rows_than_k_rejected():
    with pytest.raises(RetrievalError):
        F.check_rows([row(f"D#c#000{i}", 1.0) for i in range(1, 4)], 2, PROF_A)


def test_retrieve_end_to_end_with_fake_reader_is_deterministic():
    rows = [row("D#c#0002", 2.0), row("D#c#0001", 1.0)]
    r = F.FtsRetriever(PROF_B, reader=F.FtsReader(PROF_B, connect_fn=lambda: FakeConn(rows=rows)), glossary=GLOSSARY)
    a, b = r.retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=5), r.retrieve("Trẻ tự kỷ có hay bị động kinh không?", k=5)
    assert [h.chunk_id for h in a.results] == [h.chunk_id for h in b.results] == ["D#c#0002", "D#c#0001"]
    assert a.tsquery == b.tsquery and a.expansion == b.expansion and a.ranker == "ts_rank_cd"


# ------------------------------------------------------------------ pool artifacts (skipped if not generated)
POOL = ROOT / "eval" / "reports" / "fts_candidate_pool_2026-11-15.jsonl"
KEY = ROOT / "eval" / "reports" / "fts_candidate_pool_key_2026-11-15.jsonl"
RECORD = ROOT / "eval" / "reports" / "fts_run_record_2026-11-15.json"
BLIND_FIELDS = {"item_id", "question_id", "question_vi", "expected_answer_scope", "chunk_id", "source_id", "document_id",
                "title", "section", "page", "char_range", "content", "content_sha256", "grade", "rationale_vi",
                "annotator_id", "annotated_at"}


@pytest.mark.skipif(not POOL.exists(), reason="pool not generated")
def test_blind_export_hides_system_rank_score_and_prior_labels():
    items = [json.loads(x) for x in POOL.read_text(encoding="utf-8").splitlines()]
    for it in items:
        assert set(it) == BLIND_FIELDS
        assert it["grade"] is None and it["rationale_vi"] is None and it["annotator_id"] is None
    by_q = {}
    for it in items:
        by_q.setdefault(it["question_id"], []).append(it["item_id"])
    assert all(v == sorted(v) for v in by_q.values())  # display order = item_id order, independent of rank/system


@pytest.mark.skipif(not (KEY.exists() and RECORD.exists()), reason="pool not generated")
def test_pool_is_the_deduplicated_union_of_every_system_top20():
    key = [json.loads(x) for x in KEY.read_text(encoding="utf-8").splitlines()]
    ranked = json.loads(RECORD.read_text(encoding="utf-8"))["ranked"]
    pairs = [(k["question_id"], k["chunk_id"]) for k in key]
    assert len(pairs) == len(set(pairs))
    for q in ranked["dense"]:
        union = set().union(*({x["chunk_id"] for x in ranked[s][q][:20]} for s in ranked))
        assert {c for qq, c in pairs if qq == q} == union
    for k in key:
        for s in ("dense", "fts_a", "fts_b", "fts_c"):
            assert k[f"in_{s}"] == (s in k["ranks"])
