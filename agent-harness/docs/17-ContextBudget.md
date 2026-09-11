# 17｜Context Budget 与 Token Economics

## 1. Context Window 是硬容量，不是目标值

模型支持 200K，不代表每轮都该塞 200K。

Context 成本同时影响：

```text
latency
money
attention quality
cache hit
compaction frequency
```

## 2. Budget 分桶

一种实用方法：

```text
reserved instructions
reserved current task
reserved output
history budget
memory budget
tool-definition budget
tool-result budget
```

不要所有来源抢同一个“剩多少塞多少”。

## 3. 优先级

通常更应保留：

1. 当前 Goal / hard constraints；
2. 最新状态与关键 Observation；
3. 正在执行所需 Tool schema；
4. 与当前决策高度相关的 history / memory；
5. 可重新查询的信息最后保留。

## 4. Token Budget ≠ Character Count

真正线上系统应使用 tokenizer estimate 或 provider usage，而不是 `len(text)`。

## 5. Context Economy

每塞入一个 token 都应问：

> 它会改变当前决策吗？能否用引用、摘要、外部 artifact 代替？

## 🎯 面试

Context window 是上限，我会做分层 budget：instructions、current task、history、memory、tool definitions、tool results，并预留 output。优先保留不可重建的目标和状态，把可重查的大结果外置，避免“窗口大就全塞”。

<details><summary>自测：为什么给 Tool Definitions 单独预算？</summary>

工具很多时 schema 本身会占大量 token，并可能降低选择准确性；所以需要 discovery / progressive loading，而不是全量常驻。
</details>
