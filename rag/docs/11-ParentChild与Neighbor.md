# 11｜Parent-child、Neighbor Window 与 Context Expansion

## 1. 先讲人话

很多 RAG 系统会发现一个天然冲突：

```text
检索希望 Chunk 小一点
生成希望 Context 完整一点
```

Parent-child 和 Neighbor Window 就是在解决这个冲突。

---

## 2. Parent-child Retrieval

把一个大 Section 作为 Parent，再切成多个 Child：

```text
Parent: “退款政策”
├── Child A: 适用范围
├── Child B: 退款条件
├── Child C: 时间限制
└── Child D: 例外情况
```

索引 Child，是因为小块更容易精准匹配 Query；命中后回取 Parent，是因为 LLM 需要更完整的上下文。

---

## 3. Neighbor Window

另一种方式是命中一个 Chunk 后，补它前后相邻块：

```text
chunk_17 命中
→ 补 chunk_16 + chunk_18
```

适合顺序关系明显的长文档。

但不能机械地永远扩 N 个邻居，因为：

- 可能跨章节；
- 可能把无关内容拉进来；
- Context Token 上升。

因此最好结合 `section_id / parent_id / position` 控制 Expansion。

---

## 4. Context Expansion 的常见策略

### Parent Expansion

命中 Child → 回 Parent。

### Neighbor Expansion

命中当前 Chunk → 加前后窗口。

### Heading Expansion

补当前 Heading / Section Path。

### Table Expansion

命中某个 Cell / Row → 回取完整表头、行列说明。

### Conditional Expansion

只有当 Query 类型或候选不足时才扩大上下文。

---

## 5. 为什么不能直接索引大 Parent

如果一开始就把完整 Parent 作为 Retrieval Unit：

- Embedding 会混合多个子主题；
- 相似度可能不够尖锐；
- Top-K 中携带大量无关文字。

所以“细粒度召回 + 粗粒度补全”通常比单一粒度更灵活。

---

## 6. 数据模型前置

Parent-child 不是只写一个算法名字，需要数据层支持：

```text
parent_id
chunk_id
position
section_path
previous_chunk_id
next_chunk_id
```

如果这些关系在 Ingestion 时没保存，Query 时再想做 Context Expansion 会很麻烦。

---

## 7. Failure Case

### Child 命中但 Parent 太大

回取整章导致 Context 爆炸。可以改成只回当前 Section 或 Neighbor Window。

### Neighbor 跨章节

前一块属于“产品 A”，后一块已经进入“产品 B”，机械扩展造成事实混合。

### 多个命中重复扩展同一 Parent

Candidate 里多个 Child 都来自同一 Parent，最终 Context 重复。需要去重和 Coverage 控制。

---

## 8. 🎯 面试怎么回答

> Parent-child 的核心是把 Retrieval Granularity 和 Generation Context Granularity 分开：小 Child 用于精准召回，命中后回取较完整的 Parent 或邻居窗口。这样能缓解 Chunk 太小导致语义不完整、Chunk 太大导致检索不精准的矛盾。Production 中要保存 parent_id、position、section_path，并对 Expansion 做去重、Token Budget 和跨章节边界控制。

## 9. ⚠️ 易错点

- “Parent-child 就是多存一份文本”——关键是双层检索/回取语义。
- “命中后永远回整篇文档”——容易导致 Context Noise。
- “Neighbor Window 固定 ±2”——应结合结构与预算。

## 10. 🔍 继续追问

- Parent 和 Child 都要 Embedding 吗？
- 多个 Child 命中同一个 Parent 怎么去重？
- Expansion 在 Rerank 前还是后做？

<details><summary>查看参考答案：Expansion 在 Rerank 前还是后更合理？</summary>

没有绝对唯一答案。常见做法是先在细粒度 Candidate 上 Retrieval / Rerank，选出高质量证据后再做 Parent / Neighbor Expansion，避免候选阶段被大段上下文拖慢；但如果 Reranker 需要更完整语义，也可以先轻量扩展再排序。应通过实验验证。

</details>
