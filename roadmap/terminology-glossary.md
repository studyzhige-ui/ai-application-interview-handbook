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
| **Runtime State** | 当前执行事实：Run 到哪一步、哪些动作已发生、接下来允许什么 Transition。 | Agent |
| **History** | 已经发生过的 Message / Event / Action 记录；历史不自动等于当前 State。 | Agent |
| **Checkpoint** | 足以从明确恢复点继续正确执行的持久化快照 / 状态集合。 | Agent |

固定边界：

```text
Long Context ≠ Long-term Memory
Chat History ≠ Runtime State
Messages Snapshot ≠ Complete Checkpoint
```

---

## 2. Session / Thread / Run / Turn / Item / Step / Task / Job

先说明语境，再定义对象关系。以下保留 Codex 的交互对象，并区分教材采用的任务/执行工作定义；不把 Session→Run→Turn 规定为行业统一层级。

| 术语 | 本仓库工作定义 | 备注 |
|---|---|---|
| **Agent Session / Thread** | 跨多个交互持续存在的会话容器。 | Codex Thread 是会话，不是操作系统线程 |
| **Run** | 围绕目标的一次受管理执行，可以暂停与恢复。 | 教材工作定义；与 Thread / Turn 的关联由应用协议决定 |
| **Turn** | Codex 中一次用户请求及其后续 Agent 工作。 | 可以包含多次模型推理与工具交互，不等于一次模型调用 |
| **Item** | Codex 中有类型的输入输出单元，例如消息、工具执行、文件修改。 | 一个 Item 可以产生多个生命周期 Event |
| **Step** | 运行时自行定义的可记录推进单位。 | 不同框架可能采用不同粒度 |
| **Agent Task** | 有目标、范围、权限边界和验收条件的工作对象。 | 应用层管理；可以关联多个 Run |
| **Backend Task / Job** | 可以排队、领取、重试或恢复的后台工作单元。 | AI Backend Engineering；不默认等于用户任务 |
| **DB Session** | 数据库连接/事务使用语境中的 Session。 | MySQL / FastAPI Integration |
| **Login Session** | 用户认证登录态。 | FastAPI / AI Backend Engineering |

写作规则：不能唯一确定含义时，写明 Agent Session、DB Session 或 Login Session。执行实例、进程、会话和业务任务也不是同一个实体。详细机制见 [Agent 执行循环](../agent/docs/04-AgentLoopAndControl.md)与[执行状态](../agent/docs/07-StateAndRecovery.md)。

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

## 14. Agent 系统、层与 Harness 的边界

Agent 模块覆盖任务设计、四层职责、安全质量与生产演进；Harness / Runtime 只指以运行层为核心的执行系统，实现可以包含接入代码，不等于完整产品。

架构 L1 / L2 / L3 / L4 分别是应用 / 运行 / 接入 / 资源，与研究题库的 Depth 编号无关。层表示职责，模块承担职责，机制实现职责，协议连接对象，资源承载真实能力和事实。

完整解释只维护在[Agent 正式课程](../agent/README.md)。新增术语先说明类型、主责、动机与边界，不另增一套分类或学习路线。
