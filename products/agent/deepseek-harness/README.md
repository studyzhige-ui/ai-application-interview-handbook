# DeepSeek Harness｜沿一个任务理解上下文、记忆、工具与恢复

[↑ Agent Products](../README.md) · [通用 Agent 课程](../../../curriculum/09-agent/README.md) · [技术资料索引](../../../references/agent/README.md)

用户提出：“修复分页函数。`[10, 20, 30]` 每页两项时，第一页应返回 `[10, 20]`。只修改实现，不修改测试。”模型能建议修正偏移公式，但编码助手还要找到文件、读取项目规则、取得写入许可、运行测试，并在中断后判断哪些事情已经完成。

本模块沿 DeepSeek Harness 的真实实现追踪这项任务。**模型提出下一步，Harness 组织输入、控制工具执行、保存记录，让下一步有依据。** 分页任务是贯穿讲解的教学场景，不是产品实测成绩；它的实现与测试来自 [Coding 分页练习](../../../practice/coding/exercises/09-ai-coding-lab/README.md)。

阅读前应理解：模型接收消息，工具需要程序实际调用，异步操作可能失败。通用概念还不熟悉时，先完成 [Agent 课程](../../../curriculum/09-agent/README.md)；本模块会解释 DSH 自己的对象，不要求你预先熟悉它的包名或内部接口。

## 核心设计：先建立一个最小系统模型

| 对象 | 在分页任务中负责什么 |
|---|---|
| Agent（正在工作的智能体实例） | 接收任务，一次次请求模型，调度模型提出的工具调用 |
| Session（会话） | 按顺序记录输入、回复、工具结果和执行边界，供后续请求与恢复使用 |
| Tool（工具） | 真正读取、修改文件或运行测试，返回可供下一步检查的结果 |

一次任务通常不只请求一次模型。模型先要求读文件，程序读完，把结果交给下一次请求；模型有了代码才提出修改，之后还需要测试结果才能判断是否完成。[主循环源码][loop]

```text
用户任务与项目规则
        ↓
Agent 组织本次模型请求 ←───── Session 派生相关历史
        ↓                               ↑
模型提出读取、修改或测试                 │
        ↓                               │
程序检查权限，工具实际执行 ─── 记录调用与结果
        ↓
继续请求模型，或结束本轮
        ↓
核对文件差异、测试结果与用户约束
```

一个 Session 可以跨多次进程运行保留；Agent 的网络请求、取消信号等活动对象则需要重新创建。**历史可读取、操作已完成、任务已验收，是三件需要分别确认的事。**

## 阅读路线

| 顺序 | 入口 | 沿分页任务回答什么 |
|---:|---|---|
| 1 | [上下文生命周期](01-context-lifecycle.md) | 一次正常修复怎样经过多次请求；每次到底发送哪些内容；补充要求和压缩怎样改变后续输入 |
| 2 | [记忆生命周期](02-memory-lifecycle.md) | 第二天继续工作时，从原会话、项目规则、引用或外部存储找到什么；过期信息应在哪里更正 |
| 3 | [工具生命周期](03-tool-lifecycle.md) | 一次调用怎样经过可见性、参数、审批和执行；再看 Skill、MCP、PTC 怎样复用这条执行链 |
| 4 | [工程闭环与验证](04-engineering-evaluation.md) | 先恢复单个任务，再扩展到父子协作，最后用过程与结果验证真正完成 |

各章的正文先建立过程，相关位置的折叠说明承接配置与实现细节。章末保留面试表达、易错点和可独立作答的自测；核心规则不藏在答案里。

[源码阅读与验证实验](labs/README.md)从一个固定上游测试开始，给出准备条件、命令和观察点，再扩展到真实模型与工具实验。无需先搭建完整产品，才能开始核对一项恢复规则。

## 为什么源码分布在许多插件里

DSH 使用 **Cordis 插件框架**。插件把一项服务或处理过程注册进共同的应用上下文 `ctx`；其他插件通过接口使用它。例如，工具注册器提供 `ctx.tools`，主循环利用它调度调用。这里的 `ctx` 是程序访问服务的入口，不是全部发送给模型的提示词。[架构说明][architecture]

三个名称分工不同：

- **Plugin（插件）**实现或接入一个职责，例如模型适配器、工具注册器。主循环本身也是插件。
- **Bundle（组合包）**分发一组插件配置及其代码，例如共同基础组合 `dsh-base`。
- **Profile（运行配置档）**选择本次启动所用的组合与覆盖配置，例如 `web`、`headless`、`sdk`。

因此，查一项能力要先确认所用 Profile，再看有效插件和调用链。仓库里有实现，不代表本次运行已经启用；注册还随插件寿命结束而撤销。

<details>
<summary>核对部署配置时：独立组合、覆盖方式与启动顺序</summary>

`sdk-minimal` 是不应用 `dsh-base` 的独立组合，不能直接套用 Web 的默认行为。配置补丁按顺序覆盖指定行，替换的是整行 `config`，不是逐字段深度合并。YAML 的展示行序也不是插件启动顺序；判断依赖和生效能力，应结合组合规则及实际服务注册。[组合规则][architecture]、[基础组合源文件][base]

</details>

<a id="source-version"></a>
## 阅读版本与运行前提

本模块的实现结论固定于上游默认分支 `master` 的同一快照：

| 项目 | 固定信息 |
|---|---|
| 源码仓库 | `deepseek-ai/deepseek-harness` |
| 源码提交 | `477b4f420553e8a52c2fbccc464d7561b239c443` |
| 根包版本 | `0.1.7-rc.2` |
| 上游提交时间 | 2026-09-24 13:39:59 UTC |
| Node 运行要求 | `^22.19.0 \|\| >=24.0.0` |
| 包管理器声明 | `pnpm@11.7.0` |

版本与运行要求见[固定快照的 package.json][package]。TypeScript 是产品实现语言；Python 是分页练习对象的语言，两者不是同一项前置。源码阅读、上游单元测试、真实模型服务和操作系统沙箱各有验证边界，不能用安装成功代替产品测试成功。

## 第二遍怎样重建主线

合上正文，画出“任务—读取—修改—测试—结论”的时间线。在每个动作旁标出执行者、读写对象、留下的记录，以及中断后仍未知的结果。再把条件换成“只给修改建议，不得写文件”，检查哪些允许路径发生了变化。

[工程章的综合自测](04-engineering-evaluation.md#self-test)继续检查这种迁移能力。[精修与发布记录](../../../guide/audits/deepseek-harness-clarity-refinement-2026-09-27.md)区分源码核对、文稿检查、实际运行与发布状态；此前的证据映射保存在[读者优先修订记录](../../../guide/audits/deepseek-harness-reader-first-2026-09-27.md)。

[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/agent-loop/src/agent.ts
[architecture]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/docs/architecture.md
[base]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/bundle/base/cordis.patch.yml
[package]: https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/package.json
