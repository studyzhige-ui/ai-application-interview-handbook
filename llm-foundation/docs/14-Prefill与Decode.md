# 14｜Prefill 与 Decode

## 1. 为什么要把一次推理拆成两个阶段

一个 Chat 请求通常先有一大段输入，再生成很多输出 Token。

这两个阶段的计算形态完全不同：

```text
Prefill
→ 处理已有 Prompt / Context

Decode
→ 每次生成一个新 Token
```

如果把它们混成一个“模型推理很慢”，就很难做性能分析。

---

## 2. Prefill 是什么

Prefill 会一次处理当前输入序列：

```text
System
+ History
+ RAG Context
+ User Input
```

并为这些 Token 建立模型中间状态，包括 KV Cache。

特点：

- 输入 Token 多；
- 大量矩阵计算；
- 并行度较高；
- 更偏 Compute-bound；
- 直接影响 Time To First Token。

---

## 3. Decode 是什么

Prefill 结束后开始逐 Token 生成。

每一步：

```text
new token
→ compute current hidden state / QKV
→ read historical KV Cache
→ choose next token
→ append KV
```

特点：

- 每步只有少量新 Token；
- 高度依赖历史 KV Cache；
- 逐步串行；
- 更容易受 Memory Bandwidth 影响；
- 决定生成速度。

---

## 4. 两种常见延迟指标

### TTFT

Time To First Token。

从请求发出到用户看到第一个生成 Token。

常受：

```text
Queue
+ Network
+ Tokenization
+ Prefill
+ First Decode
```

影响。

### TPOT / Inter-token Latency

Time Per Output Token，或相邻 Token 的生成间隔。

主要反映 Decode 阶段速度。

所以：

> TTFT 快，不代表长回答生成也快；反过来也一样。

---

## 5. 为什么 RAG 特别容易拉高 Prefill

RAG 往 Prompt 中注入多个 Chunk：

```text
User Query       200 tokens
System Prompt   1500
History         3000
RAG Context    12000
```

用户感觉“模型第一字很慢”，可能不是模型输出慢，而是 Prefill 处理大量 Retrieval Context。

因此 RAG Top-K、Chunk Size、Rerank 和 Context Build 都会影响 TTFT。

---

## 6. 为什么长输出主要拖 Decode

如果用户要求：

> 生成 3000 Token 的详细报告

那么即使 Prompt 很短，也要做大约 3000 次自回归 Decode Step。

所以控制：

- max output tokens；
- 回答长度；
- 是否需要完整长文；
- 是否分阶段生成；

都是成本 / 延迟设计。

---

## 7. Prefill / Decode Disaggregation

大规模 Serving 系统可能把 Prefill 和 Decode 分到不同资源池，因为：

```text
Prefill workload
≠
Decode workload
```

理论上可以分别优化：

- GPU 类型；
- Batch 策略；
- 调度；
- 网络 / KV 传输。

但这会引入：

- KV Cache 跨节点传输；
- 调度复杂度；
- 网络开销；
- Failure Recovery。

所以不是所有系统都应该分离。

---

## 8. Troubleshooting 方法

用户说“LLM 很慢”，先拆：

```text
Queue Time?
Network?
Prefill?
First Token?
Decode Rate?
Tool / RAG before model?
```

不要只看总请求耗时。

### 例子

- TTFT 高，TPOT 正常 → 看 Queue / Prefill / 大 Context；
- TTFT 正常，TPOT 高 → 看 Decode / GPU Saturation / Model Size；
- 两者都高 → 看系统负载、模型、资源与上下文。

---

## 9. 🎯 面试怎么回答

> LLM 推理通常分成 Prefill 和 Decode。Prefill 处理完整输入 Prompt，并建立历史 KV Cache，计算并行度较高，输入越长 TTFT 通常越高；Decode 则每步只新增一个 Token，反复读取 KV Cache 并逐 Token 自回归生成，更影响 TPOT 和长输出速度。Production 排查延迟时应该把 Queue、Prefill、Decode 分开，而不是只看一个总 latency。

---

## 10. ⚠️ 易错点

错误：

> 输入 Token 和输出 Token 对延迟的影响完全一样。

错误：

> Streaming 后 TTFT 和 Decode 都自然变快。

Streaming 主要让生成结果更早送达客户端。

---

<details>
<summary>自测：RAG Top-K 从 5 调到 50，为什么首先可能明显影响 TTFT？</summary>

因为注入的 Retrieval Context 大幅增加，Prefill 必须先处理更多输入 Token，才能开始产生第一个输出 Token。

</details>
