# 18｜Precision / Quantization 与部署边界

## 1. 为什么精度格式会影响部署

模型权重本质上是大量数值参数。

如果参数更多、每个参数占用字节更多：

```text
Model Memory ↑
Load Time ↑
Memory Bandwidth ↑
Deployment Cost ↑
```

因此推理系统会使用不同数值精度：

```text
FP32
FP16 / BF16
INT8
INT4
以及其它更低精度方案
```

---

## 2. 一个最基本的容量直觉

假设模型有 N 个参数。

仅看权重粗略估算：

```text
Memory ≈ N × bytes_per_parameter
```

例如：

```text
FP32 → 4 bytes
FP16 / BF16 → 2 bytes
INT8 → 1 byte
INT4 → 0.5 byte（粗略）
```

实际部署还要额外考虑：

- KV Cache；
- Runtime buffer；
- CUDA / framework overhead；
- Tensor Parallel 通信；
- Quantization metadata。

所以不能拿“参数数 × 字节”直接当最终显存需求。

---

## 3. FP16 与 BF16

两者都是 16-bit 浮点，但指数位和尾数位分配不同。

应用工程层需要知道：

- 都能显著减少相对 FP32 的内存；
- BF16 通常拥有更大的数值范围；
- Hardware 支持会影响性能；
- 训练 / 推理生态可能偏好不同格式。

不需要为本岗位死背 IEEE 位布局。

---

## 4. Quantization 是什么

Quantization 的基本目标：

> 用更低 bit 表示模型权重或激活，在尽量保持效果的前提下降低内存和计算 / 带宽成本。

例如：

```text
16-bit weights
→ 8-bit
→ 4-bit
```

但这不是无损压缩。

---

## 5. Weight-only vs Weight + Activation

不同量化方案可能只量化：

- Weights；

也可能同时处理：

- Activations；
- KV Cache。

它们对：

```text
Memory
Kernel Support
Latency
Accuracy
Hardware Compatibility
```

影响不同。

所以面试时不要说：

> “INT4 模型就是所有计算都用 4 bit。”

---

## 6. PTQ 与 QAT

### Post-Training Quantization

训练完成后再量化。

优点：

- 成本低；
- 上手快；
- 很适合应用部署试验。

### Quantization-Aware Training

训练阶段就让模型适应量化误差。

可能获得更好的低精度效果，但训练成本更高。

应用岗重点理解边界，不必深入训练算法。

---

## 7. 为什么量化不一定更快

量化通常会降低显存占用，但速度收益取决于：

- GPU 是否有高效低精度 Kernel；
- 反量化开销；
- Batch Size；
- Model Architecture；
- Memory-bound 还是 Compute-bound；
- Serving Engine 支持。

因此：

> “模型更小”不自动等于“端到端延迟一定更低”。

必须 Benchmark。

---

## 8. 质量下降会表现在哪里

量化误差可能影响：

- Perplexity；
- Reasoning；
- Coding；
- Long Context；
- Function Calling；
- Structured Output；
- 多语言；
- 小概率边界 Case。

所以不能只跑几个 Demo 就宣布“无损”。

Production 应用要用真实 Evaluation Set 回归。

---

## 9. Quantization 与 KV Cache

即使权重量化得很小：

```text
Long Context + High Concurrency
```

仍可能让 KV Cache 成为主要显存消费者。

一些系统也会探索 KV Cache Quantization，但它有自己的精度和 Kernel Trade-off。

因此容量规划必须分：

```text
Model Weights
+
KV Cache
+
Runtime Overhead
```

---

## 10. 应用工程什么时候考虑量化

典型触发条件：

- 单卡放不下；
- 希望提高并发；
- 成本过高；
- 边缘部署；
- Self-hosting 资源有限；
- 大模型性能远超业务需求，愿意交换少量质量。

正确流程：

```text
建立 FP16/BF16 Baseline
→ 选择量化方案
→ 跑真实任务 Evaluation
→ 测 TTFT / TPOT / Throughput / Memory
→ 再决定是否上线
```

---

## 11. 🎯 面试怎么回答

> Precision 决定权重和中间状态的数值表示成本。Quantization 用 INT8、INT4 等更低精度表示模型，主要目标是降低显存和带宽，并可能提高吞吐，但会引入量化误差。它是否真正加速取决于硬件和 Kernel；质量是否可接受也必须用真实任务回归。部署时还要把模型权重和 KV Cache 分开算，不能认为权重量化后显存问题就全部解决。

---

## 12. ⚠️ 易错点

错误：

> INT4 模型全部运算都是 4 bit。

错误：

> Quantization 一定加速。

错误：

> 模型能正常聊天就说明量化无损。

---

<details>
<summary>自测：为什么权重量化后 Long Context 场景仍可能 OOM？</summary>

因为 KV Cache 会随着序列长度和并发增长；即使权重明显变小，KV Cache 与其它 Runtime Buffer 仍可能占据大量显存。

</details>
