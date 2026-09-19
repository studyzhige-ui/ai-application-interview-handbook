#!/usr/bin/env python3
"""Validate frozen HUMAN-A source coverage after the reviewed Phase 2B audit.

A source may be either:
1) mapped to >=1 Canonical Question, or
2) explicitly documented as VALID-UNMAPPED in phase2b_canonical_audit.json.
Anything else is an error.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QDIR = ROOT / "interview" / "canonical"
IDIR = ROOT / "market" / "interviews"
OUT = ROOT / "market" / "analysis" / "source-coverage-validation.md"
AUDIT = json.loads((ROOT / "tools" / "phase2b_canonical_audit.json").read_text(encoding="utf-8"))

MODULE_FILES = [
    "python.md", "fastapi.md", "ai-backend-engineering.md", "mysql.md", "redis.md",
    "vector-db.md", "llm-foundation.md", "rag.md", "agent-harness.md", "system-design.md",
]
EXPECTED = {f"S{i:03d}" for i in range(1, 280)}


def main() -> None:
    corpus_ids: set[str] = set()
    for path in sorted(IDIR.glob("batch-*.md")):
        corpus_ids.update(re.findall(r"^##\s+(S\d{3})\s+", path.read_text(encoding="utf-8"), re.M))
    if corpus_ids != EXPECTED:
        raise SystemExit(f"frozen source baseline mismatch: missing={sorted(EXPECTED-corpus_ids)}, extra={sorted(corpus_ids-EXPECTED)}")

    mapped: set[str] = set()
    active_qids: set[str] = set()
    for filename in MODULE_FILES:
        text = (QDIR / filename).read_text(encoding="utf-8")
        qmatches = list(re.finditer(r"^###\s+((?:PY|FASTAPI|AIBE|MYSQL|REDIS|VDB|LLM|RAG|AGENT|SD)-\d{3})\s+·\s+", text, re.M))
        for i, m in enumerate(qmatches):
            qid = m.group(1)
            if qid in active_qids:
                raise SystemExit(f"duplicate qid: {qid}")
            active_qids.add(qid)
            end = qmatches[i+1].start() if i+1 < len(qmatches) else len(text)
            block = text[m.start():end]
            em = re.search(r"^- \*\*Evidence Sources\*\*：(.+?)$", block, re.M)
            if not em:
                raise SystemExit(f"missing evidence: {qid}")
            evidence = set(re.findall(r"S\d{3}", em.group(1)))
            cm = re.search(r"^- \*\*Source Count\*\*：.*?(\d+)", block, re.M)
            if not cm or int(cm.group(1)) != len(evidence):
                raise SystemExit(f"source count mismatch: {qid}")
            if evidence - EXPECTED:
                raise SystemExit(f"out-of-baseline evidence: {qid}: {sorted(evidence-EXPECTED)}")
            mapped.update(evidence)

    expected_active = int(AUDIT["expected_active_after"])
    if len(active_qids) != expected_active:
        raise SystemExit(f"active canonical mismatch: {len(active_qids)} != {expected_active}")

    valid_unmapped = set(AUDIT.get("valid_unmapped", {}))
    unexpected = EXPECTED - mapped - valid_unmapped
    invalid_declared = valid_unmapped & mapped
    unknown_declared = valid_unmapped - EXPECTED
    if unexpected or invalid_declared or unknown_declared:
        raise SystemExit(
            f"coverage invalid: unexpected={sorted(unexpected)}, valid_unmapped_but_mapped={sorted(invalid_declared)}, unknown_valid_unmapped={sorted(unknown_declared)}"
        )

    lines = [
        "# Phase 2B Source Coverage Validation",
        "",
        "更新日期：2026-09-11",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| Frozen HUMAN-A | ✅ {len(EXPECTED)} / 279 |",
        f"| ACTIVE Canonical | ✅ {len(active_qids)} / {expected_active} |",
        f"| Mapped to >=1 Canonical | ✅ {len(mapped)} |",
        f"| Documented VALID-UNMAPPED | ✅ {len(valid_unmapped)} |",
        "| Unexpected uncovered | ✅ 0 |",
        "| VALID-UNMAPPED accidentally mapped | ✅ 0 |",
        "| Evidence outside S001–S279 | ✅ 0 |",
        "| Source Count != unique Evidence Sources | ✅ 0 |",
        "",
    ]
    if valid_unmapped:
        lines += ["## VALID-UNMAPPED", ""]
        for sid in sorted(valid_unmapped):
            lines.append(f"- `{sid}`：{AUDIT['valid_unmapped'][sid]}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
