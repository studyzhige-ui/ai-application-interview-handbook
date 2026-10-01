# DeerFlow｜从 Run 归属到可靠交付

[↑ Agent 产品](../README.md) · [Agent 通用课程](../../../curriculum/09-agent/README.md) · [源码依据](../../../references/agent/deer-flow-source-index.md)

分析支付页重复提交、做最小修复且不要发布，是这里的贯穿任务。DeerFlow 先让网关确认谁拥有这次运行，再组装模型与工具；之后的子任务、检查点、交付收据和长期记忆，各有自己的完成时点。理解主线的关键是跟踪这些状态怎样交接。

## 固定源码与边界

- 公开仓库：[bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- 固定提交：[4d5607229ef1ebe8a66c9b9644b91da9082c3221](https://github.com/bytedance/deer-flow/tree/4d5607229ef1ebe8a66c9b9644b91da9082c3221)，2026-10-01 02:07 UTC 核验默认分支 main
- 讲解当前 Gateway、运行工作器与 harness 实现，不用早期深度研究工作流替代这套架构
- 本轮为静态源码核验，未执行真实模型任务或上游产品测试；示例 ID、表格和时间线用于阅读推演

默认完整产品入口是嵌入运行环境的 Gateway，LangChain/LangGraph 承担内部模型与工具图。配置类默认值不等于部署有效配置；摘要、授权、MCP、任务连续性与记忆模式在实际发生处分别说明条件。已具备代码环境即可阅读，不需要新增项目或实验。

## 第一次沿一次 Run 读

| 顺序 | 章节 | 本段交出的状态或结果 |
|---|---|---|
| 1 | [Run 准入与模型循环](01-run-and-model-loop.md) | 取得运行归属，组装状态和请求，生成受控动作 |
| 2 | [工具与执行资源](02-tools-and-resources.md) | 通过执行检查，管理文件版本、沙箱租约和结果预算 |
| 3 | [技能与 MCP](03-skills-and-mcp.md) | 发现能力，核验激活，绑定连接与当次权限 |
| 4 | [三种委派](04-native-batch-and-acp.md) | 区分原生 task、持久 batch 和 ACP 外部进程的结果与寿命 |
| 5 | [交付与连续目标](05-delivery-and-goals.md) | 保存收据、检查点与终态，随后安全续轮或清除目标 |
| 6 | [状态与恢复](06-history-and-recovery.md) | 缩短历史、物化检查点、线性恢复或建立分支 |
| 7 | [长期记忆](07-memory-pipeline.md) | 从对话筛出候选、检查提交，再按范围和预算读取 |
| 8 | [观察与复盘](08-observation-and-review.md) | 连起执行证据，区分模型停止、运行成功和业务达标 |

```text
身份与同线程准入 → Run 拥有者 → 主图：模型 ↔ 受控工具
                                      │
                         原生 task / batch / ACP
                                      ↓
                       可交付内容、产物、工具收据
                                      ↓
                  Journal 与交付收据 → 检查点 → 持久终态
                                      ↓
                  安全处理连续目标；后续恢复与记忆复用
```

## 先分清四个对象

- Thread 是持续会话身份，可以包含多次 Run
- Run 是本次运行身份，负责准入、取消、归属与终态
- ThreadState 是可继续的消息与扩展状态，检查点保存它
- ModelRequest 是一次真正发给模型的投影，不等于完整状态

图中的委派不是三种等价后台模式；状态回滚也不会自动回滚工作区和外部服务。每章先讲正常交接，再在同一过程插入失败与恢复。

## 第二遍按问题回看

- 输入与上下文：[消息变化轨迹](01-run-and-model-loop.md#run-trace)、[状态与恢复](06-history-and-recovery.md)
- 权限与资源：[先读后写](02-tools-and-resources.md#5-先读后写怎样防止基于旧文件反复修改)、[技能激活](03-skills-and-mcp.md#31-allowed-tools-的边界要读完整)
- 协作与交付：[原生 task](04-native-batch-and-acp.md#native-task)、[ACP](04-native-batch-and-acp.md#acp)、[收尾](05-delivery-and-goals.md#finalization)
- 后续工作：[连续目标](05-delivery-and-goals.md#continuous-goals)、[长期记忆](07-memory-pipeline.md)
- 复述与判断：[完整证据链](08-observation-and-review.md#complete-trace)、[综合回顾](review/README.md)
