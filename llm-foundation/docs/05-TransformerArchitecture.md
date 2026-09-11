# 05｜Transformer Architecture 总览

## 1. 先讲人话

现代 LLM 可以先粗略理解成：

```text
Token IDs
  ↓
Token Embedding + Position
  ↓
Transformer Block × N
  ↓
Final Hidden State
  ↓
Linear / LM Head
  ↓
Logits
```

每个 Block 又大致包含：

```text
Self-Attention
→ Residual
→ Normalization
→ FFN
→ Residual
→ Normalization
```

具体模型在 Norm 前后顺序、Attention 变体、FFN 激活等细节上会不同，但这条主干非常稳定。

---

## 2. Transformer 解决什么

语言模型的核心任务可以简化成：

> 给定前面 Token，预测下一个 Token。

为了做好这件事，模型需要让每个位置形成“结合上下文后的表示”。

Transformer 通过 Self-Attention 让 Token 之间建立依赖，再通过 FFN 对每个位置的表示做非线性变换。

---

## 3. Decoder-only LLM

很多生成式 LLM 使用 Decoder-only 架构。

关键约束：

```text
位置 i
只能看见
位置 <= i 的 Token
```

这样训练时和生成时都符合“根据过去预测未来”的自回归目标。

这个限制通过 Causal Mask 实现，后面单独讲。

---

## 4. 一个 Block 在做什么

可以把一个 Block 直观理解为两步。

### Step 1：Attention

问：

> 当前 Token 应该关注前文哪些 Token？

### Step 2：FFN

问：

> 聚合完上下文后，这个位置的表示怎样进一步变换？

然后堆很多层：

```text
局部表示
→ 更多上下文关系
→ 更抽象表示
→ 最终用于预测下一个 Token
```

---

## 5. Residual 与 Normalization 为什么重要

深层网络如果每一层都完全覆盖前一层的信息，很难稳定训练。

Residual Connection 允许：

```text
output = input + transformation(input)
```

让信息和梯度更容易沿深层网络传递。

Normalization 则帮助控制激活尺度、稳定计算。

应用工程师不需要推导训练稳定性证明，但应该知道它们不是“装饰模块”。

---

## 6. 为什么 Transformer 取代传统 RNN 成为大模型主流

应用层最重要的直觉有两个：

### 6.1 训练阶段并行性更好

训练时已知完整序列，可以对多个位置同时做矩阵运算，而不必像经典 RNN 那样严格一步一步传播隐藏状态。

### 6.2 Attention 能直接建立远距离关系

一个 Token 可以直接关注较远位置，不必把信息逐步穿过很多时间步。

但注意：

> 生成阶段仍然是 Autoregressive，输出 Token 还是逐步产生。

这就是为什么“Transformer 并行”与“LLM 生成逐 Token”并不矛盾。

---

## 7. Transformer 与 Context Window 的关系

输入序列长度会直接影响 Attention 工作量与 KV Cache 大小。

所以 Context Window 不只是产品参数，它会继续影响：

- Prefill 延迟；
- 显存；
- Serving 并发；
- 长上下文质量。

后面 KV Cache 和 Serving 会把这条链补完整。

---

## 8. 🎯 面试怎么回答

> Transformer LLM 通常先把 Token ID 映射成向量并加入位置信息，再经过多层 Transformer Block。每个 Block 的核心是 Self-Attention 和 FFN，并通过 Residual 与 Normalization 保持深层网络稳定。Decoder-only LLM 使用 Causal Mask，只允许当前位置关注过去 Token，从而完成 next-token prediction。Attention 负责跨 Token 关系，FFN 负责每个位置的非线性表示变换。

---

## 9. ⚠️ 易错点

错误：

> Transformer 就等于 Attention。

Transformer Block 还包括 FFN、Residual、Normalization、Position 等关键机制。

错误：

> Transformer 可以并行，所以生成也能一次把整句话生成出来。

训练与 Prefill 可以高度并行，但自回归 Decode 仍依赖前一个新 Token。

---

<details>
<summary>自测：Attention 和 FFN 的职责有什么区别？</summary>

Attention 主要在不同 Token 位置之间聚合上下文信息；FFN 主要对每个位置的表示做非线性特征变换。

</details>
