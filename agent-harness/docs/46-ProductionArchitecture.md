# 46｜Production Agent Runtime Architecture

## 1. 从单进程 Demo 开始

Demo：

```text
FastAPI
  ↓
while loop
  ↓
LLM + local tools
```

Production 很快遇到：长任务、审批、多用户、崩溃恢复、Sandbox、并发和成本。

## 2. 通用组件图

```text
Client / API
    │
    ▼
Session / Run Service
    │
    ▼
Stateless Harness Worker
 ┌──┼───────────┐
 ▼  ▼           ▼
Model Router  Tool Gateway  Context/Memory
               │
               ▼
       Sandbox / Remote Hands

Durable Event / State Store
Artifact Store
Trace / Eval Pipeline
Queue / Scheduler / Quota
```

Anthropic Managed Agents 的 brain / hands / durable session 解耦提供了很好的成熟参考；这里抽象成通用架构。

## 3. 为什么 Harness Worker 尽量 Stateless

Runtime state 外置后：

- worker crash 可恢复；
- 横向扩容；
- run 可迁移；
- execution environment 可独立生命周期。

不是所有实现必须完全 stateless，但 durable truth 不应只在进程内。

## 4. Queue / Backpressure

长 Agent 不应占住 HTTP request：

```text
submit run
→ queue
→ worker
→ event stream
```

需要 per-user quota、global concurrency、provider rate limit 和 sandbox pool capacity。

## 5. Tenant Isolation

隔离：

```text
state
memory
workspace
credentials
tool catalog
trace/artifact
```

## 6. SLO

不仅 API latency：

- time to first useful event；
- task completion time；
- success rate；
- recovery time；
- cost per successful task。

## 🎯 面试

Production Agent 我会把 API、durable Run/Session、stateless Harness worker、Model Router、Tool Gateway、Sandbox pool、State/Event store、Artifact、Trace/Eval 和 Queue/Quota 分开。长任务异步执行并流式返回事件，所有 tenant state/credential/workspace 隔离。

<details><summary>自测：为什么不让每个 Agent Worker 永久绑定一个 Container？</summary>

会提高启动与资源成本，也把 Harness 生命周期和 execution environment 耦合。是否解耦取决于场景，但大规模系统通常希望独立伸缩。
</details>
