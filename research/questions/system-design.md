# System Design Canonical Questions — S001–S279 全库纵向扫描 v2

更新日期：2026-09-10

> 一级板块：**System Design**。本文件只保留端到端场景设计题。底层 MySQL / Redis / MQ / RAG / Agent 单点原理仍只在各自 Primary Module 维护；这里关注如何把多个能力组合成可交付系统。
>
> 本文件所有条目的 `Primary Module = System Design`。同一来源可以同时支撑一个底层 Canonical 与一个端到端 Scenario，但两者考察目标必须不同，不能只是换标题复制同一道题。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**24**
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数
- 当前版本：`v2`（十板块归属审计版）

System Design 是新十板块路径的最后一层，因为它本质上是在检验前九块知识能否组合起来处理容量、状态、一致性、可靠性、成本、安全和演进。

---

## 2. High-concurrency / Data Systems

### SD-001 · 设计秒杀 / 抢购 / 库存系统：怎样防止 Oversell / Undersell，并处理 Redis、DB、订单和补偿的一致性？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, MySQL, Redis
- **Topic**：Flash Sale / Inventory
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S010`, `S025`, `S090`, `S093`, `S134`, `S135`, `S148`, `S212`, `S253`, `S266`

### SD-002 · 设计高并发排行榜 / 热榜：实时更新、HotKey、排序、读取热点与持久化怎样拆？

- **Primary Module**：System Design
- **Related Modules**：Redis, AI Backend Engineering
- **Topic**：Realtime Ranking
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S083`, `S142`

### SD-003 · 设计搜索框实时联想 / 模糊搜索：如何同时支持代码、名称、拼音 / Prefix / Infix，并控制实时交互成本？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Redis
- **Topic**：Autocomplete / Fuzzy Search
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S110`, `S167`

### SD-004 · 设计 Feed / 关注流：如何让用户快速看到关注对象的新内容，并处理 Fan-out、热点和分页？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, MySQL, Redis
- **Topic**：Feed System
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S191`

### SD-005 · 设计 Notification Platform：怎样处理可靠投递、Retry、Dedup、状态与多通道扩展？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering
- **Topic**：Notification Platform
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S161`

### SD-006 · 设计每天约 10TB 数据的 Storage + Time-range Query Service：Hot / Cold Data、Index、API 与容量怎样组织？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, MySQL
- **Topic**：Large-scale Storage
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S203`

### SD-007 · 设计大规模批处理 / 数据迁移：数千万行或 20 万行 Excel 怎样分页、流式、并发、断点恢复并限制 DB 压力？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, MySQL
- **Topic**：Batch Processing / Migration
- **Question Type**：System Design / Troubleshoot
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S094`, `S207`, `S232`, `S244`

### SD-008 · 设计大规模 IP / ID Whitelist 或 Dedup Service：海量去重、Memory Estimation 与在线查询怎样权衡？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering
- **Topic**：Massive-set Processing
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S138`

---

## 3. Service / Platform Design

### SD-009 · 设计 Distributed Rate Limiter：怎样处理全局配额、低延迟、一致性、故障与下游容量约束？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Redis
- **Topic**：Distributed Rate Limiter
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S147`, `S270`

### SD-010 · 设计多实例 Access Token / Refresh Token 缓存：怎样避免 Refresh Stampede，并处理失败、旧 Token 与实例崩溃？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Redis
- **Topic**：Token Refresh Coordination
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S268`

### SD-011 · 设计二维码登录：二维码生成、手机确认、PC 状态同步、Token / Session 建立和安全边界怎样组织？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Redis
- **Topic**：QR Login
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S110`, `S188`

### SD-012 · 设计大文件 / 长视频上传与处理系统：分片、断点续传、异步任务、状态查询和失败恢复怎样实现？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Agent
- **Topic**：Large-file Processing
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S047`, `S149`, `S205`

### SD-013 · 设计统一 Model / LLM Gateway：多 Provider Schema、Routing、Streaming、Rate Limit、Cost、Failover 和 Observability 怎样组织？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, LLM Foundation（应用工程深度）, Agent
- **Topic**：LLM Gateway
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S112`, `S208`, `S244`

### SD-014 · 设计多租户 AI / Agent Platform：用户、Workspace、Permission、Resource Isolation、Usage / Cost 与 Agent Routing 怎样治理？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Agent
- **Topic**：Multi-tenant Agent Platform
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S037`, `S075`, `S119`, `S129`, `S275`

### SD-015 · 设计受限资源的多租户计算平台：SGX / EPC 等资源不足时怎样做安全隔离、Scheduling 与性能治理？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering
- **Topic**：Secure Multi-tenant Compute
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S244`

---

## 4. RAG / AI Application Design

### SD-016 · 从零设计 Enterprise Knowledge-base QA / RAG Service：Ingestion、Permission、Retrieval、Generation、Evaluation 与 Update 怎样组织？

- **Primary Module**：System Design
- **Related Modules**：Vector DB, LLM Foundation（应用工程深度）, RAG, AI Backend Engineering
- **Topic**：Enterprise RAG
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S040`, `S056`, `S147`, `S217`, `S241`, `S277`

### SD-017 · 面对 600GB–1TB PDF / 扫描件语料，怎样设计垂直 RAG：解析、Embedding 成本、Index、Hybrid Retrieval 与 Incremental Update 如何扩展？

- **Primary Module**：System Design
- **Related Modules**：Vector DB, RAG, AI Backend Engineering
- **Topic**：Large-scale Document RAG
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S217`

### SD-018 · 设计 Financial / Data Analysis Agent：从自然语言问题到检索、计算、结论 Verification 与 Citation 怎样闭环？

- **Primary Module**：System Design
- **Related Modules**：RAG, Agent, LLM Foundation（应用工程深度）
- **Topic**：Analytical Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S240`

### SD-019 · 设计 AI Customer Service Agent：Intent、RAG、订单 / 业务 Tool、Memory、Human Handoff 与高风险操作怎样分层？

- **Primary Module**：System Design
- **Related Modules**：RAG, Agent, AI Backend Engineering
- **Topic**：Customer Service Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S179`, `S207`, `S222`, `S260`

### SD-020 · 设计 Multi-modal Document / PDF → HTML Agent Workflow：文字、图片、表格、知识核对与图文输出怎样保持可追溯？

- **Primary Module**：System Design
- **Related Modules**：RAG, Agent
- **Topic**：Multimodal Document Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S080`, `S231`

---

## 5. Agent / AI-native System Design

### SD-021 · 从零设计 Production Agent Backend：Loop、State、Tool、Memory、Checkpoint、Streaming、Auth、Observability 与 Scale 怎样组合？

- **Primary Module**：System Design
- **Related Modules**：AI Backend Engineering, Agent
- **Topic**：Agent Backend
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**13**
- **Evidence Sources**：`S068`, `S082`, `S085`, `S122`, `S129`, `S171`, `S177`, `S192`, `S214`, `S221`, `S239`, `S241`, `S256`

### SD-022 · 设计 Long-running Agent Runtime：数小时 / 数天任务怎样做 Checkpoint、Resume、Cancel、Idempotency、外部副作用和状态迁移？

- **Primary Module**：System Design
- **Related Modules**：Agent, AI Backend Engineering, Redis
- **Topic**：Long-running Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S042`, `S059`, `S107`, `S130`, `S144`, `S146`, `S181`, `S209`, `S242`, `S264`

### SD-023 · 设计 Game / Interactive Agent：Goal、State、Action / Tool、Memory、Evaluation 与安全边界怎样映射具体游戏业务？

- **Primary Module**：System Design
- **Related Modules**：Agent, LLM Foundation（应用工程深度）
- **Topic**：Game Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S220`, `S235`, `S260`

### SD-024 · 设计 AI 自动内容创作 / 视频编辑 Agent：Planning、SubAgent、素材状态、人物一致性、长任务和 Evaluation 怎样闭环？

- **Primary Module**：System Design
- **Related Modules**：Agent, RAG
- **Topic**：Content Creation Agent
- **Question Type**：System Design
- **Depth**：L4
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S123`, `S220`

---

## 6. 十板块归属审计结论

System Design 与前九块的关系不是“再复制一遍底层知识”，而是保留**端到端组合题**。本轮逐项复核后，24 道均满足至少两个模块 / 多个工程约束的组合特征，因此保持 `System Design` Primary。

典型边界：

- `Rate Limit 算法 / Token Bucket / Sliding Window` → `AI Backend Engineering`；完整 Distributed Rate Limiter 的容量、一致性、故障设计 → `SD-009`。
- `DB + Cache Consistency` 原理 → `AIBE-020`；完整秒杀库存链路 → `SD-001`。
- `RAG Parse / Chunk / Rerank` → `RAG`；Enterprise / TB-scale RAG 的端到端架构 → `SD-016` / `SD-017`。
- `Checkpoint / Resume / External Side Effect` Runtime 语义 → `Agent`；数小时 / 数天 Long-running Agent 的完整系统设计 → `SD-022`。

本轮没有需要迁出的 ACTIVE Canonical。

---

## 7. 对课程结构的直接信号

System Design 不应该从零重新讲 MySQL、Redis、RAG 或 Agent，而应把前九块作为可组合组件：

```text
Requirement / SLA / Scale
        ↓
Data + State Model
        ↓
Request / Async / Streaming Path
        ↓
Consistency / Idempotency / Recovery
        ↓
Security / Permission / Cost
        ↓
Observability / Evaluation
        ↓
Evolution / Capacity / Trade-off
```

这也是为什么它必须放在新学习路径的最后。
