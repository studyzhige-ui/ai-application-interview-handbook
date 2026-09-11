# 04｜Long Context 与 Lost in the Middle

> Context Window 变大，只代表“能放进去更多”，不代表“模型会同样好地利用每一部分”。

## 1. 先讲人话

假设你给模型一本 200 页的资料，并把真正答案放在中间某个角落。

即使模型“能读完”，也不意味着它对：

```text
开头信息
中间信息
结尾信息
```

利用得一样好。

这类现象常被概括为：

> **Lost in the Middle**：长上下文中，位于中间的信息可能更难被稳定利用。

---

## 2. Long Context 解决了什么

它主要扩展：

- 单次请求可输入的历史；
- 大文档直接读取能力；
- 多文件 / 多轮上下文容量；
- Agent 长任务中可保留的事件量。

但它没有自动解决：

```text
Relevant Information Discovery
Noise Filtering
Permission
Freshness
Citation
Memory Lifecycle
Cost
Latency
```

所以更大窗口不是 Retrieval Engineering 的替代品。

---

## 3. 为什么“放进去”不等于“利用好”

从应用工程角度，可以把原因理解成几类：

### 3.1 注意力资源不是无限的

序列越长，需要处理的 Token 关系越多。

即使模型支持长上下文，也可能对不同位置和不同信息类型有不同敏感度。

### 3.2 无关信息形成竞争

Context 里如果包含大量：

- 重复历史；
- 低价值 Tool Log；
- 多个相似文档；
- 冲突规则；
- 旧信息；

真正重要的信息会被噪声包围。

### 3.3 位置本身可能影响利用率

大量实验观察到长上下文中的信息位置会影响任务表现。

应用上最重要的结论不是背曲线，而是：

> 不要假设“只要答案在 Context 里，模型就一定能找到”。

---

## 4. Long Context 与 RAG 的关系

很多人会问：

> 既然模型有 1M Context，还需要 RAG 吗？

需要分问题。

### Long Context 更擅长

- 单个有限资料包；
- 一次性代码 / 文档分析；
- 不想额外建设索引的小规模场景。

### RAG 更擅长

- 大规模语料；
- 数据持续更新；
- 权限过滤；
- 需要引用；
- 需要降低输入 Token；
- 需要可观测检索结果；
- 多租户知识库。

现实系统常常是：

```text
RAG 先找到相关内容
        ↓
Long Context 容纳更丰富证据
```

而不是二选一。

---

## 5. Long Context 与 Agent Compaction 的关系

Agent 长任务会持续产生：

```text
Messages
Tool Calls
Tool Results
Plans
Errors
File Diffs
Observations
```

即使窗口很大，也会逐渐消耗完。

因此成熟 Agent Runtime 仍需要：

```text
Context Assembly
→ Budget
→ Compression / Summary
→ Important State Preservation
→ Resume
```

Long Context 只是延后问题，不会消灭问题。

---

## 6. 应用层怎样提高长 Context 可用性

常见手段：

### 6.1 Retrieval

先缩小候选信息。

### 6.2 Rerank

把更重要证据放在更高优先级位置。

### 6.3 Structured Context

使用清晰边界：

```text
Goal
Constraints
Evidence A
Evidence B
Tool Result
Output Contract
```

### 6.4 去重与压缩

不要把相同历史、重复文档、完整 Tool Raw Log 反复塞进去。

### 6.5 把关键约束放在稳定位置

重要 System / Policy / Output Contract 不应淹没在大量低价值内容中。

---

## 7. Failure Case

### Failure 1：扩大窗口后直接把整个知识库拼进去

问题从“召回不到”变成：

- 请求巨大；
- 成本升高；
- 延迟变大；
- 噪声增加；
- 权限难控制。

### Failure 2：重要约束只出现一次，随后被长历史淹没

长 Agent Session 中尤其常见。

### Failure 3：Context 中同时存在新旧两份事实

模型可能无法知道哪一个是权威版本。

这已经是 Version / Freshness / Context Governance 问题。

---

## 8. 🎯 面试怎么回答

> Long Context 提高的是单次推理的容量上限，但容量不等于有效利用率。长序列中会有噪声竞争、位置敏感和成本问题，Lost in the Middle 就提醒我们：答案在 Context 里并不保证模型稳定使用。因此 Production 系统一般仍会做 Retrieval、Rerank、结构化 Context、去重和 Compaction。Long Context 与 RAG / Memory 更多是互补关系，而不是替代关系。

---

## 9. ⚠️ 易错点

错误：

> 只要模型支持超长 Context，就不需要向量数据库。

错误：

> Lost in the Middle 等于模型完全看不到中间 Token。

更准确：

> 这是长上下文利用率与位置敏感问题，不是一个“中间 Token 被硬截断”的规则。

---

## 10. 🔍 继续追问

- Long Context 成本为什么高？
- Attention 的计算与序列长度有什么关系？
- RAG 和 Long Context 怎么组合？
- Agent 为什么还需要 Compaction？
- Context 中出现冲突事实怎么办？

---

<details>
<summary>自测 1：模型能接收 200k Token，是否说明 200k 内每条证据利用率一致？</summary>

不是。Context Window 只定义容量边界，实际信息利用还受位置、噪声、模型能力和任务结构影响。

</details>

<details>
<summary>自测 2：为什么 Long Context 不能替代权限过滤？</summary>

因为是否“能放进去”与是否“应该让当前用户看到”是两个问题。权限必须在应用 / Retrieval 层治理，不能靠模型自己忽略无权访问的信息。

</details>
