#!/usr/bin/env python3
"""Apply the reviewed Phase 2B canonical/evidence audit idempotently.

The JSON audit file is human-reviewed. This script only materializes those decisions:
- add approved HUMAN-A Evidence Sources to existing Canonical Questions;
- insert approved new Canonical Questions;
- recompute Source Count and module ACTIVE counts;
- write a source coverage audit record.

It does NOT discover evidence and does NOT infer new mappings on its own.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_DIR = ROOT / "research" / "questions"
AUDIT_PATH = ROOT / "tools" / "phase2b_canonical_audit.json"

MODULE_FILES = [
    "python.md",
    "fastapi.md",
    "ai-backend-engineering.md",
    "mysql.md",
    "redis.md",
    "vector-db.md",
    "llm-foundation.md",
    "rag.md",
    "agent-harness.md",
    "system-design.md",
]
QID_RE = re.compile(r"^###\s+((?:PY|FASTAPI|AIBE|MYSQL|REDIS|VDB|LLM|RAG|AGENT|SD)-\d{3})\s+·\s+", re.M)


def source_sort_key(sid: str) -> int:
    return int(sid[1:])


def heat(count: int) -> str:
    if count >= 10:
        return "🔥🔥🔥"
    if count >= 4:
        return "🔥🔥"
    if count >= 2:
        return "🔥"
    return "单点真实信号"


def block_bounds(text: str, qid: str) -> tuple[int, int]:
    matches = list(QID_RE.finditer(text))
    for i, m in enumerate(matches):
        if m.group(1) == qid:
            return m.start(), matches[i + 1].start() if i + 1 < len(matches) else len(text)
    raise KeyError(qid)


def merge_evidence(text: str, qid: str, additions: set[str]) -> str:
    start, end = block_bounds(text, qid)
    block = text[start:end]
    m = re.search(r"^- \*\*Evidence Sources\*\*：(.+?)\s*$", block, re.M)
    if not m:
        raise ValueError(f"missing Evidence Sources for {qid}")
    current = set(re.findall(r"S\d{3}", m.group(1)))
    merged = sorted(current | additions, key=source_sort_key)
    evidence_line = "- **Evidence Sources**：" + ", ".join(f"`{sid}`" for sid in merged)
    block = block[:m.start()] + evidence_line + block[m.end():]

    cm = re.search(r"^- \*\*Source Count\*\*：.*$", block, re.M)
    if not cm:
        raise ValueError(f"missing Source Count for {qid}")
    count_line = f"- **Source Count**：**{len(merged)}**"
    block = block[:cm.start()] + count_line + block[cm.end():]

    hm = re.search(r"^- \*\*Interview Heat\*\*：.*$", block, re.M)
    if hm:
        heat_line = f"- **Interview Heat**：{heat(len(merged))}"
        block = block[:hm.start()] + heat_line + block[hm.end():]
    return text[:start] + block + text[end:]


def make_question_block(item: dict) -> str:
    evidence = sorted(set(item["evidence"]), key=source_sort_key)
    lines = [
        f"### {item['qid']} · {item['question']}",
        f"- **Primary Module**：{item['primary_module']}",
    ]
    if item.get("related_modules"):
        lines.append(f"- **Related Modules**：{item['related_modules']}")
    lines += [
        f"- **Topic**：{item['topic']}",
        f"- **Question Type**：{item['question_type']}",
        f"- **Depth**：{item['depth']}",
        f"- **Interview Heat**：{heat(len(evidence))}",
        f"- **Source Count**：**{len(evidence)}**",
        "- **Evidence Sources**：" + ", ".join(f"`{sid}`" for sid in evidence),
        "",
    ]
    return "\n".join(lines)


def refresh_active_count(text: str) -> str:
    count = len(QID_RE.findall(text))
    patterns = [
        r"(- ACTIVE Canonical Questions：)\*\*\d+\*\*",
        r"(- Canonical Questions：)\*\*\d+\*\*",
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            return re.sub(pattern, rf"\g<1>**{count}**", text, count=1)
    return text


def main() -> None:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    file_text = {name: (QUESTIONS_DIR / name).read_text(encoding="utf-8") for name in MODULE_FILES}

    qid_to_file: dict[str, str] = {}
    for filename, text in file_text.items():
        for qid in QID_RE.findall(text):
            if qid in qid_to_file:
                raise ValueError(f"duplicate QID before audit: {qid}")
            qid_to_file[qid] = filename

    additions_by_qid: dict[str, set[str]] = defaultdict(set)
    for sid, qids in audit.get("evidence_additions", {}).items():
        for qid in qids:
            additions_by_qid[qid].add(sid)

    # New questions also count as evidence mappings; if an evidence addition references a new
    # QID, the source is already present in the reviewed new-question evidence set.
    new_by_qid = {item["qid"]: item for item in audit.get("new_questions", [])}

    # Apply additions to existing questions first.
    for qid, sources in additions_by_qid.items():
        if qid in new_by_qid and qid not in qid_to_file:
            missing = sources - set(new_by_qid[qid]["evidence"])
            if missing:
                new_by_qid[qid]["evidence"].extend(sorted(missing, key=source_sort_key))
            continue
        filename = qid_to_file.get(qid)
        if not filename:
            raise KeyError(f"audit references unknown QID: {qid}")
        file_text[filename] = merge_evidence(file_text[filename], qid, sources)

    # Insert approved new questions, grouped per file/anchor so insertion order is stable.
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in audit.get("new_questions", []):
        grouped[(item["file"], item["insert_before"])].append(item)

    for (filename, anchor), items in grouped.items():
        text = file_text[filename]
        existing = set(QID_RE.findall(text))
        pending = [item for item in items if item["qid"] not in existing]
        if not pending:
            continue
        if anchor not in text:
            raise ValueError(f"anchor not found in {filename}: {anchor}")
        chunks: list[str] = []
        section_headings_seen: set[str] = set()
        for item in pending:
            heading = item.get("section_heading", "").strip()
            if heading and heading not in section_headings_seen and heading not in text:
                chunks.append(heading + "\n")
                section_headings_seen.add(heading)
            chunks.append(make_question_block(item))
        insertion = "\n".join(chunks).rstrip() + "\n\n---\n\n"
        text = text.replace(anchor, insertion + anchor, 1)
        file_text[filename] = text

    # Refresh module counts and write only changed files.
    final_qids: list[str] = []
    for filename in MODULE_FILES:
        text = refresh_active_count(file_text[filename])
        final_qids.extend(QID_RE.findall(text))
        path = QUESTIONS_DIR / filename
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")

    expected = int(audit["expected_active_after"])
    if len(final_qids) != expected:
        raise ValueError(f"expected {expected} active QIDs after audit, got {len(final_qids)}")
    if len(final_qids) != len(set(final_qids)):
        raise ValueError("duplicate QID after audit")

    # Human-readable record for the formerly uncovered-source audit.
    mapped_sources = sorted(audit.get("evidence_additions", {}).keys(), key=source_sort_key)
    valid_unmapped = audit.get("valid_unmapped", {})
    lines = [
        "# Phase 2B Source Coverage Audit",
        "",
        "更新日期：2026-09-11",
        "",
        "> 本文件记录首次自动校验发现的 28 个零映射 HUMAN-A 来源如何处理。原则：优先补已有 Canonical 的 Evidence；只有出现独立知识模型才新增 Canonical；确无十板块可归一化技术题的来源允许显式 `VALID-UNMAPPED`，绝不为追求 279/279 强行造题。",
        "",
        "## 补漏结果",
        "",
        f"- 重新映射来源：**{len(mapped_sources)}**",
        f"- VALID-UNMAPPED：**{len(valid_unmapped)}**",
        f"- 本轮新增 Canonical：**{len(audit.get('new_questions', []))}**",
        f"- 审计后预期 ACTIVE：**{expected}**",
        "",
        "## 新增 Canonical",
        "",
        "| QID | Module | Topic | HUMAN-A Sources |",
        "|---|---|---|---:|",
    ]
    for item in audit.get("new_questions", []):
        lines.append(f"| `{item['qid']}` | {item['primary_module']} | {item['topic']} | {len(set(item['evidence']))} |")
    lines += ["", "## 原零映射来源处理", "", "| Source | Decision | QIDs |", "|---|---|---|"]
    for sid in mapped_sources:
        qids = audit["evidence_additions"][sid]
        lines.append(f"| `{sid}` | MAPPED | {', '.join(f'`{q}`' for q in qids)} |")
    for sid, reason in sorted(valid_unmapped.items(), key=lambda kv: source_sort_key(kv[0])):
        lines.append(f"| `{sid}` | VALID-UNMAPPED | {reason} |")
    lines += [
        "",
        "## 关键补漏解释",
        "",
        "这轮不是为了把覆盖率做成 100% 而机械挂 Evidence。全语料候选扫描暴露出 Phase 1 真正遗漏的独立能力：Prompt Engineering、Prompt Injection / Untrusted Context Security、Intent Recognition / Routing、A2A、Agent Framework Selection、AI-assisted Development Workflow。它们均由 HUMAN-A 原始技术问题支持，因此正式新增 Canonical。",
        "",
        "`S271` 保留为 VALID-UNMAPPED：招聘流程明确属于 Agent 工程师大池，但当前可核验技术题是 React Hook / JavaScript / 版本号 Coding，不能安全归入现有十板块的 AI / Backend Canonical。",
    ]
    (QUESTIONS_DIR / "source-coverage-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
