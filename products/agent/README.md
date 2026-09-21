# Agent Products｜成熟 Agent 产品源码学习

[↑ Products](../README.md) · [Agent Curriculum](../../curriculum/09-agent/README.md) · [Agent References](../../references/agent/README.md) · [Learning Path](../../guide/learning-path.md)

> 本目录沿固定源码快照学习成熟 Agent 产品怎样把 Context、Memory、Tool、Permission、Persistence、Recovery、Trace 与 Evaluation 组合成真实运行时。

## 1. 学习对象与职责

[Agent Curriculum](../../curriculum/09-agent/README.md) 建立 Agent 的稳定知识模型；本目录回到完整成熟产品，沿真实数据结构、调用入口、状态变化和 Failure Path 做系统解剖。

这里不重复定义“Context 是什么”“Memory 是什么”，而是追问：

```text
一个真实用户任务从哪里进入？
→ 模型这一轮到底看见什么？
→ 长期信息怎样写入、召回和纠正？
→ 工具怎样被发现、授权、执行并回填？
→ 中断、超限、权限拒绝、工具失败以后怎样继续？
→ Trace / Test / Eval 怎样证明系统行为？
```

## 2. 固定学习结构

每个产品保持同一组一级观察视角，便于横向比较：

```text
README.md                   系统地图、源码快照、关键模块与阅读顺序
01-context-lifecycle.md     上下文从输入到请求、压缩、恢复的完整生命周期
02-memory-lifecycle.md      记忆从发现、提取、整理到召回、维护、评测的完整生命周期
03-tool-lifecycle.md        工具从注册、发现、暴露到权限、执行、回填的完整生命周期
04-engineering-evaluation.md
                            系统边界、Failure、规模化、诊断与评测
```

一级结构固定，二级结构以各产品源码真实实现为准，不强迫不同产品拥有相同的类名、存储介质或控制流。

## 3. 产品目录与固定源码快照

| 产品 | 固定源码快照 | 学习入口 |
|---|---|---|
| OpenAI Codex | `openai/codex@bb054a2b03f15787dcc2f9bd8ebfde713bc5b695` | [进入](codex/README.md) |
| Claude Code | `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b` | [进入](claude-code/README.md) |
| DeepSeek Harness | `deepseek-ai/deepseek-harness@ddefc45fbc7f8e46dd73185e68295696d1297887` | [进入](deepseek-harness/README.md) |
| DeerFlow 2.0 | `bytedance/deer-flow@29d285731b326a728a9df33d3641f73b68bbe48b` | [进入](deer-flow/README.md) |

技术证据和版本边界统一回到 [Agent References](../../references/agent/README.md)。

## 4. 四个产品的真实架构对照

下面的“设计中心”是基于固定源码快照做的工程抽象，不是四家公司共同采用的官方术语。比较的目的不是给产品排优劣，而是回答同一个系统问题在四套真实 Runtime 中分别由什么机制承担。

| 产品 | 设计中心 | 执行骨架 | 状态 / 历史 | Model Context 怎样形成 | 能力怎样扩展 | 恢复与诊断 |
|---|---|---|---|---|---|---|
| [OpenAI Codex](codex/README.md) | **强类型 Core + Lifecycle Extensions** | App Server / CLI → ThreadManager → Session → Turn → StepContext → Model / Tool Runtime | Conversation History、Thread Store、Rollout、State DB 分工，不压成单一存储 | StepContext 固定本次采样附近的执行配置；History、Context Fragments、World State 与本轮 Tool Set 共同形成请求 | Extension Registry 接 Memory / MCP / Skills / Guardian / Goal 等；Tool Runtime 统一执行 | Resume / Fork 依赖持久状态；Rollout Trace / Analytics / Tests 提供更深诊断证据 |
| [Claude Code](claude-code/README.md) | **Query-loop 驱动的 Context / Cache / Capability 编排** | REPL 或 QueryEngine → query() → queryLoop() → Model → Tool → 下一次迭代 | parent-linked Transcript + Session / File / Worktree / Content-Replacement 等恢复状态 | 每次 API 请求前经过 Tool Result Budget、Snip、Microcompact、Context Collapse、Auto Compact，并叠加 Memory / Skill 预取与可见 Tool | 动态 Tool Pool、MCP、Skills、AgentTool 围绕共享 ToolUseContext / query loop 接入 | Transcript parentUuid 链、Session Restore、Retry / Fallback、Telemetry 共同维持长会话 |
| [DeepSeek Harness](deepseek-harness/README.md) | **Cordis Plugin Composition + Event-Sourced Session** | Profile / Bundle → Cordis Plugin Tree → Agent Loop → Session Log / Surface → Model / Tool | Append-only SessionEvent Log 是持久事实；Surface 是模型可见投影 | deriveMessages() 从 Surface 构造请求；Compaction / Pruning 用 replacement 改投影而不删除原始事实 | Service / Provider / Consumer capability seam + typed Event + reversible Effect；Agent Loop 自身也是 Plugin | Session generations、durable events、crash repair、retry / compaction evidence 支撑 Resume / Replay |
| [DeerFlow 2.0](deer-flow/README.md) | **LangGraph 执行基座 + Middleware Product Runtime + 双通道持久化** | Gateway → Run Worker → LeadAgentAssembly → create_agent() / LangGraph → Ordered Middleware → Model / Tool | LangGraph Checkpoint 保存 continuation state；Run Journal 保存 execution evidence；Gateway Run Row 保存产品生命周期 | ThreadState + Runtime Context + request-time Middleware projection 共同生成 ModelRequest | Ordered Middleware、Tool Assembly、MCP、Skills、可插拔 MemoryManager、Subagent Runtime 组合能力 | Checkpoint lineage、Run Journal、Replay / Rollback、Dangling Tool Call 修复与产品事件共同恢复和诊断 |

把它压成面试时最容易先说出的四句话：

~~~text
Codex
= 强类型执行内核，能力通过 Extension / Tool Runtime 接入。

Claude Code
= 以 query loop 为中心，不断优化 Model View、Prompt Cache 和渐进式能力暴露。

DeepSeek Harness
= Everything-is-a-plugin；Cordis 负责组合与生命周期，Session Log 与 Surface 把持久事实和模型视图分开。

DeerFlow
= LangGraph / LangChain 提供基础执行，DeerFlow 用有序 Middleware、Gateway 和 Checkpoint / Journal 把它做成产品级 Harness。
~~~

这四句话只能作为开场。真正的源码差异要继续落回本表的状态所有权、Context 构造、能力接入和恢复机制，而不能只比较“谁有 Memory / MCP / Subagent”。

## 5. 源码事实与工程解释

产品源码文档不是 API Reference（接口参考手册），也不是把源码字段逐项翻译成中文。文档先讲运行场景和因果关系，再出现必要源码对象。

英文概念第一次出现时给出中文含义；真实类型名、函数名和字段名保持源码命名，用反引号标识。一个源码对象只有在它真正影响生命周期时才展开字段。

文档中的结论分为三层：

1. **直接实现事实：** 能定位到固定 commit 的类型、函数、测试或配置。
2. **跨文件调用链结论：** 由多个源码入口共同确认的真实系统行为。
3. **工程解释：** 对实现为什么这样设计的教学解释，必须建立在前两类证据上。

Prompt 中出现但没有安装入口、调用方或测试支持的概念，不描述成“完整机制已经生效”。

## 6. 核验规则

- **生命周期完整。** 不按文件名罗列功能，而是追踪信息、状态和调用从产生到结束。
- **Runtime State、Context、Memory、History、Persistence 分开。** 即使都能落盘，也不混为一个概念。
- **Prompt 回到生产者。** 说明谁生成、何时注入、角色 / slot、预算、更新条件和失败边界。
- **Tool 追到结果回填。** 只有 Registry 或 Schema 不算完整 Tool Lifecycle。
- **Memory 追到写、读、纠正与评测。** 只有向量检索或聊天历史不算完整 Memory Lifecycle。
- **规模化看预算与按需加载。** 大 Context、大 Tool / Skill Catalog 必须解释如何控制模型可见信息。
- **Failure Path 与测试属于源码。** Retry、Cancel、Permission、Sandbox、Resume、Trace、Metrics、Tests 一并核验。
- **固定快照内闭环。** 不把不同 commit 的行为拼成一套不存在的系统。

## 7. 推荐学习方式

完成 [Agent Curriculum](../../curriculum/09-agent/README.md) 与 Review 后，选择一套产品连续阅读：

```text
产品 README 的系统总图
→ 01 Context
→ 02 Memory
→ 03 Tool
→ 04 Engineering & Evaluation
→ 回到 Agent Curriculum 重新解释设计空间
→ 再进入第二套产品做横向比较
```

真正需要掌握的不是源码文件名，而是：

> **输入怎样变成模型可见上下文，长期信息怎样变成记忆，可执行能力怎样安全地变成工具，以及整个系统怎样在失败、超大规模与长期运行下保持可恢复、可诊断、可验证。**
