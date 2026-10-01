# DeepSeek Harness｜插件组合怎样持续推进一项任务

[↑ Agent 产品](../README.md) · [Agent 通用课程](../../../curriculum/09-agent/README.md) · [源码依据](../../../references/agent/deepseek-harness-source-index.md)

DSH 把模型调用、文件操作、作业、计划、目标和子任务装配在同一套服务中。理解它，先看本次实际启动了什么组合，再沿 Session 事件追踪输入怎样成为请求、动作怎样产生结果、结果怎样推动下一步。

<a id="source-version"></a>
## 固定源码与边界

- 公开仓库：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- 当前快照：[639ed015397290b3745d163aafe02ffee4aa3f84](https://github.com/deepseek-ai/deepseek-harness/tree/639ed015397290b3745d163aafe02ffee4aa3f84)，2026-10-01 02:07 UTC 核验默认分支 master
- 主要按基础组合解释，并在分支处标出 Profile、插件与平台条件；sdk-minimal 不套用 base 默认行为
- 本轮为源码与文档核验，没有运行模型任务或上游产品测试。代码环境视为已具备，不增加安装或实验要求

使用一次“修复分页，但不修改测试”的任务贯穿说明。读者应能说清输入、调用、状态和交接，源码链接只是查证依据。

## 第一次顺着运行读

| 顺序 | 章节 | 解释的连接 |
|---|---|---|
| 1 | [启动与循环](01-boot-and-agent-loop.md) | Profile/Bundle 形成服务，Agent 接纳 Inbox 并请求模型 |
| 2 | [工具、文件与作业](02-tools-files-and-jobs.md) | 工具策略怎样落实到文件版本、命令进程与完成通知 |
| 3 | [技能、MCP 与 PTC](03-skills-mcp-and-ptc.md) | 扩展能力怎样进入现有的发现、调用和结果链 |
| 4 | [计划、目标与委派](04-plans-goals-and-agents.md) | 模式切换、自动续轮、子 Agent、工作流各由谁负责 |
| 5 | [会话与恢复](05-session-and-recovery.md) | 事件落盘、Surface 压缩、活跃失败与重载修复 |
| 6 | [跨会话信息](06-cross-session-knowledge.md) | 项目规则、历史引用和外部记忆怎样成为当前依据 |
| 7 | [交付与复盘](07-delivery-and-review.md) | 把流、作业和会话事件还原成可信完成结论 |

```text
配置组合 → 服务就绪 → Agent + Session
                         ↓
Inbox → pre-step → 请求模型 → 工具策略与实际执行
             ↑                      ↓
             └──── 有序结果、附加背景、作业通知
                         ↓
             队列与停止检查允许 → 结束本轮
                         ↓
                 保存、验收、后续继续
```

Session 是顺序事实记录，Surface 是当前选给模型的消息视图，Agent 是正在执行的对象。它们的寿命不同：恢复日志不等于恢复原进程；压缩模型视图不等于删除全部历史。

## 第二遍按问题回看

- 上下文：[消息视图](01-boot-and-agent-loop.md#views)、[压缩与摘要](05-session-and-recovery.md#compaction)
- 动作：[文件版本](02-tools-files-and-jobs.md#file-observation)、[后台作业](02-tools-files-and-jobs.md#jobs)、[审批](02-tools-files-and-jobs.md#approval)
- 继续工作：[目标](04-plans-goals-and-agents.md#goal-rounds)、[子 Agent](04-plans-goals-and-agents.md#subagent)、[工作流](04-plans-goals-and-agents.md#workflow)
- 跨任务：[会话引用](06-cross-session-knowledge.md#reference)、[外部记忆](06-cross-session-knowledge.md#external-memory)
- 复盘：[完整事件轨迹](07-delivery-and-review.md#event-trace)、[面试与自测](07-delivery-and-review.md#self-test)

本组合没有与其他产品可直接等同的自动长期记忆流水线。会话恢复、项目规则、摘要、旧会话引用和外部记忆服务分别解释，不能只因都能“记住一些信息”就合成一个不存在的自动系统。
