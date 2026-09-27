# Codex｜固定源码与问题索引

[← Agent 资料索引](README.md) · [产品主线](../../products/agent/codex/README.md)

## 版本与使用边界

本索引对应 `openai/codex@67a709665ac7b50311b93e32612c9a8281684787`，源码观察日期为 2026-09-27。实现链接固定到该提交，安装版本、模型与配置另行记录。

第一次按产品入口的“上下文 → 工具 → 记忆 → 工程与评测”阅读。本页用稳定锚点定位机制，不用易漂移的小节序号替代学习路线。[原源码审查](../../guide/audits/codex-reader-source-review-2026-09-27.md)保留当时的阅读与验证范围；[讲解精修记录](../../guide/audits/codex-clarity-refinement-2026-09-27.md)说明本次内容迁移和实际检查，两次验证不混计。

## 按问题回读

以下源码路径均相对 `codex-rs/`。先按“阅读重点”找到入口，再沿正文附近的链接追到调用方；不是要求每个文件都从第一行读到底。

| 要核验的问题 | 正文入口 | 固定源码与阅读重点 |
|---|---|---|
| 两次模型请求怎样衔接 | [请求链](../../products/agent/codex/01-context-lifecycle.md#request-chain) | [session/turn.rs][turn]：`run_turn`，输入、采样、工具后续与停止条件 |
| 运行历史如何变成当前输入 | [历史视图](../../products/agent/codex/01-context-lifecycle.md#history-view) | [history.rs][history]：`ContextManager`；与 `run_turn` 的 `for_prompt` 对照 |
| 一次请求为何固定环境和工具 | [请求快照](../../products/agent/codex/01-context-lifecycle.md#request-snapshot) | [step_context.rs][step]：`StepContext` 字段；[turn_context.rs][turn-context]：初始与下一步设置；[parallel.rs][parallel]：调用持有快照 |
| 指令怎样刷新和继承 | [指令来源](../../products/agent/codex/01-context-lifecycle.md#instructions) | [agents_md_manager.rs][agents]：来源、缓存失效、校验、已应用快照与提供者继承 |
| 历史不完整或太长怎样处理 | [调用配对](../../products/agent/codex/01-context-lifecycle.md#paired-results)、[压缩](../../products/agent/codex/01-context-lifecycle.md#compaction) | [normalize.rs][normalize]：合成结果及稳定标识；[compact.rs][compact]：`InitialContextInjection`、替换历史与元数据 |
| 调用如何进入实现并回填 | [正常派发](../../products/agent/codex/03-tool-lifecycle.md#dispatch) | [registry.rs][registry]：载荷、前后钩子、错误与 `AnyToolResult`；[tool_executor.rs][executor]：说明与实现关联 |
| 三种暴露入口有何不同 | [可用性](../../products/agent/codex/03-tool-lifecycle.md#availability) | [tool_executor.rs][executor]：`is_direct`、`is_deferred`、`is_available_in_code_mode`；[spec_plan.rs][plan]：有效计划调整 |
| 搜索与脚本调用做了什么 | [发现与 Code Mode](../../products/agent/codex/03-tool-lifecycle.md#discovery-code-mode) | [tool_search.rs][search]：BM25、元数据与缓存；[code_mode/mod.rs][code-mode]：嵌套调用回到共同运行时 |
| Skill 怎样逐步加载 | [技能](../../products/agent/codex/03-tool-lifecycle.md#skills) | [catalog_prompt.rs][skills]：目录定位、完整 `SKILL.md` 与相关资源的读取指导 |
| 审批与沙箱如何配合 | [执行许可](../../products/agent/codex/03-tool-lifecycle.md#permissions) | [orchestrator.rs][orchestrator]：首次尝试、拒绝识别、升级条件与重新审核 |
| 并发和取消保证到哪里 | [并行与取消](../../products/agent/codex/03-tool-lifecycle.md#parallel-cancel) | [parallel.rs][parallel]：就绪等待、读写门控、取消竞争与致命传播 |
| 历史如何变成经验 | [记忆材料变化](../../products/agent/codex/02-memory-lifecycle.md#memory-example) | [phase1.rs][phase1]：领取、提取与三类结果；[write/lib.rs][write]：预算和并发配置 |
| 整理何时算成功 | [整理过程](../../products/agent/codex/02-memory-lifecycle.md#consolidation)、[权限与结束](../../products/agent/codex/02-memory-lifecycle.md#writer-permissions) | [phase2.rs][phase2]：工作区、版本、差异、产物、关闭、所有权及基线更新顺序 |
| 新任务怎样读取记忆 | [读取](../../products/agent/codex/02-memory-lifecycle.md#memory-reading) | [extension.rs][memory-ext]：贡献指令与工具；[prompts.rs][memory-prompts]：模板及截断；[tools/mod.rs][memory-tools]和[read/lib.rs][memory-lib]：参数、预算与错误 |
| 功能为何存在却没生效 | [入口与版本](../../products/agent/codex/02-memory-lifecycle.md#entry-version) | [features/lib.rs][features]：注册与默认值；[turn_processor.rs][turn-processor]：实际触发；[start.rs][start]：过滤、状态库、目录、额度、双写 |
| 哪些状态跨请求保留 | [资源与环境](../../products/agent/codex/04-engineering-evaluation.md#resources-environment) | [state/service.rs][service]：`SessionServices`；[extension.rs][memory-ext]：扩展配置与数据 |
| 写入何时可恢复读取 | [持久化](../../products/agent/codex/04-engineering-evaluation.md#persistence)、[恢复](../../products/agent/codex/04-engineering-evaluation.md#recovery) | [thread-store/store.rs][store]：`PersistContext`、`flush_thread`、关闭、丢弃与默认能力；[local/mod.rs][local]：具体介质 |
| 重试为什么不能统一计数 | [三类重试](../../products/agent/codex/04-engineering-evaluation.md#retry) | [responses_retry.rs][retry]：连接失败专门分支的完整条件与普通重试；[features/lib.rs][features]：默认值 |
| 子任务收据证明什么 | [协作](../../products/agent/codex/04-engineering-evaluation.md#collaboration) | [agent/api.rs][agent-api]：交付模式、容量预检查与通知；[agent/control.rs][agent-control]：本地实现 |
| 运行时发生与模型看见怎样区分 | [追踪](../../products/agent/codex/04-engineering-evaluation.md#trace) | [rollout-trace/README.md][trace]：事件、载荷引用、代码单元和关系；与 `parallel.rs` 调用处对照 |

## 证据分工

类型、条件和调用顺序支持固定快照的实现事实。注释与设计说明帮助理解意图，但结论冲突时要回到实际分支。正文中的任务、请求清单和材料变化用于教学，不是实际测量或统一 API Schema。

Code Mode 的核验深度是嵌套入口与共同运行时，不是完整脚本引擎审计。记忆实现以 `memories/write/src/` 为准；旧记忆概述仍含迁移前的位置，不能用旧 `core/src/memories/` 替代当前入口。

[OpenAI 的 Agent Loop 讲解](https://openai.com/index/unrolling-the-codex-agent-loop/)可帮助理解请求、工具结果与再次推理的关系；它发布于 2026-01-23，不替代本页较后固定快照的具体分支证据。[历史 Codex 索引](codex-source-index.md)保留原快照；[能力主责映射](runtime-capability-map.md)用于返回通用课程，不在产品文档重复维护跨系统幂等、租户隔离或协议标准教材。

[turn]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/turn.rs
[history]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/context_manager/history.rs
[step]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/step_context.rs
[turn-context]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/turn_context.rs
[parallel]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/parallel.rs
[agents]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/agents_md_manager.rs
[normalize]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/context_manager/normalize.rs
[compact]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/compact.rs
[registry]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/registry.rs
[executor]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/tools/src/tool_executor.rs
[plan]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/spec_plan.rs
[search]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/handlers/tool_search.rs
[code-mode]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/code_mode/mod.rs
[skills]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/skills/src/catalog_prompt.rs
[orchestrator]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/orchestrator.rs
[phase1]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/phase1.rs
[write]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/lib.rs
[phase2]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/phase2.rs
[memory-ext]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/memories/src/extension.rs
[memory-prompts]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/memories/src/prompts.rs
[memory-tools]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/memories/src/tools/mod.rs
[memory-lib]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/memories/src/lib.rs
[features]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/features/src/lib.rs
[turn-processor]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/app-server/src/request_processors/turn_processor.rs
[start]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/start.rs
[service]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/state/service.rs
[store]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/thread-store/src/store.rs
[local]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/thread-store/src/local/mod.rs
[retry]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/responses_retry.rs
[trace]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/rollout-trace/README.md
[agent-api]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/agent/api.rs
[agent-control]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/agent/control.rs
