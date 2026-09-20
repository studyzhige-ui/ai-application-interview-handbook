# 成熟 Agent 产品源码学习

[← Agent 模块](../README.md)

这一层不重复 `docs/01–24` 的通用知识，而是回答另一个问题：

> **成熟 Agent 产品怎样把 Context、Memory、Tool、Permission、Persistence、Recovery、Trace 与 Evaluation 组合成真实运行时？**

通用课程负责建立概念和因果链；`products/` 负责回到固定源码快照，沿真实数据结构、调用入口、状态变化和 Failure Path 做系统解剖。

---

## 1. 固定学习结构

每个产品保持同一组一级观察视角，便于横向比较：

```text
README                     系统地图、源码快照、关键模块与阅读顺序
01-context-lifecycle.md     上下文从输入到请求、压缩、恢复的完整生命周期
02-memory-lifecycle.md      记忆从发现、提取、整理到召回、维护、评测的完整生命周期
03-tool-lifecycle.md        工具从注册、发现、暴露到权限、执行、回填的完整生命周期
04-engineering-evaluation.md
                           系统边界、Failure、规模化、诊断与评测
```

一级结构固定，二级结构以各产品源码真实实现为准，不强迫不同产品拥有相同的类名、存储介质或控制流。

---

## 2. 产品目录

| 产品 | 状态 | 源码入口 | 学习入口 |
|---|---|---|---|
| OpenAI Codex | ✅ 已建立源码级学习基线 | [openai/codex](https://github.com/openai/codex) | [进入](codex/README.md) |
| Claude Code | ⏳ 待按同一口径整理 | 用户维护的源码镜像 | 待建立 |
| DeepSeek Harness | ⏳ 待按同一口径整理 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 待建立 |
| DeerFlow | ⏳ 待按同一口径整理 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 待建立 |

这里的“完成”不表示产品永远不再变化。每份文档必须记录固定 commit；后续升级时先比较源码变化，再更新结论。

---

## 3. 源码学习的证据规则

产品文档遵循以下规则：

1. **生命周期优先。** 不按文件名罗列功能，而是追踪“信息/状态/调用”从产生到结束的完整路径。
2. **实现与推导分开。** “源码明确实现什么”与“由这些实现可以得到什么工程启示”分别表述。
3. **Runtime State、Context、Memory、History、Persistence 分开。** 都可能落盘，但职责不同。
4. **Prompt 必须回到生产者。** 说明谁生成、何时注入、角色/slot、预算、更新条件和失败边界。
5. **Tool 必须追到结果回填。** 只有注册或 schema 不算完整 Tool Lifecycle。
6. **Memory 必须追到写、读、纠正与评测。** 只有向量检索或聊天历史不算完整 Memory Lifecycle。
7. **规模化问题必须看预算与按需加载。** 包括大 Context、成千上万 Tools / Skills，而不是只给抽象建议。
8. **Failure Path 与测试同样属于源码。** Retry、Cancel、Permission、Sandbox、Resume、Trace、Metrics、Tests 都纳入学习。
9. **固定源码快照。** 所有实现事实以文档首页记录的 commit 为准，避免把不同时间的实现拼接成一个不存在的系统。

---

## 4. 推荐学习方式

第一次学习仍建议先按 [Agent 通用课程](../README.md) 建立概念主线，再进入产品源码。

源码产品层建议：

```text
先看产品 README 的总时序
→ 01 Context
→ 02 Memory
→ 03 Tool
→ 04 Engineering & Evaluation
→ 回到通用课程重新解释设计空间
→ 最后横向比较不同产品为什么做出不同取舍
```

不要把源码文件名本身当作知识体系。真正要掌握的是：

> **输入怎样变成模型可见上下文，长期信息怎样变成记忆，可执行能力怎样安全地变成工具，以及整个系统怎样在失败、超大规模与长期运行下保持可恢复、可诊断、可验证。**
