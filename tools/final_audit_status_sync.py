#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"anchor not found in {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Root README: quick entrance + quality table.
replace(
    "README.md",
    "[十板块知识地图](roadmap/knowledge-map.md) · [课程建设进度](research/questions/progress.md) · [真人面经研究库](research/README.md) · [Canonical Questions](research/questions/README.md) · [粒度审计](roadmap/curriculum-granularity-audit.md) · [深度审计](roadmap/content-depth-audit.md)",
    "[十板块知识地图](roadmap/knowledge-map.md) · [v1.0 终局质量审计](roadmap/final-quality-audit.md) · [跨模块术语表](roadmap/terminology-glossary.md) · [课程建设进度](research/questions/progress.md) · [真人面经研究库](research/README.md) · [Canonical Questions](research/questions/README.md) · [粒度审计](roadmap/curriculum-granularity-audit.md) · [深度审计](roadmap/content-depth-audit.md)",
)
replace(
    "README.md",
    "| [Knowledge Map](roadmap/knowledge-map.md) | 十板块职责、主线与依赖关系 |",
    "| [Knowledge Map](roadmap/knowledge-map.md) | 十板块职责、主线与依赖关系 |\n| [Final Quality Audit](roadmap/final-quality-audit.md) | v1.0 前全仓库结构、边界、术语、版本与链接终审 |\n| [Terminology Glossary](roadmap/terminology-glossary.md) | 跨模块同名概念的稳定工作定义与 Primary Ownership |",
)

# Knowledge map top navigation and final note.
replace(
    "roadmap/knowledge-map.md",
    "[← Handbook 总目录](../README.md) · [课程进度](../research/questions/progress.md) · [Canonical Index](../research/questions/module-index.md)",
    "[← Handbook 总目录](../README.md) · [v1.0 终局质量审计](final-quality-audit.md) · [跨模块术语表](terminology-glossary.md) · [课程进度](../research/questions/progress.md) · [Canonical Index](../research/questions/module-index.md)",
)
replace(
    "roadmap/knowledge-map.md",
    "- 当前粒度与深度状态见 [Granularity Audit](curriculum-granularity-audit.md) 与 [Content Depth Audit](content-depth-audit.md)。",
    "- 当前粒度与深度状态见 [Granularity Audit](curriculum-granularity-audit.md) 与 [Content Depth Audit](content-depth-audit.md)。\n- v1.0 全仓库最终结论见 [Final Quality Audit](final-quality-audit.md)；跨模块同名概念统一以 [Terminology Glossary](terminology-glossary.md) 为工作定义。",
)

# Progress: explicit final gate.
replace(
    "research/questions/progress.md",
    "十个正式一级模块第一版系统教材全部完成；Foundation 也已完成。",
    "十个正式一级模块第一版系统教材全部完成；Foundation 也已完成。\n\n**v1.0 Final Quality Audit：✅ PASS。** 184/184 Curriculum Markdown、235/235 Canonical、仓库内链接、Mermaid、跨模块 Ownership、术语与版本敏感事实风险审计均已完成；详见 [`../../roadmap/final-quality-audit.md`](../../roadmap/final-quality-audit.md)。",
)

# Module index and Canonical README: connect research ownership to final curriculum acceptance.
replace(
    "research/questions/module-index.md",
    "> **Foundation 实际完成度已单独核实。** 见 `../../roadmap/foundation-status-audit.md`。",
    "> **Foundation 实际完成度已单独核实。** 见 `../../roadmap/foundation-status-audit.md`。\n> **v1.0 终局质量审计已通过。** 十板块跨模块 Ownership、术语边界与 184 个 Curriculum Markdown 的最终结论见 `../../roadmap/final-quality-audit.md`。",
)
replace(
    "research/questions/README.md",
    "当前 Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
    "当前十个一级模块均已完成正式教材建设与质量验收；正文深度见 `../../roadmap/content-depth-audit.md`，v1.0 全仓库终局结论见 `../../roadmap/final-quality-audit.md`，跨模块术语边界见 `../../roadmap/terminology-glossary.md`。",
)

# Documentation maintenance rule.
replace(
    "roadmap/documentation-style-guide.md",
    "[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Progress](../research/questions/progress.md)",
    "[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Final Quality Audit](final-quality-audit.md) · [Terminology Glossary](terminology-glossary.md) · [Progress](../research/questions/progress.md)",
)
replace(
    "roadmap/documentation-style-guide.md",
    "模块状态改变时，至少核验：根 README、模块 README、Review README、Knowledge Map、Progress、Module Index、Canonical README、自动生成 Analysis README 的生成源，以及本地 Markdown 链接。",
    "模块状态改变时，至少核验：根 README、模块 README、Review README、Knowledge Map、Progress、Module Index、Canonical README、自动生成 Analysis README 的生成源、本地 Markdown 链接，以及是否需要更新 Final Quality Audit / Terminology Glossary 中的跨模块边界。",
)

print("final audit status synchronized")
