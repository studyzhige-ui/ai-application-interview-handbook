# Verified Interview Follow-up Chains

更新日期：2026-09-11

> 本文件是 Phase 2B 的**人工核验层**。`cooccurrence.md` 只能证明两道 Canonical 出现在同一独立 HUMAN-A 招聘流程中，不能证明顺序。这里重新回到原始 `batch-xx.md`，只记录能够从真实问题顺序中确认的递进关系。
>
> 这里的 “Chain” 不是宣称面试官必然按固定脚本提问，而是：在多个独立真实流程中，面试经常从一个较宽的问题继续追到下一层机制、失败模式、指标或 Production 约束。

## 1. 置信等级

- **A · Strong recurring chain**：至少 3 个独立 HUMAN-A 流程出现相同方向的明显递进。
- **B · Recurring chain**：至少 2 个独立 HUMAN-A 流程出现相同方向。
- **C · Strong single-flow exemplar**：单个流程追问链极完整，但暂不把它推广成普遍模式。

课程使用原则：A/B 可直接影响章节内部顺序；C 更适合作为综合 Case / Interview Drill。

---

## 2. RAG：完整链路 → Chunk → Retrieval → Rerank → Evaluation / Bad Case

**置信：A**

```text
RAG 为什么存在 / 完整 Pipeline
        ↓
Document / Chunk 怎么做
        ↓
Dense / Sparse / Hybrid Retrieval
        ↓
Rerank / Top-K
        ↓
Evaluation
        ↓
Bad Case 到底坏在哪一层
```

### 原始流程证据

- `S081`（batch-05）：先问 RAG 父子索引，再追 `BM25 + Vector + Rerank`，随后继续问 Knowledge Base 更新与旧索引 / 缓存失效。
- `S249`（batch-21）：Jira RAG → Hybrid Retrieval → 固定 / 长文 Chunk → Rerank；面试官继续追“加 Rerank 后反而变差怎么办”以及 Query Rewrite。
- `S253`（batch-21）：二面从跨页表格解析 → RAGAS Attribution → Chunk Overlap → GraphRAG Noise Filtering，明确把数据处理、检索和评测放在一条失败归因链中。
- `S236`（batch-18）虽然是 Coding Agent 场景，也从 Retrieval / Context 协同继续追到 Benchmark 与错误 Patch 的验证，说明 RAG 不会只停留在“会搭 Pipeline”。

### 对 Canonical 的对应

`RAG-002` → `RAG-006/007/008` → `RAG-012/013/014` → `RAG-015/016` → `RAG-020/021` → `RAG-019`

### 教材含义

RAG 不应按“组件名词百科”编排。每个 Retrieval 章节都应该带一个验证闭环：**为什么这样切 / 这样召回 → 指标如何证明 → 变差时如何归因**。

---

## 3. Agent：边界 / Harness → Loop → Tool / Skill → Context / Memory → Failure / Evaluation

**置信：A**

```text
为什么这里需要 Agent？
        ↓
Harness / Runtime 为什么需要独立存在？
        ↓
Agent Loop / Planning 怎么跑？
        ↓
Tool / Skill / MCP 怎样接入？
        ↓
Context / Memory 怎样组织？
        ↓
失败、循环、重试怎样恢复？
        ↓
怎样证明 Agent 真的变好？
```

### 原始流程证据

- `S214`（batch-14）：Agent 与 Claude Code / Codex 的差异 → Harness Layer → Built-in Tool → Tool / Skill 边界 → Skill 按需加载 → 三层 Memory → Context Assembly → Compression / Checkpoint；二面继续追 Agent Evaluation。
- `S236`（batch-18）：Coding Agent 完整链路 → 多模型 Adapter → Tool Lifecycle → Tool Failure → Context 增长 / Compression → Memory 污染 → Harness → Benchmark → Patch Verification。
- `S085`（batch-05）：为什么做 Coding Agent → Context / Prompt / Harness 区分 → Tool Layer → Memory → Hallucination → ReAct → Dead Loop → Permission / Retry → Production Agent Components。
- `S077`（batch-05）：Agent Tool 数量增长 → Evaluation → Dynamic Tool Registry → Tool Retrieval / Lazy Loading → Tool Unavailable Fallback → Schema / Version / Permission → Multi-Agent。

### 对 Canonical 的对应

`AGENT-001/002` → `AGENT-003/005` → `AGENT-018/023/024` → `AGENT-008/009/014` → `AGENT-006/020/027/038` → `AGENT-034/035`

### 教材含义

Agent Harness 章节必须从**控制循环**出发，而不是从 LangChain API 出发；并且正常路径后面紧跟 Runtime Failure 与 Evaluation。

---

## 4. Context：Assembly → Compaction → Correctness → Memory Pollution → Resume

**置信：A**

```text
一次请求到底塞了什么？
        ↓
Context 为什么会膨胀？
        ↓
Trim / Summary / Compaction 怎么做？
        ↓
压缩后如何证明关键约束没丢？
        ↓
错误 Summary / Memory 怎样污染后续执行？
        ↓
Checkpoint / Session Resume 怎样恢复？
```

### 原始流程证据

- `S107`（batch-06）：Prompt / Context 组成 → 三层 Context Compression → 触发条件 → 如何发现压缩过度 → Session 恢复；二面继续追 Memory Growth、Recall 与 Token Cost。
- `S214`（batch-14）：Memory 分层 → Agent Loop Context 拼装顺序 → Compression → Checkpoint → 保留初始 Goal / Constraint → Tool Failure。
- `S219`（batch-15）：多级 Compression → System Prompt / Memory / History / Tool Result 的排列 → Tool Result 回填位置 → Long-term Memory 重新注入位置。
- `S236`（batch-18）：Context Compression → Task/File Summary → 关键约束丢失 → 过时 File Summary → 错误结论写入 Memory → 后续污染。

### 对 Canonical 的对应

`AGENT-008` → `AGENT-009` → `AGENT-010/011` → `AGENT-014/015` → `AGENT-027/029`

### 教材含义

Context Engineering 应被教授成 **Runtime Data Structure + State Correctness**，而不是“Token 超了就 Summary”。

---

## 5. Tool 能力规模化：Lifecycle → Discovery → Failure → Permission / Sandbox

**置信：A**

```text
Tool 怎样定义和调用？
        ↓
Tool 多了以后怎样发现正确能力？
        ↓
Schema / Version / Metadata 怎样管理？
        ↓
Tool 不可用 / 参数错误怎么办？
        ↓
哪些 Tool 必须权限、确认或 Sandbox？
```

### 原始流程证据

- `S077`（batch-05）：Dynamic Tool Registry → Tool >100 后 Discovery / Lazy Loading → Tool 不可用时 Fallback → Schema / Metadata / Version / Permission。
- `S214`（batch-14）：Built-in Tool → Tool / Skill → Skill Progressive Loading → 每轮选择 Skill → Tool Failure → 重复失败 Tool 的限次 / 改路 / 终止。
- `S236`（batch-18）：Tool 定义 / 注册 / 发现 / 调用 → 文件不存在 / 超时 / 权限不足 → 团队化后 File / Command / Sensitive Data / Permission / Audit。
- `S274`（batch-25）：Tool Result Context 太长 → 压缩 / 引用 / 延迟加载 → Tool List 膨胀 → Discovery / Selection。

### 对 Canonical 的对应

`AGENT-018/019` → `AGENT-021/024/025` → `AGENT-020` → `AGENT-028/044`

### 教材含义

Tool 章节不能停在 Function Calling JSON。真正高频的 Production 追问是：**能力太多、能力失败、能力有副作用、能力不可信时怎么办**。

---

## 6. AI Coding：会使用 → 需求 / Context → 修改 → Test / Review → 可交付证明

**置信：A**

```text
平时怎样使用 AI Coding？
        ↓
怎样给 Requirement / Repo Context / Spec？
        ↓
模型怎样改代码？
        ↓
怎样运行 Test / Diff / Review？
        ↓
怎样证明生成代码能进入 Production？
```

### 原始流程证据

- `S236`（batch-18）：真实需求 → 拆需求 / 读代码 → 模型修改 → 跑测试 → Review → 错误 Patch Rollback / Retry → 大 Repo 跨模块 Verification。
- `S237`（batch-18）：直接打开真实项目，让 AI 修 Bug，要求产出 Background / Root Cause / Solution 并现场汇报。
- `S261`（batch-22）：共享屏幕，用本地 AI Coding Tool 现场实现需求，并解释实现过程与验证方式；随后展示自己的 AI Coding Project。
- `S128`（batch-07）：AI Development Tool → 生成代码质量差怎样修正 / 测试 → Skill 提效 → 项目是否真正上线。
- `S215`（batch-14）：开发中怎样使用 AI → `O(N)` Coding → AI Coding 页面需求从 Requirement 到可验收结果。

### 对 Canonical 的对应

`AGENT-048` → `AGENT-037` → `AGENT-036`，并与 Project Verification / Evaluation 交叉。

### 教材含义

AI Coding 不是“工具推荐”附录，而应成为完整工程实践：**需求澄清、上下文供给、生成、验证、验收、责任边界**。

---

## 7. Agent Framework：框架选型 → State → Checkpoint / Resume → Long-running Reliability

**置信：B**

```text
为什么 LangGraph / LangChain / Spring AI？
        ↓
Graph / Node / State 到底解决什么？
        ↓
State 怎样持久化？
        ↓
失败后怎样 Resume？
        ↓
Long-running Agent 怎样保证稳定？
```

### 原始流程证据

- `S078`（batch-05）：LangChain vs LangGraph → 什么场景需要 Graph State Machine。
- `S121`（batch-07）：LangChain / LangGraph 分工与选型 → Structured Output → Multi-session Memory → Tool / Model Exception → Context 恢复。
- `S186`（batch-10）：为什么 LangGraph 而不是 Automation Script → Node 对真实业务的映射 → Long-chain Agent 稳定执行 → Evaluation。
- `S253`（batch-21）：LangGraph State 定义 / 流转 → Node 很多时 State Object OOM → Long-term Memory → 后续 Tool Parameter Failure。

### 对 Canonical 的对应

`AGENT-047` → `AGENT-003/005` → `AGENT-027/029` → `SD-022`

### 教材含义

Framework 章节应该作为 Runtime 理论的**实现映射**，而不是先教 API 再补概念。

---

## 8. Prompt → Context → Harness：工程抽象逐层上移

**置信：B**

```text
Prompt Engineering
        ↓
Context Engineering
        ↓
Harness / Loop Engineering
```

### 原始流程证据

- `S085`（batch-05）：直接要求区分 Context Engineering、Prompt Engineering、Harness Engineering，随后追 Tool Layer、Memory、Hallucination、Dead Loop。
- `S233`（batch-17）：Prompt / Context / Harness / Loop Engineering 四者边界；继续追“为什么 Context Engineering 能解决单一 Prompt 解决不了的问题”。
- `S238`（batch-18）：Skill / Prompt / MCP → Prompt Engineering 原则 → 从零设计 Context Management → FastAPI 只会 GET/POST 为什么还不够支撑 Claude Code 式 Runtime。

### 对 Canonical 的对应

`LLM-023` → `AGENT-008/009` → `AGENT-002/003`

### 教材含义

课程里应明确三个层次：Prompt 是**单次模型行为约束**；Context 是**一次调用的数据组织**；Harness 是**跨多轮、多 Tool、多状态的执行系统**。

---

## 9. Cache / Redis：压力与热点 → 一致性 → Lock Correctness

**置信：B**

```text
真实流量 / HotKey
        ↓
Cache Breakdown / Avalanche
        ↓
DB + Cache Consistency
        ↓
Distributed Lock
        ↓
Expire / Renewal / Owner / Lua Correctness
```

### 原始流程证据

- `S273`（batch-25）：项目压测 → HotKey → Bloom Filter → Cache / DB 双写一致性 → Redis Distributed Lock → Redis 数据结构 → MySQL Index。
- `S148`（batch-08）：5000 万商品 Cache → 10 万 QPS 爆款商品 → HotKey / Expiry / Eviction → DB / Cache Consistency → Redis Distributed Lock 的 NX / EX / Unlock / Watchdog。
- `S154`（batch-08）：并发更新 / Rollback → MySQL / Redis Consistency，并继续追 Redis 数据结构与 Ranking。
- `S214`（batch-14）：Database + Cache Consistency → Hot Key 到期保护；二面继续追 Redis Lua 原子业务。

### 对 Canonical 的对应

`REDIS-008/007` → `AIBE-020` → `REDIS-012/013/014`

### 教材含义

Redis 不能只按数据结构讲。面试中的稳定路径是从**流量问题**进入**一致性与正确性**。

---

## 10. MySQL：慢 → 为什么慢 → Index 机制 → 复杂查询 / Scale

**置信：B**

```text
Slow SQL / 数据增长后变慢
        ↓
Primary / Clustered / Composite Index
        ↓
Covering / Back-to-table / EXPLAIN
        ↓
Deep Pagination / Sharding / Scale
```

### 原始流程证据

- `S274`（batch-25）：真实 Slow SQL → 表数据增长后查询变慢 → UUID 为什么不适合 InnoDB PK。
- `S273`（batch-25）：Sharding → Clustered vs Non-clustered Index → Back-to-table / SQL Optimization / EXPLAIN → Isolation / Phantom Read。
- `S148`（batch-08）：`user_id + create_time` Composite Index → `ORDER BY` / Deep Pagination → MVCC / Isolation。
- `S214`（batch-14）：Index 为什么快 → `(A,B,C,D)` 联合索引 → `SELECT *` vs Covering / Back-to-table → Cache Consistency。

### 对 Canonical 的对应

`MYSQL-003` → `MYSQL-004/005/006/007` → `MYSQL-008/010` → `MYSQL-021/028`

### 教材含义

MySQL 应从“**一个查询为什么从快变慢**”作为贯穿 Case，把 Index、EXPLAIN、Pagination 和 Scale 串起来，而不是彼此孤立。

---

## 11. 跨模块最重要的真实递进

自动共现里最高的跨模块组合是：

- RAG ↔ Agent Harness / Runtime：59 个独立流程；
- AI Backend Engineering ↔ Agent Harness / Runtime：54；
- AI Backend Engineering ↔ Redis：53；
- AI Backend Engineering ↔ MySQL：46；
- LLM Foundation ↔ Agent Harness / Runtime：45。

结合上面的原始顺序核验，真正值得课程采用的不是“同时学两个模块”，而是下面几条桥：

```text
LLM / Prompt
    → Context
    → Agent Runtime

RAG Retrieval
    → Agent Tool / Memory / Context
    → Evaluation / Failure

Redis / MySQL
    → AI Backend Consistency / Reliability
    → Production Agent

AI Coding
    → Repository Understanding
    → Verification
    → Delivery
```

---

## 12. 对面试训练方式的直接结论

真实面试的高频结构并不是“定义题 → 下一道定义题”，而是：

```text
你做了什么？
   ↓
为什么这样设计？
   ↓
内部机制是什么？
   ↓
失败时怎么办？
   ↓
量大 / 变慢 / 多租户时怎么办？
   ↓
你怎么证明这个方案真的更好？
```

因此后续教材和 Review 题应默认包含六层：**概念 → 机制 → Trade-off → Failure → Scale → Evaluation / Verification**。只背第一层，和当前 2026 AI Application / Agent 岗真实面试深度明显不匹配。
