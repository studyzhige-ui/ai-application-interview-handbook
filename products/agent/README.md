# Agent Products｜成熟 Agent 产品源码学习

[↑ Products](../README.md) · [Agent Curriculum](../../curriculum/09-agent/README.md) · [Agent References](../../references/agent/README.md) · [Learning Path](../../guide/learning-path.md)

> 本目录沿固定源码快照学习成熟 Agent 产品怎样把 Context、Memory、Tool、Permission、Persistence、Recovery、Trace 与 Evaluation 组合成真实运行时。

## 1. 学习对象与职责

[Agent Curriculum](../../curriculum/09-agent/README.md) 建立 Agent 的稳定知识模型；本目录回到完整成熟产品，沿真实数据结构、调用入口、状态变化和 Failure Path 做系统解剖。

这里不重复定义“Context 是什么”“Memory 是什么”，而是追问：

```text
一个真实用户任务从哪里进入？
→ 模型这一轮到底看见什么？
→ 长期信息怎样写入、召回和纠正？
→ 工具怎样被发现、授权、执行并回填？
→ 中断、超限、权限拒绝、工具失败以后怎样继续？
→ Trace / Test / Eval 怎样证明系统行为？
```

## 2. 固定学习结构

每个产品保持同一组一级观察视角，便于横向比较：

```text
README.md                   系统地图、源码快照、关键模块与阅读顺序
01-context-lifecycle.md     上下文从输入到请求、压缩、恢复的完整生命周期
02-memory-lifecycle.md      记忆从发现、提取、整理到召回、维护、评测的完整生命周期
03-tool-lifecycle.md        工具从注册、发现、暴露到权限、执行、回填的完整生命周期
04-engineering-evaluation.md
                            系统边界、Failure、规模化、诊断与评测
```

一级结构固定，二级结构以各产品源码真实实现为准，不强迫不同产品拥有相同的类名、存储介质或控制流。

## 3. 产品目录与固定源码快照

| 产品 | 固定源码快照 | 学习入口 |
|---|---|---|
| OpenAI Codex | `openai/codex@67a709665ac7b50311b93e32612c9a8281684787` | [进入](codex/README.md) |
| Claude Code | `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b` | [进入](claude-code/README.md) |
| DeepSeek Harness | `deepseek-ai/deepseek-harness@477b4f420553e8a52c2fbccc464d7561b239c443` | [进入](deepseek-harness/README.md) |
| DeerFlow 2.0 | `bytedance/deer-flow@e2feca1e567d9bafce657de8ad8bc668bd7ad513` | [进入](deer-flow/README.md) |

技术证据和版本边界统一回到 [Agent References](../../references/agent/README.md)。

## 4. 四个产品的架构差异

四个学习模块使用相同的观察问题进行对照；具体能力是否实现、默认开启或可用，须以各自固定快照和入口条件判断，不能从同名栏目推导能力等价。

| 产品 | 核心架构 | 状态与模型视图 | 关键边界 |
|---|---|---|---|
| [OpenAI Codex](codex/README.md) | Thread / Session / Turn / StepContext 构成 Agent Core，Extension Registry 接入额外能力 | StepContext 固定单次采样的执行条件；History、Thread Store、Rollout、State DB、Trace 分工 | Core 执行语义与 Extension 能力分离 |
| [Claude Code](claude-code/README.md) | REPL / QueryEngine 汇入 `query() / queryLoop()` | Transcript 保留可恢复历史；每轮重新生成经过压缩、缓存和能力筛选的 Model View | 持久 Transcript 与 API-bound Context 分离 |
| [DeepSeek Harness](deepseek-harness/README.md) | Cordis Profile / Bundle 组装 Plugin Tree；Agent Loop 本身也是 Plugin | SessionEvent Log 保存持久事实；Surface 是模型可见投影 | Plugin 生命周期、持久事实与模型视图分离 |
| [DeerFlow 2.0](deer-flow/README.md) | Gateway + LangGraph / LangChain Agent + Ordered Middleware | ThreadState 经 Middleware 投影成请求；Checkpoint 保存 continuation state，Run Journal 保存 execution evidence | 基础 Agent 执行、Middleware Runtime 与产品运行证据分层 |

各产品 README 负责展开本产品的对象模型、真实请求链和源码边界；Context、Memory、Tool、Permission、Recovery 等专题进入对应生命周期文档。

## 5. 源码事实与工程解释

产品源码文档不是 API Reference（接口参考手册），也不是把源码字段逐项翻译成中文。文档先讲运行场景和因果关系，再出现必要源码对象。

英文概念第一次出现时给出中文含义；真实类型名、函数名和字段名保持源码命名，用反引号标识。一个源码对象只有在它真正影响生命周期时才展开字段。

文档中的结论分为三层：

1. **直接实现事实：** 能定位到固定 commit 的类型、函数、测试或配置。
2. **跨文件调用链结论：** 由多个源码入口共同确认的真实系统行为。
3. **工程解释：** 对实现为什么这样设计的教学解释，必须建立在前两类证据上。

Prompt 中出现但没有安装入口、调用方或测试支持的概念，不描述成“完整机制已经生效”。

## 6. 核验规则

- **生命周期完整。** 不按文件名罗列功能，而是追踪信息、状态和调用从产生到结束。
- **Runtime State、Context、Memory、History、Persistence 分开。** 即使都能落盘，也不混为一个概念。
- **Prompt 回到生产者。** 说明谁生成、何时注入、角色 / slot、预算、更新条件和失败边界。
- **Tool 追到结果回填。** 只有 Registry 或 Schema 不算完整 Tool Lifecycle。
- **Memory 追到写、读、纠正与评测。** 只有向量检索或聊天历史不算完整 Memory Lifecycle。
- **规模化看预算与按需加载。** 大 Context、大 Tool / Skill Catalog 必须解释如何控制模型可见信息。
- **Failure Path 与测试属于源码。** Retry、Cancel、Permission、Sandbox、Resume、Trace、Metrics、Tests 一并核验。
- **固定快照内闭环。** 不把不同 commit 的行为拼成一套不存在的系统。

## 7. 推荐学习方式

完成 [Agent Curriculum](../../curriculum/09-agent/README.md) 与 Review 后，选择一套产品连续阅读：

```text
产品 README 的系统总图
→ 01 Context
→ 02 Memory
→ 03 Tool
→ 04 Engineering & Evaluation
→ 回到 Agent Curriculum 重新解释设计空间
→ 再进入第二套产品做横向比较
```

本目录的学习目标是：

> **输入怎样变成模型可见上下文，长期信息怎样变成记忆，可执行能力怎样安全地变成工具，以及整个系统怎样在失败、超大规模与长期运行下保持可恢复、可诊断、可验证。**

<!-- product-inventory:start -->
## 模块范围与访问边界

- [Claude Code](claude-code/README.md)：4 篇专题正文，快照 `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`。
- [Codex](codex/README.md)：4 篇专题正文，快照 `openai/codex@67a709665ac7b50311b93e32612c9a8281684787`。
- [DeepSeek Harness](deepseek-harness/README.md)：4 篇专题正文，快照 `deepseek-ai/deepseek-harness@477b4f420553e8a52c2fbccc464d7561b239c443`。
- [DeerFlow 2.0](deer-flow/README.md)：4 篇专题正文，快照 `bytedance/deer-flow@e2feca1e567d9bafce657de8ad8bc668bd7ad513`。

Claude Code 使用学习用私有源码镜像，需相应访问权限；它不等同于可直接构建的官方完整仓库。其他产品也应区分源码快照、安装版本与实际运行验证。
<!-- product-inventory:end -->
