# AI Application / Agent Engineer Interview Handbook

> 面向 **AI Application / AI Agent Engineer** 求职的一套 beginner-first 学习、实践、市场研究与面试训练系统。

> **当前状态：✅ 十个正式 Curriculum 模块 V1 完成** · **🟢 招聘市场持续监测** · **🟢 HUMAN-A 真人面经持续监测**

## 快速入口

[正式课程](curriculum/README.md) · [Coding / Git 实践](practice/README.md) · [学习路线](guide/learning-path.md) · [知识地图](guide/knowledge-map.md) · [岗位市场](market/README.md) · [Canonical Questions](interview/README.md) · [权威资料](references/README.md)

---

## 1. 这个仓库现在是什么

仓库不再把“教材、面经、岗位、官方资料、项目治理”平铺在同一级。当前信息架构按职责拆成七层：

```text
curriculum/   应该系统学什么
practice/     怎样把知识写成代码、落实到开发工作流
market/       市场正在招什么、真实面试正在问什么
interview/    如何把市场证据归一化成可训练的面试能力
references/   技术事实与 Production 边界依据什么
guide/        整个学习系统怎样导航、审计和维护
tools/        研究与质量分析怎样自动化
```

核心关系：

```text
完整知识体系 ───────────────→ Curriculum
      ↑                         │
      │                         ├─→ Practice
市场岗位 JD ─→ Market ─→ Interview Canonical
真人面经 ────→ Market ────────┘
      │
      └─ 校准“哪些内容更常被问、要学多深”

官方文档 / 规范 / 论文 / 成熟源码 ─→ References
      └─ 校准“技术事实与工程边界”
```

> **知识体系决定应该学什么；市场证据决定哪些地方要学深；权威资料决定技术事实是否可靠。**

---

## 2. Curriculum｜十个正式知识模块

| # | 模块 | 一句话职责 |
|---:|---|---|
| 01 | [Python Foundation](curriculum/01-python/README.md) | Python 语言、对象模型、结构化数据与并发 Runtime 基础 |
| 02 | [FastAPI](curriculum/02-fastapi/README.md) | 把 Python Runtime 组织成可校验、可 Streaming、可部署的 AI Service |
| 03 | [AI Backend Engineering](curriculum/03-backend-engineering/README.md) | 把模型、数据与 Agent Runtime 连接成可靠 Production Backend |
| 04 | [MySQL](curriculum/04-mysql/README.md) | 结构化事实、事务、索引、并发与规模增长 |
| 05 | [Redis](curriculum/05-redis/README.md) | Cache / Session / Rate Limit / Coordination 与内存生命周期 |
| 06 | [Vector Database](curriculum/06-vector-db/README.md) | Embedding、ANN、过滤、索引生命周期与分布式 Vector DB |
| 07 | [LLM Foundation](curriculum/07-llm-foundation/README.md) | Token、Transformer、Generation、KV Cache、Serving 与模型选择 |
| 08 | [RAG](curriculum/08-rag/README.md) | Knowledge → Retrieval → Evidence → Evaluation 的完整链路 |
| 09 | [Agent](curriculum/09-agent/README.md) | Loop、Tool、Context、Memory、State、Permission、Trace、Eval、Multi-Agent |
| 10 | [System Design](curriculum/10-system-design/README.md) | 把前九个模块组合为可容量估算、可恢复、可观测、可演进系统 |

正式顺序与 Module Exit Gate 见 [Learning Path](guide/learning-path.md)。

---

## 3. Practice｜横向实践轨道

Practice 不是第 11 个知识模块。

- [Coding & Problem Solving](practice/coding/README.md)：Programming Fundamentals → ACM → DSA → Hot100 → OA → AI Coding。
- [Git + GitHub Desktop](practice/tooling/git-github-desktop-guide.md)：Pull → 开发 → Diff → Commit → Push → Branch / Conflict / .gitignore 的完整初学者工作流。

它回答的是：

> **“知识我懂了，但我能不能真正写、改、提交、调试和协作？”**

---

## 4. Market｜招聘市场证据层

[Market 首页](market/README.md) 现在包含两种互补证据：

- [非算法 AI Application / Agent 岗位 JD](market/jobs/ai-agent-jd-market.md)：回答“公司正在招什么、要求什么”。
- [HUMAN-A 真人面经](market/interviews/)：回答“真实面试官最近在问什么、追到多深”。

市场分析、持续监控与来源质量规则也全部归在 `market/`，不再和技术权威资料混在同一个 `research/` 目录。

---

## 5. Interview｜归一化面试能力层

[Canonical Questions](interview/canonical/README.md) 将大量独立真人面经归一化成稳定能力单元。

```text
Market 原始证据
→ 去重 / Provenance / Role Scope
→ Canonical Question
→ Ownership / Heat / Depth
→ 回到 Curriculum 校准复习深度
```

各 Curriculum 模块自己的 `interview/` 目录仍负责“该模块怎么复习和口述”；中央 `interview/canonical/` 负责市场证据归一化，两者职责不同。

---

## 6. References｜技术事实证据层

[References 首页](references/README.md) 用于存放官方文档、规范、论文与成熟源码索引。

当前包括：

- [Agent Runtime / Harness 证据](references/agent/README.md)
- [FastAPI 官方资料](references/fastapi/README.md)
- [AI Backend Engineering 权威资料](references/backend-engineering/README.md)

**References 不创造面试频率，不增加 HUMAN-A Source Count。**

---

## 7. Guide｜导航、规范与质量治理

[Guide 首页](guide/README.md) 包含：

- [Knowledge Map](guide/knowledge-map.md)
- [Learning Path](guide/learning-path.md)
- [Terminology Glossary](guide/terminology-glossary.md)
- [Documentation Style Guide](guide/documentation-style-guide.md)
- [Quality Audits](guide/audits/README.md)
- [Project / Migration Records](guide/project/README.md)

---

## 8. 当前目录

```text
.
├── curriculum/           # 十个正式知识模块
├── practice/             # Coding + Git / 工程实践
├── market/               # JD + HUMAN-A + 市场分析/监控/政策
├── interview/            # Canonical 面试能力归一化
├── references/           # 官方资料 / 规范 / 成熟源码证据
├── guide/                # Knowledge Map / Learning Path / Audits / Governance
├── tools/                # 研究、统计、验证脚本
├── .github/              # GitHub Actions
└── README.md
```

这套目录结构本身就是知识模型：**课程、实践、市场、面试、证据、导航、工具彼此分层，不再互相充当“杂物间”。**
