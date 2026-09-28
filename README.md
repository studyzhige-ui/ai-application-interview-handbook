# AI Application / Agent Engineer Interview Handbook

> 面向 **AI Application / AI Agent Engineer** 求职的一套 beginner-first 学习、成熟系统源码研读、工程实践、市场研究与面试训练系统。

> **课程：10 个模块 / 175 篇正文** · **Products：4 套固定源码快照学习模块** · **市场：JD + HUMAN-A 证据** · **面试能力：235 ACTIVE Canonical（冻结统计基线见 Interview）**

## 快速入口

[正式课程](curriculum/README.md) · [成熟产品源码](products/README.md) · [Coding / Git 实践](practice/README.md) · [学习路线](guide/learning-path.md) · [知识地图](guide/knowledge-map.md) · [岗位市场](market/README.md) · [Canonical Questions](interview/README.md) · [权威资料](references/README.md)

---

## 1. 仓库定位与信息架构

本仓库按职责组织为八个层级。每一层只承担一种主要职责，课程、成熟系统源码学习、实践、市场证据、面试能力、技术证据、导航治理和自动化工具彼此分离：

```text
curriculum/   应该系统学什么
products/     成熟 AI 系统怎样把这些机制组合成真实产品
practice/     怎样把知识写成代码、落实到开发工作流
market/       市场招什么、真实面试问什么
interview/    如何把市场证据归一化成可训练的面试能力
references/   技术事实、版本与 Production 边界依据什么
guide/        整个学习系统怎样导航、审计和维护
tools/        研究与质量分析怎样自动化
```

核心关系：

```text
完整知识体系 ───────────────→ Curriculum ───────┐
                                                ├─→ Products ─→ Practice / System Design / Interview
官方文档 / 规范 / 论文 / 固定源码 ─→ References ─┘

岗位 JD ─────┐
             ├─→ Market ─→ Interview Canonical ─→ 校准 Curriculum 的复习权重与深度
真人面经 ────┘
```

> **Curriculum 建立可迁移的知识模型；Products 解剖完整成熟系统；References 约束技术事实与版本边界；Practice 把理解转化为可实现、可调试、可交付的能力。**

---

## 2. Curriculum｜十个正式知识模块

| 学习顺序 | 模块 | 一句话职责 |
|---:|---|---|
| 01 | [Python Foundation](curriculum/01-python/README.md) | 名字与对象、数据容器、函数、资源和并发执行。 |
| 02 | [FastAPI](curriculum/02-fastapi/README.md) | 请求与响应、数据校验、资源生命周期、流式交付与接口验证。 |
| 03 | [MySQL](curriculum/04-mysql/README.md) | 表与查询、索引、事务、并发、恢复与数据增长。 |
| 04 | [Redis](curriculum/05-redis/README.md) | 数据操作、生命周期、缓存、原子修改、持久化与高可用。 |
| 05 | [AI Backend Engineering](curriculum/03-backend-engineering/README.md) | 在接口、数据库和缓存之上组织可靠执行、幂等、任务恢复与跨系统协作。 |
| 06 | [Vector Database](curriculum/06-vector-db/README.md) | 向量比较、精确与近似检索、索引、过滤、版本和维护。 |
| 07 | [LLM Foundation](curriculum/07-llm-foundation/README.md) | 从 Token、模型计算与生成，理解推理成本、模型选择和训练干预。 |
| 08 | [RAG](curriculum/08-rag/README.md) | 从语料和查询得到候选、证据、回答，再用评测与版本管理验证质量。 |
| 09 | [Agent](curriculum/09-agent/README.md) | 沿模型判断、程序行动、结果回填与任务验收，建立工具、上下文、记忆、安全和恢复。 |
| 10 | [System Design](curriculum/10-system-design/README.md) | 从用户动作与完成条件推导容量、状态责任和协作方案，在故障与条件变化中验证取舍。 |

目录编号是稳定路径标识；表格按推荐学习顺序排列。正式顺序与 Module Exit Gate 见 [Learning Path](guide/learning-path.md)。

---

## 3. Products｜成熟系统源码学习层

[Products 首页](products/README.md)沿固定源码快照学习完整成熟系统，关注多个通用机制在真实产品中的组合方式、运行边界、Failure Path、恢复、诊断与工程取舍。

Agent 产品源码学习入口：[Agent Products](products/agent/README.md)。

- [OpenAI Codex](products/agent/codex/README.md)
- [Claude Code](products/agent/claude-code/README.md)
- [DeepSeek Harness](products/agent/deepseek-harness/README.md)
- [DeerFlow 2.0](products/agent/deer-flow/README.md)

Products 不承担通用概念的 Primary Ownership，也不作为源码证据仓库。通用机制回到 Curriculum；固定版本、官方规范和源码证据回到 References。

---

## 4. Practice｜横向实践轨道

Practice 与十个正式 Curriculum 模块并行，作为横向实践轨道，不计入 Curriculum 编号。

- [Coding & Problem Solving](practice/coding/README.md)：程序读写与追踪 → 完整输入输出 → 数据结构与算法 → Hot100 → 笔试 → 多文件 AI Coding。
- [Git + GitHub Desktop](practice/tooling/git-github-desktop-guide.md)：Pull → 开发 → Diff → Commit → Push → Branch / Conflict / .gitignore 的完整初学者工作流。

它回答的是：

> **“知识我懂了，但我能不能真正写、改、提交、调试和协作？”**

---

## 5. Market｜招聘市场证据层

[Market 首页](market/README.md)维护两类互补证据：

- [官方非算法 AI Application / Agent 岗位 JD](market/jobs/ai-agent-jd-market.md)：回答“公司招什么、要求什么”。
- [HUMAN-A 真人面经](market/interviews/)：回答“真实面试官问什么、追到多深”。

市场分析、持续监控与来源质量规则统一维护在 `market/`。

---

## 6. Interview｜归一化面试能力层

[Canonical Questions](interview/canonical/README.md) 将大量独立真人面经归一化成稳定能力单元。

```text
Market 原始证据
→ 去重 / Provenance / Role Scope
→ Canonical Question
→ Ownership / Heat / Depth
→ 回到 Curriculum 校准复习深度
```

各 Curriculum 模块自己的 `interview/` 目录负责“该模块怎么复习和口述”；中央 `interview/canonical/` 负责市场证据归一化，两者职责不同。

---

## 7. References｜技术事实证据层

[References 首页](references/README.md)收录官方文档、规范、论文、固定源码快照与源码索引，包括：

- [Agent Runtime / Harness 证据](references/agent/README.md)
- [FastAPI 官方资料](references/fastapi/README.md)
- [AI Backend Engineering 权威资料](references/backend-engineering/README.md)
- [MySQL 官方资料](references/mysql/README.md)与[Redis 官方资料](references/redis/README.md)
- [向量数据库](references/vector-db/README.md)、[LLM](references/llm-foundation/README.md)与[RAG](references/rag/README.md)资料

**References 不创造面试频率，不增加 HUMAN-A Source Count，也不替代 Products 的完整系统源码学习。**

---

## 8. Guide｜导航、规范与质量治理

[Guide 首页](guide/README.md)提供：

- [Knowledge Map](guide/knowledge-map.md)
- [Learning Path](guide/learning-path.md)
- [Terminology Glossary](guide/terminology-glossary.md)
- [Documentation Style Guide](guide/documentation-style-guide.md)
- [Quality Audits](guide/audits/README.md)
- [Project Records](guide/project/README.md)

---

## 9. 目录结构

```text
.
├── curriculum/           # 十个正式知识模块
├── products/             # 成熟 AI 产品源码学习
├── practice/             # Coding + Git / 工程实践
├── market/               # JD + HUMAN-A + 市场分析/监控/政策
├── interview/            # Canonical 面试能力归一化
├── references/           # 官方资料 / 规范 / 固定源码证据
├── guide/                # Knowledge Map / Learning Path / Audits / Governance
├── tools/                # 研究、统计、验证脚本
├── .github/              # GitHub Actions
└── README.md
```

目录结构本身体现知识模型：**Curriculum 负责通用知识主干，Products 负责成熟系统理解，Practice 负责能力落地，Market 负责招聘证据，Interview 负责能力归一化，References 负责技术事实，Guide 负责导航与治理，Tools 负责自动化。**

<!-- learning-inventory:start -->
## 内容范围与验证边界

课程正文数量由实际文件计算；Products 和 Coding 不计入这 175 篇。完整入口与数量见[学习资源索引](guide/navigation-index.md)。

课程完成状态、源码阅读、数值实验、真实服务验证与生产验证分别以对应模块的记录为准；冻结面经统计不因文档重排而重算。
<!-- learning-inventory:end -->
