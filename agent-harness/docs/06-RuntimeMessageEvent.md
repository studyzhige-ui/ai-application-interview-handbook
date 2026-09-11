# 06｜Runtime Message / Event Model

## 1. Message 和 Event 不是一回事

**Message** 通常指模型可见的对话内容；**Event** 表示 Runtime 里真实发生的事情。

```text
Runtime Event Stream
├─ user_input_received
├─ model_started
├─ model_output
├─ tool_call_requested
├─ approval_requested
├─ tool_started
├─ tool_progress
├─ tool_completed
├─ checkpoint_written
└─ run_completed
```

模型不需要看见其中全部事件。

## 2. 为什么要分开

如果把所有 Runtime 信息都塞回 messages：

- Context 急剧膨胀；
- UI/debug 信息污染模型；
- Secret / internal metadata 泄露；
- Replay 与 model-visible history 混在一起。

Claude Code 的类型里区分多种 Message / Progress；Codex 则有 `EventMsg`、`TurnItem` 和 rollout trace，这都说明 Runtime 需要自己的事件模型。

## 3. Reducer 心智模型

一种稳定设计：

```python
new_state = reduce(old_state, event)
```

Event append-only，State 是对事件的当前投影。

好处：

- Replay；
- Debug；
- Audit；
- 派生不同 UI；
- 恢复 state。

不要求所有实现都 event sourcing，但这个模型非常适合理解 Agent Runtime。

## 4. Model-visible Projection

真正送模型的是 Event / State 的投影：

```text
Runtime Truth
→ filter / summarize / redact
→ Model Context
```

这也是后面 Context Engineering 的核心。

## 🎯 面试

我会区分 runtime event log 和 model conversation history。前者追踪真实执行事实，后者只是模型当前需要看到的投影。这样才能同时做到可恢复、可审计和 Context 可控。

<details><summary>自测：Tool progress 是否一定要喂给模型？</summary>

不一定。很多 progress 只给 UI / observability；只有会改变模型下一步决策的信息才需要成为 model-visible observation。
</details>
