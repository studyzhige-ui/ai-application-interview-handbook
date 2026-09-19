# Phase 2B Data Validation

更新日期：2026-09-11

| Check | Result |
|---|---|
| ACTIVE Canonical parsed | ✅ 235 / expected 235 |
| Frozen HUMAN-A source IDs parsed | ✅ 279 / expected 279 |
| Duplicate QID | ✅ none |
| Duplicate Sxxx heading | ✅ none |
| Source Count == unique Evidence Sources | ✅ all questions passed |
| Evidence Source outside S001–S279 | ✅ none |
| Canonical-covered source flows | 278 / 279 |
| Uncovered source flows | 1 |

The builder exits non-zero before writing final analysis if any hard consistency check fails.

Uncovered: `S271`
