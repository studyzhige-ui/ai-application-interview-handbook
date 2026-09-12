#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "python",
    "fastapi",
    "backend-engineering",
    "mysql",
    "redis",
    "vector-db",
    "llm-foundation",
    "rag",
    "agent-harness",
    "system-design",
]

MODULE_NOTE = "> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。"
REVIEW_NOTE = "> **学习路线是可选入口。** 如需整体安排，可参考 [Learning Path](../../roadmap/learning-path.md)；本 Review 也可以按个人节奏独立使用。"


def write_if_changed(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8")
    if old != text:
        path.write_text(text, encoding="utf-8")


for slug in MODULES:
    # Module README: top navigation + one compact note in recommended learning section.
    path = ROOT / slug / "README.md"
    text = path.read_text(encoding="utf-8")
    if "[Learning Path](../roadmap/learning-path.md)" not in text:
        anchor = "[↑ Handbook 总目录](../README.md)"
        if anchor not in text:
            raise RuntimeError(f"module nav anchor missing: {path}")
        text = text.replace(anchor, anchor + " · [Learning Path](../roadmap/learning-path.md)", 1)
    if MODULE_NOTE not in text:
        anchor = "## 9. 推荐学习方式\n"
        if anchor not in text:
            raise RuntimeError(f"recommended-learning anchor missing: {path}")
        text = text.replace(anchor, anchor + "\n" + MODULE_NOTE + "\n", 1)
    write_if_changed(path, text)

    # Review README: top navigation + one compact optional-use note.
    path = ROOT / slug / "review" / "README.md"
    text = path.read_text(encoding="utf-8")
    if "[Learning Path](../../roadmap/learning-path.md)" not in text:
        anchor = "[↑ Handbook 总目录](../../README.md)"
        if anchor not in text:
            raise RuntimeError(f"review nav anchor missing: {path}")
        text = text.replace(anchor, anchor + " · [Learning Path](../../roadmap/learning-path.md)", 1)
    if REVIEW_NOTE not in text:
        marker = "> **用途：第二遍复习。**"
        pos = text.find(marker)
        if pos == -1:
            raise RuntimeError(f"review usage marker missing: {path}")
        line_end = text.find("\n", pos)
        if line_end == -1:
            line_end = len(text)
        text = text[:line_end] + "\n>\n" + REVIEW_NOTE + text[line_end:]
    write_if_changed(path, text)

# Learning Path: state explicitly that timing is optional, and add one compact direct Review line.
path = ROOT / "roadmap" / "learning-path.md"
text = path.read_text(encoding="utf-8")
optional_note = "> **这是一套推荐执行节奏，不是唯一课表。** 模块 README / Review 只把本页作为可选入口；不同基础、时间预算或教学场景可以自行调整速度，但第一次系统学习仍建议保持知识依赖顺序。"
if optional_note not in text:
    anchor = "> **固定原则不变：知识体系演进顺序优先。** HUMAN-A 真人面经只影响第二遍 / 第三遍的复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的课程主干。"
    if anchor not in text:
        raise RuntimeError("learning-path principle anchor missing")
    text = text.replace(anchor, anchor + "\n>\n" + optional_note, 1)
review_links = "Review 快速入口：[Python](../python/review/README.md) · [FastAPI](../fastapi/review/README.md) · [AIBE](../backend-engineering/review/README.md) · [MySQL](../mysql/review/README.md) · [Redis](../redis/review/README.md) · [Vector DB](../vector-db/review/README.md) · [LLM](../llm-foundation/review/README.md) · [RAG](../rag/review/README.md) · [Agent](../agent-harness/review/README.md) · [System Design](../system-design/review/README.md)"
if review_links not in text:
    anchor = "不要因为 Agent / RAG 高频就从中间开始，也不要因为某个基础题真人频率低就跳过必要前置。"
    if anchor not in text:
        raise RuntimeError("learning-path order anchor missing")
    text = text.replace(anchor, anchor + "\n\n" + review_links, 1)
write_if_changed(path, text)

# Long-term documentation rule.
path = ROOT / "roadmap" / "documentation-style-guide.md"
text = path.read_text(encoding="utf-8")
text = text.replace(
    "上一模块 · Handbook 总目录 · 下一模块",
    "上一模块 · Handbook 总目录 · Learning Path · 下一模块",
    1,
)
review_rule = "- 顶部必须能返回模块主页和 Handbook；"
if "Learning Path 作为可选入口" not in text:
    text = text.replace(
        review_rule,
        review_rule + "\n- 可提供 Learning Path 作为可选入口，但不在 Review 中写死 Week / Session；",
        1,
    )
module_rule = "- Learning Path 是推荐使用方式，不是模块元数据；一级模块 README / Review README 只保留简洁入口，不写死 Week / Session，避免绑定某一种学习节奏。"
if module_rule not in text:
    anchor = "## Review README 固定结构"
    text = text.replace(anchor, module_rule + "\n\n" + anchor, 1)
write_if_changed(path, text)

# Validation.
for slug in MODULES:
    module = (ROOT / slug / "README.md").read_text(encoding="utf-8")
    review = (ROOT / slug / "review" / "README.md").read_text(encoding="utf-8")
    assert "[Learning Path](../roadmap/learning-path.md)" in module
    assert MODULE_NOTE in module
    assert "[Learning Path](../../roadmap/learning-path.md)" in review
    assert REVIEW_NOTE in review

lp = (ROOT / "roadmap" / "learning-path.md").read_text(encoding="utf-8")
for slug in MODULES:
    assert f"../{slug}/review/README.md" in lp

print("learning path links synchronized across 10 module READMEs and 10 Review READMEs")
