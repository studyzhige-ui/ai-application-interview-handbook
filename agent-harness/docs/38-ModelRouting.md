# 38｜Model Provider、Model Routing 与 Fallback

## 1. Harness 不应只认识一个模型

Production 常需要：

```text
fast/cheap model
strong reasoning model
long-context model
specialized coding model
fallback provider
```

## 2. Provider Adapter

统一内部接口：

```text
messages / tools / stream / usage / error
        ↓
Provider Adapter
        ↓
OpenAI / Anthropic / internal model
```

但不要假装所有 Provider 语义完全相同；Tool/Reasoning/Context features 需要 capability negotiation。

## 3. Model Routing Inputs

```text
task type
risk
context size
quality requirement
latency SLO
budget
provider health
```

## 4. Fallback 很难

换模型前要考虑：

- Context window 是否更小；
- Tool schema 是否兼容；
- reasoning state 是否可迁移；
- compaction 是否要先发生；
- output behavior 是否改变。

Codex 的 compaction tests/logic里对 model switch 与 context window 的处理正说明模型切换会影响 Runtime state。

## 5. Eval Route，不只 Eval Model

最终要测“router + model + harness”组合的 task outcome、cost、latency。

## 🎯 面试

我会通过 Provider Adapter 抽象公共接口，但保留模型 capability 差异；Routing 根据任务、Context、风险、SLO、预算和 provider health。Fallback 不能简单换模型名，尤其要处理 context window、tool capability 和 state compatibility。

<details><summary>自测：为什么强模型失败后直接切小模型可能再次失败？</summary>

小模型可能 context 更短、tool behavior 不同，甚至无法承接原状态；Runtime 可能要先 compact 或降级任务。
</details>
