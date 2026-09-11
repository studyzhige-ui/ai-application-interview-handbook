# 02｜Agent vs Workflow：什么时候真的需要 Agent

## 💡 先讲人话

如果步骤提前就知道，不要因为“Agent 很火”把确定流程交给模型临场决定。

```text
Workflow：人预先决定路径
Agent：模型根据 Observation 动态决定下一步
```

## 1. 三层自动化

### 单次 LLM

```text
input → model → output
```

### Workflow

```text
A → B → if condition → C / D
```

路径由程序定义。

### Agent

```text
Goal
 ↓
Model decides action
 ↓
Environment observation
 ↓
Model revises next action
 ↓
...
```

路径依赖执行中的新信息。

## 2. 什么时候 Agent 更合适

- 下一步无法提前枚举；
- 需要探索环境；
- Tool selection 依赖中间结果；
- 任务有开放结束条件；
- 错误发生后需要重新规划。

例如“修复未知 GitHub Issue”通常比“每天 9 点导出报表”更适合 Agent。

## 3. 判断公式

不要用“步骤多不多”判断，而要问：

```text
路径是否确定？
中间 Observation 是否改变后续路径？
失败是否需要重新决策？
模型自主性的价值是否高于成本和风险？
```

## 4. 权威资料映射

Anthropic《Building effective agents》强调简单可组合 pattern，区分预定义 workflow 与动态 agent；OpenAI practical guide 也把 Agent 定位为能较独立完成多步任务的系统。

## ⚠️ 易错点

- “有 Tool Calling 就是 Agent”：不一定；固定调用链仍可以是 workflow。
- “Agent 一定比 Workflow 高级”：错误。确定流程通常 workflow 更便宜、更可测、更安全。
- “Multi-Agent 比 Agent 更高级”：不是层级升级，只是特定任务的并行 / 分工设计。

## 🎯 面试怎么答

我会先看路径的不确定性。固定业务规则优先 workflow；只有当任务需要根据环境反馈动态选 Tool、调整计划、决定是否继续时才引入 Agent，因为 Agent 同时引入更高延迟、成本、评测和安全复杂度。

<details><summary>自测：RAG Pipeline 是 Agent 吗？</summary>

固定 Parse → Retrieve → Rerank → Generate 通常是 Workflow；如果模型根据 Evidence 决定是否改写 Query、继续检索、换工具或停止，才进入 Agentic control loop。
</details>
