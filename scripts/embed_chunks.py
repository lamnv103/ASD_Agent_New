"""Embedding pipeline driver. Default is a DRY RUN: database reads only, no provider call.

Dry run reports: profile/schema compatibility, chunks that pass the database gate, why every other
document is blocked, and (with --what-if) the volume per licence group if the owner approved it.

Execution sends chunk text to Cohere, so it needs BOTH --execute and --confirm-rights-approved, and it
still embeds only what v_embedding_eligible_documents admits. Batches commit one by one (checkpoint);
re-running resumes and skips vectors that already exist for the same input hash.

Usage:
  python -B scripts/embed_chunks.py                       # dry run
  python -B scripts/embed_chunks.py --what-if             # + volume estimate per licence group
  python -B scripts/embed_chunks.py --execute --confirm-rights-approved
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from psycopg.types.json import Jsonb

from app.config import CORPUS_MANIFEST, REPORTS, ROOT
from app.db import connect
from app.ingest import embed_pipeline
from app.ingest.chunking import ChunkingProfile, DocumentInfo, HFTokenCounter, chunk_document
from app.retrieval.embeddings import CohereEmbedder, EmbeddingProfile

EXPECTED = {"model_id": "embed-v4.0", "vector_dimension": 1536, "document_input_type": "search_document",
            "query_input_type": "search_query", "similarity_metric": "cosine"}
TRIAL_MONTHLY_CALLS = 1000  # x-endpoint-monthly-call-limit observed on 2026-11-14


def compatibility(conn, profile: EmbeddingProfile) -> dict:
    column = conn.execute("""SELECT format_type(a.atttypid, a.atttypmod) FROM pg_attribute a
                             WHERE a.attrelid = 'asd_rag.chunk_embeddings'::regclass
                               AND a.attname = 'embedding'""").fetchone()[0]
    mismatches = {k: (getattr(profile, k), v) for k, v in EXPECTED.items() if getattr(profile, k) != v}
    return {"profile": profile.profile_code, "db_vector_column": column,
            "column_matches_profile": column == f"vector({profile.vector_dimension})",
            "profile_matches_verified_config": not mismatches, "mismatches": mismatches,
            "cohere_key_present": bool(os.environ.get("COHERE_API_KEY"))}


def what_if(profile: EmbeddingProfile) -> dict:
    """Chunk every non-quarantined document in memory and group volume by the audited licence."""
    with open(REPORTS / "license_review_matrix.csv", encoding="utf-8-sig") as f:
        matrix = {r["source_id"]: r for r in csv.DictReader(f)}
    chunker = ChunkingProfile.load(profile.chunking_profile)
    counter = HFTokenCounter(chunker.tokenizer_path, chunker.tokenizer_sha256)
    groups: dict[str, Counter] = defaultdict(Counter)
    for line in CORPUS_MANIFEST.read_text(encoding="utf-8").splitlines():
        m = json.loads(line)
        if m["text_fidelity_warning"]:
            continue
        info = DocumentInfo(m["source_id"], m["source_id"], m["title"], m["tier"], m["source_type"], "en",
                            m["conversion_gaps"])
        chunks = [c for c in chunk_document((ROOT / m["path"]).read_text(encoding="utf-8-sig"), info, chunker,
                                            counter).chunks if c.retrieval_eligible]
        row = matrix[m["source_id"]]
        group = f"{row['license_name']} (cohere: {row['cohere_processing_allowed']})"
        groups[group].update(documents=1, chunks=len(chunks), tokens=sum(c.token_count for c in chunks))
    out = {g: dict(c) | {"api_calls": math.ceil(c["chunks"] / profile.max_texts_per_call)} for g, c in groups.items()}
    total_calls = sum(v["api_calls"] for v in out.values())
    return {"groups": out, "total_api_calls_if_all_approved": total_calls,
            "trial_monthly_call_limit": TRIAL_MONTHLY_CALLS}


def execute(conn, profile: EmbeddingProfile, inputs: list[embed_pipeline.EmbeddingInput]) -> dict:
    conn.execute("""INSERT INTO embedding_profiles (profile_code, provider, model_id, model_revision, vector_dimension,
                        document_input_type, query_input_type, similarity_metric, api_version, configuration)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (profile_code) DO NOTHING""",
                 (profile.profile_code, profile.provider, profile.model_id, profile.model_revision,
                  profile.vector_dimension, profile.document_input_type, profile.query_input_type,
                  profile.similarity_metric, profile.api_version, Jsonb(profile.__dict__)))
    profile_id = conn.execute("SELECT profile_id FROM embedding_profiles WHERE profile_code = %s",
                              (profile.profile_code,)).fetchone()[0]
    todo = embed_pipeline.pending(conn, inputs, profile_id)
    run_id = conn.execute("INSERT INTO ingestion_runs (run_type, code_version, configuration) "
                          "VALUES ('embedding', %s, %s) RETURNING run_id",
                          (f"embed:{profile.profile_code}", Jsonb({"pending": len(todo)}))).fetchone()[0]
    conn.commit()
    embedder = CohereEmbedder(profile, os.environ.get("COHERE_API_KEY", ""))
    stored = 0
    try:
        for i in range(0, len(todo), profile.max_texts_per_call):
            batch = todo[i:i + profile.max_texts_per_call]
            vectors = embedder.embed([x.text for x in batch], profile.document_input_type)
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO chunk_embeddings (chunk_id, profile_id, embedding, vector_norm, embedding_input_hash) "
                    "VALUES (%s, %s, %s::vector, %s, %s)",
                    [(x.chunk_id, profile_id, str(v), embed_pipeline.l2_norm(v), x.input_hash)
                     for x, v in zip(batch, vectors, strict=True)])
            conn.commit()  # checkpoint
            stored += len(batch)
    finally:
        embedder.close()
        status = "succeeded" if stored == len(todo) else "partial"
        conn.execute("UPDATE ingestion_runs SET status=%s, finished_at=now(), stats=%s WHERE run_id=%s",
                     (status, Jsonb({"stored": stored, "api_calls": embedder.calls}), run_id))
        conn.commit()
    return {"run_id": str(run_id), "stored": stored, "skipped_existing": len(inputs) - len(todo)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", default="cohere_embed_v4_1536_v1")
    parser.add_argument("--what-if", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-rights-approved", action="store_true")
    args = parser.parse_args()
    profile = EmbeddingProfile.load(args.profile)

    with connect("ingest", "embed_chunks") as conn:
        report = {"mode": "execute" if args.execute else "dry_run", "compatibility": compatibility(conn, profile)}
        inputs = embed_pipeline.eligible_inputs(conn, profile)
        blocked = [b for b in embed_pipeline.blockers(conn, profile) if b["blocked_by"]]
        report |= {"eligible_chunks": len(inputs), "eligible_documents": len({x.document_id for x in inputs}),
                   "blocked_documents": len(blocked),
                   "blocked_reasons": dict(Counter(r for b in blocked for r in b["blocked_by"]).most_common())}
        if args.what_if:
            report["what_if"] = what_if(profile)
        if args.execute:
            if not args.confirm_rights_approved:
                raise SystemExit("--execute needs --confirm-rights-approved (owner decision recorded in the database)")
            if not inputs:
                raise SystemExit("No chunk passes the embedding gate; nothing would be sent.")
            if not report["compatibility"]["profile_matches_verified_config"]:
                raise SystemExit("Embedding profile does not match the verified configuration.")
            report["result"] = execute(conn, profile, inputs)
    print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
