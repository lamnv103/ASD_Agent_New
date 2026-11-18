# T5.1 §4 — Evidence-to-Answer Architecture Proposal (No External LLM)

**This is a design proposal only — nothing in this document has been implemented.** It extends the
existing, already-working T4 pipeline (`app/router/classifier.py` → `app/retrieval/evidence_gate.py` →
`app/retrieval/citation_validation.py` → `app/answer/answer_generator.py`), rather than replacing it.

## Pipeline stages

```
Evidence Gate output (support_type, age_mismatch per chunk)
        │
        ▼
1. Evidence normalization        — strip boilerplate (image placeholders, table markup, reference
                                    numerals like "[1]"), keep the chunk's factual sentences
        │
        ▼
2. Topic-specific VI template     — EXISTING mechanism (7 templates today), extended per
                                     `template_expansion_plan.md`; fires only when its exact trigger
                                     source(s) are present, exactly as today
        │ (no template matches)
        ▼
3. Evidence-grounded sentence     — NEW, proposed: a constrained, non-generative sentence builder that
   construction                     fills a small set of FIXED Vietnamese sentence frames with values
                                     lifted verbatim from the normalized evidence (numbers, named tools,
                                     named age ranges) — never a free-text paraphrase
        │ (frame cannot be filled safely)
        ▼
4. Citation mapping               — EXISTING mechanism (citation_validation.py), unchanged
        │
        ▼
5. Uncertainty handling            — NEW: explicit confidence label surfaced per answer (not just per
                                     evidence item as today) — "high" only when every evidence item used
                                     is `direct`; otherwise "partial," shown to the user, not hidden
        │
        ▼
6. Safety override                — EXISTING mechanism (dosing refusal, unproven-cure caution),
                                     unchanged, still runs before any of the above
        │
        ▼
7. Extractive fallback            — EXISTING mechanism, as the final, always-safe fallback when stages
                                     2-3 produce nothing
```

## Design rules (binding on any future implementation)

- **No machine translation of technical terms.** "M-CHAT-R/F," "DSM-5," "ADOS-2," drug names, and named
  study acronyms are copied verbatim, never translated or expanded speculatively — this is already the
  convention in the 7 existing templates and must stay so for any new ones.
- **No inference beyond evidence.** Stage 3's sentence frames may only be filled with a value that
  appears *verbatim* in the normalized evidence (a number, a named tool, a named age). If a frame has a
  slot with no matching value in the evidence, that frame is not used — the question falls to extractive
  fallback (stage 7) instead of a frame with a blank or a guessed value.
- **Citation mapping is per-sentence, not per-answer.** Every frame-filled sentence records which
  specific evidence item supplied its value, so citation accuracy stays as strict as the existing
  `citation_validation.py` guarantees — this is a natural extension of the existing "only cite what the
  answer actually used" rule already in `app/api.py`.
- **Uncertainty is shown, not smoothed over.** An answer built partly from `indirect`/`generic` evidence
  must say so (reusing the existing per-source note mechanism from T4 Phase 2/7, now also summarized at
  the whole-answer level).
- **Safety override stays first in the pipeline, unchanged.** Nothing in this proposal touches
  `is_dosing_question`/`_is_unproven_cure_question` or where they run.

## 5 worked examples (built from real, already-retrieved evidence — no evidence simulated)

### Example 1 — qe028 "Dấu hiệu sớm của tự kỷ ở trẻ 18 tháng là gì?" (Group C, direct support)

- **Evidence available** (`CDC-ASD-SIGNS`, `direct`): "Avoids or does not keep eye contact · Does not
  respond to name by 9 months of age · Does not point to show you something interesting by 18 months of
  age · ..." (a literal bulleted list with specific ages attached to specific signs).
- **Proposed answer structure**: "Theo CDC, một số dấu hiệu cảnh báo cần chú ý ở trẻ khoảng 18 tháng gồm:
  không chỉ tay để cho người khác xem vật mình thích (18 tháng), không phản ứng khi được gọi tên (9
  tháng), tránh giao tiếp bằng mắt. Đây là dấu hiệu cảnh báo, khác với các mốc phát triển vận động/nhận
  thức thông thường." — built by Stage 3 filling an "age → sign" frame directly from the bulleted list,
  one bullet per frame instance, each citing the same source.
- **Refusal condition**: if the evidence for a given age bullet is missing (e.g. a question asks about
  "36 tháng" and no 36-month-specific sign exists in `CDC-ASD-SIGNS`), that age is omitted rather than
  guessed; if no age-matching bullet exists at all, falls to extractive fallback.

### Example 2 — qe036 "M-CHAT-R/F là gì và độ chính xác ra sao?" (Group C, direct support, numeric evidence)

- **Evidence available** (`ASD-CSV-002`/`ASD-CSV-029`, `direct`): "sensitivity (0.85) and specificity
  (0.99)... PPV is 0.48 for autism and 0.95 for any developmental disorder... takes about 10 min to
  complete... score of 8 or higher indicates high risk."
- **Proposed answer structure**: "M-CHAT-R/F là một bảng sàng lọc tự kỷ, thường mất khoảng 10 phút để
  hoàn thành. Theo nghiên cứu, công cụ này có độ nhạy 0.85 và độ đặc hiệu 0.99; điểm từ 8 trở lên được
  coi là nguy cơ cao. Đây là công cụ sàng lọc, không phải chẩn đoán xác định — cần đánh giá chuyên môn
  tiếp theo." — every number is copied verbatim from the evidence into a fixed "công cụ X có độ nhạy Y,
  độ đặc hiệu Z" frame; the closing caveat sentence is a **fixed, non-evidence-derived safety sentence**
  already used elsewhere (consistent with existing diagnosis-process template wording).
- **Refusal condition**: if sensitivity/specificity numbers are not both present and attributable to one
  source, do not fill the numeric frame — show the tool's name/purpose only, or fall back to extractive
  excerpt for the numbers.

### Example 3 — qe049 "Làm sao hỗ trợ trẻ tự kỷ hòa nhập ở trường phổ thông?" (Group C, direct)

- **Evidence available** (`ASD-CSV-019`, `direct`): "Included interventions targeted at least one level
  of the school environment: the autistic children, the peers, the staff, and/or the physical
  environment."
- **Proposed answer structure**: "Các can thiệp hỗ trợ hòa nhập ở trường thường tác động ở một hoặc nhiều
  cấp độ: bản thân học sinh tự kỷ, các bạn cùng lớp, giáo viên/nhân viên nhà trường, và môi trường vật lý
  của lớp học." — a direct, faithful rendering of the 4-level list structure, each item copied from the
  evidence's own enumeration, no added recommendation beyond what the review states.
- **Refusal condition**: if the evidence gave only a general claim with no enumerable list (as happens
  for many `narrative`-style sources), stage 3 does not attempt to invent a list — falls back to
  extractive excerpt.

### Example 4 — qe047 "Cải thiện giấc ngủ cho trẻ tự kỷ không dùng thuốc thế nào?" (Group C, direct,
but table-formatted evidence — an important edge case)

- **Evidence available** (`ASD-OA-PMC7407189`): a markdown table ("ABCs of SLEEPING" mnemonic) with
  columns Practice Area / Recommendation / Level of Empirical Support.
- **Proposed answer structure**: Stage 1 (normalization) must specifically handle table-formatted
  evidence — extracting `Practice Area` + `Recommendation` pairs as frame inputs, dropping the
  `Level of Empirical Support` column from the user-facing sentence but keeping it available for the
  per-answer uncertainty label (Stage 5): if the table marks a given recommendation's evidence level as
  low, the final sentence should carry a softer verb ("có thể giúp" vs. "giúp"). **This is the one
  example here that needs new normalization logic beyond what the other four need** — tables are common
  in this corpus (seen again in the melatonin/antihistamine dosing tables from T3/T4's q058 investigation)
  and are not safely handled by naive sentence-frame filling without first parsing the table structure.
- **Refusal condition**: if table parsing cannot cleanly separate recommendation from evidence level,
  fall back to showing the table excerpt as-is (current extractive fallback behavior) rather than risk
  misattributing an evidence-level claim.

### Example 5 — qe056/qe057 "Chương trình huấn luyện kỹ năng người chăm sóc của WHO gồm những gì?" (Group
C, direct, multi-document)

- **Evidence available** (`WHO-CST-PARTICIPANTS-2022`): "Session 6 focuses on teaching skills for
  everyday living... Sessions 7 and 8 focus on promoting positive behaviour and reducing challenging
  behaviours. Session 9 focuses on caregiver well-being..." — i.e. a numbered-session structure already
  present verbatim in the evidence.
- **Proposed answer structure**: "Chương trình Huấn luyện Kỹ năng cho Người Chăm sóc (Caregiver Skills
  Training) của WHO dành cho cha mẹ/người chăm sóc trẻ 2–9 tuổi có chậm phát triển hoặc khuyết tật, gồm
  nhiều buổi theo nhóm — ví dụ buổi 6 dạy kỹ năng sinh hoạt hằng ngày, buổi 7–8 về hành vi tích cực, buổi
  9 về sức khỏe tinh thần của người chăm sóc." — a direct rendering of the session list; "Caregiver
  Skills Training" is kept in English in parentheses as the official program name (per the "no machine
  translation of technical/proper names" rule).
- **Refusal condition**: if only a partial session range is found in evidence (e.g. sessions 6-9 but not
  1-5), the answer must say "gồm nhiều buổi, trong đó..." (among which...) rather than implying a
  complete session list — this is exactly the kind of completeness risk the task's "không mở rộng câu
  trả lời chỉ để làm cho nó có vẻ đầy đủ" rule is about, worth naming explicitly in the design rather than
  leaving implicit.

## Where this proposal does NOT help

- Group E's `generic`-only-support questions (qe021, qe022, qe033, qe053, qe105) — Stage 3 has no safe
  frame to fill when the evidence itself isn't confirmed on-topic; these stay in extractive fallback or
  insufficient-evidence under this design, same as today.
- Group F (50 cache-blocked questions) — this proposal operates entirely downstream of retrieval; it
  cannot answer a question that was never embedded/retrieved in the first place.
- The q033/qe045/qe081 ADHD-confusion cases — Stage 3 would faithfully render whatever evidence the gate
  hands it, including the wrong-context ADHD chunk; this proposal is not a fix for that (see
  `q033_context_analysis.md`) and should not be applied to those two questions until that is resolved.
