import sys
import os
import json
import subprocess

def get_question_passages(batch_file, qid):
    cmd = [
        r"D:/AI4LIFE/ASD_AGENT_FINALL/.venv/Scripts/python",
        "-B",
        r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/tools/show_question.py",
        batch_file,
        qid
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(f"show_question failed: {res.stderr}")
    
    text = res.stdout
    # Passages start with "### "
    parts = text.split("\n### ")
    passages = {}
    for p in parts[1:]:
        header_line = p.split("\n", 1)[0]
        content = p.split("\n", 1)[1] if "\n" in p else ""
        code = header_line.split("|")[0].strip()
        passages[code] = content.strip()
    return passages

def verify_question(qid):
    batch_file = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_20.jsonl"
    returned_file = os.path.join(r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_20", f"{qid}.jsonl")
    
    if not os.path.exists(returned_file):
        print(f"File not found: {returned_file}")
        return False
        
    passages = get_question_passages(batch_file, qid)
    print(f"Total passages from show_question for {qid}: {len(passages)}")
    
    labels = []
    seen_codes = set()
    with open(returned_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            labels.append(item)
            code = item.get("annotation_code")
            if code in seen_codes:
                print(f"ERROR: duplicate code {code} at line {line_num}")
                return False
            seen_codes.add(code)
            
    if seen_codes != set(passages.keys()):
        missing = set(passages.keys()) - seen_codes
        extra = seen_codes - set(passages.keys())
        print(f"ERROR: code mismatch! Missing: {missing}, Extra: {extra}")
        return False
        
    errors = 0
    for item in labels:
        code = item["annotation_code"]
        grade = item.get("grade")
        evidence = item.get("evidence_span", "")
        passage_content = passages[code]
        
        # Check required fields
        for k in ["annotation_code", "grade", "rationale", "evidence_span", "confidence", "needs_review", "review_note"]:
            if k not in item:
                print(f"ERROR: missing key {k} in {code}")
                errors += 1
                
        if item["needs_review"]:
            if grade is not None:
                print(f"ERROR: needs_review is true but grade is not null in {code}")
                errors += 1
            if not item.get("review_note"):
                print(f"ERROR: needs_review is true but review_note is empty in {code}")
                errors += 1
        else:
            if grade not in [-1, 0, 1, 2, 3]:
                print(f"ERROR: invalid grade {grade} in {code}")
                errors += 1
            if grade in [-1, 1, 2, 3]:
                if not evidence:
                    print(f"ERROR: non-zero grade {grade} has empty evidence_span in {code}")
                    errors += 1
                elif evidence not in passage_content:
                    print(f"ERROR: evidence_span is NOT verbatim substring in {code}!")
                    print(f"Evidence: {repr(evidence)}")
                    errors += 1
            elif grade == 0:
                if evidence != "":
                    print(f"ERROR: grade 0 has non-empty evidence_span in {code}")
                    errors += 1
                    
    if errors == 0:
        print(f"SUCCESS: {qid} verified cleanly ({len(labels)} items).")
        return True
    else:
        print(f"FAILED: {errors} errors found in {qid}.")
        return False

if __name__ == "__main__":
    qid = sys.argv[1] if len(sys.argv) > 1 else "q021"
    verify_question(qid)
