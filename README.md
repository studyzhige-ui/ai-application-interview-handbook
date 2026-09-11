# AI Application Interview Handbook

> 面向 **AI 应用开发 / AI Agent 开发** 求职的一套系统化知识体系、工程手册与真人面经验收系统。

这不是“按面试题拼起来的八股仓库”。课程主干按初学者 0→1 的知识依赖建立，真人面经只校准市场热度、真实问法、追问深度以及 Failure / Scale / Evaluation 强度。

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

不会因为某个知识点真人面经更高频，就打乱模块本身的主要演进顺序。

### 2. 研究粒度、能力粒度、教材粒度必须分开

```text
HUMAN-A / Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 可独立学习、画图、解释 Failure / Trade-off 的知识小板块
Section = 参数 / 变体 / Failure Case / 追问
```

因此不再默认 `1 Canonical ≈ 1 Markdown`。完整审计见 [`roadmap/curriculum-granularity-audit.md`](roadmap/curriculum-granularity-audit.md)。
Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。
Foundation 的真实完成度与 Python v1 质量核实见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。System Design 完成后的仓库补齐顺序是：**FastAPI → AI Backend Engineering → Python v1 定向整改**。

### 3. 从 Demo 能力走到 Production 能力

不仅会“调 API”，还要能解释 Timeout、Cancellation、Idempotency、Context Compaction、Cache Consistency、RAG Bad Case、Agent Resume / Permission / Evaluation 等系统问题。

### 4. Agent Harness 使用多层证据

```text
44 道 HUMAN-A Agent Canonical
+ Verified Follow-up Chains
+ Claude Code 固定源码快照
+ OpenAI Codex 固定源码快照
+ Anthropic / OpenAI 官方工程资料
+ MCP / A2A 官方规范
+ ReAct / SWE-bench 等原始论文
```

外部证据用于补齐成熟 Runtime 的知识边界，**不能改变 HUMAN-A Source Count**。

---

# 当前研究基线

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

# 当前教材结构

## Foundation

- [Python Foundation](python/README.md) 🟠 **v1 完整可用**；最新 15 Canonical / 当前统一深度标准的定向整改待完成
- [FastAPI](fastapi/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写
- [AI Backend Engineering](backend-engineering/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写

## Data

- [MySQL](mysql/README.md) ✅ **23 个知识小板块**；Granularity Audit PASS
- [Redis](redis/README.md) ✅ **24 个知识小板块**；已完成 27→24 颗粒度整改
- [Vector Database](vector-db/README.md) ✅ **16 个知识小板块**；已完成 23→16 颗粒度整改

## Model Foundation

- [LLM Foundation（应用工程深度）](llm-foundation/README.md) ✅ **14 个知识小板块**；已完成 29→14 颗粒度整改

## AI Application

- [RAG](rag/README.md) ✅ **14 个知识小板块**；已完成 34→14 颗粒度整改

## Agent Runtime

- [Agent Harness / Runtime](agent-harness/README.md) ✅ **23 个知识小板块**；已完成 47→23 结构整改和正文深度验收

Agent 正式主线：

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

固定源码快照：

- Claude Code：`58231dcce408f805c645cfbc352d2876b517223b`
- OpenAI Codex：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

证据入口：[`research/agent-sources/README.md`](research/agent-sources/README.md)

## Integration

- [System Design](system-design/README.md) ✅ **19 个知识小板块**；24 道 L4 Canonical 已映射到通用设计方法 + 7 类综合真人场景，Review / Interview 已完成。

---

# 为什么不同模块章节数不同

章节数不是优化目标：

```text
MySQL 23
Redis 24
Vector DB 16
LLM Foundation 14
RAG 14
Agent Harness 23
System Design 19
```

这些数字来自各模块自己的认知闭环，而不是为了统一格式。MySQL 的 B+Tree、MVCC、Lock、Replication、Sharding 本来就有独立数据结构和 Failure Model；RAG 与 LLM 原先则明显把机制切得过细，因此大幅收敛。

---

# 推荐学习顺序

```text
Python
→ FastAPI
→ AI Backend Engineering
→ MySQL
→ Redis
→ Vector DB
→ LLM Foundation
→ RAG
→ Agent Harness / Runtime
→ System Design
```

正式教材统一遵循：

> **先讲人话 → 准确定义 → 代码 / 数学 / 图解 → 原理 → 对比 → Failure Case → AI 场景 → 易错点 → 面试回答 → 深入追问 → 真人面经 → 折叠自测**

最终目标：**定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

# 当前 Phase 3 状态

| 模块 | 状态 |
|---|---|
| Python | 🟠 v1 完整可用；最新 Canonical / 当前深度标准定向整改待完成 |
| FastAPI | ⏳ README 课程骨架；正式正文未写 |
| AI Backend Engineering | ⏳ README 课程骨架；正式正文未写 |
| MySQL | ✅ 23-block；Granularity PASS |
| Redis | ✅ 24-block；整改完成 |
| Vector DB | ✅ 16-block；整改完成 |
| LLM Foundation | ✅ 14-block；整改完成 |
| RAG | ✅ 14-block；整改完成 |
| Agent Harness / Runtime | ✅ 23-block；结构整改 + 深度验收完成 |
| System Design | ✅ 19-block；正文 + Review + Interview 完成 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
