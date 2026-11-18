# T5.6 Phase 5 — Answer Quality Validation

**Method, stated up front**: for each of the 6 reference questions, this task (a) checked live whether
the question is already cached and answered today, and (b) for cache-miss questions, **actually ran** the
proposed Phase-4 pipeline offline (EXP-1b retrieval → a `RetrievedChunk` adapter, built as a one-off test
harness, not shipped code → the real, unmodified `evidence_gate.assess()` → the real, unmodified
`answer_generator.generate()` → the real, unmodified `citation_validation.validate()`) to see what it
would actually produce — not a prediction, a measured result from running the real downstream code
against newly-adapted evidence. `app/api.py` was never touched; the test harness lives entirely outside
the app's import graph. Where this measured result is a genuine, cited Vietnamese answer, it is reported
as such. **Where the corpus does not support a claim, this report says so and does not supply one from
the model's own background knowledge** — this rule was checked for every question below, not just
asserted once.

## 1. "ASD là gì?"

- **Cache status today**: cache miss (HTTP 503, `QUERY_NOT_CACHED`) — no answer of any kind.
- **Real evidence found**: EXP-1b (anchor-concept-only fallback, since this question contains no
  specific topic term) retrieves `CDC-ASD-CLINICAL` at rank 4 of a small result set, alongside
  `ASD-OA-PMC13005892`, `ASD-OA-PMC12620806`, `ASD-SUP-PMC10783429`, `ASD-CSV-029`.
- **Measured result from running the real pipeline**: `topic_template` (the `asd_definition` catch-all)
  fired. Produced text (verbatim, this task's test run): *"Rối loạn phổ tự kỷ (Autism Spectrum Disorder –
  ASD) là một rối loạn phát triển thần kinh, ảnh hưởng đến giao tiếp, tương tác xã hội và có thể biểu hiện
  qua các hành vi, sở thích hoặc hoạt động hạn chế, lặp lại. Biểu hiện và nhu cầu hỗ trợ khác nhau ở mỗi
  người."* — a structured Vietnamese answer, no raw English, no internal metadata leaked, matching the
  Answer Quality Reference exactly.
- **Supported claims**: "neurodevelopmental disorder," "affects communication and social interaction,"
  "restricted/repetitive behaviors/interests," "presentation and support needs vary by individual" — all
  directly from `CDC-ASD-CLINICAL`'s own text (the same source the live, dense-powered catch-all template
  already uses when this exact question is cached under a different phrasing, e.g. `qe001`).
- **Sources**: `CDC-ASD-CLINICAL` (primary), with `ASD-OA-PMC13005892`/`ASD-OA-PMC12620806`/
  `ASD-SUP-PMC10783429`/`ASD-CSV-029` also passing the Gate as supporting evidence.
- **Limitation**: this result depends on the EXP-1b fallback (Phase 2's addendum), which is itself an
  unshipped experiment, not a built pipeline. The live demo today gives no answer at all to this exact
  phrasing.

## 2. "Trẻ tự kỷ có những biểu hiện gì?" (What signs/manifestations does an autistic child show?)

- **Cache status today**: cache miss.
- **Real evidence found**: EXP-1b retrieves `ASD-CSV-084` ("The role of augmentative and alternative
  communication...") and `ASD-SUP-PMC13414371` ("Interventions to Promote Communication..."), both about
  communication *interventions*, not a general signs/characteristics overview.
- **Why**: this question's Vietnamese word "biểu hiện" (manifestation) is **not a trigger in either
  glossary** (confirmed this task — neither the 63-entry nor the 94-entry glossary has it; the closer
  match, "dấu hiệu," is a different word the question does not use). A genuinely new, previously
  undocumented vocabulary gap, found only by testing this exact reference question.
- **Measured result from running the real pipeline**: `extractive_fallback` — raw English excerpts,
  correctly and honestly labeled as excerpts, not synthesized Vietnamese prose, and not the structured
  answer the reference calls for.
- **Supported claims**: none synthesized; the fallback excerpts themselves discuss communication
  interventions, only tangentially related to "what signs does a child show."
- **Sources**: `ASD-CSV-084`, `ASD-SUP-PMC13414371` (shown as raw excerpts only).
- **Limitation, stated plainly**: this question does not meet the Answer Quality Reference today, and
  this task's experiments do not close the gap — the root cause is a vocabulary gap ("biểu hiện" unmapped)
  compounded by no existing template addressing general signs/characteristics as a single topic (the live
  `signs_by_age` template specifically requires an age to be named, which this question does not do).

## 3. "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?" (Early signs at 18 months)

- **Cache status today**: **already cached and answered** — `topic_template` (`signs_by_age`), HTTP 200,
  verified live this task (Phase 0, §9).
- **Real evidence**: `CDC-ASD-SIGNS`, already cited in the live response.
- **Measured result**: already meets the Answer Quality Reference today, with no experimental change
  needed. Included here only because the task listed it as one of the 6 to evaluate.
- **Supported claims / sources / limitation**: unchanged from the live system's existing, previously-
  audited behavior (T5.3/T5.4); not re-litigated in this task.

## 4. "ASD và ADHD khác nhau như thế nào?" (How do ASD and ADHD differ?)

- **Cache status today**: cache miss.
- **Real evidence found**: EXP-1 (the `adhd` concept is recognized) retrieves `ASD-CSV-078` ("Variations
  in Anxiety and Related Psychiatric Comorbidities...") and `ASD-CSV-062` ("The Presence of Comorbid
  ADHD and Anxiety Symptoms...") — both genuinely about ASD+ADHD co-occurrence, passing the Gate as
  "direct" support for the `adhd` term.
- **Measured result from running the real pipeline**: `extractive_fallback` — these comorbidity-
  prevalence/statistics papers do not contain a clean, citable sentence stating "ASD and ADHD are two
  distinct, separately-diagnosable conditions that can co-occur," which is what the question actually
  asks (the same granularity mismatch T5.5 found for `ie001`, now reproduced on the task's own reference
  wording of the same question).
- **Supported claims**: the retrieved evidence supports *that ASD and ADHD frequently co-occur and have
  been studied together*, not a definitional "are they the same or different" statement.
- **Sources**: `ASD-CSV-078`, `ASD-CSV-062` (shown as raw excerpts only, per `extractive_fallback`'s
  design — never presented as if they directly answered the definitional question).
- **Limitation, stated plainly**: no chunk in this corpus, found by any method available to this task,
  states the ASD-vs-ADHD distinction explicitly. **This report does not supply that distinction from the
  model's own background knowledge** — per the task's explicit instruction, the honest answer here is
  "the corpus has relevant context but not a direct answer to this specific framing," not a fabricated
  definitional sentence.

## 5. "Trẻ tự kỷ có thể gặp khó khăn về ngôn ngữ không?" (Can autistic children have language difficulties?)

- **Cache status today**: cache miss.
- **Real evidence found**: **zero** — neither EXP-1 nor EXP-1b's fallback found any non-anchor concept,
  because the bare word "ngôn ngữ" (language) is not itself a trigger in either glossary (only narrower
  phrases like "chậm nói"/speech delay or "giao tiếp"/communication are), and this question uses the
  broader word alone.
- **Measured result**: no retrieval attempt could even be meaningfully constructed; the question would
  fail closed under the proposed design exactly as it does today (cache miss / no evidence), not produce
  a wrong answer.
- **Cross-reference to Phase 3 of T5.5**: this corpus has only **1** chunk matching "speech delay" and 6
  matching "language delay" corpus-wide — the thinnest topic found in that audit. Even a perfect
  retrieval/glossary fix would have very little content to work with here.
- **Limitation, stated plainly**: this is simultaneously a vocabulary gap (Phase 1's domain) and a
  genuine thin-corpus-coverage topic (T5.5 Phase 3's finding, re-confirmed relevant here) — **this
  report does not invent a Vietnamese answer about language difficulties in autism from general
  knowledge**, consistent with the task's explicit prohibition.

## 6. "Người tự kỷ có thể gặp khó khăn về giấc ngủ không?" (Can autistic people have sleep difficulties?)

- **Cache status today**: cache miss.
- **Real evidence found**: EXP-1 recognizes the `giac ngu` (sleep) concept and retrieves
  `ASD-OA-PMC12620806` and `ASD-OA-PMC7407189` ("Sleeping without Prescription: Management of Sleep
  Disorders..."), among others — the exact source behind the live `sleep_nonpharma`/`melatonin_efficacy`
  templates.
- **Measured result from running the real pipeline**: `topic_template` (`sleep_nonpharma`) fired.
  Produced text (verbatim, this task's test run): *"Rối loạn giấc ngủ là tình trạng đồng mắc phổ biến ở
  trẻ tự kỷ (gặp ở khoảng 50-80% trẻ). Theo một tổng quan, các biện pháp không dùng thuốc thường được
  khuyến nghị thử trước, trong đó khuyến nghị có mức bằng chứng mạnh nhất là giữ giờ đi ngủ, giờ thức dậy
  và giờ ngủ trưa cố định, đều đặn mỗi ngày..."* — a structured Vietnamese answer, correctly scoped
  (explicitly notes it is "one of several recommendations... not fully extracted here," matching T5.3's
  own honesty-scoping fix for this exact template), with real citations.
- **Supported claims**: sleep-disorder comorbidity prevalence (50–80%), and the single highest-evidence
  non-pharmacological recommendation (consistent bedtime/wake/nap schedule) — both directly from
  `ASD-OA-PMC7407189`.
- **Sources**: `ASD-OA-PMC7407189` (primary), `ASD-OA-PMC12620806`/`ASD-CSV-095`/`ASD-OA-PMC4271434`
  also passing the Gate.
- **Limitation**: same as question 1 — depends on the unshipped EXP-1 experiment, not production code.

## Summary

| # | Question | Today | Proposed-pipeline result (measured, not predicted) | Meets reference? |
|---|---|---|---|---|
| 1 | ASD là gì? | cache miss | `topic_template` (asd_definition), via EXP-1b | **Yes**, under the proposal |
| 2 | Trẻ tự kỷ có những biểu hiện gì? | cache miss | `extractive_fallback` (vocabulary gap: "biểu hiện" unmapped) | **No** |
| 3 | Dấu hiệu sớm... 18 tháng | **already answered today** | n/a | **Yes**, already |
| 4 | ASD vs ADHD khác nhau | cache miss | `extractive_fallback` (granularity mismatch, no definitional chunk exists) | **No** |
| 5 | Khó khăn ngôn ngữ | cache miss | no evidence at all (vocabulary gap + thin corpus) | **No** |
| 6 | Khó khăn giấc ngủ | cache miss | `topic_template` (sleep_nonpharma), via EXP-1 | **Yes**, under the proposal |

**3 of 6 meet the Answer Quality Reference** (1 already live, 2 only under the unshipped Phase 4
proposal); **3 of 6 do not**, for three different, specifically-named reasons (a new vocabulary gap, a
granularity mismatch no lexical method can resolve, and a combined vocabulary+thin-corpus gap) — not
glossed over as one generic "insufficient evidence" outcome.
