# AI Application Interview Handbook

> 面向 **AI 应用开发 / AI Agent 开发** 求职的一套系统化知识体系、工程手册与真实面经验收系统。

这不是一本“AI 八股题库”。我们的目标是从 0 建立完整能力链：

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

同时持续使用 2026 高质量真实面经检查：

> **我们学会的知识，能不能真的回答面试官？**

---

## 核心原则

### 1. 知识体系是骨架，真实面经是血肉

Python、FastAPI、MySQL、Redis、Vector DB、RAG、Agent Harness 等模块都会从 0 建立完整知识体系，绝不会因为某个知识点暂时没出现在面经里就不学。

真实面经负责：

- 校准学习优先级；
- 提供面试官真实问法；
- 暴露教材知识缺口；
- 检查是否真正具备口述、追问和系统设计能力。

### 2. 从 Demo 能力走到 Production 能力

我们不止学习：

> “怎么调用 LLM / LangGraph / Milvus API？”

还要回答：

> 超时怎么办？重复执行怎么办？Context 满了怎么办？Redis 挂了怎么办？RAG 召回不准怎么定位？Agent 如何取消和恢复？1000 个并发用户怎么办？Tool 为什么不能让模型自己判断权限？

### 3. 框架会变，稳定的工程能力更重要

FastAPI、LangGraph、向量数据库产品都可能演进，因此正文会区分：

- 稳定原理；
- 当前框架事实；
- 工程设计取舍。

### 4. 面经必须同时满足“高质量 + 岗位方向正确”

正式面经样本不仅要求第一人称、可核验、问题具体，还必须服务于我们的求职方向：

```text
AI 应用开发 / AI Agent 开发 / 大模型应用开发
AI 全栈 / AI 后端 / RAG / Applied AI / FDE
Agent Harness / Runtime / Coding Agent
```

传统数据分析 / BI、纯推荐算法、纯模型训练/Infra，以及与 AI 应用没有实质关系的传统后端面经，不用于本项目的真实面试频率统计。

---

# 总知识地图

完整地图：[`roadmap/knowledge-map.md`](roadmap/knowledge-map.md)

## Foundation

### [Python Foundation](python/README.md) ✅

已经完成并从原独立 Python 手册迁入：

- 12 章系统正文；
- 12 章 Mermaid 图解 + 折叠自测；
- 55 道 Python 高频面试题；
- 25 组 Python Coding 小题；
- 面试易错点；
- 面试前速查表。

Python 在这里不仅是语法基础，还承担 GIL、asyncio、线程/进程/协程、生成器、上下文管理等 AI Backend Runtime 基础。

### [FastAPI｜AI 应用服务层](fastapi/README.md) 🟡

FastAPI 正式成为一级模块，而不是 Python 附录。

课程将覆盖：

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

目标：把“会 Python”升级成“能做真实 AI Service”。

### [AI Backend Engineering](backend-engineering/README.md) 🟡

这是贯穿所有模块的横向生产工程主线：

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

下一块正式系统教材：SQL、B+Tree、索引、EXPLAIN、事务、MVCC、锁、日志、Schema Design、MySQL + Redis 一致性，以及 AI 应用数据建模。

### Redis ⏳

数据结构、线程/I/O 模型、TTL、淘汰、RDB/AOF、BigKey/HotKey、缓存问题、分布式锁、Lua、Session、Agent State、限流。

### Vector Database ⏳

Embedding → Distance → TopK → ANN → HNSW / IVF → Metadata Filter → Dense / Sparse → Hybrid Search → RRF → Rerank → Index Lifecycle → 产品选型。

---

## AI Application

### RAG ⏳

```text
Parse / OCR / Layout
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

这是最终最深、最大的模块。

**首要权威实现参考：**

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

目标不是复制框架 API，而是从成熟 Agent 产品源码中抽取稳定 Runtime 能力：

- Agent Loop / Planning / Routing；
- Context Assembly / Compaction；
- Memory；
- Tool Runtime / Executor；
- MCP / Skills / Discovery；
- Permission / Approval / Sandbox；
- Message / Event Model；
- State / Persistence / Checkpoint；
- Resume / Cancellation；
- Retry / Idempotency / Compensation；
- Multi-Agent；
- Workspace / Coding Verification；
- Trace / Replay / Evaluation；
- Cost / Latency / Production Reliability。

详细原则：[`roadmap/agent-authoritative-sources.md`](roadmap/agent-authoritative-sources.md)

---

# 推荐学习顺序

## 第一遍：建立完整能力链

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
RAG
  ↓
Agent Harness
  ↓
System Design
```

`AI Backend Engineering` 不需要一次学完，它会在 MySQL / Redis / RAG / Agent 阶段反复回来加深。

> Batch 09–10 持续出现一个值得正式建模的信号：AI 应用岗会追问 Transformer / Attention / Temperature / Top-p、KV Cache 等 **LLM Foundation / Inference Runtime 的应用工程深度**。后续会把这一层纳入知识地图，但不会把本项目扩展成训练算法 / CUDA Infra 手册。

## 第二遍：真实面经反向验收

```text
知识章节
  ↓
Review 自测
  ↓
真实面经
  ↓
30 秒回答
  ↓
2～3 分钟完整回答
  ↓
深挖追问 / System Design
```

---

# 2026 真实面经研究

入口：[`research/README.md`](research/README.md)

当前已经建立：

- 高质量来源分级规则；
- AI Application / Agent 岗位范围准入规则；
- 原始面经层；
- Canonical Question 语义去重层；
- 跨平台 Leads；
- 高频与知识缺口分析；
- 持续监控机制。

截至 2026-09-09 当前研究状态：

- 已归档 `S001–S128` 来源记录；
- 已形成约 **205 道 canonical questions**；
- 从 Batch 06 起执行严格“宁缺毋滥”准入；
- 从 Batch 08 起增加 Role Scope Gate，排除与目标方向无关的数据分析 / BI / 纯推荐 / 纯训练 Infra 场次；
- 从 Batch 10 起开始区分 `interviewer_type`，避免自动化 AI 面试与真人技术面默认等权；
- 搜索同时保持两条 Lane：
  - **Agent / Harness Frontier**；
  - **AI Application Foundation**（Python / FastAPI / MySQL / Redis / Backend）。

> 来源记录数量不等于等权真实面试场次数量。第一人称高置信来源、合集、二次创作、自动化面试和待核实线索会严格区分，避免污染真实频率。

## 研究工作流

```text
高质量真实面经
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
频率 / 公司 / 轮次 / 深度分析
      ↓
反向校验完整知识体系
      ↓
发现 Gap → 补教材
```

第三方面经只保存来源元数据与问题的简洁转述，不复制整篇受版权保护的帖子。

---

# 写作风格

所有正式教材尽量遵循：

> **先讲人话 → 准确定义 → 代码 / 图解 → 原理 → 对比 → AI 实际场景 → 易错点 → 面试怎么答 → 深入追问 → 真实面经 → 折叠自测**

目标不是“文档很多”，而是最终让每个知识点达到：

> **定义能说、代码能写、为什么能解释、工程边界能判断、真实面试追问能接。**