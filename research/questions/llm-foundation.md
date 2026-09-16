# LLM Foundation（应用工程深度）Canonical Questions — S001–S279 全库纵向扫描 v2

更新日期：2026-09-10

> 一级板块：**LLM Foundation（应用工程深度）**。本文件只保留 AI Application Engineer 真正被问到的模型基础深度。目标不是训练算法岗题库，而是让应用工程师理解 Token、Transformer、Inference、Model API、Embedding / Rerank 与 Post-training 到足够解释系统行为和工程取舍的程度。
>
> 本文件所有条目的 `Primary Module = LLM Foundation（应用工程深度）`。RAG Pipeline 的 Chunk / Retrieval / Fusion / Evaluation 归 `RAG`；ANN Index / Vector Storage 归 `Vector DB`；Context Assembly / Memory / Tool Runtime 归 `Agent`。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**23**
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数
- 当前版本：`v2`（十板块归属审计版）

真人面经给出的边界很清楚：应用岗不一定要求推导训练算法，但会追问“为什么模型这样表现、参数怎样影响生成、Context 为什么会失效、推理成本从哪里来、Embedding / Rerank 为什么不同”。

---

## 2. Token / Context / Generation

### LLM-001 · Token 是什么？Tokenizer 为什么把文本拆成 Token，而不是按字符或单词直接处理？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Tokenization
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S002`, `S095`, `S193`, `S202`

### LLM-002 · Context Window 的能力边界由什么决定？为什么 Context 变大仍不能把所有信息无差别塞进去？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：Agent, RAG
- **Topic**：Context Window
- **Question Type**：Why / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S002`, `S106`, `S107`, `S115`, `S130`, `S218`, `S246`

### LLM-003 · Lost in the Middle 为什么发生？长 Context 中信息位置会怎样影响模型利用率？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：Agent, RAG
- **Topic**：Long-context Limitation
- **Question Type**：Why
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S002`, `S130`

### LLM-004 · 从 Prompt 输入到逐 Token 生成，一次 LLM Generation 的底层路径怎样解释？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Inference / Generation
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S241`, `S258`

---

## 3. Transformer / Attention

### LLM-005 · Transformer 的整体 Architecture 是什么？Attention、FFN、Residual / Normalization 等模块怎样协作？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Transformer Architecture
- **Question Type**：Concept / Deep Dive
- **Depth**：L2
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S002`, `S006`, `S095`, `S101`, `S102`, `S124`, `S126`, `S150`, `S152`, `S258`

### LLM-006 · Self-Attention 中 Q / K / V 怎样产生并计算？为什么这种结构能建模 Token 关系？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：QKV / Self-Attention
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**7**
- **Evidence Sources**：`S002`, `S008`, `S095`, `S126`, `S141`, `S152`, `S258`

### LLM-007 · Multi-Head Attention 为什么需要多个 Head？不同 Head 带来什么表达能力？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Multi-Head Attention
- **Question Type**：Why / Coding
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S002`, `S006`, `S126`, `S152`, `S272`

### LLM-008 · FFN 在 Transformer 中承担什么作用？Attention 与 FFN 为什么都需要？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：FFN
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S126`

### LLM-009 · RoPE / Rotary Positional Embedding 的核心思想是什么，位置关系怎样进入 Attention？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Positional Encoding / RoPE
- **Question Type**：Concept / Coding
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S272`

### LLM-010 · Transformer 为什么能够扩展到多模态？Visual Encoder 与 Language Model 怎样连接 / 对齐？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：RAG
- **Topic**：Multimodal Foundation
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S018`, `S098`, `S099`, `S126`

---

## 4. Inference / Serving

### LLM-011 · KV Cache 为什么能加速 Autoregressive Generation？它怎样影响显存与并发？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：KV Cache
- **Question Type**：Why / System
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S013`, `S071`, `S152`

### LLM-012 · Prefill 与 Decode 分别是什么？为什么 Serving 会关注 Prefill / Decode 分离？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Prefill / Decode
- **Question Type**：Concept / Why
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S071`

### LLM-013 · PagedAttention 的核心思想是什么？vLLM / SGLang 等 Serving Engine 主要优化什么？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Inference Engine
- **Question Type**：Concept / Comparison
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S054`, `S064`, `S184`, `S255`

### LLM-014 · LLM API Latency 通常由哪些阶段构成？TTFT、生成速度、模型大小与并发怎样影响用户体验？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：AI Backend Engineering
- **Topic**：Inference Latency
- **Question Type**：Troubleshoot / Trade-off
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S172`, `S209`, `S257`

---

## 5. Model API / Sampling / Selection

### LLM-015 · Temperature、Top-k、Top-p 等 Sampling 参数怎样影响生成？为什么 Temperature=0 仍不保证绝对确定？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Sampling Parameters
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S014`, `S079`, `S183`

### LLM-016 · Chat / Model API 中 Messages、Role、Model 与其它常见字段怎样组织？应用层如何适配不同 Provider？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：Agent
- **Topic**：Model API
- **Question Type**：Concept / System Design
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**5**
- **Evidence Sources**：`S119`, `S172`, `S183`, `S241`, `S246`

### LLM-017 · Base Model / Model Size 应怎样选？效果、Latency、Cost、Context、Tool Calling 与业务风险如何权衡？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Model Selection
- **Question Type**：Trade-off / Project
- **Depth**：L4
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S089`, `S092`, `S112`, `S139`, `S151`, `S177`, `S221`, `S246`, `S255`, `S260`

---

## 6. Embedding / Rerank Model Foundation

### LLM-018 · Embedding 为什么能表示语义？Embedding Model 怎样训练，Dimension / Backbone 变化带来什么权衡？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：Vector DB, RAG
- **Topic**：Embedding Model
- **Question Type**：Concept / Why
- **Depth**：L2
- **Interview Heat**：🔥🔥
- **Source Count**：**6**
- **Evidence Sources**：`S095`, `S141`, `S178`, `S211`, `S255`, `S272`

### LLM-019 · Embedding Model、Bi-Encoder 与 Cross-Encoder / Reranker 的目标、计算方式和成本有什么差异？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：Vector DB, RAG
- **Topic**：Rerank Model
- **Question Type**：Comparison / Why
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S095`, `S211`, `S272`

---

## 7. Post-training / Alignment

### LLM-020 · Fine-tuning 的基本流程是什么？应用工程师在 Dataset、Training、Evaluation 与 Deployment 上需要理解到什么深度？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：RAG
- **Topic**：Fine-tuning
- **Question Type**：Concept / Project
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**9**
- **Evidence Sources**：`S052`, `S097`, `S107`, `S126`, `S141`, `S150`, `S151`, `S158`, `S233`

### LLM-021 · SFT、LoRA、PPO、DPO、GRPO、Knowledge Distillation 分别解决什么问题，什么时候值得使用？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Topic**：Post-training / Alignment
- **Question Type**：Comparison / Why
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**8**
- **Evidence Sources**：`S002`, `S052`, `S062`, `S107`, `S152`, `S197`, `S222`, `S233`

### LLM-022 · Hallucination / Factuality 问题为什么出现？哪些属于模型本身局限，哪些应由 RAG / Agent / Verification 层治理？

- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：RAG, Agent
- **Topic**：Hallucination / Factuality
- **Question Type**：Why / Troubleshoot
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**10**
- **Evidence Sources**：`S003`, `S052`, `S085`, `S100`, `S103`, `S120`, `S148`, `S192`, `S196`, `S224`

---

## 7.5 Prompt Engineering（Phase 2B 补漏）

### LLM-023 · Prompt Engineering 应怎样从目标、角色、约束、Context、Example、Tool 与 Output Contract 组织并迭代？怎样用真实 Case / Evaluation 证明 Prompt 优化有效？
- **Primary Module**：LLM Foundation（应用工程深度）
- **Related Modules**：RAG, Agent
- **Topic**：Prompt Engineering
- **Question Type**：Concept / Project / Evaluation
- **Depth**：L3
- **Interview Heat**：🔥🔥🔥
- **Source Count**：**30**
- **Evidence Sources**：`S003`, `S008`, `S016`, `S029`, `S044`, `S049`, `S055`, `S066`, `S068`, `S071`, `S074`, `S092`, `S099`, `S100`, `S102`, `S107`, `S150`, `S159`, `S168`, `S178`, `S179`, `S200`, `S208`, `S210`, `S221`, `S230`, `S233`, `S238`, `S263`, `S277`

---

## 8. 十板块归属审计结论

本模块不再承载 RAG Retrieval Pipeline 或 Vector DB Index 题：

- Embedding / Rerank **模型原理**保留在 `LLM-018` / `LLM-019`；
- Embedding Vector 的存储、ANN / HNSW / IVF 归 `Vector DB`；
- Dense / Sparse、Hybrid、RRF、Rerank Pipeline、Top-K 与 Retrieval Evaluation 归 `RAG`；
- Long-context 的**模型本体限制**保留在 `LLM-002` / `LLM-003`，而 Context Assembly / Compaction / Memory 属于 `Agent`；
- Serving Engine / KV Cache / Prefill-Decode 属于模型推理基础，不迁入通用 AI Backend。

本轮没有需要迁出的 ACTIVE Canonical；22 道均保持唯一 Primary Ownership。

---

## 9. 对课程结构的直接信号

LLM Foundation 应控制在“应用工程深度”，但不能浅成术语解释。真人面试至少要求形成下面这条因果链：

```text
Token / Context
      ↓
Transformer / Attention
      ↓
Generation / KV Cache / Serving
      ↓
Model API / Sampling / Model Selection
      ↓
Embedding / Rerank
      ↓
Fine-tuning / Alignment 的使用边界
```

后续进入 RAG 与 Agent 时，就可以直接解释“为什么这个系统行为会发生”，而不是重新补模型基础。
