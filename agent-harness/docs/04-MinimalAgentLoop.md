# 04｜Minimal Agent Loop

## 1. 最小循环

理解 Agent 最重要的代码不是框架 API，而是这十几行：

```python
state = init_state(goal)
while True:
    context = build_context(state)
    output = model(context)

    if output.type == "final":
        return output.value

    call = validate_tool_call(output)
    result = execute_tool(call)
    state = append_observation(state, call, result)
```

这已经包含核心闭环：

```text
Reason / Decide
→ Act
→ Observe
→ Update
→ Repeat
```

ReAct 原始工作就是把 reasoning 与 action / observation 交替组织起来。

## 2. Production Loop 多了什么

真实 Runtime 会继续加：

```text
budget
permission
sandbox
retry
timeout
cancellation
checkpoint
compaction
trace
human approval
```

所以生产 Loop 更像一个状态机，而不是 `while True`。

## 3. Observation 为什么关键

Tool Result 不是“调用完成即可”。模型必须看到可理解的 Observation，才能改变下一步。

例如：

```text
ReadFile → file not found
```

好的 Loop 会把失败作为结构化 observation，让模型决定 search path / inspect repo；坏的 Loop 可能直接抛异常结束。

## 4. Stop 不是模型一句 done

最终停止通常综合：

- final answer / artifact；
- explicit stop；
- max turn；
- budget exhausted；
- unrecoverable failure；
- cancellation；
- human rejection。

后面会单独讲 Loop Guard。

## 🎯 面试

Agent Loop 的本质是 Model Decision → Runtime Action → Environment Observation → State Update 的反馈闭环。Tool Calling 只是 Act 的一种形式；生产系统还需要预算、权限、取消、恢复、上下文管理和可观测性来约束这个循环。

<details><summary>自测：为什么普通 Function Calling 不自动等于 Agent Loop？</summary>

因为一次 Function Call 可以是单步请求。Agent Loop 要把 Tool Result 重新转化为下一轮 Observation，并允许模型基于新状态继续决策直到停止。
</details>
