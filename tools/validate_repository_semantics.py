#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Counts come from the current files. The regenerated registry must agree;
# frozen interview evidence remains an independent, explicitly fixed baseline.
import json
from sync_outer_navigation import inventory
current_inventory = inventory(ROOT)
EXPECTED_BLOCKS = {'curriculum/' + m['directory']: m['chapter_count']
                   for m in current_inventory['modules']}
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

if json.loads(read("guide/navigation-index.json")) != current_inventory:
    errors.append("learning inventory drift: run tools/sync_outer_navigation.py --apply")

# Products are a top-level source-study layer, not a Curriculum subdirectory.
legacy_products = ROOT / "curriculum/09-agent/products"
if legacy_products.exists():
    errors.append("legacy products directory still exists under curriculum/09-agent")
# Each product defines its own execution/readership sequence. Validate the
# actual indexed sequence and source boundary, not a forced four-theme template.
expected_products = {
    "codex": "openai/codex",
    "claude-code": "studyzhige-ui/claude-code-source-private",
    "deepseek-harness": "deepseek-ai/deepseek-harness",
    "deer-flow": "bytedance/deer-flow",
}
indexed_products = {Path(item["readme"]).parent.name: item for item in current_inventory["products"]}
if set(indexed_products) != set(expected_products):
    errors.append(f"product modules mismatch: {sorted(indexed_products)}")
agent_products_readme = read("products/agent/README.md")
for product, repository in expected_products.items():
    item = indexed_products.get(product)
    if not item:
        continue
    if not item["reading_order"] or set(item["reading_order"]) != set(item["chapters"]):
        errors.append(f"products/agent/{product}: incomplete product-specific reading order")
    numbers = [int(Path(path).name[:2]) for path in item["reading_order"]]
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"products/agent/{product}: chapter numbers differ from reading order")
    if item["source_repository"] != repository or not re.fullmatch(r"[0-9a-f]{40}", item["source_commit"] or ""):
        errors.append(f"products/agent/{product}: missing exact source repository/commit boundary")
    if product == "claude-code" and not item["private_mirror"]:
        errors.append("Claude Code must retain its private learning-snapshot boundary")
    if f"({product}/README.md)" not in agent_products_readme:
        errors.append(f"products/agent/README.md: missing {product} reading entry")

# Current-state semantic checks.
# Validate every current module heading against the explicit learning order.
# Directory prefixes and display ranks follow the same approved reading order.
import json
learning_order = json.loads(read("guide/learning-order.json"))["modules"]
knowledge_map = read("guide/knowledge-map.md")
for rank, item in enumerate(learning_order, 1):
    directory = item["directory"]
    expected = EXPECTED_BLOCKS["curriculum/" + directory]
    pattern = (rf"^## {rank:02d}\. \[[^\]]+\]\(\.\./curriculum/"
               + re.escape(directory)
               + rf"/README\.md\) — {expected} 章$")
    if len(re.findall(pattern, knowledge_map, re.M)) != 1:
        errors.append(f"knowledge-map: heading/order/count mismatch for {directory}")
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
require("guide/audits/final-quality-audit.md", f"{total} 篇正文")
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
