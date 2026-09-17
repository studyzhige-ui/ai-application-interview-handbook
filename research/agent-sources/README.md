# Agent Harness｜源码与权威资料索引

[← Agent Harness](../../agent-harness/README.md) · [↑ Handbook 总目录](../../README.md) · [Research 首页](../README.md)

> **用途：Tier B/C 技术证据。** 只补 Runtime 实现与工程原则，不改变 HUMAN-A Source Count。

---

更新日期：2026-09-11

> 本目录是 **已完成的 Agent Harness / Runtime 23-block 教材**的证据底座，也服务后续版本维护。它不创建新的 HUMAN-A 面试证据，也不改变 `research/questions/agent-harness.md` 中任何 Source Count。

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

正式教材：[`../../agent-harness/README.md`](../../agent-harness/README.md)

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

后续若跟随新版本，必须显式记录新的 commit，不能静默覆盖旧结论。

---

## 4. 当前教材映射

研究层 Capability 很细，教材层已稳定为 23 个知识小板块：

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

## 5. 后续维护规则

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

只有后者才考虑新增教材文件，避免再次退回“一能力一文件”的旧粒度。


<a id="reader-revision-20260917"></a>

## 2026-09-17｜main读者反馈修订的核验范围

本轮只修改main的23章Agent教材及关联说明，不改16章架构分支、不重开真人采集。教学正文采用“概念中文解释→连续例子→机制→固定源码/官方对照→章末三件套”。材料类型不混用：

| 类型 | 本轮使用方式 | 不声称 |
|---|---|---|
| 用户反馈 | 确定哪里解释不足，逐章回读改写 | 把读者困惑归咎于只学一遍 |
| main既有教材 | 保留机制范围、章节和细粒度训练价值 | 每个旧句子都正确或必须照搬 |
| 固定Codex源码 | 直接读取以下路径解释实现 | 代表当前所有分发版/开关 |
| 用户提供的Claude源码快照 | 读取相应路径和条件分支 | 已独立鉴定为某公开发行版源码 |
| 官方规范/框架文档 | 解释明确版本的核心语义 | 新协议所有能力已被旧产品快照实现 |
| 教学代码和假设 | 无网络的控制逻辑/投影/恢复示意 | 等价于真实LLM、持久存储和沙箱集成测试 |

### Codex固定提交与阅读入口

提交仍为`fc948f8c473e5d11e780ffcf1fd7f812a2020932`，本轮读取公开快照，重点核对：

| 教材问题 | 直接阅读路径/符号 |
|---|---|
| 注册与模型说明 | `codex-rs/core/src/tools/router.rs`的Registry与model_visible_specs；`session/turn.rs::build_prompt` |
| 计划在哪里 | `codex-rs/core/src/tools/handlers/plan.rs`的update_plan、PlanUpdate与确认结果 |
| 初始上下文与追加 | `codex-rs/core/src/session/mod.rs::build_initial_context_with_world_state`及上下文更新；`session/turn.rs` |
| 压缩触发与分支 | `session/context_window.rs`、`session/turn.rs::run_auto_compact`、`core/src/compact.rs` |
| 摘要提示与形态 | `codex-rs/prompts/templates/compact/prompt.md`及summary_prefix.md，本地输出是摘要文本而非固定JSON |
| 记忆生命周期 | `codex-rs/memories/README.md`的启动资格、旧会话提取、两阶段整合与读取职责 |
| 恢复/观测边界 | `session/mod.rs`选定rollout项与`codex-rs/rollout-trace/README.md`；不代替自定义业务账本 |

### Claude用户固定快照与阅读入口

提交仍为`58231dcce408f805c645cfbc352d2876b517223b`。该仓库这些路径在根目录，不加错误的`src/`前缀。

| 教材问题 | 本轮核对的实现 |
|---|---|
| 工具选择/投影 | `tools.ts`的getAllBaseTools/getTools；`utils/api.ts::toolToAPISchema` |
| 请求真实编排 | `query.ts`的消息视图处理与callModel参数；`utils/api.ts`的appendSystemContext/prependUserContext |
| 新输入与取消 | `query.ts`工具结果完成后的队列筛选/附件注入、按Agent范围过滤和abort分支 |
| 待办计划 | `tools/TodoWriteTool/TodoWriteTool.ts`的当前清单、旧/新数据与模型确认，区别Todo V2及Plan Mode |
| 自动压缩阈值 | `services/compact/autoCompact.ts`的有效窗口、输出预留、13k余量与开关/失败保护 |
| 压缩后顺序 | `services/compact/compact.ts::buildPostCompactMessages`的边界、摘要、保留消息、附件、Hook结果 |
| 微压缩与补救 | `services/compact/microCompact.ts`的工具结果清理；query中可选snip/collapse/reactive路径 |
| 文件型记忆 | `memdir/memdir.ts`的保存指导、索引/主题文件与更新删除；官方Memory文档补使用语义 |

### 官方规范与框架版本口径

- [MCP 2026-07-28架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)：Host/Client/Server、无状态请求元数据、发现与调用；对照[2025-11-25初始化](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)，不混写。
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)、[Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)、[架构职责](https://modelcontextprotocol.io/specification/2026-07-28/architecture)：工具目录、调用、额外输入、权限与材料边界。部分概览仍提旧sampling描述，具体弃用状态依用户指定版本架构页说明，不从旧概览推导新实现。
- [A2A官方规范](https://a2a-protocol.org/latest/specification/)：本轮读取1.0对象和绑定；SendMessage/Task/Artifact与0.3方法命名分开。
- [Claude Memory](https://code.claude.com/docs/en/memory)、[工作过程](https://code.claude.com/docs/en/how-claude-code-works)、[Sandboxing](https://code.claude.com/docs/en/sandboxing)与[Docker安全](https://docs.docker.com/engine/security/)：用户体验/产品范围与隔离边界。
- [Agents SDK Runner](https://openai.github.io/openai-agents-python/running_agents/)、[Sessions](https://openai.github.io/openai-agents-python/sessions/)、[Handoffs](https://openai.github.io/openai-agents-python/handoffs/)、[Tracing](https://openai.github.io/openai-agents-python/tracing/)：执行、会话、交接和诊断不同责任。
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)：Checkpointer/Store、恢复单位与create_agent的真实关系。

官方可变页面以本次查阅日期为界；后续升级需要重新核对，不把官方当前页与固定源码拼成同一个不存在的版本。详见[读者修订记录](../../roadmap/agent-reader-revision.md)。
