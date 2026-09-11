# 12｜Semantic Boundary Failure：被切断的逻辑怎样修

## 1. 先讲人话

Chunking 最危险的问题不是“长度不合适”，而是：

> **把一个必须整体理解的逻辑关系切开。**

比如：

```text
只有同时满足 A 和 B，才允许退款。
但以下三类情况除外……
```

如果条件、结论和例外被切成三个互不关联的 Chunk，Retriever 可能只召回其中一块，LLM 就会得到不完整证据。

这就是 Semantic Boundary Failure。

---

## 2. 哪些内容最容易被切坏

- 充分 / 必要条件；
- 定义 + 例外；
- 法律条款；
- 操作步骤；
- 表格表头 + 数据行；
- 公式 + 解释；
- API 参数 + 返回约束；
- 跨页表格；
- 代码函数 + 注释 / 类型。

---

## 3. 常见修复方法

### Structure-aware Chunk

优先按章节、条款、列表、表格、代码符号等自然结构切。

### Overlap

给边界加少量重叠，降低句子被截断的概率。

### Parent-child

小块召回，命中后回完整 Section。

### Neighbor Expansion

命中后补前后相邻 Chunk。

### Relation-aware Metadata

保存：

```text
parent_id
section_id
position
previous_id
next_id
```

让 Query 阶段能恢复关系。

### Query-time Reconstruction

对特定 Query，例如“条件是什么”“有哪些例外”，主动合并相关兄弟块。

---

## 4. 为什么“加大 Chunk”不是万能解

直接把 Chunk 调大确实可能减少边界切断，但会引入新问题：

- Retrieval 变粗；
- Embedding 混合多个主题；
- Context Noise 增大；
- Token Cost 上升。

所以更成熟的思路是：

```text
结构识别
+ 关系保存
+ 小粒度检索
+ 按需扩展
```

而不是一味变大。

---

## 5. 怎样发现 Semantic Boundary Failure

Bad Case 中常见症状：

- 检索结果“每一块都像是对的，但组合起来缺条件”；
- LLM 回答漏掉例外；
- Citation 只指向半条规则；
- Retrieval Recall 看似命中，但 End-to-end Answer 错。

排查时回到原始文档对照：

```text
Source
→ Parsed Structure
→ Chunk Boundary
→ Retrieved Chunks
→ Final Context
```

---

## 6. AI 应用案例

### 合同问答

用户问：“什么情况下可以提前解除合同？”

如果“允许条件”和“禁止例外”分属不同 Chunk，单纯 Top-1 Retrieval 很容易误答。

更可靠的策略：

```text
命中主条款
→ 根据 section_id 回取相邻例外条款
→ 一起进入 Context
```

---

## 7. 🎯 面试怎么回答

> Semantic Boundary Failure 指 Chunking 把必须整体理解的逻辑关系拆开，比如条件、结论、例外、表头和数据行。它不能只靠把 Chunk 调大解决，更合理的是使用 Structure-aware Chunk、Parent-child、Neighbor Expansion 和关系 Metadata，并在 Bad Case 中从原文、解析结构、Chunk 边界、检索结果到最终 Context 分层定位。

## 8. ⚠️ 易错点

- “Overlap 可以解决所有边界问题”——复杂关系可能跨多个块。
- “Recall 命中了就没问题”——命中半条规则仍可能答错。
- “Chunk 大一点就好了”——会牺牲检索精度与成本。

## 9. 🔍 继续追问

- 如何针对表格做 Boundary Recovery？
- 如何评估 Chunk 边界是否真的改善？
- Parent-child 和 Neighbor Expansion 怎么选？

<details><summary>查看参考答案：为什么 Retrieval Recall 高，答案仍可能错？</summary>

因为 Recall 只说明某个相关证据被召回，不保证完整关系全部进入 Context。Semantic Boundary Failure 可能让“条件”和“例外”被拆开，因此需要对 Evidence Completeness 和 End-to-end Answer 一起评估。

</details>
