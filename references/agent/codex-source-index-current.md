# Codex｜固定源码与问题索引

[← Agent 资料索引](README.md) · [产品主线](../../products/agent/codex/README.md)

## 版本与使用边界

本索引对应 `openai/codex@67a709665ac7b50311b93e32612c9a8281684787`，源码核验日期为 2026-09-27。链接固定到该提交，不跟随 `main` 自动变化。安装版本、模型、运行配置与实际测试结果需要另行记录；不能由源码存在推断所有部署默认启用。

正文通过具体任务解释机制；本页帮助按问题找到核验入口，不另建一套学习顺序。精确阅读范围、未执行项和证据去向见[专项审查记录](../../guide/audits/codex-reader-source-review-2026-09-27.md)。

## 按问题回读

| 想解决的问题 | 正文位置 | 关键源码 | 核验重点 |
|---|---|---|---|
| 输入如何变成连续请求 | 01 §1、§4—6 | [core/src/session/turn.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/turn.rs) | run_turn 的输入、后续与停止分支；不是一次 HTTP 请求等于一个 Turn。 |
| 单次请求为何固定条件 | 01 §3—5 | [core/src/session/step_context.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/step_context.rs) | 与 turn_context.rs、agents_md_manager.rs 对照：已捕获视图、下一步设置、刷新与权限边界。 |
| 历史怎样压缩并继续 | 01 §7—11 | [core/src/context_manager/normalize.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/context_manager/normalize.rs) | 与 history.rs、compact.rs 对照：配对、稳定标识、模型窗口与宿主事实、分阶段重注入。 |
| 开关存在是否等于启用 | 入口、02 §2、03 §4、04 §4、§9 | [features/src/lib.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/features/src/lib.rs) | 稳定性、源码默认值与会话生效条件分开；旧 tool_search 项不再承担启停。 |
| 记忆写入何时触发 | 02 §2—4 | [memories/write/src/start.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/start.rs) | 与 app-server/src/request_processors/turn_processor.rs 对照真实调用方；不能只按 startup 函数名猜时机。 |
| 提取、整理如何完成 | 02 §4—8 | [memories/write/src/phase2.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/memories/write/src/phase2.rs) | 与 phase1.rs 对照：领取、版本、工作区差异、关闭、产物校验与所有权确认。 |
| 记忆怎样按需读取 | 02 §9—11 | [ext/memories/src/extension.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/memories/src/extension.rs) | 与 prompts.rs、tools/mod.rs 对照启用条件、摘要预算、专用工具及错误分类。 |
| 工具如何发现而非立即执行 | 03 §1—4 | [core/src/tools/handlers/tool_search.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/handlers/tool_search.rs) | 与 tools/spec_plan.rs、tools/src/tool_executor.rs 对照元数据搜索、暴露表面与模型能力条件。 |
| 技能指令怎样加载 | 03 §5 | [ext/skills/src/catalog_prompt.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/ext/skills/src/catalog_prompt.rs) | 目录与完整 SKILL.md 的区别；不同来源不能全部当作宿主本地路径。 |
| 调用如何走到受控动作 | 03 §6—9、§12—13 | [core/src/tools/registry.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/registry.rs) | 与 tools/orchestrator.rs 对照钩子、参数、权限、沙箱、错误与结果；执行后拒绝不撤销副作用。 |
| 并发与取消保证到哪里 | 03 §10—11 | [core/src/tools/parallel.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/parallel.rs) | 共享门控的实际范围、就绪等待与取消结果；不推导跨系统恰好一次。 |
| 资源与子 Agent 如何归属 | 04 §1—4 | [core/src/agent/api.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/agent/api.rs) | 与 state/service.rs、agent/control.rs 对照接纳、执行、加载状态、容量与尽力通知。 |
| 何时能说写入已持久化 | 04 §7—8 | [thread-store/src/store.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/thread-store/src/store.rs) | 与 thread-store/src/local/mod.rs 对照 Standard、后台持久化条件、flush、shutdown、discard。 |
| 为什么不能说重试总有次数上限 | 04 §9 | [core/src/responses_retry.rs](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/responses_retry.rs) | 连接错误专门分支的完整条件、独立退避计数与普通重试/传输备用路径。 |
| 模型看见与运行时发生如何分开 | 04 §5、§10 | [rollout-trace/README.md](https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/rollout-trace/README.md) | 追踪设计说明与 parallel.rs 调用点；Code Mode 嵌套回流另定位 core/src/tools/code_mode/mod.rs。 |

## 阅读代码时区分三种证据

类型、条件和调用顺序可以支持固定快照的实现事实；注释与设计文档说明设计意图，但若与实现不一致，应回到具体分支；教学案例与评测方案帮助推理，不构成真实运行测量。Code Mode 在本索引的核验深度是嵌套调用入口与共同运行时，不是整套脚本引擎的完整审计。

记忆写入以 `memories/write/src/` 的实现为依据。仓库中的记忆说明文档仍含旧位置描述，不能据此把已经迁移的 `core/src/memories/` 路径写成当前执行入口。沙箱、重试、功能开关也必须检查分支条件，而非只引用开头概述。

## 历史与跨模块资料

[历史 Codex Source Index](codex-source-index.md)保留其原有快照，不作为本页版本的实现证据。[能力主责映射](runtime-capability-map.md)定位通用课程；本产品文档不为外部消息幂等、SaaS 租户隔离或协议标准另行维护一套教材。
