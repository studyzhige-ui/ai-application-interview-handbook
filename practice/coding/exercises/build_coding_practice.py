#!/usr/bin/env python3
"""Generate the learner notebook from Coding 03 and test its reference answers.

Only run this on trusted course sources: reference implementations are executed.
The distributed notebook deliberately contains unfinished learner cells.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "practice/coding/docs/03-basic-exercises.md"
TARGET = ROOT / "practice/coding/exercises/03-basic-exercises.ipynb"
EXERCISE = re.compile(r"<!-- exercise:(E\d+) -->\s*(.*?)<!-- /exercise -->", re.S)


@dataclass(frozen=True)
class Exercise:
    eid: str
    question: str
    starter: str
    tests: str
    solution: str
    explanation: str


def extract(text: str) -> list[Exercise]:
    exercises: list[Exercise] = []
    for eid, body in EXERCISE.findall(text):
        chunks: dict[str, str] = {}
        for role in ("starter", "tests", "solution"):
            matches = re.findall(
                rf"<!-- {role} -->\s*```python\n(.*?)\n```", body, re.S
            )
            if len(matches) != 1:
                raise ValueError(f"{eid}: expected one {role} block")
            chunks[role] = matches[0]
            ast.parse(matches[0], filename=f"{eid}/{role}")
        question = body.split("**编写区", 1)[0].strip()
        if "任务与边界" not in question or "给定样例与预期" not in question:
            raise ValueError(f"{eid}: missing visible contract or sample")
        solution_end = re.search(r"<!-- solution -->\s*```python\n.*?\n```", body, re.S)
        assert solution_end is not None
        explanation = body[solution_end.end():].split("</details>", 1)[0].strip()
        exercises.append(Exercise(eid, question, **chunks, explanation=explanation))
    expected = [f"E{i:02}" for i in range(1, len(exercises) + 1)]
    if not exercises or [e.eid for e in exercises] != expected:
        raise ValueError("Exercise IDs must be unique and contiguous from E01")
    return exercises


def cell(kind: str, eid: str, role: str, source: str) -> dict:
    value = {
        "cell_type": kind,
        "id": f"{eid.lower()}-{role}",
        "metadata": {"exercise_id": eid, "role": role},
        "source": source.splitlines(keepends=True),
    }
    if kind == "code":
        value.update(execution_count=None, outputs=[])
    return value


def inline_html(text: str) -> str:
    """Render the course's inline code and bold subset, escaping all source HTML."""
    tokens = re.compile(r"(`[^`\n]+`|\*\*[^*\n]+\*\*)")
    parts: list[str] = []
    position = 0
    for match in tokens.finditer(text):
        parts.append(html.escape(text[position:match.start()]))
        token = match.group()
        if token.startswith("`"):
            parts.append("<code>" + html.escape(token[1:-1]) + "</code>")
        else:
            parts.append("<strong>" + html.escape(token[2:-2]) + "</strong>")
        position = match.end()
    parts.append(html.escape(text[position:]))
    return "".join(parts)


def explanation_html(text: str) -> str:
    """Preserve the explanation structures used in Coding 03.

    Supported blocks: paragraphs, flat ordered/unordered lists and blockquotes.
    This is deliberately not a general Markdown implementation. Keep generated
    answers extension-free and escape source HTML. Add explicit support/tests
    before introducing nested lists, tables or other syntax in explanations.
    """
    output: list[str] = []
    lines = text.splitlines()
    i = 0

    def kind(line: str) -> str:
        if re.match(r"^\d+\.\s+", line):
            return "ol"
        if line.startswith("- "):
            return "ul"
        if line.startswith(">"):
            return "blockquote"
        return "p"

    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        block_kind = kind(lines[i])
        group: list[str] = []
        while i < len(lines) and lines[i].strip() and kind(lines[i]) == block_kind:
            group.append(lines[i])
            i += 1
        if block_kind in ("ol", "ul"):
            start = ""
            if block_kind == "ol":
                first = int(group[0].split(".", 1)[0])
                start = f' start="{first}"' if first != 1 else ""
            items = []
            for line in group:
                content = re.sub(r"^(?:\d+\.|-)\s+", "", line)
                items.append("<li>" + inline_html(content) + "</li>")
            output.append(f"<{block_kind}{start}>\n" + "\n".join(items) + f"\n</{block_kind}>")
        elif block_kind == "blockquote":
            content = "\n".join(re.sub(r"^> ?", "", line) for line in group)
            output.append("<blockquote>\n" + explanation_html(content) + "\n</blockquote>")
        else:
            content = "\n".join(group)
            # Fail rather than silently flatten an unsupported block construct.
            if any(re.match(r"^(?:\s{2,}(?:-|\d+\.)\s|#{1,6}\s|```|\|)", line) for line in group):
                raise ValueError("Unsupported explanation block; extend the renderer and tests first")
            output.append("<p>" + inline_html(content) + "</p>")
    return "\n".join(output)


def notebook(exercises: list[Exercise]) -> dict:
    intro = (
        "# 第 03 章基础练习\n\n"
        "[返回课程正文](../docs/03-basic-exercises.md)\n\n"
        "看得懂答案，却不知道第一行怎么写？先从小题练习决定：输入是什么，"
        "结果是什么，重复做什么，需要记住什么。\n\n"
        "每题按下面的顺序完成：\n\n"
        "1. 读任务、输入和预期结果，先手算样例。\n"
        "2. 填写编写区，按 Shift+Enter 运行该单元。\n"
        "3. 运行下方测试，对照实际结果修改实现。\n"
        "4. 需要时展开参考答案，看懂后再关掉重写。\n\n"
        "> ⚠️ `pass` 是待完成区域。E22 则含有故意的越界错误。"
        "空白或缺陷实现不能通过测试是预期情况，不表示文件损坏。\n\n"
        "更换实现后，要重新运行函数定义和测试。结果像在使用旧代码时，"
        "重启 Python 3 内核，再从上到下运行。参考答案在 Markdown 折叠中，"
        "不会随“运行全部”自动执行。\n\n"
        "GitHub 提供静态预览。运行练习请使用带 Python 3 内核的 JupyterLab 等环境；"
        "折叠显示效果取决于查看器的支持。\n"
    )
    cells = [cell("markdown", "intro", "guide", intro)]
    for e in exercises:
        answer = (
            f"<details><summary>查看 {e.eid} 参考答案与解释</summary>\n"
            f"<pre><code>{html.escape(e.solution)}</code></pre>\n"
            f"{explanation_html(e.explanation)}\n</details>\n"
        )
        cells.extend([
            cell("markdown", e.eid, "question", e.question + "\n"),
            cell("code", e.eid, "starter", e.starter + "\n"),
            cell("code", e.eid, "tests", e.tests + "\n"),
            cell("markdown", e.eid, "answer", answer),
        ])
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "source_of_truth": "practice/coding/docs/03-basic-exercises.md",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def run_isolated(script: Path, *, input_text: str = "", cwd=None):
    """Keep cold execution isolated while making both pipes explicitly UTF-8."""
    return subprocess.run(
        [sys.executable, "-I", "-S", "-X", "utf8", str(script)],
        input=input_text, capture_output=True, text=True, encoding="utf-8",
        timeout=10, cwd=cwd,
    )


def validate_answers(exercises: list[Exercise]) -> int:
    assertions = 0
    with tempfile.TemporaryDirectory(prefix="coding-answers-") as directory:
        for e in exercises:
            script = Path(directory) / f"{e.eid}.py"
            script.write_text(e.solution + "\n\n" + e.tests + "\n", encoding="utf-8")
            result = run_isolated(script, cwd=directory)
            if result.returncode:
                raise AssertionError(f"{e.eid}:\n{result.stdout}\n{result.stderr}")
            assertions += sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(e.tests)))
    return assertions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on generated notebook drift; do not write")
    args = parser.parse_args()
    exercises = extract(SOURCE.read_text(encoding="utf-8"))
    generated = json.dumps(notebook(exercises), ensure_ascii=False, indent=1) + "\n"
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != generated:
            raise SystemExit("Notebook differs from Coding 03; run practice/coding/exercises/build_coding_practice.py")
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(generated, encoding="utf-8")
    assertions = validate_answers(exercises)
    print(json.dumps({
        "exercises": len(exercises), "reference_assertions": assertions,
        "notebook_in_sync": True, "learner_cells_solved": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
