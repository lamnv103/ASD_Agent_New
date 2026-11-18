# T6.1 Phase 1 - Human relevance annotation protocol

## Unit and blinded procedure

The unit is one **query-chunk** pair. Each annotator independently reads the full query and chunk, assigns a grade, and writes a concise rationale before any adjudication. Do not inspect `candidate_pool_provenance_map.json`, the T6.0 comparison CSV, or retrieval system outputs. The annotation sheets omit retriever, profile, rank, score, RRF score, and pool stratum. Keep each annotator's sheet private until both have submitted.

The sheet includes query ID/text, stable chunk ID, source ID/title and location, exact chunk content/hash, relevance grade, evidence type/span, rationale, annotator ID, completion status, disagreement reason, contradiction flag, context limitation, and adjudication grade. The separate 12-variant sheets are diagnostic only and must not be merged into the 66-query core statistics.

## Grade rubric

- **3 - Highly/directly relevant:** the chunk contains explicit evidence that directly supports a material part of the question. A topical mention or a citation to a source without supporting content is not enough.
- **2 - Relevant/partial:** provides accurate, useful information needed for an answer but leaves a material part unanswered, or supports one aspect of a multi-part question.
- **1 - Marginal:** shares the topic or terminology but offers little usable evidence for answering this specific question.
- **0 - Not relevant:** does not support answering the question, even if it is ASD-related. Use for off-topic, merely lexical matches, or content that cannot support the requested claim.
- **Needs adjudication / unassessable:** do not invent a numeric grade when the chunk is corrupted, incomplete, ambiguous, internally conflicting, or cannot reliably be assessed. Leave numeric grade blank and set `review_status=NEEDS_ADJUDICATION`, with reason.

Multiple chunks can each be relevant. Do not require any single chunk to answer the entire question. Conversely, do not award grade 3 simply because a chunk could be combined with unseen evidence. Judge the content present in that chunk against the query.

## Required rationale and evidence

For grades 0-3, provide a short, query-specific rationale. For grades 2-3, enter an exact verbatim `evidence_span` copied from the chunk, or explain why no short span is suitable. Never paraphrase as a quotation, repair malformed text, or add facts from outside the chunk. Use `evidence_type` to describe the support (e.g. direct fact, definition, recommendation/guidance, method/measurement, background/context, contradiction, none). Flag `contradiction_flag=YES` when the chunk materially conflicts with another candidate or the query premise; do not resolve the conflict alone. Record missing context or population/age/time/source limitations in `context_limitation`.

Retrieval relevance is not assessment of medical truth, clinical quality, treatment appropriateness, or patient-specific advice. Annotators must not infer relevance from source rank, score, similarity, or retrieval provenance. The package exposes source title/ID for context as requested; source identity can itself influence judgment, so note any source-authority bias and rely on chunk evidence.

## Independence, disagreement, and adjudication

Two annotators are prepared with separate randomized sheets. Each should be qualified for information relevance review and work independently. After both complete, match by `annotation_id`; compute exact agreement and weighted Cohen's kappa on numeric pairs only, reporting unassessable/blank separately. Kappa is descriptive and can be unstable under grade imbalance. Discuss disagreements without revealing system rank until initial judgments are locked. A third adjudicator resolves material disagreements and documents the reason; preserve both original labels and adjudicated label. Do not count missing grades as 0.

Before use, select annotators, provide a short calibration session on examples outside the 66-query evaluation pool, confirm CSV encoding/handling of multiline content, and agree on secure return path and reviewer IDs.
