# 16｜PagedAttention、vLLM 与 Serving Engine

## 1. PagedAttention 想解决什么

KV Cache 很大，而且每个请求长度不断变化。

如果每个请求都要求一块连续显存：

```text
Request A: 先申请一大片
Request B: 再申请一大片
Request C: 长度继续增长
```

容易出现：

- 预留过多；
- 内存碎片；
- 可用显存明明还有，但缺少足够连续空间；
- 并发容量下降。

PagedAttention 的核心思想就是：

> **像操作系统分页一样，把 KV Cache 切成固定大小 Block，用逻辑连续、物理可分散的方式管理。**

---

## 2. 传统连续 KV 分配的问题

假设一个请求最大可能生成 4000 Token，但当前只生成到 300。

如果为了未来增长提前预留很大连续空间，会浪费。

如果只按当前长度分配，又需要频繁扩容和搬迁。

因此核心矛盾是：

```text
动态增长
+
高并发
+
大 KV Cache
+
显存昂贵
```

---

## 3. PagedAttention 的 Block 思想

把 KV Cache 划成固定 Block：

```text
Logical KV blocks:
A1 → A2 → A3

Physical memory:
Block 7
Block 21
Block 5
```

逻辑上属于同一请求，物理上不要求连续。

这样：

- 请求增长时再申请新 Block；
- 完成后归还 Block；
- 更容易复用空闲显存；
- 减少外部碎片和过度预留。

---

## 4. vLLM 为什么不只是“一个模型 API Server”

从应用工程视角，vLLM 这类 Serving Engine 主要解决：

```text
Model Loading
KV Cache Management
Continuous Batching
Request Scheduling
PagedAttention-style Memory Management
Streaming
Sampling
Parallel Serving
Metrics / Capacity
```

所以它位于：

```text
Application Backend
      ↓
Model Serving Engine
      ↓
GPU / Model Weights
```

不是 Agent Framework，也不是 RAG Framework。

---

## 5. SGLang 等 Serving / Runtime 为什么会出现

现代 LLM workload 不只是单次 Chat Completion。

还会出现：

- 共享 Prompt Prefix；
- Structured Generation；
- 多轮 Tool / Agent 调用；
- 多阶段推理；
- 大量重复 System Prompt；
- 多模型或多 Adapter。

因此 Serving 系统开始优化的不只是单次 kernel，而是：

> **整个 LLM Program / Request Graph 的执行效率。**

本模块只建立这一层认知，不进入具体 Runtime DSL。

---

## 6. Prefix Cache / KV Reuse

如果多个请求共享相同前缀：

```text
相同 System Prompt
+ 相同 Reference Context
+ 不同 User Question
```

Serving Engine 可能复用前缀计算。

收益：

- 降低重复 Prefill；
- 改善 TTFT；
- 节省算力。

但要处理：

- Prefix 精确匹配；
- Tenant Isolation；
- Cache Eviction；
- Model / Adapter Version；
- 安全边界。

---

## 7. Serving Engine 与 AI Backend 的职责边界

### Serving Engine

关心：

```text
GPU
Weights
KV Cache
Batch
Decode Scheduler
Tensor / Memory
```

### AI Backend

关心：

```text
User / Tenant
Auth
Rate Limit
Timeout
Retry
Provider Routing
SSE
Billing
Audit
Business State
```

不要把 vLLM 当成完整 AI Backend。

---

## 8. Production 选型问题

选 Serving Engine 时至少看：

- 支持模型；
- Hardware；
- Throughput / TTFT / TPOT；
- Long Context；
- Quantization；
- Prefix Cache；
- Structured Output；
- Multi-LoRA / Adapter；
- Distributed Serving；
- Metrics；
- 运维复杂度。

最终必须 Benchmark 自己的 workload，而不是只看公开榜单。

---

## 9. 🎯 面试怎么回答

> PagedAttention 的主要动机是更高效地管理动态增长的 KV Cache。它把 KV Cache 划成固定大小 Block，逻辑序列可以映射到非连续物理显存，减少连续预留和碎片，从而提高 GPU 上可承载的并发序列数。vLLM 这类 Serving Engine 会进一步结合 Continuous Batching、Request Scheduling、KV Cache 管理和 Streaming，把单模型推理变成可服务的高吞吐 Runtime。

---

## 10. ⚠️ 易错点

错误：

> PagedAttention 是一种新的 Transformer Attention 数学公式。

它更核心的是 Serving 时 KV Cache 的内存管理机制。

错误：

> 使用 vLLM 后就不需要 Backend 的限流、取消和多租户治理。

两层职责不同。

---

<details>
<summary>自测：PagedAttention 为什么能提高并发容量？</summary>

因为 KV Cache 不再要求为每个请求预留大块连续显存，而是按 Block 动态分配和复用，减少碎片与未使用预留，让有限显存容纳更多活跃序列。

</details>
