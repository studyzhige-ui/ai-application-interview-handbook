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

### 2. 不同层级使用不同粒度

```text
HUMAN-A / Canonical Question
= 可独立追问的面试能力

Capability Map
= 更细的工程 primitive

教材文件
= 一个可以独立学习、复习、画图并解释 Failure / Trade-off 的知识小板块

文件内 Section
= 参数、变体、Failure Case、追问
```

因此不再默认 `1 Canonical ≈ 1 Markdown`。课程粒度审计与整改记录：[`roadmap/curriculum-granularity-audit.md`](roadmap/curriculum-granularity-audit.md)。

### 3. 从 Demo 能力走到 Production 能力

不仅学习“怎么调 API”，还要回答：超时怎么办、重复执行怎么办、Context 满了怎么办、缓存不一致怎么办、RAG 召回不准怎么定位、Agent 如何取消、恢复和验证。

### 4. Agent Harness 使用多层权威证据

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

### 5. 正式面经只认 HUMAN-A

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

完整系统正文 + Review + Interview。

### [FastAPI｜AI 应用服务层](fastapi/README.md) 🟡

已建立完整课程地图：HTTP / ASGI / Uvicorn → Routing / Pydantic → Dependency / Lifespan → async / Streaming → Auth → Provider Integration → Timeout / Cancellation → Testing / Trace / Deployment → RAG / Agent API。

### [AI Backend Engineering](backend-engineering/README.md) 🟡

已建立完整课程地图：Network / HTTP → Concurrency → Pool → Timeout / Retry / Circuit Breaker → Cancellation / Idempotency → MQ / Backpressure → Cache / Rate Limit / Consistency → Observability / Security → Deployment / Scaling。

---

## Data

### [MySQL](mysql/README.md) ✅

**23 章正文 + Review + Interview。教材粒度审计 PASS，当前不做机械合并。**

### [Redis](redis/README.md) 🟠

27 章正文 + Review + Interview 内容已完成；颗粒度审计发现少量相邻章节更适合作为同一知识板块，后续做 Minor Remediation，目标约 23 章。

### [Vector Database](vector-db/README.md) 🟠

23 章正文 + Review + Interview 内容已完成；颗粒度审计为 Moderate Remediation，计划把 Vector Space、Exact→ANN、HNSW、Index Lifecycle 等连续机制重新组合为约 16–18 个知识板块。

Vector DB 负责 Vector Infrastructure；Dense / Sparse、Hybrid、RRF、Rerank、Retrieval Evaluation 归 RAG。

---

## Model Foundation

### [LLM Foundation（应用工程深度）](llm-foundation/README.md) 🟠

29 章正文 + Review + Interview 内容已完成；知识顺序正确，但 Transformer / Generation / Serving 等部分文件过细，进入 Moderate Granularity Remediation，目标约 14–17 个知识板块。

---

## AI Application

### [RAG](rag/README.md) 🟠

34 章正文 + Review + Interview 内容已完成；Pipeline 顺序正确，但 Chunk / Query / Retrieval / Evaluation 的文件粒度明显接近 Canonical / mechanism 粒度，进入 Major Granularity Remediation，目标约 14–16 个知识板块。

---

## Agent Runtime

### [Agent Harness / Runtime](agent-harness/README.md) 🚧

旧 47 章已经完成结构重组，当前正式教材目标为 **23 个知识小板块**；`docs/` 已物理迁移为连续 `01–23`，旧碎片已清理。当前正在做深度验收与 Review / Interview 导航校准，暂不标记最终完成。

```text
Agent / Workflow / Harness
→ Loop / Run / Turn / Step / Event
→ Tool Runtime
→ Planning / Goal / Stop / Budget
→ Context Assembly / Compaction
→ Memory / State / Long-running Reliability
→ Permission / Sandbox / Injection / Containment
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping / Build-vs-Buy
```

实现参考固定版本：

- Claude Code commit：`58231dcce408f805c645cfbc352d2876b517223b`
- OpenAI Codex commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

外部权威资料索引：[`research/agent-sources/authoritative-web-sources.md`](research/agent-sources/authoritative-web-sources.md)

---

## Integration

### System Design ⏸️

System Design 仍是正式十板块的最后一块，但**暂不立刻开写**。先完成当前教材粒度整改，尤其是 Agent / RAG / LLM，避免把“Canonical 粒度 = 文件粒度”的问题复制进 System Design。

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

一个 Markdown 文件应完成一个“知识小板块”的闭环，而不是仅承载一个可独立面试追问。

最终目标：**定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

# 当前建设状态

| 模块 | 状态 |
|---|---|
| Python | ✅ 完整系统教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 完整教材；粒度审计 PASS |
| Redis | 🟠 内容完成；Minor Granularity Remediation |
| Vector DB | 🟠 内容完成；Moderate Granularity Remediation |
| LLM Foundation | 🟠 内容完成；Moderate Granularity Remediation |
| RAG | 🟠 内容完成；Major Granularity Remediation |
| Agent Harness / Runtime | 🚧 47→23 已迁移；深度验收中 |
| System Design | ⏸️ 待粒度整改后启动 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
