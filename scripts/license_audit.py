"""Write the licence review matrix (CSV) and audit report (MD) for the 73 corpus documents.

Read-only with respect to the database and data/raw. No network calls.

Usage:
  python -B scripts/license_audit.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import CORPUS_MANIFEST, RAW_CATALOG, REPORTS, ROOT
from app.rights.license_audit import ACTIONS, assess, collect

PROVIDER_TERMS = ROOT / "docs" / "provider_terms" / "cohere_2026-11-14.md"
COHERE_KEY_IS_TRIAL = True  # verified 2026-11-14 from response headers; see PROVIDER_TERMS
FIELDS = ["source_id", "title", "license_name", "license_version", "license_url", "rights_holder", *ACTIONS,
          "evidence_url", "verification_status", "verified_by", "verified_at", "review_notes",
          "catalog_rights_status", "catalog_label_matches_license", "evidence_location", "evidence_checked_at",
          "license_statement"]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def label_matches(catalog_status: str, license_name: str) -> str:
    nc_label = catalog_status == "verified_noncommercial_research"
    nc_license = "NC" in license_name
    if nc_label == nc_license:
        return "yes"
    return "no: catalog label stricter than licence" if nc_label else "no: licence is NC but label is not"


def main() -> int:
    today = date.today().isoformat()
    raw = {r["source_id"]: r for r in load_jsonl(RAW_CATALOG)}
    rows = []
    for m in sorted(load_jsonl(CORPUS_MANIFEST), key=lambda r: r["source_id"]):
        record = raw[m["source_id"]]
        ev = collect(record, m, ROOT)
        status = (record.get("rights") or {}).get("status") or ""
        rows.append({
            "source_id": ev.source_id, "title": ev.title, "license_name": ev.license_name,
            "license_version": ev.license_version, "license_url": ev.license_url, "rights_holder": ev.rights_holder,
            **assess(ev, cohere_blocks_nc=COHERE_KEY_IS_TRIAL),
            "evidence_url": ev.evidence_url, "verification_status": ev.verification_status,
            "verified_by": "", "verified_at": "",  # filled only by the accountable reviewer
            "review_notes": "; ".join(ev.notes), "catalog_rights_status": status,
            "catalog_label_matches_license": label_matches(status, ev.license_name),
            "evidence_location": ev.evidence_location, "evidence_checked_at": today,
            "license_statement": ev.statement,
        })

    REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = REPORTS / "license_review_matrix.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md_path = REPORTS / f"license_audit_{today}.md"
    md_path.write_text(render(rows, today), encoding="utf-8")
    summary = {"documents": len(rows), "by_license": dict(Counter(r["license_name"] for r in rows)),
               "by_verification": dict(Counter(r["verification_status"] for r in rows)),
               "label_mismatches": sum(r["catalog_label_matches_license"] != "yes" for r in rows),
               "csv": csv_path.relative_to(ROOT).as_posix(), "report": md_path.relative_to(ROOT).as_posix()}
    print(json.dumps(summary, indent=1))
    return 0


def _ids(rows: list[dict]) -> str:
    return ", ".join(f"`{r['source_id']}`" for r in rows) or "—"


def render(rows: list[dict], today: str) -> str:
    nc_label = [r for r in rows if r["catalog_rights_status"] == "verified_noncommercial_research"]
    rest = [r for r in rows if r not in nc_label]
    by = Counter((r["license_name"], r["license_version"]) for r in rows)
    lines = [
        f"# License & rights audit — {today}", "",
        "Phạm vi: 73 tài liệu toàn văn (core 33 + gaps 40). Không ghi DB, không gửi nội dung ra ngoài. "
        "Đây là thu thập bằng chứng kỹ thuật, **không phải tư vấn pháp lý**; mọi cờ quyền trong DB vẫn NULL "
        "cho tới khi chủ dự án phê duyệt.", "",
        "Ma trận chi tiết: [license_review_matrix.csv](license_review_matrix.csv) (1 dòng / source_id).", "",
        "## 1. Giấy phép theo bằng chứng trong bản gốc", "",
        "| Giấy phép | Phiên bản | Số tài liệu |", "|---|---|---:|",
        *[f"| {n} | {v or '—'} | {c} |" for (n, v), c in sorted(by.items())], "",
        "| Trạng thái bằng chứng | Số |", "|---|---:|",
        *[f"| {k} | {v} |" for k, v in Counter(r["verification_status"] for r in rows).most_common()], "",
        "- `evidence_in_original_document`: câu giấy phép đọc được trong file gốc (JATS `<license>`, câu public "
        "domain trong HTML của NIH, trang giấy phép trong PDF).",
        "- `agency_policy_only`: trang đã lưu không có câu giấy phép; chỉ có chính sách chung của cơ quan "
        "(CDC: \"most of the information … is in the public domain\"; NIDCD: \"unless otherwise stated … public "
        "domain\"). Chưa kiểm tra nội dung bên thứ ba từng trang.", "",
        f"## 2. 48 tài liệu mang nhãn `verified_noncommercial_research` ({len(nc_label)})", "",
    ]
    for name in sorted({r["license_name"] for r in nc_label}):
        group = [r for r in nc_label if r["license_name"] == name]
        lines.append(f"- **{name}** ({len(group)}): {_ids(group)}")
    lines += [
        "",
        "Kết luận: nhãn catalog chặt hơn giấy phép ở các tài liệu CC BY — giấy phép CC BY cho phép cả sử dụng "
        "thương mại. Nhãn này có thể là chính sách dự án có chủ đích; audit **không tự đổi nhãn**, chỉ ghi "
        "`catalog_label_matches_license` trong CSV. Đề xuất: lưu `license_type` thật vào DB (migration 004) và để "
        "chủ dự án quyết định có giữ chính sách phi thương mại cho toàn kho hay không.", "",
        f"## 3. {len(rest)} tài liệu còn lại", "",
    ]
    for name in sorted({r["license_name"] for r in rest}):
        group = [r for r in rest if r["license_name"] == name]
        lines.append(f"- **{name}** ({len(group)}): {_ids(group)}")
    lines += ["", "## 4. Đánh giá theo từng hành động (chỉ theo giấy phép)", "",
              "| Hành động | " + " | ".join(sorted({r["license_name"] for r in rows})) + " |",
              "|---|" + "---|" * len({r["license_name"] for r in rows})]
    for action in ACTIONS:
        cells = []
        for name in sorted({r["license_name"] for r in rows}):
            values = Counter(r[action] for r in rows if r["license_name"] == name)
            cells.append(", ".join(f"{k} ({v})" for k, v in values.most_common()))
        lines.append(f"| `{action}` | " + " | ".join(cells) + " |")
    blocked = [r for r in rows if r["cohere_processing_allowed"] == "blocked"]
    conflicts = [r for r in rows if r["verification_status"] in ("conflict", "unknown")]
    lines += [
        "", "Ghi chú: ShareAlike chỉ phát sinh nghĩa vụ khi **chia sẻ** bản chuyển thể; chunk/embedding nội bộ "
        "không chia sẻ ra ngoài. Public domain của cơ quan Mỹ không cấp quyền dùng logo/hình ảnh bên thứ ba và "
        "yêu cầu không ngụ ý xác nhận (endorsement).", "",
        "## 5. Danh sách BLOCKED / chưa xác minh", "",
        f"- `cohere_processing_allowed = blocked` ({len(blocked)}): {_ids(blocked)} — lý do: giấy phép NC + trial "
        "key chịu Terms of Use cho phép Cohere dùng dữ liệu cải thiện dịch vụ.",
        f"- Xung đột/không rõ bằng chứng ({len(conflicts)}): {_ids(conflicts)}",
        "- `external_llm_processing_allowed`: `pending_decision` cho cả 73 — chưa chọn nhà cung cấp LLM nên chưa "
        "có điều khoản để đối chiếu.",
        "- `verified_by` / `verified_at` để trống: chưa có người chịu trách nhiệm phê duyệt.", "",
        PROVIDER_TERMS.read_text(encoding="utf-8").strip(), "",
        "## 6. Việc cần chủ dự án quyết định", "",
        "1. Giữ hay bỏ chính sách \"phi thương mại cho toàn kho\" với 35 tài liệu CC BY.",
        "2. Phương án Cohere (production key + opt-out / ZDR / chỉ embed tài liệu không-NC / embedding local).",
        "3. Chấp nhận mức bằng chứng `agency_policy_only` (17 trang CDC + 1 trang NIDCD), hay yêu cầu kiểm tra "
        "từng trang.",
        "4. Sau khi quyết định: ghi `*_allowed`, `verified_by`, `verified_at` bằng role owner (một lệnh SQL có "
        "kiểm toán cho mỗi nhóm), rồi chạy lại `scripts/db_check.py`.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
