import json, io, re, sys

work_dir = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_18"
ret_dir = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_18"

questions = ["q046", "q051", "q044", "q005"]

problems = []
summary = {}

for q in questions:
    txt_path = f"{work_dir}/{q}.txt"
    with io.open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # split into candidate blocks by "### CODE | ..."
    parts = re.split(r"\n### ([0-9A-Fa-f]{10}) \| ", content)
    # parts[0] is header text before first match; then alternating code, body
    blocks = {}
    for i in range(1, len(parts), 2):
        code = parts[i]
        body = parts[i+1]
        # body includes "Title | Section | page -\nACTUAL CONTENT..."
        # strip up to first newline (the rest of header line) to get content
        nl = body.find("\n")
        passage = body[nl+1:] if nl != -1 else ""
        # trim trailing part before next candidate (already split) - also remove trailing blank
        blocks[code] = passage

    jsonl_path = f"{ret_dir}/{q}.jsonl"
    rows = []
    with io.open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    codes_seen = {}
    for r in rows:
        c = r["annotation_code"]
        codes_seen[c] = codes_seen.get(c, 0) + 1

    # check duplicates
    dups = [c for c, n in codes_seen.items() if n > 1]
    if dups:
        problems.append(f"{q}: duplicate codes {dups}")

    # check all candidate codes covered
    missing = [c for c in blocks if c not in codes_seen]
    if missing:
        problems.append(f"{q}: missing labels for {missing}")

    extra = [c for c in codes_seen if c not in blocks]
    if extra:
        problems.append(f"{q}: labeled codes not in candidate set {extra}")

    # check evidence_span substring
    grade_counts = {}
    needs_review_count = 0
    for r in rows:
        g = r.get("grade")
        grade_counts[g] = grade_counts.get(g, 0) + 1
        if r.get("needs_review"):
            needs_review_count += 1
        span = r.get("evidence_span", "")
        code = r["annotation_code"]
        if span:
            passage = blocks.get(code, "")
            if span not in passage:
                problems.append(f"{q}/{code}: evidence_span not found verbatim: {span!r}")

    summary[q] = {
        "n_candidates": len(blocks),
        "n_labeled": len(rows),
        "grade_counts": grade_counts,
        "needs_review": needs_review_count,
    }

print(json.dumps(summary, ensure_ascii=False, indent=2))
if problems:
    print("PROBLEMS:")
    for p in problems:
        print(" -", p)
else:
    print("NO PROBLEMS FOUND")
