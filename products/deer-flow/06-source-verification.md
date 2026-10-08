# DeerFlow 源码小实验｜先预测，再检查真实函数的结果

## 使用本页代码

本页保留源码实验说明与完整验证程序。将下方对应 Python 代码块保存到自己的临时工作目录，文件名与小节标题一致；命令中的脚本名可替换为该文件的绝对路径。DeerFlow 的片段检查从 Handbook 仓库根目录运行，以便读取同目录的学习正文。不要把源码片段检查结果当成完整产品实测。


[← 产品总览](README.md) · [上下文篇](01-context-lifecycle.md) · [记忆篇](02-memory-lifecycle.md) · [工具篇](03-tool-lifecycle.md)

本页复用正文标记的源码片段，以及字节固定的上游摘要配置文件。不维护第二份业务门控实现，不启动完整 DeerFlow，也不连接模型、数据库或沙箱。

## 1. 环境与运行

局部片段只用 Python 标准库，要求 Python `>=3.10`；完整上游应用要求 `>=3.12`。低版本通过片段实验，不代表能运行上游应用。

在学习仓库根目录执行：

```bash
python check_examples.py
```

脚本从记忆篇和工具篇提取唯一标记的代码块，编译后测试。它不会修改正文、创建长期记忆文件或调用真实工具。每次使用新输入，不依赖上次状态，无需重置。

## 2. 先预测，再核对片段结果

| 输入条件 | 要回答的问题 |
|---|---|
| 用户事实，临时寿命，描述性信息 | 门控返回什么，是否写盘？ |
| 三项标签满足长期用户数据条件 | `None` 能否证明语义正确？ |
| 标签含两端空格和大小写差异 | 是否先规范化？ |
| 同目录重复展开工具 | 名字如何去重、顺序如何保留？ |
| 目录哈希改变 | 是否继承旧名字？ |
| 新更新为 `None` | 是否清空，是否新建对象？ |

<details>
<summary>预测答案与解释</summary>

依次是：返回 `durability` 且不写盘；`None` 只代表标签检查未拒绝；先去空格并转小写；同目录按首次出现顺序去重；换目录不继承旧名字；`None` 不更新并返回原对象。

脚本还检查输入未被原地修改，以及同目录空名字更新与换目录空名字更新的区别。候选门控不判断真实自然语言意图，状态合并也不提供业务授权。

</details>

## 3. 与本机固定上游源码比较

已有干净的上游 checkout 时，在 Python `>=3.12` 下执行：

```bash
python check_examples.py --upstream-root /path/to/deer-flow
```

`/path/to/deer-flow` 要换成实际本机目录。脚本要求 HEAD 为 `e2feca1e567d9bafce657de8ad8bc668bd7ad513`，被比较文件未修改，并比较三个函数的抽象语法树；它不导入完整应用，不调用模型。

没提供目录时，这项比较记为 `not_run`，不计为通过。片段结果正确、与上游函数一致、完整系统可以运行，是三个不同结论。

<a id="summary-config-lab"></a>
<a id="4-继续使用字节固定的真实配置实验"></a>

## 4. 运行字节固定的摘要配置实验

`verify_source_config.py` 先核对上游配置文件的 Git blob，再执行同一份已校验字节。需要 Python `>=3.12` 与 Pydantic 2；使用独立实验环境，不改现有项目依赖。在该环境中缺少依赖时安装：

```bash
python -m pip install "pydantic>=2,<3"
```

**路径一：已有固定上游仓库。**

```bash
python verify_source_config.py --source-root /path/to/deer-flow
```

**路径二：只有[固定版本的配置文件][config]。** 保存原始文件字节为本机 `summarization_config.py`，替换下面路径：

```bash
python verify_source_config.py --source-file /path/to/summarization_config.py
```

不要把网页 HTML 保存成 Python 文件，也不要为绕过校验而修改脚本中的期望哈希。脚本接受的 Git blob 为 `965cd2ac12a95f912d822026de2c75dffc926922`。缺文件、版本不符或字节不匹配会明确失败，不会静默跳过再报告成功。

先预测三件事，再运行：

1. 不传配置时，`enabled`、`trigger` 与 `keep` 是什么？
2. 比例 `0.8` 和 `80` 是否都合法？
3. `enabled=true` 且未给触发项，能否仅凭配置构造成功宣称自动摘要已运行？

<details>
<summary>预测答案与验证边界</summary>

配置类默认未启用，`trigger=None`，保留最近 20 条消息。`0.8` 合法，`80` 不合法。允许构造某种配置，不代表服务已加载它、工厂已安装中间件，或本次已达到触发条件。

脚本验证默认值、范围、非法数值与可变默认值隔离，不运行摘要生成或整个工厂。自动触发的流程与失败条件须结合[上下文正文](01-context-lifecycle.md)和[实际摘要工厂][summary]理解。

</details>

## 5. 用手工轨迹检查理解，不把推演当集成测试

完成源码片段后，用正文已有例子练三条链：

| 任务 | 初始条件与操作 | 可核对结果 |
|---|---|---|
| 消息更新 | 只有 `h1`，提交日期 `h1` 与原话 `h1__user` | 同 ID 替换、新 ID 追加，共两条；不是整份历史任意拼接 |
| 工具往返 | 用户请求后，模型提出 `c1`，工具才执行并回填 | 模型提议与真实执行分开，结果用调用 ID 配对 |
| delta 恢复 | `C0 → C1 → C2`，选择 C0 恢复 | 先物化，再在当前头部写新状态继续，不把兄弟增量当所选历史 |

第一条是规则推演，不执行 LangGraph；第二条不调用真实工具；第三条不是数据库恢复实验。答案分别在[运行与消息轨迹](01-context-lifecycle.md#run-trace)和[检查点恢复](04-engineering-evaluation.md#checkpoint-recovery)。它们验证能否解释步骤，不替代运行证据。

## 6. 下一层验证什么

中间件与检查点需要上游要求的 Python 环境、锁定依赖与相应测试条件。固定快照中的 `backend/tests/test_summarization_middleware.py` 是摘要测试入口之一；应按该版本说明准备配置，不把一条命令说成所有平台都可直接成功。

真实语义提取、多用户服务隔离、远程 MCP 会话、沙箱、数据库恢复和浏览器回放属于更高层验证。运行结果分别记录，不把某次作者机器状态写成实验本身的永久性质。

源码片段版权说明：[上游 MIT License](#upstream-license)。

[config]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/config/summarization_config.py
[summary]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py

<a id="check-examples"></a>
## check_examples.py

```python
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

MODULE = Path.cwd() / "products/deer-flow"
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
```

<a id="verify-source-config"></a>
## verify_source_config.py

```python
"""Test one byte-pinned upstream source file, not a simulated DeerFlow service.

Usage (Python >= 3.12 and Pydantic 2):
    python verify_source_config.py --source-root /path/to/deer-flow
    python verify_source_config.py --source-file /path/to/summarization_config.py

No model, network, database, or sandbox is called. Only --report writes output.
The upstream source itself is intentionally not redistributed with this lab.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import types
import io
import json
from pathlib import Path
import platform
import sys
import unittest

UPSTREAM_COMMIT = 'e2feca1e567d9bafce657de8ad8bc668bd7ad513'
SOURCE_PATH = Path('backend/packages/harness/deerflow/config/summarization_config.py')
SOURCE_BLOB = '965cd2ac12a95f912d822026de2c75dffc926922'


def load_verified_source(path: Path):
    data = path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    if actual != SOURCE_BLOB:
        raise ValueError(f'Upstream bytes differ: expected {SOURCE_BLOB}, got {actual}. '
                         'Do not change the expected hash just to make this test pass.')
    # Execute exactly the verified bytes in memory: no second file read,
    # no __pycache__ written beside the upstream file.
    module = types.ModuleType('_deerflow_verified_summary_config')
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        exec(compile(data, str(path), 'exec'), module.__dict__)
    finally:
        sys.dont_write_bytecode = previous
    return module, actual


def build_tests(source):
    from pydantic import ValidationError

    class SourceConfigTests(unittest.TestCase):
        def test_automatic_summary_is_disabled_by_class_default(self):
            config = source.SummarizationConfig()
            self.assertIs(config.enabled, False)
            self.assertIsNone(config.model_name)
            self.assertIsNone(config.trigger)

        def test_retention_default_and_summary_input_budget_are_different(self):
            config = source.SummarizationConfig()
            self.assertEqual(config.keep.to_tuple(), ('messages', 20))
            self.assertEqual(config.trim_tokens_to_summarize, 4000)

        def test_fraction_including_one_is_valid(self):
            for value in (0.01, 0.8, 1):
                with self.subTest(value=value):
                    self.assertEqual(source.ContextSize(type='fraction', value=value).value, value)

        def test_percentage_style_and_nonpositive_fractions_are_rejected(self):
            for value in (80, 0, -0.1, 1.01):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='fraction', value=value)

        def test_nonfinite_values_are_rejected(self):
            for kind in ('fraction', 'tokens', 'messages'):
                for value in (float('nan'), float('inf'), -float('inf')):
                    with self.subTest(kind=kind, value=str(value)), self.assertRaises(ValidationError):
                        source.ContextSize(type=kind, value=value)

        def test_message_count_must_be_positive_integer(self):
            self.assertEqual(source.ContextSize(type='messages', value=20).to_tuple(), ('messages', 20))
            for value in (0, -1, 20.5, 20.0):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='messages', value=value)

        def test_absolute_token_threshold_is_positive(self):
            self.assertEqual(source.ContextSize(type='tokens', value=4000).value, 4000)
            for value in (0, -1):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='tokens', value=value)

        def test_unknown_threshold_kind_is_rejected(self):
            with self.assertRaises(ValidationError):
                source.ContextSize(type='percent', value=80)

        def test_explicit_configuration_is_not_a_claim_about_running_service(self):
            config = source.SummarizationConfig(
                enabled=True,
                trigger={'type': 'tokens', 'value': 32000},
                keep={'type': 'messages', 'value': 12},
            )
            self.assertTrue(config.enabled)
            self.assertEqual(config.trigger.to_tuple(), ('tokens', 32000))
            self.assertEqual(config.keep.to_tuple(), ('messages', 12))

        def test_mutable_default_lists_are_not_shared(self):
            a, b = source.SummarizationConfig(), source.SummarizationConfig()
            a.skill_file_read_tool_names.append('test_only_reader')
            self.assertNotIn('test_only_reader', b.skill_file_read_tool_names)

    return unittest.defaultTestLoader.loadTestsFromTestCase(SourceConfigTests)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument('--source-root', type=Path)
    location.add_argument('--source-file', type=Path)
    parser.add_argument('--report', type=Path, help='Optional JSON report path.')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error('Python >= 3.12 is required; no silent fallback to another version.')
    path = args.source_file or args.source_root / SOURCE_PATH
    try:
        pydantic_version = importlib.metadata.version('pydantic')
        if int(pydantic_version.split('.')[0]) != 2:
            raise RuntimeError(f'Pydantic 2 is required; installed {pydantic_version}')
        source, actual_blob = load_verified_source(path)
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(build_tests(source))
    except (OSError, ImportError, ValueError, RuntimeError) as exc:
        print(f'NOT RUN: {exc}', file=sys.stderr)
        return 2
    report = {
        'scope': 'byte-pinned upstream summarization_config.py only',
        'upstream_commit': UPSTREAM_COMMIT,
        'source_path': SOURCE_PATH.as_posix(),
        'verified_git_blob': actual_blob,
        'python': platform.python_version(),
        'pydantic': pydantic_version,
        'dependency_environment': 'local source-file test environment, not the full upstream uv.lock environment',
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'success': result.wasSuccessful(),
        'not_tested': ['agent assembly', 'summary generation', 'provider payload', 'memory queue',
                       'database durability', 'MCP', 'sandbox', 'end-to-end service'],
        'unittest_output': stream.getvalue(),
    }
    print(stream.getvalue(), end='')
    print(json.dumps({key: value for key, value in report.items() if key != 'unittest_output'},
                     ensure_ascii=False, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

<a id="upstream-license"></a>
## 上游许可

```text
MIT License

Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
Copyright (c) 2025-2026 DeerFlow Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
