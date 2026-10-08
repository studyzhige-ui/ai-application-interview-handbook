# DeepSeek Harness｜从一个恢复测试开始验证

## 使用本页代码

本页保留源码实验说明与完整验证程序。将下方对应 Python 代码块保存到自己的临时工作目录，文件名与小节标题一致；命令中的脚本名可替换为该文件的绝对路径。不要把源码片段检查结果当成完整产品实测。


[← 模块入口](README.md) · [上下文](01-context-lifecycle.md) · [记忆](02-memory-lifecycle.md) · [工具](03-tool-lifecycle.md) · [工程](04-engineering-evaluation.md)

读过恢复章节后，先验证一个很小的问题：**只有工具调用意图，与已经记录调用却没有结果，恢复时是否会得到不同标记？** 这不需要真实模型密钥，也不需要先搭好完整界面。

本页先给固定上游测试的一条完整路径，再列出真实产品实验。使用真实实现和既有测试，不另造一份近似 Harness 证明教材正确。所有命令只用于独立实验目录，不重置共享仓库或真实会话。

## 1. 准备两个互不混用的目录

| 目录 | 用来做什么 |
|---|---|
| Handbook 检出 | 阅读本页、运行 `verify_snapshot.py`，阅读 Coding 分页契约 |
| 独立 DSH 检出 | 固定上游版本、安装其依赖、运行上游测试 |

运行 DSH 要求 Node `^22.19.0 || >=24.0.0`、`pnpm@11.7.0`。Python 仅用于本页的只读检查脚本和后面的分页练习，不是 DSH 的实现语言。[固定版本声明][package]

已经有独立上游检出就核对它，不必重复克隆。没有时，在你自己的实验父目录执行：

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git deepseek-harness-reader-lab
cd deepseek-harness-reader-lab
git checkout --detach 477b4f420553e8a52c2fbccc464d7561b239c443
git rev-parse HEAD
node --version
pnpm --version
```

`--detach` 让实验固定在给定提交，而非跟随分支移动。最后三条命令分别确认实际源码和工具版本；不要在有其他工作的目录执行切换。联网克隆与安装失败属于环境阻塞，不是产品行为失败。

将本页附录保存为 `verify_snapshot.py` 后，从自己的临时工作目录运行：

```bash
python verify_snapshot.py /path/to/deepseek-harness-reader-lab
```

把示例路径换成实际检出位置。脚本只读取 Git、关键源码字节、包版本及本机版本，不安装依赖、不切换源码、不调用模型。返回码 `0` 表示所检查前提未发现阻塞；`2` 表示需先解决差异。**两种结果都不是上游测试成绩。** CRLF 自动转换导致字节不同会被拒绝；应在自己的检出核对换行设置，不修改预期哈希掩盖差异。

<a id="first-test"></a>
## 2. 最小闭环：运行一个真实的恢复测试文件

### 2.1 准备依赖并选定测试

在固定的 DSH 检出根目录，阅读[上游开发约定][agents]后执行：

```bash
pnpm install --frozen-lockfile
pnpm run build:native-system
pnpm exec vitest run packages/core/session/tests/repair.spec.ts --reporter=verbose
```

逐条确认上一条成功，再继续下一条。

| 命令 | 作用 | 失败时先检查什么 |
|---|---|---|
| `pnpm install --frozen-lockfile` | 按既有锁文件安装工作区依赖，不更新锁文件 | 网络、Node/pnpm 版本、依赖安装错误 |
| `pnpm run build:native-system` | 准备上游标准测试入口使用的本机系统扩展 | 上游原生构建所需工具链与平台支持 |
| `pnpm exec vitest run …` | 用已安装的 Vitest 运行指定恢复测试文件 | 工作目录、测试路径、配置与具体失败断言 |

命令依据根 `package.json`：标准 `test` 先运行原生构建，再运行 Vitest。本页拆成两步，便于区分环境构建与行为测试。根 `vitest.config.ts` 包含这个测试路径，并配置源码路径解析和测试初始化；不要复制单个 `.spec.ts` 到空目录运行。[脚本][package]、[测试配置][vitest]

原生构建失败时，按[上游原生组件说明][native]解决所需编译环境；不要删测试或跳过失败后声称通过。本页没有在当前编写环境实际执行上述上游命令，运行结果必须由自己的实验记录确认。

### 2.2 先预测两组输入，再观察断言

测试文件直接调用真实恢复函数，并用构造的会话事件检验分支。它是**真实实现的单元测试**，不是实际杀掉一个生产 Agent。

| 测试名中的识别片段 | 构造的初始状态 | 断言检查什么 |
|---|---|---|
| `marks an assistant tool request with no recorded call as not started` | 开放的 Turn、Step，有助手工具意图，没有 `tool/call` | 补工具结果、步骤结束与轮次结束；错误码是 `TOOL_NOT_STARTED` |
| `synthesized tool/result carries surfaceOp and sourceEventSeqs when tool/call was logged` | 上述意图后又记录 `tool/call`，仍没有结果 | 合成错误为 `TOOL_OUTCOME_UNKNOWN`，保留来源序号与核验副作用的提示 |

先在[原测试][repair-test]找到这两处 `it(...)`，看传入的事件数组，再看 `expect(...)` 比较的值。**区别不是函数随机返回两种错误，而是第二组多了一条调用开始记录。**

只想聚焦第一条测试时，在同一个上游根目录执行：

```bash
pnpm exec vitest run packages/core/session/tests/repair.spec.ts -t "marks an assistant tool request with no recorded call as not started" --reporter=verbose
```

`-t` 按测试名称过滤，`--reporter=verbose` 展示执行明细。该用例位于 `describe.each` 中，分别检查 interrupted 与 forked 两种原因，因此可能看到同一断言的多次执行；以实际报告为准，不把被过滤测试算作通过。

### 2.3 怎样判断这次实验有没有完成

保存命令退出码、实际测试名称、通过/失败/跳过数量，并用自己的话解释：为什么第二组是结果未知，而不是自动重试成功。

- **找到测试但断言失败：** 保存差异，确认固定源码、实际版本与测试初始化，不改断言迎合输出。
- **没有找到测试：** 检查是否在上游根目录、路径和筛选字符串是否一致；零测试不是通过。
- **安装或原生构建失败：** 记录阻塞，行为测试为未执行。
- **测试通过：** 只证明这些构造输入下真实恢复函数满足断言，不证明磁盘抗断电、实际模型调用或远端操作恰好一次。

该文件还有已闭合日志、已存在结果、分叉提示与公开恢复入口等用例。第一次闭环完成后，再按[工程章](04-engineering-evaluation.md#semantic-recovery)的问题扩展读取，不需要一开始就跑全仓库测试。

## 3. 再准备一个真实编码任务

产品实验沿用 [AI Coding 的分页契约](../../practice/coding/docs/09-ai-coding.md)。在自己的独立实验目录建立 `README.md`、`pagination.py`、`test_pagination.py`，按契约编写测试，再用错误偏移构造可复现的初始缺陷。

在这个练习目录运行：

```bash
python -m unittest discover -v
```

初始实现故意有缺陷，应先得到可解释的失败：默认第一页本应返回 `[10, 20]`，错误偏移却得到 `[30]`。修复还必须满足非法参数、空数据、末页、越界页、不修改原列表等原有约定，不能只换公式就宣布全部完成。[任务与失败定位][coding]

运行真实 DSH 前，按上游支持的 Profile 入口准备模型和权限，明确指向这个练习副本。不得修改测试。保存初始文件副本或哈希、实际工具调用、最终 diff 与同版本测试结果。每轮只重置自己的练习副本，不操作其他对话正在修改的仓库。

## 4. 实验 A：补充要求何时进入请求

**前提：** 使用新会话和独立工作目录，真实入口能观察请求与事件；否则选择上游对应单元测试，并注明验证层不同。

**任务：** 模型第一次读取期间，补充“第二页应返回 `[30]`”；检查入口把它作为 Queue 还是 Steer 处理。另一次仅注入背景、不唤醒，观察有无独立请求。

**观察顺序：** 入队事件 → 领取 → 用户消息提交 → 下一次实际请求。已发送请求不会被追溯修改，背景入队不等于服务端收到，同一步重试不应重复追加用户输入。

<details>
<summary>检查提示</summary>

从 `agent.ts`、`inbox.ts` 追真实入口，不从按钮文字推测行为。只读环境脚本不模拟调度；真实请求证据缺失时，不能只凭界面回答判断输入已送达。

</details>

## 5. 实验 B：引用快照与外部记忆分别验证

**初始状态：** A 记录唯一测试字符串，B 显式引用 A；之后 A 更正字符串。另建没有引用 A 的 C。

**任务与结果：** B 的旧快照不自动更新；普通工具结果不会全部导入引用。外部记忆子任务则要显式启用真实服务，观察 A 的写工具与 C 的读工具，确认同一存储范围、正确标记及实际使用。引用成功不能替代外部记忆成功。

**清理：** 用测试账户和独立空间，按服务真实删除接口清理，再在新会话核对；不猜统一删除命令，不删共享目录。未配置服务则对应子任务为未执行。

## 6. 实验 C：工具执行与结果传播

**前提：** 使用固定上游工具、调度测试中的相应案例；秘密样本只用专用测试字符串。

**任务：** 分别检查批准后 guard 否决、只替换 `content`、A/B 反序完成三种条件。观察业务调用计数、规范值、模型内容与结果提交顺序。

**结果：** 守卫拒绝时业务未运行；只替换展示可能保留原规范值；允许并行的读取仍按模型顺序回填。`timeoutMs` 的执行还依赖超时策略。不能由此推导任意写入可取消、任意共享文件可并行或真实秘密全通道安全。

## 7. 实验 D：从恢复函数扩展到真实中断

最小实验已经核对合成标记，现在才扩大到实际持久化和工具边界。**只在隔离副本故障注入，不破坏真实用户会话文件。** 优先使用上游后端测试已有注入点。

分别截断在调用前、调用后但结果未可靠保存、结果已保存三个时点。记录磁盘与会话状态；文件已写而结果未知时，恢复后先只读检查，再决定是否重试。

检查合成错误没有冒充真实回执，不支持的新格式没有静默回退，尾部修复没有掩盖完整记录损坏。真实进程崩溃、Windows/POSIX 锁、断电持久性与远端取消各自验证，纯函数单元测试不能替代它们。

## 8. 最终记录卡

| 项目 | 本次填写什么 |
|---|---|
| 源码与环境 | 实际 SHA、Node/pnpm、平台、工作区差异 |
| 生效配置 | Profile、插件、权限、模型路由；不记录秘密 |
| 测试身份 | 文件与测试名，或真实任务及输入 |
| 实际执行 | 命令、退出码、调用与结果记录 |
| 验收结果 | 测试数量、失败与跳过原因、文件 diff、测试未改证据 |
| 验证边界 | 源码、单元测试、模拟、真实服务、跨平台分别填，不以空白当通过 |

初学者先完成第 2 节的一个闭环，便有可检查的实验结果；后面的真实任务逐项追加证据。最终模型结束仍不能替代文件、测试和授权约束的共同验收。

[package]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/package.json
[agents]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/AGENTS.md
[vitest]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/vitest.config.ts
[native]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/native/README.md
[repair-test]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/session/tests/repair.spec.ts
[coding]: ../../practice/coding/docs/09-ai-coding.md

<a id="verify-snapshot"></a>
## verify_snapshot.py

```python
#!/usr/bin/env python3
"""Read-only source/environment gate. It does NOT run DeepSeek Harness tests."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

TARGET_SHA = '477b4f420553e8a52c2fbccc464d7561b239c443'
TARGET_VERSION = '0.1.7-rc.2'
CRITICAL_BLOBS = {
    'packages/core/agent-loop/src/agent.ts': 'bcd7ad17a82699c395c3a14855cdee6ed4a2b905',
    'packages/core/agent-loop/src/inbox.ts': 'ef00887a544c2dededb484ff7b9ce0efe83dea21',
    'packages/core/agent-loop/src/tool-calls.ts': 'f1f6256cb1e776e3b300f5cfaac8c6c344c5b03d',
    'packages/core/session/src/repair.ts': 'b87a69c35122cb5aedea5545259604cdbce7971e',
    'packages/core/tools/src/schema.ts': '5aea4f4f7fecb2b3408608e3abd5f97436d7e437',
    'packages/session/session-format-catalog/src/generated.ts': 'eab9d914564be9be6ccd331562bd9d4be97a6bd9',
    'packages/session/session-checkpoint-policy/src/index.ts': '0fc456eb08853b9fe54d0bf9ca3a26c05b4413cf',
    'packages/subagent/subagent/src/child-agent.ts': '0004567a30f5f9e50a91518c071ed87ce72ae671',
}
TEST_ROOTS = (
    'packages/core/agent-loop/', 'packages/core/session/', 'packages/core/tools/',
    'packages/context/session-reference/', 'packages/compaction/compaction-basic/',
    'packages/session/session-persistence-jsonl/', 'packages/subagent/subagent/',
)

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def supported_node(text: str) -> bool:
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', text.strip())
    if not match:
        return False
    major, minor, patch = map(int, match.groups())
    return (major == 22 and (minor, patch) >= (19, 0)) or major >= 24

def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), capture_output=True, text=True, timeout=25)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f'{args[0]} exited {result.returncode}')
    return result.stdout.strip()

def version(name: str) -> str | None:
    executable = shutil.which(name)
    if not executable:
        return None
    try:
        return run([executable, '--version'])
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        return f'ERROR: {exc}'

def inspect(root: Path) -> dict:
    root = root.resolve(strict=True)
    head = run(['git', 'rev-parse', 'HEAD'], root)
    status = run(['git', 'status', '--porcelain=v1', '--untracked-files=no'], root)
    package = json.loads((root / 'package.json').read_text(encoding='utf-8'))
    node, pnpm = version('node'), version('pnpm')
    blockers: list[str] = []
    if head != TARGET_SHA:
        blockers.append('HEAD differs from the teaching snapshot')
    if status:
        blockers.append('Tracked source has local changes; inspect before interpreting results')
    if package.get('version') != TARGET_VERSION:
        blockers.append('package.json version differs from the teaching snapshot')
    if not node or not supported_node(node):
        blockers.append('Node does not satisfy ^22.19.0 || >=24.0.0')
    manager = package.get('packageManager', '')
    required_pnpm = manager.split('@', 1)[1].split('+', 1)[0] if manager.startswith('pnpm@') else None
    if not required_pnpm or pnpm != required_pnpm:
        blockers.append(f'pnpm must match packageManager ({manager})')
    blobs: dict[str, dict] = {}
    for relative, expected in CRITICAL_BLOBS.items():
        path = root / relative
        actual = git_blob(path.read_bytes()) if path.is_file() else None
        blobs[relative] = {'expected': expected, 'actual': actual, 'match': actual == expected}
        if actual != expected:
            blockers.append(f'Source bytes differ or are missing: {relative}')
    tracked = run(['git', 'ls-files', '-z'], root).split('\0')
    tests = sorted(p for p in tracked if p.startswith(TEST_ROOTS) and p.endswith(('.test.ts', '.spec.ts')))
    return {
        'kind': 'source-and-environment-gate-only', 'checkout': str(root),
        'head': head, 'target_sha': TARGET_SHA, 'version': package.get('version'),
        'node': node, 'pnpm': pnpm, 'package_manager': manager,
        'critical_source_blobs': blobs, 'discovered_test_files': tests,
        'blockers': blockers, 'ready_for_test_setup': not blockers,
        'product_tests_executed': False, 'real_service_executed': False,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, help='Existing upstream checkout; never fetched or changed')
    args = parser.parse_args()
    try:
        report = inspect(args.checkout)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'error': str(exc), 'product_tests_executed': False}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ready_for_test_setup'] else 2

if __name__ == '__main__':
    sys.exit(main())
```
