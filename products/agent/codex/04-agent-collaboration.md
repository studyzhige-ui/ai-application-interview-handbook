# 子 Agent｜从任务交接到结果回收

[← 上一章](03-extensions-and-discovery.md) · [本产品目录](README.md) · [下一章 →](05-history-and-recovery.md)

单个 Agent 已能读文件、修改和测试。子 Agent 增加的是一条有独立身份、输入队列和运行状态的任务线。父级交出一个任务以后，还必须知道谁接纳、谁运行、结果存在哪，以及何时能安全续做。

<a id="collaboration"></a>
## 先认识委派的对象与责任边界

分页练习很小，未必值得拆分。任务足够大时，可以让一个子 Agent 调查测试，另一个检查实现，但前提是工作能独立推进和验收。

`AgentControl` 协调 Agent 树，本地实现是 `LocalAgentControl` 及共享运行状态。接口处理创建子线程、输入交付、恢复加载、状态观察、中断与共享资源；这是 Rust 内部协作接口，不是已经保证所有远端语义的网络协议。[接口][src-agent-api]、[本地实现][src-agent-control]。

共享预算和容量帮助控制扩张，但轮次执行容量的预检查不预留槽位，对应本地准入与计数也不是原子预留；完成通知是尽力交付，不是已经去重的可靠消息队列。[源码：容量与通知承诺][src-agent-api]。

> ⚠️ **注意：分开上下文并不隔离同一文件。** 子 Agent 若同时写同一处，仍可能冲突；应划分修改范围，并在整合前重新读取差异和测试。本地工具门控不自动成为跨进程业务锁。

通用多 Agent 与 Multi-Agent V2 是不同功能项，该快照的 V2 并非默认开启。使用某个 V2 行为解释实际会话前，要确认配置与路径。[功能注册表][src-features]。

<a id="child-lifecycle"></a>
## 父级交出的是什么，子级返回的又是什么

先建立子线程身份及父级归属，再决定初始历史。无继承时子级从明确任务开始；全历史或截断继承时，宿主选取可继承的父级材料并过滤不应带过去的控制信息。它不是把父进程的全部内存、连接和批准对象复制一份。环境与策略有自己的继承规则；显式环境选择也要进入子级的环境快照。[创建与继承](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/spawn.rs)

子线程接纳输入以后，触发型交付才尝试开启工作；只入队型交付只是把消息留给它。运行容量控制并不等于业务任务队列的可靠投递协议。子级执行终止后，完成观察者取得状态与最终结果，尽力把终态通知放进父级队列，且不主动因此启动父级新一轮。父级消费后再核对结果，因此“子级完成”“父级收到”和“父任务验收”是三个不同时间点。[输入交付](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/delivery.rs)、[终态回报](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/completion.rs)

对审核拒绝次数过多造成的子级错误，使用明确的审核中断通知。父级应据此处理权限边界，不能把它误读成普通计算失败后换一个子级重试。

## 空闲、停止和恢复为什么需要重新检查

中断停止当前轮次，关闭/卸载运行对象释放活跃资源，持久身份和已保存记录则可能仍在。恢复不是让旧句柄继续活着，而是读取记录、重建运行对象并恢复可继续的输入状态。V2 还核对子级登记、父级归属与记录中的版本身份；不一致不能仅凭知道线程编号就接管。

恢复使用当前权限。适用的本地权限可以求安全交集；远端环境发生不兼容权限变化时，相应恢复路径拒绝。已有历史可以帮助模型继续理解任务，但不能复活此前的更宽授权。恢复链也携带历史 revision，用它判断预读取历史是否已经落后于磁盘记录。[V2 恢复和身份检查](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/spawn.rs)、[恢复运行对象](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/resume.rs)

**推演。** 子级已经写入测试结果，通知父级时失败。父级只能确认此前任务被接纳时，不能宣布成功；应读取子级状态和结果。若子级已经卸载，需按现行权限恢复或读取持久结果，而不是再创建一个子级重复所有动作。

## 关闭一棵 Agent 树，要等待哪些参与者

树级关闭先设置准入围栏，阻止共享同一个本地运行树的新启动，再向已接纳的会话与操作发关闭信号。返回关闭句柄只说明已经开始；调用它的 wait，才等待围栏前已接纳的操作和会话清理结束。放弃等待不会撤销关闭。

正在创建的子级也有成员身份。初始输入尚未接纳而创建流程被取消时，PendingSpawn 清理子线程、等待它关闭、丢弃未发布运行记录，并在任何尚未完成的 Open 边写入之后将父子边标为 Closed。清理或持久写者终止失败，会让树级等待报告错误，不用“从字典移除了”冒充释放成功。

这个围栏只覆盖同一运行树的启动；另一个顶层加载/恢复仍须由调用者在持久所有权交接时串行化。树关闭也不是子级业务完成，不应给父级发送一份伪造任务结果。[树级关闭](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/thread_manager/shutdown.rs)、[创建取消清理](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control/spawn_guard.rs)

## 面试与自测

- 一句话复述：委派建立独立任务状态，完成通知帮助交接，父级仍负责消费结果与验收
- 常见误解：不同上下文等于不同文件系统；实际上共享环境仍可能互相覆盖
- 自测：收到启动身份而没有终态结果，可以写“已完成”吗？不能；身份只定位任务，必须继续确认执行与结果

[← 上一章](03-extensions-and-discovery.md) · [本产品目录](README.md) · [下一章 →](05-history-and-recovery.md)

[src-features]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/features/src/lib.rs
[src-agent-api]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/api.rs
[src-agent-control]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/agent/control.rs
