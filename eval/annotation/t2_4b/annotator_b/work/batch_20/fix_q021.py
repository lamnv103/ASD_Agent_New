import json
import os
import sys

sys.path.insert(0, 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_20')
from verify_question import get_question_passages
passages = get_question_passages('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_20.jsonl', 'q021')

# Load previous annotations from write_q021
from write_q021 import annotations_q021

# Fix evidence spans to be exact substrings of passages
fixes = {
    '19C7D4B5CF': 'His behaviour is getting worse anyway.”',
    '6CDDA56B42': 'This systematic review provides preliminary evidence on the effectiveness of remotely delivered parent-mediated intervention training.',
    '1AB1F82F85': 'Maya’s mother should avoid stopping the activity when Maya is whining. If she stops braiding when Maya is whining, it will make it more likely that Maya will whine in future.',
    '91E7089759': 'Find out the reason for your child’s challenging behaviour and decide how to respond based on that reason (to get access or attention, to avoid or to get a sensation).',
    '7D37DB0FEB': 'Ignore behaviour if it is safe and OK to do so.',
    '0C9915D78B': 'Find out the reason for your child’s challenging behaviour and decide how to respond based on that reason (to get access or attention, to avoid or to get a sensation)',
    '812AB7A5F4': 'What happened immediately after the behaviour?',
    '6A42C35638': 'If Anna’s father comes over to tell Anna to be quiet, this gives her attention and even negative attention can be a reward for a child.',
    'AFD04D85D5': 'Children learn best when they are calm and cool.',
    '00A80947AD': 'If your child has a “meltdown” or “tantrum”, stay calm and wait for the child to calm down.',
}

for item in annotations_q021:
    code = item['annotation_code']
    if code in fixes:
        item['evidence_span'] = fixes[code]
        
outpath = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_20/q021.jsonl'
with open(outpath, 'w', encoding='utf-8') as f:
    for ann in annotations_q021:
        f.write(json.dumps(ann, ensure_ascii=False) + '\n')
print(f'Updated {len(annotations_q021)} annotations in q021.jsonl')
