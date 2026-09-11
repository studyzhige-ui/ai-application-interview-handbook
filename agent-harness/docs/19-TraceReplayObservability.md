# 19｜Trace、Replay 与 Observability

> Agent Observability 不是“打印 Prompt 和 Response”。Production Runtime 要能重建：**模型看到了什么、做了什么、Tool/State 怎样变化、为什么停下。**

## 1. Trace 的层级

```text
Trace = 一次 Run / Task
└─ Span / Event
   ├─ model request
   ├─ tool call
   ├─ guardrail
   ├─ handoff
   ├─ checkpoint
   └─ state transition
```

## 2. 至少记录什么

```text
run / turn / step ids
model + provider
context snapshot/reference
model output / tool call
tool result / artifact
state transition
permission decision
latency / tokens / cost
error / retry / fallback
final outcome
```

敏感内容需要 redact / reference，不能为 Trace 牺牲安全。

## 3. Log 与 Trace 的区别

```text
Log
= 一条局部记录

Trace
= 一条有因果与层级关系的执行链
```

只有日志字符串很难回答：

> “这个错误 Tool Call 是被哪条 Retrieval Evidence、哪次 Compaction、哪个 Handoff 影响的？”

## 4. Replay

Replay 有两类：

```text
Evidence Replay
→ 用保存的模型输入/输出、Tool Result 重建当时发生了什么

Re-execution
→ 重新调用模型/Tool
```

后者受模型随机性和外部环境变化影响，不能保证复现。

## 5. Agent-specific Metrics

除了 Backend 常规 QPS/Latency，还要：

```text
task success rate
steps per successful run
tool failure rate
repair / retry rate
compaction count
permission denial rate
fallback rate
token / cost per success
dead-loop termination rate
```

## 6. Context Observability

Context 本身也应该可观测：

```text
input tokens by source
memory items injected
tool schemas loaded
compaction trigger / ratio
artifact offload count
stale-context correction
```

否则只能看到“Token 很高”，却不知道为什么。

## 7. 源码证据

Codex 固定快照 `rollout-trace` 区分 raw payload evidence、ConversationItem、ToolCall、TerminalOperation、InteractionEdge 等信息层；Compaction 还有独立 trigger/reason/phase/status/token/latency analytics。

OpenAI Agents SDK 官方 tracing 也按 agent/turn/generation/tool/guardrail/handoff 等层级组织 Trace。

## 8. HUMAN-A

`AGENT-043 Execution Trace / Observability` 有 7 个独立来源，主要追问卡住、失败、延迟、Token 异常以及 Replay / Debug。

## 9. 🎯 面试回答

> Agent Trace 要围绕 Run/Turn/Step 建立结构化执行证据，覆盖 model input/output、tool call/result、state transition、permission、retry/fallback、token/cost 和最终 outcome。它和普通日志的区别是能表达因果链并支持 Replay；Replay 最好优先基于保存的 evidence，而不是假设重新调用模型可以得到相同结果。

<details><summary>自测：为什么只记录最终 Prompt/Answer 不足以 Debug Agent？</summary>

因为真正的失败可能发生在 Tool Discovery、Permission、Tool Execution、Compaction、State Transition 或 Multi-Agent Handoff；最终 Prompt 无法还原整条 Runtime 因果链。
</details>