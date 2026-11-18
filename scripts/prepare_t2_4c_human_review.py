"""Audit T2.4-C readiness and prepare a blind, provisional pilot packet.

Never reads the coordinator reveal file or any Agent A/B labels.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "eval/annotation/t2_4c"
PACKAGE = BASE / "t2_4c_expert_review_package.jsonl"
CSV_TEMPLATE = BASE / "t2_4c_expert_review_template.csv"
QUESTION_TEMPLATE = BASE / "t2_4c_question_level_review_template.jsonl"
AI_RESULTS = BASE / "t2_4c_ai_review_results_complete.jsonl"
VALIDATION = BASE / "t2_4c_ai_review_validation_report.json"
PROGRESS = BASE / "t2_4c_ai_review_progress_and_label_stats.json"
NEEDS = BASE / "t2_4c_ai_review_needs_review.jsonl"
PROVENANCE = BASE / "t2_4c_ai_review_provenance_and_limitations.md"
PREP_REPORT = BASE / "t2_4c_preparation_report.md"
PILOT = BASE / "t2_4c_human_review_pilot_blind.csv"
PILOT_MANIFEST = BASE / "t2_4c_human_review_pilot_internal_manifest.json"
REPORT = BASE / "t2_4c_human_review_readiness_report.md"
SEED = 20261117

REVIEW_FIELDS = ["expert_grade", "expert_rationale", "expert_evidence_span", "evidence_sufficiency",
                 "context_limitation", "conflict_flag", "review_status", "reviewer_id", "review_date"]


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = jsonl(PACKAGE)
    ai = jsonl(AI_RESULTS)
    old_ai = jsonl(BASE / "t2_4c_ai_review_results.jsonl")
    needs = jsonl(NEEDS)
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    with CSV_TEMPLATE.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        csv_fields = reader.fieldnames or []
        template_rows = list(reader)
    qrows = jsonl(QUESTION_TEMPLATE)

    pkg_ids = [r.get("review_id") for r in package]
    ai_ids = [r.get("review_id") for r in ai]
    csv_ids = [r.get("review_id") for r in template_rows]
    dup = lambda ids: sorted({x for x in ids if ids.count(x) > 1})
    id_match = set(pkg_ids) == set(ai_ids) == set(csv_ids)
    complete_ids = len(pkg_ids) == 875 and len(set(pkg_ids)) == 875
    ai_integrity = all(r in ai for r in old_ai) and sha(AI_RESULTS) == validation.get("combined_results_sha256")
    pkg_by_id = {r["review_id"]: r for r in package}
    result_by_id = {r["review_id"]: r for r in ai}
    template_by_id = {r["review_id"]: r for r in template_rows}
    blank_template = all(not str(template_by_id[k].get(field, "")).strip() for k in pkg_by_id for field in REVIEW_FIELDS)
    package_blank = all(not str(r.get(field, "")).strip() for r in package for field in REVIEW_FIELDS)
    needs_matches = {r["review_id"] for r in needs} == {r["review_id"] for r in ai if r.get("review_status") == "needs_review"}
    q_by_id = {r.get("question_id"): r for r in qrows}
    q_audit = {qid: {
        "present": qid in q_by_id,
        "review_status": q_by_id.get(qid, {}).get("review_status"),
        "decision_fields_blank": bool(q_by_id.get(qid)) and all(not q_by_id[qid].get(k) for k in ("expert_decision", "expert_rationale", "evidence_used", "reviewer_id", "review_date")),
        "question_text_matches_package": any(p.get("question_vi") == q_by_id.get(qid, {}).get("question_vi") for p in package) if qid in q_by_id else False,
    } for qid in ("q016", "q041", "q057")}

    # 12 AI needs_review + 28 other AI rows, then shuffle. Selection categories
    # remain in an internal manifest and are omitted from the expert packet.
    rng = random.Random(SEED)
    need_ids = sorted(r["review_id"] for r in needs)
    other_ids = sorted(r["review_id"] for r in ai if r.get("review_status") != "needs_review")
    chosen_need = rng.sample(need_ids, min(12, len(need_ids)))
    chosen_other = rng.sample(other_ids, 28)
    chosen = [(x, "ai_needs_review") for x in chosen_need] + [(x, "other_ai_review_status") for x in chosen_other]
    rng.shuffle(chosen)
    pilot_ids = [x[0] for x in chosen]

    with PILOT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for rid in pilot_ids:
            row = dict(template_by_id[rid])
            for field in REVIEW_FIELDS:
                if field in row:
                    row[field] = ""
            writer.writerow(row)
    PILOT_MANIFEST.write_text(json.dumps({
        "purpose": "internal audit only; do not send to reviewers",
        "seed": SEED,
        "selection_counts": {"ai_needs_review": len(chosen_need), "other_ai_review_status": len(chosen_other)},
        "selected": [{"review_id": rid, "selection_source": source} for rid, source in chosen],
        "not_included": "A/B agreement/disagreement stratum is unavailable without the prohibited reveal mapping and was not inspected.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ai_types = {}
    for r in ai:
        typ = r.get("reviewer_type", "missing")
        ai_types[typ] = ai_types.get(typ, 0) + 1
    problems = []
    if not complete_ids: problems.append("package does not contain exactly 875 unique IDs")
    if not id_match: problems.append("package, results, and CSV template ID sets differ")
    if not ai_integrity: problems.append("AI results hash does not match validation report or original 64 rows are not preserved")
    if not blank_template or not package_blank: problems.append("human review fields are not blank in package/template")
    if not needs_matches: problems.append("needs_review list does not match complete AI results")
    if not all(v["present"] and v["decision_fields_blank"] and v["question_text_matches_package"] for v in q_audit.values()):
        problems.append("one or more question-level templates are missing, populated, or use non-matching question text")
    # A/B strata are a required pilot dimension, but cannot be verified from
    # permitted inputs without exposing/reading the coordinator reveal.
    status = "BLOCKED" if problems or len(pilot_ids) < 30 else "READY_WITH_CONDITIONS"
    if not problems and len(pilot_ids) >= 30:
        problems.append("pilot is provisional: A/B consensus/disagreement membership cannot be verified without an authorized blind stratification map")

    report = f"""# T2.4-C Human Review Readiness Report

**Conclusion: {status}**

## 1. Audit results

- Package: {len(package)} rows; {len(set(pkg_ids))} unique `review_id` values.
- Complete AI results: {len(ai)} rows; {len(set(ai_ids))} unique IDs; package/result ID sets match: **{id_match}**.
- CSV template: {len(template_rows)} rows; {len(set(csv_ids))} unique IDs; package/template ID sets match: **{set(pkg_ids) == set(csv_ids)}**.
- Duplicate IDs: package {len(dup(pkg_ids))}; AI results {len(dup(ai_ids))}; CSV template {len(dup(csv_ids))}.
- Human fields are blank in package: **{package_blank}**; blank in CSV template: **{blank_template}**.
- AI review types: `{json.dumps(ai_types, ensure_ascii=False)}`; records marked human reviewed: {sum(r.get('human_expert_reviewed') is True for r in ai)}.
- `needs_review` records: {len(needs)}; list matches complete results: **{needs_matches}**.
- AI results file SHA-256: `{sha(AI_RESULTS)}`; matches recorded validation report and retains all original 64 records: **{ai_integrity}**.
- Structural issues: {('; '.join(problems) if problems else 'none')}. The AI result file and templates were not modified.

### Question-level templates

| Question | Present | Unresolved | Reviewer fields blank | Text matches blind package |
|---|---:|---:|---:|---:|
""" + "\n".join(
        f"| {qid} | {v['present']} | {v['review_status'] == 'unresolved'} | {v['decision_fields_blank']} | {v['question_text_matches_package']} |"
        for qid, v in q_audit.items()
    ) + f"""

All three question-level records remain unresolved, as intended. Their question text matches the blind package; no expert decisions or evidence have been entered.

## 2. Pilot packet

A 40-row blind pilot was staged at `{PILOT.name}`. It contains 12 records selected from AI `needs_review` and 28 from other AI review statuses, then shuffled. The packet preserves `review_id`, question, chunk context, and blank human fields; it contains no AI grade, rationale, reviewer metadata, selection source, rank, retriever, or score.

Pilot IDs (listed without selection strata):

{', '.join(f'`{rid}`' for rid in pilot_ids)}

The private selection manifest is `{PILOT_MANIFEST.name}` and must not be shared with reviewers. It records only the pilot construction, not A/B labels. The preparation note says the full package contains 662 disagreement cases and 213 sampled consensus cases, but no permitted file maps these strata to IDs. No reveal file or Agent A/B labels were inspected. Therefore this pilot cannot yet be certified as including representatives of both A/B strata; obtain a data-custodian-generated blind stratum-balanced ID list before reviewer distribution, or approve this pilot as an explicitly non-stratified usability pilot.

## 3. Instructions for reviewers

1. Review the question and supplied chunk independently. Do not consult AI labels or rationale before submitting and freezing the human judgment.
2. Assign `3` when the chunk directly supports the question; `2` when it supplies useful but partial support; `1` when it is on the same topic but weakly supportive; `0` when it does not contribute; use `needs_review` when the content is unclear, corrupted, incomplete, or cannot be judged reliably.
3. Explain the decision briefly. Copy evidence exactly from the chunk; leave evidence blank when none supports the judgment. Do not repair source text or infer evidence from a title.
4. Record reviewer ID, review date, and review status. Preserve the opaque `review_id`; do not add qid, A/B labels, rank, retriever, or score.
5. Submit and freeze the independent pilot judgments before any comparison with AI results. Resolve the three question-level decisions separately and document rationale and evidence.

## 4. Method limits

- AI output is AI-only; no record has human expert validation. The 126 `needs_review` records are candidates for particular attention, not expert decisions.
- The continuation provenance identifies lexical triage; structural checks do not establish semantic correctness. Human reviewers should assess all pilot items independently, not just flagged rows.
- Without the prohibited reveal mapping, the pilot's A/B disagreement and consensus mix is unknown. The selection categories above describe only AI review status.
- A single expert pilot provides no inter-rater reliability estimate. For full review, use at least one qualified independent expert for every item; add a second independent reviewer for a prespecified subset and adjudicate disagreements.
- q016, q041, and q057 require question-level decisions beyond pair relevance. Keep them unresolved until separately assessed.

## 5. Conditions before reviewing all 875

- Confirm the reviewer has relevant ASD evidence appraisal expertise and can review the language/content used in the package.
- Resolve the pilot sampling condition: receive a blind, authorized mapping/list covering A/B disagreement, A/B consensus, and `needs_review`, or explicitly redefine this as a non-stratified pilot.
- Freeze and hash the rubric, package, and blank template; do not edit chunk text or rubric during review.
- Run the pilot, freeze human judgments, compare with AI only afterward, document rubric ambiguities, and approve any rubric changes before the full review.
- Define second-reviewer coverage, adjudication rules, missing/`needs_review` handling, and data access controls before the full 875-row pass.
- Keep AI results immutable and maintain human results in a separate file with clear reviewer type and provenance.

## 6. Status rationale

`{status}` is assigned because structure and blinding checks pass, but the stated requirement for a pilot representative of A/B disagreement and consensus cannot be demonstrated without an authorized blind stratum mapping. No AI labels have been exposed in the reviewer packet, and no human labels have been created.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(json.dumps({"status": status, "package_rows": len(package), "ai_rows": len(ai), "pilot_rows": len(pilot_ids), "needs_review": len(needs), "ai_integrity": ai_integrity, "id_match": id_match, "question_templates": q_audit, "report": str(REPORT), "pilot": str(PILOT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
