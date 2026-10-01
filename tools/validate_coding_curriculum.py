#!/usr/bin/env python3
"""Cold-run Coding examples; verify visible exercise contracts and notebook sync.

This is a mechanical regression check, not a proof of readability or completeness.
Run only for trusted teaching content; the code fences and lab tests execute locally.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from build_coding_practice import extract, notebook, validate_answers, SOURCE, TARGET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "practice/coding/docs"
FENCE = re.compile(r"```python\n(.*?)\n```", re.S)
RUN = re.compile(r"<!-- run: (\{[^\n]*\}) -->\s*$")
LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^\s)]+)\)")


def run_examples() -> dict:
    counts: dict[str, int] = {}
    exact_outputs = 0
    expected_errors = 0
    assertions = 0
    chapters = sorted(DOCS.glob("[0-9][0-9]-*.md"))
    if [p.name[:2] for p in chapters] != [f"{i:02}" for i in range(1, 10)]:
        raise ValueError("Expected exactly nine numbered Coding chapters")
    with tempfile.TemporaryDirectory(prefix="coding-cold-run-") as directory:
        for path in chapters:
            text = path.read_text(encoding="utf-8")
            if len(re.findall(r"^# ", text, re.M)) != 1:
                raise ValueError(f"{path.name}: expected one document title")
            if text.count("<details>") != text.count("</details>"):
                raise ValueError(f"{path.name}: unbalanced details")
            if text.count("```") % 2:
                raise ValueError(f"{path.name}: unbalanced fences")
            if path.name.startswith("03-"):
                continue  # Its starter/tests/solution roles are validated separately.
            count = 0
            for index, match in enumerate(FENCE.finditer(text), 1):
                code = match[1]
                ast_tree = ast.parse(code, filename=f"{path.name}/{index}")
                assertions += sum(isinstance(node, ast.Assert) for node in ast.walk(ast_tree))
                directive = RUN.search(text[:match.start()])
                options = json.loads(directive[1]) if directive else {}
                if "input(" in code and "stdin" not in options:
                    raise ValueError(f"{path.name}/{index}: input example lacks stdin")
                script = Path(directory) / "example.py"
                script.write_text(code, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-I", "-S", "-X", "utf8", str(script)], input=options.get("stdin", ""),
                    capture_output=True, text=True, encoding="utf-8", timeout=10, cwd=directory,
                )
                expected_error = options.get("error")
                if expected_error:
                    if result.returncode == 0 or not re.search(
                        rf"^{re.escape(expected_error)}:", result.stderr, re.M
                    ):
                        raise AssertionError(f"{path.name}/{index}: expected {expected_error}\n{result.stderr}")
                    expected_errors += 1
                elif result.returncode:
                    raise AssertionError(f"{path.name}/{index}:\n{result.stderr}")
                if "stdout" in options:
                    if result.stdout != options["stdout"]:
                        raise AssertionError(f"{path.name}/{index}: unexpected stdout {result.stdout!r}")
                    exact_outputs += 1
                count += 1
            counts[path.name] = count
    return {"cold_run_blocks": counts, "exact_stdout_checks": exact_outputs,
            "expected_error_checks": expected_errors, "example_assertions": assertions}


def validate_lab() -> dict:
    lab = ROOT / "practice/coding/exercises/09-ai-coding-lab"
    readme = (lab / "README.md").read_text(encoding="utf-8")
    match = re.search(r"<!-- solution:pagination -->\s*```python\n(.*?)\n```", readme, re.S)
    if match is None:
        raise ValueError("Missing lab reference solution")
    tests = (lab / "test_pagination.py").read_text(encoding="utf-8")
    count = len(re.findall(r"^    def test_", tests, re.M))
    results = {}
    for label, code in [("starter", (lab / "pagination.py").read_text(encoding="utf-8")),
                        ("reference", match[1])]:
        with tempfile.TemporaryDirectory(prefix="coding-lab-") as directory:
            Path(directory, "pagination.py").write_text(code, encoding="utf-8")
            Path(directory, "test_pagination.py").write_text(tests, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-v"],
                cwd=directory, capture_output=True, text=True, encoding="utf-8", timeout=10,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            results[label] = result.returncode
            if label == "starter" and result.returncode == 0:
                raise AssertionError("Lab starter unexpectedly passes; exercise lost its failure")
            if label == "reference" and result.returncode != 0:
                raise AssertionError(result.stderr)
    return {"tests": count, "starter_expected_to_fail": results["starter"] != 0,
            "reference_passed": results["reference"] == 0}


def check_ownership() -> dict:
    """Lexical guardrails only; a human must review sequence and explanations."""
    content = (DOCS / "02-python-coding-basics.md").read_text(encoding="utf-8")
    # A small floor of core concepts, not an API inventory. Task-local tools are
    # allowed to appear later with an explanation; lexical matches do not prove it.
    owners = {
        "list": ("tuple", ["append", "pop", "copy", "sort", "reverse", "切片", "enumerate", "解包"]),
        "tuple": ("str", ["解包", "不可变", "return"]),
        "str": ("dict", ["split", "join", "sorted", "不可变"]),
        "dict": ("set", ["get", "keys", "values", "items", "del", "次数"]),
        "set": (None, ["set()", "add", "remove", "discard", "成员"]),
    }
    for owner, (following, words) in owners.items():
        start = content.index(f'<a id="{owner}"></a>')
        stop = content.index(f'<a id="{following}"></a>') if following else content.index("## 7. 跨容器")
        section = content[start:stop]
        missing = [word for word in words if word not in section]
        if missing:
            raise ValueError(f"{owner}: missing owned operations {missing}")
    mapping = (ROOT / "practice/coding/hot100-map.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\| (\d+) \|", mapping, re.M)
    if len(ids) != 100 or len(set(ids)) != 100:
        raise ValueError("Hot100 frozen snapshot must contain 100 unique rows")
    return {"container_sections": list(owners), "hot100_unique_rows": len(ids)}


def check_learning_sections() -> dict:
    """Check only missing learning sections; no prose-length/readability score."""
    checked = []
    for path in sorted(DOCS.glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        for marker in ("本章小结", "面试怎么答", "⚠️", "自测", "知识课程回看"):
            if marker not in text:
                raise ValueError(f"{path.name}: missing learning section {marker}")
        if "算法应用在第 07 章" in text:
            raise ValueError(f"{path.name}: restored an empty forward-reference heading")
        checked.append(path.name)
    return {"checked_chapters": len(checked), "scope": "section-presence-only"}


def check_local_links() -> list[str]:
    missing: list[str] = []
    paths = list((ROOT / "practice/coding").rglob("*.md"))
    for path in paths:
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK.findall(text):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            bare = target.split("#", 1)[0]
            if bare and not (path.parent / bare).resolve().exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-external-navigation", action="store_true",
                        help="For a scoped export only: report links outside exported files rather than fail")
    args = parser.parse_args()
    exercises = extract(SOURCE.read_text(encoding="utf-8"))
    expected = json.dumps(notebook(exercises), ensure_ascii=False, indent=1) + "\n"
    if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != expected:
        raise SystemExit("Notebook out of sync; run tools/build_coding_practice.py")
    result = run_examples()
    result["exercises"] = len(exercises)
    result["reference_assertions"] = validate_answers(exercises)
    result["lab"] = validate_lab()
    result["ownership_guardrails"] = check_ownership()
    result["learning_sections"] = check_learning_sections()
    result["missing_local_links"] = check_local_links()
    internal_missing = [link for link in result["missing_local_links"]
                        if (ROOT / link.split(" -> ")[0]).parent.joinpath(link.split(" -> ")[1]).resolve().is_relative_to(ROOT / "practice/coding")]
    if internal_missing or (result["missing_local_links"] and not args.allow_external_navigation):
        raise ValueError("Broken local links:\n" + "\n".join(result["missing_local_links"]))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
