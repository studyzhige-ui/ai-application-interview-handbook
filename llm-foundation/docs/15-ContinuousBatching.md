# 15｜Batching 与 Continuous Batching

## 1. 为什么 Serving 要做 Batch

GPU 擅长大规模并行矩阵计算。

如果每个请求单独执行：

```text
Request A → GPU
Request B → 等待
Request C → 等待
```

GPU 利用率可能很差。

Batching 的思路是：

> 把多个请求组合起来一起算，让 GPU 更充分工作。

---

## 2. Static Batching 的问题

传统静态 Batch 会把一组请求绑在一起。

但 LLM 请求长度差异很大：

```text
A 输出 20 Token
B 输出 200 Token
C 输出 1000 Token
```

如果 Batch 必须等最慢请求结束：

```text
A 已完成，但位置还占着
B 已完成，但位置还占着
C 继续生成
```

就会浪费资源。

---

## 3. Continuous Batching

Continuous Batching 的核心：

> 请求可以动态进入和退出正在运行的 Batch。

例如：

```text
Step 1: A B C
Step 2: A 完成 → D 进入
Step 3: B 完成 → E 进入
```

这样可以持续把活跃请求塞进 GPU，提升吞吐。

---

## 4. 为什么 LLM 特别适合 Continuous Batching

Decode 本来就是一轮一轮进行：

```text
每个活跃请求
→ 生成下一个 Token
```

所以 Scheduler 可以在每轮 Decode 重新决定：

- 哪些请求继续；
- 哪些新请求加入；
- 哪些请求因为 KV Cache / Token Budget 暂停；
- 哪些请求取消。

这就是 Serving Engine 的重要职责之一。

---

## 5. Throughput 和 Latency 的冲突

更大的 Batch 往往提高 GPU 利用率和总体吞吐，但也可能增加单请求等待。

因此系统需要权衡：

```text
Throughput
vs
TTFT
vs
TPOT
vs
Fairness
```

不能只追求 QPS。

---

## 6. Batch 中的长度不一致

不同请求可能有：

- 不同 Prompt Length；
- 不同 Output Length；
- 不同 Sampling 参数；
- 不同模型 Adapter；
- 不同优先级。

Serving Engine 需要处理这些异构请求，否则 Padding 和资源碎片会很严重。

---

## 7. 与 KV Cache 的关系

Continuous Batching 需要动态管理每个请求自己的 KV Cache。

于是出现新的问题：

```text
请求进入 / 退出
→ KV Block 分配 / 释放
→ 内存碎片
→ 容量调度
```

这正是 PagedAttention 一类技术的工程背景。

---

## 8. AI Backend 的边界

Model Server 内部负责：

```text
GPU Batch Scheduling
KV Cache
Decode Scheduling
```

外部 AI Backend 仍然负责：

```text
Admission Control
Tenant Quota
Rate Limit
Timeout
Cancellation
Priority
Retry
Circuit Breaker
```

两层调度不能混为一谈。

---

## 9. 🎯 面试怎么回答

> Batching 是为了提高 GPU 利用率，但 LLM 请求输出长度差异很大，静态 Batch 容易因为短请求等待长请求而浪费资源。Continuous Batching 允许在每个推理 step 动态加入新请求、移除已完成请求，从而提高吞吐。它需要和 KV Cache 内存管理、请求调度、TTFT / TPOT 公平性一起设计。

---

## 10. ⚠️ 易错点

错误：

> Batch 越大，单请求延迟一定越低。

通常吞吐和延迟需要权衡。

错误：

> Continuous Batching 就是 Backend 把多个 HTTP 请求合并。

这里主要指 Model Serving Engine 内部的推理调度。

---

<details>
<summary>自测：为什么静态 Batch 在 LLM Decode 中特别容易浪费？</summary>

因为不同请求生成长度不同，短请求完成后如果不能动态释放并让新请求进入，它们原本占用的 Batch / KV 资源会闲置直到整个 Batch 结束。

</details>
