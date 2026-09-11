# 01｜LLM Foundation 在 AI Application 中负责什么

> 这一章先回答一个最基础的问题：**AI 应用工程师为什么需要学模型基础？**

## 1. 先讲人话

如果把一个 AI 应用画成：

```text
User
  ↓
API / Agent / RAG
  ↓
LLM
```

那么 LLM Foundation 负责解释：

> 最下面这个“LLM 黑盒”为什么会这样响应、为什么会慢、为什么会贵、为什么会忘、为什么会胡说、为什么同一个 Prompt 换模型后行为会变。

应用工程师不一定要自己训练 70B 模型，但必须知道模型行为的**工程因果链**。

否则很多问题只能靠试参数：

```text
回答不稳定 → 再改 Prompt
延迟很高   → 再加机器
Context 满了 → 换更大窗口
召回不好   → 再换 Embedding
```

但你不知道为什么。

---

## 2. 本模块回答哪些问题

完整主线：

```text
Text
→ Token
→ Context
→ Transformer
→ Attention
→ Generation
→ KV Cache
→ Serving
→ Latency / Cost
→ Model Selection
→ Embedding / Rerank
→ Prompt
→ Hallucination
→ Fine-tuning Boundary
```

最终你应该能回答：

- 为什么 1 万汉字不等于 1 万 Token？
- Context Window 为什么不是“越大越好”？
- Attention 到底在算什么？
- 为什么生成是逐 Token 的？
- Temperature 为什么改变输出随机性？
- KV Cache 为什么提高速度却消耗显存？
- TTFT 和生成速度为什么是两种延迟？
- 为什么 Embedding 和 Reranker 不是一类模型？
- 为什么 Prompt 优化必须做 Regression？
- 什么时候该 RAG，什么时候该 Fine-tuning？

---

## 3. 模型层与系统层必须分开

一个 AI 请求可能失败在不同层：

```text
User Input
   ↓
Prompt / Context
   ↓
Model Inference
   ↓
Generated Output
   ↓
Application Verification
```

例如“回答错了”可能是：

1. Prompt 目标不清；
2. Context 中根本没有答案；
3. 重要信息被放在超长 Context 中间；
4. 模型能力不够；
5. Sampling 太随机；
6. RAG 召回错误；
7. Tool 返回错误；
8. 模型生成了事实性错误；
9. 应用没有做验证。

所以不能把所有失败都叫：

> “模型幻觉”。

这也是后续 RAG、Agent、System Design 能正确分层定位的前提。

---

## 4. AI Application Engineer 需要学多深

### 需要真正理解

```text
Tokenization
Context Window
Transformer Block
Self-Attention / QKV
Causal Generation
Sampling
KV Cache
Prefill / Decode
Serving Metrics
Embedding / Reranker
Prompt Engineering
Hallucination Boundary
Fine-tuning Boundary
```

### 需要知道概念与工程影响，但不要求训练算法岗推导

```text
Backpropagation 细节
Optimizer 数学推导
Distributed Training
Tensor Parallel / Pipeline Parallel 深度实现
CUDA Kernel
FlashAttention Kernel 级优化
RL 算法证明
```

不是这些不重要，而是它们不属于当前岗位主线。

---

## 5. 为什么这个模块放在 Vector DB 之后、RAG 之前

前面已经学了：

```text
Vector
→ Similarity
→ ANN
→ Vector DB
```

但还没真正解释：

> Embedding 是怎么来的？模型为什么能产生语义表示？

LLM Foundation 会补上模型侧。

然后 RAG 就可以自然连接：

```text
Embedding Model
        ↓
Vector DB
        ↓
Retrieval
        ↓
Reranker
        ↓
Context
        ↓
LLM
```

---

## 6. 一个典型 AI 请求的模型侧生命周期

```text
Raw Text
  ↓
Tokenizer
  ↓
Token IDs
  ↓
Embedding + Position
  ↓
Transformer Blocks
  ↓
Logits
  ↓
Sampling / Decoding
  ↓
Next Token
  ↓
循环直到 Stop
```

Serving 侧还会额外出现：

```text
Request
  ↓
Queue / Batch
  ↓
Prefill
  ↓
KV Cache
  ↓
Decode × N
  ↓
Stream Tokens
```

这两张图就是整个模块的骨架。

---

## 7. AI 应用里的三个最重要边界

### Boundary 1：模型能力 ≠ 外部事实

模型参数中的知识并不保证：

- 最新；
- 精确；
- 可引用；
- 与企业私有数据一致。

因此才需要 RAG / Tool / Verification。

### Boundary 2：Context Window ≠ Memory

能塞进 Context 的内容只是当前推理输入。

长期 Memory 是应用系统的状态管理问题，Primary 在 Agent Harness。

### Boundary 3：Model API ≠ Agent Runtime

模型可以返回 Tool Call，但：

```text
工具是否允许执行
参数是否可信
执行是否超时
是否重试
是否幂等
结果怎样写回状态
```

这些不是模型本身负责，而是 Agent Runtime 负责。

---

## 8. 🎯 面试怎么回答

如果面试官问：

> AI 应用工程师为什么还要学 Transformer / KV Cache 这些？

可以回答：

> 因为应用层很多关键决策都由模型机制决定。Tokenization 决定 Context 和成本，Attention / Context Window 决定长文本利用边界，Autoregressive Generation 和 Sampling 决定输出行为，KV Cache、Prefill / Decode 决定延迟与并发，Embedding / Reranker 决定检索模型选型。我的目标不是训练模型，而是理解这些机制后能正确做 Prompt、模型选型、Serving、RAG 和 Agent 的工程权衡。

---

## 9. ⚠️ 面试易错点

不要说：

> “LLM Foundation 就是学 Transformer 八股。”

也不要说：

> “应用开发只需要会调 API。”

更准确的是：

> 应用工程师需要掌握**会改变系统行为的模型机制**，但不必把课程扩成训练 Infra。

---

## 10. 🔍 继续追问

- Token 和字符有什么区别？
- Context Window 为什么有限？
- Transformer 为什么适合序列建模？
- 为什么生成要逐 Token？
- KV Cache 缓存的到底是什么？
- Embedding 和 Generation Model 有什么区别？
- Prompt、RAG、Fine-tuning 各解决什么问题？

这些就是后面 28 章要逐步回答的问题。

---

<details>
<summary>自测 1：Context Window 大是不是就不需要 RAG 了？</summary>

不是。更大的 Context 只提高单次请求可输入的 Token 上限，并不自动解决检索成本、信息定位、权限、数据新鲜度、引用、长上下文利用率和长期知识治理问题。

</details>

<details>
<summary>自测 2：LLM 能返回 Tool Call，是不是工具执行属于模型能力？</summary>

不是。模型可以生成结构化调用意图，但权限、参数验证、真实执行、超时、重试、幂等、审计与状态恢复属于 Agent Harness / Backend Runtime。

</details>
