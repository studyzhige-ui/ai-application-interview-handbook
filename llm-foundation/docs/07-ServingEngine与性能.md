# 07｜LLM Serving Engine：Continuous Batching、PagedAttention、Latency、Cost 与 Quantization

单请求能跑起来，不等于模型服务能承载 Production 流量。

Serving Engine 真正解决的是：

```text
很多请求长度不同
→ 同时到达 / 同时生成
→ KV Cache 大小不同
→ GPU 资源有限
→ 怎样调度、分配内存并达到好的 Throughput / Latency / Cost？
```

因此 Batching、PagedAttention、性能指标和 Precision/Quantization 应该在同一个 Serving 系统里理解。

---

## 1. 为什么普通 Static Batch 不适合在线生成

假设一个 Batch 有三个请求：

```text
A → 20 output tokens
B → 200 output tokens
C → 800 output tokens
```

如果用固定 Batch 生命周期：

```text
A 很早结束
但资源可能要等 B/C
```

不同请求生成长度高度不一致，会造成 GPU Slot 浪费。

---

## 2. Continuous Batching 的核心思想

不把 Batch 当成“从开始到结束固定的一组请求”，而是动态调度：

```text
Request A finishes
→ immediately free slot
→ admit Request D
```

因此：

```text
Batch membership changes continuously
```

它提高 GPU 利用率和系统吞吐，尤其适合 Autoregressive Decode。

---

## 3. 为什么 Decode 更适合动态 Batch

每个请求 Decode 都是在循环：

```text
produce one token
→ update sequence
→ next iteration
```

不同请求可以在同一轮 GPU Forward 中批量执行当前 Decode Step。

但它们：

- Sequence Length 不同；
- KV Cache 大小不同；
- Stop 时间不同。

所以 Scheduler 必须持续管理 Active Sequence。

---

## 4. KV Cache 传统连续内存的问题

如果每个 Sequence 预留一个大连续 KV Buffer：

```text
request A reserves max length
request B reserves max length
...
```

会出现：

- Internal Fragmentation；
- 预留但没用的空间；
- Sequence 长度不可预测；
- Batch 动态变化时难管理。

这会限制并发。

---

## 5. PagedAttention 的核心直觉

PagedAttention 借鉴虚拟内存分页思想，把 KV Cache 切成固定大小 Block/Page：

```text
Logical KV Sequence
→ Block Table
→ Physical KV Blocks
```

因此一个 Sequence 不必占用物理连续的大块显存。

好处包括：

- 减少 Fragmentation；
- 按需分配 KV Block；
- 更方便动态 Sequence；
- 更容易共享某些 Prefix Block；
- 提高可驻留 Batch 数。

重要的是思想，不要把 PagedAttention 等同于“Attention 算法本身变成另一种数学公式”。

---

## 6. Serving Scheduler 还要做什么

除了 Continuous Batching，还要处理：

```text
Queueing
Admission Control
Prefill vs Decode Scheduling
Priority
Max Batch Tokens
KV Cache Pressure
Preemption / Swap（依实现）
Cancellation
Timeout
```

所以一个 Serving Engine 是完整 Runtime，不只是模型 Forward Wrapper。

---

## 7. 四个最重要的在线指标

### TTFT

Time To First Token：

```text
request arrival
→ queue
→ prefill
→ first token
```

### TPOT

Time Per Output Token：首 Token 后平均每个 Decode Token 的间隔。

### Throughput

可以看：

```text
requests/s
tokens/s
```

### End-to-end Latency

从请求到全部输出结束。

不同产品场景看重的指标不同。

---

## 8. 为什么 Throughput 和 Latency 会冲突

更大的 Batch 往往：

```text
GPU 利用率 ↑
Throughput ↑
```

但如果为了凑 Batch 让请求排队：

```text
TTFT ↑
```

所以 Production 需要在：

```text
User Latency SLA
vs
GPU Utilization / Cost
```

之间选择 Operating Point。

---

## 9. Capacity 不是“GPU 能不能放下模型”

至少还要容纳：

```text
Model Weights
KV Cache
Activation / Workspace
CUDA Runtime / Kernel Buffer
Batch Temporary Memory
```

模型 Weight 能放进 GPU，并不代表长 Context 高并发也能服务。

KV Cache 经常决定：

```text
Max Concurrent Sequences
```

---

## 10. Precision 为什么影响 Serving

模型权重可以采用不同精度：

```text
FP32
FP16 / BF16
INT8
INT4
...
```

更低 Precision 通常可以减少：

- Weight Memory；
- Memory Bandwidth；
- 某些硬件上的计算成本。

但也可能影响：

- Quality；
- Numerical Stability；
- Kernel Support；
- Hardware Compatibility。

---

## 11. Quantization 不是“压缩模型就结束”

常见区分：

```text
Weight-only Quantization
Weight + Activation Quantization
KV Cache Quantization
```

以及：

```text
Post-training Quantization
Quantization-aware Training
```

不同方案对质量、速度、硬件支持不同。

应用工程师需要关注的是：

> **量化到底降低了哪部分 Memory / Compute，是否真的提升目标硬件上的 Throughput，以及业务质量下降多少。**

---

## 12. Model Size、Context、Output 对成本的不同影响

### 更大 Model

```text
Weights ↑
Compute per token ↑
```

### 更长 Input

```text
Prefill ↑
KV Cache ↑
TTFT ↑
```

### 更长 Output

```text
Decode Steps ↑
End-to-end Latency ↑
Output Cost ↑
```

所以 Cost Optimization 不是只换小模型。

---

## 13. Provider API 场景怎么理解 Serving

即使你不自建 vLLM，也应该懂这些机制。

因为 Provider API 的：

- TTFT；
- Rate Limit；
- Context Pricing；
- Cached Input Pricing；
- Batch API；
- Model Tier；

背后仍然受类似 Serving Economics 影响。

理解 Runtime 能帮助你正确做：

```text
Model Routing
Context Budget
Output Limit
Concurrency Limit
Cost Estimation
```

---

## 14. Benchmark 应该怎么做

不要只测：

```text
one request, prompt=128, output=32
```

Production Benchmark 应覆盖真实分布：

```text
Short / Medium / Long Prompt
Short / Long Output
Concurrent Requests
Prefill-heavy
Decode-heavy
不同 Model / Precision
不同 Context Length
```

同时记录：

```text
TTFT
TPOT
P95/P99 End-to-end
Tokens/s
GPU Memory
GPU Utilization
Cost/request
```

---

## 15. 常见错误

- Continuous Batching 就是普通固定 Batch：错。
- PagedAttention 是新的 Attention 数学公式：不是，它主要是 KV Cache 内存管理思想。
- 模型能放进 GPU 就表示可以高并发服务：错。
- Quantization 一定让所有硬件都更快：错，要看 Kernel/Hardware。
- Throughput 越高用户体验越好：可能 TTFT 已经恶化。
- 只优化 Input Token，不控制 Output：长 Output 的 Decode Cost 可能更大。

---

## 16. 面试怎么答

### Q：Continuous Batching 为什么能提高 LLM Serving 吞吐？

> 在线生成请求长度不同、结束时间不同。Continuous Batching 会在某个 Sequence 完成后立即回收 Slot 并加入新请求，而不是等待固定 Batch 全部结束，从而让 GPU 持续保持更高利用率。

### Q：PagedAttention 解决什么问题？

> 它把 KV Cache 按 Block/Page 管理，通过 Logical-to-Physical Block Mapping 避免每个 Sequence 预留大块连续显存，减少 Fragmentation，提高 KV Cache 利用率和可驻留并发数。

### Q：LLM Serving 该看哪些性能指标？

> 至少分 TTFT、TPOT、End-to-end Latency、Request/Token Throughput、GPU Memory/Utilization 和单位成本，同时用真实 Prompt/Output 长度与并发分布压测，因为 Throughput 与用户延迟通常存在权衡。

---

## 17. 自测

<details><summary>1. 为什么 Continuous Batching 比 Static Batch 更适合 Autoregressive Serving？</summary>
因为不同请求生成长度和结束时间不同，动态移入移出请求能减少空闲 Slot。
</details>

<details><summary>2. PagedAttention 为什么能提高并发？</summary>
因为 KV Cache 不再要求大块连续预留，按需 Block 分配减少碎片和浪费。
</details>

<details><summary>3. 为什么 Quantization 不能只比较模型文件大小？</summary>
因为真正价值要看目标硬件上的 Kernel 支持、Throughput、Latency、Memory 和业务质量损失。
</details>
