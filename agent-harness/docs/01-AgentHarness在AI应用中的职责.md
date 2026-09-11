# 01｜Agent Harness 在 AI 应用中的职责

## 💡 先讲人话

LLM 只负责“想”。Agent 产品还需要一套系统负责：给它什么信息、允许它做什么、工具执行后发生什么、什么时候继续、什么时候停、失败后怎么恢复。这套围绕模型的执行系统就是 Harness / Runtime。

```text
Model = decision engine
Harness = execution system around the model
```

## 1. 从普通 LLM Call 看起

最简单调用：

```python
answer = model.generate(prompt)
```

它没有：工具、副作用、长任务、恢复、权限、状态机。

Agent 则更像：

```python
while not done:
    context = runtime.build_context(state)
    decision = model(context)
    event = runtime.apply(decision)
    state = runtime.reduce(state, event)
```

真正难的通常不是 `model(context)`，而是 `build_context / apply / reduce / recover`。

## 2. Harness 的七类责任

```text
Control     Loop / Stop / Routing
Context     Assembly / Budget / Compaction
Capability  Tool / MCP / Skill
State       Session / Memory / Checkpoint
Execution   Sandbox / Task / Cancellation
Safety      Permission / Approval / Guardrail
Evidence    Trace / Replay / Eval
```

## 3. 为什么不能全塞进 Prompt

Prompt 无法真正提供：

- 文件系统隔离；
- API 权限；
- Tool schema validation；
- durable checkpoint；
- kill 正在运行的 process；
- side-effect dedup；
- trace / replay。

这些必须由软件 Runtime 保证。

## 4. 源码对应

Claude Code 固定快照中的 `QueryEngine.ts` 明确把 conversation lifecycle、跨 turn messages / cache / usage、tools、agents、MCP、permission callback、abort controller 和 budget 组织在一个 Runtime 对象中。

Codex 则把 Session / Turn / Step、Tool、Sandbox、Compaction、Event / Trace 等拆成多个模块。这两种组织方式不同，但都说明 Agent 产品远大于“一次模型调用”。

## ⚠️ 易错点

> “Agent = LLM + Tools”

太粗。Tools 只是 Capability Plane。没有 State、Context、Permission、Recovery、Trace，最多只是一个能 Function Call 的聊天程序。

## 🎯 面试 30 秒

Agent Harness 是模型外层的执行 Runtime。它负责 Agent Loop、Context、Tool 调度、State / Memory、Permission / Sandbox、Checkpoint / Resume、Cancellation、Trace / Eval 等。模型负责产生下一步决策，Harness 把这个决策变成可控、可恢复、可审计的真实执行。

<details><summary>自测：为什么 Permission 不能只写在 System Prompt？</summary>

因为 Prompt 只能影响模型行为，不能形成强制执行边界。真正的权限需要 Runtime 在执行 Tool 前校验，并由 Sandbox / Credential scope 限制即使模型做错也不能越界。
</details>
