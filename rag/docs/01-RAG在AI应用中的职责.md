# 01｜RAG 在 AI Application 中负责什么

## 1. 先讲人话

LLM 很强，但它不是你的企业数据库，也不会天然知道今天刚更新的制度。

RAG = Retrieval-Augmented Generation。

核心思想：

```text
User Question
    ↓
先从外部知识源找到相关证据
    ↓
把证据放进当前 Context
    ↓
让 LLM 基于证据回答
```

它不是“给 LLM 加一个向量库”这么简单，而是一套**知识进入、检索、证据构造、生成和验证系统**。

---

## 2. RAG 主要解决什么

### 私有知识

例如：

- 公司内部 Wiki；
- 产品文档；
- 合同 / 制度；
- 用户自己的文件。

### 新鲜知识

知识今天更新，不想重新训练模型。

### 可引用知识

回答要能说：

> 这句话来自哪个 Document / Page / Section？

### 大规模知识

知识库远大于 Context Window，必须先检索再注入。

---

## 3. RAG 不能解决所有问题

### 行为风格问题

模型总是不按特定品牌口吻说话，可能是 Prompt / Fine-tuning 问题。

### 实时事务状态

订单余额、库存、账户权限，更适合调用 Tool / DB，而不是把所有状态向量化。

### Runtime Reliability

Tool 超时、重试、Checkpoint、Permission 不是 RAG 的职责。

### 模型能力不足

模型连给定证据里的复杂推理都做不好，单纯增加 Retrieval 不一定解决。

---

## 4. RAG vs Long Context

Long Context 解决：

> 单次能放多少 Token。

RAG 解决：

> 在大量知识中，当前到底应该放哪些证据。

现实中经常是组合：

```text
Large Corpus
   ↓
RAG 找到相关内容
   ↓
Long Context 容纳较丰富 Evidence
```

不是简单二选一。

---

## 5. RAG vs Fine-tuning

### RAG

改变：

```text
当前模型看到的外部知识
```

适合：

- 知识频繁变化；
- 需要引用；
- 多租户权限；
- 私有 Corpus。

### Fine-tuning

改变：

```text
模型长期行为倾向
```

适合：

- 稳定任务模式；
- 风格；
- 分类边界；
- 专用行为。

---

## 6. RAG vs 文件搜索 / Tool Search

不是所有 Retrieval 都必须 Vector DB。

例如：

```text
文件名明确
→ Filesystem Search

精确错误码
→ Keyword / grep

结构化字段
→ SQL / Metadata Filter

语义相似问题
→ Dense Retrieval
```

成熟系统应该根据数据和 Query 选择检索机制，而不是强行全向量化。

---

## 7. Production RAG 的完整责任链

```text
Source
→ Ingestion
→ Parse
→ Clean
→ Chunk
→ Metadata / Permission
→ Embed / Index
→ Query Transform
→ Retrieve
→ Fuse
→ Rerank
→ Context Build
→ Generate
→ Ground / Cite
→ Evaluate
→ Observe
→ Update / Rollback
```

所以真正难点通常不是：

> “会不会调 `similarity_search()`。”

而是：

> 哪一层出了错，怎么证明改动真的更好？

---

## 8. 一个最重要的思维模型

RAG 输出错时，不要第一反应：

> “换一个更强 Embedding。”

先沿链路问：

```text
Corpus 对吗？
Parse 完整吗？
Chunk 切坏了吗？
Query 理解对吗？
Retriever 召回了吗？
Fusion / Rerank 排对了吗？
Context 拼对了吗？
LLM 使用证据了吗？
Citation 映射对吗？
```

这叫 Failure Attribution。

---

## 9. 🎯 面试怎么回答

> RAG 的作用不是单纯给 LLM 接向量库，而是把外部、私有、可更新的知识转成当前请求可验证的 Evidence。完整链路包括 Corpus、Parsing、Chunking、Embedding / Index、Query Transformation、Retrieval、Fusion、Rerank、Context Construction、Generation、Grounding 和 Evaluation。Long Context 解决容量，RAG 解决信息选择；动态事实优先 RAG / Tool，稳定行为差距才考虑 Fine-tuning。

---

## 10. ⚠️ 易错点

错误：

> 有 Vector DB 就是 RAG。

错误：

> Context Window 足够大就不需要 RAG。

错误：

> RAG 一定能消灭 Hallucination。

错误：

> RAG 只负责 Retrieval，Corpus 和 Evaluation 不重要。

---

<details>
<summary>自测：公司政策每周更新且回答必须引用来源，为什么 RAG 比 Fine-tuning 更自然？</summary>

因为知识可以独立更新、删除和版本化，检索结果还能映射回真实来源；如果频繁 Fine-tune，更新与撤回成本高，也难做权限和 Citation。

</details>
