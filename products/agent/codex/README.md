# Codex｜一项编程任务怎样持续执行

[↑ Agent 产品](../README.md) · [Agent 通用课程](../../../curriculum/09-agent/README.md) · [源码依据](../../../references/agent/codex-source-index-current.md)

用户要求修复分页错误。Codex 必须先建立线程和执行环境，把要求变成模型请求；模型提出动作后，由宿主检查、执行并回填。长命令可能跨调用运行，子任务可能稍后回报，历史还要保存、压缩和恢复。这里沿这一条任务读完主要运行模块，而不是把它们分别当作提示技巧。

## 源码边界

- 公开仓库：[openai/codex](https://github.com/openai/codex)
- 本次固定提交：[cda82a2c6853b484e0ba56d38f13902adfb2a6a1](https://github.com/openai/codex/tree/cda82a2c6853b484e0ba56d38f13902adfb2a6a1)，2026-10-01 02:07 UTC 核验默认分支
- 范围：公开客户端核心、工具与扩展、协作、历史存储及记忆流水线；不推断闭源模型和完整云端服务
- 方法：对照新旧完整 Git tree，再核对讲解涉及的源文件与变化。正文是静态源码讲解，示意记录不是实际产品运行日志

功能存在、源码默认开启、当前会话实际可用是三件事。记忆与 Multi-Agent V2 在此快照默认关闭；Code Mode、执行环境、MCP 和诊断还各有配置与能力边界，正文在机制发生处说明。已有代码环境足够阅读，无需先搭建新项目。

## 第一次按任务的发生顺序读

| 顺序 | 章节 | 这一段工作如何交给下一段 |
|---|---|---|
| 1 | [线程与输入](01-thread-and-turn.md) | 建立资源，接纳输入，固定首个请求的条件 |
| 2 | [工具与进程](02-tools-and-processes.md) | 调用通过门控、Hook 与许可，改变资源并产生结果 |
| 3 | [扩展与发现](03-extensions-and-discovery.md) | 解释工具来源、MCP 版本绑定、搜索、Code Mode 与技能 |
| 4 | [子 Agent](04-agent-collaboration.md) | 建立子任务，接纳输入，取得终态，再由父级消费 |
| 5 | [历史与恢复](05-history-and-recovery.md) | 先保存生产过程，再解释压缩、重载与真实状态核对 |
| 6 | [经验记忆](06-memory-pipeline.md) | 合格历史经提取、整理，成为后续任务可读取的材料 |
| 7 | [交付与复盘](07-delivery-and-review.md) | 将运行事件、差异和测试连成可检查的完成结论 |

```text
线程和环境就绪 → 输入接纳 → 请求快照 → 模型流
                                  ↑           ↓
                            回填工具结果 ← 受控执行
                                  ↓
                          无后续且停止检查放行
                                  ↓
                        保存与交付 → 后续恢复/经验复用
```

一条正常路径与它的重要分支放在同一章：长命令的创建、轮询、输入审核和释放一起解释；子任务的创建、回报、卸载和恢复一起解释。源码链接用于查证，理解正文不需要自己沿文件列表拼回调用链。

## 第二遍按问题回看

- 上下文：[请求视图](01-thread-and-turn.md#history-view)、[配对与压缩](05-history-and-recovery.md#paired-results)
- 执行动作：[完整调用](02-tools-and-processes.md#dispatch)、[进程寿命](02-tools-and-processes.md#process-lifetime)、[MCP](03-extensions-and-discovery.md#mcp-lifecycle)
- 持续状态：[子任务](04-agent-collaboration.md#child-lifecycle)、[持久化](05-history-and-recovery.md#persistence)、[记忆](06-memory-pipeline.md#memory-example)
- 交付与表达：[完整记录读法](07-delivery-and-review.md#execution-trace)、[回顾图与面试自测](07-delivery-and-review.md#review-map)

贯穿的分页例子沿用仓库已有题面，只用它说明“工具执行”和“结果正确”怎样分别取证；本模块不新增实验或实现要求。
