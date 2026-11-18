import json, re

qs = {
    "q008": r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_15/q008.txt",
    "q059": r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_15/q059.txt",
    "q048": r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_15/q048.txt",
}

for qid, srcpath in qs.items():
    with open(srcpath, encoding="utf-8") as f:
        src = f.read()
    # split into candidate blocks by "### CODE |"
    blocks = {}
    parts = re.split(r"\n### ([0-9A-F]{10}) \| ", src)
    # parts[0] is header; then alternating code, content
    for i in range(1, len(parts), 2):
        code = parts[i]
        content = parts[i+1]
        blocks[code] = content

    outpath = rf"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_15/{qid}.jsonl"
    seen = set()
    n = 0
    problems = []
    with open(outpath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            n += 1
            code = obj["annotation_code"]
            if code in seen:
                problems.append(f"DUPLICATE {code}")
            seen.add(code)
            span = obj.get("evidence_span", "")
            if obj["grade"] in (1,2,3,-1):
                if not span:
                    problems.append(f"{code}: missing evidence_span for grade {obj['grade']}")
                else:
                    content = blocks.get(code, "")
                    if span not in content:
                        problems.append(f"{code}: span not found verbatim: {span!r}")
            if obj["grade"] == 0 and span:
                problems.append(f"{code}: grade 0 should have empty span")

    missing = set(blocks.keys()) - seen
    extra = seen - set(blocks.keys())
    print(f"{qid}: candidates={len(blocks)} labeled={n} missing={missing} extra={extra}")
    if problems:
        print("  PROBLEMS:")
        for p in problems:
            print("   -", p)
    else:
        print("  OK, no problems")
