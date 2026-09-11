# 13. KV Cache、Prefill 与 Decode：LLM 推理的两阶段模型

如果只懂 Transformer，却不懂推理时的 **KV Cache / Prefill / Decode**，就很难解释：

```text
为什么长 Prompt 会让 TTFT 变慢？
为什么长输出特别耗时？
为什么并发时 KV Cache 会成为显存瓶颈？
为什么 Agent 的 Context 越长，Serving 越难？
```

这三个概念本来就是同一条推理链。

---

## 1. 为什么 Autoregressive Generation 会重复用历史 Token

每生成一个新 Token，都需要让当前位置 Attention 到之前的 Context。

假设已经有：

```text
Token 1 ... Token 1000
```

生成 Token 1001 时，会用到历史位置的 K / V。

生成 Token 1002 时，同样还会用到前 1001 个位置的 K / V。

如果每一步都重新计算历史所有 Token 的 K/V，会造成大量重复计算。

所以引出：

```text
KV Cache
```

---

## 2. KV Cache 缓存什么

在每一层 Attention 中，历史 Token 的 Key / Value 一旦计算完，在后续 Decode 中通常可以复用。

于是：

```text
Past Tokens
→ K/V tensors
→ cache

New Token
→ compute only new Q/K/V
→ attend to cached K/V
```

核心价值：

> **用显存换取 Decode 阶段少做大量重复计算。**

---

## 3. KV Cache 为什么会变成资源瓶颈

它的大小大致随以下因素增长：

```text
Batch / Concurrent Sequences
× Sequence Length
× Number of Layers
× KV Heads
× Head Dimension
× Precision
```

所以：

```text
Context 越长
并发越高
模型越深
```

KV Cache 占用越大。

这也是为什么超长上下文 Agent 在高并发 Serving 中很贵。

---

## 4. Prefill 是什么

第一次收到完整 Prompt：

```text
System + User + History + Retrieval + Tool Context
```

模型需要一次处理整个输入序列，为每个位置建立 Hidden State 和 KV Cache。

这个阶段叫：

```text
Prefill
```

它的特征是：

- 输入 Token 多；
- 大量矩阵计算可以并行；
- Context 越长，Prefill 越贵；
- 主要影响 TTFT。

---

## 5. Decode 是什么

Prefill 完成后，开始逐 Token 生成：

```text
next token
→ append
→ next token
→ append
```

每一步通常只处理新 Token，但要读取历史 KV Cache。

Decode 的特征：

- 严格 Autoregressive；
- 每步计算量较小但次数很多；
- 常更受 Memory Bandwidth / KV Cache 访问影响；
- 主要影响 TPOT / Tokens per second。

---

## 6. Prefill 和 Decode 为什么性能特征不同

可以简单记：

| 阶段 | 主要输入 | 特征 | 典型用户指标 |
|---|---|---|---|
| Prefill | 整段 Prompt | 计算密集、并行度高 | TTFT |
| Decode | 每次 1 个新 Token | 串行依赖、KV 访问重 | TPOT / Output TPS |

因此一个 Serving Engine 会对两种阶段做不同优化。

---

## 7. TTFT 与 TPOT

### Time To First Token

```text
Request arrival
→ Queue
→ Prefill
→ First Token
```

TTFT 受：

- Prompt Length；
- Queue；
- Prefill Batch；
- Model Size；
- Hardware；

影响。

### Time Per Output Token

首 Token 后：

```text
Token 2
Token 3
...
```

平均每个输出 Token 的耗时常用 TPOT 观察。

所以：

```text
长 Prompt → TTFT 压力
长 Output → TPOT × Token Count
```

---

## 8. 为什么长 Context 会同时拖累体验和容量

长 Context 不只是多付 Input Token 钱。

还意味着：

```text
Prefill Compute ↑
KV Cache ↑
TTFT ↑
GPU Memory Pressure ↑
Max Concurrent Sequences ↓
```

所以 Agent Harness 做 Compaction / Tool Result Offloading，不只是为了防止硬 Context Overflow，也是在治理 Serving Capacity。

---

## 9. Prefix / Prompt Cache 的直觉

很多请求可能共享相同前缀：

```text
same system prompt
same tool definitions
same long document prefix
```

如果 Serving Provider 支持 Prefix / Prompt Cache，可以复用部分前缀计算或缓存结果，降低重复 Prefill 成本。

但具体缓存粒度、生命周期和计费依 Provider / Engine 而异。

应用层只需掌握：

> **稳定前缀有潜在复用价值，因此 Context Assembly 的顺序和稳定性可能影响 Cache Hit。**

---

## 10. KV Cache 和 Application Cache 不是一回事

### KV Cache

```text
模型推理内部
保存历史 Attention K/V Tensor
```

### Response Cache / Semantic Cache

```text
应用层
保存整个请求结果或语义相近请求结果
```

两者层级完全不同。

---

## 11. GQA / MQA 为什么和 KV Cache 有关

传统 Multi-Head Attention 每个 Head 都有独立 K/V，会让 Cache 很大。

MQA / GQA 通过让多个 Query Head 共享更少的 KV Head，降低：

```text
KV Cache Memory
Memory Bandwidth
```

这是现代 Serving 中很重要的模型架构优化。

应用工程师不必推导完整矩阵，但需要理解：

> 模型 Attention Architecture 会影响 Serving Memory Footprint。

---

## 12. Streaming 和 Decode

API Streaming 通常是在 Decode 产生 Token 后尽快把它推给客户端：

```text
Decode Token
→ Server Event / Chunk
→ Client render
```

Streaming 不会让模型本身总生成时间消失，但可以显著改善：

```text
Perceived Latency
```

所以 AI Backend 会关心 TTFT 和 Stream Backpressure。

---

## 13. 常见错误

- KV Cache 缓存的是模型最终答案：错误。
- KV Cache 让 Decode 完全不需要 Attention：错误，仍要让新 Query 读取历史 K/V。
- Prefill 和 Decode 性能完全一样：错误。
- Context Window 越大只影响输入费用：还影响 Prefill 和 KV Cache。
- Streaming 能降低模型总 Decode 计算量：通常不能，它主要改善用户感知。

---

## 14. 面试怎么答

### Q：KV Cache 为什么能加速 LLM 推理？

> Autoregressive Decode 每一步都会再次用到历史 Token 的 Key/Value。KV Cache 保存各层历史 K/V，使新 Token 只计算自己的新 K/V，再读取缓存进行 Attention，避免每一步重新计算整个历史序列。代价是显存占用随序列长度和并发增长。

### Q：Prefill 和 Decode 有什么区别？

> Prefill 一次处理完整 Prompt，计算并行度高、主要影响 TTFT；Decode 逐 Token 生成，有严格串行依赖并反复读取 KV Cache，主要影响 TPOT 和输出吞吐。两阶段的瓶颈和 Serving 优化策略不同。

---

## 15. 自测

<details><summary>1. 为什么长 Context 会降低可承载并发？</summary>
因为每个请求的 KV Cache 更大，占用更多 GPU Memory，使同时可驻留的 Sequence 数减少。
</details>

<details><summary>2. 为什么 Output 很长时主要看 Decode 而不是 Prefill？</summary>
因为每个输出 Token 都要进行一个新的 Autoregressive Decode Step，数量随输出长度线性增加。
</details>

<details><summary>3. KV Cache 和 Redis Semantic Cache 有什么根本区别？</summary>
前者是模型内部 Attention 中间张量缓存，后者是应用层结果复用机制。
</details>
