# AI Application / Agent Engineer Interview Handbook

面向 **AI 应用开发与 Agent 工程师**的学习、产品研读、开发实践与面试准备手册。

从零建立最小完整的工程知识模型，再用真实问题决定学习深度。目标是既能解释系统怎样运行，也能独立实现、定位故障，并说清设计取舍。

## 🧭 从哪里开始

| 你的目标 | 入口 | 这里提供什么 |
| --- | --- | --- |
| 系统学习工程基础与 AI 应用技术 | [通用课程](curriculum/README.md) | 十个知识域的连贯正文、阅读顺序与压缩复习 |
| 看懂成熟产品如何组织完整系统 | [优秀产品学习](products/README.md) | Codex、Claude Code、DeepSeek Harness、DeerFlow 的固定源码快照研读 |
| 把理解变成可运行、可提交的成果 | [编程训练与开发实践](practice/README.md) | 编程练习、算法与 AI Coding，以及 Git 等开发工具教程 |
| 准备口述、追问与临场复习 | [面试准备](interview/README.md) | 按知识域整理的实质回答、易混易错点与速查材料 |
| 了解岗位要求与真实考察重点 | [市场材料与分析](market/README.md) | 官方岗位描述、一手面试记录及可回查的分析 |

核心关系：

```text
完整知识体系 ──→ 通用课程 ──→ 产品研读 / 编程与开发实践

官方岗位 JD + 真人面经 ──→ 市场材料与分析 ──→ 面试资料
```

产品研读与实践可和课程并行；市场分析用于校准学习重点与深度。

## 📚 三条学习主线

### 1. 通用课程：建立可以迁移的知识模型

按前置关系依次学习。已有基础时，可直接进入对应模块，再补齐不熟悉的前置知识。

| 顺序 | 课程入口 | 重点理解什么 |
| ---: | --- | --- |
| 01 | [Python](curriculum/01-python/README.md) | 名字与对象、容器、函数、资源管理和并发执行 |
| 02 | [FastAPI](curriculum/02-fastapi/README.md) | 请求与响应、数据校验、依赖、资源生命周期与流式接口 |
| 03 | [MySQL](curriculum/03-mysql/README.md) | 关系表与查询、索引、事务、锁、恢复和数据增长 |
| 04 | [Redis](curriculum/04-redis/README.md) | 数据结构、缓存、过期、原子操作、持久化与高可用 |
| 05 | [后端工程](curriculum/05-backend-engineering/README.md) | 网络与并发、可靠任务、幂等、容量控制和跨系统恢复 |
| 06 | [大模型基础](curriculum/06-llm-foundation/README.md) | Token、注意力、生成、训练与推理、模型适配和成本 |
| 07 | [向量数据库](curriculum/07-vector-db/README.md) | 向量与相似度、精确与近似检索、索引、过滤和数据维护 |
| 08 | [RAG](curriculum/08-rag/README.md) | 文档处理、检索、证据组织、回答生成、评测与更新 |
| 09 | [Agent](curriculum/09-agent/README.md) | 模型判断、工具执行、上下文与记忆、授权、恢复和验收 |
| 10 | [系统设计](curriculum/10-system-design/README.md) | 从业务需求推导容量、状态责任、协作方式与故障方案 |

每个模块都按 **README → docs → review** 使用：先看目标与顺序，再读连贯正文，最后用压缩复习检查自己能否解释机制、边界与取舍。[课程总览](curriculum/README.md)说明模块之间的前置关系。

### 2. 优秀产品学习：沿一次真实任务读懂系统

在课程模型的基础上，看多个机制怎样组成产品：输入如何变成模型上下文，工具怎样执行，状态怎样保存，失败后怎样恢复，以及凭什么判定任务完成。

| 产品 | 阅读重点 |
| --- | --- |
| [OpenAI Codex](products/codex/README.md) | 用户请求、模型调用与工具回填如何形成运行循环；上下文、许可与执行边界 |
| [Claude Code](products/claude-code/README.md) | 代码任务中的上下文、记忆、工具与工程验证 |
| [DeepSeek Harness](products/deepseek-harness/README.md) | 插件、Agent、Session 与工具如何装配并协作 |
| [DeerFlow 2.0](products/deer-flow/README.md) | Gateway、任务执行、中间件与子任务如何组织完整工作流 |

从各产品 README 进入整体概览与阅读顺序；固定源码版本和访问条件见[产品总览](products/README.md)。Claude Code 使用需要相应权限的私有学习镜像。

### 3. 编程训练与开发实践：通过实现和调试验证理解

实践可以与课程并行，不必等十个模块全部读完。

| 实践入口 | 训练路径 |
| --- | --- |
| [Coding：编程与问题求解](practice/coding/README.md) | 程序执行与 Python 数据操作 → 完整输入输出 → 数据结构与算法 → Hot100、在线笔试与 AI Coding |
| [Software：软件与开发工作流](practice/software/README.md) | 跟随编号教程练习开发工具；从 [Git 与 GitHub Desktop](practice/software/01-GitHub.md)入手，完成同步、查看差异、提交、分支、PR 与冲突处理 |

## 💬 面试准备：把理解组织成回答

[面试资料总览](interview/README.md)按十个知识域提供三类材料：

- **高频面试题**：有实质内容的建议回答，帮助解释机制与应对追问。
- **易混易错点**：辨析相近概念，检查结论成立的条件。
- **面试速查**：面试前快速回忆主线与关键边界。

| 工程基础 | AI 应用技术 |
| --- | --- |
| [Python](interview/python/README.md) | [大模型基础](interview/llm-foundation/README.md) |
| [FastAPI](interview/fastapi/README.md) | [向量数据库](interview/vector-db/README.md) |
| [MySQL](interview/mysql/README.md) | [RAG](interview/rag/README.md) |
| [Redis](interview/redis/README.md) | [Agent](interview/agent/README.md) |
| [后端工程](interview/backend-engineering/README.md) | [系统设计](interview/system-design/README.md) |

先尝试口述，再对照回答；遇到无法解释的机制，回到课程正文。真实问法、教学归纳与必要的基础补足在材料中分别说明，具体考察重点可回查[面经分析](market/interview-experience/02-analysis/README.md)。

## 🔎 市场材料：了解招什么、问什么

| 入口 | 主要用途 |
| --- | --- |
| [岗位描述](market/job-description/README.md) | 阅读官方岗位要求与职责，核对公司、岗位和来源材料 |
| [面试经历](market/interview-experience/README.md) | 回读真实题序与追问，了解考察重点、深度及分析依据 |

课程按知识依赖组织学习，市场材料帮助校准重点和深度，面试资料把理解整理成可练习的回答。

## 🗂️ 目录与维护

```text
curriculum/   通用课程：学习入口、连贯正文、压缩复习
products/     优秀产品：整体概览与固定源码研读
practice/     编程训练与软件使用教程
interview/    按知识域组织的回答、辨析与速查
market/       岗位与面试原始材料、分析及采集管理
tools/        跨仓库维护检查
.github/      工作流配置
```

内容编写遵循[写作规范](WRITING.md)；目录、导航与链接检查见[维护工具](tools/README.md)。
