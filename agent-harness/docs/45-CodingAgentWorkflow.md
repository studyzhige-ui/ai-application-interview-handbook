# 45｜Coding Agent：Repo Understanding → Patch → Test → Verify

## 1. Coding Agent 不等于代码生成

完整链：

```text
Requirement / Issue
→ Repository Discovery
→ Read / Search / Inspect
→ Hypothesis
→ Modify
→ Test / Lint / Typecheck
→ Diff / Review
→ Verify Outcome
→ Deliver
```

HUMAN-A 中 AI-assisted Development Workflow、Repository Understanding、Code Verification 都是独立高频能力。

## 2. Repository Understanding

大 Repo 不应全塞 Context：

```text
filesystem / glob / grep
symbol / AST / LSP
repo instructions
selective read
```

先定位，再读相关代码。

## 3. Patch 之后必须验证

最低：

```text
focused test
→ broader test
→ lint/typecheck
→ inspect diff
```

根据项目增加 build / integration / e2e。

## 4. Verification 和“模型自评”不同

模型说：

> 我已经修复。

证据应该是：

```text
failing test before
passing test after
expected behavior
clean diff
```

## 5. AI-assisted Development 是人机 Workflow

成熟使用方式还包括：

```text
需求澄清
Context 提供
Agent 生成/修改
人看 Diff
自动测试
验收
```

不是“Prompt 越长越好”。

## 🎯 面试

Coding Agent 的核心不是生成代码，而是 Repo Understanding + safe modification + verification loop。大 Repo 用搜索/符号工具渐进取 Context，修改后用 tests/lint/typecheck/diff 验证，最终以可执行证据而不是模型自述作为完成条件。

<details><summary>自测：为什么测试通过仍可能不够？</summary>

测试可能覆盖不足或 Agent 为了过测试做了错误 workaround；还要看 diff、需求语义和必要的集成验证。
</details>
