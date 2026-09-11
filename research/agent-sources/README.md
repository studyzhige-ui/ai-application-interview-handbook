# Agent Harness / Runtime Evidence Base

更新日期：2026-09-11

> 本目录服务于 Phase 3 的 Agent Harness / Runtime 正式教材建设。它不创建新的 HUMAN-A 面试证据，也不改变 `research/questions/agent-harness.md` 中任何 Source Count。

## 1. 四层证据体系

### Tier A｜HUMAN-A 真人面试证据

来源：

- `research/questions/agent-harness.md`
- `research/analysis/follow-up-chains.md`
- `research/interviews/batch-01.md` ～ `batch-26.md`

负责回答：

```text
企业实际在问什么？
→ 问到多深？
→ 常见追问怎样递进？
```

当前冻结口径：**44 道 Agent Harness / Runtime Primary Canonical**。频率只能由 Tier A 决定。

### Tier B｜成熟产品源码

一级参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

负责回答：

```text
成熟 Coding Agent 实际需要哪些 Runtime 能力？
→ 状态怎样组织？
→ Tool 怎样执行？
→ Context 怎样压缩？
→ Permission / Sandbox 怎样落地？
→ Session / Task / Trace 怎样存在于代码中？
```

源码索引：

- [`claude-code-source-index.md`](claude-code-source-index.md)
- [`codex-source-index.md`](codex-source-index.md)

### Tier C｜官方文章、开放规范与原始论文

优先：Anthropic / OpenAI 官方工程文章、OpenAI Agents SDK 官方文档、MCP / A2A 官方规范、ReAct / SWE-bench 等原始论文。

负责回答：

```text
哪些设计原则跨产品成立？
→ Workflow 与 Agent 怎样区分？
→ Context Engineering 怎样抽象？
→ HITL / Guardrail / Trace / Eval 怎样组织？
→ MCP / A2A 的协议边界是什么？
```

索引：[`authoritative-web-sources.md`](authoritative-web-sources.md)

### Tier D｜课程抽象

Tier D 不是新的事实来源，而是把 A + B + C 抽象为适合初学者的稳定知识体系。

入口：[`runtime-capability-map.md`](runtime-capability-map.md)

---

## 2. 冲突处理顺序

不同证据回答不同问题，不简单互相覆盖：

```text
市场频率
→ 只认 Tier A

具体产品实现
→ 以对应 Tier B 源码为准

协议定义
→ 以 Tier C 官方规范为准

课程顺序
→ 以初学者 0→1 的知识依赖为准
```

例如：

- Claude Code 某个版本怎样做 Permission，不代表所有 Agent 都必须同构实现；
- MCP 官方定义的 Tool / Resource / Prompt 控制边界，不因某个产品 UI 不暴露全部 primitive 而改变；
- Context Compaction 即使面试频率很高，也不能在学生理解 Context Assembly / Runtime State 之前开讲；
- 外部文章即使非常权威，也不能增加 HUMAN-A Source Count。

---

## 3. 固定源码快照

为避免“今天看到的实现”和以后 main/master 漂移混在一起，本轮课程设计先固定：

```text
Claude Code
repo   = studyzhige-ui/claude-code-source-private
branch = master
commit = 58231dcce408f805c645cfbc352d2876b517223b

OpenAI Codex
repo   = openai/codex
branch = main
commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

后续章节如果重新跟随新版本，必须显式记录新的 commit，而不是静默覆盖旧结论。

---

## 4. 课程构建规则

Agent Harness 是整套 Handbook 中最容易被框架 API 带偏的模块，因此固定：

> **先学 Runtime Problem → 再学 Runtime Primitive → 再看 Claude Code / Codex 怎么实现 → 最后才映射 LangGraph / LangChain / OpenAI Agents SDK 等 Framework。**

正式教材不能写成：

```text
安装 LangGraph
→ 定义 Node
→ 定义 Edge
→ 做一个 Demo
```

而应先回答：

```text
Agent 为什么需要 Loop？
→ 一轮 Runtime 到底发生什么？
→ Model / Tool / State / Context 怎样交互？
→ 中途失败、取消、权限不足、Context 爆掉怎么办？
→ 长任务怎样恢复？
→ 怎样证明 Agent 真的完成任务？
```
