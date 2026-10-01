# 计划、目标与委派｜决定谁在什么时候继续

[← 上一章](03-skills-mcp-and-ptc.md) · [本产品目录](README.md) · [下一章 →](05-session-and-recovery.md)

运行循环不只由用户的下一句话推动。计划模式改变工作阶段，目标驱动安排新轮次，子 Agent 和工作流增加独立执行者。本章分别讲清它们的状态和交接，不把“自动继续”混成一种能力。

<a id="plan-mode"></a>
## 计划模式：改变当前工作阶段，不偷偷删掉工具

计划模式将当前状态保存在 `plan/mode` 事件中，通过折叠最近值恢复。没有打开轮次时可立即变更；运行中变更先等待下一次接纳的 pre-step 才进入日志。还没到该边界就退出进程，待生效变更可能丢失，不能把界面上“准备切换”当作已持久化。

模式开启后注入计划指导，但工具目录保持一致；这是维持请求形状和缓存稳定的选择，**不是只读沙箱**。真正的禁止写入仍要由工具权限和沙箱实现。普通新建子任务默认不在计划模式，fork 可以继承已记录状态。

模型完成计划时，用 `exit_plan_mode` 提交完整计划，专门交互让用户审阅这份内容。批准后退出模式；要求继续规划则把反馈交回循环；没有可用交互端时，工具不能假装获得批准。直接 `/plan off` 是用户主动的另一退出入口。仍被其他活跃父 Agent 拥有的子任务不能自己开启这种审阅，应把未决问题交回父级。[计划状态与退出合同](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/plan/plan-mode/README.md)

<a id="goal-rounds"></a>
## 持续目标：在同一个会话中安排下一轮

目标服务保存目标及其版本，目标工具改变状态，`goal-round-driver` 只负责调度。它在整个 Agent 空闲、目标仍有效、续轮已被允许、没有竞争输入且轮数有余量时，预留下一轮。预留并未消耗配额；目标来源消息真正进入历史，才增加已启动轮数。

安排前先等待目标变更持久化，然后重新检查版本和输入；pre-step 的前后也核对预留的目标身份与 revision。用户在等待期间改目标或发来新任务，旧自动提示不能强行进入。暂停、完成、阻塞、取消、输出上限、持久化失败和插件卸载都会阻止相应继续路径。

恢复或 fork 后，即使日志里目标仍为 active，也不会自动重新获得续轮授权。需要明确的、人类授权的 resume 才重新武装。轮数上限是循环限制，不是 token、金额或时间预算；它们是独立策略。该驱动也不是独立评测器，目标被模型标完成不等于代码已经通过验收。[同会话目标驱动](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/goal/goal-round-driver/README.md)

## 基础组合实际上提供哪种委派

基础组合给 spawn 配置可继续的子任务工具，给 fork 配置一次性子任务工具；workflow 使用 spawn 提供方。先知道这个实际选择，再看历史、能力、寿命和所有权四个维度，避免从工具名字推断所有部署都相同。[组合选择](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/bundle/base/cordis.patch.yml)

<a id="workflow"></a>
## Workflow：有明确持有者的脚本与子任务运行

PTC 只说明程序内可以组合调用；workflow 另有运行身份和完整生命周期。开始前先验证元信息、解析脚本、确认子 Agent 提供方存在，并把请求的总子任务上限与部署上限比较。此时失败，根本没有发布一个运行中的工作流。

通过后创建运行句柄并发出 start。脚本在共享的沙箱化 Node PTC 执行器中运行，使用父 Session 的文件策略；它可以通过受控绑定启动子 Agent。阶段、日志、子任务开始/结束是观测事件，真正输出值留给持有运行句柄的调用方，不能只从“阶段完成”事件推导结果。

外部取消只认第一次原因，传播到运行控制器，并请求释放已发布子任务；若一个启动在取消后才返回，也会被清理。最终无论完成、错误还是取消，都先停止继续接纳、等待在途绑定和子任务释放，再结算结果。已经返回运行句柄以后，失败通过 `result.stopReason` 表达，而不是让消费者永久等待一个拒绝且无人处理的 Promise。[发布与边界](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/workflow/workflow-ptc/src/index.ts)、[取消与收尾](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/workflow/workflow-ptc/src/host.ts)

基础组合还装配 `ralph`，用于经人类明确要求的独立重复尝试；它与同会话目标续轮不同，不能仅因任务困难就把两者互换。每轮新建一个不继承父对话的子任务，只给不变目标、轮次上限和上轮有界结构化报告；跨轮长期依据是共享工作区。报告必须包含状态、总结、证据、下一步和阻塞信息，并满足该状态的规则，例如完成报告必须有证据且没有下一步。无效或超大报告报错，不偷偷截短后继续。

`ralph` 是前台固定循环：模型只提交目标和轮次上限，不能改循环脚本或提供方。子级报告完成/阻塞或轮数用尽后返回最后报告；普通子级失败终止运行，不自动重试。取消进入工作流，finally 释放并等待清理。没有后台编号、进程重启续跑或独立验收器，“complete”仍是工作者报告。[Ralph 使用边界](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/workflow/tool-ralph/README.md)

<a id="subagent"></a>
## 先走一次委派，再区分子任务的四个维度

父 Agent 可以让子 Agent 审阅分页边界，再整合结果。只有分工带来收益时才值得委派；多一个角色会增加传递、等待和冲突成本。

一次可理解的委派过程是：**父任务明确目标与限制 → 选择子任务的初始历史和能力 → 子任务执行并返回 → 父任务核对与整合 → 结束或保留可继续的会话。** DSH 的不同提供方在这些阶段各有实现，不能只凭“子 Agent”一个名称推断全部行为。[子任务服务][subagent]

| 维度 | 需要作出的选择 | 与其他维度的区别 |
|---|---|---|
| 历史 | 从新会话开始，还是带父会话前缀 | 不决定权限 |
| 能力 | 模型、预设、工具限制和资源权限 | 不等于复制全部父级局部状态 |
| 寿命 | 一次性返回，还是后续继续收消息 | 不由 spawn 或 fork 的名字单独决定 |
| 所有权 | 谁管理活动对象、结果与释放 | 持久会话不等于常驻进程对象 |

### 初始历史：spawn 与 fork

Spawn 从不带父会话种子的子会话开始，需要父任务明确传入背景。进程内 fork 捕获父会话截至最后一个 `turn/end` 的完整前缀；父会话没有完成过一轮时，前缀可为空。[共享驱动][driver]、[fork 提供方][fork]

例如，父会话已完成前两轮，第三轮用户刚说“只审查，不改代码”。在第三轮 fork，种子不会自动包含尚未完成的这一轮。父任务应明确传入新限制，并核对子任务权限。

> ⚠️ **fork 是快照，不是实时共享。** 父会话后续事件不自动同步。子任务答案必须来自子 Agent 自己的输出，不能把继承的父消息当成子任务已经完成的结果。

### 能力：继承组合，不等于继承全部权限

创建与冷恢复时，子 Agent 加入父 Agent 实际使用的预设组合，再安装自己的角色指导与工具限制。父级临时局部注册和限制并非全部自动复制；要让审阅子任务只读，仍需检查子作用域和底层资源权限。[子 Agent 组装][child]

进程内委派在审批能力存在时把子会话审批固定为 `never`。它表示子任务不能自行通过新审批扩大授权，不是禁止一切已允许工具，也不是继承父任务的一次性批准。需要超出范围时，应向父任务报告。

<details>
<summary>委派配置怎样捕获与恢复</summary>

模型选项优先来自父会话最近实际请求路由，尚未请求时才回退创建选项。更换模型路由但未明确推理强度，会清除旧路由的强度，让新模型解析默认值。

进程内委派在第一次异步等待前捕获显式沙箱覆盖；父级为 Auto 或 Full access 时保留相应权限预设身份，避免 fork 种子的旧身份覆盖新委派状态。相关事实追加在种子后，可由子日志重建；其他外部提供方仍需核对自身权限系统。[配置与政策源码][child]

</details>

### 寿命：会话可以保留，活动对象可以释放

One-shot（一次性）子任务产生结果后结束；continuable（可继续）子任务保留稳定身份和持久会话，后续还能接收消息。历史来源与持续寿命是两个维度，支持哪些组合取决于提供方和工具配置。[生命周期][subagent]

Activation（活跃执行实例）是在进程里实际工作的一组对象。可继续会话在需要时创建或冷恢复活动实例，空闲后可以释放；这不等于删除持久文件。当前消息授权以直接父子相邻关系为边界，不是拿到任意 Agent ID 就能跨会话发消息。

**没有正在进行的模型请求，也不一定空闲。** 实例可能有待处理消息、正在等待子任务或尚未收尾；这些活动也影响容量。对应限制仅针对特定可继续实例池，不是所有一次性与外部子任务的统一并发上限。

<details>
<summary>容量与空闲释放的具体检查</summary>

`maxActiveSubagents` 默认 8，控制连续可继续父子链中的活跃实例池。等待子任务、队列未清或正在停止的实例仍占槽位；冷恢复先取容量，给驻留子实例发消息复用槽位。容量不足接纳失败，而不是无限排队，避免父任务占槽等后代、后代却一直拿不到槽位。

释放前等待活动结束、队列清空、所属子任务收束并刷写最终状态；随后在锁内重新核对唤醒代、会话序号和队列，同步关闭新输入接纳，防止空闲判断与新消息竞争。深度、活跃数量、累计历史和 Token 成本是不同限制。[容量与收束][subagent]

</details>

### 所有权：谁负责半成品和最终收尾

启动成功返回前，创建者负责尚未发布资源，失败应清理半成品；成功交出运行句柄后，调用方承担释放责任。卸载提供方阻止后续启动，不直接撤销已接受任务。[共享驱动][driver]

释放要取消等待、停止循环、等已启动工作收束、关句柄并撤销局部注册，不是只删除一个字典项。移除活动会话也不自动删除持久化文件；当前 JSONL 服务不提供自动清理所有会话文件的保证。[存储边界][persistence]

> ⚠️ **独立 Session 不是独立操作系统或工作区。** 进程内子 Agent 不自动获得进程崩溃隔离、独立文件目录或跨文件事务；共同修改资源仍需限定范围与协调。

[← 上一章](03-skills-mcp-and-ptc.md) · [本产品目录](README.md) · [下一章 →](05-session-and-recovery.md)

[persistence]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/session/session-persistence-jsonl/README.md
[fork]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent-fork-in-process/README.md
[driver]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent-in-process-driver/README.md
[subagent]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent/README.md
[child]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/subagent/subagent/src/child-agent.ts
