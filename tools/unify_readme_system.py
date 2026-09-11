from __future__ import annotations

from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    {
        "slug": "python",
        "name": "Python Foundation",
        "title": "Python Foundation｜Python 语言与运行时基础",
        "level": "Foundation",
        "role": "建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。",
        "blocks": 13,
        "canonical": 15,
        "sources": 15,
        "canonical_file": "python.md",
        "mainline": "Object Model / Containers → Function / Scope → Iterator / Context Manager → OOP / Protocol → Structured Data → Memory / GIL → Thread / Process / asyncio → Data Structure",
        "signals": ["dict / Hash / Slicing 成本", "GIL 与 Thread / Process", "asyncio / Timeout / Cancellation", "Lock / RLock / Semaphore", "Structured Output / JSON Validation"],
        "boundaries": [
            "Python 负责语言与 Runtime 语义；HTTP / ASGI Service 进入 FastAPI。",
            "Timeout / Retry / MQ / Backpressure 等跨服务机制进入 AI Backend Engineering。",
            "Agent Loop / Tool / Memory / Checkpoint 进入 Agent Harness / Runtime。",
        ],
        "parts": [(1, 5, "Part A｜对象、容器与函数"), (6, 10, "Part B｜Python 工程抽象"), (11, 13, "Part C｜Runtime、并发与复杂度")],
        "extra_interview": [("Python 高频 Coding 小题", "interview/Python高频Coding小题.md")],
    },
    {
        "slug": "fastapi",
        "name": "FastAPI",
        "title": "FastAPI｜AI 应用服务层",
        "level": "Foundation",
        "role": "把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。",
        "blocks": 16,
        "canonical": 4,
        "sources": 3,
        "canonical_file": "fastapi.md",
        "mainline": "ASGI Request Lifecycle → API Contract / Validation → DI / Middleware / Resource Lifecycle → Async Boundary → SSE / WebSocket → Security / External Resource → Cancellation → Testing / Observability / Deployment → AI Service Patterns",
        "signals": ["ASGI / Request Lifecycle", "Middleware vs Dependency", "FastAPI + SSE / Agent Streaming", "CRUD Framework 与 Production Agent Service 的边界"],
        "boundaries": [
            "asyncio 的语言 Runtime 语义归 Python；FastAPI 只解释框架怎样承接它。",
            "通用 Retry / Idempotency / MQ / Backpressure 归 AI Backend Engineering。",
            "Agent Loop / State / Tool Runtime 归 Agent Harness。",
        ],
        "parts": [(1, 6, "Part A｜从 Python 到 ASGI Service"), (7, 9, "Part B｜AI Service Transport 与安全"), (10, 12, "Part C｜外部系统与可靠请求生命周期"), (13, 16, "Part D｜Production FastAPI")],
        "source_index": "../research/fastapi-sources/README.md",
    },
    {
        "slug": "backend-engineering",
        "name": "AI Backend Engineering",
        "title": "AI Backend Engineering｜Production 后端工程底座",
        "level": "Foundation",
        "role": "把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。",
        "blocks": 22,
        "canonical": 39,
        "sources": 125,
        "canonical_file": "ai-backend-engineering.md",
        "mainline": "Request / Network → Concurrency / Pool / Backpressure → Timeout / Retry / Idempotency → MQ / Kafka / Durable Task → Consistency / State / Auth → Discovery / Observability / Linux / K8s → Config / Security → Cross-language Runtime Mapping",
        "signals": ["DB + Cache Consistency", "TCP / Streaming Reliability", "Thread Pool / Backpressure", "MQ Reliability / Kafka", "Rate Limit / Retry / Idempotency", "MySQL / Redis State Layering"],
        "boundaries": [
            "FastAPI 负责框架请求生命周期；AIBE 负责跨框架 Production Primitive。",
            "MySQL / Redis / Vector DB 的内部机制仍归各自数据模块。",
            "完整端到端架构组合与容量方案进入 System Design。",
        ],
        "parts": [(1, 3, "Part A｜Network 与 Service Communication"), (4, 6, "Part B｜Concurrency、Capacity 与 Overload"), (7, 9, "Part C｜Timeout、Retry 与 Side-effect Safety"), (10, 12, "Part D｜Messaging 与 Long-running Task"), (13, 16, "Part E｜Consistency、State 与 Permission"), (17, 21, "Part F｜Operations 与 Production Runtime"), (22, 22, "Part G｜跨语言 Runtime 映射")],
        "source_index": "../research/backend-sources/README.md",
    },
    {
        "slug": "mysql",
        "name": "MySQL",
        "title": "MySQL｜关系型数据、事务与查询工程",
        "level": "Data",
        "role": "理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。",
        "blocks": 23,
        "canonical": 26,
        "sources": 55,
        "canonical_file": "mysql.md",
        "mainline": "SQL Execution → Index / B+Tree / Optimizer / EXPLAIN → Transaction / Isolation / MVCC / Lock / Log → Pagination / Schema → Replication / Sharding / CDC / Bulk Write → AI Data Modeling / Cache Boundary",
        "signals": ["Isolation Levels", "B+Tree", "Slow SQL / EXPLAIN", "Index Invalidation / Composite Index", "Sharding", "MVCC / Lock"],
        "boundaries": [
            "InnoDB 索引、事务、MVCC、锁与日志归 MySQL。",
            "DB + Cache 最终一致性的完整机制归 AI Backend Engineering。",
            "Redis Lock、TTL、Cluster 归 Redis；跨组件架构选择归 System Design。",
        ],
        "parts": [(1, 10, "Part A｜查询与索引"), (11, 15, "Part B｜事务与并发正确性"), (16, 21, "Part C｜数据增长与生产扩展"), (22, 23, "Part D｜AI Application 数据层边界")],
    },
    {
        "slug": "redis",
        "name": "Redis",
        "title": "Redis｜缓存、短状态与分布式协调",
        "level": "Data",
        "role": "掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。",
        "blocks": 24,
        "canonical": 19,
        "sources": 69,
        "canonical_file": "redis.md",
        "mainline": "Key / Data Structure / Encoding → Runtime / TTL / Eviction → Cache Failure / HotKey → RDB / AOF / Replication / Sentinel / Cluster → Transaction / Pipeline / Lua / Distributed Lock → Streams / Session / Rate Limit / Troubleshooting",
        "signals": ["Distributed Lock 与 Correctness", "Cache Penetration / Breakdown / Avalanche", "Core Data Structures", "BigKey / HotKey", "Lua / Atomicity", "HA / Cluster"],
        "boundaries": [
            "Redis 数据结构、TTL、持久化、高可用与锁实现归 Redis。",
            "DB + Cache 一致性、通用 Rate Limit 与 MQ 选型归 AI Backend Engineering。",
            "Agent Checkpoint / Resume 的执行语义归 Agent Harness。",
        ],
        "parts": [(1, 6, "Part A｜数据模型与 Runtime"), (7, 10, "Part B｜内存生命周期与 Cache"), (11, 14, "Part C｜Persistence、HA 与 Scale"), (15, 18, "Part D｜原子性与分布式协调"), (19, 24, "Part E｜Backend / AI 场景")],
    },
    {
        "slug": "vector-db",
        "name": "Vector Database",
        "title": "Vector Database｜向量检索与索引系统",
        "level": "Data",
        "role": "理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。",
        "blocks": 16,
        "canonical": 12,
        "sources": 37,
        "canonical_file": "vector-db.md",
        "mainline": "Vector Space / Similarity → Exact vs ANN → HNSW / IVF / Quantization / Index Selection → Schema / Filter / Tenant → Index Lifecycle / Distributed → Performance Diagnosis / Product Boundary",
        "signals": ["Vector Storage / Architecture Selection", "HNSW 与参数", "HNSW vs IVF / Index Selection", "Index Lifecycle / Rebuild", "Metadata Filter", "Graph DB vs Vector DB"],
        "boundaries": [
            "Embedding / Reranker 模型原理归 LLM Foundation。",
            "Dense / Sparse / Hybrid / RRF / Retrieval Eval 归 RAG。",
            "Vector DB 负责高效可靠地存和找向量，不负责完整 Retrieval Pipeline。",
        ],
        "parts": [(1, 3, "Part A｜Vector Space 与 ANN 基础"), (4, 8, "Part B｜ANN Index"), (9, 13, "Part C｜Data Model、Filter 与 Lifecycle"), (14, 16, "Part D｜Production 与 Architecture Boundary")],
    },
    {
        "slug": "llm-foundation",
        "name": "LLM Foundation（应用工程深度）",
        "title": "LLM Foundation（应用工程深度）｜模型机制与推理基础",
        "level": "Model Foundation",
        "role": "以应用工程深度理解 Token、Transformer、Generation、KV Cache、Serving、模型选择与 Prompt / Fine-tuning 的边界。",
        "blocks": 14,
        "canonical": 23,
        "sources": 82,
        "canonical_file": "llm-foundation.md",
        "mainline": "Token / Context → Transformer / Attention / Position → Generation / Decoding → KV Cache / Prefill / Decode → Serving → Model API / Selection → Embedding / Reranker / Multimodal → Prompt / Factuality → Fine-tuning / Post-training",
        "signals": ["Prompt Engineering", "Transformer / Attention", "Model Selection", "Hallucination / Factuality", "Fine-tuning / Post-training", "Context / KV Cache / Serving"],
        "boundaries": [
            "HNSW / IVF / Vector Filter 归 Vector DB。",
            "Chunk / Hybrid / RRF / Retrieval Evaluation 归 RAG。",
            "Context Compaction / Memory / Tool Protocol 归 Agent Harness；Provider Retry 归 AIBE。",
        ],
        "parts": [(1, 4, "Part A｜模型输入与核心计算"), (5, 7, "Part B｜生成与 Serving"), (8, 10, "Part C｜应用模型能力"), (11, 14, "Part D｜行为、事实与适配边界")],
    },
    {
        "slug": "rag",
        "name": "RAG",
        "title": "RAG｜检索增强生成工程",
        "level": "AI Application",
        "role": "把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。",
        "blocks": 14,
        "canonical": 29,
        "sources": 88,
        "canonical_file": "rag.md",
        "mainline": "Corpus Governance → Document Processing → Chunk Design → Query Planning → Dense / Sparse / Hybrid / Fusion → Rerank / Candidate Budget → Evidence / Grounding / Citation → Retrieval & E2E Evaluation → Production Governance / Scale → GraphRAG / Agentic RAG",
        "signals": ["End-to-end Pipeline", "Chunk Strategy", "Hybrid Retrieval", "Reranking", "End-to-end Evaluation", "Bad Case Attribution", "Query Transformation"],
        "boundaries": [
            "Embedding / Reranker 内部原理归 LLM Foundation。",
            "ANN / HNSW / IVF / Filter 存储机制归 Vector DB。",
            "Agentic Retrieval 的控制循环归 Agent Harness；RAG 负责 Evidence Quality。",
        ],
        "parts": [(1, 3, "Part A｜Knowledge Ingestion"), (4, 5, "Part B｜Retrieval Unit"), (6, 9, "Part C｜Query → Candidate → Evidence"), (10, 11, "Part D｜Quality Engineering"), (12, 14, "Part E｜Production Governance 与 Advanced RAG")],
    },
    {
        "slug": "agent-harness",
        "name": "Agent Harness / Runtime",
        "title": "Agent Harness / Runtime｜Agent 执行系统",
        "level": "Agent Runtime",
        "role": "从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。",
        "blocks": 23,
        "canonical": 44,
        "sources": 166,
        "canonical_file": "agent-harness.md",
        "mainline": "Agent Boundary / Loop → Tool Runtime → Planning / Control → Context Assembly / Compaction → Memory / Session / Checkpoint → Permission / Sandbox / Injection → MCP / Skills / Hooks / Routing → Multi-Agent / A2A → Trace / Eval / Coding Agent → Production Runtime / Framework Mapping",
        "signals": ["Context Compaction", "Agent Loop", "Memory Architecture", "Tool Calling / Failure", "Multi-Agent", "Agent Evaluation", "Framework Selection"],
        "boundaries": [
            "Prompt Engineering 归 LLM Foundation；Harness 负责跨轮、跨 Tool、跨 State 的执行。",
            "RAG 负责 Evidence Quality；Agent Harness 决定何时检索、如何继续执行。",
            "通用 MQ / Retry / Idempotency 归 AIBE；Agent 只讲其 Runtime 特化语义。",
        ],
        "parts": [(1, 3, "Part A｜Agent 与 Runtime 基础"), (4, 7, "Part B｜Tool Runtime"), (8, 10, "Part C｜Planning 与 Context"), (11, 13, "Part D｜Memory、State 与 Long-running Reliability"), (14, 18, "Part E｜Security、Capability 与 Multi-Agent"), (19, 23, "Part F｜Observability、Evaluation 与 Production")],
        "source_index": "../research/agent-sources/README.md",
    },
    {
        "slug": "system-design",
        "name": "System Design",
        "title": "System Design｜AI Application / Agent Production 系统设计",
        "level": "Integration",
        "role": "把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。",
        "blocks": 19,
        "canonical": 24,
        "sources": 71,
        "canonical_file": "system-design.md",
        "mainline": "Requirement / SLO → Workload / Capacity → API / Data / State → Flow / Cache / Partition → Consistency / Queue → Reliability / Security → Observability / Evaluation / Cost / Evolution → High-concurrency / Realtime / Data Processing / LLM Gateway / Enterprise RAG / Production Agent Cases",
        "signals": ["Production / Long-running Agent Backend", "Flash Sale / Inventory", "Enterprise RAG", "Multi-tenant AI Platform", "Large-scale Data / Migration", "Vertical AI Agent Scenarios"],
        "boundaries": [
            "System Design 负责组合与决策，不重复单点机制的完整原理。",
            "Timeout / Retry / Queue / Backpressure 的机制归 AIBE。",
            "MySQL / Redis / Vector / RAG / Agent 的内部机制回到对应 Primary Module。",
        ],
        "parts": [(1, 12, "Part A｜通用 System Design 方法"), (13, 19, "Part B｜真人高频 Scenario Patterns")],
    },
]

MODULE_BY_SLUG = {m["slug"]: m for m in MODULES}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def module_link(m: dict, from_root: bool = True) -> str:
    path = f"{m['slug']}/README.md" if from_root else f"../{m['slug']}/README.md"
    return f"[{m['name']}]({path})"


def clean_label(label: str) -> str:
    label = re.sub(r"^\s*\d{1,2}[.、]\s*", "", label.strip())
    return label


def current_doc_labels(module: dict) -> dict[str, str]:
    readme = ROOT / module["slug"] / "README.md"
    labels: dict[str, str] = {}
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for label, target in re.findall(r"\[([^\]]+)\]\((docs/[^)#]+\.md)\)", text):
            labels[target] = clean_label(label)
    for p in sorted((ROOT / module["slug"] / "docs").glob("[0-9][0-9]-*.md")):
        rel = f"docs/{p.name}"
        if rel in labels:
            continue
        first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        first = re.sub(r"^\d{1,2}\s*[.、｜|-]\s*", "", first)
        labels[rel] = first
    return labels


def top_nav(i: int) -> str:
    bits = []
    if i > 0:
        prev = MODULES[i - 1]
        bits.append(f"[← {prev['name']}](../{prev['slug']}/README.md)")
    bits.append("[↑ Handbook 总目录](../README.md)")
    if i + 1 < len(MODULES):
        nxt = MODULES[i + 1]
        bits.append(f"[{nxt['name']} →](../{nxt['slug']}/README.md)")
    return " · ".join(bits)


def render_module(module: dict, i: int) -> str:
    labels = current_doc_labels(module)
    docs = sorted((ROOT / module["slug"] / "docs").glob("[0-9][0-9]-*.md"))
    if len(docs) != module["blocks"]:
        raise SystemExit(f"{module['slug']}: expected {module['blocks']} docs, got {len(docs)}")
    nums = [int(p.name[:2]) for p in docs]
    if nums != list(range(1, module["blocks"] + 1)):
        raise SystemExit(f"{module['slug']}: non-contiguous docs {nums}")

    chain = " → ".join(module_link(m, from_root=False) if m is not module else f"**{m['name']}**" for m in MODULES)
    chapter_by_num = {int(p.name[:2]): p for p in docs}
    catalog: list[str] = []
    for start, end, part in module["parts"]:
        catalog += [f"### {part}", ""]
        for n in range(start, end + 1):
            p = chapter_by_num[n]
            target = f"docs/{p.name}"
            label = labels.get(target, p.stem[3:])
            catalog.append(f"{n}. [{label}]({target})")
        catalog.append("")

    evidence = [
        f"- [Canonical Questions](../research/questions/{module['canonical_file']})：市场真实问法与 Source Count；",
        "- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；",
        "- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；",
    ]
    if module.get("source_index"):
        evidence.append(f"- [权威技术 / 源码资料索引]({module['source_index']})：只校准技术事实，不改变 HUMAN-A 频率；")
    evidence += [
        "- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；",
        "- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。",
    ]

    interviews = [
        "| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |",
        "| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |",
        "| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |",
        "| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |",
    ]
    for label, target in module.get("extra_interview", []):
        interviews.append(f"| {label} | [进入]({target}) | 额外专项训练 |")

    next_text = "整套十板块已学完，可以进入全局 Review / 面试训练。"
    if i + 1 < len(MODULES):
        nxt = MODULES[i + 1]
        next_text = f"下一环：[{nxt['name']}](../{nxt['slug']}/README.md)。"

    return f"""# {module['title']}

{top_nav(i)}

> **状态：✅ 第一版系统教材完成**  
> **教材：{module['blocks']} 个连续知识小板块** · **HUMAN-A Canonical：{module['canonical']}** · **独立来源覆盖：{module['sources']}**  
> **质量：Granularity / Coverage / Content Depth 已验收**

{module['role']}

---

## 1. 这个模块解决什么

{module['role']}

学习目标不是记住一组名词，而是能稳定回答：

```text
为什么需要它？
→ 核心机制怎样工作？
→ 正常路径怎样流动？
→ Failure / Trade-off 在哪里？
→ Production 场景怎样验证与排障？
→ 面试官继续追问时怎样解释边界？
```

---

## 2. 在十板块中的位置

{chain}

当前模块角色：**{module['level']} / {module['role']}**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **{module['canonical']} 道 Canonical → {module['blocks']} 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
{module['mainline']}
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

{chr(10).join(catalog).rstrip()}

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **{module['canonical']} 道 Primary Canonical、{module['sources']} 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

{chr(10).join('- ' + x for x in module['signals'])}

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

{chr(10).join('- ' + x for x in module['boundaries'])}

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
{chr(10).join(interviews)}

研究与质量证据：

{chr(10).join(evidence)}

---

## 9. 推荐学习方式

1. **第一遍：建立因果链。** 按 `docs/01 → {module['blocks']:02d}` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–{module['blocks']:02d} 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

{next_text}
"""


def render_root() -> str:
    table = ["| # | 一级模块 | 层级 | 一句话职责 | 教材 | Canonical | 状态 |", "|---:|---|---|---|---:|---:|---|"]
    for i, m in enumerate(MODULES, 1):
        table.append(f"| {i:02d} | [{m['name']}]({m['slug']}/README.md) | {m['level']} | {m['role']} | {m['blocks']} | {m['canonical']} | ✅ |")
    chain = " → ".join(module_link(m, True) for m in MODULES)
    return f"""# AI Application Interview Handbook

> 面向 **AI Application / AI Agent Engineer** 求职的一套 beginner-first 系统教材、真人面经研究库与面试训练体系。

> **当前状态：✅ 十个正式一级模块第一版教材全部完成** · **Phase 3 Curriculum Build ✅**  
> **研究基线：279 个 HUMAN-A 招聘流程（S001–S279，Frozen）** · **235 ACTIVE Canonical**

## 快速入口

[十板块知识地图](roadmap/knowledge-map.md) · [课程建设进度](research/questions/progress.md) · [真人面经研究库](research/README.md) · [Canonical Questions](research/questions/README.md) · [粒度审计](roadmap/curriculum-granularity-audit.md) · [深度审计](roadmap/content-depth-audit.md)

---

## 1. 这是什么项目

它不是“按面试题拼起来的八股仓库”。项目把三类信息严格分层：

```text
完整知识体系
→ 决定初学者 0→1 的课程主干

HUMAN-A 真人面经
→ 校准市场热度、真实问法、追问深度、Failure / Scale / Evaluation 强度

官方文档 / 规范 / 论文 / 成熟源码
→ 校准技术事实与 Production 工程边界
```

核心原则：**知识体系决定先学什么；真人面经决定哪些地方必须学深，但不能反过来打乱课程演进。**

---

## 2. 十个正式一级模块

{chr(10).join(table)}

### 正式学习顺序

{chain}

所有模块标题和名称都可以直接点击进入对应 README。

---

## 3. 每个模块现在都使用同一套结构

```text
README.md
├─ 模块职责 / 在十板块中的位置
├─ beginner-first 正式主线
├─ 正式章节目录
├─ HUMAN-A 如何影响复习深度
├─ 模块边界
├─ Review / Interview / Evidence 入口
└─ 完成状态与上一环 / 下一环导航

docs/
└─ 系统正文

review/
└─ 第二遍总图与综合自测

interview/
├─ 高频面试题
├─ 面试易错点
└─ 面试前速查表
```

Python 额外保留 Coding 小题；Agent / FastAPI / AIBE 还维护专门的权威资料或源码索引。

---

## 4. 为什么教材文件数和 Canonical 数不一样

```text
HUMAN-A / Canonical Question = 可独立追问的面试能力
Capability Primitive          = 更细的工程机制
教材 Markdown                 = 一个完整认知闭环
Section                       = 参数 / 变体 / Failure / 追问
```

因此不会默认 `1 Canonical = 1 Markdown`。当前 10 个模块共 **184 个正文知识块**，但研究层仍保持 **235 道 ACTIVE Canonical**。

详见：[Curriculum Granularity Audit](roadmap/curriculum-granularity-audit.md)。

---

## 5. 真人面经证据体系

正式市场证据只允许来自 **HUMAN-A：候选人本人第一人称、高信息密度、可核验的真实招聘流程**。

```text
Frozen HUMAN-A              279
ACTIVE Canonical            235
Mapped Sources              278
VALID-UNMAPPED                1（S271）
Unexpected uncovered          0
Source Count mismatch         0
```

源码、官方文章、规范和论文可以帮助我们补齐知识边界，但**不能创建面试频率，也不能提高 Source Count**。

入口：[Research Home](research/README.md) · [Market Analysis](research/analysis/README.md) · [Verified Follow-up Chains](research/analysis/follow-up-chains.md)

---

## 6. 统一学习方法

1. **正文第一遍：** 按模块和章节顺序建立完整因果链。
2. **Review 第二遍：** 从空白纸重新画机制 / 数据流 / Failure，而不是重新抄正文。
3. **Interview 第三遍：** 练真实问法、30 秒回答、深挖与易错边界。
4. **项目复盘：** 把自己的项目沿 `为什么 → 机制 → Trade-off → Failure → Scale → Verification` 重新讲一遍。

正式教材统一追求：

> **定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

## 7. 项目质量与维护入口

| 文档 | 作用 |
|---|---|
| [Knowledge Map](roadmap/knowledge-map.md) | 十板块职责、主线与依赖关系 |
| [Documentation Style Guide](roadmap/documentation-style-guide.md) | README / 描述文件统一规范 |
| [Granularity Audit](roadmap/curriculum-granularity-audit.md) | 研究粒度与教材粒度为什么分开 |
| [Content Depth Audit](roadmap/content-depth-audit.md) | 正文深度与完成状态 |
| [Foundation Status](roadmap/foundation-status-audit.md) | Python / FastAPI / AIBE 完成状态 |
| [Progress](research/questions/progress.md) | Phase 1–3 当前正式状态 |
| [Module Index](research/questions/module-index.md) | Canonical Ownership ↔ Curriculum 映射 |

---

## 8. 仓库目录

```text
python/              FastAPI/             backend-engineering/
mysql/               redis/               vector-db/
llm-foundation/      rag/                 agent-harness/
system-design/

research/            # HUMAN-A / Canonical / Analysis / Source Index
roadmap/             # Knowledge Map / Audits / Documentation Rules
tools/               # Research validation / reproducible analysis
```

> 仓库最新 README、Knowledge Map、Progress 与 Module Index 是当前状态的正式来源；历史聊天和旧摘要不能覆盖仓库当前描述。
"""


def render_knowledge_map() -> str:
    lines = [
        "# AI Application Engineer｜十板块知识地图",
        "",
        "[← Handbook 总目录](../README.md) · [课程进度](../research/questions/progress.md) · [Canonical Index](../research/questions/module-index.md)",
        "",
        "> 十个一级模块已经全部完成第一版系统教材。这里强调**模块职责、知识依赖与边界**；章节细节进入各模块 README。",
        "",
        "## 总路线",
        "",
        " → ".join(f"[{m['name']}](../{m['slug']}/README.md)" for m in MODULES),
        "",
        "## 总览",
        "",
        "| # | 模块 | Blocks | Canonical | 核心角色 |",
        "|---:|---|---:|---:|---|",
    ]
    for i, m in enumerate(MODULES, 1):
        lines.append(f"| {i:02d} | [{m['name']}](../{m['slug']}/README.md) | {m['blocks']} | {m['canonical']} | {m['role']} |")
    lines += ["", "---", ""]
    for i, m in enumerate(MODULES, 1):
        lines += [
            f"## {i:02d}. [{m['name']}](../{m['slug']}/README.md) ✅ — {m['blocks']} blocks",
            "",
            m["role"],
            "",
            "```text",
            m["mainline"],
            "```",
            "",
            f"市场校准：**{m['canonical']} Canonical / {m['sources']} independent HUMAN-A flows**。",
            "",
        ]
    lines += [
        "---", "", "## 使用规则", "",
        "- 学习顺序由知识依赖决定，不按面经频率重排；",
        "- 真人面经只调整复习权重、真实问法和追问深度；",
        "- 跨模块问题只在 Primary Module 维护完整机制；",
        "- 章节数是认知闭环的结果，不是统一 KPI；",
        "- 当前粒度与深度状态见 [Granularity Audit](curriculum-granularity-audit.md) 与 [Content Depth Audit](content-depth-audit.md)。",
    ]
    return "\n".join(lines)


def render_foundation_status() -> str:
    return """# Foundation｜状态与质量审计

[← Handbook 总目录](../README.md) · [十板块知识地图](knowledge-map.md) · [Content Depth Audit](content-depth-audit.md)

> **当前状态：✅ Foundation COMPLETE。** Python、FastAPI、AI Backend Engineering 均已具备正式正文、Review、Interview 与 Canonical Coverage / Depth 验收。

| 模块 | Curriculum | Canonical | 状态 | 入口 |
|---|---:|---:|---|---|
| Python Foundation | 13 | 15 | ✅ | [README](../python/README.md) |
| FastAPI | 16 | 4 | ✅ | [README](../fastapi/README.md) |
| AI Backend Engineering | 22 | 39 | ✅ | [README](../backend-engineering/README.md) |

## 正式学习顺序

[Python Foundation](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md)

```text
Python
= 语言 / 对象 / Runtime / 并发基础

FastAPI
= Python Runtime → HTTP / ASGI AI Service

AI Backend Engineering
= Service → Production Reliability / Messaging / Consistency / Operations
```

## 统一完成标准

三块均满足：

```text
docs/ 连续知识块
+ Review
+ Interview
+ Canonical Coverage
+ Granularity / Content Depth Review
```

真人面经只校准重点；完整 Foundation 骨架仍按 `语言 → 服务框架 → Production Backend` 演进。
"""


def render_granularity() -> str:
    lines = [
        "# Curriculum Granularity Audit｜教材粒度最终口径",
        "",
        "[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Content Depth Audit](content-depth-audit.md)",
        "",
        "> 研究粒度、能力粒度、教材文件粒度不是同一个层级。**Canonical 可以很细，但一个 Markdown 应形成完整认知闭环。**",
        "",
        "## 固定规则", "",
        "```text",
        "HUMAN-A / Canonical Question = 面试最小可独立追问单元",
        "Capability Primitive          = 工程机制最小单元",
        "教材 Markdown                 = 可独立学习 / 画图 / 解释 Failure & Trade-off 的知识块",
        "Section                       = 参数 / 变体 / Failure / 深挖追问",
        "```", "",
        "独立成文件时，主题应能回答一个完整大问题，并拥有自己的机制、Failure Model / Trade-off 和验证闭环。",
        "", "## 当前最终结构", "",
        "| 模块 | 研究 / 历史输入 | 当前 Curriculum | 状态 |",
        "|---|---|---:|---|",
        "| Python | 12-block v1 / 15 Canonical | 13 | ✅ |",
        "| FastAPI | ~40 outline topics / 4 Canonical | 16 | ✅ |",
        "| AI Backend Engineering | ~55 outline topics / 39 Canonical | 22 | ✅ |",
        "| MySQL | 26 Canonical | 23 | ✅ |",
        "| Redis | 27 old blocks / 19 Canonical | 24 | ✅ |",
        "| Vector DB | 23 old blocks / 12 Canonical | 16 | ✅ |",
        "| LLM Foundation | 29 old blocks / 23 Canonical | 14 | ✅ |",
        "| RAG | 34 old blocks / 29 Canonical | 14 | ✅ |",
        "| Agent Harness | 47 old blocks / 44 Canonical | 23 | ✅ |",
        "| System Design | 24 Scenario Canonical | 19 | ✅ |",
        "", "这些数字是结果，不是目标。教材重组永远不能改变 HUMAN-A、Source Count、Primary Ownership 或 Verified Follow-up Chain。",
    ]
    return "\n".join(lines)


def render_depth() -> str:
    total = sum(m["blocks"] for m in MODULES)
    lines = [
        "# Curriculum Content Depth Audit｜正文深度最终口径",
        "",
        "[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Granularity Audit](curriculum-granularity-audit.md)",
        "",
        "> 当前十个一级模块共 **%d 个正文知识块**。本文件统一记录完成状态；文件大小只用于发现异常，不作为质量结论。" % total,
        "", "## 验收标准", "",
        "一个知识块应覆盖其主题所需要的大部分：",
        "", "```text",
        "为什么需要",
        "→ 准确定义 / Mental Model",
        "→ 机制 / 数据流 / 算法",
        "→ Failure / Trade-off",
        "→ Production / AI Application 场景",
        "→ 模块边界",
        "→ 面试表达 / 易错点 / 深挖",
        "→ 折叠自测",
        "```", "",
        "窄主题可以较短；大型 Production 子系统如果只有概览则不能通过。",
        "", "## 当前状态", "",
        "| 模块 | Blocks | Numbering | Quality Status |",
        "|---|---:|---|---|",
    ]
    for m in MODULES:
        lines.append(f"| [{m['name']}](../{m['slug']}/README.md) | {m['blocks']} | ✅ `01–{m['blocks']:02d}` | ✅ PASS |")
    lines += [
        "", f"**当前正文总量：{total} blocks。**", "",
        "## 验收历史说明", "",
        "- Python：保留 v1 主干后做 Canonical Coverage / Depth Remediation；",
        "- FastAPI / AIBE / System Design：首版即按当前粒度和深度标准建设；",
        "- Redis / Vector DB / LLM / RAG：完成旧结构颗粒度整改后重新做深度复核；",
        "- MySQL：原 23-block 结构本身健康，机制与 correctness 边界审阅通过；",
        "- Agent Harness：47→23 后对旧短稿区域做第二轮深写与源码 / 官方证据验收。",
        "", "## 后续规则", "",
        "```text",
        "先定认知闭环 → 写正文 → QA 找异常 → 人工复核 → 再标记完成",
        "```",
        "", "自动检查只负责发现异常，不能代替人工判断。",
    ]
    return "\n".join(lines)


def render_integration_status() -> str:
    return """# Repository Integration Status｜当前仓库整合状态

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Progress](../research/questions/progress.md)

> **状态：✅ 十个一级模块已完成整合与第一版系统教材建设。** 本文件不再作为“Python 迁移进度”日志，而记录当前仓库的一体化状态。

## 当前十板块

[Python](../python/README.md) → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector DB](../vector-db/README.md) → [LLM Foundation](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent Harness / Runtime](../agent-harness/README.md) → [System Design](../system-design/README.md)

## Integration 已完成的内容

- 原独立 Python Handbook 已迁入并升级为 13-block Foundation；
- FastAPI 与 AI Backend Engineering 已从课程骨架补成正式教材；
- Data / LLM / RAG / Agent 模块完成粒度与深度统一；
- System Design 作为最终 Integration 模块完成；
- 279 个 HUMAN-A 与 235 Canonical 的研究层保持独立，不因教材重组改变；
- README / Knowledge Map / Progress / Module Index 使用统一状态口径。

历史 Python 独立仓库可以继续作为历史版本，但本仓库是当前 AI Application Interview Handbook 的主维护入口。
"""


def render_pr_summary() -> str:
    return """# Repository Integration Summary

[← Handbook 总目录](../README.md) · [Current Integration Status](integration-status.md) · [Knowledge Map](knowledge-map.md)

> 这个路径最初用于 Python / FastAPI / Backend 的整合 PR 摘要。当前整合已经完成，因此这里只保留一个**当前事实入口**，不再维护历史 PR 过程状态。

当前结果：

- 十个一级模块第一版教材 ✅；
- Foundation（Python / FastAPI / AIBE）✅；
- 课程粒度与正文深度审计 ✅；
- HUMAN-A `S001–S279` / 235 Canonical Frozen 基线保持不变；
- 当前状态以 [根 README](../README.md)、[Knowledge Map](knowledge-map.md) 与 [Progress](../research/questions/progress.md) 为准。
"""


def render_progress() -> str:
    rows = ["| # | Module | Curriculum | Canonical | Status |", "|---:|---|---:|---:|---|"]
    for i, m in enumerate(MODULES, 1):
        rows.append(f"| {i:02d} | [{m['name']}](../../{m['slug']}/README.md) | {m['blocks']} | {m['canonical']} | ✅ |")
    return f"""# Curriculum & Research Progress｜当前正式状态

[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Knowledge Map](../../roadmap/knowledge-map.md)

> **Repository-first：仓库当前文件高于历史聊天总结。**

## Frozen Research Baseline ✅

```text
HUMAN-A                    279 / 279
ACTIVE Canonical          235 / 235
Mapped Sources            278
VALID-UNMAPPED              1（S271）
Unexpected uncovered        0
Source Count mismatch       0
```

Phase 1 Canonicalization ✅ · Phase 2A Global Merge/Split ✅ · Phase 2B Market Analysis ✅

## Phase 3 Curriculum Build ✅

{chr(10).join(rows)}

十个正式一级模块第一版系统教材全部完成；Foundation 也已完成。

## 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

> **Canonical / Capability / Curriculum Markdown 使用不同粒度。**

## 模块完成后的强制同步清单

每次新增、重组或更新一个一级模块，都必须同步核验：

1. 模块 `README.md`；
2. 模块 `review/README.md` 与 Interview 入口；
3. 根 `README.md`；
4. `roadmap/knowledge-map.md`；
5. 本文件与 `module-index.md`；
6. `research/questions/README.md`；
7. 自动生成 `research/analysis/README.md` 的生成源；
8. `roadmap/documentation-style-guide.md` 的统一格式；
9. README 本地链接、章节数量与旧状态描述。

后续工作进入**全仓库质量维护、复习路线与面试训练**，不再存在未撰写的一级模块。
"""


def render_module_index() -> str:
    lines = [
        "# Canonical Ownership & Curriculum Module Index",
        "",
        "[← Canonical Questions](README.md) · [↑ Handbook 总目录](../../README.md) · [Progress](progress.md)",
        "",
        "> Canonical 数量描述面试能力粒度；Curriculum Blocks 描述教材认知闭环，两者不会机械相等。",
        "",
        "| # | Module | Canonical File | ACTIVE | Curriculum | Curriculum Entry | Status |",
        "|---:|---|---|---:|---:|---|---|",
    ]
    moved = {"python": 0, "fastapi": 1, "backend-engineering": 0, "mysql": 2, "redis": 5, "vector-db": 11, "llm-foundation": 0, "rag": 1, "agent-harness": 4, "system-design": 0}
    for i, m in enumerate(MODULES, 1):
        lines.append(f"| {i:02d} | {m['name']} | [{m['canonical_file']}]({m['canonical_file']}) | {m['canonical']} | {m['blocks']} | [README](../../{m['slug']}/README.md) | ✅ |")
    lines += [
        "", "**ACTIVE total = 235. Legacy MOVED = 24.**", "",
        "## 主要 Ownership 边界", "",
        "- FastAPI async Runtime 本体 → Python；",
        "- DB + Cache 一致性 / 通用 Rate Limit / Retry / MQ → AI Backend Engineering；",
        "- Dense / Sparse / Hybrid / RRF / Rerank / Retrieval Eval → RAG；",
        "- Embedding / Reranker 模型内部原理 → LLM Foundation；",
        "- Agent Tool / Context / Memory / Checkpoint → Agent Harness；",
        "- 端到端组合与 Scenario Trade-off → System Design。",
        "", "## 研究事实不随教材重组改变", "",
        "HUMAN-A、Source Count、Primary Ownership、Verified Follow-up Chain 与 Frequency Ranking 均保持 Frozen Research 层独立维护。",
    ]
    return "\n".join(lines)


def render_questions_readme() -> str:
    rows = ["| Module | Canonical | Curriculum | Entry |", "|---|---:|---:|---|"]
    for m in MODULES:
        rows.append(f"| [{m['name']}]({m['canonical_file']}) | {m['canonical']} | {m['blocks']} | [教材 README](../../{m['slug']}/README.md) |")
    return f"""# Canonical Questions｜真人面试能力归一化层

[← Research 首页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Module Index](module-index.md) · [Progress](progress.md)

> Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据。官方资料、源码、论文可以校准课程技术边界，但不能创建频率或提高 Source Count。

## Frozen Baseline

```text
HUMAN-A            S001–S279
ACTIVE Canonical   235
Mapped Sources     278
VALID-UNMAPPED       1（S271）
```

## 十板块 Ownership

{chr(10).join(rows)}

## 四种粒度

```text
Canonical Question = 面试最小独立追问单元
Capability         = 更细工程机制
Curriculum Block   = 完整教材认知闭环
Interview Drill    = 训练时可以再次细分的真实问法
```

因此 235 道 Canonical 不等于 184 篇正文。

## 主要入口

- [schema.md](schema.md)：Canonical 字段与证据规则；
- [module-index.md](module-index.md)：Ownership ↔ Curriculum；
- [progress.md](progress.md)：当前研究 / 教材状态；
- [global-audit.md](global-audit.md)：Merge / Split / Reassignment；
- [Market Analysis](../analysis/README.md)：自动统计层；
- [Verified Follow-up Chains](../analysis/follow-up-chains.md)：人工回读原始流程后的追问链。
"""


def render_research_readme() -> str:
    return """# Research｜2026 AI Application / Agent 真人面经研究库

[↑ Handbook 总目录](../README.md) · [Canonical Questions](questions/README.md) · [Market Analysis](analysis/README.md) · [Curriculum Knowledge Map](../roadmap/knowledge-map.md)

> **状态：✅ Frozen。** 当前研究基线为 `S001–S279` 共 279 个 HUMAN-A 独立招聘流程；主动采集已暂停。

## 1. 研究目的

这里不是“网上见过什么题就都收”的题库，而是回答：

```text
真实 AI Application / Agent 岗位在问什么？
→ 哪些能力反复出现？
→ 一道题会追到多深？
→ 项目怎样被验证？
→ Failure / Scale / Coding / System Design 怎样进入真实面试？
```

课程关系固定为：

> **完整知识体系决定应该学什么；HUMAN-A 面经告诉我们市场怎么问、问多深。**

## 2. 当前冻结基线

| 项目 | 当前值 |
|---|---:|
| HUMAN-A 来源 | 279 |
| Source IDs | `S001–S279` |
| 正式 Batch | 26 |
| ACTIVE Canonical | 235 |
| Mapped Sources | 278 |
| VALID-UNMAPPED | 1（S271） |
| 主动采集 | Frozen |

## 3. HUMAN-A Gate

正式来源必须满足：

```text
候选人本人第一人称
+ 真实招聘流程 / 面试官痕迹
+ 高信息密度
+ 目标 AI Application / Agent Role Scope
+ 正文稳定可核验
+ 非转载 / 非答案帖 / 非重复
```

详细规则：

- [Source Quality Policy](quality/source-quality-policy.md)
- [Role Scope Policy](quality/role-scope-policy.md)

## 4. 去重原则

任何未来新增必须先直接回读全历史，并同时检查 URL、作者、公司、岗位、日期/轮次、项目语义、连续题序与复制链。Search / Code Search 的“0 命中”不能证明未收录。

同一候选人、同一公司、同一招聘流程的多轮面试合并为一个 `Sxxx`；不同候选人的独立流程即使问到同样问题，仍分别计数。

## 5. 目录

```text
research/
├── interviews/          # S001–S279 原始 HUMAN-A 研究记录
├── quality/             # Source / Role Scope Gate
├── monitoring/          # 若未来重开采集时的 Inbox
├── questions/           # 235 Canonical Ownership
├── analysis/            # Frequency / Coverage / Follow-up / Gap
├── agent-sources/       # Agent 源码 + 官方资料证据层
├── fastapi-sources/     # FastAPI 官方资料
└── backend-sources/     # Backend Engineering 权威资料
```

## 6. 研究与教材的边界

- HUMAN-A → 市场频率 / 真实问法 / 追问深度；
- 官方资料 / 源码 → 技术事实 / Production 边界；
- Curriculum → beginner-first 的完整知识演进。

研究层永远不能因为教材 Merge / Rename 而修改 Source Count。

## 7. 如果未来重开采集

从保留编号 `S280` 开始，但必须先读取本 README、质量规则、Inbox 和 `batch-01.md`～`batch-26.md` 全历史，再重新执行同样的 HUMAN-A / 去重 Gate。
"""


def standardize_review(module: dict) -> None:
    path = ROOT / module["slug"] / "review" / "README.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Drop old first heading only; preserve the review body and diagrams.
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    body = "\n".join(lines).lstrip()
    prefix = f"""# {module['name']}｜Review 与综合自测

[← 模块主页](../README.md) · [↑ Handbook 总目录](../../README.md) · [高频面试题 →](../interview/高频面试题.md)

> **用途：第二遍复习。** Review 不负责重新复制正文，而是要求从空白纸重建主线、机制、Failure / Trade-off 与面试表达。

---

"""
    write(path, prefix + body)


def prepend_standard(path: Path, title: str, nav: str, status: str) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    body = "\n".join(lines).lstrip()
    write(path, f"# {title}\n\n{nav}\n\n> {status}\n\n---\n\n{body}")


def update_market_builder() -> None:
    path = ROOT / "tools" / "build_market_analysis.py"
    text = path.read_text(encoding="utf-8")
    old = '''    summary_lines = [\n        "# Phase 2B Market Analysis Summary",\n        "",\n        "更新日期：2026-09-11",\n        "",\n        "> 自动统计层。这里不做课程知识补全，只描述冻结真人面经数据本身。",\n'''
    new = '''    summary_lines = [\n        "# Research Analysis｜Phase 2B Market Analysis",\n        "",\n        "[← Research 首页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Canonical Questions →](../questions/README.md)",\n        "",\n        "> **状态：✅ Frozen Analysis。** 自动统计层只描述冻结 HUMAN-A 市场数据，不承担课程知识补全，也不维护易过期的 Curriculum 下一步状态。",\n        "",\n        "更新日期：2026-09-11",\n'''
    if old in text:
        text = text.replace(old, new, 1)
    elif "# Research Analysis｜Phase 2B Market Analysis" not in text:
        raise SystemExit("market builder summary header anchor changed")
    old_footer = '''        "下一步人工研究层：基于 `cooccurrence.md` 回到原始 Batch 核验真正的 Follow-up Chain，并将 `curriculum-evidence-matrix.md` 与最新 `roadmap/knowledge-map.md` 对照，形成 Knowledge Gap Analysis。",\n'''
    new_footer = '''        "Phase 2B 自动统计与人工核验层均已完成。Curriculum 的实时状态以 `research/questions/progress.md` 与 `roadmap/knowledge-map.md` 为准；本自动生成 README 不重复维护课程状态。",\n'''
    if old_footer in text:
        text = text.replace(old_footer, new_footer, 1)
    elif "本自动生成 README 不重复维护课程状态" not in text:
        raise SystemExit("market builder footer anchor changed")
    write(path, text)
    subprocess.run(["python", str(path)], cwd=ROOT, check=True)


def render_doc_style() -> str:
    return """# Documentation Style Guide｜README 与状态描述规范

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Progress](../research/questions/progress.md)

> 目标：让任何人打开任意一级模块或核心状态页，都能使用同一种信息架构理解“这是什么、现在是什么状态、从哪里来、接下来去哪里”。

## 一级模块 README 固定结构

```text
# Module｜一句话角色
上一模块 · Handbook 总目录 · 下一模块
状态 / Blocks / Canonical / Source Coverage

1. 这个模块解决什么
2. 在十板块中的位置
3. 固定课程原则
4. 正式学习主线
5. 正式课程目录
6. HUMAN-A 怎样影响本模块
7. 模块边界
8. Review / Interview / Evidence 入口
9. 推荐学习方式
10. 完成状态
```

## Review README 固定结构

- 顶部必须能返回模块主页和 Handbook；
- 明确它属于第二遍复习，不重复正文；
- 自测答案默认使用 `<details>` 折叠；
- 图解优先使用保守 GitHub Mermaid。

## 根 README / Knowledge Map

- 十个一级模块名称必须直接可点击；
- 所有模块使用同一列信息：角色、Blocks、Canonical、状态；
- 不在根 README 对某个模块展开数倍于其它模块的细节；
- 详细内容进入模块 README。

## 状态源优先级

```text
当前仓库文件
> Progress / Knowledge Map / Module README
> 历史审计记录
> 聊天摘要 / 旧 PR 描述
```

## 同步规则

模块状态改变时，至少核验：根 README、模块 README、Review README、Knowledge Map、Progress、Module Index、Canonical README、自动生成 Analysis README 的生成源，以及本地 Markdown 链接。
"""


def update_description_headers() -> None:
    # Current-state roadmap docs are fully rewritten where stale history was misleading.
    write(ROOT / "roadmap" / "knowledge-map.md", render_knowledge_map())
    write(ROOT / "roadmap" / "foundation-status-audit.md", render_foundation_status())
    write(ROOT / "roadmap" / "curriculum-granularity-audit.md", render_granularity())
    write(ROOT / "roadmap" / "content-depth-audit.md", render_depth())
    write(ROOT / "roadmap" / "integration-status.md", render_integration_status())
    write(ROOT / "roadmap" / "pr-summary.md", render_pr_summary())
    write(ROOT / "roadmap" / "documentation-style-guide.md", render_doc_style())

    # Source strategy doc is not rewritten; only receive consistent navigation/status header.
    prepend_standard(
        ROOT / "roadmap" / "agent-authoritative-sources.md",
        "Agent Harness｜Authoritative Source Strategy",
        "[← Agent Harness](../agent-harness/README.md) · [↑ Handbook 总目录](../README.md) · [Agent Source Index](../research/agent-sources/README.md)",
        "**用途：技术证据策略。** HUMAN-A 决定市场频率；源码 / 官方资料只补成熟 Runtime 事实与工程边界。",
    )


def update_research_readmes() -> None:
    write(ROOT / "research" / "README.md", render_research_readme())
    write(ROOT / "research" / "questions" / "README.md", render_questions_readme())
    write(ROOT / "research" / "questions" / "progress.md", render_progress())
    write(ROOT / "research" / "questions" / "module-index.md", render_module_index())

    prepend_standard(
        ROOT / "research" / "agent-sources" / "README.md",
        "Agent Harness｜源码与权威资料索引",
        "[← Agent Harness](../../agent-harness/README.md) · [↑ Handbook 总目录](../../README.md) · [Research 首页](../README.md)",
        "**用途：Tier B/C 技术证据。** 只补 Runtime 实现与工程原则，不改变 HUMAN-A Source Count。",
    )
    prepend_standard(
        ROOT / "research" / "fastapi-sources" / "README.md",
        "FastAPI｜官方技术资料索引",
        "[← FastAPI](../../fastapi/README.md) · [↑ Handbook 总目录](../../README.md) · [Research 首页](../README.md)",
        "**用途：技术事实校准。** 官方资料只说明当前框架机制，不改变 HUMAN-A 面试频率。",
    )
    prepend_standard(
        ROOT / "research" / "backend-sources" / "README.md",
        "AI Backend Engineering｜权威工程资料索引",
        "[← AI Backend Engineering](../../backend-engineering/README.md) · [↑ Handbook 总目录](../../README.md) · [Research 首页](../README.md)",
        "**用途：Production Engineering 技术事实校准。** Google SRE / AWS / Kafka / K8s / OTel / OAuth / OWASP 等不计入 HUMAN-A Source Count。",
    )


def validate_local_links(paths: list[Path]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    errors = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for raw in link_re.findall(text):
            target = raw.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target)
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {raw}")
    if errors:
        raise SystemExit("broken local links:\n" + "\n".join(errors[:80]))


def main() -> None:
    # 1. Render module READMEs while old labels are still available.
    rendered = [(ROOT / m["slug"] / "README.md", render_module(m, i)) for i, m in enumerate(MODULES)]
    for path, text in rendered:
        write(path, text)

    # 2. Root and Review layer.
    write(ROOT / "README.md", render_root())
    for m in MODULES:
        standardize_review(m)

    # 3. Roadmap / research description system.
    update_description_headers()
    update_research_readmes()

    # 4. Fix auto-generated analysis README at its source and regenerate.
    update_market_builder()

    # 5. Validate actual README inventory and local links.
    all_readmes = sorted(ROOT.rglob("README.md"))
    expected = {
        Path("README.md"),
        *[Path(m["slug"]) / "README.md" for m in MODULES],
        *[Path(m["slug"]) / "review" / "README.md" for m in MODULES],
        Path("research/README.md"),
        Path("research/questions/README.md"),
        Path("research/analysis/README.md"),
        Path("research/agent-sources/README.md"),
        Path("research/fastapi-sources/README.md"),
        Path("research/backend-sources/README.md"),
    }
    actual = {p.relative_to(ROOT) for p in all_readmes}
    missing = expected - actual
    if missing:
        raise SystemExit(f"expected README missing: {sorted(map(str, missing))}")

    # Every non-root README should offer a route back to the project entrypoint.
    for p in all_readmes:
        rel = p.relative_to(ROOT)
        if rel == Path("README.md"):
            continue
        head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:12])
        if "Handbook 总目录" not in head and "Research 首页" not in head and "模块主页" not in head:
            raise SystemExit(f"README missing standard navigation near top: {rel}")

    description_paths = [
        ROOT / "roadmap" / "knowledge-map.md",
        ROOT / "roadmap" / "foundation-status-audit.md",
        ROOT / "roadmap" / "curriculum-granularity-audit.md",
        ROOT / "roadmap" / "content-depth-audit.md",
        ROOT / "roadmap" / "integration-status.md",
        ROOT / "roadmap" / "pr-summary.md",
        ROOT / "roadmap" / "documentation-style-guide.md",
        ROOT / "roadmap" / "agent-authoritative-sources.md",
        ROOT / "research" / "questions" / "progress.md",
        ROOT / "research" / "questions" / "module-index.md",
    ]
    validate_local_links(all_readmes + description_paths)

    # Current-state wording guard.
    current_docs = [ROOT / "README.md", ROOT / "roadmap" / "knowledge-map.md", ROOT / "roadmap" / "foundation-status-audit.md", ROOT / "research" / "questions" / "progress.md"]
    forbidden = ["正式正文未写", "只有 README 课程骨架", "Foundation 当前唯一正式教材缺口"]
    for p in current_docs:
        text = p.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                raise SystemExit(f"stale current-state wording in {p}: {phrase}")

    print(f"README system unified: {len(all_readmes)} README files; {sum(m['blocks'] for m in MODULES)} curriculum docs indexed.")


if __name__ == "__main__":
    main()
