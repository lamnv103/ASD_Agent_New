"""Preflight for the research embedding run (groups A/B/C). Database READ ONLY; no provider call.

Builds the union of the three groups by source_id (never by adding group counts), applies the chunk rules
of app/ingest/embedding_manifest.py, checks provenance/traceability/duplicates/URLs, and writes:
  eval/reports/embedding_manifest.csv       eligible chunks (embedding_status = pending)
  eval/reports/embedding_excluded.csv       every excluded chunk or source, one reason each
  eval/reports/embedding_preflight_report.md

Usage: python -B scripts/embedding_preflight.py [--profile cohere_embed_v4_1536_v1]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import REPORTS, ROOT
from app.db import connect
from app.ingest import embed_pipeline
from app.ingest.chunking import ChunkingProfile, HFTokenCounter
from app.ingest.embedding_manifest import ChunkRow, classify, group_membership, valid_url
from app.retrieval.embeddings import EmbeddingProfile

FIELDS = ["source_id", "document_id", "chunk_id", "title", "organization", "source_url", "section", "page",
          "content_hash", "chunk_version", "character_count", "estimated_token_count", "group_membership",
          "embedding_status", "exclusion_reason", "char_range", "license_type", "input_sha256"]

DOCS = """
SELECT d.document_id, d.source_id, d.document_version, d.corpus_relative_path, d.file_sha256, d.file_format,
       d.character_count, d.content_review_status, d.content_warning, d.is_current,
       s.title, s.publisher, s.source_url, s.corpus_role, r.rights_status, r.license_type
FROM documents d JOIN sources s USING (source_id) JOIN source_rights r USING (source_id)
"""
CHUNKS = """
SELECT c.chunk_id, c.document_id, c.section_type, c.completeness_status, c.retrieval_eligible, c.content,
       c.content_sha256, c.page_start, c.page_end, c.char_start, c.char_end, c.section_heading, c.section_path,
       c.chunk_index
FROM chunks c WHERE c.chunking_profile = %s ORDER BY c.chunk_id
"""
NOT_FULL_TEXT = """
SELECT s.source_id, s.title, s.publisher, s.source_url, s.corpus_role, r.rights_status, r.license_type
FROM sources s JOIN source_rights r USING (source_id) WHERE s.corpus_role NOT IN ('core', 'gaps') ORDER BY 1
"""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", default="cohere_embed_v4_1536_v1")
    args = parser.parse_args()
    profile = EmbeddingProfile.load(args.profile)
    chunker = ChunkingProfile.load(profile.chunking_profile)
    tokens = HFTokenCounter(chunker.tokenizer_path, chunker.tokenizer_sha256)
    with open(REPORTS / "license_review_matrix.csv", encoding="utf-8-sig") as f:
        matrix = {r["source_id"]: r for r in csv.DictReader(f)}

    with connect("ingest", "embedding_preflight") as conn:
        conn.read_only = True
        docs = {r[0]: r for r in conn.execute(DOCS).fetchall()}
        chunks = conn.execute(CHUNKS, (profile.chunking_profile,)).fetchall()
        others = conn.execute(NOT_FULL_TEXT).fetchall()
        blockers = embed_pipeline.blockers(conn, profile)
        gate_docs = conn.execute("SELECT count(*) FROM v_embedding_eligible_documents").fetchone()[0]
        column = conn.execute("""SELECT format_type(atttypid, atttypmod) FROM pg_attribute
                                 WHERE attrelid = 'asd_rag.chunk_embeddings'::regclass
                                   AND attname = 'embedding'""").fetchone()[0]
        existing_vectors = conn.execute("SELECT count(*) FROM chunk_embeddings").fetchone()[0]
        db_version = conn.execute("SELECT current_setting('server_version'), "
                                  "(SELECT extversion FROM pg_extension WHERE extname = 'vector')").fetchone()

    # ---- groups (union by source_id) --------------------------------------------------------------
    current = {d[1]: d for d in docs.values() if d[9]}  # source_id -> current document row
    membership = {sid: group_membership(d[13], d[14], matrix.get(sid, {}).get("verification_status", ""))
                  for sid, d in current.items()}
    groups = {g: {sid for sid, m in membership.items() if g in m} for g in "ABC"}
    quarantined = sorted(sid for sid, d in current.items() if d[7] == "quarantined")
    union = (groups["A"] | groups["B"] | groups["C"])

    # ---- chunk rules -------------------------------------------------------------------------------
    rows = []
    for c in chunks:
        d = docs[c[1]]
        rows.append(ChunkRow(chunk_id=c[0], document_id=c[1], source_id=d[1], section_type=c[2],
                             completeness_status=c[3], retrieval_eligible=c[4], content=c[5], content_sha256=c[6],
                             file_format=d[5], page_start=c[7], page_end=c[8], char_start=c[9], char_end=c[10]))
    reasons = classify(rows)
    extra = {c[0]: c for c in chunks}

    # ---- traceability per document -----------------------------------------------------------------
    trace_problems = []
    for doc_id in sorted({r.document_id for r in rows}):
        d = docs[doc_id]
        path = ROOT / d[3]
        if not d[9]:
            trace_problems.append(f"{doc_id}: chunks belong to a non-current document")
        if not path.is_file():
            trace_problems.append(f"{doc_id}: corpus file missing ({d[3]})")
        elif sha256_file(path) != d[4]:
            trace_problems.append(f"{doc_id}: corpus file sha256 differs from documents.file_sha256")
        if d[1] not in union:
            trace_problems.append(f"{doc_id}: source {d[1]} not in any group")

    manifest, excluded = [], []
    for r in rows:
        d, c = docs[r.document_id], extra[r.chunk_id]
        reason = reasons[r.chunk_id]
        if reason is None and r.source_id in quarantined:
            reason = "quarantined_document"
        if reason is None and r.source_id not in union:
            reason = "source_not_in_groups"
        if reason is None and not valid_url(d[12]):
            reason = "malformed_source_url"
        text = embed_pipeline.build_input(profile, d[10], c[11], c[5])
        record = {
            "source_id": r.source_id, "document_id": r.document_id, "chunk_id": r.chunk_id, "title": d[10],
            "organization": d[11] or "", "source_url": d[12] or "",
            "section": " > ".join(c[12] or []) or (c[11] or ""),
            "page": "" if r.page_start is None else (f"{r.page_start}" if r.page_start == r.page_end
                                                     else f"{r.page_start}-{r.page_end}"),
            "content_hash": r.content_sha256, "chunk_version": f"{profile.chunking_profile}@{d[2]}",
            "character_count": len(r.content), "estimated_token_count": tokens.count(text),
            "group_membership": ";".join(membership.get(r.source_id, ())),
            "embedding_status": "pending" if reason is None else "excluded", "exclusion_reason": reason or "",
            "char_range": "" if r.char_start is None else f"{r.char_start}-{r.char_end}",
            "license_type": d[15] or "", "input_sha256": embed_pipeline.input_hash(profile, text),
        }
        (manifest if reason is None else excluded).append(record)
    for sid in quarantined:
        d = current[sid]
        excluded.append({k: "" for k in FIELDS} | {
            "source_id": sid, "document_id": d[0], "title": d[10], "organization": d[11] or "",
            "source_url": d[12] or "", "group_membership": ";".join(membership[sid]), "embedding_status": "excluded",
            "exclusion_reason": "quarantined_document (no section_v2_1 chunks)", "license_type": d[15] or ""})
    for sid, title, publisher, url, role, _rights, lic in others:
        excluded.append({k: "" for k in FIELDS} | {
            "source_id": sid, "title": title, "organization": publisher or "", "source_url": url or "",
            "embedding_status": "excluded", "exclusion_reason": f"{role}_source (no full text)",
            "license_type": lic or ""})

    # ---- checks ------------------------------------------------------------------------------------
    hashes = Counter(m["content_hash"] for m in manifest)
    inputs = Counter(m["input_sha256"] for m in manifest)
    batches = [manifest[i:i + profile.max_texts_per_call] for i in range(0, len(manifest), profile.max_texts_per_call)]
    payload_bytes = []
    for b in batches:
        texts = [embed_pipeline.build_input(profile, m["title"], extra[m["chunk_id"]][11], extra[m["chunk_id"]][5])
                 for m in b]
        payload_bytes.append(len(json.dumps(profile.payload(texts, profile.document_input_type)).encode("utf-8")))
    checks = {
        "duplicate content hash among eligible": sum(v - 1 for v in hashes.values() if v > 1),
        "duplicate embedding input among eligible": sum(v - 1 for v in inputs.values() if v > 1),
        "empty eligible chunks": sum(1 for m in manifest if m["character_count"] == 0),
        "eligible chunks with malformed source_url": sum(1 for m in manifest if not valid_url(m["source_url"])),
        "eligible chunks without source_id": sum(1 for m in manifest if not m["source_id"]),
        "eligible chunks from quarantined documents": sum(1 for m in manifest if m["source_id"] in quarantined),
        "eligible chunks without provenance (page or char range)": sum(
            1 for m in manifest if not m["page"] and not m["char_range"]),
        "eligible chunks with unverified structure status": sum(
            1 for m in manifest if extra[m["chunk_id"]][3] not in
            ("complete", "document_has_gaps", "references_missing_component")),
        "eligible chunks containing /gid glyph codes": sum(1 for m in manifest if "/gid" in extra[m["chunk_id"]][5]),
        "document traceability problems": len(trace_problems),
    }
    preflight_ok = not any(checks.values())

    REPORTS.mkdir(parents=True, exist_ok=True)
    for name, data in (("embedding_manifest.csv", manifest), ("embedding_excluded.csv", excluded)):
        with open(REPORTS / name, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(data)
    digests = {n: sha256_file(REPORTS / n) for n in ("embedding_manifest.csv", "embedding_excluded.csv")}

    # ---- report ------------------------------------------------------------------------------------
    per_group = {}
    for g in "ABC":
        ms = [m for m in manifest if g in m["group_membership"].split(";")]
        per_group[g] = (len(groups[g]), len(groups[g] - set(quarantined)), len({m["source_id"] for m in ms}),
                        len(ms), sum(m["estimated_token_count"] for m in ms))
    reason_counts = Counter(e["exclusion_reason"].split(":")[0] if e["chunk_id"] else e["exclusion_reason"]
                            for e in excluded)
    by_licence = defaultdict(lambda: [set(), 0, 0])
    for m in manifest:
        by_licence[m["license_type"] or "?"][0].add(m["source_id"])
        by_licence[m["license_type"] or "?"][1] += 1
        by_licence[m["license_type"] or "?"][2] += m["estimated_token_count"]
    total_tokens = sum(m["estimated_token_count"] for m in manifest)
    gate_reasons = Counter(x for b in blockers if b["blocked_by"] for x in b["blocked_by"])
    agency_orgs = Counter(current[s][11] for s in groups["C"])
    now = datetime.now(UTC).isoformat(timespec="seconds")

    L = [f"# Embedding preflight — {now[:10]}", "",
         f"**Trạng thái: {'COMPLETED' if preflight_ok else 'FAILED'}** (chỉ đọc DB, không gọi Cohere). "
         f"Sinh lúc {now} bởi `scripts/embedding_preflight.py`.", "",
         "## 1. Môi trường",
         "| Kiểm tra | Kết quả |", "|---|---|",
         f"| `COHERE_API_KEY` trong môi trường | {'có' if os.environ.get('COHERE_API_KEY') else 'KHÔNG'} "
         "(không in giá trị) |",
         f"| Model / dimension / input type | `{profile.model_id}` / {profile.vector_dimension} / "
         f"`{profile.document_input_type}` (tài liệu), `{profile.query_input_type}` (câu hỏi) |",
         f"| PostgreSQL / pgvector | {db_version[0]} / {db_version[1]} |",
         f"| Cột `chunk_embeddings.embedding` | `{column}` → "
         f"{'khớp' if column == f'vector({profile.vector_dimension})' else 'KHÔNG KHỚP'} |",
         f"| Vector đang có trong DB | {existing_vectors} |",
         f"| Chunking profile | `{profile.chunking_profile}` |", "",
         "## 2. Ba nhóm và hợp nhất theo `source_id`",
         "| Nhóm | Định nghĩa | Nguồn | Không cách ly | Nguồn có chunk đủ điều kiện | Chunk đủ điều kiện | Token |",
         "|---|---|---:|---:|---:|---:|---:|"]
    defs = {"A": "toàn văn `core`+`gaps`", "B": "`rights_status = verified_noncommercial_research` (giấy phép NC)",
            "C": "bằng chứng giấy phép chỉ ở cấp chính sách cơ quan (`agency_policy_only`)"}
    for g in "ABC":
        n, nq, ns, nc, nt = per_group[g]
        L.append(f"| {g} | {defs[g]} | {n} | {nq} | {ns} | {nc:,} | {nt:,} |")
    L += ["",
          f"- B ⊂ A: **{groups['B'] <= groups['A']}**, C ⊂ A: **{groups['C'] <= groups['A']}** → hợp nhất = "
          f"**{len(union)} nguồn** ({len(union) - len(set(quarantined) & union)} không cách ly); "
          "không cộng số đếm giữa các nhóm.",
          f"- Nhóm C theo tổ chức: {', '.join(f'{k} {v}' for k, v in agency_orgs.most_common())}.",
          f"- Cách ly (loại cả tài liệu): {', '.join(quarantined)}. Không có chunk `section_v2_1`.",
          f"- Không đưa vào: {sum(1 for o in others if o[4] == 'metadata_only')} nguồn `metadata_only`, "
          f"{sum(1 for o in others if o[4] == 'excluded')} nguồn `excluded` (không có toàn văn).", "",
          "## 3. Tập sẽ embedding (hợp nhất, mỗi chunk một lần)",
          "| Chỉ số | Giá trị |", "|---|---:|",
          f"| Nguồn / tài liệu | {len({m['source_id'] for m in manifest})} / "
          f"{len({m['document_id'] for m in manifest})} |",
          f"| Chunk `section_v2_1` của các tài liệu này | {len(rows):,} |",
          f"| Chunk đủ điều kiện (`embedding_manifest.csv`) | **{len(manifest):,}** |",
          "| Token ước tính (tokenizer embed-v4.0 trên văn bản gửi đi: tiêu đề + heading + nội dung) | "
          f"{total_tokens:,} |",
          f"| Token lớn nhất một input | {max(m['estimated_token_count'] for m in manifest):,} |",
          f"| Lô (≤ {profile.max_texts_per_call}) / lời gọi API dự kiến | {len(batches)} |",
          f"| Payload lớn nhất một lô | {max(payload_bytes) / 1024:,.0f} KiB |", "",
          "Theo giấy phép:", "", "| Giấy phép | Nguồn | Chunk | Token |", "|---|---:|---:|---:|"]
    for lic, (srcs, n, t) in sorted(by_licence.items()):
        L.append(f"| {lic} | {len(srcs)} | {n:,} | {t:,} |")
    L += ["", "## 4. Loại trừ (`embedding_excluded.csv`)", "| Lý do | Số dòng |", "|---|---:|"]
    for k, v in sorted(reason_counts.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {v:,} |")
    L += ["",
          "Quy tắc (theo thứ tự, mỗi chunk một lý do — `app/ingest/embedding_manifest.py`, có unit test):",
          "1. Trạng thái cấu trúc chưa kiểm chứng: `table_structure_unrecoverable` (bảng PDF mất cấu trúc), "
          "`table_recovered_pending_review`, `text_encoding_lost` (chuỗi `/gid…`).",
          "2. Mục không phải nội dung (`retrieval_eligible = false`): tham khảo, người đóng góp, "
          "front/back matter, nhiễu.",
          "3. Chunk rỗng; còn mã glyph; thiếu provenance (PDF: trang; HTML/XML: khoảng ký tự).",
          "4. **Nội dung chưa xác định**: `section_type = unclassified` — lẫn danh mục tham khảo, danh sách hình, "
          "boilerplate nhà xuất bản (đã đọc 32/32); loại cả nhóm, chờ duyệt thủ công.",
          "5. **Mảnh vụn** < 6 từ (mảnh bảng GRADE \"HAZ 9 RCTs No serious\", mảnh lưu đồ, dòng mục lục).",
          "6. **Trùng nguyên văn**: giữ chunk có `chunk_id` nhỏ nhất, các bản khác `duplicate_content_of:<chunk_id>` "
          "(mẫu CDC milestones lặp ở nhiều trang tuổi, thông báo NIH, câu lặp trong sổ tay WHO).",
          "7. Cấp tài liệu/nguồn: cách ly; không thuộc nhóm; `source_url` sai định dạng.",
          "",
          "Chunk tốt và xấu trong cùng tài liệu: chỉ loại chunk xấu. `clinical_reviewed` không đổi (false).", "",
          "## 5. Kiểm tra preflight", "| Kiểm tra | Số vi phạm |", "|---|---:|"]
    for k, v in checks.items():
        L.append(f"| {k} | {v} {'✔' if not v else '✘'} |")
    for p in trace_problems:
        L.append(f"- {p}")
    L += ["",
          "Truy vết: mọi tài liệu có chunk là bản hiện hành; file corpus tồn tại và SHA-256 khớp "
          "`documents.file_sha256`; mỗi chunk có `source_id`, `document_id`, URL, trang (PDF) hoặc khoảng ký tự.", "",
          "## 6. Cổng quyền đang chặn",
          f"`v_embedding_eligible_documents` (production) cho qua **{gate_docs}** tài liệu. "
          "Lý do chặn (số tài liệu):", "",
          "| Điều kiện | Tài liệu |", "|---|---:|"]
    for k, v in gate_reasons.most_common():
        L.append(f"| `{k}` | {v} |")
    L += ["",
          "Không ghi `*_allowed = true`, không duyệt nội dung, không sửa view production. "
          "Cơ chế nghiên cứu tách riêng (migration 006) được mô tả trong "
          "[embedding_research_gate_proposal_2026-11-14.md](embedding_research_gate_proposal_2026-11-14.md).", "",
          "## 7. File", "| File | SHA-256 |", "|---|---|"]
    for n, h in digests.items():
        L.append(f"| [{n}]({n}) | `{h}` |")
    (REPORTS / "embedding_preflight_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(json.dumps({"ok": preflight_ok, "groups": {g: per_group[g] for g in "ABC"}, "union_sources": len(union),
                      "eligible_chunks": len(manifest), "eligible_sources": len({m["source_id"] for m in manifest}),
                      "tokens": total_tokens, "batches": len(batches), "max_payload_kib": max(payload_bytes) // 1024,
                      "excluded": dict(reason_counts), "checks": checks, "digests": digests,
                      "api_calls_estimate": math.ceil(len(manifest) / profile.max_texts_per_call)},
                     ensure_ascii=False, indent=1))
    return 0 if preflight_ok else 1


if __name__ == "__main__":
    sys.exit(main())
