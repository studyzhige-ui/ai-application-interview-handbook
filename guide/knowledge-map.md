# AI Application Engineer｜十板块知识地图

[← Handbook 总目录](../README.md) · [成熟产品源码](../products/README.md) · [Coding & Problem Solving](../practice/coding/README.md) · [正式学习路线](learning-path.md) · [审计记录索引](audits/README.md) · [跨模块术语表](terminology-glossary.md) · [Canonical 冻结覆盖](../interview/canonical/progress.md) · [Canonical Index](../interview/canonical/module-index.md)

> 本页按当前正式文件描述十个模块，不以历史验收状态替代后续版本验证。这里强调**模块职责、知识依赖与边界**；章节细节进入各模块 README，实际每天怎样学习见 [Learning Path](learning-path.md)。

## 总路线

[Python Foundation](../curriculum/01-python/README.md) → [FastAPI](../curriculum/02-fastapi/README.md) → [MySQL](../curriculum/04-mysql/README.md) → [Redis](../curriculum/05-redis/README.md) → [AI Backend Engineering](../curriculum/03-backend-engineering/README.md) → [Vector Database](../curriculum/06-vector-db/README.md) → [LLM Foundation（应用工程深度）](../curriculum/07-llm-foundation/README.md) → [RAG](../curriculum/08-rag/README.md) → [Agent](../curriculum/09-agent/README.md) → [System Design](../curriculum/10-system-design/README.md)

### 成熟产品源码层（不计入十模块）

[Products](../products/README.md) 用固定源码快照回答“成熟系统怎样把多个通用机制组合起来”。它不改变十模块的 Primary Ownership，也不把某个产品实现提升成通用标准。

Agent 产品源码入口：[Codex](../products/agent/codex/README.md) · [Claude Code](../products/agent/claude-code/README.md) · [DeepSeek Harness](../products/agent/deepseek-harness/README.md) · [DeerFlow 2.0](../products/agent/deer-flow/README.md)。

```text
Curriculum 通用机制
→ Products 完整系统源码
→ Practice / System Design / Interview 中迁移与表达
```

### 横向实践轨道（不计入十模块）

[Coding & Problem Solving](../practice/coding/README.md) 与知识主线并行：

```text
01—03：读写与追踪 Python 程序 → 04：完整输入输出 → 05—06：数据结构与算法 → 07：Hot100 练习 → 08：笔试 → 09：多文件 AI Coding
```

它不改变十模块的 Primary Ownership / Canonical 统计，只负责把“知道”转成“能写、能跑、能调试、能交付”。Hot100 不是孤立终点，而是从基础阶段按依赖逐步嵌入；见 [Hot100 Curriculum Map](../practice/coding/hot100-map.md)。

## 总览

| 学习顺序 | 模块 | 正文章节 | Canonical | 核心角色 |
|---:|---|---:|---:|---|
| 01 | [Python Foundation](../curriculum/01-python/README.md) | 13 | 15 | 名字与对象、数据容器、函数、资源和并发执行。 |
| 02 | [FastAPI](../curriculum/02-fastapi/README.md) | 16 | 4 | 请求与响应、数据校验、资源生命周期、流式交付与接口验证。 |
| 03 | [MySQL](../curriculum/04-mysql/README.md) | 19 | 26 | 表与查询、索引、事务、并发、恢复与数据增长。 |
| 04 | [Redis](../curriculum/05-redis/README.md) | 18 | 19 | 数据操作、生命周期、缓存、原子修改、持久化与高可用。 |
| 05 | [AI Backend Engineering](../curriculum/03-backend-engineering/README.md) | 22 | 39 | 在接口、数据库和缓存之上组织可靠执行、幂等、任务恢复与跨系统协作。 |
| 06 | [Vector Database](../curriculum/06-vector-db/README.md) | 16 | 12 | 向量比较、精确与近似检索、索引、过滤、版本和维护。 |
| 07 | [LLM Foundation（应用工程深度）](../curriculum/07-llm-foundation/README.md) | 14 | 23 | 从 Token、模型计算与生成，理解推理成本、模型选择和训练干预。 |
| 08 | [RAG](../curriculum/08-rag/README.md) | 14 | 29 | 从语料和查询得到候选、证据、回答，再用评测与版本管理验证质量。 |
| 09 | [Agent](../curriculum/09-agent/README.md) | 24 | 44 | 从任务与执行角色建立工具、上下文、记忆、状态、安全、恢复与评测。 |
| 10 | [System Design](../curriculum/10-system-design/README.md) | 19 | 24 | 从需求、容量、状态和数据流推导方案，验证可靠性、成本与演进。 |

---

## 01. [Python Foundation](../curriculum/01-python/README.md) — 13 章
<a id="01-python-foundation---13-blocks"></a>

名字与对象、数据容器、函数、资源和并发执行。

```text
数据与对象 → 函数与执行 → 对象协作与输入边界 → 运行机制、并发与成本
```

市场校准：**15 Canonical / 15 independent HUMAN-A flows**。

## 02. [FastAPI](../curriculum/02-fastapi/README.md) — 16 章
<a id="02-fastapi---16-blocks"></a>

请求与响应、数据校验、资源生命周期、流式交付与接口验证。

```text
请求与数据契约 → 依赖、资源与执行 → 流式交付与访问控制 → 外部工作、取消与退出 → 测试、部署与综合实践
```

市场校准：**4 Canonical / 3 independent HUMAN-A flows**。

## 03. [MySQL](../curriculum/04-mysql/README.md) — 19 章
<a id="04-mysql--19-blocks"></a>

表与查询、索引、事务、并发、恢复与数据增长。

```text
表与 SQL → 关系、约束与统计 → 索引与执行计划 → 事务、MVCC、锁与恢复 → 分页、结构演进与批量写入 → 复制、CDC 与分片 → 应用数据建模与跨系统边界
```

市场校准：**26 Canonical / 55 independent HUMAN-A flows**。

## 04. [Redis](../curriculum/05-redis/README.md) — 18 章
<a id="05-redis---18-blocks"></a>

数据操作、生命周期、缓存、原子修改、持久化与高可用。

```text
数据与生命周期 → 缓存读取、更新与失效 → 执行成本与多步修改 → 持久化、复制与分片 → 消息、状态与故障判断
```

市场校准：**19 Canonical / 69 independent HUMAN-A flows**。

## 05. [AI Backend Engineering](../curriculum/03-backend-engineering/README.md) — 22 章
<a id="03-ai-backend-engineering---22-blocks"></a>

在接口、数据库和缓存之上组织可靠执行、幂等、任务恢复与跨系统协作。

```text
请求责任与持久状态 → 网络与流式交付 → 执行者、容量与等待预算 → 操作身份、幂等与重试 → 消息、可靠任务与一致性 → 安全、观测、部署与演进
```

市场校准：**39 Canonical / 125 independent HUMAN-A flows**。

## 06. [Vector Database](../curriculum/06-vector-db/README.md) — 16 章
<a id="06-vector-database---16-blocks"></a>

向量比较、精确与近似检索、索引、过滤、版本和维护。

```text
向量、距离与精确基线 → 图、倒排与压缩索引 → 索引选择 → 数据、过滤与版本 → 分布式执行、评测与维护
```

市场校准：**12 Canonical / 37 independent HUMAN-A flows**。

## 07. [LLM Foundation（应用工程深度）](../curriculum/07-llm-foundation/README.md) — 14 章
<a id="07-llm-foundation应用工程深度---14-blocks"></a>

从 Token、模型计算与生成，理解推理成本、模型选择和训练干预。

```text
Token 与上下文 → Transformer、注意力与位置 → 生成与解码 → KV 缓存与推理服务 → 模型接口、检索模型与多模态 → Prompt、事实性与训练干预
```

市场校准：**23 Canonical / 82 independent HUMAN-A flows**。

## 08. [RAG](../curriculum/08-rag/README.md) — 14 章
<a id="08-rag---14-blocks"></a>

从语料和查询得到候选、证据、回答，再用评测与版本管理验证质量。

```text
任务与语料 → 解析、清洗与切分 → 查询与检索 → 融合、重排与证据组装 → 回答、引用与评测 → 权限、版本和生产治理
```

市场校准：**29 Canonical / 88 independent HUMAN-A flows**。

## 09. [Agent](../curriculum/09-agent/README.md) — 24 章
<a id="09-agent---24-blocks"></a>

从任务与执行角色建立工具、上下文、记忆、状态、安全、恢复与评测。

```text
任务与执行角色 → 工具契约、发现与受控执行 → 计划、上下文与记忆 → 状态、持久化与恢复 → 安全、协议、扩展与协作 → 诊断、评测与工程落地
```

市场校准：**44 Canonical / 166 independent HUMAN-A flows**。

## 10. [System Design](../curriculum/10-system-design/README.md) — 19 章
<a id="10-system-design---19-blocks"></a>

从需求、容量、状态和数据流推导方案，验证可靠性、成本与演进。

```text
需求与容量 → API、状态和数据 → 缓存、分区与协作 → 一致性、队列、安全与可靠性 → 观测、评估和演进 → 综合系统方案
```

市场校准：**24 Canonical / 71 independent HUMAN-A flows**。

---

## 使用规则

- 学习顺序由知识依赖决定，不按面经频率重排；
- Products 是成熟系统源码学习层，不作为第 11 个知识模块制造新的 Canonical Ownership；
- Coding 是并行实践轨道，不作为第 11 个知识模块制造新的 Canonical Ownership；
- 真人面经只调整复习权重、真实问法和追问深度；
- 跨模块问题只在 Primary Module 维护完整机制；
- 章节数是认知闭环的结果，不是统一 KPI；
- 第一次完整学习使用 [Learning Path](learning-path.md) 的 Curriculum → Review → Interview 三遍法；
- 历史粒度与深度审查见 [Granularity Audit](audits/curriculum-granularity-audit.md) 与 [Content Depth Audit](audits/content-depth-audit.md)；
- v1.0 历史基线结论见 [Final Quality Audit](audits/history/final-quality-audit-2026-09-12.md)；跨模块同名概念统一以 [Terminology Glossary](terminology-glossary.md) 为工作定义。


Agent 模块使用 24 章正式学习顺序；历史重组、固定实现对照与核验范围见 [Agent Reader Revision](project/agent-reader-revision.md)。

<!-- learning-inventory:start -->
## 当前文件范围

10 个课程模块合计 **175 篇正文**。Products 为 **4 套 / 16 篇专题正文**，Coding 为 **9 篇正文**，均作为独立轨道，不加入课程章节合计。

完整入口见[学习资源索引](navigation-index.md)。Canonical 列和各模块来源覆盖保留冻结基线，不能相加推算独立面经总量。
<!-- learning-inventory:end -->
