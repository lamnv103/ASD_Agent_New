# Instructions for ANNOTATOR B (AI annotator agent) — T2.4-B

You are ANNOTATOR B, an independent relevance annotator for a research evaluation of an autism (ASD) question-answering system for Vietnamese parents. You judge how well each document passage answers ONE specific question. Your labels are recorded as AI annotation (not human). Your batch number (NN) is given in your task message.

## Strict independence rules
- You may read ONLY:
  1. The guideline (read it fully first; Vietnamese; authoritative rubric): D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/annotation_guidelines_t2_4b_2026-11-15.md
  2. This instruction file.
  3. Your batch, ONLY through the helper:
     D:/AI4LIFE/ASD_AGENT_FINALL/.venv/Scripts/python -B D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/tools/show_question.py D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_NN.jsonl [question_id]
     (without question_id it lists the batch's questions; question ids are lowercase, e.g. q012).
  4. Files you yourself created inside your private work directory (below).
- Private work directory (the ONLY place for temporary files, e.g. saved helper output or label-writing scripts):
  D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_NN/
  Do NOT use your scratchpad, the system temp directory or any other directory. Do NOT open, list or search anything else (in particular nothing under eval/reports, eval/datasets, eval/annotation/t2_4b/coordinator, the other annotator's folder, other batches' work or returned folders, logs, data, scripts, and no temp/scratchpad directories).
- Do not use the web. Do not start other agents. Nobody has told you how the passages were found; do not try to infer it.

## Task
For EVERY question in your batch and EVERY candidate passage of that question (identified by its annotation code after "###"):
- Judge relevance to that exact question following the guideline rubric: 3 / 2 / 1 / 0 / -1 (conflicting). Read the whole passage; do not judge by title; keyword overlap is not relevance; no outside medical inference.
- If you genuinely cannot decide: "needs_review": true, "grade": null, and explain in "review_note". Do not guess.

## Output — one file per question, written right after finishing that question
D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_NN/<question_id>.jsonl
Valid JSONL, one object per candidate, covering ALL candidates of the question, exactly these keys:
{"annotation_code": "...", "grade": 2, "rationale": "...", "evidence_span": "...", "confidence": "high", "needs_review": false, "review_note": ""}
- grade: integer -1..3, or null only when needs_review is true.
- rationale: 1-2 short sentences in Vietnamese, checkable against the passage.
- evidence_span: REQUIRED for grades 1, 2, 3 and -1: a short span (max ~250 characters) copied VERBATIM from the passage (exact substring: same characters, punctuation, spacing; no ellipsis, no paraphrase). For grade 0 use "".
- confidence: "high", "medium" or "low".
Write files with Python json.dumps(obj, ensure_ascii=False) per line. Before finishing, verify with a script (in your work directory) that every code of each question is labelled exactly once and every evidence_span is an exact substring of its passage.

## Final reply
Only: questions done, candidates labelled per question, counts per grade, number of needs_review, problems. Do not paste labels.
