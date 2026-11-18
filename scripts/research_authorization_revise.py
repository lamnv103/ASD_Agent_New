"""Revise the research authorization by excluding a verified list of chunks (Phase 6.2 T2.0, decision D-1).

Non-destructive by design: no vector, chunk or embedding row is touched. The current authorization is
REVOKED (row kept, revoked_at set) and a new authorization is inserted with allowlist = old allowlist minus
the exclusion manifest, in ONE transaction (owner role). Restoring is symmetric (--restore).

  python -B scripts/research_authorization_revise.py --exclusions <exclusion manifest CSV>
        dry run: validates the manifest against the active authorization, prints counts, writes nothing
  ... --execute --authorized-by "..." --basis "..."
        writes the new allowlist CSV (its SHA-256 becomes manifest_sha256), revokes the old authorization,
        inserts the new one (+ sources + chunks)
  python -B scripts/research_authorization_revise.py --restore --revoke <new_id> --reactivate <old_id>
        reverts a revision (revoke the new authorization, clear revoked_at of the old one)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS
from app.db import connect

PROFILE = "cohere_embed_v4_1536_v1"
RECORDED_BY = "Claude Code via scripts/research_authorization_revise.py (asd_rag_v2_owner)"


def load_exclusions(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    ids = [r["chunk_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("exclusion manifest has duplicate chunk_ids")
    bad = [r["chunk_id"] for r in rows if not r["verification_status"].startswith("verified")]
    if bad:
        raise SystemExit(f"{len(bad)} exclusions are not verified; refusing")
    return rows


def plan(conn, exclusions: list[dict]) -> dict:
    active = conn.execute("""SELECT authorization_id, chunking_profile, manifest_sha256
                             FROM research_embedding_authorizations
                             WHERE revoked_at IS NULL AND profile_code = %s""", (PROFILE,)).fetchall()
    if len(active) != 1:
        raise SystemExit(f"expected exactly one active authorization for {PROFILE}, found {len(active)}")
    old_id, chunking_profile, old_sha = active[0]
    allow = {cid: (sid, h) for cid, sid, h in conn.execute(
        "SELECT chunk_id, source_id, content_sha256 FROM research_embedding_authorization_chunks "
        "WHERE authorization_id = %s",
        (old_id,))}
    groups = dict(conn.execute("SELECT source_id, group_membership FROM research_embedding_authorization_sources "
                               "WHERE authorization_id = %s", (old_id,)).fetchall())
    problems = []
    for r in exclusions:
        cur = allow.get(r["chunk_id"])
        if cur is None:
            problems.append(f"not in active allowlist: {r['chunk_id']}")
        elif cur[1] != r["content_sha256"] or cur[0] != r["source_id"]:
            problems.append(f"hash/source mismatch: {r['chunk_id']}")
    if problems:
        raise SystemExit("exclusion manifest does not match the active authorization:\n" + "\n".join(problems[:20]))
    excluded = {r["chunk_id"] for r in exclusions}
    keep = {cid: v for cid, v in allow.items() if cid not in excluded}
    vectors = {cid for (cid,) in conn.execute(
        "SELECT e.chunk_id FROM research_chunk_embeddings e JOIN embedding_profiles p USING (profile_id) "
        "WHERE p.profile_code = %s", (PROFILE,))}
    docs = dict(conn.execute("SELECT chunk_id, document_id FROM chunks WHERE chunk_id = ANY(%s)",
                             (list(keep),)).fetchall())
    return {"old_id": old_id, "old_manifest_sha256": old_sha, "chunking_profile": chunking_profile,
            "old_allowlist": len(allow), "excluded": len(excluded), "new_allowlist": len(keep),
            "new_without_vector": len(set(keep) - vectors), "sources_old": len(groups),
            "sources_new": len({v[0] for v in keep.values()}), "keep": keep, "groups": groups, "docs": docs}


def write_allowlist(p: dict, path: Path) -> str:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["chunk_id", "document_id", "source_id", "content_sha256", "group_membership"])
        for cid in sorted(p["keep"]):
            sid, h = p["keep"][cid]
            w.writerow([cid, p["docs"][cid], sid, h, ";".join(p["groups"][sid])])
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(conn, p: dict, sha: str, authorized_by: str, basis: str, exclusions_path: Path, excl_sha: str) -> int:
    notes = json.dumps({"revision_of_authorization_id": p["old_id"], "decision": "D-1 (Phase 6.2 T2.0)",
                        "excluded_chunks": p["excluded"], "exclusion_manifest": exclusions_path.name,
                        "exclusion_manifest_sha256": excl_sha}, ensure_ascii=False)
    with conn.transaction():
        n = conn.execute("UPDATE research_embedding_authorizations SET revoked_at = now() "
                         "WHERE authorization_id = %s AND revoked_at IS NULL", (p["old_id"],)).rowcount
        if n != 1:
            raise SystemExit("could not revoke the active authorization (concurrent change?)")
        new_id = conn.execute("""INSERT INTO research_embedding_authorizations (scope, authorized_by, recorded_by,
                                     basis, profile_code, chunking_profile, manifest_sha256, notes)
                                 VALUES ('research_test', %s, %s, %s, %s, %s, %s, %s) RETURNING authorization_id""",
                              (authorized_by, RECORDED_BY, basis, PROFILE, p["chunking_profile"], sha,
                               notes)).fetchone()[0]
        srcs = sorted({v[0] for v in p["keep"].values()})
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO research_embedding_authorization_sources VALUES (%s, %s, %s)",
                            [(new_id, s, p["groups"][s]) for s in srcs])
            cur.executemany("INSERT INTO research_embedding_authorization_chunks VALUES (%s, %s, %s, %s)",
                            [(new_id, sid, cid, h) for cid, (sid, h) in sorted(p["keep"].items())])
        got = conn.execute("SELECT count(*) FROM research_embedding_authorization_chunks WHERE authorization_id = %s",
                           (new_id,)).fetchone()[0]
        if got != p["new_allowlist"]:
            raise SystemExit(f"allowlist count mismatch after insert ({got} != {p['new_allowlist']}); rolled back")
    return new_id


def restore(conn, revoke_id: int, reactivate_id: int) -> dict:
    with conn.transaction():
        a = conn.execute("UPDATE research_embedding_authorizations SET revoked_at = now() "
                         "WHERE authorization_id = %s AND revoked_at IS NULL", (revoke_id,)).rowcount
        b = conn.execute("UPDATE research_embedding_authorizations SET revoked_at = NULL "
                         "WHERE authorization_id = %s AND revoked_at IS NOT NULL", (reactivate_id,)).rowcount
        if (a, b) != (1, 1):
            raise SystemExit(f"restore expected 1+1 rows, got {a}+{b}; rolled back")
    return {"revoked": revoke_id, "reactivated": reactivate_id}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--exclusions", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorized-by")
    parser.add_argument("--basis")
    parser.add_argument("--allowlist-out", type=Path,
                        default=REPORTS / "research_authorization_allowlist_rev_d1_2026-11-14.csv")
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--revoke", type=int)
    parser.add_argument("--reactivate", type=int)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    with connect("owner", "research_authorization_revise") as conn:
        conn.autocommit = True  # explicit transaction blocks below
        if args.restore:
            if not (args.revoke and args.reactivate):
                raise SystemExit("--restore needs --revoke and --reactivate")
            print(json.dumps(restore(conn, args.revoke, args.reactivate)))
            return 0
        if not args.exclusions:
            raise SystemExit("--exclusions is required")
        exclusions = load_exclusions(args.exclusions)
        excl_sha = hashlib.sha256(args.exclusions.read_bytes()).hexdigest()
        p = plan(conn, exclusions)
        if p["new_without_vector"]:
            raise SystemExit(f"{p['new_without_vector']} allowlisted chunks have no vector; refusing")
        summary = {k: v for k, v in p.items() if k not in ("keep", "groups", "docs")}
        summary["exclusion_manifest_sha256"] = excl_sha
        if not args.execute:
            print(json.dumps(summary | {"mode": "dry_run"}, indent=1))
            return 0
        if not (args.authorized_by and args.basis):
            raise SystemExit("--execute needs --authorized-by and --basis")
        if args.allowlist_out.exists():
            raise SystemExit(f"{args.allowlist_out} exists; refusing to overwrite")
        sha = write_allowlist(p, args.allowlist_out)
        new_id = execute(conn, p, sha, args.authorized_by, args.basis, args.exclusions, excl_sha)
        print(json.dumps(summary | {"mode": "execute", "new_authorization_id": new_id,
                                    "allowlist_file": args.allowlist_out.name, "allowlist_sha256": sha}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
