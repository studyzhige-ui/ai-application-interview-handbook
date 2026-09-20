#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_BLOCKS = {
    "curriculum/01-python": 13,
    "curriculum/02-fastapi": 16,
    "curriculum/03-backend-engineering": 22,
    "curriculum/04-mysql": 23,
    "curriculum/05-redis": 24,
    "curriculum/06-vector-db": 16,
    "curriculum/07-llm-foundation": 14,
    "curriculum/08-rag": 14,
    "curriculum/09-agent": 24,
    "curriculum/10-system-design": 19,
}
FROZEN_CANONICAL_MAX_SOURCE = 279
EXPECTED_ACTIVE_CANONICAL = 235

errors: list[str] = []


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        errors.append(f"missing required file: {path}")
        return ""
    return p.read_text(encoding="utf-8")


def require(path: str, needle: str) -> None:
    text = read(path)
    if needle not in text:
        errors.append(f"{path}: missing required text: {needle}")


def forbid(path: str, needle: str) -> None:
    text = read(path)
    if needle in text:
        errors.append(f"{path}: stale text remains: {needle}")


# Curriculum file counts and contiguous numbering.
total = 0
for module, expected in EXPECTED_BLOCKS.items():
    docs = sorted((ROOT / module / "docs").glob("*.md"))
    total += len(docs)
    if len(docs) != expected:
        errors.append(f"{module}: expected {expected} docs, found {len(docs)}")
        continue
    nums = []
    for p in docs:
        m = re.match(r"^(\d+)-", p.name)
        if not m:
            errors.append(f"{module}: non-numbered doc {p.name}")
            continue
        nums.append(int(m.group(1)))
    if nums != list(range(1, expected + 1)):
        errors.append(f"{module}: numbering mismatch {nums}")

if total != 185:
    errors.append(f"Curriculum total must be 185, found {total}")

# Products are a top-level source-study layer, not a Curriculum subdirectory.
legacy_products = ROOT / "curriculum/09-agent/products"
if legacy_products.exists():
    errors.append("legacy products directory still exists under curriculum/09-agent")
for product in ("codex", "claude-code", "deepseek-harness", "deer-flow"):
    product_dir = ROOT / "products/agent" / product
    expected_files = {
        "README.md",
        "01-context-lifecycle.md",
        "02-memory-lifecycle.md",
        "03-tool-lifecycle.md",
        "04-engineering-evaluation.md",
    }
    actual_files = {p.name for p in product_dir.glob("*.md")} if product_dir.exists() else set()
    if actual_files != expected_files:
        errors.append(f"products/agent/{product}: expected {sorted(expected_files)}, found {sorted(actual_files)}")

# Current-state semantic checks.
require("guide/knowledge-map.md", "## 04. [MySQL](../curriculum/04-mysql/README.md) ✅ — 23 blocks")
forbid("guide/knowledge-map.md", "## 04. [MySQL](../curriculum/04-mysql/README.md) ✅ — 24 blocks")
forbid("interview/canonical/progress.md", "Agent23章")
forbid("interview/canonical/progress.md", "roadmap/documentation-style-guide.md")
forbid("interview/canonical/schema.md", "采集阶段已经结束")
require("interview/canonical/schema.md", "S280+")
forbid("curriculum/09-agent/interview/面试易错点.md", "按23章")
forbid("references/agent/README.md", "研究层 Capability")
require("README.md", "products/     成熟 AI 系统怎样把这些机制组合成真实产品")
require("curriculum/09-agent/README.md", "../../products/agent/README.md")
forbid("curriculum/09-agent/README.md", "products/codex/README.md")
forbid("interview/canonical/module-index.md", "Frozen Research 层")
require("guide/audits/final-quality-audit.md", "Curriculum Blocks          185")
require("market/analysis/knowledge-gap-analysis.md", "S280–S288")
require("guide/audits/history/README.md", "2026-09-12")
require("market/analysis/history/README.md", "2026-09-11")

# Agent interview link labels must match the actual docs/NN target.
agent_q = read("curriculum/09-agent/interview/高频面试题.md")
for m in re.finditer(r"\[([^\]]*第(\d+)章[^\]]*)\]\(\.\./docs/(\d+)-[^)]+\)", agent_q):
    shown = int(m.group(2))
    target = int(m.group(3))
    if shown != target:
        errors.append(f"Agent interview chapter label mismatch: shown {shown}, target {target}: {m.group(1)}")

# Current Market evidence is dynamic; derive it from Batch files and require current entry pages to agree.
batch_files = sorted((ROOT / "market/interviews").glob("batch-*.md"))
source_ids: list[int] = []
for p in batch_files:
    source_ids.extend(int(x) for x in re.findall(r"^## S(\d{3})\b", p.read_text(encoding="utf-8"), re.M))
unique_ids = sorted(set(source_ids))
if not unique_ids:
    errors.append("no HUMAN-A source IDs found")
else:
    if unique_ids != list(range(1, max(unique_ids) + 1)):
        errors.append("HUMAN-A source IDs are not contiguous")
    current_max = max(unique_ids)
    current_count = len(unique_ids)
    market = read("market/README.md")
    inbox = read("market/monitoring/inbox.md")
    range_text = f"S001–S{current_max:03d}"
    batch_text = f"{len(batch_files)} Batch"
    if range_text not in market or batch_text not in market:
        errors.append(f"market/README.md does not match current evidence: {range_text} / {batch_text}")
    if range_text not in inbox:
        errors.append(f"market/monitoring/inbox.md does not match current evidence range: {range_text}")
    print(f"Market evidence: {current_count} sources / {len(batch_files)} batches / max S{current_max:03d}")

# Frozen Canonical baseline stays separate from current Market evidence.
canonical_readme = read("interview/canonical/README.md")
if "S001–S279" not in canonical_readme or "235" not in canonical_readme:
    errors.append("interview/canonical/README.md must declare S001–S279 / 235 ACTIVE frozen baseline")

canonical_files = [
    p for p in (ROOT / "interview/canonical").glob("*.md")
    if p.name not in {"README.md", "schema.md", "module-index.md", "progress.md", "global-audit.md", "source-coverage-audit.md"}
]
seen_evidence: set[int] = set()
for p in canonical_files:
    for sid in re.findall(r"\bS(\d{3})\b", p.read_text(encoding="utf-8")):
        seen_evidence.add(int(sid))
if seen_evidence and max(seen_evidence) > FROZEN_CANONICAL_MAX_SOURCE:
    errors.append(f"Canonical evidence leaked beyond frozen S279: max S{max(seen_evidence):03d}")

# Current-state files must not point back to removed top-level research/ or roadmap/ paths.
current_state_files = [
    "README.md",
    "curriculum/README.md",
    "products/README.md",
    "products/agent/README.md",
    "products/agent/codex/README.md",
    "products/agent/claude-code/README.md",
    "products/agent/deepseek-harness/README.md",
    "products/agent/deer-flow/README.md",
    "practice/README.md",
    "market/README.md",
    "interview/README.md",
    "interview/canonical/README.md",
    "interview/canonical/progress.md",
    "interview/canonical/schema.md",
    "interview/canonical/module-index.md",
    "references/README.md",
    "references/agent/README.md",
    "references/backend-engineering/README.md",
    "references/fastapi/README.md",
    "guide/README.md",
    "guide/knowledge-map.md",
    "guide/learning-path.md",
    "guide/documentation-style-guide.md",
    "guide/audits/README.md",
    "guide/audits/final-quality-audit.md",
    "tools/README.md",
    ".github/workflows/rebuild-market-analysis.yml",
    ".github/workflows/validate-handbook.yml",
]
legacy_path = re.compile(r"(?<![A-Za-z0-9_-])(?:research|roadmap)/")
legacy_products_path = re.compile(r"curriculum/09-agent/products/")
for path in current_state_files:
    for line_no, line in enumerate(read(path).splitlines(), 1):
        if legacy_path.search(line):
            errors.append(f"{path}:{line_no}: removed top-level path remains: {line.strip()}")
        if legacy_products_path.search(line):
            errors.append(f"{path}:{line_no}: legacy Agent products path remains: {line.strip()}")

if errors:
    print("\nRepository semantic validation FAILED:")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print(f"Curriculum blocks: {total}")
print(f"Frozen Canonical baseline: S001–S{FROZEN_CANONICAL_MAX_SOURCE} / {EXPECTED_ACTIVE_CANONICAL} ACTIVE")
print("Repository semantic validation: PASS")
