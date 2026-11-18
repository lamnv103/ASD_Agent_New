# T5.5 — Retrieval Coverage & Generalization Analysis — Final Report

## Scope re-stated

Root-cause analysis of why the demo failed to answer most of T5.4's 31 new, independent cache-miss
questions — focused on retrieval, the Evidence Gate, and generalization, explicitly *not* on mechanically
adding more answer templates. Strictly read-only: **zero code changes were made in this task** (one new,
read-only diagnostic script, `scripts/t5_5_fts_diagnostics.py`, was added — it calls only existing,
unmodified `app/retrieval/fts.py` and `app/nlp/text_match.py` code via the read-only `research_reader`
role; no file under `app/` was edited).

## Direct answers to the task's 8 required questions

1. **"Trong 31 cache miss, bao nhiêu trường hợp thực sự thiếu kiến thức?"** — **7** (`ie017`, `ie018`,
   `ie021`, `ie022`, `ie024`, `ie026`, `ie029`), confirmed by direct corpus keyword search beyond FTS's
   own query construction, not inferred from FTS alone.
2. **"Bao nhiêu trường hợp có kiến thức nhưng retrieval không tìm thấy?"** — **11** (`ie004`, `ie007`,
   `ie008`, `ie009`, `ie015`, `ie019`, `ie020`, `ie025`, `ie027`, `ie028`, `ie032`) have demonstrable,
   specific corpus content — several landing on the exact same source a live template already uses for an
   adjacent, already-answered question — that the live pipeline never got the chance to retrieve, because
   the cache-only gate stops it before dense retrieval is even attempted. A further 9 have adjacent-but-
   not-precisely-matching content (category 2).
3. **"Bao nhiêu trường hợp bị Evidence Gate từ chối?"** — **0**, and this is architectural, not a
   measurement gap: the Evidence Gate requires a `cosine_similarity` field that only dense retrieval
   populates, and dense retrieval never runs for a cache-miss query. The Gate and the cache-coverage
   problem are two completely independent failure surfaces.
4. **"Bao nhiêu trường hợp chưa thể kết luận do giới hạn cache-only?"** — **4** outright-indeterminate
   even with FTS diagnostics (`ie002`, `ie010`, `ie011`, `ie012`); in the strict mechanical sense all 31
   share the same cache-only cause, but FTS resolved 27 of them to a more specific sub-finding.
5. **"Dense Retrieval và FTS đang có ưu/nhược điểm gì?"** — Dense: strong recall on cached, well-formed
   text (re-confirmed via T2.3's unchanged 66/66 regression this task), but categorically unusable on any
   uncached text, with no semantic fallback. FTS: usable on any text with zero embedding cost, but raw
   Vietnamese is 0% usable against the English-only `tsvector` config (0/31 FTS-A hits, reproducing T2.4's
   0/66 finding exactly), and the two glossary-expansion modes trade AND-loss (0 results on
   multi-concept questions) against OR-dilution (swamped by generic high-frequency terms).
6. **"Nên ưu tiên cải thiện thành phần nào?"** — The cache-coverage gap (exact-text query keying) is the
   single dominant cause of unanswered questions, by a wide margin over corpus content or Gate behavior:
   11/31 independent-set cache misses have confirmed matchable content sitting unused behind the cache
   gate, and the 105-set's dominant failure mode (T5.4) was the same 50/105 cache misses, not wrong
   answers. If one component must be prioritized, it is **query-time coverage** (either via A1's FTS
   fallback as an immediate, cache-only-compliant partial mitigation, or via C1's live-embedding
   re-authorization as the structural fix) — not further template expansion, consistent with this task's
   explicit instruction not to just add more templates.
7. **"Những cải thiện nào không cần xin quyền mới?"** — The 4 Level-A proposals in
   `t5_5_improvement_proposal.md`: wiring FTS as a labeled fallback (A1), reconciling/expanding the two
   glossaries with the specific gaps this task found (A2), a minimum-concept-match FTS query mode to fix
   AND-loss/OR-dilution (A3), and completing human annotation of the already-built, already-frozen FTS
   candidate pool (A4) — the last of these needs only human annotator time, no technical authorization.
8. **"Những cải thiện nào phải chờ phê duyệt?"** — Level B: a DB migration for `unaccent`/reweighted FTS
   ranking (B1) and sourcing new corpus content for the confirmed-thin/absent topics (B2, speech/language
   specifically, adult-life outcomes, adolescent sex education, ASD-vs-hearing-impairment, the
   vitamin-B6-cure myth). Level C: re-authorizing live query embedding (C1, revisits T2.6 — not
   recommended for or against here, only identified as the change that would most directly address
   finding #6) and, conditionally, embedding any new corpus content from B2 (C2).

## What this task did and did not establish

**Established, with concrete evidence**: the dominant cause of unanswered independent-set questions is
cache-text-exact-match coverage, not missing corpus knowledge or Evidence Gate over-rejection; FTS-A is
unusable on raw Vietnamese against this corpus (0/31, reproducing a known, now twice-confirmed finding);
FTS-B/C have real but noisy signal, with two specific, named, reproducible failure modes (AND-loss,
OR-dilution via generic high-frequency terms); the term-matching heuristic shared by the Evidence Gate and
this task's diagnostics has a confirmed false-positive mode on generic vocabulary (Case F, `ie002`); the
two glossaries used across the codebase are unreconciled and incomplete in specific, now-documented ways;
one topic (speech/language delay) has a genuinely thin corpus footprint (1 chunk for "speech delay"
literally) independent of any retrieval-method question.

**Not established, and explicitly not claimed**: no official Recall@K, precision, or nDCG number for
either the 66-question or the 31-question set, beyond what T2.4 already reported as exploratory (unchanged
this task) — because no human-adjudicated relevance label exists for either pool. No claim about what
dense retrieval specifically would return on any of the 31 questions — dense cannot be run on uncached
text without live embedding, which was never attempted. No recommendation for or against T2.6's
authorization decision itself — this task identifies the *effect* of the constraint, not a vote on
lifting it.

## Protected boundaries — compliance re-confirmed

- `ASD_DEMO_MODE=true`, all three `ENABLE_LIVE_*` flags `False`, fail-loud gates unchanged (re-read
  `app/config.py` this task; unmodified).
- No Cohere or other external service call was made at any point — every retrieval action this task
  performed was either `research_reader`-role read-only SQL (dense's own cache-only path was never
  invoked at all; FTS needs no embedding) or local Python term-matching. Confirmed by the fact that no API
  client code (`app/retrieval/embeddings.py`'s `CohereEmbedder`) was imported by this task's diagnostic
  script.
- No write to the database, no change to the 2,291 retrievable chunks or their vectors, no change to the
  embedding model/dimension, no corpus/annotation/frozen-benchmark edit, no sealed/reveal file access, no
  Docker start/stop (the DB container was already running throughout, confirmed via a successful
  `research_reader` connection at the start of this task), no DB schema/role/permission change, no Git
  commit/push.
- **No code was modified in `app/` at all.** One new, purely additive, read-only analysis script was
  added under `scripts/` (same precedent as every prior T5.x task's evaluation scripts) — it imports but
  does not alter `app/retrieval/fts.py` or `app/nlp/text_match.py`.
- Full unit-test suite (404 tests) re-run after adding the new script: unchanged pass count, confirming no
  accidental interference with existing code.

## Final status

```
T5_5_PARTIAL
```

**Rationale**: all 5 phases were completed and all 8 required deliverable files were produced, with
concrete, re-checkable evidence (FTS diagnostic output, direct corpus keyword searches, cross-references
to existing live templates) behind every classification — not invented numbers. The task cannot be marked
`T5_5_COMPLETE` because genuine open questions remain that this task's tooling cannot resolve: whether
dense retrieval itself would find the 11 category-3 cases' content (untestable without live embedding),
whether the 4 category-5 cases are true knowledge gaps or retrieval-method artifacts (genuinely
indeterminate with current tools), and because none of the proposed improvements — even the Level-A ones
— were implemented (by this task's own explicit instruction, "Không sửa code trong T5.5"). This is **not**
`DEMO_READY_FOR_USER_VALIDATION`, which this report does not claim.
