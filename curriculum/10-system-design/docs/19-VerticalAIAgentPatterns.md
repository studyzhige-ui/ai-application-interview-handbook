# 19｜Vertical AI Agent Patterns：Analysis、Customer Service、Multimodal、Game、Content

最后一章不是给五种业务各背一套架构，而是训练：

> **怎样把同一套 Agent / RAG / Tool / State / Eval 原语映射到不同垂直业务，并识别每个业务真正的高风险约束。**

对应真人 Scenario：

```text
SD-018 Financial / Data Analysis Agent
SD-019 AI Customer Service Agent
SD-020 Multimodal Document / PDF → HTML Agent
SD-023 Game / Interactive Agent
SD-024 Content Creation / Video Editing Agent
```

---

## 1. 垂直 Agent 的共同框架

任何业务都先问：

```text
Goal 是什么？
Authoritative Data 在哪？
哪些能力是 Tool？
哪些知识是 RAG？
哪些状态必须持久化？
哪些动作有副作用？
什么时候必须 Human Handoff？
怎样验证结果？
```

共同骨架：

```text
User Goal
→ Intent / Plan
→ Retrieve / Observe
→ Tool / Action
→ Verify
→ Update State
→ Stop / Handoff
```

真正差异来自 Domain Invariant。

---

# 2. Financial / Data Analysis Agent

问题：

```text
用户问：为什么 Q3 毛利率下降？
```

Agent 可能需要：

```text
理解指标
→ 找财报 / SQL / Spreadsheet
→ 计算
→ 交叉验证
→ 给结论 + Citation
```

它不是纯 RAG。

---

# 3. Analysis Agent 的 Source of Truth

要区分：

```text
Narrative Knowledge
→ report / policy / note

Numeric Fact
→ database / spreadsheet / calculation
```

如果问题是：

> “2026 Q3 revenue 是多少？”

优先查结构化 Source，而不是让 LLM 从旧文档记忆回答。

---

# 4. Analysis Agent 的 Verification

每个结论最好能追：

```text
Claim
→ Formula / Query
→ Source Rows / Evidence
→ Version / Timestamp
```

对于计算：

```text
LLM proposes formula
→ deterministic code executes
→ result checked
```

不要让模型“心算”关键财务结果。

---

# 5. Customer Service Agent

共同流程：

```text
User Message
→ Intent
→ FAQ / RAG
→ Order / Account Tool
→ Response
→ Handoff if needed
```

但真正难点是：

```text
knowledge answer
vs
live business fact
vs
high-risk action
```

三者必须分层。

---

# 6. Customer Service 的 Tool Boundary

例如：

```text
“退款规则是什么？”
→ RAG

“我的订单状态？”
→ Order Tool

“帮我退款 3000 元”
→ high-risk Tool + approval / policy
```

不能让 RAG 文档直接决定实时订单事实，也不能让 LLM 自己凭文本完成退款。

---

# 7. Human Handoff

需要明确条件：

```text
low confidence
policy conflict
customer angry / escalation
high value refund
identity uncertain
repeated failure
```

Handoff 时不要只发最后一句聊天，要带：

```text
summary
evidence
tool results
action history
risk flags
```

让人工不用从头阅读全部历史。

---

# 8. Multimodal Document / PDF → HTML Agent

目标可能：

```text
PDF
→ text / table / image / layout
→ structured HTML
→ verify citations / assets
```

这里关键不是让一个 Multimodal Model 一次输出整页。

更稳：

```text
Parse / OCR / Layout
→ Asset Extraction
→ Semantic Structure
→ Generate HTML
→ Render
→ Visual / Structural Verify
```

---

# 9. Multimodal 的可追溯性

HTML 中一个表格 / 图片最好能追到：

```text
source page
bounding box / element id
asset file
extracted text
```

否则模型改错数字或图像引用时无法定位。

这也是 RAG Lineage 在生成工作流中的延伸。

---

# 10. Game / Interactive Agent

Game Agent 的状态通常比普通 Chat 更结构化：

```text
world state
player state
goal
inventory
allowed actions
history
```

模型不是自由写文本，而是：

```text
observe state
→ choose valid action
→ environment executes
→ new state
```

很接近 Agent Runtime + Environment Loop。

---

# 11. Game Agent 的 Safety / Validity

Action 必须经过：

```text
schema validation
permission / rule check
environment constraint
```

模型说：

> “我穿墙到坐标 X。”

不代表 Environment 应执行。

游戏规则才是 Source of Truth。

---

# 12. Game Agent Evaluation

不能只看自然语言“像不像人”。

可以看：

```text
goal completion
invalid action rate
resource efficiency
step count
stuck / loop rate
safety violation
```

如果是 NPC 还可能加：

```text
persona consistency
user engagement
```

---

# 13. Content Creation / Video Editing Agent

长内容工作流常：

```text
Brief
→ Plan / Storyboard
→ Asset Search / Generate
→ Scene / Shot Tasks
→ Compose
→ Review
→ Revise
→ Export
```

适合分阶段 State Machine，而不是一个 Prompt 生成全部。

---

# 14. SubAgent 怎样拆

可以按职责：

```text
Planner
Researcher
Script Writer
Asset Agent
Editor
Reviewer
```

但不要为了“多 Agent”而多 Agent。

真正拆分依据：

```text
Context Isolation
Tool / Permission Difference
Parallelism
Independent Verification
```

否则只增加通信和状态复杂度。

---

# 15. 人物 / 素材一致性

视频生成常遇到：

```text
character identity drift
style drift
asset version drift
```

需要持久化：

```text
character spec
reference assets
style guide
scene state
approved asset version
```

不能只靠每轮 Prompt 重新描述。

---

# 16. Long-running Content Workflow

一个视频任务可能几小时。

因此复用：

```text
Durable Run
Checkpoint
Artifact Store
Per-step Retry
Cancellation
Approval
Cost Budget
```

昂贵 Generation Step 还应缓存 / 版本化 Artifact，避免 Resume 后全部重跑。

---

# 17. 统一的 Vertical Agent Decision Table

| 业务 | Authoritative State | 高风险动作 | 关键验证 |
|---|---|---|---|
| Analysis | DB / report | financial conclusion | query/formula/citation |
| Customer Service | order/account system | refund/write action | policy + auth + tool result |
| Multimodal Doc | original document | publish transformed content | layout/data/asset trace |
| Game | game environment | state-changing action | action validity + goal |
| Content | project/asset store | publish/export | artifact consistency + review |

---

# 18. Vertical Agent 最重要的设计原则

> **LLM 是决策/生成组件，不是业务事实、权限和环境规则的最终拥有者。**

真实系统仍需要：

```text
Source of Truth
Validation
Tool Boundary
State Machine
Verification
Human Handoff
```

---

# 19. 真人面经影响

这些 Scenario 的独立来源不如 Production Agent Backend 高频，但它们证明面试已经从“解释 Agent”走向：

```text
把 Agent 映射到真实业务
→ 识别 Domain Constraint
→ 设计 Tool / State / Verification
```

因此教材把它们合成一个迁移能力章节，而不是五篇互相重复的模板。

---

# 20. 🎯 面试怎么答陌生 Vertical Agent

> 我会先把业务拆成 Goal、Authoritative State、Read/Retrieve、Action Tool、Durable State、High-risk Side Effect 和 Verification。LLM 主要负责理解、规划和生成，但实时事实由业务 Tool/DB 提供，业务规则和权限由确定性系统校验。长任务用 Durable Run/Checkpoint，结果需要 Domain-specific Evaluation；高风险或低置信场景进入 Human Handoff。这样即使业务换成金融、客服、游戏或视频，设计方法仍然可复用。

---

# 21. 本章自测

<details><summary>1. 为什么 Analysis Agent 不应该让 LLM 直接算关键财务数字？</summary>
关键计算应该由确定性代码/查询执行并保留公式和数据来源，LLM 更适合规划和解释。
</details>

<details><summary>2. 为什么 Customer Service 的退款规则和订单状态不能都只用 RAG？</summary>
规则文档适合 RAG，但实时订单状态属于业务 Source of Truth，需要实时 Tool/DB；退款还是高风险写操作，需要权限和审批。
</details>

<details><summary>3. 多 Agent 什么时候才值得拆？</summary>
当子任务需要独立 Context、不同 Tool/Permission、可并行执行或独立 Verification 时；否则多 Agent 可能只增加协调成本。
</details>
