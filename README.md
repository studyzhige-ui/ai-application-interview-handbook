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
MySQL → Redis → Vector DB
                  ↓
                 RAG
                  ↓
            Agent Harness
                  ↓
             System Design
```

同时持续用 2026 真人高质量面经检查：

> **我们学会的知识，能不能真的回答面试官？**

---

## 核心原则

### 1. 知识体系是骨架，真人面经是血肉

Python、FastAPI、MySQL、Redis、Vector DB、RAG、Agent Harness 等模块都会从 0 建立完整知识体系，绝不会因为某个知识点暂时没出现在面经里就不学。

真人面经负责：校准优先级、保留真实问法、发现教材缺口、验证口述 / 追问 / System Design 能力。

### 2. 从 Demo 能力走到 Production 能力

我们不只学习“怎么调用 LLM / LangGraph / Milvus API”，还要回答：

> 超时怎么办？重复执行怎么办？Context 满了怎么办？Redis 挂了怎么办？RAG 召回不准怎么定位？Agent 如何取消和恢复？Tool 为什么不能让模型自己判断权限？

### 3. Agent Harness 以成熟产品源码为最高实现参考

Agent Harness / Runtime 的首要权威实现参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

目标不是复制框架 API，而是抽取 Agent Loop、Context、Memory、Tool Runtime、MCP / Skill、Permission / Sandbox、Checkpoint、Resume、Cancellation、Multi-Agent、Trace、Evaluation、Cost 与 Reliability 等稳定工程能力。

### 4. 正式面经只认 HUMAN-A

从 Batch 11 起，新的正式研究样本必须同时满足：

```text
真人面试官
   +
候选人本人高质量第一人称复盘
   +
AI Application / Agent 目标岗位
   ↓
HUMAN-A Core
```

AI 自动面试、低信息密度复盘、合集 / 整理、`含完整答案` / 标准答案、SEO 博客、水短视频和无法核验的线索不进入新的正式 Batch。

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

真实真人面经已经持续出现 Transformer / Attention / Token / Long Context / Lost in the Middle / KV Cache 等问题。课程边界是理解模型行为、推理延迟和应用决策，不扩展成 CUDA / RLHF / 分布式训练手册。

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

截至 2026-09-09：

- 历史来源 ID 已到 `S141`；
- 当前约 **209 道 canonical questions**；
- 最新 [`Batch 11`](research/interviews/batch-11.md) 新增 `S129–S141` 共 13 个 **HUMAN-A** 样本；
- 从 Batch 11 起正式样本只收真人面试官 + 高质量第一人称；
- 旧批次中曾保存的 automated / B/C/D/E 信号只保留历史追溯，不进入后续 HUMAN-A 真人频率核心；
- 搜索继续保持两条 Lane：Agent / Harness Frontier 与 AI Application Foundation；
- 当前判断：**高质量真人来源远未饱和，继续搜索。**

研究工作流：

```text
HUMAN-A 真人面经
      ↓
Role Scope Gate
      ↓
来源归档
      ↓
问题提取
      ↓
转载 / 语义去重
      ↓
Canonical Question
      ↓
模块 / 知识点标签
      ↓
公司 / 轮次 / 深度 / 频率分析
      ↓
反向校验完整知识体系
      ↓
发现 Gap → 补教材
```

---

# 写作风格

所有正式教材尽量遵循：

> **先讲人话 → 准确定义 → 代码 / 图解 → 原理 → 对比 → AI 实际场景 → 易错点 → 面试怎么答 → 深入追问 → 真人面经 → 折叠自测**

最终让每个知识点达到：

> **定义能说、代码能写、为什么能解释、工程边界能判断、真人面试追问能接。**
