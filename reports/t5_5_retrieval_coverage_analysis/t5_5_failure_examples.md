# T5.5 — Failure Examples (detailed case dossiers)

Six representative cases, one per taxonomy category plus two extra category-3 cases (the most actionable
category), each with the actual retrieved content, not just a classification label. Full raw output for
all 31 questions is in `eval/reports/t5_5_fts_diagnostics.json`.

## Case A — Category 3 (strongest finding): `ie015`, melatonin

**Question**: "Melatonin mua ở hiệu thuốc có dùng được cho trẻ tự kỷ không, có cần hỏi bác sĩ không?"
(Can pharmacy-bought melatonin be used for an autistic child, should a doctor be asked?)

**Cache status**: `blocked_uncached`, `QUERY_NOT_CACHED`, no retrieval ever attempted.

**FTS-B result** (glossary-AND, triggered by the `melatonin` glossary key): top hit is
`ASD-OA-PMC7407189`, "Sleeping without Prescription: Management of Sleep Disorders," content: "Sleep
pills should be considered to be an additional treatment option to improve sleep in children when
non-pharmacological interventions ar[e insufficient]..."

**Why this matters**: `ASD-OA-PMC7407189` is the *exact same source* already used by the live
`melatonin_efficacy` and `sleep_nonpharma` templates (confirmed directly in `app/answer/
answer_generator.py` and in T5.3's `template_selection_audit.md`). The live system already has a correct,
cited, Vietnamese answer for "does melatonin help" (`qe048`). `ie015` asks a closely related but
distinctly-phrased question (OTC availability + "should I ask a doctor"), and it cache-misses purely
because the text differs from `qe048`'s cached string — not because the corpus lacks the content, and
almost certainly not because dense retrieval (which handles paraphrase far better than exact-string
matching) would have failed to find the same chunk, had it been allowed to run.

## Case B — Category 1 (genuine gap): `ie017`, vitamin B6 cure claim

**Question**: "Nghe nói uống vitamin B6 liều cao chữa được tự kỷ, có đúng không?" (Heard that high-dose
vitamin B6 cures autism — true?)

**FTS-B result**: 0 hits (no glossary term for "vitamin B6"). **Direct `content ILIKE '%vitamin B6%'`**:
2 chunks, both from `ASD-OA-PMC7407189` (the same sleep-disorder paper as Case A):
> "A solution containing melatonin, Trp and vitamin B6 proved to be significantly more effective than
> melatonin alone in reducing the number of tests that had to be repeated due to awakening of the child."

**Why this matters**: the only corpus mentions of B6 are about B6 as a *minor ingredient in a sleep-aid
combination product*, not about megavitamin therapy as a standalone "cure." A naive keyword-only check
("B6 is mentioned, so there's coverage") would have been wrong — reading the actual content was necessary
to see this is a false-positive token overlap, not real support for or against the claim. This is a
genuine corpus gap for this specific unproven-cure myth, distinct from the vaccine/stem-cell myths the
live system already handles via `vaccine_myth` and `_is_unproven_cure_question`'s stem-cell branch.

## Case C — Category 2 (topic exists, wrong granularity): `ie001`, ASD-vs-ADHD same-or-different

**Question**: "Tự kỷ với tăng động giảm chú ý có phải là một bệnh không hay là hai chuyện khác nhau?"

**FTS-B result**: top hit `ASD-CSV-078`, "Variations in Anxiety and Related Psychiatric Comorbidities in
[ADHD/ASD]," content: "Discussion — We conducted a literature review on the differing levels of anxiety
and psychiatric comorbidities in children with ADHD, ASD, and..."

**Why this matters**: this chunk is genuinely about ASD and ADHD, confirming the general topic area is
well represented (144 "comorbid" chunks corpus-wide, per `t5_5_corpus_coverage.md`) — but it is a
statistical comparison of anxiety *rates*, not a statement that ASD and ADHD are "two distinct,
separately-diagnosable neurodevelopmental conditions that can co-occur," which is what the question
actually needs. No chunk at this specific granularity was found in 10 FTS-B results or 10 FTS-C results
for this question.

## Case D — Category 5 (genuinely indeterminate): `ie012`, 3-part multi-intent question

**Question**: "Con em 2 tuổi hay vẫy tay liên tục, không biết chỉ tay, và cũng chưa nói được từ nào — vậy
có đáng lo không, cần đi khám ở đâu, và nếu đúng là tự kỷ thì can thiệp ra sao?" (3 parts: signs, where to
seek help, intervention.)

**FTS-B result**: only **1** hit total (`NIHR-SENITA-2022`, a sensory-integration-therapy qualitative
interview study) — a strong AND-loss collapse, since the glossary expansion tried to AND together
concepts from all three sub-questions (`can thiệp`→intervention, `chưa nói`→not talking/speech delay,
plus the implicit signs concept) and almost nothing in the corpus satisfies all of them simultaneously.

**Why this is category 5, not 1/2/3**: the single hit returned is very unlikely to be the right answer to
any of the three sub-questions, but its *absence of good hits* could mean either "the corpus lacks
content addressing this exact combination" (category 1/2) or "FTS's AND construction destroyed recall
that would exist for each sub-question individually" (a retrieval-method artifact, closer to category 3).
Distinguishing these would require testing each sub-question's retrieval separately and is exactly the
kind of judgment call this task's instructions forbid making up evidence for — so it is left as
indeterminate.

## Case E — Category 3: `ie032`, preschool-specific inclusion (a near-miss worth fixing)

**Question**: "...trẻ tự kỷ có cần chế độ học riêng ở độ tuổi mầm non hay học chung với các bé khác?"
(Does an autistic child need a separate program at preschool age, or should they be mainstreamed?)

**FTS-B/C result**: both returned only generic, off-topic hits (gastrointestinal symptoms, general food
selectivity) — a clean miss for this retriever. **Direct `content ILIKE '%preschool%'`**: **71** chunks
corpus-wide, and the live `school_inclusion` template's own source, `ASD-CSV-019` ("School-Based
Interventions for Increasing Autistic Pupils' [participation]"), is a strong topical match for this
exact question. FTS simply never connected the two, because the question's Vietnamese phrasing
("học riêng"/"học chung") has no entry in either glossary (`app/nlp/text_match.py`'s 63 or
`config/query_glossary_vi_en_v1.json`'s 94).

**Why this matters**: this is the clearest example in the whole set of a case where the corpus content is
confirmed present and topically on point, and the only reason the live demo (hypothetically, if it could
try) would plausibly miss it via FTS is a vocabulary gap — not a corpus gap. Whether dense retrieval
(unavailable to test here) would do better is unknown but plausible, since dense does not depend on an
explicit glossary at all.

## Case F — A confirmed false-positive in the term-matching heuristic itself: `ie002`

**Question**: "Con tui bị tự kỷ với ADHD cùng lúc thì ưu tiên can thiệp bên nào trước ạ?" (comorbid
ASD+ADHD, which intervention to prioritize)

**FTS-B result, rank 2**, classified **"direct"** by the Phase 2 diagnostic script's reuse of
`app/nlp/text_match.chunk_matches_terms`: `ASD-SUP-PMC7726187`, "Evaluating Sensory Integration/Sensory
Processing [interventions]" — a paper about sensory-integration therapy, with no connection to ADHD
comorbidity or care prioritization at all.

**Why this happened**: the glossary key `"can thiep"` maps to `["intervention", "treatment"]`, both
extremely generic words present in nearly every clinical paper in the corpus. The classification heuristic
(borrowed from the live Evidence Gate's own `chunk_matches_terms`) marked this a "direct" match purely
because the chunk's title contains "Evaluating... interventions." **This reproduces, on new text, the
exact limitation the Evidence Gate's own module docstring already discloses**: it cannot tell a
topically-adjacent-but-wrong-condition chunk apart from a truly relevant one when both happen to share an
overly generic queried term. It is reported here as a confirmation of a known, disclosed limitation, not
a new defect — and specifically not something this task fixes, since no code change is permitted in T5.5.
