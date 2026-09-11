# 10. Autoregressive Generation：Logits、Softmax、Sampling 与 Decoding

理解 LLM 输出最重要的一条链是：

```text
Context
→ Transformer Forward
→ Logits
→ Probability Distribution
→ Decoding / Sampling
→ Next Token
→ append to context
→ repeat
```

所以原来的 Autoregressive、Logits 和 Sampling 应该在同一章学习。

---

## 1. Autoregressive 是什么

LLM 生成文本时不是一次吐出整段，而是：

```text
P(token_t | token_1 ... token_{t-1})
```

每次根据已有 Token 预测下一个 Token。

简化循环：

```python
while not stop:
    logits = model(tokens)
    next_token = decode(logits)
    tokens.append(next_token)
```

真实 Serving 会使用 KV Cache，不会每次从头重复全部历史计算，但逻辑仍是逐 Token 决策。

---

## 2. 为什么 Output Token 数直接影响延迟

因为每个新 Token 都依赖上一步：

```text
Token 1
→ Token 2
→ Token 3
→ ...
```

无法像 Prefill 那样把整段未来输出一次并行算完。

因此：

```text
Long Output
→ 更多 Decode Steps
→ 更高 Latency
→ 更高 Cost
```

这也是为什么控制 `max_tokens`、让模型简洁回答、Early Stop 都有工程价值。

---

## 3. Logits 是什么

模型最后一层会为词表中的每个 Token 产生一个分数：

```text
logit[token_1]
logit[token_2]
...
logit[token_vocab]
```

Logit 不是概率。

它可以是任意实数，表示模型对不同候选 Token 的相对偏好。

---

## 4. Softmax 怎么把 Logits 变成概率

简化形式：

```text
p_i = exp(z_i) / Σ exp(z_j)
```

得到：

```text
Σ p_i = 1
```

这样就形成 Next Token Distribution。

但最终选哪个 Token，还取决于 Decoding Strategy。

---

## 5. Greedy Decoding

最简单：

```text
next_token = argmax(probability)
```

优点：

- 简单；
- 可重复性强；
- 适合部分结构化/确定性任务。

缺点：

- 可能陷入局部最优；
- 文本更单一；
- 对开放生成不一定最佳。

---

## 6. Temperature 在做什么

Temperature 通常作用于 Logits：

```text
softmax(logits / T)
```

### T 较低

```text
Probability 更尖锐
→ 更偏向高概率 Token
→ 输出通常更稳定
```

### T 较高

```text
Distribution 更平
→ 低概率 Token 有更多机会
→ 输出更多样
```

Temperature 不是“准确率旋钮”。

低 Temperature 也不能保证事实正确。

---

## 7. Top-k

只保留概率最高的 k 个 Token：

```text
Vocabulary
→ sort / select top k
→ renormalize
→ sample
```

这样可以避免从极低概率长尾中抽样。

`k` 太小会限制多样性，太大则过滤效果弱。

---

## 8. Top-p / Nucleus Sampling

不是固定保留 k 个，而是保留累计概率达到 `p` 的最小候选集合。

例如：

```text
p = 0.9
```

当模型很确定时，候选集合可能很小；模型不确定时，集合会变大。

因此 Top-p 是动态候选范围。

---

## 9. Top-k、Top-p 和 Temperature 怎么组合

典型管线可以理解为：

```text
Logits
→ Temperature rescale
→ Top-k / Top-p filtering
→ Renormalize
→ Sample
```

不同 Provider / Engine 的具体顺序和支持参数可能不同。

工程上不要同时乱调所有旋钮。

更好的方式是先定义任务：

```text
Coding / Extraction / Tool Args
→ 稳定、低随机

Creative Writing / Brainstorming
→ 允许更多样
```

再通过 Evaluation 验证参数。

---

## 10. “Temperature=0 就完全 deterministic”为什么不绝对

即使解码策略本身选择最大概率 Token，实际系统仍可能受：

- GPU Kernel 非确定性；
- Floating Point；
- Batch Scheduling；
- Provider 后端变化；
- Model Version；
- Tie-breaking；

影响。

因此应用层不应该把 LLM 当作严格数学函数：

```text
same input → byte-identical output
```

如果业务需要真正稳定结构，要使用：

- Structured Output；
- Validation；
- Retry；
- Deterministic Business Logic；
- Regression Test。

---

## 11. Stop Condition

生成循环还需要知道何时结束：

```text
EOS Token
max_output_tokens
stop sequence
protocol-specific stop
```

Agent Tool Calling 中还可能因为：

```text
tool call
handoff
approval required
```

而结束当前 Model Turn。

因此生成的“Stop”与 Agent Runtime 的“Run Stop”不是同一个层级。

---

## 12. Repetition 与 Degeneration

Autoregressive Model 可能出现：

- 重复句子；
- 循环生成；
- 某些 Token 模式被不断强化。

不同模型/API 可能提供：

```text
frequency penalty
presence penalty
repetition penalty
```

但使用时要理解 Provider 语义，不要把名字相似的参数当作完全等价。

---

## 13. Structured Output 与 Sampling 的关系

如果模型需要生成：

```json
{"city":"Singapore","days":3}
```

不能只靠低 Temperature 保证 JSON 合法。

更可靠的是：

```text
Schema-constrained Generation
→ Parse
→ Validate
→ Retry / Repair
```

Structured Output 本质上是输出协议约束，不是 Sampling 参数的替代品。

---

## 14. AI Application 怎么调生成参数

一个实用原则：

### Tool / Extraction / Routing

目标：

```text
稳定、可验证、低创造性
```

更依赖 Schema / Validation，随机性通常较低。

### Knowledge QA

目标：

```text
Grounded / Factual
```

Sampling 只是次要因素，更重要的是 Context / Retrieval / Citation / Verification。

### Creative

可以提高多样性，但仍应做安全和格式边界。

---

## 15. 常见错误

- Logits 就是概率：错。
- Temperature 越低事实性一定越高：错。
- Top-k 和 Top-p 是同一个东西：错。
- Temperature=0 能保证跨 Provider/硬件完全 deterministic：不能绝对保证。
- 输出不稳定只要调 Sampling：很多问题来自 Prompt、Context、Model、Tool Protocol。
- JSON 输出只要 Temperature 设低就够：错。

---

## 16. 面试怎么答

### Q：LLM 是怎么生成下一个 Token 的？

> 模型根据当前 Context 做 Forward，在 Vocabulary 上输出一组 Logits；Logits 经过 Softmax 等处理形成相对概率分布，再由 Greedy、Temperature、Top-k、Top-p 等 Decoding Strategy 选择下一个 Token，把它追加回 Context 后继续下一步，因此是 Autoregressive 逐 Token 生成。

### Q：Temperature、Top-k、Top-p 有什么区别？

> Temperature 调整整个概率分布的尖锐程度；Top-k 固定保留概率最高的 k 个候选；Top-p 保留累计概率达到阈值的动态候选集合。它们控制的是生成多样性/随机性，不应被当作事实准确率的直接旋钮。

---

## 17. 自测

<details><summary>1. 为什么 Output Token 越多通常延迟越高？</summary>
因为 Decode 是逐 Token 依赖，每个 Token 都需要一次新的模型推理步骤。
</details>

<details><summary>2. Logit 和 Probability 的区别是什么？</summary>
Logit 是模型未归一化分数，Softmax 等转换后才得到总和为 1 的概率分布。
</details>

<details><summary>3. 为什么低 Temperature 不能替代 Structured Output？</summary>
因为低随机性仍不保证语法/Schema 合法，真正可靠的协议输出需要约束、解析和校验。
</details>
