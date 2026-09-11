# 25｜Hallucination、Factuality 与 Verification Boundary

## 1. 先讲人话

LLM 的训练目标主要是：

> 根据上下文生成高概率的下一个 Token。

它不是一个天然带外部事实校验器的数据库。

所以模型可能生成：

```text
语言上很合理
语气上很自信
实际上是错的
```

这类事实性错误通常被称为 Hallucination。

---

## 2. 不要把所有错误都叫幻觉

一个 AI 系统回答错，根因可能在不同层。

```text
Wrong Answer
├─ Model knowledge wrong
├─ Prompt ambiguous
├─ RAG retrieved wrong chunk
├─ Reranker reordered badly
├─ Context contains stale data
├─ Tool returned error
├─ Tool result was parsed wrong
├─ User asked underspecified question
└─ Model fabricated unsupported detail
```

如果不先做 Attribution，就无法知道该修哪一层。

---

## 3. 模型本体为什么会产生事实错误

从应用工程角度理解几个核心原因：

### 3.1 训练目标不是事实查询

模型优化 next-token likelihood，不是每句话都和实时数据库核验。

### 3.2 参数知识有时间边界

模型训练数据有截止时间与覆盖偏差。

### 3.3 长尾知识弱

冷门事实、细粒度数字、公司内部知识可能没有可靠参数记忆。

### 3.4 生成需要继续

在证据不足时，模型仍可能倾向生成一个流畅 continuation，而不是天然停止。

---

## 4. Factuality 和 Calibration

一个关键问题是：

> 模型知道自己不知道吗？

如果模型在未知问题上仍给出高置信措辞，就属于校准不好。

应用可以通过：

- 明确拒答规则；
- Evidence Requirement；
- Retrieval；
- Tool Query；
- Verification；

降低风险。

但不要把“请不要胡说”当成完整治理方案。

---

## 5. RAG 能解决什么

RAG 可以把外部证据放进 Context：

```text
Query
→ Retrieve Evidence
→ LLM Generate from Evidence
```

它有助于：

- 私有知识；
- 新鲜知识；
- 引用；
- 可追溯性。

但 RAG 也会失败：

```text
没召回
召回错
Chunk 不完整
Context 冲突
模型没使用证据
```

所以：

> RAG 能降低某类 Hallucination，不等于消灭 Hallucination。

---

## 6. Tool 能解决什么

对于：

- 实时余额；
- 天气；
- 订单状态；
- 数据库统计；

更合理的是调用权威 Tool，而不是让模型靠参数知识猜。

但 Tool 结果仍可能：

- 超时；
- 错误；
- 权限失败；
- 返回脏数据。

因此 Agent Runtime 还要做验证。

---

## 7. Verification Layer

高风险系统应该在生成后继续验证：

```text
Generated Claim
→ Evidence Check
→ Schema / Rule Validation
→ Citation Check
→ Business Constraint
→ Human Review if needed
```

例如代码 Agent：

```text
Generate Patch
→ Compile
→ Unit Test
→ Static Check
→ Diff Review
```

这类 Verification 不能只靠模型“自我反思一句”。

---

## 8. Citation 不等于 Grounding

模型可以生成一个看起来像引用的 URL 或文档编号。

真正可靠的 Citation 应该：

- 来自 Retriever / Tool 的真实 Source ID；
- 能回到具体证据；
- Claim 与 Evidence 匹配；
- 不允许模型随意编造 Source。

完整 Grounding / Citation Pipeline 在 RAG 模块展开。

---

## 9. 怎样评估 Hallucination

不能只问：

> “感觉回答真实吗？”

可以构建：

- Known-answer factual QA；
- Evidence-grounded QA；
- Unanswerable Questions；
- Contradictory Context；
- Freshness Cases；
- Citation Accuracy Cases。

指标可能包括：

```text
Factual Accuracy
Unsupported Claim Rate
Abstention Accuracy
Citation Precision
Task Success
```

---

## 10. 风险分层

### Low Risk

创意写作、Brainstorm。

允许一定开放性。

### Medium Risk

企业知识助手。

需要 Grounding / Citation。

### High Risk

金融、医疗、法律、自动执行 Tool。

需要更强 Verification、权限、Human-in-the-loop。

系统强度应该和错误代价匹配。

---

## 11. 🎯 面试怎么回答

> Hallucination 的根本原因之一是 LLM 优化的是条件生成概率，不是实时事实查询，因此语言流畅不等于事实正确。工程上我先做 Failure Attribution，区分模型本体、RAG、Tool、Context 和解析错误；再根据场景用 RAG 提供证据、Tool 获取权威状态、拒答规则处理证据不足，并在高风险任务增加 Citation / Business Rule / Test / Human Review 等 Verification。RAG 能降低部分事实错误，但不能保证零幻觉。

---

## 12. ⚠️ 易错点

错误：

> Temperature 调到 0 就不会 Hallucinate。

错误：

> 有 RAG 就没有幻觉。

错误：

> 模型给了 Citation 就说明 Grounded。

错误：

> 所有错误都是模型问题。

---

<details>
<summary>自测：为什么 Temperature=0 不能解决事实错误？</summary>

因为 Temperature 主要控制 Decoding 随机性。如果最高概率的续写本身就是错误事实，Greedy 仍会稳定地产生错误。

</details>
