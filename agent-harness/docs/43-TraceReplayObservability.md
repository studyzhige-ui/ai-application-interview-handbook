# 43｜Trace、Replay 与 Observability

## 1. Agent Debug 为什么比 API Debug 难

失败路径可能是：

```text
wrong context
→ wrong model decision
→ wrong tool
→ tool result misunderstood
→ compaction loses fact
→ later failure
```

只看最终 response 完全不够。

## 2. Trace Hierarchy

一个有用层级：

```text
Run / Task
└─ Agent / Turn
   ├─ Generation
   ├─ Tool Call
   ├─ Guardrail / Approval
   ├─ Handoff
   └─ State Transition
```

OpenAI Agents SDK 官方 tracing 就显式记录 task/agent/turn/generation/tool/guardrail/handoff；Codex rollout trace 则区分 model-visible ConversationItem、ToolCall、TerminalOperation 与 information-flow edge。

## 3. 关键字段

```text
run_id / turn_id / call_id
model + config
context version / token usage
tool args/result reference
latency / cost
state transition
error / retry
artifact / outcome
```

## 4. Replay

Trace 应支持回答：

> 当时模型到底看到了什么？

而不是只保留“模型调用成功”。

Replay 时对外部 side effect 应 mock / freeze，避免调试再次真实执行。

## 5. Metrics

- task success；
- turns per task；
- tool error rate；
- retry / approval rate；
- compaction frequency；
- token/cost；
- TTFT / total latency；
- cancellation / abandonment。

## 🎯 面试

Agent Observability 要记录 Run→Turn→Generation/Tool/State 的层级 Trace，并保留 model-visible context 与真实 tool evidence 的关联。这样才能 Debug、Replay、做 Eval；但敏感 input/tool result 要 redaction。

<details><summary>自测：为什么只有 Prompt/Response Log 不够？</summary>

缺少 Tool、state transition、approval、retry、environment outcome，无法重建真实执行链。
</details>
