# 扩展与发现｜能力怎样进入当前请求

[← 上一章](02-tools-and-processes.md) · [本产品目录](README.md) · [下一章 →](04-agent-collaboration.md)

前一章已经知道工具怎样执行。本章解释模型为什么能找到这个工具，以及说明、实际实现和权限依据怎样保持一致。核心工具、MCP、Code Mode 和技能都接到同一条请求与执行链上，但作用不同。

<a id="availability"></a>
## 工具存在，为什么模型本次仍可能看不到

一次调用链已经清楚后，再考虑工具从哪里来。`build_tool_router` 根据模型、环境、MCP 绑定与策略组装本次工具计划：核心工具、MCP 工具、扩展工具和动态工具可以贡献能力，模型托管能力还可能以单独规格加入。[源码：工具计划][src-plan]。

扩展是向已有流程贡献能力的组件，不需要另写一套主循环。来源接通后，还要经过注册、策略过滤和有效暴露；外部重复名称与保留名称也有处理，避免后注册的实现覆盖重要工具。[源码：注册策略与名称冲突][src-registry]。

| 状态 | 说明什么 | 还未说明什么 |
|---|---|---|
| 已注册 | 宿主能按标识找到实现 | 模型已经获得说明 |
| 已暴露 | 模型有对应使用入口 | 当前参数和资源已获授权 |
| 已获准 | 该动作可以尝试执行 | 实际执行成功 |
| 执行完成并回填 | 有对应工具结果 | 整个业务任务通过验收 |

接入多个应用后，可能有数百个工具。全部说明一起进入请求既占容量，也增加在相似名称间误选的机会。Codex 因此提供**三个独立的可见或调用入口**：首个工具列表直接提供、通过搜索发现、由 Code Mode 脚本调用。Code Mode 是模型用脚本组织工具动作的方式，下一节说明其过程。

| 源码暴露方式 | 初始列表直接可见 | 可搜索发现 | 可被嵌套 Code Mode 调用 |
|---|---|---|---|
| `Direct` | 是 | 否 | 是 |
| `DirectModelOnly` | 是 | 否 | 否 |
| `Deferred` | 否 | 是 | 是 |
| `DeferredModelOnly` | 否 | 是 | 否 |
| `CodeModeOnly` | 否 | 否 | 是 |
| `Hidden` | 否 | 否 | 否 |

表中是 `ToolExposure` 自身的三项判断；最终还受本次功能、模型与工具计划约束，“是”不是无条件启用承诺。[源码：`is_direct`、`is_deferred`、`is_available_in_code_mode`][src-executor]。

因此，`Deferred` 与 `DeferredModelOnly` 都能被搜索，但脚本调用资格不同。不能把“先搜索”和“脚本调用”合并成一个含糊的间接调用状态。

> ⚠️ **注意：隐藏是入口选择，不是安全沙箱。** 注册、暴露、授权、执行各自有职责，工具未出现在提示里不能代替实际权限限制。

<a id="discovery-code-mode"></a>
## 搜索找到说明，Code Mode 组织调用

`tool_search` 搜索延迟工具的元数据，而不是执行那些工具。固定实现用 BM25 组织名称、描述等文本的检索。BM25 是按词项匹配排序的方法；它需要工具说明准确表达用途，不应描述成必定使用向量嵌入。[源码：搜索处理与缓存][src-search]。

例如任务需要读取一个外部应用的说明，可以这样推进：

```text
搜索读取能力 → 得到候选工具及参数说明
                       ↓
               构造具体读取调用
                       ↓
               执行并查看实际内容
```

搜索命中只完成发现。实现还检查空查询、零数量等条件，并根据延迟工具集合与来源信息决定缓存是否可复用。缓存保存检索结构，不是永久忽略目录变化。

实际可用性还看模型的 `supports_search_tool`、命名空间工具条件及当前目录。旧 `ToolSearch` 功能项已是兼容空项，不再作为实际启停入口；这不等于每次请求都可以搜索所有工具。[功能注册表][src-features]、[`search_tool_enabled` 与计划调整][src-plan]。

Code Mode 改变的是调用的组织方式。逐次调用时，模型常在每次工具结果后再决定下一步；使用脚本时，可以在一个代码单元内组织若干调用和返回值处理，再把选定结果交给模型。下表仍是教学示意：

| 组织方式 | 中间过程 | 模型最后得到什么 |
|---|---|---|
| 逐次工具调用 | 调用 A、取得结果，再提出调用 B | 各次约定回填的结果 |
| Code Mode | 脚本调用 A、B，并整理返回值 | 脚本选择交出的输出，不必是所有中间值 |

在已核验路径中，嵌套调用回到 `ToolCallRuntime`，携带步骤上下文与 Code Mode 来源信息；它没有绕开工具运行边界。[嵌套入口][src-code-mode]、[共用调用运行时][src-parallel]。Code Mode 与 Code Mode Host 也是分别定义的功能项，底层宿主存在不代表当前请求已开启完整能力。[功能注册表][src-features]。

脚本可以减少某些往返，却可能隐藏更多中间结果。诊断时要分别找代码单元、嵌套调用和最终输出，见[交付章的追踪证据](07-delivery-and-review.md#trace)。

<a id="mcp-lifecycle"></a>
## MCP：发现的说明和调用的连接属于同一个版本

MCP 连接管理器启动配置中的服务器、完成能力发现，并把工具目录变成本次路由的来源。Session 持有可复用连接，StepContext 捕获 `McpBinding`：模型可见的清单、客户端、目录版本和调用权限依据一并固定。连接复用需要配置、启动/关闭状态及凭证条件仍匹配，不能看到相同服务器名字就随意复用旧连接。

模型根据目录 T1 构造调用后，执行在 T1 对应的目录快照保护下进入。若此时服务器已经更新目录，旧调用被拒绝，不会以旧参数解释新同名工具。下一次请求重新发现/捕获后，模型才能根据新说明构造调用。真正的不可逆调用准备也放在这个准入范围内，避免先造成副作用再发现目录过期。[绑定与目录检查](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/codex-mcp/src/binding.rs)

调用超时取服务器上限与调用者上限中更严格的一个；可信访问上下文准备也消耗这份时间，实际发往服务器时只剩余下预算。普通服务错误回到相应工具结果，连接生命周期与目录刷新由拥有连接的管理器处理。对已发出的远端写入，超时仍可能代表结果未知，不能把重连当作自动安全重放。[连接生命周期](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/codex-mcp/src/connection_manager.rs)

<a id="skills"></a>
## Skill 提供工作方法，不是另一种自动执行函数

工具说明告诉模型“动作是什么、参数是什么”；Skill（技能包）提供“完成一类任务应该怎样工作”的指令，还可以附带参考资料、脚本和资源。选择测试技能，不代表已经运行测试。

技能目录先提供名称、描述和来源定位。选中以后，使用指导要求完整读取该技能的 `SKILL.md`，再按任务需要读取相关资源；分页读取应继续到结束。这就是此处的 Progressive Disclosure（渐进披露）：先少量定位，再完整取得已选中的必要指令，而不是把关键指令读到一半就行动。[源码：技能目录提示][src-skills]。

来源可能是宿主文件、执行环境拥有的包、云端包或自定义资源。读取时应使用实际返回的定位信息，不能将任何来源都猜成一个本地路径。

例如，测试技能要求保留原测试、在练习目录运行、提交差异与结果；这些是工作指导。需要硬性只读时，还要让工具权限和执行环境落实限制，不能只靠一句技能文本证明写入一定被阻止。指导是否被模型遵守，需要运行证据。

### 技能来源、读取与失效是一条链

线程启动时，技能扩展保存配置与可用来源；存在本地环境会影响云端来源是否可用。配置变化更新线程状态，构造请求时再按实际选择的执行根建立宿主或执行器技能入口。目录只携带定位和说明；读全文及引用资源时必须保留它返回的包身份，不能把云端包拼成本机目录。

本快照在呈现目录前优先保留云端可见的、带插件限定名的技能；宿主目录里相同限定名的条目不再重复展示，然后再做预算处理。这个规则针对实际可见的云端限定名，不是把所有同名技能都无条件合并。环境或配置变了，要重新构造相应目录视图；上次读过一个技能，不代表本轮的另一环境拥有它的脚本或文件。[线程/步骤贡献点](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/ext/skills/src/extension.rs)、[目录去重](https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/ext/skills/src/render_dedup.rs)

<a id="extensions"></a>
## 扩展贡献能力，宿主保留同一条执行主线

记忆读取与技能能力可以参加已有流程，不必各自再造一个 Agent。以记忆扩展为例：线程启动时保存配置，更新配置时调整有效状态，构造上下文时贡献指令，条件满足时贡献工具；对应状态存入扩展数据。[扩展贡献点][src-extension]、[资源与扩展数据归属][src-service]。

```text
已有执行流程
  上下文准备时：接纳扩展提供的指令
  工具计划构建时：接纳扩展提供的能力
  仍由宿主完成请求、调用与结果处理
```

扩展可以保持职责集中，但相互作用仍要验证。例如一个扩展改写输入，另一个据此审批，顺序和最终参数就会影响安全。不能仅测试每个扩展能够加载，而忽略组合后的行为。

[← 上一章](02-tools-and-processes.md) · [本产品目录](README.md) · [下一章 →](04-agent-collaboration.md)

[src-parallel]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/tools/parallel.rs
[src-registry]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/tools/registry.rs
[src-executor]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/tools/src/tool_executor.rs
[src-plan]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/tools/spec_plan.rs
[src-search]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/tools/handlers/tool_search.rs
[src-features]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/features/src/lib.rs
[src-code-mode]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/tools/code_mode/mod.rs
[src-skills]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/ext/skills/src/catalog_prompt.rs
[src-extension]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/ext/memories/src/extension.rs
[src-service]: https://github.com/openai/codex/blob/cda82a2c6853b484e0ba56d38f13902adfb2a6a1/codex-rs/core/src/state/service.rs
