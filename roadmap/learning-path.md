# Learning Path｜十板块正式学习路线

[← Handbook 总目录](../README.md) · [十板块知识地图](knowledge-map.md) · [跨模块术语表](terminology-glossary.md) · [课程进度](../research/questions/progress.md)

> **状态：✅ 第一版正式学习路线完成。** 这份路线解决“185 个正文知识块应该怎样真正学完、复习并转化成面试能力”。
>
> **固定原则不变：知识体系演进顺序优先。** HUMAN-A 真人面经只影响第二遍 / 第三遍的复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的课程主干。
>
> **这是一套推荐执行节奏，不是唯一课表。** 模块 README / Review 只把本页作为可选入口；不同基础、时间预算或教学场景可以自行调整速度，但第一次系统学习仍建议保持知识依赖顺序。

---

## 1. 正式学习顺序永远不变

[Python Foundation](../python/README.md)
→ [FastAPI](../fastapi/README.md)
→ [AI Backend Engineering](../backend-engineering/README.md)
→ [MySQL](../mysql/README.md)
→ [Redis](../redis/README.md)
→ [Vector Database](../vector-db/README.md)
→ [LLM Foundation](../llm-foundation/README.md)
→ [RAG](../rag/README.md)
→ [Agent](../agent/README.md)
→ [System Design](../system-design/README.md)

不要因为 Agent / RAG 高频就从中间开始，也不要因为某个基础题真人频率低就跳过必要前置。

Review 快速入口：[Python](../python/review/README.md) · [FastAPI](../fastapi/review/README.md) · [AIBE](../backend-engineering/review/README.md) · [MySQL](../mysql/review/README.md) · [Redis](../redis/review/README.md) · [Vector DB](../vector-db/review/README.md) · [LLM](../llm-foundation/review/README.md) · [RAG](../rag/review/README.md) · [Agent](../agent/review/README.md) · [System Design](../system-design/review/README.md)

---

## 2. “学完”不是把 Markdown 看完

每个知识块至少经过五步：

```text
Read
→ Close Book Recall
→ Self-test
→ Explain Aloud
→ Error Log
```

每个一级模块再经过：

```text
全部 docs 按顺序完成
→ review/README.md 闭卷重建总图
→ interview/ 高频真实问法
→ 易错点校正
→ Exit Gate
→ 才进入下一模块
```

### 一个标准 Session（约 2.5–3 小时）

1. **15 min｜Spaced Recall**：不看笔记，复述上一 Session 的主线。
2. **75–90 min｜正文**：连续学习 2–3 个相邻知识块，大章节可以少读一个。
3. **20 min｜闭卷重建**：画 Data Flow / State Machine / Mechanism，不抄正文。
4. **20 min｜折叠自测**：先回答，再展开 `<details>` 对答案。
5. **20 min｜面试口述**：至少做 2 个 30 秒回答，其中 1 个继续追到 Failure / Trade-off。
6. **10 min｜Error Log**：只记“刚才真正答错、混淆或说不清”的东西。

时间不足时可以把一个 Session 拆成两天；时间充足时可以连续做两个 Session，但**不能改变章节顺序**。

---

## 3. 三遍学习法

### Pass 1｜Curriculum Pass：100% 正文，建立完整知识体系

目标：

```text
知道为什么存在
→ 理解机制
→ 能画正常路径
→ 知道最关键 Failure / Trade-off
```

这一遍 **185 个 Curriculum Markdown 全部要过**，不根据面经频率删减。

### Pass 2｜Review Pass：从“看懂”变成“能重建”

每完成一个一级模块，立即进入该模块 `review/README.md`。

要求：

- 不看正文先画总图；
- 能解释每条箭头为什么存在；
- 能指出至少 3 个 Failure / Boundary；
- 自测答错的题进入 Error Log；
- 答不出来再回具体正文，不从头重读整个模块。

### Pass 3｜Interview Pass：真人面经只在这一层加权

当前 Frozen HUMAN-A Frequency：

```text
🔥🔥🔥 >=10 sources   82 Canonical
🔥🔥   4–9 sources   83 Canonical
🔥     2–3 sources   37 Canonical
single 1 source      33 Canonical
```

建议复习权重：

| Market Heat | 口述次数 | 最低要求 |
|---|---:|---|
| 🔥🔥🔥 | 3 | 30 秒定义 → 2 分钟机制 → Failure / Scale / Verification 深挖 |
| 🔥🔥 | 2 | 30 秒定义 → 2 分钟机制 / 边界 |
| 🔥 | 1 | 能准确回答，并知道 Primary Module |
| single | 1 次识别 | 不因低频删除知识；属于前置 / Core 时仍按正常课程掌握 |

**Depth 再单独叠加：所有 L4 不论频率高低，都必须至少做一次 Failure / Scale / Verification 深挖。**

所以 Heat 决定“重复多少次”，Depth 决定“要追多深”；二者都不能决定第一次学习顺序。

---

# 4. 13 周标准路线（推荐第一次完整学习）

默认：**每周 6 个学习 Session + 1 天 Buffer / Rest**。共 13 周、78 个可用 Session；75 个覆盖正式模块，额外 3 个用于 Foundation / 全局复盘。

## Week 1｜Python Foundation

- S1：`01–03`
- S2：`04–05`
- S3：`06–08`
- S4：`09–11`
- S5：`12–13`
- S6：Python Review + Interview + Exit Gate

产出：能从对象模型一路解释到 asyncio / Structured Output，而不是把 Python 当语法题。

## Week 2｜FastAPI 主体

- S1：`01–03`
- S2：`04–06`
- S3：`07–08`
- S4：`09–11`
- S5：`12–14`
- S6：`15–16`

本周先把正文完成，Review 放到下一周第一个 Session。

## Week 3｜FastAPI 收口 + AIBE 前半

- S1：FastAPI Review + Interview + Exit Gate
- S2：AIBE `01–03`
- S3：AIBE `04–06`
- S4：AIBE `07–09`
- S5：AIBE `10–12`
- S6：AIBE `13–15`

## Week 4｜AIBE 收口 + Foundation 总复盘

- S1：AIBE `16–18`
- S2：AIBE `19–20`
- S3：AIBE `21–22`
- S4：AIBE Review + Interview + Exit Gate
- S5：Foundation 白板复盘：Python → FastAPI → AIBE
- S6：Foundation 综合追问：async / pool / timeout / cancellation / streaming / durable task

Foundation 结束时，应能完整解释：

```text
Python Runtime
→ ASGI Service
→ Production Backend
```

## Week 5｜MySQL 前半

- S1：`01–03`
- S2：`04–06`
- S3：`07–09`
- S4：`10–12`
- S5：`13–15`
- S6：`16–18`

## Week 6｜MySQL 收口 + Redis 起步

- S1：MySQL `19–21`
- S2：MySQL `22–23`
- S3：MySQL Review + Interview + Exit Gate
- S4：Redis `01–03`
- S5：Redis `04–06`
- S6：Redis `07–09`

## Week 7｜Redis 收口

- S1：`10–12`
- S2：`13–15`
- S3：`16–18`
- S4：`19–21`
- S5：`22–24`
- S6：Redis Review + Interview + Exit Gate

## Week 8｜Vector Database

- S1：`01–03`
- S2：`04–06`
- S3：`07–09`
- S4：`10–12`
- S5：`13–16`
- S6：Vector DB Review + Interview + Exit Gate

Data 阶段结束时，应能回答：

```text
业务事实为什么进 MySQL？
什么值得进入 Redis？
什么需要 Vector Retrieval？
三类状态谁是 SoT / Derived / Ephemeral？
```

## Week 9｜LLM Foundation

- S1：`01–03`
- S2：`04–06`
- S3：`07–09`
- S4：`10–12`
- S5：`13–14`
- S6：LLM Review + Interview + Exit Gate

## Week 10｜RAG

- S1：`01–03`
- S2：`04–06`
- S3：`07–09`
- S4：`10–12`
- S5：`13–14`
- S6：RAG Review + Interview + Exit Gate

## Week 11｜Agent 前半

- S1：`01–03`
- S2：`04–06`
- S3：`07–09`
- S4：`10–12`
- S5：`13–15`
- S6：`16–18`

## Week 12｜Agent 收口 + System Design 起步

- S1：Agent `19–21`
- S2：Agent `22–24`
- S3：Agent Review + Interview + Exit Gate
- S4：System Design `01–03`
- S5：System Design `04–06`
- S6：System Design `07–09`

## Week 13｜System Design 收口 + 全局复盘

- S1：System Design `10–12`
- S2：System Design `13–15`
- S3：System Design `16–17`
- S4：System Design `18–19`
- S5：System Design Review + Interview + Exit Gate
- S6：十板块全局白板复盘 + Error Log 清算

最终闭环：

```text
Python
→ FastAPI
→ AIBE
→ MySQL / Redis / Vector DB
→ LLM
→ RAG
→ Agent Runtime
→ System Design
```

---

# 5. 十个模块的 Exit Gate

只有通过 Exit Gate 才进入下一模块。不是考试分数，而是防止“读过但没有形成可调用知识”。

| Module | Exit Gate：闭卷至少能完成什么 |
|---|---|
| Python | 解释对象 / 引用 / dict / Protocol / Structured Output / GIL / asyncio；比较 Thread / Process / Coroutine；写出 `gather` vs `as_completed` 选择逻辑。 |
| FastAPI | 画 ASGI Request Lifecycle；解释 Middleware vs Dependency、yield / Lifespan、`def` vs `async def`、SSE / WebSocket、Disconnect / Cancellation。 |
| AIBE | 画 Pool / Queue / Backpressure；解释 Deadline → Retry → Idempotency；MQ / Durable Task；DB+Cache Consistency；Observability / K8s 故障链。 |
| MySQL | 解释 SQL Execution / B+Tree / EXPLAIN；Isolation / MVCC / Lock；redo / undo / binlog；Replication / Sharding / CDC。 |
| Redis | 解释核心数据结构、TTL / Eviction、Cache Failure、RDB/AOF、Replication/Sentinel/Cluster、Lua / Lock、Streams / Rate Limit。 |
| Vector DB | 解释 Similarity、Exact vs ANN、HNSW / IVF / PQ、Filter / Tenant、Index Lifecycle、Distributed / Product Selection。 |
| LLM | 解释 Token / Context、Transformer / Attention、Generation、KV Cache / Prefill / Decode、Serving、Embedding/Reranker、Prompt / Hallucination 边界。 |
| RAG | 从 Source 画完整 Pipeline；解释 Parse / Chunk、Hybrid / RRF / Rerank、Evidence / Citation、Retrieval / E2E Eval、Bad Case Attribution。 |
| Agent | 画 Agent Loop / Tool Runtime；区分 Context / Memory / State；解释 Compaction、Checkpoint / Resume、Permission / Sandbox、Multi-Agent、Trace / Eval。 |
| System Design | 面对陌生题能按 Requirement → Capacity → State → Flow → Consistency → Reliability → Security → Observability / Evaluation 走完整设计，而不是套模板。 |

### Exit Gate 的建议通过线

- Review 折叠自测：闭卷正确率约 **80%+**；
- 随机抽 5 个面试题：至少 4 个能先给 30 秒回答；
- 其中至少 2 个能继续追到 Failure / Trade-off；
- 能画一张本模块总图；
- 能说清至少 2 个“这个问题 Primary 不在本模块”的边界。

如果没通过：只回补 Error Log 对应章节，不从头重读整个模块。

---

# 6. Spaced Review：避免学到 Agent 时忘了 Python

建议固定三个回看点：

```text
D+1   10–15 min：复述上一 Session
D+7   20–30 min：闭卷画模块主线 / 关键 Failure
D+21  30–45 min：只做高 Heat + L4 真人问法
```

每完成新模块，至少抽一个旧模块做 15 分钟随机回忆。

重点不是制造大量 Anki 卡，而是保持：

```text
Mental Model
→ Mechanism
→ Failure
→ Interview Expression
```

仍然能从长期记忆中被调用。

---

# 7. 8 周加速路线

**适用：每天约 4 小时、已经有一部分基础，希望更快进入秋招面试。**

规则：使用完全相同的 75 个 Module Session，只是每天约完成 `1.5–2` 个标准 Session；**不能跳低频前置知识，也不能把 Review 全删掉。**

建议周结构：

| Week | 目标 |
|---|---|
| 1 | Python + FastAPI |
| 2 | AIBE |
| 3 | MySQL |
| 4 | Redis + Vector DB |
| 5 | LLM + RAG |
| 6 | Agent 01–12 |
| 7 | Agent 13–24 + System Design 01–08 |
| 8 | System Design 09–19 + 全局 Review / Interview |

如果发现连续两天 Exit / Self-test 大量失败，就退回 13 周节奏，不要继续用时长换“看完速度”。

---

# 8. 14 天面试前冲刺路线

**不适合第一次学习。只适用于已经完成 Pass 1 的人。**

| Day | 复习重点 |
|---:|---|
| 1 | Python + FastAPI：async / validation / lifecycle / streaming / cancellation |
| 2 | AIBE：pool / timeout / retry / idempotency / MQ / consistency |
| 3 | MySQL：index / optimizer / transaction / MVCC / lock / log |
| 4 | Redis：cache failure / HA / Lua / distributed lock / rate limit |
| 5 | Vector DB：ANN / HNSW / IVF / filter / lifecycle / selection |
| 6 | LLM：context / attention / decoding / KV / serving / prompt |
| 7 | RAG：pipeline / parse / chunk / hybrid / rerank |
| 8 | RAG：evaluation / bad case / freshness / production |
| 9 | Agent：boundary / loop / tool runtime / planning |
| 10 | Agent：context / compaction / memory / checkpoint |
| 11 | Agent：security / MCP / multi-agent / trace / eval |
| 12 | System Design：Requirement / Capacity / State / Reliability |
| 13 | System Design Cases + 跨模块连续追问 |
| 14 | 只清 Error Log + 30 秒回答，不再大面积读新内容 |

冲刺阶段优先顺序：

```text
Error Log
> 🔥🔥🔥 Canonical
> L4 Failure / System Design
> 🔥🔥 Canonical
> 其它识别性复习
```

但这只是**已经学完后的复习顺序**，不是 Curriculum 顺序。

---

# 9. 学习时不要做什么

- 不要逐字抄正文做“漂亮笔记”；
- 不要第一遍就从高频题倒着学；
- 不要每个术语都做卡片；
- 不要把 Review 当成再读一遍正文；
- 不要只背 30 秒回答而跳过机制；
- 不要因为一个 Session 没完成就打乱模块顺序；
- 不要因为 Source Count 低就删掉知识前置；
- 不要在还不能解释 Failure 时急着背 System Design 模板。

---

# 10. 最终完成标准

完成整条路线后，你应该同时具备四层能力：

```text
Knowledge
= 十板块因果链完整

Recall
= 不看正文可以重建机制与边界

Interview
= 高频题能 30 秒开场并承接深挖

Transfer
= 陌生问题能找到正确 Primary Module，并把多个模块组合起来
```

学习路线结束后，下一层才是：

```text
Bridge Labs
→ 把多个模块变成工程实战能力

Cross-module Mock Interview
→ 把多个模块变成连续面试应答能力
```

这两层不再扩展知识主干，而是训练“组合与迁移”。
