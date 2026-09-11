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

## 核心原则

### 1. 知识体系决定主干，真人面经校准重点

所有模块都先按初学者认知依赖从 0→1 建立完整体系。真人面经只负责调整复习优先级、保留真实问法、补充追问链，并检查 Failure / Scale / Evaluation 深度。

**不会因为某个知识点真人面经更高频，就打乱模块本身的主要演进顺序。**

### 2. 从 Demo 能力走到 Production 能力

不仅学习“怎么调 API”，还要回答：超时怎么办、重复执行怎么办、Context 满了怎么办、缓存不一致怎么办、RAG 召回不准怎么定位、Agent 如何取消、恢复和验证。

### 3. Agent Harness 使用多层权威证据

Agent Harness / Runtime 正式教材综合：

```text
44 道 HUMAN-A Agent Canonical
+ Verified Follow-up Chains
+ Claude Code 固定源码快照
+ OpenAI Codex 固定源码快照
+ Anthropic / OpenAI 官方工程资料
+ MCP / A2A 官方规范
+ ReAct / SWE-bench 等原始论文
```

源码与外部权威资料用于补齐成熟 Runtime 知识边界，**不能反向改变 HUMAN-A Source Count**。

证据入口：[`research/agent-sources/README.md`](research/agent-sources/README.md)

### 4. 正式面经只认 HUMAN-A

只有满足真人候选人第一人称、高质量现场证据、岗位范围符合、原文可核验且非转载 / 非同场重复的来源，才能进入正式研究并贡献频率。

详细规则：[`research/quality/source-quality-policy.md`](research/quality/source-quality-policy.md)

---

# 当前正式研究基线

入口：[`research/README.md`](research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
正式 Batch：26
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
主动采集：已暂停
```

Phase 2B 已完成：Global Canonical Index、Frequency、Market Coverage、Depth / Question Type、Co-occurrence、Verified Follow-up Chains、Curriculum Evidence Matrix 与 Knowledge Gap Analysis。

---

# 总知识地图

完整地图：[`roadmap/knowledge-map.md`](roadmap/knowledge-map.md)

## Foundation

### [Python Foundation](python/README.md) ✅

完整 12 章系统正文 + Review + Interview。

### [FastAPI｜AI 应用服务层](fastapi/README.md) 🟡

已建立完整课程地图：HTTP / ASGI / Uvicorn → Routing / Pydantic → Dependency / Lifespan → async / Streaming → Auth → Provider Integration → Timeout / Cancellation → Testing / Trace / Deployment → RAG / Agent API。

### [AI Backend Engineering](backend-engineering/README.md) 🟡

已建立完整课程地图：Network / HTTP → Concurrency → Pool → Timeout / Retry / Circuit Breaker → Cancellation / Idempotency → MQ / Backpressure → Cache / Rate Limit / Consistency → Observability / Security → Deployment / Scaling。

---

## Data

### [MySQL](mysql/README.md) ✅

第一版系统教材已完成：**23 章正文 + Review + 高频面试题 + 易错点 + 面试前速查。**

### [Redis](redis/README.md) ✅

第一版系统教材已完成：**27 章正文 + Review + 35 道面试题 + 45 个易错点 + 面试前速查。**

### [Vector Database](vector-db/README.md) ✅

第一版系统教材已完成：**23 章正文 + Review + 31 道面试题 + 45 个易错点 + 面试前速查。**

Vector DB 负责 Vector Infrastructure；Dense / Sparse、Hybrid、RRF、Rerank、Retrieval Evaluation 归 RAG。

---

## Model Foundation

### [LLM Foundation（应用工程深度）](llm-foundation/README.md) ✅

第一版系统教材已完成：**29 章正文 + Review + 30 道面试题 + 55 个易错点 + 面试前速查。**

```text
Token / Context
→ Transformer / Attention / RoPE
→ Generation / Sampling
→ KV Cache / Prefill / Decode
→ Serving / Cost
→ Model API / Selection
→ Embedding / Reranker / Multimodal
→ Prompt / Hallucination
→ SFT / LoRA / Preference Optimization / Distillation
```

---

## AI Application

### [RAG](rag/README.md) ✅

第一版系统教材已完成：**34 章正文 + Review + 40 道高频面试题 + 60 个易错点 + 面试前速查。**

```text
Corpus / Lineage / Parse / Clean
→ Chunk
→ Query Transformation
→ Dense / Sparse / Hybrid / RRF
→ Rerank / Top-K
→ Context / Grounding / Citation
→ Metrics / Eval / Regression / Bad Case
→ Freshness / Permission / Scale / Observability
→ GraphRAG / Agentic RAG
```

---

## Agent Runtime

### [Agent Harness / Runtime](agent-harness/README.md) ✅

第一版 0→1 系统教材已完成：**47 章正文 + Review + 56 道高频/核心面试题 + 86 个易错点 + 面试前速查。**

主干不是 Framework API，而是 Runtime 问题演进：

```text
Agent vs Workflow
→ Harness / Runtime Boundary
→ Agent Loop
→ Run / Turn / Step / Event
→ Tool Contract / Validation / Execution / Failure
→ Planning / Stop / Budget
→ Context Assembly / Budget / Tool-result Offload
→ Compaction / Correctness
→ Memory / Session / State / Persistence
→ Checkpoint / Resume / Fork / Cancellation
→ Idempotency / Side Effect / Compensation
→ Permission / Approval / Sandbox / Guardrails
→ Prompt Injection / Secret Containment
→ Tool Discovery / MCP / Skills / Hooks
→ Intent / Model Routing
→ Multi-Agent / Handoff / A2A / Workspace Concurrency
→ Trace / Replay / Evaluation
→ Coding Agent Verification
→ Production Runtime Architecture
→ Framework Mapping / Build-vs-Buy
```

实现参考已固定版本：

- Claude Code commit：`58231dcce408f805c645cfbc352d2876b517223b`
- OpenAI Codex commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

外部权威资料索引：[`research/agent-sources/authoritative-web-sources.md`](research/agent-sources/authoritative-web-sources.md)

---

## Integration

### System Design 🚧

**下一块正式系统教材。**

它会把 FastAPI、Backend、MySQL、Redis、Vector DB、LLM、RAG 与 Agent Harness 汇合到完整 Production Architecture。

---

# 推荐学习顺序

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
LLM Foundation
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

---

# 写作风格

正式教材遵循：

> **先讲人话 → 准确定义 → 代码 / 数学 / 图解 → 原理 → 对比 → Failure Case → AI 场景 → 易错点 → 面试回答 → 深入追问 → 真人面经 → 折叠自测**

最终目标：**定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

# 当前建设状态

| 模块 | 状态 |
|---|---|
| Python | ✅ 完整系统教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 第一版完整系统教材 |
| Redis | ✅ 第一版完整系统教材 |
| Vector DB | ✅ 第一版完整系统教材 |
| LLM Foundation | ✅ 第一版完整系统教材 |
| RAG | ✅ 第一版完整系统教材 |
| Agent Harness / Runtime | ✅ 第一版完整系统教材 |
| System Design | 🚧 **下一块正式系统教材** |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
