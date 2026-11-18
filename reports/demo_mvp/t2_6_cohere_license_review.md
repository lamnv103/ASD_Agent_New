# T2.6 — Cohere Authorization & Source License Review

**Scope:** read-only audit. No live Cohere API request was sent, no query embedding was enabled, no
database write occurred, no document or chunk was uploaded anywhere, and no production permission was
changed. This report synthesizes evidence that already exists in the repository (produced by earlier,
independent audits) with the specific question T2.6 asks: *can live Cohere query embedding be enabled for
the student demo right now?*

Primary sources read for this report: `docs/provider_terms/cohere_2026-11-14.md`,
`config/embedding_profiles.json`, `app/retrieval/embeddings.py`,
`reports/demo_mvp/t2_5_local_encoder_compatibility_audit.md`, `eval/reports/license_audit_2026-11-14.md`,
`eval/reports/license_review_matrix.csv`, `eval/reports/license_classification_repair_2026-11-14_phase5.md`,
`app/rights/license_audit.py`, and `migrations/001_core_schema.sql` / `004_rights_evidence_and_chunk_v2.sql`.

---

## Phase 1 — Provider terms (Cohere)

All figures below come from `docs/provider_terms/cohere_2026-11-14.md`, which was produced by making only
two no-content calls (`GET /v1/models/embed-v4.0`, `POST /v1/check-api-key`) — no document or query text
was sent during that check.

| Item | Finding | Evidence |
|---|---|---|
| Key type | **Trial (evaluation)** key | Response headers `x-trial-endpoint-call-limit: 100`, `x-trial-endpoint-call-remaining: 99`, `x-endpoint-monthly-call-limit: 1000`; `check-api-key` → `valid: true` |
| Trial rate limits | 1,000 API calls/month; Embed endpoint 2,000 inputs/minute | Cohere "Rate limits" docs, as cited in the provider-terms file |
| Trial → production | Must upgrade to "serve Cohere in production"; the page does not explicitly ban commercial use on a trial key | Cohere "Going live" docs |
| Terms that apply to a trial key | **Terms of Use + Privacy Policy** — explicitly **not** the Enterprise Data Commitments (Zero Data Retention etc.) | Cohere "Enterprise Data Commitments" page: "Our Terms of Use and Privacy Policy apply to data we receive from users using a trial API key" |
| Data usage for paying (non-trial) customers | Prompts/generations may be used for training **unless the customer opts out** via Settings → Data Controls; logs deleted after 30 days; Zero Data Retention (ZDR) is enterprise-only and requires approval | same Enterprise Data Commitments page |
| Cohere's rights over submitted data (Terms of Use) | Non-exclusive, perpetual licence to access, store, and use submitted data "to improve and enhance the Cohere solution and our other offerings," including sharing API data with third parties that provide services to Cohere (§4.1); customer warrants it holds sufficient rights to the data it uploads (§13.5) and indemnifies Cohere (§21.4) | Cohere Terms of Use, version accessed and dated **2022-09-07** in the provider-terms note |
| Technical spec | Model `embed-v4.0`; `output_dimension` ∈ {256, 512, 1024, 1536}, default 1536; max 96 texts/call; `input_type` ∈ {`search_document`, `search_query`}; `truncate=NONE` errors instead of silently truncating | Cohere Models / Embed API v2 docs; matches `config/embedding_profiles.json` exactly |

**Query-specific retention/processing conditions:** the provider-terms note does not distinguish
`search_query` input from `search_document` input anywhere in Cohere's published terms — the Terms of Use
licence grant in §4.1 applies to "data" generically, with no carve-out for short query strings versus
document text. **No query-specific exemption is documented.** Treat query text under the same terms as
document text unless and until Cohere states otherwise in writing.

**Commercial/non-commercial restriction:** this is a restriction from the *source documents'* Creative
Commons licences (Phase 2 below), not from Cohere's own terms — Cohere's terms say nothing about the
licence status of what is submitted; they only grant Cohere its own usage rights over whatever is sent.

**Research/demo applicability:** nothing in the cited Cohere documentation grants a research- or
education-use exemption from the Terms of Use data-rights grant. A student demo is not a special case
under these terms as evidenced; it is ordinary trial-key usage.

### Uncertainties requiring confirmation from Cohere (explicitly unresolved — not interpreted as permission)

1. Whether the Terms of Use version accessed and dated 2022-09-07 is still the current version, or
   whether a newer version or a separate SaaS Agreement applies to production keys.
2. Whether a **trial** account can toggle the "Data Controls" training opt-out at all (the official page
   does not say; opt-out is documented only in the context of paying/production accounts).
3. The Privacy Policy itself has not been read in any audit to date.
4. Whether sending third-party-governed (CC BY-NC) text to Cohere as a data processor constitutes
   "commercial use" under those licences is a legal question outside the scope of any audit performed —
   it requires a person with legal authority to answer, not an inference from these documents.

None of these open items were resolved by assuming they favor the project; each is carried into Phase 4
and the approval request as an open question.

---

## Phase 2 — Source license audit

Evidence: `eval/reports/license_audit_2026-11-14.md` (73 full-text documents: 33 core + 40 gaps) and the
corrected classification in `eval/reports/license_classification_repair_2026-11-14_phase5.md`. The
embedding run covered 71 of these 73 (2 — `ASD-CSV-077` and `NIH-NIMH-CHILDREN` — remain quarantined for
reasons unrelated to licensing and are excluded from the 2,338-vector set per
`t2_5_local_encoder_compatibility_audit.md`). Both quarantined documents are CC BY / Public Domain, so all
13 non-commercial-licensed documents **are** among the 71 that were research-embedded.

### Current license classification (post-repair, as stored in the catalog)

| License | Version | Documents | Notes |
|---|---|---:|---|
| CC BY | 4.0 | 34 | Repaired from an over-strict catalog label on 2026-11-14 (Phase 5, Task A) |
| CC BY | 3.0 | 1 | `NIHR-SENITA-2022` |
| CC BY-NC | 4.0 | 9 | |
| CC BY-NC | 3.0 | 1 | |
| CC BY-NC-SA | 3.0 IGO | 3 | `WHO-CST-INTRO-2022`, `WHO-CST-PARTICIPANTS-2022`, `WHO-ECD-GUIDELINE-2020` |
| Public Domain | — | 24 | 17 CDC + 1 NIDCD pages have `agency_policy_only` evidence (site-wide reuse policy, not a per-page statement); the rest have an explicit public-domain statement in the original file |

Evidence quality: 55 documents have `evidence_in_original_document` (a licence statement or JATS
`<license>` tag read directly from the original file); 18 (CDC/NIDCD) have only `agency_policy_only`
evidence (a site-wide reuse policy, not a per-page statement) — flagged as weaker evidence, not treated as
equivalent to a document-level statement.

### Other license categories / pending review

- **Pending rights review:** `source_rights.*_allowed` is **NULL for all 73 documents** in the production
  table — per schema comment, "NULL in `*_allowed` = not verified = not allowed. Processing permissions
  are a human decision, never inferred from the licence label" (`migrations/001_core_schema.sql:48`).
  `verified_by`/`verified_at` are also empty for all rows — no one has signed off on a permission decision
  yet, as of the last check (2026-11-14; not re-verified against a live database in this report, since no
  DB connection was opened for T2.6).
- **Catalog-label vs. licence conflicts:** the 35 CC BY documents previously carried a stricter catalog
  label (`verified_noncommercial_research`) than their actual licence permits; this was corrected on
  2026-11-14 to `verified_cc_by`. The correction is a *classification* fix, not a *permission* grant — all
  `*_allowed` columns remained NULL throughout.
- **Third-party material:** every evidence row for the 36 academic-article sources (CC BY and CC BY-NC)
  carries a note that per-figure/per-table third-party credit lines exist and were **not adjudicated
  independently** — i.e., the article's overall CC licence does not necessarily cover every embedded
  figure, and this has not been checked.

### Does the proposed Cohere use create unresolved concerns?

**Yes, for 13 of 71 embedded documents; open, not yet resolved, for the remaining 58.**

- The 13 CC BY-NC / CC BY-NC-SA documents permit **non-commercial use only**. Cohere's Terms of Use (trial
  key) grant Cohere a right to use submitted data to "improve and enhance" its own commercial offerings —
  a plausible conflict with the non-commercial restriction. The existing license audit already classifies
  `cohere_processing_allowed = blocked` for exactly these 13 documents, for this reason
  (`license_audit_2026-11-14.md` §5).
- The remaining 58 documents (CC BY, Public Domain) are not blocked *by licence*, but accepting Cohere's
  data-rights terms for them is recorded as the **project owner's operational decision**
  (`cohere_processing_allowed = pending_decision`), not an automatic yes.
- This matters for T2.6 specifically because **query text, not document text, is the open question here**
  — but since Cohere's terms draw no distinction between query and document input (Phase 1), the same
  conflict analysis applies to any query text that paraphrases or quotes NC-licensed content retrieved
  from those 13 documents, and the same pending-decision status applies to query text touching the
  remaining 58.

**Not concluded:** that all sources are prohibited (58 of 71 have no licence-level objection) or that all
are permitted (13 of 71 have a documented conflict, and 0 of 71 have an owner-signed approval of any kind).
Both blanket conclusions would contradict the evidence above.

---

## Summary table

| Question | Answer | Evidence |
|---|---|---|
| Does Cohere's trial key carry a data-rights grant broader than query use alone? | Yes — generic "improve and enhance" licence over all submitted data, no query/document distinction | Terms of Use §4.1 (via provider-terms note) |
| Is there a non-commercial-use conflict? | Yes, for 13/71 embedded sources (CC BY-NC / CC BY-NC-SA) | `license_audit_2026-11-14.md` §5 |
| Is there an owner sign-off on any Cohere processing permission? | No — all `*_allowed` NULL, `verified_by`/`verified_at` empty for all 73 catalog documents | `license_classification_repair_2026-11-14_phase5.md` §5 |
| Is there a research/demo exemption in Cohere's terms? | Not found in any document reviewed | absence of such a clause in the provider-terms note |
| Is ZDR or training opt-out available on the current (trial) key? | Opt-out exists for *production* keys; trial-key availability is undocumented; ZDR is enterprise-only | provider-terms note, "Điểm chưa rõ" |
