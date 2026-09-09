# AI Application Interview Handbook

> 面向 **AI 应用开发 / AI Agent 开发** 求职的一套系统化知识体系、工程手册与真人面经验收系统。

这不是一本“AI 八股题库”。目标是从 0 建立完整能力链：

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
Agent Harness / Runtime
  ↓
System Design
```

同时持续用 2026 真人高质量面经检查：

> **我们学会的知识，能不能真的回答面试官？**

---

## 核心原则

### 1. 知识体系是骨架，高质量真人面经是血肉

Python、FastAPI、AI Backend、MySQL、Redis、Vector DB、LLM Foundation、RAG、Agent Harness 等模块都会从 0 建立自己的完整知识体系。

知识体系决定：**应该学什么。**

真人面经负责：

- 校准复习优先级；
- 保留真人面试官的真实问法；
- 判断问题通常追到什么深度；
- 验证是否真的能口述、设计和 Coding。

低质量帖子、题库、合集或二次创作不会为了“补知识点”增加额外学习任务。

### 2. 从 Demo 能力走到 Production 能力

我们不只学习“怎么调用 LLM / LangGraph / Milvus API”，还要回答：

> 超时怎么办？重复执行怎么办？Context 满了怎么办？Redis 挂了怎么办？RAG 召回不准怎么定位？Agent 如何取消和恢复？Tool 为什么不能让模型自己判断权限？

### 3. Agent Harness 以成熟产品源码为最高实现参考

Agent Harness / Runtime 的首要权威实现参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

目标不是复制框架 API，而是抽取 Agent Loop、Context、Memory、Tool Runtime、MCP / Skill、Permission / Sandbox、Checkpoint、Resume、Cancellation、Multi-Agent、Trace、Evaluation、Cost 与 Reliability 等稳定工程能力。

### 4. 正式面经只认 HUMAN-A

平台可以来自牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、个人博客或其他公开来源，但所有平台执行完全相同的准入标准：

```text
真人面试官
   +
候选人本人第一人称复盘
   +
高信息密度与真实现场痕迹
   +
AI Application / Agent 目标岗位
   +
正文可稳定核验
   +
非转载 / 非合集 / 非同场重复
   ↓
HUMAN-A
```

不满足任一条件的内容不进入正式研究，也不贡献面试题、频率或课程优先级。

详细规则：[`research/quality/source-quality-policy.md`](research/quality/source-quality-policy.md)

---

# 总知识地图

完整地图：[`roadmap/knowledge-map.md`](roadmap/knowledge-map.md)

## Foundation

### [Python Foundation](python/README.md) ✅

已经迁入主仓库：12 章系统正文、12 章 Mermaid 图解 + 折叠自测、55 道高频题、25 组 Coding 小题、易错点与速查表。

Python 不只是语法基础，还承担 GIL、asyncio、线程 / 进程 / 协程、生成器、上下文管理等 AI Backend Runtime 基础。

### [FastAPI｜AI 应用服务层](fastapi/README.md) 🟡

```text
HTTP / ASGI / Uvicorn
→ Routing
→ Pydantic / Schema
→ Dependency Injection
→ Lifespan
→ def vs async def
→ Event Loop
→ StreamingResponse / SSE / WebSocket
→ Auth
→ DB / Redis / LLM Client
→ Timeout / Cancellation
→ Testing / Trace / Deployment
→ RAG / Agent API Design
```

FastAPI 是从“会 Python”走到“能做真实 AI Service”的独立一环。

### [AI Backend Engineering](backend-engineering/README.md) 🟡

```text
Concurrency
→ Connection Pool
→ Timeout / Retry
→ Circuit Breaker
→ Cancellation
→ Idempotency
→ Lock / Lease
→ MQ / Reliable Task
→ Backpressure
→ Cache / Rate Limit
→ Observability
→ Security
→ Deployment / Scaling
```

---

## Data

### MySQL ⏳

SQL、B+Tree、索引、EXPLAIN、事务、MVCC、锁、redo / undo / binlog、Crash Recovery、Schema Design、MySQL + Redis 一致性，以及 AI 应用数据建模。

### Redis ⏳

数据结构、线程 / I/O 模型、TTL、淘汰、RDB / AOF、BigKey / HotKey、缓存问题、分布式锁、Lua、Cluster、Session、Agent State、限流。

### Vector Database ⏳

Embedding → Distance → TopK → ANN → HNSW / IVF → Metadata Filter → Dense / Sparse → Hybrid Search → RRF → Rerank → Index Lifecycle → 产品选型。

---

## AI Application

### LLM Foundation（应用工程深度） 🔎

目标是理解模型行为和应用决策需要的基础：Token、Transformer / Attention、Long Context、KV Cache、Decoding 等。

这一层服务于 AI 应用工程，不扩展成 CUDA / RLHF / 分布式训练 Infra 手册。

### RAG ⏳

```text
Parse / OCR / Layout
→ Corpus Audit
→ Chunk
→ Embedding
→ Retrieval
→ Query Rewrite
→ Hybrid Search
→ Rerank
→ Context Build
→ Grounding / Citation
→ Evaluation
→ Observability
→ Version / Snapshot
→ Incremental Update
→ Agentic RAG
```

---

## Agent Runtime

### Agent Harness / Runtime 🔬

重点研究：

- Agent Loop / Planning / Routing；
- Context Assembly / Compaction；
- Memory；
- Tool Runtime / Executor / Structured Tool Call；
- MCP / Skills / Discovery；
- Permission / Approval / Sandbox；
- Message / Event Model；
- State / Persistence / Checkpoint；
- Resume / Cancellation；
- Retry / Idempotency / Compensation；
- Multi-Agent / Sub-agent；
- Workspace / Coding Verification；
- Trace / Replay / Evaluation；
- Cost / Latency / Production Reliability。

---

# 推荐学习顺序

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering 基础
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用层）
  ↓
RAG
  ↓
Agent Harness
  ↓
System Design
```

`AI Backend Engineering` 是横向主线，会在 MySQL / Redis / RAG / Agent 阶段反复加深。

---

# 2026 真人面经研究

入口：[`research/README.md`](research/README.md)

当前研究已经完成严格清洗，并从干净基线继续扩大：

- 当前正式来源：**S001–S051，共 51 个 HUMAN-A 样本**；
- 当前正式批次：[`Batch 01`](research/interviews/batch-01.md) + [`Batch 02`](research/interviews/batch-02.md) + [`Batch 03`](research/interviews/batch-03.md)；
- Batch 02 新增 18 个 HUMAN-A；Batch 03 又新增 **20 个 HUMAN-A**；
- Canonical Question 层已经重置，只允许由 HUMAN-A 来源重新建立；
- 不保留低质量来源产生的额外面试题；
- 不使用自动化面试、合集、二次创作、标准答案、低信息密度复盘或无法核验线索；
- 搜索平台开放，但质量标准固定；
- 对登录态 / 搜索索引受限的平台，通过搜索摘要定位、企业 / 话题页回溯、作者主页、个人博客和跨平台原帖交叉验证来提高 Recall；
- 当前高质量真人来源仍远未饱和。

研究工作流：

```text
公开平台扩大搜索召回
      ↓
定位候选原帖
      ↓
HUMAN-A Gate
      ↓
Role Scope Gate
      ↓
原帖核验 / 跨平台去重
      ↓
来源归档
      ↓
问题简洁转述
      ↓
Canonical Question 语义去重
      ↓
公司 / 轮次 / 深度 / 频率分析
      ↓
校准复习优先级
```

---

# 写作风格

所有正式教材尽量遵循：

> **先讲人话 → 准确定义 → 代码 / 图解 → 原理 → 对比 → AI 实际场景 → 易错点 → 面试怎么答 → 深入追问 → 真人面经 → 折叠自测**

最终让每个知识点达到：

> **定义能说、代码能写、为什么能解释、工程边界能判断、真人面试追问能接。**