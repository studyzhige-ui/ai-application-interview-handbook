# 15｜Stop Condition、Loop Guard 与 Budget

## 1. Agent 为什么会死循环

典型：

```text
Tool fails
→ model repeats same call
→ same failure
→ repeat
```

或者反复 search / reread 同一文件。

## 2. Stop Condition

正常停止：

- task outcome verified；
- model final output 且满足 contract；
- external workflow terminal state。

异常停止：

- max turns；
- time deadline；
- token/cost budget；
- repeated failure；
- permission denied；
- user cancellation。

Claude Code QueryEngine 配置直接存在 maxTurns / maxBudgetUsd，这说明预算是 Runtime concern。

## 3. Loop Guard

可追踪 signature：

```text
(tool, normalized args, error code)
```

若重复 N 次：

```text
force replan
→ ask user
→ terminate
```

也可检测 state 没有进展：文件 hash、test result、task state 都没变化。

## 4. Budget 不只有 Token

```text
model tokens
dollar cost
wall-clock time
tool calls
external API quota
sandbox CPU
```

不同任务价值不同，预算也应不同。

## 🎯 面试

Agent 必须有可观测 Stop Condition 和 Loop Guard。我会同时设 turn/time/cost/tool-call budget，并检测重复 action 或无进展状态；达到阈值后 replan、请求人工或终止，而不是无限让模型自己判断“下一次也许会成功”。

<details><summary>自测：为什么 max_turns 不是完整 Loop Guard？</summary>

它只能最终止损，不能识别第 3 轮已经明显重复的坏循环，也不能判断外部资源预算。
</details>
