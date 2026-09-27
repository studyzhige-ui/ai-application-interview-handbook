#!/usr/bin/env python3
"""Run the exact marked source examples from the DeerFlow teaching chapters.

No model, database, network or remote sandbox is used. Optional --upstream-root
compares the displayed functions with a clean checkout of the pinned upstream.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

MODULE = Path(__file__).resolve().parents[1]
UPSTREAM_SHA = "e2feca1e567d9bafce657de8ad8bc668bd7ad513"
EXAMPLES = {
    "fact_scope_gate": (
        "02-memory-lifecycle.md",
        "backend/packages/harness/deerflow/agents/memory/backends/deermem/deermem/core/updater.py",
        ("_normalize_gate_label", "_fact_scope_gate_reason"),
    ),
    "promoted_tools": (
        "03-tool-lifecycle.md",
        "backend/packages/harness/deerflow/agents/thread_state.py",
        ("merge_promoted",),
    ),
}


def extract_example(example_id: str) -> str:
    chapter = MODULE / EXAMPLES[example_id][0]
    text = chapter.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"<!-- source-example: {re.escape(example_id)} -->\s*\n```python\n(.*?)\n```",
        re.S,
    )
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"{chapter.name}: expected one marked example {example_id}, got {len(matches)}")
    return matches[0] + "\n"


def load_example(example_id: str) -> dict:
    code = extract_example(example_id)
    namespace: dict = {"__name__": f"deerflow_teaching_{example_id}"}
    exec(compile(code, EXAMPLES[example_id][0], "exec"), namespace)
    return namespace


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def function_ast(text: str, name: str) -> str:
    nodes = [node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise ValueError(f"Expected one top-level function {name}, found {len(nodes)}")
    return ast.dump(nodes[0], include_attributes=False)


def compare_upstream(root: Path) -> list[str]:
    # Comparing the complete upstream source requires its declared Python floor.
    if sys.version_info < (3, 12):
        raise RuntimeError("Upstream source comparison requires Python >=3.12; local excerpt tests have a lower floor.")
    actual = git(root, "rev-parse", "HEAD").decode().strip()
    if actual != UPSTREAM_SHA:
        raise ValueError(f"Wrong upstream checkout: {actual}; expected {UPSTREAM_SHA}")
    compared = []
    for key, (_, path, names) in EXAMPLES.items():
        committed = git(root, "show", f"HEAD:{path}")
        if (root / path).read_bytes() != committed:
            raise ValueError(f"Locally modified upstream source: {path}")
        displayed = extract_example(key)
        for name in names:
            if function_ast(displayed, name) != function_ast(committed.decode("utf-8"), name):
                raise ValueError(f"Source AST mismatch: {path}::{name}")
            compared.append(f"{path}::{name}")
    return compared


GATE = load_example("fact_scope_gate")["_fact_scope_gate_reason"]
MERGE = load_example("promoted_tools")["merge_promoted"]


class FactGateTests(unittest.TestCase):
    def fact(self, **changes):
        return {"scope": "user", "durability": "durable", "authority": "descriptive", **changes}

    def test_accepts_declared_durable_user_data(self):
        self.assertIsNone(GATE(self.fact()))

    def test_missing_label(self):
        self.assertEqual(GATE({"scope": "user"}), "missing")

    def test_non_string_label(self):
        self.assertEqual(GATE(self.fact(scope=True)), "missing")

    def test_task_scope_is_rejected(self):
        self.assertEqual(GATE(self.fact(scope="thread")), "scope")

    def test_temporary_is_rejected(self):
        self.assertEqual(GATE(self.fact(durability="temporary")), "durability")

    def test_instruction_authority_is_rejected(self):
        self.assertEqual(GATE(self.fact(authority="instruction")), "authority")

    def test_case_and_whitespace_normalize(self):
        self.assertIsNone(GATE(self.fact(scope=" USER ", durability="DURABLE")))

    def test_gate_does_not_mutate_input(self):
        fact = self.fact(scope=" USER ")
        before = copy.deepcopy(fact)
        GATE(fact)
        self.assertEqual(fact, before)


class PromotionTests(unittest.TestCase):
    def test_none_preserves_object(self):
        old = {"catalog_hash": "A", "names": ["read"]}
        self.assertIs(MERGE(old, None), old)

    def test_both_none(self):
        self.assertIsNone(MERGE(None, None))

    def test_initial_deduplicates(self):
        self.assertEqual(MERGE(None, {"catalog_hash": "A", "names": ["read", "read"]}),
                         {"catalog_hash": "A", "names": ["read"]})

    def test_same_catalog_union_preserves_order(self):
        self.assertEqual(MERGE({"catalog_hash": "A", "names": ["read"]},
                               {"catalog_hash": "A", "names": ["read", "search"]}),
                         {"catalog_hash": "A", "names": ["read", "search"]})

    def test_new_catalog_drops_old_names(self):
        self.assertEqual(MERGE({"catalog_hash": "A", "names": ["read"]},
                               {"catalog_hash": "B", "names": ["export"]}),
                         {"catalog_hash": "B", "names": ["export"]})

    def test_empty_names_same_catalog_does_not_clear(self):
        self.assertEqual(MERGE({"catalog_hash": "A", "names": ["read"]},
                               {"catalog_hash": "A", "names": []}),
                         {"catalog_hash": "A", "names": ["read"]})

    def test_empty_names_changed_catalog_clears(self):
        self.assertEqual(MERGE({"catalog_hash": "A", "names": ["read"]},
                               {"catalog_hash": "B", "names": []}),
                         {"catalog_hash": "B", "names": []})

    def test_merge_does_not_mutate_inputs(self):
        old, new = {"catalog_hash": "A", "names": ["read"]}, {"catalog_hash": "A", "names": ["search"]}
        before = copy.deepcopy((old, new))
        result = MERGE(old, new)
        self.assertEqual((old, new), before)
        self.assertIsNot(result, old)
        self.assertIsNot(result["names"], old["names"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Write machine-readable local test results.")
    parser.add_argument("--upstream-root", type=Path, help="Optionally compare actual upstream function ASTs.")
    args = parser.parse_args()
    comparisons = []
    if args.upstream_root:
        try:
            comparisons = compare_upstream(args.upstream_root)
        except (OSError, ValueError, RuntimeError, SyntaxError) as exc:
            parser.exit(2, f"Upstream comparison failed: {exc}\n")
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {
        "scope": "Marked upstream-derived pure-function excerpts from teaching chapters only",
        "python": sys.version,
        "upstream_sha": UPSTREAM_SHA,
        "upstream_ast_comparison": "performed" if args.upstream_root else "not_run",
        "compared_functions": comparisons,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "excerpt_sha256": {key: hashlib.sha256(extract_example(key).encode()).hexdigest() for key in EXAMPLES},
        "not_tested": ["full DeerFlow runtime", "LLM extraction", "MCP", "database", "remote sandbox", "production"],
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
