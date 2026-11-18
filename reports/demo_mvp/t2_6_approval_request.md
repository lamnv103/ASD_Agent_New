# T2.6 — Approval Request: Live Cohere Query Embedding for the ASD-RAG Student Demo

**This document requests a decision; it does not grant one.** Preparing this request does not authorize
live Cohere query embedding. Nothing described here has been enabled. See
[`t2_6_cohere_license_review.md`](t2_6_cohere_license_review.md) and
[`t2_6_authorization_decision_matrix.md`](t2_6_authorization_decision_matrix.md) for full supporting
evidence.

## What is being requested

Permission to send **end-user query text** (not document text) to Cohere's hosted Embed API, so that the
ASD-RAG demo can answer questions whose exact wording is not already in the local query cache.

## Purpose

Student research/demo use of the ASD-RAG retrieval system: letting a demo user type a free-form question
and get a retrieved answer, instead of being limited to the 66 pre-cached evaluation questions.

## Data being sent

- Only the text the user typed into the query box, sent as `input_type=search_query`.
- No document chunks, no full source documents, no database credentials, and no internal evaluation
  labels — these are structurally excluded by the existing code path (see data-flow section of the
  decision matrix), not by a new filter added for this request.
- Query text **could** contain personal or sensitive information if a user types it in; no technical
  filter currently prevents this. See "Open questions" below.

## Service provider and model

- Provider: Cohere (`api.cohere.com`).
- Model: `embed-v4.0`, Embed API v2, `output_dimension=1536` — the exact profile already used for the
  existing 2,338 document vectors (`cohere_embed_v4_1536_v1`). No new model and no re-embedding of
  documents is requested here.
- Current key: a **trial** key (1,000 calls/month, 2,000 inputs/minute); subject to Cohere's Terms of Use
  and Privacy Policy, not the Enterprise Data Commitments.

## Intended duration

Not fixed by this request — proposed as **time-boxed to the student demo period**, to be re-reviewed
(not auto-renewed) if the demo continues beyond that period or moves toward any non-research use. The
owner should specify an end date or review checkpoint when granting approval.

## Access controls (proposed, not yet built)

- A single explicit feature flag (e.g. `ASD_RAG_ENABLE_LIVE_QUERY_EMBEDDING`), defaulting to **off**,
  gating whether `CohereQueryEmbedder` is constructed as the `CachedQueryEmbedder`'s `inner` embedder in
  `app/api.py`. Today this is hardcoded to `inner=None` (always off); enabling the flag is new work, not
  yet implemented.
- The flag would be set to "on" only in the specific demo deployment the owner approves — every other
  environment (local dev, CI, any other deployment) stays cache-only/fail-closed by default.
- No change to database write permissions, production retrieval permissions, or the research-track
  embedding authorization already recorded in `research_embedding_authorizations`.

## Retention / privacy questions for the project owner

1. Do you want to apply a blanket "non-commercial use only" policy across the *entire* corpus regardless
   of each document's actual licence (affects whether Scenario B should include all 71 embedded sources
   or exclude the 13 NC-licensed ones), or treat each document by its own licence terms?
2. Are you willing to accept Cohere's Terms of Use data-rights grant (§4.1: non-exclusive, perpetual
   licence to use submitted data to improve Cohere's own offerings) for query text that might paraphrase
   or quote content from the 13 CC BY-NC / CC BY-NC-SA sources?
3. What is the acceptable duration/scope for this authorization — one demo session, a semester, indefinite
   until revoked?
4. Should the demo UI warn or block users from entering identifying personal details before a query is
   embedded?

## Questions requiring written confirmation

**From the project/data owner (required before any implementation work on Option B):**
- Explicit go/no-go on Scenario B vs. staying on Scenario A/C (see decision matrix).
- Answers to retention/privacy questions 1–4 above.
- Who is authorized to flip the feature flag in the approved deployment, and who can revoke it.

**From Cohere (required to close the open items in the licence review, before relying on any assumption
about data handling):**
- Confirm whether the Terms of Use version accessed and dated 2022-09-07 is current for trial keys, or
  whether a different/updated agreement now applies.
- Confirm whether a trial-tier account can access the training opt-out in Data Controls, or whether that
  requires upgrading to a paid/production key.
- Confirm whether Zero Data Retention can be requested for a small research/education deployment, or is
  strictly enterprise-only regardless of volume.

## Revocation procedure

If authorization is granted and later revoked:

1. Set the feature flag back to off (or remove it), which reverts `CachedQueryEmbedder` to
   `inner=None` — immediately fail-closed for any uncached query, with no further code change needed.
2. No cached data needs to be deleted to revoke: the on-disk query cache stores only
   `sha256(profile|model|dim|input_type|text)` and the resulting vector, never the raw query text
   (`app/retrieval/query_embedding.py` module docstring) — so revocation does not require a data-deletion
   step on the local side.
3. Whether previously-sent query text can be deleted from Cohere's systems is governed by Cohere's own
   retention terms (30-day log retention is documented for paying accounts; trial-key retention is one of
   the open items above) — this is outside this project's control and should be asked of Cohere directly
   if revocation requires it.

## Final status

**`APPROVAL_REQUIRED`**

No scenario in the decision matrix has been authorized. Scenario A (cache-only, fail-closed) remains the
operating state. This request packages what is needed for the owner to grant Scenario B, but granting it
is a decision for the project/data owner (and, for the open items above, written confirmation from
Cohere) — not a conclusion this audit is positioned to reach on the evidence gathered so far.
