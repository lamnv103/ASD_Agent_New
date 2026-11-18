# T2.6 — Authorization Decision Matrix (Cohere Live Query Embedding)

Companion to [`t2_6_cohere_license_review.md`](t2_6_cohere_license_review.md). This report covers Phase 3
(data flow) and Phase 4 (the three scenarios) of T2.6. No code change, no config change, and no API
request were made while producing this report.

---

## Phase 3 — Data flow if live query embedding were enabled

Based on the existing, already-implemented code path (`app/retrieval/query_embedding.py`,
`app/retrieval/embeddings.py`), which this report does **not** modify:

**What would be sent to Cohere, per request:**

| Field | Value | Source |
|---|---:|---|
| Payload content | The end user's query text only (`texts` list), as given to `CohereQueryEmbedder.embed_queries` | `query_embedding.py:51` |
| Task type | `input_type = "search_query"` (`profile.query_input_type`) | `embedding_profiles.json`; `query_embedding.py:53` |
| Model identifier | `embed-v4.0` | `embedding_profiles.json` |
| Other request metadata | `embedding_types: ["float"]`, `output_dimension: 1536`, `truncate: "NONE"` | `embeddings.py:66-68` (`payload()`) |
| Transport metadata | HTTPS to `https://api.cohere.com/v2/embed`; `Authorization: Bearer <COHERE_API_KEY>` header | `embeddings.py:21,87-88` |

**Explicitly excluded from this call, by construction of the existing code — not by a new restriction
added for this report:**

- **Document chunks / full source documents** — `CohereQueryEmbedder.embed_queries` only ever receives
  the `texts` argument passed by its caller (the API's query handler); nothing in the dense-retrieval path
  feeds chunk content back into the query embedder. Chunks are embedded by a separate code path
  (`app/ingest/embed_pipeline.py`) that is not invoked at query time.
- **Personal or sensitive information** — not excluded by code, because the embedder sends whatever text
  it is given verbatim. This is a **content risk, not a code risk**: if a demo user types personal health
  information into the query box, that text is what would be sent. See "Input restriction" below.
- **Database credentials** — never part of the embed payload; the only credential used is the Cohere API
  key itself, read from the environment and never logged (`embeddings.py` module docstring: "Never logs or
  returns input texts or the API key").
- **Internal evaluation labels** — the `retrieval_eval_v1.jsonl` gold labels, silver judgments, and
  regression metrics are not referenced anywhere in the query-embedding call path.

### Could query text contain personal or sensitive information?

Yes — a demo invites free-text questions, and nothing currently stops a user from typing something like a
child's name, a specific diagnosis timeline, or other identifying detail into the query box; that text
would be embedded (and, under Option B, sent to Cohere) exactly as typed.

**Proposed input restrictions (for Phase 5 approval, not implemented here):**

1. Add demo-UI guidance telling users not to enter real names, dates of birth, addresses, or other
   identifying details — ask about ASD topics in general terms, not about a specific child.
2. Consider a length cap and a simple pattern check (e.g., flag strings that look like an email, phone
   number, or full date) that warns the user before the query is sent, rather than silently blocking —
   this is a UX/product decision for whoever builds the input box, not a change made by this audit.
3. Do not log raw query text anywhere server-side beyond what already exists; the query cache already
   stores only `sha256(profile|model|dim|input_type|text)` plus the vector, never the text itself
   (`query_embedding.py` module docstring) — this property must be preserved if Option B is implemented.

---

## Phase 4 — Authorization decision matrix

### Scenario A — No external query processing permitted

- Keep `CachedQueryEmbedder` constructed with `inner=None`, exactly as it is today
  (`app/api.py:29`: `CachedQueryEmbedder(embedding_profile, retrieval_profile.query_cache_dir, inner=None)`).
- Cache hits (currently 66/66 on the evaluation set, per T2.3/T2.5) continue to work; any new,
  uncached query text fails closed with HTTP 503 `embedding_unavailable` (`app/api.py`).
- Demo continues to operate only over the pre-cached evaluation question set, or any other text whose
  vector someone manually added to the cache out-of-band.
- **No further owner or Cohere decision is required to adopt this scenario** — it is the status quo.

### Scenario B — Cohere query embedding explicitly authorized

If the project owner authorizes this scenario, it should be scoped as follows (not implemented by this
report):

- **Approved model and scope:** exactly the existing profile `cohere_embed_v4_1536_v1` —
  model `embed-v4.0`, `output_dimension=1536`, `input_type=search_query` — with no change to the
  document-side embeddings. Scope is query text only; this authorization would not extend to re-embedding
  documents or to any other Cohere endpoint.
- **Explicit feature flag required (does not exist today):** `app/api.py:29` currently hardcodes
  `inner=None` with no flag. Enabling Option B would require adding a single, explicit gate — e.g. an
  environment variable such as `ASD_RAG_ENABLE_LIVE_QUERY_EMBEDDING=true` — read once at startup, that
  decides whether `CohereQueryEmbedder` is constructed and passed as `inner`. Absent that variable (or set
  to anything other than the exact enable value), the service must behave exactly as Scenario A.
- **Cache-only default must be preserved outside the approved environment:** the flag must default to
  **off** in every environment except the one explicitly approved (e.g., a single demo deployment), so
  that development, testing, and any other deployment remain fail-closed by default.
- **Document scope within Scenario B — unresolved and must be decided before enabling:** per the license
  review, 13 of 71 embedded sources carry a documented NC-licence conflict with the trial key's data-rights
  terms. Enabling live query embedding does not, by itself, resend any document text — but a retrieved
  answer could surface content *derived from* those 13 documents in a way a user's follow-up query quotes
  or paraphrases. The owner must decide whether this risk is acceptable under Scenario B, or whether
  Scenario B should initially exclude retrieval results drawn from those 13 sources.

### Scenario C — Authorization remains uncertain

- Live query embedding stays **disabled** (identical operational state to Scenario A: `inner=None`).
- The following questions remain open and must be recorded, not resolved by assumption:
  1. Is the 2022-09-07 Terms of Use version still current for the trial key, or does a newer version /
     separate SaaS Agreement apply?
  2. Can a trial-tier Cohere account access the training opt-out in Data Controls?
  3. Has the Cohere Privacy Policy (not yet read in any audit) been reviewed for additional constraints?
  4. Does submitting CC BY-NC-derived query text to Cohere as a data processor constitute "commercial use"
     under those licences? (A legal question outside any audit's authority to answer.)
  5. Does the project owner wish to apply a blanket non-commercial-use policy across the whole corpus
     regardless of licence (a decision already flagged as open in
     `license_audit_2026-11-14.md` §6, item 1), which would also bear on Scenario B's scope?
- This scenario is the operational twin of Scenario A (same code state) but exists to make clear that
  "disabled because we haven't decided" is a distinct, trackable state from "disabled because the owner
  decided not to."

---

## Decision outcome of this report

No scenario has been selected. Phase 4 defines the three options for the project owner to choose among;
choosing one is not within this audit's authority. Scenario A (the current `inner=None` state) remains in
effect until the owner selects B or explicitly records C.
