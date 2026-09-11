# 10｜Tool Executor 与 Result 回填

## 1. 一次 Tool Call 的完整路径

```text
Model Tool Call
→ Parse
→ Validate
→ Resolve Tool
→ Permission / Approval
→ Acquire Environment
→ Execute
→ Normalize Result
→ Persist Event
→ Project Observation into Context
```

缺少任何一步，Demo 都可能工作，但恢复/审计会出问题。

## 2. Executor 为什么独立

Tool definition 描述能力；Executor 负责运行环境。

同一个 logical tool 可以有：

```text
local executor
remote executor
sandbox executor
mock executor (eval)
```

这使测试和 Production policy 更清晰。

## 3. Result 有两份视图

真实执行结果可能很大：

```text
Raw Result → durable artifact / trace
          ↘ summary/reference → model context
```

模型不需要看到全部 50MB log，但 Runtime 应保留足够证据用于 debug。

## 4. Call ID 贯穿生命周期

```text
tool_call_requested(call_id)
tool_started(call_id)
tool_progress(call_id)
tool_completed(call_id)
```

这是 streaming UI、retry、approval 与 replay 的基础。

## 5. 结果回填位置

Tool Result 应与对应 Call 成对，避免在复杂 Multi-Agent / 并发下把 Observation 注入错误 Turn。

## 🎯 面试

Tool Executor 是模型意图和真实环境之间的执行层。我会让 call_id 贯穿 validate、approve、execute、result 和 trace；raw result 可持久化，但只把经过裁剪或结构化的 observation 回填 Context。

<details><summary>自测：为什么 raw result 和 model-visible result 要分开？</summary>

因为模型上下文有限且可能包含敏感信息；但 Debug / Replay 又需要保留真实执行证据。
</details>
