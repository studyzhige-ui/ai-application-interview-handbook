# Terminology Glossary｜跨模块术语与边界

[← Handbook 总目录](../README.md) · [十板块知识地图](knowledge-map.md) · [Documentation Style Guide](documentation-style-guide.md)

> 这份 Glossary 不替代各模块正文。它只解决一个全仓库问题：**同一个词在不同技术层级里可能长得相似，但语义不能混用。**
>
> 规则：正文优先使用本表中的稳定工作定义；产品 / Framework 自己的命名可以保留，但必须说明它映射到哪一层，不能把产品术语写成全行业唯一标准。

---

## 1. Context / Memory / State / History / Checkpoint

| 术语 | 本仓库工作定义 | Primary Module |
|---|---|---|
| **Context** | 当前一次 Model Call 实际可见的输入视图；受 Token Budget 约束。 | LLM Foundation / Agent |
| **Memory** | 为未来调用保存、选择并重新取回的信息；不等于当前 Context。 | Agent |
| **Runtime State** | 程序为了继续/停止需要知道的当前情况，例如A已读、B待结果、用户已取消、报告未验收；Plan只是其中一部分。 | Agent |
| **History** | 已经发生过的 Message / Event / Action 记录；历史不自动等于当前 State。 | Agent |
| **Checkpoint** | 可恢复位置的状态快照及必要引用；不回滚外部世界，两次快照间未知写入仍需核对。 | Agent |

固定边界：

```text
Long Context ≠ Long-term Memory
Chat History ≠ Runtime State
Messages Snapshot ≠ Complete Checkpoint
```

---

## 2. Session / Thread / Run / Turn / Step / Task / Job

这些词在不同Framework中不完全一致。教学`Session→Run→Turn→Step`只在声明了Turn含义后使用；不能强制映射Codex的`Thread→Turn→Item`，Item与生命周期事件也不是一一对应。

| 术语 | 本仓库工作定义 | 备注 |
|---|---|---|
| **Session / Thread** | 跨多个交互持续存在的长期交互容器。 | Agent 语境；不要和 DB Session 混用 |
| **Run** | 围绕一个 Goal 启动的一次可追踪 Agent 执行。 | Agent |
| **Turn** | 必须声明口径。Agent教学树中可指一次决策—行动—观察周期；Codex Turn则是一段用户请求及后续工作，可跨多次模型调用。 | Agent |
| **Step** | Run 内更细的执行动作，如 model call / tool call / checkpoint。 | Agent |
| **Task / Job** | Backend 中可排队、领取、重试、恢复的工作单元。 | AI Backend Engineering |
| **DB Session** | 数据库连接/事务使用语境中的 Session。 | MySQL / FastAPI Integration |
| **Login Session** | 用户认证登录态。 | FastAPI / AI Backend Engineering |

写作规则：出现 `Session` 时，如果上下文不能唯一确定含义，应写成 `Agent Session`、`DB Session` 或 `Login Session`。

---

## 3. Timeout / Deadline / Cancellation / Disconnect / Business Cancel

| 术语 | 本仓库工作定义 | Primary Module |
|---|---|---|
| **Timeout** | 某个等待/操作最多愿意等待多久。 | AIBE；FastAPI/Python 讲本层执行语义 |
| **Deadline** | 整条业务请求必须在某个时间点前完成的端到端预算。 | AIBE |
| **Cancellation** | 对某个执行单元发出停止推进的控制信号。 | Python / FastAPI / Agent 按层解释 |
| **Client Disconnect** | Transport 连接断开。 | FastAPI |
| **Business Cancel** | 业务层取消一个 Durable Task / Agent Run。 | AIBE / Agent |

固定边界：

```text
Timeout ≠ 下游一定停止
Client Disconnect ≠ Business Cancel
Coroutine Cancel ≠ External Side Effect 一定撤销
```

---

## 4. Cache / KV Cache / Semantic Cache / Retrieval Cache

| 术语 | 定义 | Primary Module |
|---|---|---|
| **Cache** | 可失效、可重建的派生副本，用于降低访问成本或延迟。 | Redis / AIBE |
| **KV Cache** | LLM Attention 推理过程中保存历史 Key/Value Tensor 的模型内部缓存。 | LLM Foundation |
| **Semantic Cache** | 应用层按语义相似性复用结果的缓存。 | Redis / AI Application Boundary |
| **Retrieval Cache** | 缓存检索结果，Key 通常必须包含 Query、Filter、Permission、Index Generation 等版本语义。 | RAG |
| **Answer Cache** | 缓存最终回答；风险高，必须考虑知识版本、权限、Prompt、Model、Context。 | RAG / System Design |

固定边界：`KV Cache` 和 Redis / Semantic Cache 完全不是同一层机制。

---

## 5. Source of Truth / Primary / Derived / Ephemeral

| 术语 | 定义 |
|---|---|
| **Source of Truth (SoT)** | 多个副本冲突时最终被视为权威的业务事实来源。 |
| **Primary State** | 业务不可随意丢弃、需要明确持久性与正确性的事实状态。 |
| **Derived State** | 能从 Primary / Source 重建的派生状态，如 Cache、Search Index、Vector Index。 |
| **Ephemeral State** | 短生命周期执行状态，如 Lease、临时 Progress、Buffer。 |

示例：

```text
MySQL / Business DB = 常见 Primary / SoT
Redis Cache          = Derived
Vector Index         = Derived Retrieval State
Lease / Hot Progress = Ephemeral
```

具体系统可以选择不同 SoT，但必须显式说明，不能因为某个存储更快就默认变成权威状态。

---

## 6. Idempotency / Retry / Replay / Resume / Reconciliation / Compensation

| 术语 | 定义 | Primary Module |
|---|---|---|
| **Idempotency** | 同一个逻辑操作被重复提交时，不产生额外重复副作用。 | AIBE |
| **Retry** | 在允许的失败语义下再次尝试操作。 | AIBE |
| **Replay** | 重放 Event / Evidence / History 以重建状态、调试或评估；不默认等于再次触发真实副作用。 | Agent |
| **Resume** | 从持久化状态继续同一执行 lineage。 | Agent |
| **Reconciliation** | 比对 SoT 与派生/外部状态，发现长期不一致并修复。 | AIBE |
| **Compensation** | 对已经发生、无法物理 Rollback 的业务副作用执行新的补偿动作。 | AIBE / System Design |

固定边界：

```text
Retry ≠ 一定安全
Replay ≠ 再执行一遍所有 Tool
Compensation ≠ Database Rollback
```

---

## 7. Lock / Lease / Ownership / Fencing

| 术语 | 定义 | Primary Module |
|---|---|---|
| **Lock** | 协调并发访问的互斥/同步机制。 | Python / MySQL / Redis 按层解释 |
| **Lease** | 有过期时间的临时执行/资源所有权。 | AIBE / Agent |
| **Ownership** | 当前谁被允许推进或修改某个 Task / Run / Resource。 | AIBE / Agent |
| **Fencing Token / Generation** | 单调递增的所有权版本，用于阻止过期 Owner 在恢复后继续写新状态。 | Redis / AIBE / Agent |

`Redis Lock`、`MySQL Lock`、`Python Lock` 不应因为都叫 Lock 就被视为同一抽象层。

---

## 8. Message / Event / Tool Result / Trace

| 术语 | 定义 |
|---|---|
| **Message** | 主要服务于模型或用户交互的输入/输出表示。 |
| **Runtime Event** | 系统真实发生的执行事实，如 tool_started / checkpoint_written / cancel_requested。 |
| **Tool Result** | 一次 Tool Invocation 的结构化结果，可有 model-visible、host metadata、artifact 等不同 projection。 |
| **Trace** | 记录一次请求/Run 中各阶段的因果链、输入输出引用、版本与时延，用于 Debug / Replay / Eval / Audit。 |

固定边界：`Runtime Event ≠ Chat Message`，`Tool Result ≠ 一段日志字符串`。

---

## 9. Embedding / Vector Search / Retrieval / Rerank

```text
Embedding Model
= 把对象映射到向量表示

Vector DB / ANN
= 高效地存储并搜索近邻向量

Retrieval
= 根据 Query 从一个或多个 Source 获取候选 Evidence

Rerank
= 对较小 Candidate Set 做更精细的相关性排序
```

Primary ownership：

- Embedding / Reranker 模型原理 → **LLM Foundation**；
- HNSW / IVF / ANN / Vector Filter / Lifecycle → **Vector DB**；
- Dense / Sparse / Hybrid / RRF / Candidate Budget / Retrieval Eval → **RAG**。

---

## 10. Prompt / Context Engineering / Harness Engineering

```text
Prompt Engineering
= 设计模型本次调用中的指令与输出约束

Context Engineering
= 决定一次 inference 实际看见哪些信息，以及如何压缩/选择/组织

Harness Engineering
= 管理跨多轮、多 Tool、多 State 的执行、权限、恢复、Trace 与 Eval
```

Primary ownership：Prompt → LLM Foundation；Context / Harness Runtime → Agent。

---

## 11. Tool / MCP / Skill / Hook

```text
Tool
= 一次可执行能力与其 Contract

MCP
= 外部能力 / Context 的标准连接协议

Skill
= 可发现、按需加载的程序性知识 / 资源包

Hook
= Runtime 生命周期中的扩展点
```

这些概念有关联，但不是同义词。

---

## 12. Observability / Evaluation / Verification

| 术语 | 定义 |
|---|---|
| **Observability** | 通过 Metrics / Logs / Trace 等信号理解系统运行状态与故障。 |
| **Evaluation** | 用 Dataset / Ground Truth / Judge / Benchmark 等判断系统输出质量或能力。 |
| **Verification** | 对一次具体结果是否满足显式要求进行检查，如 Test、Schema、Invariant、Evidence Support。 |

例子：

```text
P99 Tool latency       → Observability
Agent task success rate→ Evaluation
tests_passed?          → Verification
```

三者在 Production AI 系统中互补，不能用“有日志”代替 Evaluation，也不能用平均 Eval 分数代替一次高风险动作的 Verification。

---

## 13. 写作与面试表达规则

遇到跨模块同名概念，回答时优先说出层级：

```text
这是 Python Runtime 的 Lock
这是 Redis 协调层的 Lease
这是 Agent Run 的 Ownership
```

而不是只抛一个术语。

最终要求：**同词先分层，再谈机制；产品名先映射到稳定概念，再讨论实现差异。**


## 本轮补充：恢复与诊断的数据最小化

Persistence（持久化）是让选定信息活过进程重启，不是把全部内存写入存储。Resume（恢复执行）不是Summary（摘要）；Compaction（上下文压缩）只管理模型输入规模。Trace（执行追踪）用于定位阶段、耗时与失败，不是默认的恢复账本。

关键操作身份与回执按业务可靠性保存；产物按交付需要保存；诊断可采样、脱敏和到期删除。版本用于确实发生的并发、变更或兼容问题，ID用于标识；不要求每个事件复制完整Prompt、工具定义和所有版本。见[状态与持久化](../curriculum/09-curriculum/09-agent/docs/12-StateHistoryAndPersistence.md)、[检查点与恢复](../curriculum/09-curriculum/09-agent/docs/13-CheckpointResumeAndRecovery.md)、[Trace](../curriculum/09-curriculum/09-agent/docs/20-TraceReplayAndDiagnosis.md)。
