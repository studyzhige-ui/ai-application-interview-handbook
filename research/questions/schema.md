# Canonical Question 数据规范

更新日期：2026-09-10

本目录把 `research/interviews/batch-01.md` ～ `batch-26.md` 中冻结的 `S001–S279` HUMAN-A 来源，归一化为可统计、可回溯、可反哺课程设计的 Canonical Question 数据集。

> 完整知识体系决定“应该学什么”；Canonical Question 只负责记录真实市场“怎么问、问多深、在哪些场景追问”。

---

## 1. 唯一正式一级板块

Canonical Question 的一级分类必须严格使用下面这套学习路径，不再沿用旧的“先做五大核心模块、再补支持模块”划分：

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent
  ↓
System Design
```

对应文件：

| 一级板块 | 文件 | QID Prefix |
|---|---|---|
| Python | `python.md` | `PY-` |
| FastAPI | `fastapi.md` | `FASTAPI-` |
| AI Backend Engineering | `ai-backend-engineering.md` | `AIBE-` |
| MySQL | `mysql.md` | `MYSQL-` |
| Redis | `redis.md` | `REDIS-` |
| Vector DB | `vector-db.md` | `VDB-` |
| LLM Foundation（应用工程深度） | `llm-foundation.md` | `LLM-` |
| RAG | `rag.md` | `RAG-` |
| Agent | `agent-harness.md` | `AGENT-` |
| System Design | `system-design.md` | `SD-` |

`Coding / Debug / AI Coding` 不再作为一级板块，而是 `Question Type`。例如：

- Python 装饰器现场编码 → `Python`；
- FastAPI 异步接口 Debug → `FastAPI`；
- MQ / ThreadPool / Network 故障排查 → `AI Backend Engineering`；
- Agent 现场 AI Coding / Repo 修改 → `Agent`；
- 端到端架构设计 → `System Design`。

---

## 2. 为什么仍然按模块做“全库纵向扫描”

采集阶段已经结束，因此不再按 Batch 增量生成 `canonical-batch-xx.md`。现在改为：

```text
S001–S279 全历史
      ↓
按十个正式一级板块分别纵向扫描全部来源
      ↓
原子化真实问题
      ↓
语义聚类 / Merge-Split 审计
      ↓
Primary Module 归属审计
      ↓
跨模块 Related Modules 关联
      ↓
全局频率 / 深度 / 课程覆盖分析
```

第一阶段只有在 **十个一级板块都完成全库纵向扫描，并完成 Primary Module 归属复核** 后才算完成。

---

## 3. Canonical Question 的字段

每道正式问题至少维护：

| 字段 | 含义 |
|---|---|
| `QID` | 一级板块内稳定编号，如 `MYSQL-003` |
| `Canonical Question` | 归一化后的核心问题 |
| `Primary Module` | 十个正式一级板块之一；每题只能有一个 |
| `Related Modules` | 可选；跨模块关联，不重复创建同一道题 |
| `Topic` | 二级知识点 |
| `Question Type` | Concept / Why / Comparison / Project / Troubleshoot / System Design / Coding / Debug / Trade-off / AI Coding |
| `Language / Ecosystem` | 可选；Python / Java / Go / Language-agnostic / Framework-specific 等 |
| `Evidence Sources` | 支撑该问题的独立 HUMAN-A `Sxxx` |
| `Source Count` | `Evidence Sources` 去重后的数量 |
| `Real Wording Variants` | 来自真实面试的典型问法变体，保留语境但不机械复制 |
| `Depth` | L1 概念、L2 原理、L3 工程场景、L4 Production / Failure / System Design |
| `Curriculum Link` | 后续教材对应章节；课程未建立时可暂缺 |

最终分析阶段还会从 Source Metadata 派生：独立公司数、岗位 / 轮次分布、时间分布、高频追问链和模块交叉关系。

---

## 4. 一级板块边界

### Python

Python 语言本身：对象 / 类型、容器、函数参数、迭代器 / 生成器、装饰器、Context Manager、GIL、`threading` / `multiprocessing` / `asyncio` 等。通用 OS 并发概念不因为 Python 能实现就放进 Python。

### FastAPI

FastAPI / ASGI 应用框架层：Request Lifecycle、Uvicorn / ASGI、Middleware、Dependency、Async Endpoint、Streaming / SSE 在 FastAPI 中的实现、参数校验与 API 层工程实践。协议本身的原理归 AI Backend Engineering。

### AI Backend Engineering

AI 应用服务端的通用工程底座：HTTP / HTTPS / TCP / RPC、SSE / WebSocket、异步与并发、ThreadPool / Event Loop、MQ、Backpressure、Rate Limit、Retry / Circuit Breaker / Degrade、Idempotency、Auth、Session、Linux / Docker / K8s、Observability、Microservice / DDD / Service Discovery、Java / Go 等后端生态信号。

MySQL / Redis 的内部机制分别归独立模块；跨存储的一致性场景可以把 Primary Module 放在 AI Backend Engineering，并用 Related Modules 指向 MySQL / Redis。

### MySQL

SQL 执行、索引、B+Tree、事务、MVCC、锁、日志、复制、Sharding 等 MySQL / InnoDB 核心机制。

### Redis

数据结构、过期 / 淘汰、持久化、主从 / Sentinel / Cluster、HotKey / BigKey、Distributed Lock、Redis Lua、Session / Cache 等 Redis 核心机制。

### Vector DB

向量存储与 ANN 检索基础设施：Embedding Vector 的存储语义、Similarity、HNSW / IVF、FAISS / Milvus / pgvector / ES Vector 等 Index / Storage / Filter / Scale 问题。RAG Pipeline 的 Retrieval Strategy 归 RAG。

### LLM Foundation（应用工程深度）

只保留应用工程需要掌握的模型基础：Tokenization、Transformer / Attention / QKV / FFN / RoPE、KV Cache、Prefill / Decode、PagedAttention / vLLM / SGLang、Model API 参数、Model Selection、Context Window / Lost in the Middle、Embedding / Rerank Model 原理、SFT / LoRA / DPO / GRPO / Distillation 等。

### RAG

从 Ingestion / Parsing / Chunking 到 Retrieval / Fusion / Rerank / Evaluation / Freshness / Permission / Bad-case Attribution 的完整 Retrieval-Augmented Generation 工程链路。Vector DB 只负责底层向量基础设施，不把完整 RAG 检索策略重复放入 Vector DB。

### Agent

Agent Loop、Planning、Context Assembly / Compaction、Memory、Tool / Function Calling、MCP、Skill、Checkpoint / Resume / Cancel、Retry / Fallback、Permission / Sandbox、Multi-Agent、Trace / Observability、Agent Evaluation / Benchmark、Coding Agent / AI Coding Runtime 等。

### System Design

端到端场景题：跨多个基础模块完成容量、可靠性、一致性、状态、成本、安全和演进设计。System Design 文件保留“完整场景”，底层单点原理仍只在对应 Primary Module 维护。

---

## 5. Primary Module / Related Modules 规则

同一道核心能力只建立一个 Canonical Question。

例如：

```text
“Redis + MySQL 双写一致性”
```

不再在 `mysql.md` 与 `redis.md` 各维护一份完全相同的问题。应选择一个 Primary Module（通常为 `AI Backend Engineering` 的 Data Consistency / Cache Architecture），再标：

```text
Related Modules: MySQL, Redis
```

又例如：

```text
“Vector + BM25 → RRF → Rerank”
```

如果问的是 RAG Retrieval Pipeline，Primary Module = `RAG`；如果问的是 HNSW / IVF / 向量索引本身，Primary Module = `Vector DB`。

`System Design` 同理：端到端设计作为独立 Scenario；不要复制所有底层 MySQL / Redis / MQ 问题来虚增全局题数。

---

## 6. Merge / Split 规则

只有当两个真实问法共享同一个核心知识模型，且主要差异只是措辞 / 场景包装时才合并。

以下情况必须拆分：

- 一个问“是什么”，另一个问“失败时怎么办”；
- 一个问算法原理，另一个问参数 / Trade-off；
- 一个问单机，另一个问分布式；
- 一个问实现，另一个问 Evaluation；
- 一个问正常路径，另一个问 Crash / Retry / Idempotency；
- 一个问题本身就包含面试官连续追到的独立能力点。

例如：

```text
MySQL MVCC 是什么？
≠
RR 下幻读如何治理？
≠
两个并发事务逐条 SELECT / UPDATE 时会发生什么？
```

---

## 7. 频率规则

`Source Count` 只按独立 HUMAN-A 来源计数。

同一 `Sxxx` 中同一主题连续追问多次，仍只为该 Canonical Question 贡献 `1` 个来源；同一候选人同一公司同一招聘流程多轮已在采集层合并；不同候选人的独立流程分别计数。

```text
频率 = 独立真实面试流程中出现过该核心能力的次数
```

不是关键词出现次数。

---

## 8. Depth 定义

| Level | 含义 | 例子 |
|---|---|---|
| L1 | 定义 / 基础概念 | “MVCC 是什么？” |
| L2 | 原理 / 为什么 | “ReadView 如何判断可见性？” |
| L3 | 工程场景 / Troubleshooting | “Slow SQL 怎样定位？” |
| L4 | Production / Failure / System Design | “外部副作用成功但 Checkpoint 写失败，Resume 怎样避免重复执行？” |

一个 Canonical Question 可以覆盖多个 Level，最终以真实来源中出现过的最高稳定深度标记。

---

## 9. 面试热度与课程重要度严格分离

面试频率不能决定课程边界。后续教材同时维护：

```text
Knowledge Importance
Core / Important / Advanced

Interview Heat
🔥🔥🔥 / 🔥🔥 / 🔥 / 单点信号
```

建议热度：

- `>= 10` 个独立 HUMAN-A：🔥🔥🔥
- `4–9`：🔥🔥
- `2–3`：🔥
- `1`：单点真实信号，不因为频率低而自动删除

基础知识即使面经频率较低，只要它是完整知识体系的必要前置，仍进入教材。

---

## 10. 证据边界

Canonical Question 只能由正式 `S001–S279` HUMAN-A 产生证据。搜索摘要、转载 / 二次整理、标准答案 / 题库、付费内容包装、自动 AI 面试、Role Scope 外场次和已删除的重复来源都不能贡献 Source Count。

Canonical Question 可以被教材进一步扩展，但扩展内容必须明确属于“知识体系补全”，不能伪装成“2026 真实面试高频”。
