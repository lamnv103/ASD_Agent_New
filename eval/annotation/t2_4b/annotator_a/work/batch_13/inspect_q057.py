import json

with open('eval/annotation/t2_4b/annotator_a/batches/batch_13.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data['question_id'] == 'q057':
            cands = data['candidates']
            print(f'Total candidates: {len(cands)}')
            for i, c in enumerate(cands):
                text = c['content'].lower()
                has_vax = any(k in text for k in ['vaccin', 'vắc-xin', 'tiêm', 'mmr', 'immuniz'])
                has_cause = any(k in text for k in ['cause', 'etiolog', 'nguyên nhân', 'nguy cơ', 'risk factor'])
                print(f"{i}: {c['annotation_code']} | vax:{has_vax} | cause:{has_cause} | doc:{c['doc_title'][:25]} | sec:{c['section_title'][:25]}")
                if has_vax:
                    print(f"   -> MATCH VAX in {c['annotation_code']}")

