# 33｜Tool Discovery 与 Progressive Loading

## 1. 为什么不能把所有 Tool 都塞给模型

Tool 数量从 8 个变成 800 个后会出现：

```text
schema token 爆炸
选择混淆
同名/近义工具增加
延迟与成本上升
```

Anthropic Advanced Tool Use 明确把 on-demand discovery 当成大规模能力库的核心问题；Claude Code `Tool.ts` 也有 `searchHint` 与 dynamic skill discovery 相关状态。

## 2. 两阶段能力选择

```text
Capability Catalog
→ Search / Filter / Rank
→ Load selected full schemas
→ Model chooses exact tool
```

第一阶段不一定用 LLM，可以用 tag、keyword、embedding、rules。

## 3. Tool Metadata

Discovery 需要轻量 metadata：

```text
name
capability phrase
tags
source
risk
latency/cost
availability
```

完整 schema 延迟加载。

## 4. Discovery Failure

- 找不到正确 Tool；
- 错误 Tool 排得太高；
- capability metadata 过期；
- dynamic Tool 当前 unavailable；
- tool version 改了。

因此 Tool Discovery 也需要 eval：给一组真实 tasks，看正确 capability 是否进入候选集。

## 🎯 面试

当 Tool 规模上百时，我不会全量注入 schema，而是先维护轻量 capability catalog，用 keyword/semantic/rule 做 discovery，选出少量候选后再加载完整 contract。Discovery 本身要测 recall 和误选，不是单纯省 token。

<details><summary>自测：Tool Discovery 的 Recall 为什么重要？</summary>

如果正确 Tool 根本没进入候选集，后面的模型再强也无法选择它。
</details>
