# Agent Harness / Runtime 权威实现参考

本项目的 Agent 模块不以单一框架教程为最高标准，而优先研究成熟 Agent 产品的真实实现。

## 一级参考

### Claude Code

仓库：`studyzhige-ui/claude-code-source-private`（私有）

当前已确认仓库包含顶层 `Tool.ts`、`QueryEngine.ts`、`Task.ts`、`context.ts`，以及 `assistant/`、`bootstrap/`、`bridge/`、`commands/`、`components/`、`context/` 等目录。后续会围绕 Harness / Runtime 主题继续定向追踪实际代码路径。

### OpenAI Codex

仓库：`openai/codex`

当前源码检索已明确发现以下实现主题：

- Core 中存在 compact / remote compact 相关模块。
- 配置中存在 `model_context_window` 与自动 compact token 阈值。
- TUI 中存在 Memory 与 MCP 的显式命令入口。
- Core / Protocol 中有 MCP tool、动态工具响应和权限相关类型。
- 配置层存在 sandbox mode；协议/会话层包含 sandbox 与 permission profile。
- App server protocol 中存在 Pre/Post Tool Use、PreCompact 等 Hook 相关配置。

这些只是源码导航结果，不直接等价于最终课程结论。后续每个 Agent 章节会继续读取具体实现文件，再抽象出稳定原理。

## 课程设计原则

Agent Harness 模块后续至少要覆盖：

1. Agent Runtime 生命周期
2. Session / Turn / State
3. Prompt 与上下文构建
4. Context Window 与 Compaction
5. Tool Registry / Tool Schema / Tool Execution
6. Tool Result 与错误传播
7. Permission / Approval
8. Sandbox / Filesystem / Command Execution 边界
9. MCP 与外部能力接入
10. Skills / Commands / Reusable capability
11. Task / Subagent / Orchestration
12. Async / Streaming / Cancellation
13. Retry / Timeout / Idempotency / Recovery
14. Hooks / Extensibility
15. Memory / Persistence
16. Observability / Logs / Tracing / Rollout
17. Evaluation
18. Security / Prompt Injection / Secret Boundary
19. Human-in-the-loop
20. Production deployment & resource control

> 真实面经负责校准“企业正在追问哪些部分”；Claude Code 与 Codex 源码负责校准“成熟 Agent 产品实际上需要哪些 Harness / Runtime 能力”。
