# 02. Agent vs Workflow：什么时候真的需要 Agent

`AGENT-001` 在冻结 HUMAN-A 中有 **30 个独立来源**，属于 Agent 模块最稳定的第一层追问之一。

面试官问这个问题，通常不是想听：

> “Agent 比 Workflow 更智能。”

而是想判断你有没有工程判断力：

> **什么任务应该交给模型动态决策，什么任务应该继续用确定性程序控制？**

---

# 1. 先讲人话：不是“用了 LLM”就叫 Agent

先看三个系统。

## 系统 A：固定流水线

```text
上传 PDF
→ OCR
→ 切 Chunk
→ Embedding
→ 写 Vector DB
```

每一步都由程序预先规定。

这更像：

> **Workflow / Pipeline。**

---

## 系统 B：固定流程里调用 LLM

```text
收到客服消息
→ LLM 分类
→ 根据分类进入固定 Branch
→ 模板化回复
```

虽然用了模型，但控制流仍然主要由程序定义。

它仍然更接近：

> **LLM-enhanced Workflow。**

---

## 系统 C：模型根据环境动态决定下一步

```text
用户：修复这个仓库的测试失败
        ↓
模型先读错误日志
        ↓
决定搜索某个 symbol
        ↓
读文件
        ↓
判断根因
        ↓
修改代码
        ↓
运行测试
        ↓
根据结果决定继续修还是结束
```

这里核心控制路径无法在运行前完全写死。

它更接近：

> **Agent。**

---

# 2. 一个实用判断：谁拥有“下一步决策权”

可以把 Workflow 和 Agent 的区别压缩成一句话：

> **Workflow 主要由开发者预先编码控制流；Agent 允许模型在运行时根据当前 Context / State / Observation 动态选择下一步 Action。**

这不是绝对二元，而是一条连续谱：

```text
完全确定性程序
    ↓
固定 Workflow + LLM 节点
    ↓
部分动态 Routing
    ↓
Agent Loop + Tool Use
    ↓
Long-running Autonomous Agent
```

💡 **新手理解**：

> “Agent 化”本质上是把一部分原来由工程师提前写死的控制逻辑，交给模型在运行时做决策。

而一旦把控制权交出去，就必须付出新的工程成本：

- 不确定性；
- Token / 延迟；
- 失败恢复；
- 安全边界；
- Evaluation；
- 可解释与 Trace。

所以 Agent 不是默认升级版，而是一种 Trade-off。

---

# 3. Workflow 的优势到底是什么

很多人一听 Agent 就觉得 Workflow “落后”。

其实对大量业务来说，Workflow 更好。

## 3.1 可预测

例如支付流程：

```text
创建订单
→ 冻结库存
→ 支付
→ 确认订单
→ 发货
```

你通常不希望模型自由决定：

```text
“我觉得这次可以跳过库存冻结。”
```

固定状态机更适合。

## 3.2 容易测试

确定性 Workflow 可以写清楚：

```text
Given state A
When event B
Then state C
```

而 Agent 需要做概率性 Evaluation。

## 3.3 成本低

普通代码分支：

```python
if risk_score > 0.8:
    require_review()
```

不需要每次消耗推理 Token。

## 3.4 安全边界清晰

可执行路径越固定，Blast Radius 越容易控制。

---

# 4. Agent 的价值在哪里

Agent 适合解决这些特征明显的任务。

## 4.1 步骤事先不完全确定

例如：

```text
“帮我定位线上这个性能问题。”
```

可能需要：

- 看日志；
- 看 Trace；
- 查 SQL；
- 看代码；
- 跑命令；
- 对比版本；

具体顺序取决于中间 Observation。

## 4.2 需要处理非结构化环境

例如大型代码仓库、文档、网页、用户自然语言需求。

## 4.3 需要动态选择 Tool

当 Runtime 暴露：

```text
search_code
read_file
run_test
query_db
search_ticket
create_issue
```

模型可以根据当前状态决定下一步用哪个能力。

## 4.4 任务需要多轮反馈闭环

```text
Action
→ Observation
→ Re-plan
→ Action
```

这就是 Agent Loop 的核心。

---

# 5. 判断一个任务是否值得 Agent 化

可以用六个问题快速判断。

| 问题 | 如果答案是“是” | 倾向 |
|---|---|---|
| 步骤能否稳定写成固定流程？ | 能 | Workflow |
| 中间结果是否会强烈影响下一步？ | 会 | Agent |
| 是否存在大量非结构化输入？ | 有 | Agent |
| 错误动作风险是否很高？ | 很高 | 更谨慎，偏 Workflow/HITL |
| 是否需要探索多个信息源/工具？ | 需要 | Agent |
| 是否有可验证的最终 Outcome？ | 有 | 更适合 Agent |

注意最后一点。

Agent 越自主，就越需要：

> **明确的完成条件与验证机制。**

否则你只是让模型“自由发挥”。

---

# 6. 一个反例：不该 Agent 化的简单 CRUD

需求：

```text
用户提交表单
→ 校验字段
→ 写数据库
→ 返回结果
```

没必要写：

```text
LLM 判断下一步是否应该校验字段
→ LLM 决定是否写数据库
→ Agent Tool 调 DB
```

这会引入：

- 更多延迟；
- 更多成本；
- 更多故障点；
- 更难测试；
- 更难保证正确性。

🎯 **面试里很加分的一句话**：

> 我不会因为能用 Agent 就 Agent 化。确定性强、规则稳定、风险高的主链路优先保留普通程序和 Workflow；Agent 更适合处理探索性、非结构化、步骤动态变化的部分。

---

# 7. 真实系统往往是 Hybrid，而不是纯 Agent

生产系统很少是：

```text
所有事情都交给 Agent
```

更常见的是：

```text
Deterministic Workflow
        │
        ├─ 固定鉴权
        ├─ 固定数据校验
        ├─ 固定支付 / 事务
        │
        └─ Agentic Step
             │
             ├─ 理解目标
             ├─ 搜索
             ├─ Tool Use
             └─ 生成建议
```

例如客服系统：

```text
登录 / 权限 → Workflow
订单读取     → Tool + Backend
问题诊断     → Agent
退款高风险动作 → Approval + Deterministic Transaction
```

这比“全链路自由 Agent”更可靠。

---

# 8. Agent 化意味着引入哪些新问题

假设把一个固定 Workflow 改成 Agent：

```text
before:
step1 -> step2 -> step3

now:
model -> choose action -> observe -> choose next action
```

你立刻需要回答：

```text
模型选错 Tool 怎么办？
Tool 参数错怎么办？
一直循环怎么办？
Context 爆了怎么办？
中途崩溃怎么办？
执行高风险动作怎么办？
怎样证明 Agent 完成任务？
```

所以：

> **Agent 的价值来自动态决策；Agent 的工程成本也正来自动态决策。**

---

# 9. 一个简单的 Hybrid Router

不要一上来就让 LLM 决定所有请求。

可以先用确定性规则做第一层：

```python
from enum import Enum


class Route(str, Enum):
    FAQ = "faq"
    REFUND = "refund"
    INVESTIGATION = "investigation"


def route_request(text: str) -> Route:
    if "退款" in text:
        return Route.REFUND

    if text.startswith("什么是"):
        return Route.FAQ

    return Route.INVESTIGATION
```

然后：

```text
FAQ
→ RAG / one-shot LLM

Refund
→ deterministic workflow + approval

Investigation
→ Agent loop
```

这里体现一个重要设计原则：

> **Agent 是系统中的一种执行模式，不一定是系统的全部。**

---

# 10. Anthropic 对 Workflow / Agent 的区分

Anthropic 的 `Building effective agents` 明确强调：

- Workflow：LLM 和 Tool 按预定义代码路径编排；
- Agent：LLM 动态决定 process 和 tool usage。

更重要的是，它建议从简单模式开始，只有当任务确实需要时再提高 autonomy。

这和工程实践非常一致：

```text
能用一个 Call 解决
→ 不要先上 Agent

能用固定 Workflow 解决
→ 不要先上开放 Loop

真正需要动态探索
→ 再引入 Agent
```

官方来源：

https://www.anthropic.com/engineering/building-effective-agents

---

# 11. OpenAI 的 Agent 判断也强调“独立完成任务”

OpenAI 的 `A practical guide to building agents` 把 Agent 定义为能代表用户较独立地完成任务的系统，并把 Model、Tools、Instructions/Orchestration、Guardrails 放在同一个工程视角里。

这也说明：

> Agent 不是“聊天机器人换了个名字”，而是执行权和环境交互能力提升后的系统形态。

来源：

https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/

---

# 12. Agent 不等于 ReAct

ReAct 是经典的 Reason / Act / Observe 交替范式：

```text
Reason
→ Action
→ Observation
→ Reason
→ ...
```

它非常适合帮助理解 Agent Loop。

但：

```text
Agent ≠ ReAct
```

实际系统还可能用：

- Plan → Execute；
- Planner / Executor；
- Router；
- Critic / Verifier；
- State Graph；
- Multi-Agent。

范式选择会在第 14 章展开。

ReAct 原始论文：

https://arxiv.org/abs/2210.03629

---

# 13. Claude Code / Codex 为什么属于强 Agent Runtime 参考

Claude Code 的固定源码快照里，`QueryEngine` 会跨 Turn 保存 Conversation State，并管理 Tools、Agents、MCP、Permission、Budget、Abort。

Codex 固定源码中也有：

- Session / Turn / Step；
- Tool Router；
- Sandbox；
- Compaction；
- Trace。

这类系统之所以复杂，不是因为它们“用了更长 Prompt”，而是因为它们承担：

> **动态执行、多步环境交互、长任务状态和安全控制。**

这正是 Agent 与简单 Workflow 的工程分水岭。

---

# 14. 三个典型场景判断

## 场景 A：批量把 CSV 导入 MySQL

步骤明确：

```text
parse
→ validate
→ batch insert
→ report
```

优先：Workflow。

Agent 没必要。

---

## 场景 B：分析一个未知线上故障

需要：

```text
查日志
→ 根据错误再查 Trace
→ 决定看代码还是 DB
→ 运行诊断 Tool
→ 根据结果继续
```

优先：Agent 或 Agent-assisted Investigation。

---

## 场景 C：自动删除用户数据

任务可能简单，但副作用高。

优先：

```text
Deterministic Workflow
+ Strong Auth
+ Human Approval
+ Audit
```

而不是让开放 Agent 自由执行。

---

# 15. 一个更完整的判断矩阵

| 维度 | Workflow 更适合 | Agent 更适合 |
|---|---|---|
| 控制流 | 稳定、已知 | 运行时动态 |
| 输入 | 结构化 | 非结构化 / 开放 |
| Tool 选择 | 固定 | 动态 |
| 任务长度 | 短 / 中 | 多步 / 长 |
| 错误成本 | 高且不可容忍 | 可隔离 / 可验证 |
| 可测试性 | 状态机/单测 | Eval + Outcome |
| 延迟成本 | 敏感 | 可接受额外推理 |
| 安全 | 路径容易封闭 | 需要 Permission/Sandbox |
| 典型场景 | 交易、ETL、CRUD | 研究、Coding、调查、复杂助手 |

---

# 16. 面试官最爱追的一个问题：Agent 是否越自主越好？

不是。

Autonomy 增加会带来：

```text
Exploration Ability ↑
Flexibility ↑

同时：
Uncertainty ↑
Cost ↑
Latency ↑
Security Risk ↑
Evaluation Difficulty ↑
```

因此成熟设计通常不是追求最大自主，而是：

> **在完成任务所需的最小范围内给予模型足够自主权。**

这叫做“有边界的 autonomy”。

---

# 17. 常见失败模式

## 17.1 把能写 if/else 的地方交给 LLM

结果：

- 慢；
- 贵；
- 不稳定。

## 17.2 没有 Stop Condition

Agent：

```text
search
→ read
→ search
→ read
→ ...
```

一直循环。

## 17.3 没有 Outcome Verification

Agent 自己说 Done 就结束。

## 17.4 高风险动作也完全自主

没有 Approval / Sandbox。

## 17.5 Framework-first

先选 LangGraph，再强行把简单需求建成图。

这些都属于“为了 Agent 而 Agent”。

---

# 18. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Workflow 的控制流主要由开发者预先定义，Agent 则允许模型根据当前 Context、State 和 Tool Observation 动态决定下一步。Agent 适合步骤不确定、需要探索、需要动态 Tool 选择的任务；规则稳定、风险高、流程确定的业务更适合普通程序或 Workflow。生产系统通常是 Hybrid，而不是所有东西都 Agent 化。

## Level 2｜2–3 分钟

可以再补：

> 我判断是否 Agent 化会看五点：控制流能不能写死、输入是否非结构化、中间 Observation 是否改变后续步骤、动作风险是否可控、最终结果是否可验证。如果只是 CRUD、支付、ETL，我会保留 deterministic workflow；如果是 Coding、Research、故障排查这种需要边执行边观察边改计划的任务，Agent 更有价值。Agent 化之后还必须补 Loop Guard、Permission、Checkpoint、Trace 和 Evaluation。

## Level 3｜继续追问

🔍 **Workflow 里用了 LLM 算不算 Agent？**  
不一定。判断重点不是“有没有 LLM”，而是谁拥有运行时控制流。

🔍 **怎么避免 Agent 过度自主？**  
缩小 Tool Set、限制 Permission、设置 Approval、明确 Stop/Budget、Sandbox、Outcome Verification。

🔍 **什么时候从 Agent 降级回 Workflow？**  
当真实路径高度稳定、Eval 表明模型动态决策没有明显收益、成本/风险超过收益时。

---

# 19. HUMAN-A 真实信号

`AGENT-001`：

> Agent 与普通 LLM Call / Chatbot / 固定 Workflow 的本质区别是什么？什么任务真正值得 Agent 化？

- Source Count：**30**
- Depth：L3

Verified Follow-up Chain 中多次出现：

```text
为什么需要 Agent
→ Harness / Runtime
→ Loop
→ Tool / Context / Memory
→ Failure / Evaluation
```

所以这不是“概念八股”，而是后续整条 Runtime 追问链的入口。

---

# 20. 自测

<details><summary>1. 一个固定 DAG 中有三个 LLM 节点，它一定是 Agent 吗？</summary>

不一定。如果控制路径主要由开发者预定义，模型只是执行节点，它更接近 LLM-enhanced Workflow。是否 Agent 化主要看模型是否拥有运行时选择下一步行动/工具/路径的控制权。
</details>

<details><summary>2. 为什么支付主链路通常不应该完全 Agent 化？</summary>

支付流程规则稳定、错误成本高、事务和审计要求强，确定性状态机更容易验证和约束。可以把 Agent 用在辅助理解、客服诊断等外围，但关键副作用主链路通常应该由确定性程序、权限和审批控制。
</details>

<details><summary>3. 什么任务特别适合 Agent？</summary>

步骤事先无法完全确定、需要根据中间 Observation 动态调整、涉及多个工具和非结构化环境、且最终结果可以被验证的任务，例如 Coding Agent、Research Agent、故障调查助手。
</details>

<details><summary>4. 为什么 Agent 的最终 Outcome 必须可验证？</summary>

因为模型自述“完成”并不可靠。自主程度越高，越要依赖外部 Test、Artifact、Environment State、Metric 或 Grader 判断任务是否真的完成。
</details>
