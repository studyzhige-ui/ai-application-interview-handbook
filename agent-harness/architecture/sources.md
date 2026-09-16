# 资料依据、版本与维护规则

[架构总纲](README.md) · [概念归位表](concept-atlas.md) · [执行与状态](lifecycle-and-state.md) · [设计与自测](design-and-review.md)

> 最后核验：2026-09-16。只使用官方文档、官方工程文章和可定位源码作为外部技术依据。
>
> 发布日期表示文章首次标注的日期，不代表文中所有产品行为今天仍然相同。持续更新文档使用访问日期；源码使用固定提交，不使用 main 作为可重复证据。

## 怎样理解本组笔记的证据

**官方事实**包括 Codex 的 Thread / Turn / Item 定义，以及 MCP、Skills、A2A 的协议或能力定义。

**教材抽象**包括“任务契约 + 四层 + 两类横切要求”、概念归位方式、Task / Run 的示意定义、设计问卷、状态结构和通用可靠性建议。这些是为了学习与设计形成的参考模型，不应标成某家厂商的原文标准。

**产品实例**用于验证责任边界确实可以落地，不用于证明所有 Agent 都必须采用同一种实现、框架或部署方式。

本文的架构 L1–L4 表示四类软件职责，与研究库中用于表示面试追问或知识深度的同名标签不是一回事。

---

## S01

**OpenAI — Unrolling the Codex agent loop**  
发布：2026-01-23。  
原文：https://openai.com/index/unrolling-the-codex-agent-loop/

支持：模型推理、工具交互与 Agent Loop 的关系。不要从中推断任务契约、所有生产后端服务或所有模型内部实现都已被该文章覆盖。

## S02

**OpenAI — Unlocking the Codex harness: how we built the App Server**  
发布：2026-02-04。  
原文：https://openai.com/index/unlocking-the-codex-harness/

支持：多种客户端、共享核心、App Server、生命周期与双向交互的架构实例。文章中的阶段性迁移计划不能直接当作今天的已发布状态。

## S03

**OpenAI — Codex App Server documentation**  
持续更新；访问：2026-09-16。  
入口：https://developers.openai.com/codex/app-server/  
本次入口重定向：https://learn.chatgpt.com/docs/app-server

支持：Thread、Turn、Item 及工作过程的产品语义。具体字段、实验开关与支持范围应按所接入版本查证，不应把整个协议固定成教材通用标准。

## S04

**Anthropic — Scaling Managed Agents: Decoupling the brain from the hands**  
发布：2026-04-08。  
原文：https://www.anthropic.com/engineering/managed-agents

支持：会话记录、Harness 与执行环境解耦的架构实践。本文借鉴的是责任与生命周期边界，不照搬其托管产品部署。

## S05

**Anthropic — Effective context engineering for AI agents**  
发布：2025-09-29。  
原文：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

支持：上下文作为有限资源，需要随执行持续选择和管理。本文对执行状态、外部事实与记忆的进一步区分是工程综合，不是对该文的逐段重述。

## S06

**Anthropic — Writing effective tools for agents — with agents**  
发布：2025-09-11。  
原文：https://www.anthropic.com/engineering/writing-tools-for-agents

支持：围绕任务设计工具语义、参数、结果和评测，而不是无选择地暴露已有 API。

## S07

**Anthropic — Demystifying evals for AI agents**  
发布：2026-01-09。  
原文：https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

支持：区分执行轨迹与任务结果，按任务和环境设计评测，利用失败支持迭代。这里不引用任何产品成绩作为本仓库自己的成绩。

## S08

**Anthropic — Building effective agents**  
发布：2024-12-19；属于基础架构资料，不冒充最新产品指南。  
原文：https://www.anthropic.com/engineering/building-effective-agents

支持：预定义控制路径与模型动态选择路径的区分，以及按需要组合控制模式。工具生态和产品实现以更新文档为准。

## S09

**LangChain — LangGraph Persistence**  
持续更新；访问：2026-09-16。  
原文：https://docs.langchain.com/oss/python/langgraph/persistence

支持：线程状态、checkpoint 和跨线程存储的框架实例。不要把 LangGraph 的 thread、checkpoint 或步骤语义强行等同于 Codex 的同名对象。

## S10

**Model Context Protocol — Architecture overview**  
访问：2026-09-16；本次通用入口解析到 2026-07-28 版本文档。  
通用入口：https://modelcontextprotocol.io/docs/learn/architecture  
版本化入口：https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture

支持：Host / Client / Server、工具、资源与提示等接入边界；MCP 不规定宿主如何管理模型与上下文。不同版本的初始化、发现、传输和扩展语义可能不同，本组总纲不混用具体请求字段。

## S11

**Agent Skills — Official overview**  
持续更新；访问：2026-09-16。  
入口：https://agentskills.io/what-are-skills  
本次入口重定向：https://agentskills.io/home

支持：Skills 作为指令与资源的可加载能力包。安装技能、读取技能说明和获得实际动作授权是不同事件。

## S12

**A2A Protocol — Core Concepts**  
持续更新；访问：2026-09-16。  
原文：https://a2a-protocol.org/latest/topics/key-concepts/

支持：Agent 协作中的能力、消息、任务状态与产物等协议概念。接入协议不替宿主确定任务分工、权限或完成标准。

## S13

**OpenAI — Codex Security documentation**  
持续更新；访问：2026-09-16。  
入口：https://developers.openai.com/codex/security/  
本次入口重定向：https://learn.chatgpt.com/docs/security

支持：审批与执行限制的区分及其产品实例。实际默认权限和平台能力需按具体版本核对。

## S14

**Anthropic — Effective harnesses for long-running agents**  
发布：2025-11-26。  
原文：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

支持：长任务需要可承接的进度、环境和验证，仅有 compaction 不足以保证持续可靠推进。本文不移植其具体项目流程。

## S15

**Anthropic — How we built our multi-agent research system**  
发布：2025-06-13。  
原文：https://www.anthropic.com/engineering/multi-agent-research-system

支持：多 Agent 分工、上下文与协作成本的实例；不用于推出“多 Agent 总比单 Agent 好”。

## S16

**OpenAI Codex — 固定源码快照**  
参考提交：`5bf132cd527311eb61bbec46562e3890eb49df80`。  
本次核验：2026-09-16。该提交用于可追溯阅读，不宣称它是未来访问时的最新版本。

| 入口 | 本次用于核对什么 |
|---|---|
| [core/src/lib.rs](https://github.com/openai/codex/blob/5bf132cd527311eb61bbec46562e3890eb49df80/codex-rs/core/src/lib.rs) | Context、Session、Tools、MCP、Skills、历史与环境等模块边界 |
| [core/src/tools/orchestrator.rs](https://github.com/openai/codex/blob/5bf132cd527311eb61bbec46562e3890eb49df80/codex-rs/core/src/tools/orchestrator.rs) | 审批、沙箱选择与工具执行协调 |
| [core/README.md](https://github.com/openai/codex/blob/5bf132cd527311eb61bbec46562e3890eb49df80/codex-rs/core/README.md) | Core 的共享逻辑定位与环境依赖 |

源码路径用于理解具体实现，不用于给四层模型盖“官方认证”。文件存在也不代表所有功能默认开启。

---

## 本仓库中的位置与原有教材关系

本次审阅以仓库提交 `0266cbfa131ff4157cad9f4c18b75fe153c0b846` 为基线。Agent 模块已经有学习主线、分组、边界说明和生产架构章节，因此不能评价为“完全没有结构”。更准确的问题是：**从运行机制切入较多，缺少一个前置、贯穿全文的系统设计视图。**

本目录补这个视图，原有机制仍回到唯一的正式维护位置：

[Agent Harness](../README.md) · [RAG](../../rag/README.md) · [System Design](../../system-design/README.md) · [AI Backend Engineering](../../backend-engineering/README.md) · [术语表](../../roadmap/terminology-glossary.md)

不会因这组导航性笔记增加 HUMAN-A 来源、调整面试频率、重排题目 ID，或改变“23 个 Agent 正式知识块”的统计口径。

## GitHub 与 Notion 的记录决策

**当前建议：GitHub 作为架构正文的唯一主库。** 理由来自现有资料组织：本组笔记需要持续链接已有教材、核对源码快照和管理跨模块边界，把正文继续放在仓库内更容易保持同一来源。

Notion 可以作为个人使用层，记录阅读进度、自己的复述、错题、待解决问题和项目映射，并链接主库正文。这是工作流建议，不代表本次已经创建了 Notion 页面或配置了同步。

不要同时手工维护两份“最新版总纲”。将来需要镜像时，应明确单向来源、主库版本和同步时间，并把个人批注与镜像正文分开。

## 后续维护约定

新增术语先标注类型、主责、动机、边界和验证方式，再加入归位表；不要轻易增加新的架构层。

新增深度机制优先链接已有 Primary Module；只有出现真正的新知识闭环才新增正式章节。若改变正式课程数量或状态，再按[文档规范](../../roadmap/documentation-style-guide.md)同步相关入口与统计。

正文维持供应商无关的职责边界；模型名称、协议请求字段、默认权限和框架 API 留在对应版本化资料中。这样新产品发布不需要推翻整张知识地图。
