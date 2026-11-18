import json

with open('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_a/batches/batch_20.jsonl', 'r', encoding='utf-8') as f:
    items_q023 = [json.loads(l) for l in f if json.loads(l)['question_id'] == 'q023']

item_map = {it['annotation_code']: it['content'] for it in items_q023}

# Question q023: Sở thích hạn hẹp có ảnh hưởng đến việc học không?
# Does restricted interests affect learning?
# Look at BD341B7D8A: "Cognitive diversity is increasingly emphasized. Monotropism theory suggests deep, sustained focus on restricted domains, explaining both restricted interests and exceptional skills [50]. Systemizing theory highlights strengths in rule-based reasoning and pattern detection, while empathizing-systemizing imbalances explain sex differences and overlap with STEM achievement [51]." -> Grade 3!
# Look at CF2287B5D0: Laila's mother uses her interest in the elephant in the book to engage her and teach her ("shared engagement"). -> Grade 2.
# Look at 6F8BC92317: "restricted or repetitive behaviors or interests. People with ASD may also have different ways of learning, moving, or paying attention." -> Grade 2.
# Look at 2526443327: "People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests. * People with ASD may also have different ways of learning, moving, or paying attention." -> Grade 2.
# Look at BD484F11D2: "Autism spectrum disorder (ASD) is a neurological and developmental disorder that affects how people interact with others, communicate, learn, and behave." -> Grade 1.
# Look at CDDF119B47: Examples of restricted/repetitive behaviors, lasting intense interest in specific topics like numbers, details or facts. -> Grade 2.
# Look at A009F8D9A3: "Having lasting, intense interest in specific topics, such as numbers, details, or facts" -> Grade 2.
# Look at 84FC8ABB1D: DSM-5 criterion B3: "Highly restricted, fixated interests that are abnormal in intensity or focus (e.g., strong attachment to or preoccupation with unusual objects, excessively circumscribed or perseverative interests)." -> Grade 1.
# Look at E3D107BDAB: fixation on socially irrelevant sounds influencing communication and participation. -> Grade 1.

test_spans = {
    "E3D107BDAB": "Together, enhanced sensitivity or fixation on socially irrelevant sounds, and a reduced tendency to attend to socially important ones such as speech, likely influence communication abilities and social participation",
    "CF2287B5D0": "Laila’s mother tries again. She notices Laila looking at an elephant in the book. Laila’s mother shows Laila the elephant and says, “We have an elephant!” Laila watches this time.",
    "84FC8ABB1D": "3. Highly restricted, fixated interests that are abnormal in intensity or focus (e.g., strong attachment to or preoccupation with unusual objects, excessively circumscribed or perseverative interests).",
    "BD484F11D2": "Autism spectrum disorder (ASD) is a neurological and developmental disorder that affects how people interact with others, communicate, learn, and behave.",
    "A009F8D9A3": "Having lasting, intense interest in specific topics, such as numbers, details, or facts",
    "CDDF119B47": "Having lasting, intense interest in specific topics, such as numbers, details, or facts",
    "399BBC4ED8": "tickling, a favourite routine (such as peekaboo, or swinging in the air). ƒ Sometimes, you can choose to give your child a small “prize” for trying to learn a new skill",
    "6F8BC92317": "People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests. People with ASD may also have different ways of learning, moving, or paying attention.",
    "2526443327": "People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests.  * People with ASD may also have different ways of learning, moving, or paying attention.",
    "BD341B7D8A": "Monotropism theory suggests deep, sustained focus on restricted domains, explaining both restricted interests and exceptional skills [50]. Systemizing theory highlights strengths in rule-based reasoning and pattern detection"
}

for code, span in test_spans.items():
    if span not in item_map[code]:
        print(f"FAILED: {code}")
    else:
        print(f"OK: {code} (len {len(span)})")

