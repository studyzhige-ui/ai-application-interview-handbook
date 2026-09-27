# Curriculum Granularity Audit｜教材粒度最终口径

[← Handbook 总目录](../../README.md) · [Knowledge Map](../knowledge-map.md) · [Content Depth Audit](content-depth-audit.md)

> 研究粒度、能力粒度、教材文件粒度不是同一个层级。**Canonical 可以很细，但一个 Markdown 应形成完整认知闭环。**

## 固定规则

```text
HUMAN-A / Canonical Question = 面试最小可独立追问单元
Capability Primitive          = 工程机制最小单元
教材 Markdown                 = 可独立学习 / 画图 / 解释 Failure & Trade-off 的知识块
Section                       = 参数 / 变体 / Failure / 深挖追问
```

独立成文件时，主题应能回答一个完整大问题，并拥有自己的机制、Failure Model / Trade-off 和验证闭环。

## 当前最终结构

| 模块 | 研究 / 历史输入 | 当前 Curriculum | 状态 |
|---|---|---:|---|
| Python | 12-block v1 / 15 Canonical | 13 | ✅ |
| FastAPI | ~40 outline topics / 4 Canonical | 16 | ✅ |
| AI Backend Engineering | ~55 outline topics / 39 Canonical | 22 | ✅ |
| MySQL | 26 Canonical | 19 | ✅ |
| Redis | 27 old blocks / 19 Canonical | 18 | ✅ |
| Vector DB | 23 old blocks / 12 Canonical | 16 | ✅ |
| LLM Foundation | 29 old blocks / 23 Canonical | 14 | ✅ |
| RAG | 34 old blocks / 29 Canonical | 14 | ✅ |
| [Agent](../../curriculum/09-agent/README.md) | 原23章丰富版 / 44 Canonical；协议与扩展生命周期分别闭环 | 24 | 已重组并核对内容去向 |
| System Design | 24 Scenario Canonical | 19 | ✅ |

这些数字是结果，不是目标。教材重组永远不能改变 HUMAN-A、Source Count、Primary Ownership 或 Verified Follow-up Chain。
