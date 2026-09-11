# 14｜Planning、ReAct 与 Execute-Observe

## 1. Planning 不是必须先写十步计划

Agent 的计划粒度应该跟环境不确定性匹配。

```text
低不确定：plan several steps
高不确定：act one step → observe → replan
```

ReAct 的核心价值就是把 reasoning 与 action / observation 交替，让新证据能改变计划。

## 2. 三种常见控制方式

### Reactive

```text
observe → next action
```

适合探索性任务。

### Plan-and-execute

```text
plan → execute steps → revise if needed
```

适合可分解任务。

### State Graph / Workflow-assisted

把必须满足的业务 stage 固定下来，stage 内允许 agentic decision。

## 3. Plan 应是可变 State

不要把 Plan 当成一段不可修改的自然语言。可以维护：

```json
{
  "goal":"fix issue",
  "steps":[...],
  "current":2,
  "blocked":[],
  "evidence":[]
}
```

但也不要过度结构化到模型只能填表。

## 4. Planning 的 Failure

- 计划幻觉；
- 一开始过度规划；
- observation 来了仍死守旧计划；
- 花大量 Token 写计划却不执行；
- planning tool 与 task state 不一致。

## 🎯 面试

Planning 的目标不是让模型写更长的 TODO，而是帮助 Runtime 在复杂任务里管理目标和下一步。开放环境我更偏 ReAct/增量 replanning；确定业务阶段则用 workflow/state graph 固定约束，在局部让 Agent 自主。

<details><summary>自测：为什么“一次性生成完整计划再执行”在代码修复里容易失败？</summary>

因为读代码、跑测试后的 Observation 会改变问题理解，初始计划往往基于不完整环境信息。
</details>
