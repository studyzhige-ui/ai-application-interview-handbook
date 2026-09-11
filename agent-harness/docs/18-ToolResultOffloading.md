# 18｜Large Tool Result、Offloading 与 Reference

## 1. 最常见 Context 杀手

不是用户 Prompt，而是：

```text
shell log
large file
search results
SQL rows
browser DOM
MCP result
```

一次 Tool 就可能产生数万 token。

## 2. 三种处理

### Truncate

只保留首尾 / 关键段。便宜，但可能丢信息。

### Summarize

模型或程序提炼。压缩率高，但有信息失真风险。

### Offload + Reference

```text
raw result → artifact store
context → artifact_id + summary + retrieval hint
```

需要时再 Read/Query。

这通常是更可扩展的模式。

## 3. 引用要可寻址

坏：

```text
“结果太长，我省略了”
```

好：

```json
{
  "artifact_id":"toolres_123",
  "summary":"120 test failures, 3 clusters",
  "read_tool":"read_artifact"
}
```

## 4. Claude Code / Anthropic 信号

Claude Code Tool context 中直接存在 tool-result content replacement state；Anthropic 也公开讨论 Tool definitions / results 对 Context 的压力和按需访问。

## 🎯 面试

大 Tool Result 不应无限回填。常用策略是 truncate、summary、或把 raw result 外置为 artifact，只在 Context 保留稳定 reference 和当前决策所需摘要；同时 Trace 保留原始结果用于 Debug。

<details><summary>自测：为什么单纯 summary 可能不够？</summary>

摘要可能漏掉后来才重要的细节。若 raw artifact 仍可寻址，Agent 后续可以按需重新读取。
</details>
