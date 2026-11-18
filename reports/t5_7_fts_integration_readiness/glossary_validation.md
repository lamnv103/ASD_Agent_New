# T5.7 Phase 2 — Glossary Validation

Reuses `reports/t5_6_retrieval_improvement/t5_6_glossary_reconciliation.md`'s mapping directly (re-
verified unchanged this task — both glossary files are byte-identical to their T5.6 state). **No glossary
file is changed in this task either.**

## Classification, using T5.6's mapping

| Class | Count | Examples |
|---|---:|---|
| **Compatible** (same VI trigger, compatible EN scope on both sides) | 35 of 37 overlaps | `melatonin`, `risperidone`, `dau hieu`, `vac xin`, `so thich han hep` |
| **Different scope** (same VI trigger, meaningfully different EN breadth — flagged, not merged) | 2 of 37 overlaps | `can thiep` (TM broader: includes bare "treatment"), `chua noi` (QG broader: bare "talk"/"speech"/"words") — re-examined in context in `fts_precision_audit.md`; neither is a simple "delete the broader side" fix |
| **Missing translation / missing synonym** (one side has it, the other doesn't, same concept) | 25 TM-only + 59 QG-only = 84 | TM-only: `dong mac` (comorbid), `giao duc` (education), `hanh vi` (behavior). QG-only: `cure`, `developmental_delay`, `nonverbal`, `co_occurring`, `boys`/`girls`, `prevalence` |
| **Template-only** (used by template-gating/Evidence Gate, never reaches FTS) | all 63 TM entries, since FTS never imports `text_match.py` | confirmed again this task (§ below) |
| **FTS-only** (used by FTS query construction, never reaches template-gating/Evidence Gate) | all 94 QG entries, since `text_match.py` never imports the FTS glossary | confirmed again this task |

## Re-confirmation of the template-only / FTS-only split, this task

Re-read both files' import graphs directly: `app/answer/answer_generator.py` and
`app/retrieval/evidence_gate.py` import `app.nlp.text_match` only; `app/retrieval/fts.py` imports neither
of those and loads `config/query_glossary_vi_en_v1.json` only via its own `Glossary` class. **Zero
cross-pollination exists in the current code**, exactly as T5.6 found — re-confirmed, not assumed.

## New finding this task: a term's *scope-mismatch risk* should be tracked per-term, not just per-glossary

Phase 1's audit (`fts_precision_audit.md`) found that `can thiep`'s problem is not "the term is wrong,"
it is "the term, when it is the ONLY or WEAKEST corroborating concept in a 2-concept match, needs a
stronger co-occurrence rule." This is new information T5.6's binary "compatible/mismatched" classification
did not capture — a term can be *compatible in scope* (same general meaning on both sides) while still
*carrying different reliability* depending on what other concept it is paired with. The unified structure
proposed below has a field for this.

## Proposed unified term-management structure (design only, not implemented)

A single, future, versioned glossary file both consumers could read from (neither `text_match.py` nor
`fts.py` would need to change their *matching logic*, only where they load their term lists from) — one
entry per concept:

```json
{
  "concept_id": "comorbid",
  "vi_triggers": ["đồng mắc", "kèm theo", "kèm"],
  "en_terms": ["comorbid", "co-occurring", "comorbidity"],
  "provenance": {
    "text_match_py": {"present": false, "introduced_in": null},
    "fts_glossary_json": {"present": true, "introduced_in": "T2.4 (2026-11-15)", "original_id": "dong_mac"}
  },
  "specificity": "high",
  "reliability_notes": "Safe to use alone; does not require a corroborating concept.",
  "known_false_positives": []
}
```

versus a flagged entry:

```json
{
  "concept_id": "intervention_generic",
  "vi_triggers": ["can thiệp"],
  "en_terms": ["intervention", "treatment"],
  "provenance": {
    "text_match_py": {"present": true, "introduced_in": "T3.1-T3.6"},
    "fts_glossary_json": {"present": true, "introduced_in": "T2.4 (2026-11-15)", "original_id": "intervention"}
  },
  "specificity": "low",
  "reliability_notes": "High document frequency; do NOT treat as sufficient alone when paired with only one other low-specificity concept. Safe when paired with a HIGH-specificity concept (e.g. 'aba', 'ndbi', 'melatonin').",
  "known_false_positives": ["ie002 (T5.5/T5.6): paired with 'adhd' alone, surfaced an unrelated sensory-integration-therapy chunk"]
}
```

### Why this design, and what it deliberately does not do

- **Preserves provenance explicitly** (which consumer introduced it, when) — directly answering this
  phase's "giữ provenance và khả năng truy vết" requirement, and making future audits able to tell, at a
  glance, whether a term's absence from one side is an oversight or a deliberate scope choice (today, that
  distinction is invisible — both "never considered" and "deliberately excluded" look identical: absence).
- **Adds a `specificity`/`reliability_notes` field** carrying exactly the nuance Phase 1 found (`can
  thiep` is not simply good or bad, it is conditionally reliable) — something neither existing glossary
  file has any way to express today.
- **Does not auto-merge anything.** Building this file would still require the same human/future-task
  judgment calls T5.6 declined to make automatically — this design only gives that future decision a
  place to be recorded with its reasoning intact, not a mechanism that makes the decision itself.
- **Does not require either consumer to change its matching algorithm.** `text_match.py`'s substring
  matching and `fts.py`'s tsquery construction would each read `en_terms`/`vi_triggers` from this file
  exactly as they read their own file today — only the loading step would change, in a future task, not
  this one.

## Conclusion of Phase 2

No glossary data changed. The classification required by this phase is complete and reuses T5.6's own
mapping (re-verified unchanged). One structural gap in that mapping was found and is proposed, not built:
today's compatible/mismatched/missing classification has no way to express *conditional* reliability
(a term that is fine alone but risky when paired only with another weak term) — the proposed schema adds
that field for a future task to populate.
