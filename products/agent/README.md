# Agent 产品｜沿真实任务理解完整机制

[↑ Products](../README.md) · [Agent 通用课程](../../curriculum/09-agent/README.md) · [源码与资料](../../references/agent/README.md) · [学习路线](../../guide/learning-path.md)

通用课程把模型、工具、状态和权限分别讲清；这里回到具体产品，看一次用户任务怎样被接纳、执行、交付，失败以后又怎样继续。正文解释过程，源码提供证据，不要求读者自己从文件清单拼出系统。

## 选择一条产品主线

| 产品 | 第一次阅读的线索 | 最值得分清的边界 |
|---|---|---|
| [Codex](codex/README.md) | 线程与请求 → 受控执行 → 扩展与子任务 → 历史恢复 → 经验 → 交付 | 请求快照与当前权限；进程寿命与工具返回；日志与查询投影 |
| [Claude Code](claude-code/README.md) | 输入分流 → 流式工具循环 → 扩展与子任务 → 压缩/记忆 → 保存恢复 → SDK 结果 | 零模型命令与真实请求；参数改写与批准；后台身份与最终结果 |
| [DeepSeek Harness](deepseek-harness/README.md) | 插件组合 → Inbox 与步骤 → 文件/作业 → 计划/目标/委派 → Session 恢复 → 交付 | 默认组合与可选插件；事件日志与 Surface；同会话目标与独立尝试 |
| [DeerFlow](deer-flow/README.md) | Run 准入 → 模型与工具 → 三类委派 → 收尾/目标 → 检查点恢复 → 记忆 | 运行归属、工具收据、交付终态；原生 task、batch 与 ACP |

四款产品各用自己的连续章节，页码与 README、上下章导航一致。上下文、记忆、工具和工程是第二遍比较视角，不再限定每款必须拆成相同四篇。

## 固定版本与访问边界

- Codex：[cda82a2c6853b484e0ba56d38f13902adfb2a6a1](https://github.com/openai/codex/tree/cda82a2c6853b484e0ba56d38f13902adfb2a6a1)
- Claude Code：[58231dcce408f805c645cfbc352d2876b517223b](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b)，使用指定的私有学习源码，需访问权限，不等同官方完整公开仓库
- DeepSeek Harness：[639ed015397290b3745d163aafe02ffee4aa3f84](https://github.com/deepseek-ai/deepseek-harness/tree/639ed015397290b3745d163aafe02ffee4aa3f84)
- DeerFlow：[4d5607229ef1ebe8a66c9b9644b91da9082c3221](https://github.com/bytedance/deer-flow/tree/4d5607229ef1ebe8a66c9b9644b91da9082c3221)

三个公开仓库在 2026-10-01 02:07 UTC 核验默认分支并固定快照；后续上游变化不自动改变本页结论。源码存在、默认开启、实际部署可用分别核对。本轮没有运行真实产品、模型请求或故障实验。

## 怎样读懂，而不只是记住名称

跟踪同一任务的每一步：为什么需要它，谁给它什么，它按什么条件改变状态，结果交给谁，何时停止或转入失败恢复。读完正常路径后，再改变一个条件，例如连接目录更新、命令仍运行、子级只交部分结果、保存失败或用户刚修改目标，判断下一步。

正文保留有用的小结、面试表达、误区和自测。第一次连续读一款，第二次按产品入口的问题索引回看；不新增安装任务、项目、实验或课程进度要求。

## 第二遍做横向比较

- 请求：从哪些状态形成输入，什么时候刷新，压缩怎样保住可继续条件
- 动作：工具怎样被发现、授权、执行，结果如何回到模型，真实资源何时释放
- 后续信息：是历史恢复、规则文件、会话引用，还是独立记忆流水线
- 交付：模型停止、工具终态、持久记录和业务正确分别需要什么证据

同名能力不代表相同合同。DSH 的跨会话信息不虚构成自动记忆流水线，ACP 不借用原生子任务恢复承诺，所有恢复都要区分内部状态与外部副作用。

技术事实和源码索引见 [References](../../references/agent/README.md)；真人面试频率仍由原有市场证据决定，产品代码不增加面试样本计数。

<!-- product-inventory:start -->
## 模块范围与访问边界

- [Claude Code](claude-code/README.md)：8 篇专题正文，快照 `studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`。
- [Codex](codex/README.md)：7 篇专题正文，快照 `openai/codex@cda82a2c6853b484e0ba56d38f13902adfb2a6a1`。
- [DeepSeek Harness](deepseek-harness/README.md)：7 篇专题正文，快照 `deepseek-ai/deepseek-harness@639ed015397290b3745d163aafe02ffee4aa3f84`。
- [DeerFlow](deer-flow/README.md)：8 篇专题正文，快照 `bytedance/deer-flow@4d5607229ef1ebe8a66c9b9644b91da9082c3221`。

Claude Code 使用获授权的私人学习快照，需相应访问权限；其重建/整理范围以模块说明为准，不等同于官方完整源码。其他产品也应区分源码快照、安装版本与实际运行验证。
<!-- product-inventory:end -->
