# 05｜Run / Turn / Step 与状态机

## 1. 先统一名词

不同产品命名不同，但课程采用稳定分层：

```text
Run / Session
└─ Turn
   ├─ Step: model inference
   ├─ Step: tool execution
   └─ Step: state transition
```

- **Run/Session**：一次可持续很久、可暂停恢复的任务上下文。
- **Turn**：一次用户输入或一次逻辑交互周期。
- **Step**：Turn 内最小可观察执行动作。

Codex 源码显式存在 `Session / TurnContext / StepContext`，说明这不是纯教学造词。

## 2. 为什么分层

如果只有一个 `messages[]`：

- 不知道失败属于哪一轮；
- 无法对单个 Tool Step retry；
- 不知道 Checkpoint 放在哪；
- Trace 无法聚合；
- Cancellation 范围不清楚。

## 3. Run State Machine

```text
CREATED
  ↓
RUNNING ↔ WAITING_APPROVAL
  ↓  ↘
PAUSED  FAILED
  ↓
RUNNING
  ↓
COMPLETED / CANCELLED
```

状态必须有合法 transition，而不是随便写字符串。

## 4. Step ID / Tool Call ID

分布式或可恢复执行里，需要稳定 identity：

```text
run_id
turn_id
step_id
tool_call_id
```

这样 retry 才能判断“这是新动作还是同一个动作重放”。

## 🎯 面试

我会把 Agent 执行分成 Run/Session、Turn、Step。这样预算、Trace、Checkpoint、Retry、Approval 和 Cancellation 都能绑定明确 scope；否则恢复后很容易重复执行 Tool 或丢失状态。

<details><summary>自测：为什么 tool_call_id 对外部副作用很重要？</summary>

它可以作为幂等键的一部分，让恢复 / retry 时识别同一次动作，避免重复扣款、发送消息或创建资源。
</details>
