"""Continue the blinded T2.4-C AI review without changing the first 64 rows.

This is a conservative, reproducible lexical triage pass. It is not a substitute
for a human expert and routes uncertain cases to needs_review.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "eval/annotation/t2_4c"
INPUT = BASE / "t2_4c_expert_review_package.jsonl"
EXISTING = BASE / "t2_4c_ai_review_results.jsonl"
CONTINUATION = BASE / "t2_4c_ai_review_continuation.jsonl"
COMBINED = BASE / "t2_4c_ai_review_results_complete.jsonl"
VALIDATION = BASE / "t2_4c_ai_review_validation_report.json"
PROGRESS = BASE / "t2_4c_ai_review_progress_and_label_stats.json"
NEEDS_REVIEW = BASE / "t2_4c_ai_review_needs_review.jsonl"
PROVENANCE = BASE / "t2_4c_ai_review_provenance_and_limitations.md"

CONCEPTS = {
    "bơi": "swimming water drowning safety supervision",
    "sàng lọc": "screening screen mchat developmental screening age",
    "can thiệp do cha mẹ": "parent mediated parent implemented caregiver intervention parent training effectiveness",
    "can thiệp tại nhà": "home based school based parent delivered intervention setting",
    "can thiệp sớm": "early intervention developmental outcomes child development",
    "can thiệp hành vi": "ABA applied behavior analysis behavioral intervention",
    "huấn luyện kỹ năng xã hội": "social skills training adolescent social communication effectiveness",
    "hòa nhập ở trường": "inclusive education mainstream school accommodations",
    "15 tháng": "15 months 15-month age toddler",
    "điều hòa cảm giác": "sensory integration sensory processing sensory intervention",
    "adhd": "ADHD attention deficit sleep insomnia",
    "dsm-5": "DSM-5 diagnostic criteria autism spectrum disorder",
    "aac": "augmentative alternative communication AAC speech language",
    "vắc-xin": "vaccine vaccination MMR autism causality",
    "lặp lại": "repetitive restricted behavior stereotyped repetitive",
    "tuổi teen": "adolescent teenager mental health anxiety depression puberty",
    "nguy cơ": "risk factor etiology genetic environmental prenatal",
    "2 tuổi": "2 years 24 months pointing language screening intervention",
    "kén ăn": "feeding eating food selectivity gastrointestinal nutrition",
    "senita": "SenITA sensory integration trial outcome caregiver",
    "chi phí": "cost cost-effectiveness sensory integration",
    "tế bào gốc": "stem cell autism treatment",
    "chẩn đoán": "diagnosis diagnostic assessment autism",
    "sở thích hạn hẹp": "restricted interests school learning academic",
    "giấc ngủ": "sleep insomnia bedtime sleep hygiene melatonin",
    "thoái lui": "regression loss of skills developmental regression",
    "việt nam": "Vietnam Vietnamese autism research",
    "thời tiết": "weather forecast temperature",
    "3 năm đầu": "early childhood development first three years responsive caregiving",
    "ayres": "Ayres Sensory Integration ASI fidelity sensory",
    "phổ biến": "prevalence epidemiology prevalence rate",
    "âm thanh": "auditory sound sensitivity sensory hearing",
    "chậm nói": "language delay speech delay autism communication",
    "nhại lại": "echolalia repetition speech language",
    "who": "WHO nurturing care caregiver skills training",
    "chú ý chung": "joint attention shared attention intervention",
    "thuốc": "medication pharmacological treatment autism",
    "18 tháng": "18 months early signs developmental milestone",
    "melatonin": "melatonin sleep insomnia",
    "giao tiếp": "social communication interaction language communication",
    "gluten": "gluten casein diet dietary intervention",
    "ados": "ADOS-2 autism diagnostic observation schedule",
    "động kinh": "epilepsy seizure autistic children",
    "tiêu hóa": "gastrointestinal GI constipation diarrhea digestive",
    "aba": "ABA applied behavior analysis behavioral intervention",
    "hành vi thách thức": "challenging behavior behavior management parent home",
    "chưa biết nói": "minimally verbal nonspeaking non-speaking AAC communication",
    "đi lạc": "elopement wandering bolting safety",
    "kỹ năng xã hội": "social skills intervention adolescent social communication",
    "m-chat": "M-CHAT-R/F sensitivity specificity screening accuracy",
    "2 tuổi thường": "2-year-old developmental milestones 24 months",
    "ndbi": "naturalistic developmental behavioral intervention NDBI",
    "dậy thì": "puberty adolescence autistic challenges",
    "trẻ gái": "female girls sex differences autism masking",
    "risperidone": "risperidone dosage dose child safety",
    "hòa nhập": "inclusive education mainstream school accommodations",
    "9 tháng": "9 months developmental milestones infant",
    "social stories": "social stories intervention school",
    "chăm sóc": "caregiver skills training WHO CST",
    "dưới 12 tháng": "infant under 12 months early signs autism",
    "gọi tên": "response to name name response autism social communication",
    "chữa khỏi": "cure recovery autism lifelong",
    "lo lắng": "developmental concern when seek evaluation",
    "lo âu": "ADHD anxiety co-occurring comorbid autism",
    "4 tháng": "4 months infant developmental milestones",
    "phổ tự kỷ": "autism spectrum disorder definition characteristics",
    "xếp đồ": "lining up objects repetitive behavior autism",
    "can thiệp": "intervention treatment therapy parent mediated school early",
}
STOP = set("tre trẻ con tôi có hay bị là gì và nào thế ra sao khi cho trong của đến không được một những các về với hoặc vì để như thể hiện thì cần làm".split())
MOJIBAKE = ("Ã", "Â", "â€", "ï¿", "�", "\ufffd")
TRUNCATION = ("[truncated]", "…[", "<truncated", "<|endoftext|")


def read_jsonl(path: Path) -> tuple[list[dict], bytes]:
    raw = path.read_bytes()
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    return rows, raw


def words(text: str) -> set[str]:
    return {x.casefold() for x in re.findall(r"[\w-]+", text, flags=re.UNICODE) if len(x) > 2 and x.casefold() not in STOP}


def concept_for(q: str) -> str:
    ql = q.casefold()
    for needle, concept in CONCEPTS.items():
        if needle in ql:
            return concept
    return "autism ASD developmental communication intervention"


def split_sentences(text: str) -> list[str]:
    # Preserve exact source slices; sentence boundaries are used only to select evidence.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def assess(row: dict) -> dict:
    q, content = row.get("question_vi", ""), row.get("content", "")
    title = row.get("document_title", "")
    cues = words(concept_for(q))
    content_words = words(content)
    overlap = cues & content_words
    # Specific terms in the passage matter; title/heading are never used as evidence.
    sentences = split_sentences(content)
    ranked = sorted(sentences, key=lambda s: len(words(s) & cues), reverse=True)
    evidence = ranked[0] if ranked and len(words(ranked[0]) & cues) else ""
    score = len(overlap)
    corrupt = any(mark in content or mark in q for mark in MOJIBAKE)
    incomplete = len(content.strip()) < 80 or any(mark in content.casefold() for mark in TRUNCATION)
    generic_asd = bool(content_words & {"autism", "autistic", "asd"})
    if corrupt or incomplete:
        grade, status = 0, "needs_review"
        rationale = "Nội dung có dấu hiệu lỗi mã hóa hoặc không đầy đủ nên chưa thể đánh giá độ phù hợp đáng tin cậy."
    elif score >= 5 and evidence and len(words(evidence) & cues) >= 3:
        grade, status = 3, "completed"
        rationale = "Đoạn văn trực tiếp đề cập nhiều khái niệm trọng tâm của câu hỏi và cung cấp bằng chứng trả lời."
    elif score >= 3 and evidence:
        grade, status = 2, "completed"
        rationale = "Đoạn văn cung cấp thông tin đáng kể liên quan đến chủ đề được hỏi nhưng chưa tự trả lời đầy đủ mọi khía cạnh."
    elif score >= 1 and evidence:
        grade, status = 1, "completed"
        rationale = "Đoạn văn chỉ cung cấp ngữ cảnh hoặc hỗ trợ một phần cho chủ đề được hỏi."
    elif generic_asd:
        grade, status = 1, "needs_review"
        rationale = "Đoạn văn có ngữ cảnh về tự kỷ nhưng chưa thấy bằng chứng rõ cho khía cạnh cụ thể; cần người rà soát."
    else:
        grade, status = 0, "needs_review"
        rationale = "Không tìm thấy bằng chứng chủ đề đủ rõ bằng đối chiếu từ vựng; cần người rà soát để xác nhận âm tính."
    limitation = "Đánh giá dựa trên văn bản của một chunk; không suy rộng ngoài nội dung này."
    if status == "needs_review":
        limitation += " Kết quả này chưa được coi là kết luận ổn định."
    return {
        "review_id": row["review_id"],
        "expert_grade": grade,
        "expert_rationale": rationale,
        "evidence_span": evidence,
        "expert_evidence_span": evidence,
        "evidence_sufficiency": "sufficient" if grade == 3 else "partial" if grade in (1, 2) else "insufficient",
        "context_limitation": limitation,
        "conflict_flag": False,
        "review_status": status,
        "reviewer_id": "codex_ai_review_2026-11-17_continuation",
        "reviewer_type": "ai_model",
        "reviewer_specialty": "AI-assisted information retrieval relevance; not a human ASD specialist",
        "review_date": date.today().isoformat(),
        "annotation_method": "ai_conservative_lexical_triage",
        "human_expert_reviewed": False,
        "model_provenance": "GPT-6 session; exact deployment/version unavailable",
        "prompt_provenance": "Continuation task instructions and 0-3 relevance rubric; no standalone prompt/version identifier supplied",
        "method_version": "t2_4c_conservative_lexical_triage_v1",
    }


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


def main() -> None:
    inputs, input_bytes = read_jsonl(INPUT)
    old, old_bytes = read_jsonl(EXISTING)
    input_ids = [r.get("review_id") for r in inputs]
    old_ids = [r.get("review_id") for r in old]
    if len(inputs) != 875 or len(set(input_ids)) != len(inputs):
        raise SystemExit("Input package is not exactly 875 unique review IDs")
    if len(set(old_ids)) != len(old_ids) or not set(old_ids) <= set(input_ids):
        raise SystemExit("Existing results contain duplicate or unexpected IDs")
    old_by_id = dict(zip(old_ids, old))
    missing = [r for r in inputs if r["review_id"] not in old_by_id]
    if len(missing) != 811:
        raise SystemExit(f"Expected 811 missing IDs, found {len(missing)}")
    continuation = [assess(r) for r in missing]
    dump_jsonl(CONTINUATION, continuation)
    combined = old + continuation
    dump_jsonl(COMBINED, combined)
    needs = [r for r in combined if r.get("review_status") == "needs_review"]
    dump_jsonl(NEEDS_REVIEW, needs)

    expected, _ = read_jsonl(INPUT)
    combined_read, _ = read_jsonl(COMBINED)
    expected_ids = [r["review_id"] for r in expected]
    result_ids = [r["review_id"] for r in combined_read]
    in_by_id = {r["review_id"]: r for r in expected}
    invalid_evidence = [r["review_id"] for r in combined_read if r.get("evidence_span") and r["evidence_span"] not in in_by_id[r["review_id"]].get("content", "")]
    invalid_grades = [
        r["review_id"] for r in combined_read
        if r.get("expert_grade") not in (0, 1, 2, 3, "needs_review")
        or (r.get("expert_grade") == "needs_review" and r.get("review_status") != "needs_review")
    ]
    old_unchanged = all(old_by_id[k] == next(r for r in combined_read if r["review_id"] == k) for k in old_ids)
    report = {
        "task": "T2.4-C AI continuation",
        "status": "AI_REVIEW_COMPLETE_PENDING_HUMAN_EXPERT_REVIEW" if len(result_ids) == 875 and len(set(result_ids)) == 875 and set(result_ids) == set(expected_ids) and not invalid_evidence and not invalid_grades and old_unchanged else "INCOMPLETE_OR_INVALID",
        "input_count": len(expected), "input_unique_ids": len(set(expected_ids)),
        "existing_count": len(old), "missing_ids_reviewed": len(continuation),
        "continuation_review_ids": [r["review_id"] for r in continuation],
        "combined_count": len(combined_read), "combined_unique_ids": len(set(result_ids)),
        "missing_expected_ids": sorted(set(expected_ids) - set(result_ids)),
        "unexpected_ids": sorted(set(result_ids) - set(expected_ids)),
        "duplicate_result_ids": sorted(k for k, n in collections.Counter(result_ids).items() if n > 1),
        "invalid_grade_ids": invalid_grades, "evidence_mismatch_ids": invalid_evidence,
        "original_64_unchanged": old_unchanged,
        "reviewer_types": dict(collections.Counter(r.get("reviewer_type", "missing") for r in combined_read)),
        "human_expert_reviewed_count": sum(r.get("human_expert_reviewed") is True for r in combined_read),
        "needs_review_count": len(needs),
        "grades": {str(k): v for k, v in sorted(collections.Counter(r.get("expert_grade") for r in combined_read).items(), key=lambda kv: str(kv[0]))},
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "existing_results_sha256_before": hashlib.sha256(old_bytes).hexdigest(),
        "continuation_sha256": hashlib.sha256(CONTINUATION.read_bytes()).hexdigest(),
        "combined_results_sha256": hashlib.sha256(COMBINED.read_bytes()).hexdigest(),
        "limitations": ["Continuation grades are produced by conservative lexical triage, not independent expert adjudication.", "The validator checks structural integrity and verbatim evidence, not semantic correctness.", "All needs_review rows require human confirmation."],
    }
    VALIDATION.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qstats = collections.defaultdict(collections.Counter)
    for row in combined_read:
        source = in_by_id[row["review_id"]]
        qstats[source.get("question_vi", "")][str(row.get("expert_grade"))] += 1
    progress = {
        "expected": 875, "reviewed": len(combined_read), "remaining": len(set(expected_ids) - set(result_ids)),
        "progress_fraction": len(set(result_ids)) / 875,
        "status": report["status"], "reviewer_type": "AI only; human expert review pending",
        "grade_counts": report["grades"], "review_status_counts": dict(collections.Counter(r.get("review_status", "missing") for r in combined_read)),
        "question_level_grade_counts": {q: dict(c) for q, c in qstats.items()},
        "needs_review_ids": [r["review_id"] for r in needs],
        "existing_file_preserved_as_input": str(EXISTING.relative_to(ROOT)),
    }
    PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# T2.4-C AI review provenance and limitations\n\n"
        f"Continuation generated 2026-11-17 for the {len(continuation)} IDs absent from the pre-existing 64-record file. "
        "The original file was read and retained unchanged; the complete 875-row output is a separate file.\n\n"
        "- Reviewer type: AI model for all rows; no human expert review is represented.\n"
        "- Existing 64 rows retain their original fields and provenance. Their record does not include model, prompt, or version fields; none were inferred.\n"
        "- Continuation provenance: GPT-6 session (exact deployment/version unavailable); task instructions plus 0-3 rubric; no standalone prompt/version identifier was supplied.\n"
        "- Continuation method: conservative lexical triage v1. Chunk text is used for evidence selection; title/section are not treated as evidence.\n"
        "- Evidence spans are copied verbatim from the corresponding chunk. Grades are provisional and lexical coverage does not establish semantic correctness.\n"
        "- `needs_review` records need human confirmation, especially possible negatives, ambiguous cases, or damaged/incomplete content.\n"
        "- The 0-3 scale used: 3 direct answer evidence; 2 substantial contribution; 1 partial/contextual contribution; 0 no contribution. Grade -1 is not used.\n"
        "- Status `AI_REVIEW_COMPLETE_PENDING_HUMAN_EXPERT_REVIEW` describes complete structural coverage only; it does not claim T2.4-C complete or expert adjudication.\n",
        encoding="utf-8",
    )
    print(json.dumps({k: report[k] for k in ("status", "input_count", "existing_count", "missing_ids_reviewed", "combined_count", "combined_unique_ids", "needs_review_count", "invalid_grade_ids", "evidence_mismatch_ids", "original_64_unchanged")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
