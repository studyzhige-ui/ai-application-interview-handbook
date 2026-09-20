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
| Claude Code | ✅ 已建立源码级学习基线 | [私有源码镜像](https://github.com/studyzhige-ui/claude-code-source-private) · `58231dc` | [进入](claude-code/README.md) |
| DeepSeek Harness | ⏳ 待按同一口径整理 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 待建立 |
| DeerFlow | ⏳ 待按同一口径整理 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 待建立 |

这里的“完成”不表示产品永远不再变化。每份文档必须记录固定 commit；后续升级时先比较源码变化，再更新结论。

---

## 3. 源码学习的证据与写作规则

产品源码文档不是 API Reference（接口参考手册），也不是把源码字段翻译成中文后逐项罗列。它首先是一份给学习者阅读的教材，所以固定采用“先讲运行场景和因果关系，再出现必要源码对象”的顺序。

英文概念第一次出现时给出中文含义；代码里的真实类型名、函数名和字段名保持原样，用反引号标识，不为了中文化而改造源码命名。一个源码对象只有在它真正影响生命周期时才展开字段，不做无目的的数据结构抄录。

章节内部优先用连续自然语言解释“为什么需要 → 正常路径怎样走 → 状态在哪里改变 → Failure 时谁负责 → 如何验证”，避免把一个完整流程拆成几十个只有两三句话的小标题。

### 源码事实和工程抽象必须分开

文档中的事实有三种来源层级：

1. **直接实现事实：** 能定位到当前固定 commit 的类型、函数、测试或配置。
2. **跨文件调用链结论：** 由多个源码入口共同确认，例如 Memory Extension 确实既贡献 Context 又注册 Tool。
3. **工程解释：** 对实现为什么这样设计的教学解释。它必须明确建立在前两类证据上，不能反过来把通用教材观点写成产品事实。

如果一个概念只存在于 Prompt 模板或注释，却找不到安装入口、调用方或测试，不把它描述成“完整实现已经生效”。

---

## 4. 源码核验规则

产品文档遵循以下规则：

1. **生命周期优先。** 不按文件名罗列功能，而是追踪“信息 / 状态 / 调用”从产生到结束的完整路径。
2. **实现与推导分开。** “源码明确实现什么”与“由这些实现可以得到什么工程启示”分别表述。
3. **Runtime State、Context、Memory、History、Persistence 分开。** 都可能落盘，但职责不同。
4. **Prompt 必须回到生产者。** 说明谁生成、何时注入、角色/slot、预算、更新条件和失败边界。
5. **Tool 必须追到结果回填。** 只有注册或 schema 不算完整 Tool Lifecycle。
6. **Memory 必须追到写、读、纠正与评测。** 只有向量检索或聊天历史不算完整 Memory Lifecycle。
7. **规模化问题必须看预算与按需加载。** 包括大 Context、成千上万 Tools / Skills，而不是只给抽象建议。
8. **Failure Path 与测试同样属于源码。** Retry、Cancel、Permission、Sandbox、Resume、Trace、Metrics、Tests 都纳入学习。
9. **固定源码快照。** 所有实现事实以文档首页记录的 commit 为准，避免把不同时间的实现拼接成一个不存在的系统。

---

## 5. 推荐学习方式

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
