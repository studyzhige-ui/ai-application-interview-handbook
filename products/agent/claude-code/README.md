# Claude Code｜从一次代码任务理解完整执行过程

[↑ Agent 产品源码](../README.md) · [↑ Products](../../README.md) · [Agent 课程](../../../curriculum/09-agent/README.md) · [源码与技术资料](../../../references/agent/README.md)

Claude Code 把用户的代码任务转换成多轮模型请求与工具操作。本模块沿固定源码快照，学习程序如何组织模型可见信息、保存与召回记忆、控制工具执行，以及在中断后恢复任务。

## 学习对象与版本边界

学习对象是 [`studyzhige-ui/claude-code-source-private`](https://github.com/studyzhige-ui/claude-code-source-private) 的固定快照 [`58231dcce408f805c645cfbc352d2876b517223b`](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b)。它是用于源码阅读的私有镜像，不在本文中等同于某个已确认的官方发行版本，也不代表完整、可直接构建的官方仓库。

正文引用固定提交解释实现；[官方文档](https://code.claude.com/docs/en/overview)说明公开产品的使用方式。两者不能跨版本拼成同一套实现。出现 `feature(...)` 时，表示这条路径受构建功能开关控制；还需要区分配置是否启用、当前入口是否调用，以及服务端是否支持。

## 核心设计

理解这套实现，先区分三个对象：**保存的会话记录、每次请求的模型输入，以及已经发生的工具操作。** 它们有关联，但不是同一份状态。

会话记录支持恢复。每轮模型输入是在历史上经过筛选、结果替换、必要压缩和协议整理形成的视图。工具操作则可能改变文件或远端系统；删除一段模型历史不会撤销文件修改，恢复会话也不会让一次外部写入重新变成“尚未执行”。

```text
用户输入
   │
   ├─ 交互入口：REPL（终端交互界面）
   └─ 程序入口：QueryEngine（会话查询管理器）
                    │
                 query()
                    │
          为本次请求组织模型输入
                    │
                 模型响应
                    │
           ┌────────┴─────────┐
      需要调用工具          可以结束本轮
           │                    │
    校验、权限与实际执行      返回结果并处理结束事件
           │
      结果进入后续历史
           │
       下一次循环迭代
```

这张图展示控制关系，不代表所有入口都经过同一个界面，也不代表每轮都发生压缩、记忆提取或子智能体调用。具体状态转移以 [`query.ts`](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts) 为主线。

## 阅读顺序

| 顺序 | 正文 | 读完要能解释的问题 |
|---|---|---|
| 1 | [上下文生命周期](01-context-lifecycle.md) | 程序保存了什么，模型实际看见什么；压缩改变了哪一层？ |
| 2 | [记忆生命周期](02-memory-lifecycle.md) | 哪些信息值得跨会话保存，怎样写入、召回、纠正与删除？ |
| 3 | [工具生命周期](03-tool-lifecycle.md) | 从发现工具到确认动作完成，中间有哪些相互独立的检查？ |
| 4 | [恢复、协作与验证](04-engineering-evaluation.md) | 发生中断、重试或多智能体协作后，怎样恢复并证明任务做对？ |

四篇沿同一个教学任务展开：修复一个分页函数，保持公开接口不变，保留原测试，并说明实际验证结果。示例状态和故障条件均为教学设定，不是 Claude Code 的生产运行记录。

## 必要前提

读者需要知道：模型接收消息后生成响应；工具调用是模型提出的结构化请求，由程序执行；文件内容与内存变量不是同一份状态；异步任务发出取消请求后，不一定立即停止。

这些概念尚不熟悉时，可先读 [Agent Loop](../../../curriculum/09-agent/docs/03-AgentLoopAndExecutionScopes.md) 与 [Tool Contract](../../../curriculum/09-agent/docs/04-ToolContractAndValidation.md)。正文仍会在使用时建立最小模型，不要求先背诵源码类名。若希望先体验调查、修复和验证的完整任务，可使用 [AI Coding 分页练习](../../../practice/coding/docs/09-ai-coding.md)。

## 使用方式

第一遍先跟随正文中的具体对象和状态变化，源码链接用来核对关键分支，不必按目录逐文件阅读。第二遍隐藏章末答案，画出一次请求、一次记忆写入和一次工具调用经过的状态，再用自测里的新条件检验理解。

源码阅读任务不要求安装这个镜像。真实产品实验则必须记录 `claude --version`、使用入口、模型、权限模式、功能开关与实际结果；没有运行就不能把源码推演写成实验通过。完整实验条件、证据范围与维护事项见[模块修订记录](../../../guide/project/claude-code-reader-revision.md)。
