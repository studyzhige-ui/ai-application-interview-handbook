# DeepSeek Harness｜固定源码与机制索引

[← Agent 资料](README.md) · [产品主线](../../products/agent/deepseek-harness/README.md)

固定提交为 [639ed015397290b3745d163aafe02ffee4aa3f84](https://github.com/deepseek-ai/deepseek-harness/tree/639ed015397290b3745d163aafe02ffee4aa3f84)，2026-10-01 02:07 UTC 核验 master。下表帮助核对正文中的因果关系，不是必须按顺序打开的文件清单。

| 机制问题 | 正文 | 对应实现 |
|---|---|---|
| 配置如何成为可运行服务 | [启动](../../products/agent/deepseek-harness/01-boot-and-agent-loop.md#boot) | [启动合同][boot]、[基础组合][base] |
| 输入何时变成请求，何时继续 | [输入](../../products/agent/deepseek-harness/01-boot-and-agent-loop.md#input) | [Agent 阶段机][loop] |
| 动作经过哪些检查 | [调用链](../../products/agent/deepseek-harness/02-tools-files-and-jobs.md#pipeline) | [工具注册和执行][tools] |
| 文件依据如何避免覆盖外部修改 | [观察与版本](../../products/agent/deepseek-harness/02-tools-files-and-jobs.md#file-observation) | [观察策略][fs] |
| 前台等待怎样转为后台结果 | [作业](../../products/agent/deepseek-harness/02-tools-files-and-jobs.md#jobs) | [Bash][bash]、[完成通知][jobs] |
| 审批如何持久记录 | [审批](../../products/agent/deepseek-harness/02-tools-files-and-jobs.md#approval) | [审批服务][approval] |
| 能力如何发现、失效和重连 | [扩展](../../products/agent/deepseek-harness/03-skills-mcp-and-ptc.md) | [技能目录][skills]、[MCP 连接][mcp] |
| 计划、目标、工作流为何不同 | [运行编排](../../products/agent/deepseek-harness/04-plans-goals-and-agents.md) | [计划][plan]、[目标驱动][goal]、[Workflow 收尾][workflow] |
| 子任务怎样创建和冷恢复 | [委派](../../products/agent/deepseek-harness/04-plans-goals-and-agents.md#subagent) | [ChildAgent][child] |
| 调度失败如何闭合历史 | [活跃修复](../../products/agent/deepseek-harness/05-session-and-recovery.md#live-step-repair) | [调用恢复器][repair]、[消费点][loop] |
| 压缩如何选择、替换和结束 | [压缩](../../products/agent/deepseek-harness/05-session-and-recovery.md#compaction) | [区间与事务][region]、[摘要合同][summary] |
| 哪些信息跨会话仍能使用 | [信息来源](../../products/agent/deepseek-harness/06-cross-session-knowledge.md) | [引用投影][reference] |

## 本轮核验边界

完整新旧 Git tree 对照发现 1,633 个新增/变化文件与 10 个删除文件。根递归响应过大时，按根目录各子树取得完整结果，没有把 Compare API 的 300 文件返回当作全量差异。这些数量仅说明差异范围，不表示逐个精读所有文件。

本轮重读主循环、工具调度与恢复器，核对原文引用的最新组合、文件观察、命令/作业、审批、计划、目标、子任务、扩展、压缩、持久化与引用入口；工作流补读发布与持有者收尾。最新的活跃步骤错误修复、装配兼容性和遥测批次边界已进入正文。

没有执行产品、上游测试、模型请求或故障注入。原有 labs 是历史检查材料，其旧快照与执行状态不能算作本轮结果；首次阅读无需完成实验。

[boot]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/boot/app-boot/README.md
[base]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/bundle/base/cordis.patch.yml
[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/agent-loop/src/agent.ts
[tools]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/tools/src/index.ts
[fs]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/fs/fs-observation-policy/src/index.ts
[bash]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/shell/tool-bash/src/index.ts
[jobs]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/jobs/tool-jobs/src/index.ts
[approval]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/interaction/user-approval/src/index.ts
[skills]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/skill/tool-skill/src/index.ts
[mcp]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/mcp/mcp-client/src/connection.ts
[plan]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/plan/plan-mode/README.md
[goal]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/goal/goal-round-driver/README.md
[workflow]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/workflow/workflow-ptc/src/host.ts
[child]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent/src/child-agent.ts
[repair]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/session/src/repair.ts
[region]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-basic/src/region.ts
[summary]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/compaction/compaction-basic/src/summarizer.ts
[reference]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/context/session-reference/src/projection.ts
