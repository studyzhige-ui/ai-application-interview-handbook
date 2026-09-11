# 21｜Memory Architecture 与生命周期

## 1. Memory 不是一个 vector_db

先按时间与语义分：

```text
Working Memory   当前 Run 临时信息
Episodic Memory  过去任务 / interaction
Semantic Memory  稳定知识 / preference
Procedural Memory 可复用步骤 / skill
```

不同 Memory 生命周期不同。

## 2. Memory 写入

不要“每轮自动总结全部写长期 Memory”。

应该有：

```text
candidate
→ importance / confidence
→ dedup / conflict
→ write
```

否则错误结论会永久污染未来任务。

## 3. Memory 读取

```text
current task
→ retrieve candidate memories
→ filter by relevance / tenant / freshness
→ inject selected memory
```

Memory store 和 Context 是两层。

## 4. Forget / Update

长期 Memory 需要：

- version；
- timestamp；
- source；
- confidence；
- superseded / delete。

## 5. Memory Pollution

真人追问常见：错误 summary 写入 Memory 后怎么办？

可用：

```text
provenance
confidence
write gate
user correction
versioning
revalidation
```

## 🎯 面试

我会把 Memory 当有生命周期和 provenance 的外部信息层，而不是无限 append 的聊天摘要。写入要筛选和去重，读取要按 relevance/freshness/permission 选择，错误 Memory 必须能修正、失效或删除。

<details><summary>自测：Conversation History 等于 Memory 吗？</summary>

不等于。History 是过去事件记录；Memory 是从过去信息中选择、持久化、未来可重新取回的内容。
</details>
