"""Research/test embedding track (migration 006) — separate from production approval.

  authorize  owner role: records the project owner's research authorization for the preflight manifest
             (sources + exact chunk allowlist). Never touches source_rights.*_allowed or approvals.
  run        ingest role: DRY RUN by default. With --execute, embeds the pending candidates of the active
             authorization with Cohere (search_document), batch ≤ 96, paced, one transaction per batch.
  verify     read-only checks of stored research vectors; writes embedding_quality_check.md and
             embedding_run_report.md. --query-check also embeds a few test QUERIES (search_query) and runs
             an exact cosine search (no document text is sent by verify).

Usage:
  python -B scripts/embedding_preflight.py
  python -B scripts/embed_research.py authorize --authorized-by "..." --basis "..."
  python -B scripts/embed_research.py run                 # dry run
  python -B scripts/embed_research.py run --execute
  python -B scripts/embed_research.py verify [--query-check]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from psycopg.types.json import Jsonb

from app.config import REPORTS, ROOT
from app.db import connect
from app.ingest import embed_pipeline
from app.retrieval.embeddings import CohereEmbedder, EmbeddingError, EmbeddingProfile

MANIFEST = REPORTS / "embedding_manifest.csv"
RUN_MANIFEST = REPORTS / "embedding_run_manifest.csv"
FAILED_BATCHES = REPORTS / "embedding_failed_batches.csv"
LOGS = ROOT / "logs"
INPUTS_PER_MINUTE = 1800  # below the trial limit of 2,000 embed inputs per minute
# Run db86b899 (2026-11-14) showed a per-minute token ceiling on the trial key: ~80–150k tokens went through
# at each minute boundary, the rest got HTTP errors until the next minute. Pace on a rolling 60 s window.
TOKENS_PER_MINUTE = 90_000
STOP_CODES = {"missing_key", "provider_auth"}
RECORDED_BY = "Claude Code via scripts/embed_research.py (asd_rag_v2_owner)"
CANDIDATES = """
SELECT v.chunk_id, v.source_id, v.document_id, v.title, v.section_heading, v.content, v.content_sha256,
       v.group_membership
FROM v_research_embedding_candidates v WHERE v.authorization_id = %s ORDER BY v.chunk_id
"""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_manifest() -> list[dict]:
    with open(MANIFEST, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def active_authorization(conn, profile: EmbeddingProfile) -> tuple[int, str] | None:
    return conn.execute("""SELECT authorization_id, manifest_sha256 FROM research_embedding_authorizations
                           WHERE revoked_at IS NULL AND profile_code = %s ORDER BY authorization_id DESC LIMIT 1""",
                        (profile.profile_code,)).fetchone()


# ---------------------------------------------------------------------------------------- authorize
def authorize(profile: EmbeddingProfile, authorized_by: str, basis: str, notes: str | None) -> dict:
    rows = read_manifest()
    digest = sha256_file(MANIFEST)
    with connect("owner", "embed_research_authorize") as conn:
        conn.execute("""INSERT INTO embedding_profiles (profile_code, provider, model_id, model_revision,
                            vector_dimension, document_input_type, query_input_type, similarity_metric, api_version,
                            configuration)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (profile_code) DO NOTHING""",
                     (profile.profile_code, profile.provider, profile.model_id, profile.model_revision,
                      profile.vector_dimension, profile.document_input_type, profile.query_input_type,
                      profile.similarity_metric, profile.api_version, Jsonb(profile.__dict__)))
        existing = conn.execute("""SELECT authorization_id FROM research_embedding_authorizations
                                   WHERE revoked_at IS NULL AND profile_code = %s AND manifest_sha256 = %s""",
                                (profile.profile_code, digest)).fetchone()
        if existing:
            return {"authorization_id": existing[0], "created": False, "manifest_sha256": digest}
        # every allowlisted chunk must still exist with the same content
        db = dict(conn.execute("SELECT chunk_id, content_sha256 FROM chunks WHERE chunk_id = ANY(%s)",
                               ([r["chunk_id"] for r in rows],)).fetchall())
        stale = [r["chunk_id"] for r in rows if db.get(r["chunk_id"]) != r["content_hash"]]
        if stale:
            raise SystemExit(f"{len(stale)} manifest chunks changed or vanished since preflight; re-run preflight")
        aid = conn.execute("""INSERT INTO research_embedding_authorizations (scope, authorized_by, recorded_by, basis,
                                  profile_code, chunking_profile, manifest_sha256, notes)
                              VALUES ('research_test', %s, %s, %s, %s, %s, %s, %s) RETURNING authorization_id""",
                           (authorized_by, RECORDED_BY, basis, profile.profile_code, profile.chunking_profile, digest,
                            notes)).fetchone()[0]
        sources = {r["source_id"]: r["group_membership"].split(";") for r in rows}
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO research_embedding_authorization_sources VALUES (%s, %s, %s)",
                            [(aid, s, g) for s, g in sorted(sources.items())])
            cur.executemany("INSERT INTO research_embedding_authorization_chunks VALUES (%s, %s, %s, %s)",
                            [(aid, r["source_id"], r["chunk_id"], r["content_hash"]) for r in rows])
        conn.commit()
    return {"authorization_id": aid, "created": True, "manifest_sha256": digest, "sources": len(sources),
            "chunks": len(rows)}


# ---------------------------------------------------------------------------------------------- run
def preflight_run(conn, profile: EmbeddingProfile, rows: list[dict]) -> tuple[int, int, list[dict], dict]:
    problems = []
    if not os.environ.get("COHERE_API_KEY"):
        problems.append("COHERE_API_KEY missing")
    if (profile.model_id, profile.vector_dimension, profile.document_input_type) != (
            "embed-v4.0", 1536, "search_document"):
        problems.append("embedding profile differs from the verified configuration")
    column = conn.execute("""SELECT format_type(atttypid, atttypmod) FROM pg_attribute
                             WHERE attrelid = 'asd_rag.research_chunk_embeddings'::regclass
                               AND attname = 'embedding'""").fetchone()[0]
    if column != f"vector({profile.vector_dimension})":
        problems.append(f"research vector column is {column}")
    prof = conn.execute("SELECT profile_id, model_id, vector_dimension FROM embedding_profiles WHERE profile_code = %s",
                        (profile.profile_code,)).fetchone()
    auth = active_authorization(conn, profile)
    if not prof or not auth:
        raise SystemExit("No embedding profile / active research authorization: run `authorize` first.")
    if auth[1] != sha256_file(MANIFEST):
        problems.append("embedding_manifest.csv changed after authorization (re-run preflight + authorize)")
    candidates = []
    for chunk_id, sid, did, title, heading, content, chash, groups in conn.execute(CANDIDATES, (auth[0],)):
        text = embed_pipeline.build_input(profile, title, heading, content)
        candidates.append({"chunk_id": chunk_id, "source_id": sid, "document_id": did, "content_hash": chash,
                           "group_membership": ";".join(groups), "text": text,
                           "input_sha256": embed_pipeline.input_hash(profile, text)})
    by_manifest = {r["chunk_id"]: r for r in rows}
    if {c["chunk_id"] for c in candidates} != set(by_manifest):
        problems.append("database candidates differ from the preflight manifest")
    drift = [c["chunk_id"] for c in candidates
             if c["chunk_id"] in by_manifest and c["input_sha256"] != by_manifest[c["chunk_id"]]["input_sha256"]]
    if drift:
        problems.append(f"{len(drift)} inputs differ from preflight (title/heading/content drift)")
    if problems:
        raise SystemExit("Preflight failed, nothing sent: " + "; ".join(problems))
    stored = {cid: h for cid, h in conn.execute(
        "SELECT chunk_id, embedding_input_hash FROM research_chunk_embeddings WHERE profile_id = %s", (prof[0],))}
    stale = [c["chunk_id"] for c in candidates
             if c["chunk_id"] in stored and stored[c["chunk_id"]] != c["input_sha256"]]
    if stale:
        raise SystemExit(f"{len(stale)} stored research vectors have a different input hash; refusing to overwrite")
    todo = [c for c in candidates if c["chunk_id"] not in stored]
    return prof[0], auth[0], todo, {"candidates": len(candidates), "already_stored": len(candidates) - len(todo)}


def run(profile: EmbeddingProfile, execute: bool) -> dict:
    rows = read_manifest()
    tokens = {r["chunk_id"]: int(r["estimated_token_count"]) for r in rows}
    with connect("ingest", "embed_research") as conn:
        profile_id, auth_id, todo, counts = preflight_run(conn, profile, rows)
        step = profile.max_texts_per_call
        batches = [todo[i:i + step] for i in range(0, len(todo), step)]
        plan = counts | {"authorization_id": auth_id, "pending": len(todo), "batches": len(batches),
                         "pending_tokens_estimate": sum(tokens[c["chunk_id"]] for c in todo)}
        if not execute:
            return {"mode": "dry_run"} | plan
        conn.commit()
        run_id = conn.execute("""INSERT INTO ingestion_runs (run_type, code_version, input_fingerprint, configuration)
                                 VALUES ('embedding', %s, %s, %s) RETURNING run_id""",
                              (f"embed_research:{profile.profile_code}", sha256_file(MANIFEST),
                               Jsonb(plan | {"scope": "research_test", "model_id": profile.model_id,
                                             "vector_dimension": profile.vector_dimension,
                                             "inputs_per_minute_cap": INPUTS_PER_MINUTE}))).fetchone()[0]
        conn.commit()
        LOGS.mkdir(exist_ok=True)
        log_path = LOGS / f"embedding_research_{run_id}.jsonl"
        embedder = CohereEmbedder(profile, os.environ.get("COHERE_API_KEY", ""))
        results, failed, events = {}, [], []
        started, stored, last_call = time.monotonic(), 0, 0.0
        min_interval = step * 60.0 / INPUTS_PER_MINUTE
        window: list[tuple[float, int]] = []  # (send time, estimated tokens) of the last 60 s
        stop_reason = None
        try:
            for n, batch in enumerate(batches, 1):
                batch_tokens = sum(tokens[c["chunk_id"]] for c in batch)
                wait = min_interval - (time.monotonic() - last_call)
                if last_call and wait > 0:
                    time.sleep(wait)
                while True:
                    window = [(t, k) for t, k in window if time.monotonic() - t < 60.0]
                    if not window or sum(k for _, k in window) + batch_tokens <= TOKENS_PER_MINUTE:
                        break
                    time.sleep(max(0.5, 60.0 - (time.monotonic() - window[0][0])))
                window.append((time.monotonic(), batch_tokens))
                texts = [c["text"] for c in batch]
                payload_bytes = len(json.dumps(profile.payload(texts, profile.document_input_type)).encode("utf-8"))
                calls_before, t0 = embedder.calls, time.monotonic()
                last_call = t0
                event = {"batch": n, "size": len(batch), "payload_bytes": payload_bytes,
                         "tokens_estimate": batch_tokens,
                         "first_chunk": batch[0]["chunk_id"], "last_chunk": batch[-1]["chunk_id"]}
                try:
                    vectors = embedder.embed(texts, profile.document_input_type)
                    if len(vectors) != len(batch):  # also enforced in the client; never store a partial batch
                        raise EmbeddingError("invalid_response", "embedding count does not match input count")
                except EmbeddingError as exc:
                    event |= {"status": "failed", "error_code": exc.code, "error": str(exc)[:120],
                              "attempts": embedder.calls - calls_before, "seconds": round(time.monotonic() - t0, 2)}
                    with open(log_path, "a", encoding="utf-8") as log:  # code + HTTP status only, no text/key
                        log.write(json.dumps(event | {"run_id": str(run_id), "at": now()}) + "\n")
                    failed.append(event | {"at": now(), "chunk_ids": ";".join(c["chunk_id"] for c in batch)})
                    for c in batch:
                        results[c["chunk_id"]] = ("failed", n, None)
                    events.append(event)
                    if exc.code in STOP_CODES:
                        stop_reason = exc.code
                        break
                    continue
                with conn.cursor() as cur:
                    cur.executemany(
                        """INSERT INTO research_chunk_embeddings (chunk_id, profile_id, authorization_id, run_id,
                               model_id, vector_dimension, input_type, embedding, vector_norm, content_sha256,
                               embedding_input_hash)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector, %s, %s, %s)""",
                        [(c["chunk_id"], profile_id, auth_id, run_id, profile.model_id, profile.vector_dimension,
                          profile.document_input_type, str(v), embed_pipeline.l2_norm(v), c["content_hash"],
                          c["input_sha256"]) for c, v in zip(batch, vectors, strict=True)])
                    written = cur.execute("SELECT count(*) FROM research_chunk_embeddings WHERE run_id = %s",
                                          (run_id,)).fetchone()[0]
                if written != stored + len(batch):
                    conn.rollback()
                    stop_reason = "database_count_mismatch"
                    event |= {"status": "failed", "error_code": stop_reason}
                    failed.append(event | {"at": now(), "chunk_ids": ";".join(c["chunk_id"] for c in batch)})
                    events.append(event)
                    break
                conn.commit()  # checkpoint: one batch = one transaction
                stored += len(batch)
                for c, v in zip(batch, vectors, strict=True):
                    results[c["chunk_id"]] = ("stored", n, embed_pipeline.l2_norm(v))
                event |= {"status": "stored", "attempts": embedder.calls - calls_before,
                          "seconds": round(time.monotonic() - t0, 2)}
                events.append(event)
                with open(log_path, "a", encoding="utf-8") as log:  # no text, no key
                    log.write(json.dumps(event | {"run_id": str(run_id), "at": now()}) + "\n")
        except Exception as exc:  # unsafe: stop, record, re-raise after closing the run
            conn.rollback()
            stop_reason = f"unexpected:{type(exc).__name__}"
            raise
        finally:
            embedder.close()
            duration = round(time.monotonic() - started, 1)
            status = "succeeded" if stored == len(todo) else ("partial" if stored else "failed")
            stats = {"stored": stored, "pending_at_start": len(todo), "failed_batches": len(failed),
                     "api_requests": embedder.calls, "logical_batches": len(events),
                     "billed_input_tokens": embedder.billed_input_tokens, "duration_seconds": duration,
                     "stop_reason": stop_reason, "events": events}
            conn.execute("UPDATE ingestion_runs SET status = %s, finished_at = now(), stats = %s, error_summary = %s "
                         "WHERE run_id = %s",
                         (status, Jsonb(stats), stop_reason or (f"{len(failed)} failed batches" if failed else None),
                          run_id))
            conn.commit()
            write_run_files(rows, results, failed, str(run_id), profile)
    return {"mode": "execute", "run_id": str(run_id), "status": status} | {k: v for k, v in stats.items()
                                                                            if k != "events"}


def write_run_files(rows: list[dict], results: dict, failed: list[dict], run_id: str,
                    profile: EmbeddingProfile) -> None:
    fields = ["chunk_id", "source_id", "document_id", "group_membership", "content_hash", "input_sha256",
              "estimated_token_count", "batch", "status", "run_id", "model_id", "vector_dimension", "vector_norm"]
    with connect("ingest", "embed_research_files") as conn:
        stored = {cid: (str(rid), norm) for cid, rid, norm in conn.execute(
            "SELECT chunk_id, run_id, vector_norm FROM research_chunk_embeddings")}
    with open(RUN_MANIFEST, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            status, batch, _norm = results.get(r["chunk_id"], (None, "", None))
            if status is None:
                status = "stored" if r["chunk_id"] in stored else "not_attempted"  # final state; run_id says which run
            rid, db_norm = stored.get(r["chunk_id"], ("", None))
            w.writerow({k: r[k] for k in ("chunk_id", "source_id", "document_id", "group_membership", "content_hash",
                                          "input_sha256", "estimated_token_count")}
                       | {"batch": batch, "status": status, "run_id": rid or (run_id if status == "failed" else ""),
                          "model_id": profile.model_id if rid else "",
                          "vector_dimension": profile.vector_dimension if rid else "",
                          "vector_norm": "" if db_norm is None else f"{db_norm:.6f}"})
    previous = []  # keep the failed batches of earlier runs: the file is cumulative
    if FAILED_BATCHES.exists():
        with open(FAILED_BATCHES, encoding="utf-8-sig") as f:
            previous = [r for r in csv.DictReader(f) if r["run_id"] != run_id]
    with open(FAILED_BATCHES, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["run_id", "batch", "size", "error_code", "error", "attempts", "seconds",
                                          "payload_bytes", "tokens_estimate", "first_chunk", "last_chunk",
                                          "chunk_ids", "at"], extrasaction="ignore")
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in w.fieldnames} for r in previous)
        for b in failed:
            w.writerow({"run_id": run_id} | {k: b.get(k, "") for k in w.fieldnames if k != "run_id"})


# ------------------------------------------------------------------------------------------- verify
QUERIES = [
    "Dấu hiệu sớm của rối loạn phổ tự kỷ ở trẻ 18 tháng tuổi là gì?",
    "What early intervention approaches improve communication in autistic preschool children?",
    "Cha mẹ có thể làm gì khi trẻ tự kỷ có hành vi thách thức ở nhà?",
    "Sensory integration therapy effectiveness for autistic children",
    "Tỷ lệ trẻ tự kỷ có kèm rối loạn tăng động giảm chú ý (ADHD)",
]


def verify(profile: EmbeddingProfile, query_check: bool) -> dict:
    rows = read_manifest()
    manifest_ids = {r["chunk_id"] for r in rows}
    with open(REPORTS / "embedding_excluded.csv", encoding="utf-8-sig") as f:
        excluded_ids = {r["chunk_id"] for r in csv.DictReader(f) if r["chunk_id"]}
    with connect("ingest", "embed_research_verify") as conn:
        conn.read_only = True
        one = lambda sql, *p: conn.execute(sql, p).fetchone()[0]  # noqa: E731
        prof_id = one("SELECT profile_id FROM embedding_profiles WHERE profile_code = %s", profile.profile_code)
        vecs = conn.execute("""SELECT e.chunk_id, e.run_id, e.model_id, e.vector_dimension, vector_dims(e.embedding),
                                      e.vector_norm, e.content_sha256 = c.content_sha256, e.input_type,
                                      d.source_id, d.document_id, s.source_url, c.page_start, c.char_start
                               FROM research_chunk_embeddings e JOIN chunks c USING (chunk_id)
                               JOIN documents d ON d.document_id = c.document_id
                               JOIN sources s ON s.source_id = d.source_id WHERE e.profile_id = %s""",
                            (prof_id,)).fetchall()
        non_finite = one("""SELECT count(*) FROM research_chunk_embeddings e, LATERAL unnest(e.embedding::real[]) x
                            WHERE x = 'NaN'::real OR x IN ('Infinity'::real, '-Infinity'::real)""")
        not_candidates = one("""SELECT count(*) FROM research_chunk_embeddings e WHERE NOT EXISTS (
            SELECT 1 FROM v_research_embedding_candidates v WHERE v.chunk_id = e.chunk_id
              AND v.authorization_id = e.authorization_id AND v.content_sha256 = e.content_sha256)""")
        dup = one("""SELECT count(*) FROM (SELECT chunk_id FROM research_chunk_embeddings GROUP BY chunk_id
                     HAVING count(*) > 1) x""")
        production = {"chunk_embeddings": one("SELECT count(*) FROM chunk_embeddings"),
                      "v_embedding_eligible_documents": one("SELECT count(*) FROM v_embedding_eligible_documents"),
                      "v_retrieval_ready_chunks": one("SELECT count(*) FROM v_retrieval_ready_chunks"),
                      "approved_for_embedding": one("SELECT count(*) FROM documents WHERE approved_for_embedding"),
                      "rights_flags_set": one("""SELECT count(*) FROM source_rights WHERE archive_allowed IS NOT NULL
                           OR text_mining_allowed IS NOT NULL OR chunking_allowed IS NOT NULL
                           OR embedding_allowed IS NOT NULL OR cohere_processing_allowed IS NOT NULL
                           OR external_llm_processing_allowed IS NOT NULL""")}
        runs = conn.execute("""SELECT run_id, status, started_at, finished_at, stats, error_summary FROM ingestion_runs
                               WHERE code_version = %s ORDER BY started_at""",
                            (f"embed_research:{profile.profile_code}",)).fetchall()
        auth = conn.execute("""SELECT authorization_id, authorized_by, recorded_by, basis, authorized_at,
                                      manifest_sha256, production_approval FROM research_embedding_authorizations
                               WHERE revoked_at IS NULL ORDER BY authorization_id DESC LIMIT 1""").fetchone()
        query_results = None
        if query_check:
            embedder = CohereEmbedder(profile, os.environ.get("COHERE_API_KEY", ""))
            try:
                qv = embedder.embed(QUERIES, profile.query_input_type)
            finally:
                embedder.close()
            query_results = {"api_requests": embedder.calls, "billed_input_tokens": embedder.billed_input_tokens,
                             "results": []}
            for q, v in zip(QUERIES, qv, strict=True):
                top = conn.execute("""SELECT e.chunk_id, d.source_id, 1 - (e.embedding <=> %s::vector) AS cosine,
                                             left(regexp_replace(c.content, '\\s+', ' ', 'g'), 110)
                                      FROM research_chunk_embeddings e JOIN chunks c USING (chunk_id)
                                      JOIN documents d ON d.document_id = c.document_id
                                      ORDER BY e.embedding <=> %s::vector LIMIT 3""", (str(v), str(v))).fetchall()
                query_results["results"].append({"query": q, "top": [
                    {"chunk_id": t[0], "source_id": t[1], "cosine": round(float(t[2]), 4), "snippet": t[3]}
                    for t in top]})

    ids = [v[0] for v in vecs]
    norms = [float(v[5]) for v in vecs]
    checks = {
        "stored vectors = eligible chunks": (len(vecs), len(rows)),
        "every eligible chunk has a vector": len(manifest_ids - set(ids)) == 0,
        "no vector outside the manifest": len(set(ids) - manifest_ids) == 0,
        "no vector for an excluded chunk": len(set(ids) & excluded_ids) == 0,
        "all dimensions = 1536 (column, record, actual)": all(v[3] == 1536 and v[4] == 1536 for v in vecs),
        "model = embed-v4.0, input_type = search_document": all(
            v[2] == "embed-v4.0" and v[7] == "search_document" for v in vecs),
        "no NaN/Inf coordinate": non_finite == 0,
        "vector norms finite and > 0": all(math.isfinite(n) and n > 0 for n in norms),
        "content hash matches current chunk": all(v[6] for v in vecs),
        "one vector per chunk_id": dup == 0 and len(ids) == len(set(ids)),
        "every vector is an authorized current candidate": not_candidates == 0,
        "provenance: source_id, document_id, URL, page or char range": all(
            v[8] and v[9] and v[10] and (v[11] is not None or v[12] is not None) for v in vecs),
        "production untouched (0 vectors / gates / approvals / rights flags)": not any(production.values()),
    }
    ok = all(v is True or (isinstance(v, tuple) and v[0] == v[1]) for v in checks.values())
    groups = {g: [r for r in rows if g in r["group_membership"].split(";")] for g in "ABC"}
    stored_ids = set(ids)
    summary = {
        "ok": ok, "checks": checks, "production": production, "non_finite": non_finite,
        "norm_min": min(norms, default=None), "norm_max": max(norms, default=None),
        "per_group": {g: {"sources": len({r["source_id"] for r in rs}), "chunks": len(rs),
                          "stored": sum(1 for r in rs if r["chunk_id"] in stored_ids)} for g, rs in groups.items()},
        "union": {"sources": len({r["source_id"] for r in rows}), "documents": len({r["document_id"] for r in rows}),
                  "chunks": len(rows), "stored": len(stored_ids & manifest_ids)},
        "runs": [{"run_id": str(r[0]), "status": r[1], "started_at": r[2].isoformat(timespec="seconds"),
                  "finished_at": r[3].isoformat(timespec="seconds") if r[3] else None,
                  "stats": {k: v for k, v in (r[4] or {}).items() if k != "events"}, "error": r[5]} for r in runs],
        "authorization": auth, "queries": query_results,
    }
    write_reports(summary)
    return summary


def write_reports(s: dict) -> None:
    status = "COMPLETED" if s["ok"] else ("PARTIAL" if s["union"]["stored"] else "FAILED")
    L = [f"# Embedding quality check — {now()[:10]}", "",
         f"**Trạng thái: {status}** — kiểm tra trên vector thật trong `asd_rag.research_chunk_embeddings` "
         f"(sinh bởi `scripts/embed_research.py verify`, {now()}).", "",
         "| Kiểm tra | Kết quả |", "|---|---|"]
    for k, v in s["checks"].items():
        shown = f"{v[0]:,} / {v[1]:,} {'✔' if v[0] == v[1] else '✘'}" if isinstance(v, tuple) else ("✔" if v else "✘")
        L.append(f"| {k} | {shown} |")
    L += ["", f"Chuẩn L2 của vector: min {s['norm_min']:.4f}, max {s['norm_max']:.4f}." if s["norm_min"] else "",
          "", "Production (phải bằng 0): " + ", ".join(f"`{k}` = {v}" for k, v in s["production"].items()) + ".", ""]
    if s["queries"]:
        L += ["## Kiểm tra truy vấn (search_query, exact cosine, chỉ để kiểm tra kỹ thuật)",
              f"{len(QUERIES)} câu hỏi thử, {s['queries']['api_requests']} lời gọi API, "
              f"{s['queries']['billed_input_tokens']} token tính phí. Không phải đánh giá chất lượng truy xuất "
              "(Phase 5/7, cần bộ câu hỏi chuẩn có chuyên gia duyệt).", ""]
        for r in s["queries"]["results"]:
            L.append(f"**{r['query']}**")
            L += [f"- {t['cosine']:.3f} · `{t['source_id']}` · {t['snippet']}…" for t in r["top"]]
            L.append("")
    (REPORTS / "embedding_quality_check.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", default="cohere_embed_v4_1536_v1")
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("authorize")
    a.add_argument("--authorized-by", required=True)
    a.add_argument("--basis", required=True)
    a.add_argument("--notes")
    r = sub.add_parser("run")
    r.add_argument("--execute", action="store_true")
    v = sub.add_parser("verify")
    v.add_argument("--query-check", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    profile = EmbeddingProfile.load(args.profile)
    if args.cmd == "authorize":
        out = authorize(profile, args.authorized_by, args.basis, args.notes)
    elif args.cmd == "run":
        out = run(profile, args.execute)
    else:
        out = verify(profile, args.query_check)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    return 0 if out.get("ok", True) and out.get("status", "succeeded") == "succeeded" else 1


if __name__ == "__main__":
    sys.exit(main())
