# T5.1 §5 — q033 (ADHD/ASD Confusion) Context Analysis

**No code was changed to produce this report.** `app/retrieval/evidence_gate.py` was read and traced
against the live chunk content below, not modified.

## The exact mechanism (re-traced live, with the actual chunk text)

Query: `"Can thiệp do cha mẹ thực hiện có hiệu quả không?"` ("Is parent-delivered intervention
effective?"). `specific_terms()` finds `"cha me"` (GLOSSARY → `["parent"]`) as the query's one
topic-specific term — correctly, since the question is genuinely about parent-delivered intervention.

Among the Top-5 retrieved chunks, `NIH-NIMH-ADHD` ranked highly and was classified `direct` support. Its
actual content:

```
Title:   "Attention-Deficit/Hyperactivity Disorder: What You Need to Know"
Section: "How is ADHD treated? > Parent education and support"
Content: "Therapy for children and teens requires parents to play an active role... Mental health
          professionals can educate parents about the disorder... parenting skills training,
          stress management techniques for parents, and support groups..."
```

### Why lexical matching produces this false positive

1. **The section heading literally is "Parent education and support."** `evidence_gate.py`'s
   `support_type` logic checks `title + section` first and grants `"direct"` (the *strongest* label) the
   moment the specific term appears there — by design, because a term in the heading usually means the
   chunk is genuinely *about* that topic (this is exactly the mechanism that correctly fixed the earlier
   q007 "signs" bug in T4). The same mechanism that fixes one false negative creates this false positive,
   because **"parent" is not specific to ASD** — it is a completely generic clinical-communication word
   that appears in the heading of a parent-support section for *any* child condition, ADHD included.
2. **The query's only specific term ("cha mẹ"/"parent") is not discriminating between conditions.** Unlike
   "vaccine," "risperidone," or "stem cell" — which only appear in chunks actually discussing those exact
   things — "parent" appears constantly across the entire corpus regardless of which disorder a document
   is about. The gate has no way to know the query is about *autism* parenting specifically rather than
   parenting of a child with *any* condition, because the query's only specific term says nothing about
   which condition.
3. **The ASD anchor ("tự kỷ") is present in the query but is deliberately excluded from the specific-term
   check** (see `app/nlp/text_match.py` — anchor terms are intentionally generic across the whole corpus,
   so they cannot be used to discriminate a chunk's topic; that is the entire reason they're kept
   separate from the glossary). This means the system correctly knows the query is about ASD, but has no
   mechanism to check that the *retrieved chunk* is also about ASD specifically, as opposed to a different
   developmental/psychiatric condition that happens to share the word "parent."

### Could a context rule remove the wrong-context evidence, without a semantic model?

**Partially, with real trade-offs — not attempted in this task (analysis only, Evidence Gate untouched).**
Two lexical rule ideas, each evaluated honestly:

- **"Require the ASD anchor itself to appear somewhere in the chunk, not just in the query."** This would
  have correctly rejected the `NIH-NIMH-ADHD` chunk (it never says "autism" or "ASD" anywhere). It would
  **not** break any of the 7 working templates or the 17 Group-C fallback cases, because all of their
  trigger/supporting chunks are from ASD-specific documents that do mention autism/ASD by name — this was
  checked by inspecting each Group-C chunk's source document title in `topic_gap_matrix.md`, all of which
  are ASD-named sources (`CDC-ASD-*`, `NIH-NIMH-ASD-2025`, ASD-focused PMC papers). The real risk: a
  genuinely useful ASD-relevant chunk from a *comorbidity* document that correctly discusses ASD+ADHD
  together (e.g. the evidence for qe081, which legitimately needs ADHD-labeled content since the question
  is explicitly about the ASD+ADHD combination) could be wrongly excluded by a blanket "must mention
  autism" rule. This is a real, named trade-off, not a free win.
- **"Down-rank (not exclude) a chunk whose document-level topic is a different, named condition than the
  query's."** More conservative, but requires a per-document "primary condition" tag that does not
  currently exist in the retrieved metadata (`RetrievedChunk` carries `source_id`/`title`/`section`, not a
  structured topic label) — building one would mean either inferring it lexically (circular — the same
  problem) or adding new metadata to the database view, which is a schema change, not something this
  read-only analysis task can do or should casually recommend without the project owner's sign-off.

**Verdict**: a context rule *could* reduce this specific failure mode with a known, bounded trade-off (the
ADHD-comorbidity-question case), but it cannot be added without deciding how to handle that trade-off —
which is a product decision, correctly left for `template_expansion_plan.md`/the project owner, not
silently decided inside this analysis.

### What genuinely needs a semantic model

Distinguishing "this chunk is about parenting a child with ADHD" from "this chunk is about parenting a
child with ASD" when **neither the query nor a simple anchor check can settle it from word presence
alone** — e.g. a chunk that discusses "supporting your child" without naming either condition, in a
corpus that contains comorbid-condition documents on purpose. No lexical rule can resolve this because
it requires understanding *what a chunk is fundamentally about*, not just which words it contains. This
is the same limitation already stated in `reports/final_hardening/phase_2_evidence_gate_audit.md` and
confirmed, not newly discovered, by this deeper trace.

### What can be done with no new data-processing authorization (no LLM, no live Cohere)

1. The "require ASD anchor in the chunk" rule above — pure lexical, no external call, implementable
   entirely with existing retrieved text. **Recommended as the first fix**, with the qe081-style
   comorbidity trade-off explicitly flagged for the project owner to accept or reject before
   implementation (not decided here).
2. **Exclude the affected 2 questions (qe045, qe081) from Group-C template candidates until the rule above
   is resolved** — i.e., do not build a parent-intervention template yet, since its best current evidence
   includes the ADHD chunk. This is a scope decision for `template_expansion_plan.md`, not a code change.
3. **Do not** attempt a disease-name denylist ("never show a chunk whose title contains another named
   condition") as a shortcut — it would incorrectly block legitimate ASD+comorbidity content (anxiety,
   ADHD, epilepsy, GI) that this corpus intentionally contains and that several *working* Group-A/C
   answers rely on (e.g. `ASD-OA-PMC12620806`'s GI/vaccine content explicitly discusses comorbid and
   environmental topics by design).
