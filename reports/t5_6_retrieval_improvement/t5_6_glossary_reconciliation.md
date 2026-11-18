# T5.6 Phase 1 — Glossary Reconciliation Mapping

**No glossary data file was changed in this phase.** This is a mapping report only, produced before any
data change, per the task's explicit instruction. Comparison method: fold both glossaries' Vietnamese
trigger keys through `app.nlp.text_match.fold()` (lowercase, diacritic-strip, punctuation-collapse) so
that spelling/diacritic variants of the same trigger are compared as the same key, then compare the
English term sets each side maps that key to.

## Overall counts

| | Count |
|---|---:|
| `app/nlp/text_match.py` `GLOSSARY` entries | 63 |
| `config/query_glossary_vi_en_v1.json` entries (concepts) | 94 |
| Folded-key overlap (same VI trigger, both glossaries) | 37 |
| TM-only folded keys (in text_match.py, absent from the FTS glossary) | 25 |
| QG-only concepts (in the FTS glossary, with no overlapping VI trigger in text_match.py) | 59 |

## Provenance, kept separate per the task's instruction

- `app/nlp/text_match.py`'s `GLOSSARY`: built across T3.1–T5.3, incrementally, specifically to gate which
  of the 17 live answer templates fires and to drive the Evidence Gate's direct/indirect/generic
  classification. Each entry's purpose is "does this query ask about X specifically enough to trust a
  template/chunk about X."
- `config/query_glossary_vi_en_v1.json`: built in T2.4 (2026-11-15), specifically to construct PostgreSQL
  `tsquery` boolean expressions for the FTS-B/C experimental retrieval profiles, evaluated only against
  the frozen 66-question set. Each entry's purpose is "what English lexeme(s) should a `tsquery` look
  for," a different design goal than TM's (TM never builds a tsquery; it does plain substring matching).

These two glossaries were never meant to be, and are not, interchangeable by construction — reconciling
them means identifying where they already agree, where they genuinely differ in scope (not simply
"missing" from one side), and where one glossary has vocabulary the other could safely absorb without
changing either's existing meaning.

## 37 overlapping triggers — classified by whether the EN mapping is compatible or scope-mismatched

Full machine-readable comparison: produced this task, available by re-running the comparison snippet in
this report's methodology (not saved as a separate data file, since it is fully reproducible from the two
glossary files directly and this task must not create a third, half-merged glossary file by accident).

**Compatible (same or near-same EN scope — 35 of 37)**: e.g. `melatonin`→`melatonin` (identical);
`risperidone`→`risperidone` (identical); `dau hieu`→TM `["sign","symptom"]` vs QG `["sign","signs"]`
(QG narrower but not contradictory); `vac xin`→TM `["vaccine","vaccination","immuniz"]` vs QG
`["vaccination","vaccinations","vaccine","vaccines"]` (same concept, QG lacks the `immuniz` stem that
also matches "immunization"); `so thich han hep`→TM `["restricted interest"]` vs QG
`["circumscribed interests","restricted interests"]` (QG is actually broader here — includes the clinical
synonym "circumscribed interests" that TM lacks).

**Scope-mismatched (genuinely different breadth, flagged, NOT auto-merged — 2 of 37)**:
- **`can thiep`** ("intervention"): TM maps to `["intervention", "treatment"]`; QG maps to
  `["intervention", "interventions"]`. TM's inclusion of the bare word `"treatment"` is markedly broader
  — "treatment" appears in nearly every clinical paper in the corpus regardless of topic. This is the
  **confirmed root cause of the T5.5 Case F false-positive** (`ie002`'s comorbidity-priority question
  being "directly" matched to an unrelated sensory-integration-therapy chunk purely because both mention
  "treatment"). **Not merged automatically**: TM's broader scope may be intentional (catching more
  phrasing variants for template-gating purposes, where false positives are cheaper because a wrong
  template still requires the gated source to also be present) but is actively harmful when reused,
  unmodified, for FTS ranking (where "treatment" alone has almost no discriminating power). This
  scope difference is exactly why Phase 2's experiments treat the two glossaries' English term lists as
  NOT freely interchangeable.
- **`chua noi`** ("not yet talking"): TM maps to `["not talking", "no words", "speech delay"]` (specific
  phrases); QG's same-folded-key concept (`talk`) maps to `["speak", "speech", "talk", "talking",
  "words"]` — bare, extremely generic single words that will match almost any chunk discussing
  communication at all, not specifically "not yet talking by a certain age." Flagged, not merged, for the
  same reason as `can thiep`.

## 25 TM-only triggers (used for template-gating today, absent from the FTS glossary)

Representative sample (full list is the complete diff of the two key sets, reproducible from the glossary
files): `hanh vi` (behavior/behaviour), `di truyen` (genetic/gene/heredit), `dong mac` (comorbid),
`giao duc` (education), `trieu chung` (symptom), `tiem chung`/`vacxin` (no-diacritic vaccine variants —
QG's `vac xin` entry only has the diacritic form as a VI trigger), `thanh nien`/`truong thanh`/`nguoi lon`
(adolescent/adult), `thuoc tam than` (psychiatric medication), `huan luyen ky nang` (caregiver skills
training — QG has a near-identical concept `caregiver_skills_training` but under a *different* VI
trigger phrase, so the folded-key diff counts it as TM-only even though QG has an adjacent entry — see
"near-miss" note below).

**Direct relevance to T5.5's findings**: `dong mac` (comorbid) is exactly the missing concept that would
have let `ie001`/`ie002`/`ie003`/`ie028` connect to the corpus's 144 "comorbid" chunks via FTS;
`giao duc` (education) is relevant to `ie032`'s preschool-inclusion question. Neither of these TM-only
terms currently has any effect on FTS at all, since FTS only reads the 94-entry QG file.

## 59 QG-only concepts (used for FTS today, absent from the TM glossary entirely)

Representative sample directly relevant to T5.5's confirmed gaps: `cure` (chữa/chữa khỏi/chữa được —
would have let TM's template-gating and Evidence Gate recognize `ie013`'s "will it ever be cured"
question as specific rather than falling through to the generic catch-all logic); `developmental_delay`
(chậm phát triển — relevant to `ie004`); `nonverbal` (chưa biết nói — relevant to `ie004`); `co_occurring`
(kèm/kèm theo — relevant to the comorbidity questions); `boys`/`girls` (bé trai/bé gái — relevant to
`ie031`'s sex-difference question); `prevalence` (phổ biến/tỷ lệ); `gastrointestinal`; `regression`/
`skill_loss`; `parent_mediated`; `early_signs`; `home`. None of these 59 currently has any effect on the
live answer path or the Evidence Gate, since `text_match.py` only has 63 of its own entries and does not
import the FTS glossary.

## "Near-miss" entries — same concept, different VI trigger phrase, undercounted by the naive key diff

A few concepts exist on both sides but under *different* Vietnamese trigger wording, so the folded-key
comparison above counts them as non-overlapping even though they clearly correspond:
- TM `huan luyen ky nang` ("huấn luyện kỹ năng") ↔ QG's `caregiver_skills_training` concept, triggered by
  the longer phrase "chương trình huấn luyện kỹ năng cho người chăm sóc" — TM's shorter trigger would
  actually match a strict substring of QG's longer one, but the folded-key set comparison treats them as
  distinct strings. This is disclosed as a methodology caveat, not fixed in this phase (fixing it would
  require either an edit — out of scope for a mapping-only phase — or a substring-aware comparison
  algorithm, which was not built here to keep this phase strictly read-only-analysis).

## Explicit non-action, per instruction

**No automatic merge was performed.** The two scope-mismatched cases above (`can thiep`, `chua noi`) are
specifically flagged as needing a human/future-task decision about which scope is correct for which
consumer (template-gating tolerates more false positives than ranking does), not resolved by this report.
Any future glossary change should treat TM-only and QG-only entries as candidates to *propose adding* to
the other side — starting from the specific, corpus-confirmed-relevant items named above — rather than a
wholesale automatic union, exactly as the task instructs.
