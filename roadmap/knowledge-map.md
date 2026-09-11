# AI Application Engineer 求职知识总地图

> 围绕 **AI 应用开发 / Agent 开发岗位**，从语言 → 服务 → 数据 → 模型基础 → 检索 → Agent Runtime → Production System 建立完整 0→1 能力链。
>
> 当前真人面经研究基线：`S001–S279` HUMAN-A（Frozen），**235 ACTIVE Canonical**。面经只校准市场频率、真实问法和追问深度，不反向限制完整知识体系。

## 1. 正式十板块

```text
01 Python
        ↓
02 FastAPI
        ↓
03 AI Backend Engineering
        ↓
04 MySQL
        ↓
05 Redis
        ↓
06 Vector DB
        ↓
07 LLM Foundation（应用工程深度）
        ↓
08 RAG
        ↓
09 Agent Harness / Runtime
        ↓
10 System Design
```

贯穿所有模块：Evaluation / Verification、Reliability / Failure Recovery、Security / Permission、Observability、AI-assisted Development、Cost / Latency / Scale。

---

# 2. 教材文件粒度规则

研究层和教材层不使用同一粒度：

```text
Canonical Question
= 可独立追问能力

Capability Primitive
= 工程最小机制

教材文件
= 一个完整知识小板块 / 认知闭环

Section
= 参数、变体、Failure、追问
```

审计记录：[`curriculum-granularity-audit.md`](curriculum-granularity-audit.md)。

---

# 3. Foundation

## Python ✅
入口：[`../python/README.md`](../python/README.md) — 完整系统教材 + Review + Interview。

## FastAPI 🟡
入口：[`../fastapi/README.md`](../fastapi/README.md) — 完整课程骨架，正文后续补齐。

## AI Backend Engineering 🟡
入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 完整课程骨架，是贯穿后续模块的横向主线。

---

# 4. Data

## MySQL ✅
入口：[`../mysql/README.md`](../mysql/README.md) — **23 章 + Review + Interview**。

教材粒度审计：**PASS**。查询性能、事务并发和生产扩展的章节都形成独立知识闭环，不为了和其它模块统一数字而机械合并。

## Redis 🟠
入口：[`../redis/README.md`](../redis/README.md) — 当前 **27 章 + Review + Interview**。

内容体系已完成，进入 Minor Granularity Remediation：重点审查 Runtime/Performance、Transaction/Pipeline/Lua、Distributed Lock 等相邻文件，目标约 23 个知识板块。

## Vector Database 🟠
入口：[`../vector-db/README.md`](../vector-db/README.md) — 当前 **23 章 + Review + Interview**。

内容体系已完成，进入 Moderate Granularity Remediation：Vector Space、Exact→ANN、HNSW、Index Lifecycle、Production Diagnosis 等应按知识闭环重新组合，目标约 16–18 个知识板块。

Primary Boundary：Vector DB 负责向量基础设施；Dense/Sparse、Hybrid、RRF、Rerank、Retrieval Evaluation 归 RAG。

---

# 5. Model Foundation

## LLM Foundation（应用工程深度） 🟠
入口：[`../llm-foundation/README.md`](../llm-foundation/README.md) — 当前 **29 章 + Review + Interview**。

知识演进顺序正确，但 Transformer / Generation / Serving 等部分按 mechanism 拆得过细，进入 Moderate Granularity Remediation，目标约 14–17 个知识板块。

```text
Token / Context
→ Transformer / Attention / RoPE
→ Generation / Sampling
→ KV Cache / Serving / Cost
→ Model API / Selection
→ Embedding / Reranker / Multimodal
→ Prompt / Hallucination
→ Fine-tuning / Alignment Boundary
```

---

# 6. AI Application

## RAG 🟠
入口：[`../rag/README.md`](../rag/README.md) — 当前 **34 章 + Review + Interview**。

Pipeline 顺序本身正确，但 Chunk、Query、Retrieval、Evaluation 等连续机制被切成过多小文件，进入 Major Granularity Remediation，目标约 14–16 个知识板块。

```text
Corpus / Lineage / Parse / Clean
→ Chunk
→ Query Transformation
→ Dense / Sparse / Hybrid / RRF / Rerank
→ Context / Grounding / Citation
→ Evaluation / Regression / Bad Case
→ Freshness / Permission / Scale
→ GraphRAG / Agentic RAG
```

---

# 7. Agent Runtime

## Agent Harness / Runtime 🚧

入口：[`../agent-harness/README.md`](../agent-harness/README.md)

旧 47 章目录已经完成颗粒度重组，当前 `docs/` 正式为 **23 个连续知识小板块**；旧碎片文件已删除。当前继续做深度验收和 Review / Interview 导航校准，因此暂不标为最终完成。

证据体系：

```text
44 Agent HUMAN-A Canonical
+ Verified Follow-up Chains
+ Claude Code fixed source snapshot
+ OpenAI Codex fixed source snapshot
+ Anthropic / OpenAI official engineering materials
+ MCP / A2A official specifications
+ ReAct / SWE-bench primary papers
```

证据入口：[`../research/agent-sources/README.md`](../research/agent-sources/README.md)

固定实现快照：

```text
Claude Code commit = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

正式 0→1 主线：

```text
Agent / Workflow / Harness
→ Loop / Run / Turn / Step / Event
→ Tool Runtime
→ Planning / Goal / Stop / Budget
→ Context Assembly / Compaction
→ Memory / State / Checkpoint / Resume
→ Permission / Sandbox / Injection / Containment
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping / Build-vs-Buy
```

课程继续坚持：

> **先 Runtime Problem，再 Runtime Primitive，再看成熟源码实现，最后才映射 Framework。**

因此 LangGraph / LangChain / OpenAI Agents SDK 不作为课程起点。

---

# 8. System Design ⏸️

System Design 仍是第 10 个正式一级模块，但现在暂缓启动。

先完成当前 Granularity Remediation，尤其是 Agent / RAG / LLM，避免把：

```text
Canonical Question
≈ Markdown Chapter
```

这种错误粒度复制到 System Design。

未来 System Design 仍会汇合：

- 企业知识库 RAG；
- 大规模文档 RAG；
- 多租户 AI Chat / Agent Platform；
- Coding Agent Backend；
- Long-running Agent Platform；
- Multi-Agent Workflow；
- AI Customer Service；
- Data / Analytical Agent。

---

# 9. Bridge Labs

```text
Bridge A：FastAPI + Async LLM Service
Bridge B：MySQL + Redis + MQ 的可靠 AI Backend
Bridge C：Vector DB + RAG Evaluation Pipeline
Bridge D：RAG + Agent Harness + Long-running Runtime
```

---

# 10. Interview Reality

研究入口：[`../research/README.md`](../research/README.md)

```text
HUMAN-A：S001–S279（Frozen）
ACTIVE Canonical：235
Mapped Sources：278
VALID-UNMAPPED：1（S271）
```

> 面经决定“哪里高频、哪里追得深”，不决定“只学哪些知识”，也不决定“每一道题都必须独立成为一章”。

---

# 11. 当前 Phase 3 状态

| 模块 | 当前状态 |
|---|---|
| Python | ✅ 完整教材 |
| FastAPI | 🟡 完整课程骨架 |
| AI Backend Engineering | 🟡 完整课程骨架 |
| MySQL | ✅ 23 章；Granularity PASS |
| Redis | 🟠 27 章内容完成；Minor Remediation |
| Vector DB | 🟠 23 章内容完成；Moderate Remediation |
| LLM Foundation | 🟠 29 章内容完成；Moderate Remediation |
| RAG | 🟠 34 章内容完成；Major Remediation |
| Agent Harness / Runtime | 🚧 已迁移为 23 章；深度验收中 |
| System Design | ⏸️ Granularity Remediation 后启动 |
| 真人面经研究 | ✅ Frozen Phase 2B 完成 |
