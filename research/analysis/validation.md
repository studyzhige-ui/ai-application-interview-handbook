# Phase 2B Data Validation

更新日期：2026-09-11

| Check | Result |
|---|---|
| ACTIVE Canonical parsed | ✅ 229 / expected 229 |
| Frozen HUMAN-A source IDs parsed | ✅ 279 / expected 279 |
| Duplicate QID | ✅ none |
| Duplicate Sxxx heading | ✅ none |
| Source Count == unique Evidence Sources | ✅ all questions passed |
| Evidence Source outside S001–S279 | ✅ none |
| Canonical-covered source flows | 251 / 279 |
| Uncovered source flows | 28 |

The builder exits non-zero before writing final analysis if any hard consistency check fails.

Uncovered: `S076`, `S077`, `S078`, `S082`, `S085`, `S099`, `S103`, `S113`, `S121`, `S128`, `S141`, `S142`, `S143`, `S153`, `S155`, `S157`, `S160`, `S186`, `S190`, `S196`, `S197`, `S213`, `S215`, `S219`, `S221`, `S239`, `S261`, `S271`
