# Products｜成熟 AI 系统源码学习

[↑ Handbook 总目录](../README.md) · [Curriculum](../curriculum/README.md) · [Practice](../practice/README.md) · [References](../references/README.md) · [Learning Path](../guide/learning-path.md)

> Products 回答：**成熟 AI Application / Agent 产品怎样把多个通用机制组合成可运行、可恢复、可诊断、可验证的完整系统？**

## 1. 这一层解决什么

Curriculum 按知识依赖拆开学习机制；Products 沿真实产品的固定源码快照重新把这些机制组合起来。

```text
Curriculum
→ 学清楚 Context / Memory / Tool / Database / Runtime / Evaluation 等通用机制
→ Products
→ 沿真实对象、调用链、状态变化和 Failure Path 还原完整系统
→ Practice / System Design / Interview
→ 把观察到的工程取舍迁移到自己的实现与表达
```

Products 的目标不是背产品 API，也不是把源码字段翻译成中文，而是回答：

- 用户任务怎样进入系统并形成一次真实执行；
- 多个模块怎样共享状态、上下文、权限与持久化边界；
- 正常路径、失败路径、恢复路径分别由谁负责；
- 为什么成熟产品会采用不同的工程取舍；
- 哪些结论属于某个固定版本，哪些可以抽象成更通用的工程知识。

## 2. 与其他层的边界

| 层 | 主要问题 |
|---|---|
| [Curriculum](../curriculum/README.md) | 应该系统掌握哪些可迁移机制？ |
| **Products** | 成熟系统怎样把这些机制组合成真实产品？ |
| [Practice](../practice/README.md) | 自己怎样实现、修改、调试和交付？ |
| [References](../references/README.md) | 技术事实、固定版本与源码依据是什么？ |
| [Market](../market/README.md) | 企业招什么、真实面试问什么？ |
| [Interview](../interview/README.md) | 怎样把市场证据归一化为可训练能力？ |

Products 不创建新的 Canonical Ownership，不改变 Curriculum 顺序，也不增加 HUMAN-A Source Count。

## 3. 产品类别

| 类别 | 学习范围 | 入口 |
|---|---|---|
| Agent | Coding Agent / Agent Harness / Super Agent Runtime | [进入](agent/README.md) |

Agent 类别包含四套成熟源码学习基线：

- [OpenAI Codex](agent/codex/README.md)
- [Claude Code](agent/claude-code/README.md)
- [DeepSeek Harness](agent/deepseek-harness/README.md)
- [DeerFlow 2.0](agent/deer-flow/README.md)

## 4. 产品源码学习规则

每套产品学习遵循同一组约束：

1. **固定源码快照。** 版本敏感事实必须绑定 repo、commit 与核验日期。
2. **产品语义优先。** 先还原产品自己的对象模型与执行路径，再映射到通用课程术语。
3. **生命周期优先。** Context、Memory、Tool、Permission、Persistence、Recovery、Trace 与 Evaluation 都追到完整输入、状态变化、输出和失败边界。
4. **事实与解释分开。** 源码直接事实、跨文件调用链结论、工程解释分别表达。
5. **Failure 与 Tests 属于系统本身。** Retry、Cancel、Approval、Sandbox、Resume、Replay、Metrics、Tests 都纳入阅读。
6. **不强迫产品同构。** 没有实现的能力明确写成边界，不为了横向对齐虚构模块。
7. **证据回到 References。** 源码索引、官方规范和固定版本事实由 References 维护。

## 5. 推荐进入方式

Products 建议在对应 Curriculum 模块建立完整知识主线并完成 Review 后进入。Agent 产品的统一入口是 [Agent Products](agent/README.md)。

第一次阅读一套产品时，优先保持产品内部的连续顺序，不按自己熟悉的术语跳着找文件；完成一套产品后，再进行跨产品比较。
