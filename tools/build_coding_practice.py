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

ROOT = Path(__file__).resolve().parents[1]
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


def notebook(exercises: list[Exercise]) -> dict:
    intro = (
        "# 第 03 章基础练习\n\n"
        "[返回课程正文](../docs/03-basic-exercises.md)\n\n"
        "看得懂答案，却不知道第一行怎么写？先从小题练习决定：输入是什么，"
        "要得到什么，重复做什么，要记住什么。每题先手算，再填写编写区，最后运行测试。\n\n"
        "`pass` 是留给你完成的空语句；E22 有故意的越界错误。空白函数不能通过测试，"
        "不表示文件损坏。需要时展开参考答案，看完再关掉重写；答案不会随运行全部自动执行。\n\n"
        "Shift+Enter 运行当前单元。更换实现后重新运行函数定义与测试；"
        "遇到旧结果，重启 Python 3 内核再按顺序运行。GitHub 只提供静态预览，"
        "实际运行使用 JupyterLab 等环境，折叠效果由查看器支持情况决定。\n"
    )
    cells = [cell("markdown", "intro", "guide", intro)]
    for e in exercises:
        answer = (
            f"<details><summary>查看 {e.eid} 参考答案与解释</summary>\n"
            f"<pre><code>{html.escape(e.solution)}</code></pre>\n"
            f"<p>{html.escape(e.explanation)}</p>\n</details>\n"
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


def validate_answers(exercises: list[Exercise]) -> int:
    assertions = 0
    with tempfile.TemporaryDirectory(prefix="coding-answers-") as directory:
        for e in exercises:
            script = Path(directory) / f"{e.eid}.py"
            script.write_text(e.solution + "\n\n" + e.tests + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-I", "-S", str(script)], capture_output=True,
                text=True, timeout=10, cwd=directory,
            )
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
            raise SystemExit("Notebook differs from Coding 03; run tools/build_coding_practice.py")
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
