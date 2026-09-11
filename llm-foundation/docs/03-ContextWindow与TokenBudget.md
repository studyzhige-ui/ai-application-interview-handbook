# 03｜Token Budget、Context Window 与输入成本

> Tokenization 之后，下一个必须建立的概念是：**一次推理到底能塞多少 Token，以及这些 Token 该怎么分配。**

## 1. Context Window 是什么

Context Window 可以理解为：

> 模型单次推理能够处理的 Token 序列容量边界。

应用里的真实 Context 往往是：

```text
System Prompt
+ Developer / Policy Instructions
+ User Message
+ Conversation History
+ Retrieved Context
+ Tool Results
+ Structured Metadata
+ Output Reserve
```

不是只有用户最后一句话。

---

## 2. Token Budget 为什么是系统设计问题

假设模型最多允许一个有限上下文窗口。

你不能把所有空间都给输入，因为还要留输出。

于是有：

```text
Total Context Budget
= Input Budget
+ Output Budget
```

输入里又要继续拆：

```text
Input Budget
= Fixed Instructions
+ History
+ Retrieval
+ Tool Result
+ Current User Input
```

这已经是一个资源分配问题。

---

## 3. 为什么 Context 越大不等于越好

更大的 Context 解决的是“容量上限”，但会带来：

- 更多输入 Token 成本；
- 更重的 Prefill；
- 更多无关噪声；
- Attention / 模型利用率问题；
- 重要信息可能被稀释；
- 更复杂的权限与数据泄露风险。

所以：

> Context Engineering 的目标不是“尽量塞满”，而是“让最需要的信息进入有限预算”。

---

## 4. 一个典型预算例子

假设一个 Agent 请求需要：

```text
System Instructions      2k
Conversation History     8k
Retrieved Docs          12k
Tool Results             6k
Current User Input       2k
Output Reserve           4k
```

那么请求不是“用户只输入了 2k”，而是总共约 34k Token 级别的预算问题。

如果再把所有历史 Tool Log 都塞进去，很快就会膨胀。

---

## 5. Context Window 和模型“记忆”不是一回事

Context Window 是：

> 当前这一轮模型真正能看到的输入序列。

Memory 是：

> 应用在多轮甚至跨 Session 之间保存、检索、压缩和重新注入信息的系统能力。

所以：

```text
Long Context
≠
Long-term Memory
```

后者属于 Agent Harness。

---

## 6. 输入 Token 和输出 Token 对性能影响不同

应用工程上通常要区分：

```text
Input Tokens
→ 主要影响 Prefill / Context Processing

Output Tokens
→ 需要逐 Token Decode
```

因此：

> “总 Token 数一样”不代表延迟结构一样。

后面 Prefill / Decode 会详细展开。

---

## 7. RAG 与 Agent 为什么特别依赖 Budget

### RAG

检索结果不能无限追加：

```text
Top-K 越大
→ Context 越长
→ 成本更高
→ 噪声可能更多
```

所以 RAG 需要 Chunk / Retrieval / Rerank / Context Build。

### Agent

Agent 会不断累积：

```text
User
Assistant
Reasoning Trace / Summary
Tool Call
Tool Result
Observation
Next Step
```

如果没有 Context Assembly / Compaction，长任务迟早撞上预算边界。

---

## 8. 常见 Token Budget 策略

应用层可能做：

- 固定 System / Policy 预算；
- 给当前 User Input 留最低空间；
- 给输出预留上限；
- History 只取最近 N 轮；
- 历史做 Summary；
- Tool Result 做裁剪 / Structured Compression；
- RAG Context 按 Rerank 分数择优；
- 不同信息源设置独立上限；
- 超预算时按优先级淘汰。

真正复杂的 Compaction / Correctness 在 Agent Harness 再讲。

---

## 9. Failure Case

### Failure 1：把 Context Window 当成目标长度

窗口 128k，不代表每次都应该发 128k。

### Failure 2：只限制 RAG 文档，不限制 Tool Result

Agent 工具可能返回几十 KB JSON，反而成为最大 Token 源。

### Failure 3：不预留输出

输入接近上限后，模型无法生成足够长的结果。

### Failure 4：按 Token 数平均裁剪

不同信息价值不同。System Policy 和最近用户需求通常不能与低价值旧日志等价裁剪。

---

## 10. 🎯 面试怎么回答

> Context Window 是模型单次推理能够处理的 Token 序列容量。真实 AI 应用要做 Token Budget，因为 System Prompt、History、RAG Context、Tool Result、User Input 和输出都共享这个窗口。更大窗口只提高容量上限，并不意味着应该塞满；输入越长会增加 Prefill 成本和噪声，还可能出现长上下文利用率下降。因此应用层需要按信息价值做预算、检索、压缩和输出预留。

---

## 11. ⚠️ 易错点

错误：

> Context Window 128k，就能稳定利用 128k 里每个位置的信息。

错误：

> 有了 Long Context 就不需要 RAG / Memory。

错误：

> 只要请求没超过最大 Token 就没有问题。

真正的问题还包括成本、延迟、噪声和信息利用率。

---

<details>
<summary>自测 1：为什么必须为输出预留 Token？</summary>

因为输入和生成输出共享单次推理的 Context 容量。如果输入占满窗口，就没有足够空间继续生成目标答案。

</details>

<details>
<summary>自测 2：Long Context 和 Long-term Memory 最大区别是什么？</summary>

Long Context 是单次推理输入容量；Long-term Memory 是应用跨轮次保存、筛选并重新注入信息的状态系统。

</details>
