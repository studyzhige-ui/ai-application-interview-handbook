# Agent｜源码与权威资料索引

[← Agent Harness](../../curriculum/09-agent/README.md) · [↑ Handbook 总目录](../../README.md) · [Market 首页](../../market/README.md)

> **用途：Tier B/C 技术证据。** 只补 Runtime 实现与工程原则，不改变 HUMAN-A Source Count。

---

证据核验日期：2026-09-11

> 本目录是 **Agent Harness / Runtime 24 章教材**的技术证据底座，服务源码、规范与版本事实校准。它不创建 HUMAN-A 面试证据，也不改变 `interview/canonical/agent-harness.md` 中的 Source Count。

## 1. 四层证据体系

### Tier A｜HUMAN-A 真人面试证据

来源：

- `interview/canonical/agent-harness.md`
- `market/analysis/follow-up-chains.md`
- `market/interviews/batch-01.md` ～ `batch-26.md`

负责回答：

```text
企业实际在问什么？
→ 问到多深？
→ 常见追问怎样递进？
```

Canonical 统计基线：**44 道 Agent Harness / Runtime Primary Canonical**。频率只能由 Tier A 决定。

### Tier B｜成熟产品源码

一级参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

负责回答成熟 Coding Agent 实际如何处理 Tool、Context、Permission、Session、Task、Trace 等 Runtime 问题。

源码索引：

- [`claude-code-source-index.md`](claude-code-source-index.md)
- [`codex-source-index.md`](codex-source-index.md)

### Tier C｜官方文章、开放规范与原始论文

优先：Anthropic / OpenAI 官方工程文章、OpenAI Agents SDK 官方文档、MCP / A2A 官方规范、ReAct / SWE-bench 等原始论文。

负责回答哪些设计原则跨产品成立。

索引：[`authoritative-web-sources.md`](authoritative-web-sources.md)

### Tier D｜课程抽象

Tier D 不是新的事实来源，而是把 A+B+C 抽象成适合初学者的稳定知识体系。

能力入口：[`runtime-capability-map.md`](runtime-capability-map.md)

正式教材：[Agent教材](../../curriculum/09-agent/README.md)

---

## 2. 冲突处理顺序

```text
市场频率 → 只认 Tier A
具体产品实现 → 以对应 Tier B 固定源码快照为准
协议定义 → 以 Tier C 官方规范为准
课程顺序 / 文件粒度 → 以 beginner-first 知识依赖与认知闭环为准
```

因此：

- Claude Code 某个版本怎样做 Permission，不代表所有 Agent 必须同构实现；
- MCP 官方 Tool / Resource / Prompt 边界，不因产品 UI 而改变；
- Context Compaction 即使面试频率极高，也必须先学 Context Assembly；
- 外部文章即使权威，也不能增加 HUMAN-A Source Count；
- 源码中一个独立 class / primitive 不自动对应一个 Markdown 文件。

---

## 3. 固定源码快照

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

版本更新规则：如切换源码快照，必须显式记录新的 commit，并保留原快照对应结论的可追溯性。

---

## 4. 教材映射

研究层 Capability 粒度更细，教材层组织为 24 个知识小板块：

```text
Agent / Workflow / Harness
→ Loop / Event / State
→ Tool Runtime
→ Planning / Goal / Stop / Budget
→ Context Assembly / Compaction
→ Memory / Session / Checkpoint
→ Permission / Sandbox / Injection
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping
```

Capability 到教材的正式映射见 [`runtime-capability-map.md`](runtime-capability-map.md)。

---

## 5. 维护规则

如果未来：

- Claude Code / Codex Runtime 演进；
- MCP / A2A 规范更新；
- HUMAN-A 新阶段重新开放采集；
- Agent Framework 出现新的稳定 Runtime Primitive；

先更新对应证据索引，再判断：

```text
只是章节内新 Section？
还是形成新的独立认知闭环？
```

只有形成新的独立认知闭环时才新增教材文件，以保持稳定的课程粒度。


<a id="reader-revision-20260917"></a>

## 6. 读者修订与核验记录

读者反馈、逐章修订、固定源码阅读路径与测试范围属于项目演进记录，统一维护在 [Agent Reader Revision](../../guide/project/agent-reader-revision.md)。本 README 只维护可复用的证据体系、固定源码快照、教材映射和版本更新规则。
