# 21｜Coding Agent：Repo Understanding → Patch → Test → Verify

> 本章把旧 Coding Agent Workflow、Repository Understanding、Code Verification 与 AI-assisted Development Workflow 合并成完整工程链。重点不是“会用 Cursor/Claude Code/Codex”，而是：**怎样把真实软件任务从 Requirement 推进到可交付证据。**

## 1. 一条完整 Coding Agent 链

```text
Requirement
→ Clarify / Acceptance Criteria
→ Repo Discovery
→ Build Context
→ Plan
→ Patch
→ Test / Lint / Typecheck
→ Diff / Review
→ Fix Regression
→ Verify Outcome
→ Deliver
```

任何一步缺失，都可能出现“代码生成了，但不能交付”。

## 2. Repository Understanding

大型仓库不能把全部代码塞 Context。

常用能力：

```text
ripgrep / filesystem search
AST / symbol index
LSP / references
Dependency Graph
Vector / semantic retrieval
build/test metadata
```

没有一种方法包打天下。

### Keyword / ripgrep

适合精确 symbol、error string、config key。

### AST / LSP

适合定义、引用、类型、调用关系。

### Vector Retrieval

适合自然语言意图与语义相关文件，但对精确依赖关系较弱。

稳定模式通常是 Hybrid Repository Search。

## 3. Context 不是“相关文件越多越好”

Coding Context 可能包含：

```text
issue / requirement
relevant source files
interfaces / types
tests
build config
recent diff
error logs
project instructions
```

应按任务阶段动态加载，而不是一次塞整个 Repo。

## 4. Patch Boundary

Agent 修改前需要知道：

```text
哪些文件允许改？
是否允许 dependency change？
是否允许 migration？
是否能执行 shell？
是否能联网？
```

这把 Coding Agent 与 Permission / Sandbox 连接起来。

## 5. Verification Pyramid

```text
syntax / parse
→ typecheck / lint
→ targeted unit test
→ integration test
→ broader regression
→ diff review
→ task-specific acceptance
```

不是每次都必须跑全部测试，但至少要按风险选择验证层级。

## 6. Diff Review

Agent 生成 Patch 后应检查：

```text
unrelated changes
secret / debug code
API compatibility
error handling
security regression
performance concern
test coverage
```

模型自己的“解释”不能代替 Diff。

## 7. Retry / Rollback

错误 Patch：

```text
apply
→ tests fail
→ inspect failure
→ repair or revert
```

必须保存 Workspace Version，避免多轮修改后无法回到稳定点。

## 8. AI-assisted Development 的人机责任边界

人负责：

```text
problem framing
risk boundary
acceptance criteria
architecture decision
final accountability
```

Agent 擅长：

```text
repo search
boilerplate
candidate patch
mechanical refactor
test generation
iterative fix
```

真实研发流程不是“Vibe Coding = 不看代码”。

## 9. 源码 / Benchmark 证据

Claude Code 与 Codex 两套源码本身就是大型 Coding Agent Runtime 的实现样本：Tool、Repo Context、Permission、Sandbox、Trace、Compaction 都围绕长代码任务存在。

SWE-bench 以真实 GitHub issue + repository environment 验证模型是否真正解决问题，强调最终结果必须由环境和测试证明。

## 10. HUMAN-A

- `AGENT-036` Code Verification：24 来源；
- `AGENT-037` Repository Understanding：9 来源；
- `AGENT-048` AI-assisted / Vibe Coding Workflow：37 来源。

真人流程经常直接让候选人在真实项目里：

```text
读需求
→ 找代码
→ 用 AI 改
→ 跑测试
→ 解释 diff
→ 证明可交付
```

## 11. 🎯 面试回答

> Coding Agent 的核心不是生成 Patch，而是闭环：先从 Requirement 和 Acceptance Criteria 出发，用 ripgrep、AST/LSP、Dependency Graph、语义检索等组合做 Repo Understanding，按需构造 Context，再生成 Patch；之后必须用 lint/typecheck/test、diff review 和任务验收验证 Outcome，失败时可回滚和重试。人在风险边界、架构决策和最终责任上仍然不可缺席。

<details><summary>自测：为什么 Vector RAG 不能单独解决大型 Repo Understanding？</summary>

因为语义相似不等于符号引用和依赖关系；精确代码理解还需要 keyword search、AST/LSP、dependency/build/test 信息等结构化信号。
</details>