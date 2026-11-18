# T5.10 — Targeted Medication Safety Classifier Repair

## Final status

```text
T5_10_COMPLETE
```

All three original T5.9 defects were reproduced before code changes, repaired within the medication classifier, and checked against positive and negative intent boundaries. B8's exact historical behavior and `ACCEPT_WITH_DOCUMENTED_RESIDUAL_RISK` decision remain unchanged. Required regression suites were executed and their results and superseded historical expectations are documented.

## What changed

- Direct dosage questions are detected without requiring a number or named medication. Dose-related research, efficacy, risk, and side-effect questions are kept outside automatic dosage refusal unless the text also expresses a self-management action.
- Self-increase, self-decrease, self-adjustment, and self-stop are distinguished from supervised medication-switch questions and switching research.
- The bare phrase `thuốc tâm thần` no longer triggers a refusal; explicit dose and self-management language with the same phrase still do.
- Focused tests cover 34 intent queries plus a separate non-prescriptive medication-choice fallback check.

The classifier remains rule-based and lexical. Medication-choice questions with no evidence produce the existing insufficient-evidence fallback; with retrieved evidence, the observed harness output is an explicitly labeled source excerpt rather than a personalized medication recommendation. This does not establish clinical suitability or validate the content.

## Verification summary

- Original defects A2, B4, and D4: reproduced pre-change, then corrected.
- Focused T5.10 tests: 35 passed.
- Existing medication-safety generator tests: 30 passed.
- Full unit suite: 449 passed.
- Full integration suite: 50 passed.
- T5.8 adversarial set: 29/31 match its archived expected modes. The two differences, B5 supervised switch and B8, follow the newer mandatory T5.10 boundaries; both pass under those clarified criteria. The archival script was preserved.
- T2.3 retrieval: 66/66 rankings identical and zero metric mismatches. The full artifact check is partial because five retrieval-code hashes differ from the older report snapshot; metric values and run data are identical after excluding those hashes and timing/log fields.
- Reconstructed 23-template check: 23/23 returned template modes, with all 22 cases that have recorded baseline modes unchanged.
- Independent 32-question set: same routing and mode distribution.
- T5.7 22-question set: 22/22 modes unchanged.
- Ruff: all changed Python files passed.

See [baseline_reproduction.md](baseline_reproduction.md), [intent_boundary_test_matrix.md](intent_boundary_test_matrix.md), [implementation_changes.md](implementation_changes.md), [adversarial_test_results.md](adversarial_test_results.md), [b8_preservation_check.md](b8_preservation_check.md), and [regression_report.md](regression_report.md) for detailed evidence and commands.

## Boundaries and limitations

No templates, Evidence Gate, retrieval implementation, embeddings, corpus, frozen benchmarks, or database configuration were changed. FTS regression checks used the existing read-only T5.7 harness; FTS was not integrated into the demo API. No database writes, external embedding/model calls, sealed data access, clinical validation, or user-readiness claim is part of this result.

The T5.8 script retains its historic expectations for B5 and B8. Those expectations are superseded by T5.10's explicit clarifications and remain visible as two differences in the regression report rather than being silently rewritten.

The T5.8 harness briefly wrote its run output over the existing generated-results JSON. I restored the B5/B8 rows to the archived refusal outcomes; byte-for-byte identity with the prior file could not be verified because no backup was present. The regression report records this restoration. No frozen benchmark labels or source records were modified.
