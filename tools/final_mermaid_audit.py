#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
warnings = []
blocks = 0

for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for i, m in enumerate(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.S), 1):
        blocks += 1
        block = m.group(1)
        rel = path.relative_to(ROOT)
        if re.search(r"<br\s*/?>", block, re.I):
            warnings.append(f"{rel} block#{i}: HTML <br> inside Mermaid")
        for lineno, raw in enumerate(block.splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("%%"):
                continue
            if line.startswith("subgraph "):
                rest = line[len("subgraph "):].strip()
                # Conservative GitHub style: complex display titles should be quoted in ["..."] form.
                if re.search(r"[\s:/()（）｜，。？]", rest) and '["' not in rest:
                    warnings.append(f"{rel} block#{i}:{lineno}: complex unquoted subgraph title: {line}")
            # Node labels such as A[complex label] / D{complex label}; simple identifiers are fine.
            for nm in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\s*([\[\{])([^\]\}]+)[\]\}]", line):
                label = nm.group(2).strip()
                if not label:
                    continue
                if label.startswith('"') and label.endswith('"'):
                    continue
                if re.fullmatch(r"[A-Za-z0-9_.+-]+", label):
                    continue
                warnings.append(f"{rel} block#{i}:{lineno}: complex unquoted node label: {line}")

print(f"Mermaid blocks scanned: {blocks}")
print(f"Warnings: {len(warnings)}")
for w in warnings:
    print("WARN", w)
