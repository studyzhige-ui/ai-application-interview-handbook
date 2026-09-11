# 30｜Bad Case Attribution：到底坏在哪一层

## 1. 先讲人话

用户说“RAG 答错了”只是现象，不是根因。

真正的排查必须沿 Pipeline 分层：

```text
Source
→ Parse
→ Clean
→ Chunk
→ Embed / Index
→ Query Transform
→ Retrieve
→ Fusion
→ Rerank
→ Context
→ Prompt / Model
→ Answer / Citation
```

Bad Case Attribution 的目标是：

> **把“答案错”定位成某一层可修复的问题。**

---

## 2. 第一问：Source 里有答案吗？

如果 Source of Truth 本身没有信息：

```text
不是 Retrieval Bug
```

此时应该：

- 更新知识源；
- Refuse；
- Clarify；
- 使用其它数据源。

---

## 3. Parsing / Cleaning 问题

检查：

- OCR 是否识别错；
- 表格是否断裂；
- Cleaner 是否误删正文；
- 页面顺序是否错；
- 最新版本是否成功 Ingest。

---

## 4. Chunking 问题

典型症状：

- 条件和结论被拆开；
- 标题丢失；
- Chunk 太大；
- Overlap 重复；
- Parent Relation 丢失。

---

## 5. Retrieval 问题

先问：

> Ground Truth Chunk 是否进入候选？

如果没有：

- Query Rewrite；
- Embedding；
- Sparse；
- Filter；
- ANN；
- Candidate Budget；
- Freshness。

如果已经召回，就继续看 Rerank / Context。

---

## 6. Rerank 问题

正确 Evidence 在候选里，却被排到后面：

- Domain Mismatch；
- Truncation；
- Score 配置；
- Candidate Diversity；
- Query Drift。

---

## 7. Context Construction 问题

正确 Evidence 虽然排前，但最终没有进入 Prompt：

- Token Budget 截断；
- 去重误删；
- Parent Expansion 错；
- Version / Permission Filter 错；
- 排序错误。

---

## 8. Generation 问题

正确 Evidence 已经完整进入 Context，模型仍答错：

- Prompt 约束不足；
- Evidence 冲突；
- 模型推理错误；
- Hallucination；
- Output Parsing 错。

这时才主要属于 Generation 层。

---

## 9. Trace 是 Attribution 的前提

每次请求至少保存：

```text
query / rewrite
filters
candidate ids + scores
fusion
rerank
final context
source/version
prompt/model
answer/citation
latency
```

没有 Trace，就只能凭感觉调参数。

---

## 10. 建立 Bad Case Taxonomy

长期可以统计：

```text
Parsing 12%
Chunk 18%
Retrieval 30%
Rerank 10%
Context 8%
Generation 15%
Data Freshness 7%
```

这样优化优先级来自真实故障分布，而不是个人偏好。

---

## 11. 🎯 面试怎么回答

> RAG Bad Case 不能直接归因成“模型幻觉”。我会先确认 Source 是否有答案，再逐层检查 Parsing、Chunk、Query Transform、Retrieval、Rerank、Context 和 Generation。最关键的分界是 Ground Truth 是否进入候选、是否被排前、是否进入最终 Context。Production 中要保留完整 Trace，并建立 Bad Case Taxonomy，用真实故障分布指导优化。

## 12. ⚠️ 易错点

- 所有错误都叫 Hallucination；
- 一出错就换 Embedding Model；
- 没有请求 Trace；
- 只修单个 Case，不沉淀 Failure Category。

<details><summary>查看参考答案：定位 RAG 错误最关键的三个检查点是什么？</summary>

1. 正确 Evidence 是否存在于 Source；2. 是否进入 Retrieval/Rerank Candidate；3. 是否真正进入最终 LLM Context。三个分界能迅速把问题定位到数据、检索或生成阶段。

</details>
