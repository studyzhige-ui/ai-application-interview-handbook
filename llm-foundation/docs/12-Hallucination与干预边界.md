# 12｜Hallucination、Factuality 与 Prompt / RAG / Fine-tuning 的干预边界

“模型答错了怎么办？”不能直接跳到 Fine-tuning。

一个成熟的应用工程判断应该先区分错误来源：

```text
Instruction 不清楚？
Knowledge 不存在/过期？
Retrieved Evidence 错？
模型即使看到证据仍推错？
输出格式不稳定？
领域行为/风格不符合？
```

然后才决定使用：

```text
Prompt
RAG
Tool / Verification
Fine-tuning
Model Change
```

所以 Hallucination 与“什么时候换手段”应该在同一个知识块里学习。

---

## 1. Hallucination 是什么

应用工程里可以把它宽泛理解为：

> **模型生成了缺乏可靠依据、与事实/给定证据冲突，或不应该自信断言的内容。**

它不等于：

```text
所有回答错误
```

错误还可能来自：

- Retrieval；
- Parser；
- Tool；
- Business Logic；
- Stale Data；
- Permission；
- Prompt Ambiguity。

所以第一步是 Attribution。

---

## 2. 模型为什么会“编”

LLM 的基本目标是：

```text
predict plausible next token
```

它不是内建的数据库查询器或事实验证器。

因此即使模型在训练中见过某个事实，也不意味着：

- 总能精确召回；
- 知道事实是否过期；
- 知道当前组织内部数据；
- 会在不确定时自动拒答。

这就是为什么 Application Layer 需要 Grounding 和 Verification。

---

## 3. Factuality 和 Fluency 不一样

一段回答可以：

```text
语言流畅
结构完整
逻辑听起来合理
```

但事实仍然错。

这正是 LLM 应用危险之处：

> **错误往往是“高可读性的错误”。**

所以不能把语言质量当作事实质量的代理指标。

---

## 4. Prompt 能解决什么

Prompt 适合解决：

- Task Definition；
- Role / Style；
- Output Format；
- Constraints；
- Few-shot Examples；
- Reasoning Procedure 提示；
- 明确“证据不足时拒答”。

如果问题只是：

```text
模型不知道输出 JSON
```

或：

```text
任务说明含糊
```

通常先修 Prompt / Schema，而不是训练模型。

---

## 5. Prompt 不能稳定补充模型没有的动态知识

如果问题是：

```text
公司最新政策是什么？
今天库存多少？
用户当前订单状态？
```

这些知识：

- 动态；
- 私有；
- 频繁变化；

不能靠 Fine-tuning 或 Prompt 永久“记进去”。

更自然的是：

```text
RAG / Database / Tool
```

把当前事实提供给模型。

---

## 6. RAG 主要解决什么

RAG 适合：

```text
需要外部知识
知识不断更新
需要 Citation
需要 Permission / Tenant
知识量远大于 Context Window
```

它做的是：

```text
Query
→ Retrieve evidence
→ Put evidence into context
→ Generate grounded answer
```

所以 RAG 主要改变：

> **模型当前能看到什么证据。**

它不会改变模型参数本身。

---

## 7. Fine-tuning 主要解决什么

Fine-tuning 更适合改变：

- 行为模式；
- 输出风格；
- 特定任务能力；
- 格式遵循；
- 领域语言习惯；
- 某类决策边界。

它不适合把大量频繁变化事实当数据库灌进去。

可以记住：

```text
RAG → Knowledge at inference time
Fine-tuning → Behavior / capability in model parameters
```

这是非常重要的边界。

---

## 8. Tool / Verification 什么时候更合适

如果任务需要精确操作或外部事实：

```text
算税
查数据库
下订单
读取当前天气
验证代码测试
```

比起让模型“凭语言推理猜答案”，更可靠的是：

```text
LLM decides
→ Tool executes deterministic operation
→ Model explains result
```

所以“降低 Hallucination”不只是 RAG，还包括把可验证步骤移出模型自由生成。

---

## 9. 一个错误归因决策树

```text
Answer Wrong
│
├─ Instruction misunderstood?
│  └─ Prompt / Examples / Schema
│
├─ Missing current/private knowledge?
│  └─ RAG / Tool / DB
│
├─ Evidence retrieved wrong?
│  └─ RAG Pipeline Debug
│
├─ Correct evidence present but model ignored/misreasoned?
│  ├─ Better Model
│  ├─ Context Construction
│  ├─ Prompt
│  └─ Verification
│
├─ Repeated behavior/style/task pattern wrong?
│  └─ Fine-tuning / SFT / Preference Optimization
│
└─ Output requires deterministic side effect?
   └─ Tool / Business Logic
```

这比一句“换大模型”更有工程价值。

---

## 10. Grounding 怎么降低风险

Grounding 的目标是：

```text
Answer Claims
↔
Explicit Evidence
```

常见做法：

- 给可信 Context；
- 指示只基于 Context 回答；
- 要求 Citation；
- Evidence 不足时拒答；
- 生成后 Verification；
- Claims-to-source 检查。

但 Prompt 说“不要 hallucinate”本身没有可靠保证。

---

## 11. 为什么 Citation 也可能是假的

如果 Citation 只是让模型自由生成：

```text
[1] [2] [3]
```

模型可能引用不存在或不支持 Claim 的 Source。

更可靠的系统应该：

```text
retrieval result has stable source ID
→ context keeps provenance
→ answer references those IDs
→ application validates cited source exists
```

完整设计属于 RAG。

---

## 12. “不知道就说不知道”为什么仍需要 Eval

Prompt 加一句：

```text
If unsure, say I don't know
```

可能改善行为，但不能证明：

```text
什么时候真的会拒答
什么时候错误自信
什么时候过度拒答
```

需要专门测试：

```text
answerable queries
unanswerable queries
adversarial queries
conflicting evidence
```

然后比较：

```text
False Answer Rate
Refusal Precision / Recall
```

---

## 13. Fine-tuning 为什么不能自动修复事实性

训练数据本身如果：

- 过期；
- 错误；
- 覆盖不足；

Fine-tuning 可能把错误模式固化进参数。

而动态事实仍会继续变化。

所以“知识过期”通常优先考虑 Retrieval / Tool，而不是频繁重新训练。

---

## 14. Model Change 什么时候有意义

如果在同样 Prompt / Evidence 下：

```text
Model A consistently fails reasoning / tool use
Model B consistently succeeds
```

说明问题可能是基础模型能力上限。

这时换模型可能比无限 Prompt Engineering 更有效。

但必须通过 Eval 证明，而不是凭模型名大小判断。

---

## 15. 一个实际改进顺序

很多团队可以采用：

```text
1. Define Eval
2. Fix Prompt / Output Contract
3. Add Retrieval / Tools if knowledge missing
4. Improve Context / Verification
5. Compare stronger/different models
6. Fine-tune if repeated behavior gap remains
```

Fine-tuning 通常不是第一步，因为它：

- 数据准备成本高；
- 训练和部署复杂；
- 容易过拟合；
- 迭代周期比 Prompt/RAG 长。

---

## 16. 常见错误

- Hallucination = 所有回答错误：过于宽泛。
- Temperature 调低就没有 Hallucination：错误。
- RAG 一定能消除 Hallucination：错误，Retrieval 和 Generation 都可能失败。
- Fine-tuning 最适合记最新知识：通常不是。
- Prompt Engineering 永远能弥补基础模型能力不足：错误。
- Citation 出现就说明答案 Grounded：必须验证 Citation 真支持 Claim。

---

## 17. 面试怎么答

### Q：怎么降低大模型 Hallucination？

> 我会先做错误归因，而不是只调 Temperature。动态/私有知识缺失用 RAG 或 Tool；检索错误先修 Retrieval；已有正确证据但模型不遵循则优化 Context/Prompt、使用更强模型或做 Verification；高风险事实还应要求 Citation、拒答策略和 deterministic checks。Fine-tuning 更适合长期行为/任务能力适配，不是动态知识库替代品。

### Q：Prompt、RAG、Fine-tuning 怎么选？

> Prompt 优先解决任务说明、格式、约束和示例；RAG/Tool 解决推理时需要的外部、动态、私有事实；Fine-tuning 用于稳定改变模型行为、风格或特定任务能力。先定义 Eval，再选择最小有效干预。

---

## 18. 自测

<details><summary>1. 公司政策每天变化，应该优先 RAG 还是 Fine-tuning？</summary>
RAG/Tool，因为这是动态外部事实，不适合反复写入模型参数。
</details>

<details><summary>2. 为什么“答案带 Citation”仍不能证明 Grounded？</summary>
模型可能生成错误引用，必须验证 Citation 对应真实检索来源且真正支持 Claim。
</details>

<details><summary>3. Fine-tuning 更适合改变 Knowledge 还是 Behavior？</summary>
在应用工程语境下更常用来稳定改变行为、风格和任务能力；动态知识更适合 Retrieval/Tool。
</details>
