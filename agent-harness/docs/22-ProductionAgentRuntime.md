# 22｜Production Agent Runtime Architecture

> 本章把前 21 个知识板块汇合成可上线架构。它不是 System Design 模块的替代，而是回答：**Agent Runtime 自身在 Production 中需要哪些组件和故障边界。**

## 1. 一个通用 Production 拆分

```text
Client / API
    ↓
Session / Run Service
    ↓
Agent Runtime Worker
 ┌──────┼────────┐
 ▼      ▼        ▼
Model  Tool    Context/State
Router Gateway  Services
 │      │        │
 ▼      ▼        ▼
Provider Sandbox Durable Store
              / Event Log
```

旁路：

```text
Permission / Policy
Trace / Eval
Queue / Quota
Artifact Store
Secrets
```

## 2. Brain / Hands / Durable Session

一个成熟抽象：

```text
Brain
= Model + Harness decision loop

Hands
= isolated execution environment / tools

Durable Session
= context-window 之外的 event/state/artifact history
```

把三者解耦有利于：

- Worker 横向扩展；
- Sandbox 生命周期独立；
- Crash 后恢复；
- Session 跨机器；
- Trace / Audit。

Anthropic Managed Agents 的工程资料提供了类似成熟参考，但课程只抽象通用能力，不复制产品拓扑。

## 3. Stateless Worker vs Durable State

Runtime Worker 尽量可以被替换：

```text
worker crash
→ another worker loads checkpoint/state
→ resume
```

因此关键状态不应只放进进程内存。

## 4. Execution Environment Pool

Coding / Browser / Shell Agent 常需要：

```text
container / VM
workspace
filesystem policy
network policy
CPU / memory quota
lifecycle cleanup
```

环境可以按 Session、Task 或 Tool 复用，取决于 isolation 与 warm-start trade-off。

## 5. Queue / Backpressure / Quota 边界

通用 Queue / Backpressure 原理属于 AI Backend Engineering；Agent Runtime 要定义自己的工作量单位：

```text
active run
model tokens
concurrent tools
sandbox slots
provider quota
per-tenant budget
```

否则一个长 Agent Run 可以占满整个服务。

## 6. Failure Domains

至少区分：

```text
API failure
Runtime worker failure
Model/provider failure
Tool dependency failure
Sandbox failure
State store failure
Artifact store failure
queue overload
```

每一层决定：

```text
retry?
fallback?
resume?
degrade?
fail run?
```

## 7. Multi-tenant Production

需要贯穿：

```text
Auth
Session
Memory
State
Artifact
Tool Permission
Sandbox
Secrets
Trace
Quota
```

Tenant Isolation 不是一个数据库 WHERE 条件。

## 8. Cost Model

Agent Cost 不只有模型 Token：

```text
model input/output
repeated context
compaction
tool compute
sandbox time
retrieval
artifact storage
trace / eval
retry / fallback
```

应看：

```text
cost per successful task
```

而不是只看每 1M Token 单价。

## 9. Graceful Degradation

例如：

```text
strong model unavailable
→ fallback smaller model for safe steps

sandbox pool full
→ queue / partial read-only mode

memory unavailable
→ continue without long-term memory if policy allows

external write tool unavailable
→ preserve run state and ask user / retry later
```

降级必须保持安全下限。

## 10. HUMAN-A / 模块边界

Agent-specific Production Runtime 与 `SD-021/022` 有交叉，但本章关注内部 Runtime Component；完整跨 MySQL/Redis/VectorDB/RAG/Queue/API 的平台架构归 System Design。

## 11. 🎯 面试回答

> Production Agent Runtime 最好把 API/Session、Harness Worker、Model Gateway、Tool/Sandbox、Durable State/Event Log、Artifact Store、Permission/Secrets、Trace/Eval 分开。Worker 可以无状态替换，长任务状态和副作用证据必须 Durable；执行环境与 Brain 解耦，支持隔离和横向扩展。容量要按 active run、sandbox slot、tool concurrency、provider quota 和 cost per successful task 管理，并为不同 failure domain 设计 retry/fallback/resume/degrade。

<details><summary>自测：为什么只把 Agent Worker 做成 Kubernetes 多副本还不等于 Production Ready？</summary>

因为长任务状态、Sandbox、Tool 副作用、Session 路由、Provider 配额、Checkpoint/Resume、Tenant Isolation、Trace/Eval 等都仍然需要独立的可靠性设计。
</details>