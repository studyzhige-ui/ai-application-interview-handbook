# LLM Foundation（应用工程深度）｜AI 应用开发秋招系统手册

> LLM Foundation 是这套 Handbook 的第 7 个正式一级模块。
>
> 它不是“训练算法岗 Transformer 八股大全”，也不是“会调一个 Chat API 就算懂 LLM”。目标是从 AI Application Engineer 的视角建立一条完整因果链：**文本怎样变成 Token → Token 怎样通过 Transformer 建模 → 模型怎样逐 Token 生成 → Context / KV Cache / Serving 为什么决定延迟与成本 → Model / Embedding / Reranker 怎样选 → Prompt / Hallucination 怎样治理 → 什么时候才值得 Fine-tuning。**

## 1. 最重要的课程原则

继续固定遵守：

> **知识体系演进顺序优先，真实面经只用于调整复习权重、补充真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

冻结 `S001–S279` HUMAN-A 中，Prompt Engineering 有 30 个独立来源，是本模块最强市场信号；但课程不会第一章就教“Prompt 模板”。

因为你必须先知道：

```text
Token 是什么
→ Context Window 为什么有限
→ Transformer 怎样处理 Token
→ Attention / QKV 在做什么
→ 模型怎样自回归生成
→ Sampling 怎样改变输出
→ Context / KV Cache / Serving 怎样改变成本和延迟
→ 才能真正理解 Prompt 为什么有效、为什么也会失效
```

面经决定 Prompt、Model Selection、Hallucination 这些章节需要更强的工程与 Evaluation 深度，但不决定教材顺序。

---

## 2. 本模块在整套体系中的边界

本模块负责：

```text
Tokenization
Context Window / Long Context Limitation
Transformer / Attention / FFN / RoPE
Autoregressive Generation
Sampling / Decoding
KV Cache
Prefill / Decode
Batching / Serving Engine
Inference Latency / Throughput / Cost
Model API / Provider Boundary
Model Selection
Embedding Model Foundation
Reranker / Cross-Encoder Foundation
Multimodal Foundation
Prompt Engineering
Hallucination / Factuality Boundary
Fine-tuning / SFT / LoRA / Preference Optimization / Distillation Boundary
```

明确不抢这些知识模型：

| 问题 | Primary Module |
|---|---|
| Vector Index / HNSW / IVF / Metadata Filter | Vector DB |
| Chunk / Dense-Sparse / Hybrid / RRF / Retrieval Top-K | RAG |
| RAG End-to-end Evaluation / Bad Case Attribution | RAG |
| Agent Context Assembly / Compaction / Memory | Agent Harness / Runtime |
| Tool Calling Protocol / MCP / Permission | Agent Harness / Runtime |
| LLM Provider Timeout / Retry / Circuit Breaker | AI Backend Engineering |
| 完整 AI 系统中的模型路由与跨组件权衡 | System Design / Agent Harness |

一句话：

> **LLM Foundation 解释“模型为什么这样工作和这样表现”；RAG / Agent / Backend 决定“怎样把模型可靠地放进系统”。**

---

## 3. 真人面经只校准重点

冻结研究中本模块当前有 **23 道 Primary Canonical、82 个独立 HUMAN-A 来源**覆盖。

| Topic | HUMAN-A Sources | 深度 |
|---|---:|---:|
| Prompt Engineering | 30 | L3 |
| Transformer Architecture | 10 | L2 |
| Model Selection | 10 | L4 |
| Hallucination / Factuality | 10 | L3 |
| Fine-tuning | 9 | L3 |
| Post-training / Alignment | 8 | L3 |
| Context Window | 7 | L3 |
| QKV / Self-Attention | 7 | L2 |
| Embedding Model | 6 | L2 |
| Model API | 5 | L3 |
| Multi-Head Attention | 5 | L2 |
| Tokenization | 4 | L2 |
| Multimodal Foundation | 4 | L2 |
| Inference Engine | 4 | L3 |
| KV Cache | 3 | L3 |
| Inference Latency | 3 | L3 |
| Sampling Parameters | 3 | L2 |
| Reranker Foundation | 3 | L3 |

> **Interview Heat ≠ Knowledge Importance。** Causal Mask、Residual / Norm、Continuous Batching、Precision / Quantization、Model Evaluation 等即使当前没有独立高频 Canonical，也属于理解现代 LLM 应用行为的必要节点，因此保留。

---

## 4. 事实与资料口径

本模块优先讲跨模型 / 跨 Provider 稳定的机制，再用具体实现做映射，不把某一家 API 或某个版本写成永恒规则。

推荐权威入口：

- Transformer：<https://arxiv.org/abs/1706.03762>
- RoPE：<https://arxiv.org/abs/2104.09864>
- vLLM / PagedAttention：<https://arxiv.org/abs/2309.06180>
- LoRA：<https://arxiv.org/abs/2106.09685>
- DPO：<https://arxiv.org/abs/2305.18290>
- Sentence-BERT：<https://arxiv.org/abs/1908.10084>
- Lost in the Middle：<https://arxiv.org/abs/2307.03172>

课程只讲到能支撑 AI Application / RAG / Agent 工程判断所需的数学与训练深度。

---

## 5. 七条主线

### 主线 A｜文本怎样进入模型

```text
Text
→ Tokenizer
→ Token ID
→ Embedding
→ Position
→ Context Window
→ Token Budget
```

### 主线 B｜Transformer 怎样计算

```text
Transformer Block
→ Q / K / V
→ Self-Attention
→ Multi-Head
→ Causal Mask
→ FFN
→ Residual / Normalization
→ RoPE / Position
```

### 主线 C｜模型怎样生成

```text
Prompt Tokens
→ Forward
→ Logits
→ Probability Distribution
→ Decoding / Sampling
→ Next Token
→ Autoregressive Loop
```

### 主线 D｜推理系统为什么决定性能

```text
KV Cache
→ Prefill / Decode
→ Dynamic / Continuous Batching
→ PagedAttention
→ Serving Engine
→ TTFT / TPOT / Throughput
→ Cost / Capacity
→ Precision / Quantization
```

### 主线 E｜应用怎样调用与选择模型

```text
Messages / Roles
→ Model API
→ Provider Adapter
→ Structured Output Boundary
→ Model Selection
→ Effect / Latency / Cost / Context / Risk
```

### 主线 F｜Embedding / Rerank / Multimodal

```text
Embedding Model
→ Bi-Encoder
→ Vector Representation
→ Cross-Encoder / Reranker
→ Multimodal Encoder / Alignment
```

### 主线 G｜Prompt、事实性与适配

```text
Prompt Engineering
→ Evaluation / Regression
→ Hallucination / Factuality
→ Prompt vs RAG vs Fine-tuning
→ SFT / LoRA
→ DPO / RLHF / GRPO / Distillation Boundary
```

---

## 6. 完整 29 章

### Part A｜Token、Context 与模型输入

1. [LLM Foundation 在 AI Application 中负责什么](docs/01-LLMFoundation在AI应用中的职责.md)
2. [Token 与 Tokenization](docs/02-Token与Tokenization.md)
3. [Token Budget、Context Window 与输入成本](docs/03-ContextWindow与TokenBudget.md)
4. [Long Context 与 Lost in the Middle](docs/04-LongContext与LostInTheMiddle.md)

### Part B｜Transformer 从整体到细节

5. [Transformer Architecture 总览](docs/05-TransformerArchitecture.md)
6. [Self-Attention 与 Q / K / V](docs/06-SelfAttention与QKV.md)
7. [Multi-Head Attention 与 Causal Mask](docs/07-MultiHead与CausalMask.md)
8. [FFN、Residual 与 Normalization](docs/08-FFNResidualNorm.md)
9. [Positional Encoding 与 RoPE](docs/09-RoPE与位置编码.md)

### Part C｜从 Logits 到逐 Token 生成

10. [Autoregressive Generation](docs/10-AutoregressiveGeneration.md)
11. [Logits、Softmax 与 Decoding](docs/11-Logits与Decoding.md)
12. [Temperature / Top-k / Top-p 与 Determinism](docs/12-Sampling参数.md)

### Part D｜Inference / Serving

13. [KV Cache](docs/13-KVCache.md)
14. [Prefill 与 Decode](docs/14-Prefill与Decode.md)
15. [Batching 与 Continuous Batching](docs/15-ContinuousBatching.md)
16. [PagedAttention、vLLM 与 Serving Engine](docs/16-PagedAttention与ServingEngine.md)
17. [TTFT / TPOT / Throughput / Cost](docs/17-推理延迟与成本.md)
18. [Precision / Quantization 与部署边界](docs/18-Precision与Quantization.md)

### Part E｜Model API 与模型选择

19. [Messages、Role、Model API 与 Provider Adapter](docs/19-ModelAPI与ProviderAdapter.md)
20. [Model Selection：效果、Latency、Cost、Context 与风险](docs/20-ModelSelection.md)

### Part F｜Embedding、Rerank 与 Multimodal

21. [Embedding Model 为什么能表示语义](docs/21-EmbeddingModel.md)
22. [Bi-Encoder、Cross-Encoder 与 Reranker](docs/22-Reranker与CrossEncoder.md)
23. [Multimodal Foundation](docs/23-MultimodalFoundation.md)

### Part G｜Prompt、事实性与模型适配

24. [Prompt Engineering：从写提示词到可评估工程](docs/24-PromptEngineering.md)
25. [Hallucination、Factuality 与 Verification Boundary](docs/25-Hallucination与Factuality.md)
26. [Prompt vs RAG vs Fine-tuning：什么时候该换手段](docs/26-PromptRAGFineTuning边界.md)
27. [Fine-tuning 与 SFT 基础](docs/27-FineTuning与SFT.md)
28. [LoRA / PEFT：低成本参数适配](docs/28-LoRA与PEFT.md)
29. [RLHF / DPO / GRPO / Distillation 的应用工程边界](docs/29-PostTraining与Distillation.md)

---

## 7. 为什么加入面经之外的章节

### Causal Mask / Residual / Normalization

只会背 QKV 并不能解释一个 Decoder-only LLM 为什么能自回归，也不能理解 Transformer Block 的稳定训练与信息流。

### Continuous Batching

AI Application 的高并发延迟问题不能只停在“加机器”。Serving Engine 为什么能提高 GPU 利用率，必须知道请求的 Prefill / Decode 长度不同，以及传统静态 Batch 为什么浪费。

### Precision / Quantization

模型大小、显存、吞吐、精度与部署成本的关系，是 Model Selection 与自部署边界的自然组成部分。

所以这些属于知识骨架，不因面经没有独立高频题就删除。

---

## 8. 推荐三遍学习法

第一遍严格按 `01 → 29`，目标是形成因果链，而不是一次记住公式。

第二遍自己画：

- Token → Embedding → Transformer Block；
- Q / K / V Attention；
- Autoregressive Generation Loop；
- KV Cache；
- Prefill / Decode；
- Continuous Batching；
- Embedding vs Reranker；
- Prompt / RAG / Fine-tuning Decision Tree。

第三遍进入：

- `review/`
- `interview/高频面试题.md`
- `interview/面试易错点.md`
- `interview/面试前速查表.md`

顺序始终是：

```text
理解模型机制
→ 能解释应用行为
→ 能做工程 Trade-off
→ 再练面试表达
```

---

## 9. 下一环

LLM Foundation 完成后进入 **RAG**。

到那时：

```text
Embedding / Reranker Model Foundation
        +
Vector DB / ANN Infrastructure
        ↓
RAG Retrieval Pipeline
        ↓
Chunk / Rewrite / Hybrid / RRF / Rerank
        ↓
Evaluation / Bad Case / Freshness / Permission
```

这样 RAG 不需要再从“Embedding 是什么、向量库是什么”重新讲起，而能直接进入真正的 Retrieval Engineering。
