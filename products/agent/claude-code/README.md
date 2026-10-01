# Claude Code｜从输入分流到可恢复的代码任务

[↑ Agent 产品源码](../README.md) · [↑ Products](../../README.md) · [Agent 课程](../../../curriculum/09-agent/README.md) · [源码与技术资料](../../../references/agent/README.md)

Claude Code 把输入处理、模型查询、工具执行和会话状态组织成一个持续工作的代码助手。本模块沿一次分页修复，解释每个模块怎样取得输入、改变状态、交回结果，以及在取消、压缩和恢复后怎样继续。

## 学习对象与版本边界

学习对象是授权私有仓库 [`studyzhige-ui/claude-code-source-private`](https://github.com/studyzhige-ui/claude-code-source-private) 的固定学习快照 [`58231dcce408f805c645cfbc352d2876b517223b`](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b)，2026-10-01 核验 master 所指版本。它不是官方完整公开仓库，尚未与某个官方发行号建立确定映射，也不承诺可直接构建。

正文依据可读快照解释实现；[官方文档](https://code.claude.com/docs/en/overview)只作公开使用背景，不能反推私有快照的行为。源码存在、构建包含、配置启用、入口调用和服务端支持是不同条件。受 `feature(...)`、运行模式或远端配置控制的路径均不能当作所有版本默认行为。

本模块是静态源码讲解与状态推演，未声称运行真实 Claude Code、构建镜像或验证真实 MCP 服务。已核验的机制和未展开的边界集中于[源码索引](../../../references/agent/claude-code-source-index.md)。

## 首次阅读主线

先知道任务由谁接纳、谁决定继续，再理解扩展与子任务，最后理解为什么长任务能够压缩、保存和恢复。无需先背诵源码类名。

| 顺序 | 正文 | 读完应能解释 |
|---|---|---|
| 1 | [输入与查询循环](01-input-and-query-loop.md) | 输入为何可能零模型完成，流式工具怎样促成下一请求，何时真正停止 |
| 2 | [工具与权限](02-tool-execution-and-permissions.md) | 工具池到调用结果的全链，改写、批准竞态、并发与取消 |
| 3 | [Skill、Hook 与 MCP](03-skills-hooks-and-mcp.md) | 技能发现和 inline/fork、阶段反馈、远端工具与结果适配 |
| 4 | [子任务与协作](04-subagents-and-task-ownership.md) | 前台/后台的输入、取消、回报、续做与清理归属 |
| 5 | [上下文与压缩](05-context-and-compaction.md) | 材料如何进请求，结果预算、微压缩、完整摘要及状态重注入 |
| 6 | [会话摘要与自动记忆](06-session-and-auto-memory.md) | 摘要游标怎样接历史，反馈怎样保存、召回、纠正和整理 |
| 7 | [持久化与恢复](07-persistence-and-resume.md) | 保存及 flush 时点、保留区间接链、工作目录与副作用核对 |
| 8 | [观察与交付](08-observation-and-delivery.md) | 如何解读事件与 SDK 结果，并在最终版本判断业务完成 |

贯穿任务只有一个：“修复分页，不改公开接口，不删除原测试，说明实际验证结果。”示例消息、数字和时序均为教学设定，不是产品实测成绩。

```text
输入规范化与命令分流
  ├─ 本地完成 / Hook 阻止 → 直接结果
  └─ 查询 → 模型流 → 工具 / Skill / MCP / 子任务
                         ↓
                 权限、执行、消息与状态回填
                         ↓
              继续请求 / 停止检查 / 最终结果
                         ↓
                 保存与恢复、业务结果验收
```

压缩和记忆在各自消费点维持连续性，不是每轮固定执行的附加工序。恢复消息也不会撤销已经发生的文件或远端操作。

## 第二遍按问题回看

- 上下文：第五章的请求字段、预算冻结、时间清理与缓存编辑，再接第七章的恢复接链
- 记忆：第六章区分 Session Memory 与 Auto Memory，再回看第一章工具后的机会性消费点
- 能力执行：第二章走通一次调用，第三章看扩展怎样接入，第四章看委派怎样结束
- 工程交付：第七章核对恢复条件，第八章区分运行结果、观察证据和最终验收

章末小结回收因果链，面试回答训练简洁表达，误区与自测检查容易混淆的状态；这些是阅读复盘，不增加安装、编码项目或实验交付要求。

## 必要前提与延伸

需要理解模型请求、工具调用、文件与内存状态、异步取消。概念背景见 [Agent Loop](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) 与 [Tool Contract](../../../curriculum/09-agent/docs/04-ToolContractAndValidation.md)。正文先解释机制，源码锚点只负责核对依据。

历史讲解审查见[精修记录](../../../guide/audits/claude-code-clarity-refinement-2026-09-27.md)与[项目记录](../../../guide/project/claude-code-reader-revision.md)；它们记录过去的范围，不替代本模块的当前阅读目录。
