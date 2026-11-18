import sys
import json
sys.path.insert(0, 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_20')
from verify_question import get_question_passages
passages = get_question_passages('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_20.jsonl', 'q030')

# Let's inspect each candidate
for code, text in passages.items():
    print(f"=== {code} ===")
    print(text[:300])
    print("...\n")
