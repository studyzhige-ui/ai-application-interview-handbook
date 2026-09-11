# 13｜KV Cache

## 1. KV Cache 为什么存在

Autoregressive Generation 每次只新增一个 Token。

如果第 1001 个 Token 生成时，重新把前 1000 个历史 Token 的 Attention K/V 全算一遍，会产生大量重复计算。

KV Cache 的核心就是：

> **把历史 Token 在每层 Attention 中已经计算出的 K / V 保存下来，后续新 Token 直接复用。**

---

## 2. 没有 KV Cache 会怎样

假设已有：

```text
T1 T2 T3 ... T1000
```

生成 T1001 时需要历史上下文。

没有 Cache：

```text
重新计算 T1...T1000 的 K/V
→ 再算 T1001
```

生成 T1002 又重复一次。

这种重复对长序列非常昂贵。

---

## 3. 有 KV Cache 后

Prefill 阶段先计算：

```text
K1, V1
K2, V2
...
K1000, V1000
```

并缓存。

Decode 新 Token 时只新增：

```text
K1001, V1001
```

当前 Q 去查询：

```text
[K1...K1001]
[V1...V1001]
```

历史 K/V 不需要重复投影计算。

---

## 4. 为什么缓存 K/V 而不是所有东西

未来新 Token 做 Attention 时，需要：

```text
current Q
×
historical K
→ attention weights
→ historical V
```

所以历史 K/V 会被后续重复访问。

当前 Q 只服务当前 Token，不需要作为未来历史查询库长期保存。

---

## 5. KV Cache 的代价：显存

KV Cache 不是免费优化。

它的规模会随以下因素增长：

```text
Layers
× KV Heads
× Head Dimension
× Sequence Length
× Precision Bytes
× Concurrent Sequences
```

因此：

> Context 越长、并发越高，KV Cache 显存压力越大。

这就是 Long Context 和 Serving Capacity 强耦合的原因。

---

## 6. MHA / MQA / GQA 为什么影响 KV Cache

标准 MHA 中多个 Attention Head 有独立 K/V。

MQA / GQA 通过共享更少的 K/V Head，降低：

- KV Cache 容量；
- Memory Bandwidth；
- Decode 压力。

因此模型架构本身也会影响同样 GPU 上能承载多少并发请求。

---

## 7. Prefix Cache / Prompt Cache 与 KV Cache

需要区分几个概念。

### KV Cache

通常指一个正在生成请求的历史 Attention K/V 状态。

### Prefix / Prompt Cache

如果多个请求共享相同前缀，Serving 系统可能复用已经计算过的前缀状态，减少重复 Prefill。

例如：

```text
相同 System Prompt
+ 相同大型静态文档前缀
```

可以存在复用机会。

但缓存命中、隔离、安全与 Provider 实现各不相同。

---

## 8. KV Cache 与 Agent Context

Agent 长任务可能拥有很长 History / Tool Result。

这会同时带来：

```text
Context Token ↑
→ Prefill Cost ↑
→ KV Cache Memory ↑
→ 并发 Capacity ↓
```

所以 Agent Compaction 不只是“防止超过 Context Window”，也会影响 Serving 成本。

---

## 9. Failure / Production 视角

### 9.1 请求过长导致显存占用异常

长上下文 + 高并发可能导致：

- OOM；
- 排队；
- KV Cache Eviction；
- Throughput 下降。

### 9.2 Cache Fragmentation

不同请求长度不同，传统连续内存管理容易浪费空间。

PagedAttention 就是后面要解决的问题之一。

### 9.3 Session Cache 不是长期状态

不要把 GPU 上的 KV Cache 当业务持久化 Memory。

实例重启 / 调度后它可能不存在。

---

## 10. 🎯 面试怎么回答

> KV Cache 缓存历史 Token 在每层 Attention 中的 K 和 V，避免自回归 Decode 时每生成一个新 Token 都重新计算完整前缀。它显著降低重复计算，但会占用大量显存，规模随层数、KV Head、维度、序列长度和并发请求增长。Long Context、高并发、GQA/MQA、PagedAttention 和 Serving Capacity 都与 KV Cache 强相关。

---

## 11. ⚠️ 易错点

错误：

> KV Cache 是缓存模型输出文本。

它缓存的是 Attention 中间状态 K/V。

错误：

> KV Cache 只会提升性能，没有代价。

代价主要是显存与内存带宽。

错误：

> KV Cache 就是 Agent Memory。

完全不是同一个层次。

---

<details>
<summary>自测：Context 长度翻倍为什么可能显著影响 Serving 并发？</summary>

因为单请求需要保存更多历史 Token 的 K/V，KV Cache 占用增加，同一 GPU 能同时容纳的活跃序列数量可能下降。

</details>
