#!/usr/bin/env python3
"""Generate a conservative raw-corpus keyword candidate list for manual gap review.

This is a recall aid only. A keyword hit is NOT Canonical evidence until the source section
is manually reviewed under research/questions/schema.md.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVIEWS = ROOT / "research" / "interviews"
OUT = ROOT / "research" / "analysis" / "raw-term-candidates.md"

TERMS = {
    "Prompt / Prompt Engineering": [r"\bPrompt\b", r"Prompt Engineering", r"Prompt Optimization", r"Prompt 调"],
    "Prompt Injection / Prompt Attack": [r"Prompt Injection", r"Prompt Attack", r"指令注入"],
    "Intent Recognition": [r"Intent Recognition", r"意图识别", r"Intent Classification"],
    "LangGraph / LangChain": [r"LangGraph", r"LangChain"],
    "A2A": [r"\bA2A\b", r"Agent-to-Agent"],
    "AI Coding / Vibe Coding": [r"AI Coding", r"Vibe Coding", r"AI-assisted", r"Cursor"],
    "Spec-driven Development": [r"\bSDD\b", r"Spec-driven", r"OpenSpec", r"Structured-document-driven", r"Spec Coding"],
}

SOURCE_RE = re.compile(r"^##\s+(S\d{3})\s+(.+?)\s*$", re.M)


def main() -> None:
    sections: dict[str, tuple[str, str]] = {}
    for path in sorted(INTERVIEWS.glob("batch-*.md")):
        text = path.read_text(encoding="utf-8")
        matches = list(SOURCE_RE.finditer(text))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections[m.group(1)] = (m.group(2).strip(), text[m.start():end])

    lines = [
        "# Raw Term Candidates for Knowledge-gap Audit",
        "",
        "更新日期：2026-09-11",
        "",
        "> 这是**召回辅助表**，不是正式 Evidence。命中关键词只表示该 HUMAN-A 来源值得人工回读；不得直接据此增加 Source Count。",
        "",
    ]
    for label, patterns in TERMS.items():
        hits = []
        regexes = [re.compile(p, re.I) for p in patterns]
        for sid in sorted(sections):
            heading, body = sections[sid]
            if any(r.search(body) for r in regexes):
                snippets = []
                for line in body.splitlines():
                    if any(r.search(line) for r in regexes):
                        cleaned = line.strip()
                        if cleaned and cleaned not in snippets:
                            snippets.append(cleaned)
                    if len(snippets) >= 3:
                        break
                hits.append((sid, heading, " / ".join(snippets)))
        lines += [f"## {label}", "", f"候选来源：**{len(hits)}**", "", "| Source | Flow | Match snippets |", "|---|---|---|"]
        for sid, heading, snippet in hits:
            esc = lambda s: s.replace("|", "\\|")
            lines.append(f"| `{sid}` | {esc(heading)} | {esc(snippet)} |")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
