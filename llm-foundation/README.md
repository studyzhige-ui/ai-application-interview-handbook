# LLM Foundation（应用工程深度）｜AI 应用开发秋招系统手册

> **Granularity Audit：✅ 已完成。** 原 29 章在不删知识点的前提下收敛为 **14 个正式知识小板块**。研究层 23 道 LLM Canonical、HUMAN-A Source Count 与模块边界完全不变。
>
> 目标不是训练算法岗 Transformer 八股，而是让 AI Application Engineer 真正理解：**输入 Token 怎样占用 Context → Transformer 怎样处理 → 模型怎样逐 Token 生成 → KV Cache / Serving 为什么决定延迟与成本 → Model / Embedding / Reranker 怎样选 → Prompt / Factuality / Fine-tuning 应在什么边界使用。**

---

## 1. 固定课程原则

> **知识体系演进顺序优先，真人面经只校准复习权重、追问深度与工程 Failure，不反过来打乱 0→1 主干。**

第二条原则：

> **机制可以细讲，但教材文件应该代表完整认知闭环。**

因此这次不再让 `Logits`、`Temperature`、`Prefill`、`PagedAttention` 等子机制各自成为独立文件。

---

## 2. 模块边界

LLM Foundation 负责：

```text
Token / Context
Transformer / Attention / RoPE
Autoregressive Generation / Sampling
KV Cache / Prefill / Decode
Serving / Batching / PagedAttention / Quantization
Model API / Model Selection
Embedding / Reranker Foundation
Multimodal
Prompt Engineering
Hallucination / Factuality
Fine-tuning / LoRA / Post-training Boundary
```

| 问题 | Primary Module |
|---|---|
| HNSW / IVF / Vector Filter | Vector DB |
| Chunk / Hybrid / RRF / Retrieval Evaluation | RAG |
| Agent Context Compaction / Memory / Tool Protocol | Agent Harness |
| Provider Retry / Circuit Breaker | AI Backend Engineering |

一句话：

> **LLM Foundation 解释模型为什么这样表现；RAG / Agent / Backend 解释怎样把它可靠地变成系统。**

---

## 3. 真人面经信号

本模块有 **23 道 Primary Canonical、82 个独立 HUMAN-A 来源**覆盖。

强信号包括：Prompt Engineering、Transformer、Model Selection、Hallucination、Fine-tuning、Post-training、Context Window、QKV/Self-Attention、Embedding、Model API、KV Cache、Serving、Sampling、Reranker 等。

面经没有单独高频问到的 Causal Mask、Residual/Norm、Continuous Batching、PagedAttention 等仍属于完整知识体系，不因频率低而删掉。

---

## 4. 为什么从 29 合并为 14

```text
Tokenization + Context Budget + Long Context
→ Token / Context Window

Transformer Architecture + FFN / Residual / Norm
→ Transformer Block

QKV + Multi-Head / Causal + RoPE
→ Attention & Position

Autoregressive + Logits + Sampling
→ Generation & Decoding

KV Cache + Prefill / Decode
→ LLM Inference Two-stage Model

Continuous Batching + PagedAttention + Latency/Cost + Precision
→ Serving Engine

Model API + Model Selection
→ Model Access & Selection

Embedding + Cross-Encoder / Reranker
→ Retrieval Model Foundation

Hallucination + Prompt/RAG/Fine-tune Boundary
→ Factuality & Intervention Boundary

SFT + LoRA/PEFT
→ Fine-tuning & Parameter-efficient Adaptation
```

Multimodal、Prompt Engineering 和 Post-training/Distillation 各自有独立知识边界，因此继续单章。

> 文件保留合并后最早历史编号；正式学习顺序以下面的 14-block 列表为准。

---

## 5. 正式 14 个知识小板块

1. [LLM Foundation 在 AI Application 中负责什么](docs/01-LLMFoundation在AI应用中的职责.md)
2. [Token、Context Window 与 Long Context](docs/02-TokenContext与LongContext.md)
3. [Transformer Block：Architecture、FFN、Residual、Norm](docs/05-TransformerBlock.md)
4. [Attention 与 Position：QKV、Multi-Head、Causal Mask、RoPE](docs/06-Attention与Position.md)
5. [Autoregressive Generation：Logits、Softmax、Sampling、Decoding](docs/10-Generation与Decoding.md)
6. [KV Cache、Prefill 与 Decode](docs/13-KVCache与PrefillDecode.md)
7. [LLM Serving Engine：Batching、PagedAttention、Latency、Cost、Quantization](docs/15-ServingEngine与性能.md)
8. [Model API、Provider Adapter 与 Model Selection](docs/19-ModelAPI与Selection.md)
9. [Embedding 与 Reranker：Bi-Encoder / Cross-Encoder](docs/21-Embedding与Reranker.md)
10. [Multimodal Foundation](docs/23-MultimodalFoundation.md)
11. [Prompt Engineering：从提示词到可评估工程](docs/24-PromptEngineering.md)
12. [Hallucination、Factuality 与 Prompt / RAG / Fine-tuning 边界](docs/25-Hallucination与干预边界.md)
13. [Fine-tuning、SFT 与 LoRA / PEFT](docs/27-FineTuning与LoRA.md)
14. [RLHF / DPO / GRPO / Distillation 的应用工程边界](docs/29-PostTraining与Distillation.md)

---

## 6. 四条主线

### A｜模型输入与计算

```text
Token / Context
→ Transformer Block
→ Attention / Position
```

### B｜生成与 Serving

```text
Autoregressive Generation
→ KV Cache / Prefill / Decode
→ Serving Engine / Quantization
```

### C｜应用模型选择

```text
Provider API / Model Selection
→ Embedding / Reranker
→ Multimodal
```

### D｜行为与事实治理

```text
Prompt Engineering
→ Hallucination / Factuality
→ Prompt vs RAG vs Fine-tuning
→ SFT / LoRA
→ Post-training / Alignment / Distillation
```

---

## 7. 推荐学习法

第一遍按 14 个知识块建立机制链；第二遍进入 [`review/README.md`](review/README.md) 从空白画 Token→Transformer→Generation→Serving；第三遍使用：

- [`interview/高频面试题.md`](interview/高频面试题.md)
- [`interview/面试易错点.md`](interview/面试易错点.md)
- [`interview/面试前速查表.md`](interview/面试前速查表.md)

最终目标不是背公式，而是能解释：

```text
为什么 Context 贵
为什么 Output 慢
为什么 KV Cache 吃显存
为什么 Serving 需要动态调度
为什么选这个模型
为什么 RAG / Prompt / Fine-tuning 解决不同问题
```
