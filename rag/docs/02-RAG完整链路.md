# 02｜Production RAG End-to-end Pipeline

## 1. 一张总图

完整 RAG 最好拆成两条链。

### Offline / Ingestion

```text
Data Source
→ Load
→ Parse / OCR / Layout
→ Clean / Dedup
→ Chunk
→ Metadata / Permission
→ Embedding
→ Index / Store
```

### Online / Query

```text
User Query
→ Normalize / Rewrite / Clarify
→ Retrieve
→ Hybrid / Fusion
→ Rerank
→ Top-K / Threshold
→ Context Construction
→ LLM
→ Grounding / Citation
→ Response
```

旁边必须还有：

```text
Evaluation
Observability
Freshness / Version
Permission
Cost / Latency
```

---

## 2. Ingestion 不是“把 PDF 扔进向量库”

一份文档真正进入系统前，要回答：

- 来源是谁？
- 当前版本是什么？
- 是否允许索引？
- Parser 是否完整？
- 是否重复？
- 表格 / 图片是否丢失？
- Chunk 如何映射回原文？
- Permission 如何跟随 Chunk？

如果这些问题没解决，后面 ANN 再快也没有意义。

---

## 3. Query 也不是直接 Embed

真实用户 Query 可能：

- 太短；
- 有歧义；
- 有代词；
- 同时问多个问题；
- 带精确型号 / 编号；
- 实际应该先澄清。

所以在线链路经常需要：

```text
raw query
→ intent / normalize
→ rewrite / decomposition
→ retrieval query
```

---

## 4. Retrieve 不是最后一步

Retriever 更偏“尽量别漏掉正确候选”。

随后还可能：

```text
Dense Results
+
BM25 Results
→ Fusion
→ Rerank
→ Final Evidence
```

于是检索系统的目标通常不是单纯追求 Top-1，而是逐层把：

```text
Recall
→ Precision
→ Context Quality
```

做好。

---

## 5. Context Construction 是独立步骤

检索到 10 个 Chunk，不代表直接把 10 个原样拼到 Prompt。

还要考虑：

- 去重；
- 排序；
- 邻居块；
- Parent Context；
- 标题；
- Source ID；
- 权限；
- Token Budget；
- 冲突版本。

所以：

```text
Retrieved Candidates
≠
Final LLM Context
```

---

## 6. Generation 也需要边界

LLM 应该知道：

- 哪些内容是 Evidence；
- Evidence 不足时怎么办；
- Citation 怎样输出；
- 是否允许使用参数知识；
- 冲突证据怎样处理。

高可信知识助手通常会要求：

> 没有足够证据时明确说不知道，而不是补全一个听起来合理的答案。

---

## 7. Evaluation 必须横穿全链路

不能只评最终答案。

至少分：

```text
Data Quality
Parsing Quality
Chunk Quality
Retrieval Quality
Rerank Quality
Context Quality
Answer Correctness
Faithfulness / Grounding
Latency / Cost
```

否则“最终答案变差”时无法定位是哪一层。

---

## 8. Trace 是 Production 必需品

每次请求最好能回放：

```text
raw_query
rewritten_query
retrieved_chunk_ids + scores
fusion ranks
rerank scores
final_context_ids
prompt_version
model_version
answer
citations
latency_by_stage
```

没有 Trace，就很难做 Bad Case Attribution。

---

## 9. Offline / Online 的版本必须能对应

一次回答至少应该知道自己用了：

```text
Corpus Version
Parser Version
Chunk Strategy Version
Embedding Version
Index Version
Reranker Version
Prompt Version
Model Version
```

不一定每个都暴露给用户，但内部必须可追溯。

---

## 10. 🎯 面试怎么回答

> Production RAG 我会拆成 Offline Ingestion 和 Online Query 两条链。Offline 从 Source、Parse、Clean、Chunk、Metadata / Permission 到 Embedding / Index；Online 从 Query Transformation、Retrieve、Hybrid / Fusion、Rerank、Top-K 到 Context Construction、LLM 和 Citation。Evaluation、Trace、Version、Permission、Freshness 是横向能力。这样 Bad Case 才能按数据、检索、排序、Context、生成逐层归因，而不是只调一个向量库参数。

---

<details>
<summary>自测：为什么 Retrieved Top-K 不能直接等价于最终 Context？</summary>

因为候选可能重复、顺序不合理、缺邻居块、超过 Token Budget、包含旧版本或权限不符。Context Construction 需要在最终送给 LLM 前再次治理。

</details>
