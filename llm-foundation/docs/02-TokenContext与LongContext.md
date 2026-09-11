# 02. Token、Context Window 与 Long Context：从输入单位到上下文预算

AI Application 里所有“上下文太长、成本太高、信息放不下”的问题，最前面都要先理解三个概念：

```text
Token
→ Token Budget
→ Context Window
```

这一章把原先分开的 Tokenization、Context Budget 和 Long Context 合成一个完整输入模型。

---

## 1. Token 是什么

LLM 不直接处理“汉字、单词、句子”，而是先通过 Tokenizer 把文本转成 Token ID：

```text
Text
→ Tokenizer
→ Token IDs
→ Embedding
→ Transformer
```

Token 可以是：

- 一个完整词；
- 子词片段；
- 标点；
- 汉字或字节片段；
- 特殊控制符。

所以：

```text
1 token ≠ 1 word
1 token ≠ 1 character
```

不同模型的 Tokenizer 不同，同一段文本的 Token 数也可能不同。

---

## 2. Token 为什么是工程成本单位

模型调用成本和性能通常直接受 Token 数影响：

```text
Input Tokens
+
Output Tokens
```

会影响：

- Context 是否放得下；
- Prefill 计算；
- KV Cache 占用；
- 网络 Payload；
- API Cost；
- TTFT；
- Agent 长任务可持续性。

因此 Token Count 是 AI Application 的基础容量单位，而不是 NLP 细节。

---

## 3. Context Window 是什么

可以把一次模型调用看成：

```text
System Instruction
+ Developer / Policy Context
+ User Messages
+ Conversation History
+ Retrieved Documents
+ Tool Results
+ Memory
+ Generated Output Reserve
```

这些共同竞争有限的 Context Window。

如果模型最大上下文是 `C`：

```text
Input Tokens + Output Reserve <= C
```

不能把整个 Window 全塞满输入，否则模型没有足够空间生成输出。

---

## 4. Context Budget 不只是“不能超长度”

即使还没超过硬上限，也存在软预算问题：

```text
更多 Context
→ 更多 Prefill Compute
→ 更高成本
→ 更高 KV Cache 占用
→ 更长 TTFT
→ 更复杂 Attention
```

而且更多内容不一定带来更好答案。

所以正确问题不是：

> “还能不能再塞 20K Token？”

而是：

> **“这 20K Token 是否真的值得占用 Context Budget？”**

---

## 5. 长上下文为什么不等于无限记忆

Long Context 解决的是：

```text
一次调用能看到更多 Token
```

它不自动解决：

- 跨 Session 长期记忆；
- 信息选择；
- 过期事实；
- 权限；
- Context Compression；
- 多任务状态；
- 数据持久化。

因此：

```text
Long Context
≠ Long-term Memory
```

Agent Harness 会进一步学习 Memory、Compaction 和 State。

---

## 6. Lost in the Middle 的直觉

长 Context 中，模型对所有位置的信息利用能力并不天然均匀。

工程上经常观察到：

```text
相关证据存在于 Context
≠ 模型一定可靠使用它
```

尤其当 Context 中包含：

- 大量无关内容；
- 多份相似证据；
- 冲突指令；
- 很长 Tool Result；
- 关键事实被淹没在中间位置；

模型可能出现检索/利用下降。

所以 Context Engineering 的目标之一是提高：

```text
Information Density
```

而不是只扩大 Window。

---

## 7. 为什么 RAG 仍然有价值

即使模型 Context 很长，RAG 仍可帮助：

```text
从大知识库选少量相关证据
→ 控制 Token Cost
→ 提高相关信息密度
→ 附带 Source / Citation
→ 管理 Freshness / Permission
```

所以：

```text
Long Context
≠ RAG 失去意义
```

---

## 8. 为什么 Agent 更容易遇到 Context Pressure

普通 Chat 主要积累 Message。

Agent 还会积累：

```text
Tool Calls
Tool Results
Plans
File Contents
Search Results
Memory
Runtime State Projection
```

尤其 Coding Agent 中，一个大文件或终端输出可能一次消耗大量 Token。

因此成熟 Agent Runtime 会设计：

- Tool Result Offloading；
- Context Selection；
- Compaction；
- Summary / Artifact Reference；
- Cache-aware Assembly。

这些属于 Agent Harness，但基础仍是这里的 Token Budget。

---

## 9. Context 预算怎么估

一个实用模板：

```text
Maximum Context
- Output Reserve
- System / Policy Reserve
- Tool Schema / Protocol Reserve
= Dynamic Context Budget
```

Dynamic Context 再分配给：

```text
Conversation
Retrieval
Memory
Tool Results
Task Artifacts
```

而不是让每个组件无限追加。

---

## 10. Token Cost 和 Latency 的关系

### Input Token 增加

主要增加：

```text
Prefill Work
TTFT
KV Cache Allocation
Input Cost
```

### Output Token 增加

Autoregressive Decode 是逐 Token 生成，因此会直接增加：

```text
Generation Time
TPOT × Token Count
Output Cost
```

所以“限制输出长度”常常是最直接的成本/延迟优化手段之一。

---

## 11. 常见错误

- 字符数可以直接等于 Token 数：错。
- Context Window 越大，答案必然越好：错。
- 只要没超过硬上限，就无需做 Context Budget：错。
- Long Context 可以替代 Memory：错。
- RAG 在百万 Token Context 后没意义：过度简化。
- Agent 只要保存完整聊天历史就能长期运行：错。

---

## 12. 面试怎么答

### Q：Context Window 是什么？

> Context Window 是模型一次 Forward/Generation 可处理的 Token 总预算，输入消息、系统指令、检索结果、Tool Result 以及输出空间都会竞争它。工程上不仅要防止超过硬限制，还要控制 TTFT、KV Cache、成本和信息密度，所以会做 Context Selection、RAG、Compaction 等治理。

### Q：Long Context 能替代 RAG 吗？

> 不能简单替代。Long Context 提高单次可见容量，但 RAG 还承担知识选择、Freshness、Permission、Citation 和成本控制，而且长 Context 中相关信息不一定被模型稳定利用。

---

## 13. 自测

<details><summary>1. 为什么必须预留 Output Tokens？</summary>
因为 Context Window 是输入和生成共享的总预算，输入占满后模型没有足够空间输出。
</details>

<details><summary>2. 为什么 Agent 比普通 Chat 更容易超 Context？</summary>
因为除了消息还会累积 Tool Result、文件、搜索结果、计划、Memory 和 Runtime State。
</details>

<details><summary>3. Long Context 与 Long-term Memory 的核心差异是什么？</summary>
前者是单次调用可见容量；后者涉及跨调用的持久化、选择、更新和召回机制。
</details>
