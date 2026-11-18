import os
import json
import sys

sys.path.insert(0, 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_20')
from verify_question import verify_question

questions = ['q021', 'q030', 'q047']
total_counts = {}
all_grades = {}
total_needs_review = 0

for qid in questions:
    ok = verify_question(qid)
    if not ok:
        print(f"Verification FAILED for {qid}")
        sys.exit(1)
        
    returned_file = os.path.join(r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_20", f"{qid}.jsonl")
    count = 0
    with open(returned_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            count += 1
            g = item.get('grade')
            all_grades[g] = all_grades.get(g, 0) + 1
            if item.get('needs_review'):
                total_needs_review += 1
    total_counts[qid] = count

print("\n=== FINAL AUDIT SUMMARY FOR BATCH_20 ===")
print("Questions and pair counts:", total_counts)
print("Total pairs annotated:", sum(total_counts.values()))
print("Grade distribution across all questions:", dict(sorted(all_grades.items(), key=lambda x: str(x[0]))))
print("Total needs_review:", total_needs_review)
