"""Print every candidate of one question from a blind batch file (blind fields only).

usage: python show_question.py <batch_file.jsonl>                 list the questions in the batch
       python show_question.py <batch_file.jsonl> <question_id>   print that question's candidates in full
"""

import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
with open(sys.argv[1], encoding="utf-8") as f:
    rows = [json.loads(x) for x in f if x.strip()]
if len(sys.argv) < 3:
    seen: list[str] = []
    for r in rows:
        if r["question_id"] not in seen:
            seen.append(r["question_id"])
    for q in seen:
        items = [r for r in rows if r["question_id"] == q]
        print(q, len(items), items[0]["question_vi"])
    sys.exit(0)
items = [r for r in rows if r["question_id"] == sys.argv[2]]
if not items:
    sys.exit(f"no question {sys.argv[2]} in this batch")
print(f"QUESTION {sys.argv[2]}: {items[0]['question_vi']}  ({len(items)} candidates)\n")
for r in items:
    print(f"### {r['annotation_code']} | {r['document_title']} | {r['section']} | page {r['page'] or '-'}")
    print(r["content"])
    print()
