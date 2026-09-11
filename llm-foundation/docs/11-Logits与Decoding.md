# 11｜Logits、Softmax 与 Decoding

## 1. 模型最后输出的不是“文字”

Transformer 最后一层会得到 hidden state，再经过 LM Head 映射到词表维度：

```text
hidden state
  ↓
LM Head
  ↓
logits over vocabulary
```

如果词表有 100k 个 Token，那么当前位置就会得到约 100k 个分数。

这些原始分数叫 Logits。

---

## 2. Logits 不是概率

Logits 可以是任意实数。

经过 Softmax 后才得到概率分布：

```text
p_i = exp(z_i) / Σ exp(z_j)
```

于是：

```text
Token A  0.52
Token B  0.20
Token C  0.07
...
```

Decoding 再从这个分布里选一个 Token。

---

## 3. Greedy Decoding

最简单方式：

```text
argmax(probability)
```

每一步都选概率最高 Token。

优点：

- 简单；
- 稳定；
- 不引入额外采样随机性。

问题：

- 可能局部最优；
- 文本较僵硬；
- 不能探索其它高概率路径。

---

## 4. Sampling

Sampling 不是总选 Top-1，而是从概率分布抽样。

它让生成具有多样性，但也带来波动。

因此不同任务需要不同 Decoding：

```text
代码 / JSON / 抽取
→ 更偏确定性

创意文案 / Brainstorm
→ 可以更高随机性
```

具体还要结合模型和 Provider 实现。

---

## 5. 为什么局部概率最高不代表整句最好

Greedy 每一步只看当前最优 Token。

一个序列的整体概率是多步条件概率的组合：

```text
P(x1, x2, ..., xn)
= Π P(xt | x<t)
```

所以局部选择并不保证全局序列质量最好。

传统生成任务会讨论 Beam Search，但现代开放式 LLM Chat 更常见的是各种 Sampling 策略。

---

## 6. Logit Bias / Constrained Decoding

有些系统允许在生成阶段：

- 提高 / 降低某些 Token 分数；
- 约束 JSON Grammar；
- 强制结构化输出；
- 限制可选 Token 集合。

关键思想是：

> Structured Output 不一定只是“Prompt 里说请返回 JSON”，更可靠的方法可以在 Decoding 层约束允许生成的 Token。

具体 Provider 能力归具体 API 文档，不写死在本课程里。

---

## 7. 为什么 Softmax 概率不等于事实置信度

一个 Token 概率高，只说明：

> 在当前模型和上下文下，它是高概率续写。

不等于：

- 这个事实是真的；
- 模型经过外部验证；
- 概率可以直接当业务置信度。

这点和 Hallucination 非常重要。

---

## 8. 🎯 面试怎么回答

> LLM 最后一层先产生词表维度的 logits，它们是未归一化分数；Softmax 把 logits 转为下一 Token 的概率分布。Decoding 再决定从这个分布怎样选 Token，比如 greedy 直接取最高概率，sampling 则按分布抽样。模型 Token 概率表达的是续写概率，不等同于事实正确率或业务置信度。

---

## 9. ⚠️ 易错点

错误：

> Logit 就是概率。

错误：

> 模型说某答案概率高，所以事实可信。

错误：

> 返回 JSON 只靠 Prompt 就能保证。

更可靠的系统可能使用 Schema / Grammar / Constrained Decoding。

---

<details>
<summary>自测：为什么 Token 概率高不能直接当事实置信度？</summary>

因为模型优化的是条件续写概率，而不是对外部世界事实做经过校验的概率估计；高概率错误仍然可能非常“自信”。

</details>
