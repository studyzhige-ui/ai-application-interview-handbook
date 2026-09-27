# Claude Code｜从一次代码任务理解完整执行过程

[↑ Agent 产品源码](../README.md) · [↑ Products](../../README.md) · [Agent 课程](../../../curriculum/09-agent/README.md) · [源码与技术资料](../../../references/agent/README.md)

Claude Code 把用户的代码任务转换成多轮模型请求与工具操作。本模块沿固定源码快照，学习程序如何组织模型可见信息、保存与召回记忆、控制工具执行，以及在中断后恢复并验证任务。

## 学习对象与版本边界

学习对象是 [`studyzhige-ui/claude-code-source-private`](https://github.com/studyzhige-ui/claude-code-source-private) 的固定快照 [`58231dcce408f805c645cfbc352d2876b517223b`](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b)。它是源码阅读用的私有镜像，尚未与某个官方发行号建立确定映射，也不代表完整、可直接构建的官方仓库。

正文用固定提交解释实现；[官方文档](https://code.claude.com/docs/en/overview)说明公开产品的使用方式。源码存在、构建包含、配置启用、当前入口调用和服务端支持，是不同条件。`feature(...)` 表示受构建开关控制的路径，不能仅凭出现函数名推导所有版本默认执行。

## 核心设计

先区分三个对象：**保存的会话记录、每次请求的模型输入、已经发生的工具操作。**

会话记录支持恢复；每轮模型输入从历史和当前材料中组装；工具操作可能改变文件或远端系统。删除一段模型历史不会撤销文件修改，恢复聊天也不会把一次外部写入重新变成尚未执行。

```text
用户输入
  ↓
交互入口 REPL / 程序化会话 QueryEngine
  ↓
query() → queryLoop()
  ↓
组织本次模型输入
  ↓
模型响应
  ├─ 提出工具请求 → 校验、授权、执行 → 结果进入后续请求
  └─ 满足结束条件 → 返回结果并处理结束事件
```

这张图表达控制关系，不代表每轮都发生压缩、记忆提取或子任务调用。实现主线见 [`queryLoop()`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts#L219-L330)。

## 阅读顺序

| 顺序 | 正文 | 读完应能独立推演 |
|---|---|---|
| 1 | [上下文生命周期](01-context-lifecycle.md) | 一条项目约定怎样进入请求，四条旧工具结果在不同条件下怎样变化 |
| 2 | [记忆生命周期](02-memory-lifecycle.md) | 一条反馈怎样保存、发现、注入后续任务，并在纠正后停止传播旧结论 |
| 3 | [工具生命周期](03-tool-lifecycle.md) | 模型输入被钩子改写后，校验、批准、执行及后续状态分别针对什么 |
| 4 | [恢复、协作与验证](04-engineering-evaluation.md) | 中断或并行工作后，怎样在同一份最终代码上确认任务完成 |

四篇沿同一个分页修复任务展开：不改变公开接口，保留原测试，报告实际验证结果。示例状态和故障条件均为教学设定，不是生产运行记录。

## 必要前提

读者需要知道：模型接收消息后生成响应；工具调用是模型提出、程序执行的请求；文件与内存变量不是同一份状态；异步取消不保证已经发生的动作回滚。

不熟悉这些概念时，先读 [Agent Loop](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) 与 [Tool Contract](../../../curriculum/09-agent/docs/04-ToolContractAndValidation.md)。正文会在使用时解释必要对象，不要求先背诵源码类名。需要实际练习调查、修改和测试时，可使用 [AI Coding 分页练习](../../../practice/coding/docs/09-ai-coding.md)。

## 使用方式

第一遍连续读正文、状态表和例子，先预测每次操作后发生什么。折叠中的容量计算、调度默认值和实现变体按需阅读，不是主线自测的隐藏前提。

第二遍隐藏章末答案，重画一次请求、一条记忆和一次工具调用的过程。关键源码链接提供固定函数或行范围，用于核对正文已经解释的分支；[源码索引](../../../references/agent/claude-code-source-index.md)提供更广的查找入口。

源码学习不要求安装镜像。真实产品实验应记录 `claude --version`、入口、模型、权限、功能配置和实际结果；源码推演与产品运行分别报告。审查范围和验证记录见 [讲解精修记录](../../../guide/audits/claude-code-clarity-refinement-2026-09-27.md)；早期修订保存在 [项目记录](../../../guide/project/claude-code-reader-revision.md)。
