# 03｜工具：从可发现能力到受控副作用

[← 记忆](02-memory-lifecycle.md) · [DeerFlow 总览](README.md) · [下一篇：工程与评测 →](04-engineering-evaluation.md)

用户让智能体查询监控、修复支付页，但不要发布。模型提出 `write_file` 调用后，事情还没有发生：程序需要检查目标文件、权限和执行环境，工具真正返回后，模型才获得新的观察。

同样，配置了一个发布工具，不代表本轮模型应该看见它；模型看见了，也不代表这次调用获准执行。读 DeerFlow 工具源码，先把**存在、可见、允许执行和实际完成**四个状态拆开。

## 1. 工具怎样进入这次运行

`get_available_tools` 汇合配置工具、内建工具、MCP 工具、ACP 外部智能体工具和插件贡献。MCP（模型上下文协议）在这里用于标准化接入外部能力；ACP（Agent Client Protocol，智能体客户端协议）工具则把一个外部智能体封装为可调用能力，不能与本地原生子任务直接画等号。

并不是所有工具都由这个函数一次性加入。主智能体组装还会按条件追加记忆、项目文档和任务连续性等工具。因此要追“本次到底有哪些工具”，需要读工具汇合函数，也要读调用它的工厂。[候选工具汇合](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/tools.py#L104-L330) · [项目工具追加](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py#L185-L218)

### 1.1 配置名字、模型说明与执行名字必须对齐

工具说明包括名字、参数结构和用途，模型据此选择调用；程序按实际工具对象的名字执行。配置中的名字与 `BaseTool.name` 不一致时，该实现会警告，并以实际名字绑定，不能误写成“一发现不同就拒绝启动”。同名候选会按实现的优先次序去重，不能让模型收到含义不确定的重复说明。

视觉工具只在模型声明支持视觉时加入。`write_file` 的描述也可能根据**已构造模型的实际输出上限**附上写入长度提示；组装器复制工具后修改描述，避免把一个模型的预算写到共享单例，污染另一模型。这种字符数提示是启发式换算，不是每种语言都精确成立的 token 计数。[身份、去重与描述生成](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/tools.py#L149-L330)

### 1.2 本地沙箱的名字不等于安全隔离

`LocalSandboxProvider` 在宿主环境执行，本身不是安全隔离边界。DeerFlow 默认隐藏这条模式下的宿主 Bash，只有明确允许才暴露；这不是“已经有一条安全的本地 Sandbox Bash，因此去掉多余 Host Bash”。

允许执行命令之前，必须明确它会落在哪个环境、能接触哪些文件和网络。AIO、E2B、OpenSandbox 等提供者具有各自实现与限制，换提供者不能自动推导所有安全和持久语义不变。[本地 Bash 门控](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/sandbox/security.py)

## 2. 工具很多时，为什么先给索引，再给完整说明

假设 MCP 工具很多，而用户只需要查询支付错误。每次都把所有参数结构塞进模型输入，会占用本可用于任务和证据的空间。DeerFlow 的延迟发现机制保留执行端的工具注册，却暂时隐藏未展开工具的完整说明。

```text
组装：执行端注册 MCP 工具
   │
   ├─ 模型先得到有界的发现入口和目录信息
   │
   ▼
tool_search 或基于路由提示的自动展开
   │
   ▼
ThreadState.promoted 记录本目录下已展开的名字
   │
   ▼
下一次请求加入相应完整工具说明
   │
   ▼
真正调用时，仍检查发现状态和独立授权
```

这里的 promotion 可以理解为“从目录项展开成可使用的工具定义”，不是给用户授予业务权限。`tool_search` 支持精确选名、限定名字关键词等检索方式；自动路由读取当前用户请求，按路由元数据展开少量相关工具，本身不执行业务操作。[发现实现](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/builtins/tool_search.py) · [自动路由](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/mcp_routing_middleware.py)

### 2.1 为什么展开状态还要记目录哈希

假设历史记录说工具 `monitor_search` 已展开，但服务器更新了这个名字对应的参数与含义。不能仅因名字一样，就沿用旧状态。

目录哈希用来标识一组工具定义。下面是该快照的实际状态合并函数，连同所需类型一起保留。输入是旧展开状态和新状态；返回新状态，代码本身不执行工具，不访问模型。

<!-- source-example: promoted_tools -->
```python
from typing import TypedDict


class PromotedTools(TypedDict):
    catalog_hash: str
    names: list[str]


def merge_promoted(existing: PromotedTools | None, new: PromotedTools | None) -> PromotedTools | None:
    """Reducer for deferred-tool promotions, scoped by catalog hash.

    - new None/empty -> preserve existing (node didn't touch promotions).
    - catalog_hash changed -> replace wholesale, dropping stale names (prevents a
      persisted bare name from exposing a different tool after catalog drift).
    - same catalog_hash -> union names, dedupe, preserve order.
    """
    if not new:
        return existing
    if existing is None or existing.get("catalog_hash") != new["catalog_hash"]:
        return {
            "catalog_hash": new["catalog_hash"],
            "names": list(dict.fromkeys(new["names"])),
        }
    return {
        "catalog_hash": existing["catalog_hash"],
        "names": list(dict.fromkeys(existing["names"] + new["names"])),
    }
```

旧值是 `{"catalog_hash":"A","names":["search"]}`，新值是 `{"catalog_hash":"A","names":["search","read"]}` 时，得到 A 目录下的 `search, read`。新值若属于 B 目录且只有 `export`，则只保留 B 的 `export`，不会把 A 的 `search` 带过去。传入 `None` 表示不更新，会返回原对象；不要误认成“清空工具”。[原类型与合并函数](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py#L139-L163)

这只是状态合并。执行时，`DeferredToolFilterMiddleware` 还会检查状态中的哈希是否匹配当前目录。即使模型从历史猜到了一个未展开工具名，也会收到错误消息，而不是绕过发现路径直接执行。[可见性与执行双检查](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/deferred_tool_filter_middleware.py)

## 3. Skill 提供做事方法，但不能自行创造权限

Skill（技能）通常是一份 `SKILL.md` 加相关资源。目录先告诉模型技能的名字、用途和位置，详细正文及资源按需要读取。它与 Tool 的关系不是两个同义词：技能可以教模型怎样组合工具，工具才由程序实际执行。

启用或安装一个技能，只代表它可以被发现。用户显式 `/skill-name`，或模型实际读取了技能文件，才形成对应的激活依据。显式选择由 `SkillActivationMiddleware` 加载技能正文；被动读取则通过工具结果中的可靠来源信息捕获引用，不相信外部工具自己伪造“技能已读”标记。[激活与策略](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/skill_tool_policy_middleware.py#L37-L179) · [技能读取来源标记](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L97-L165)

### 3.1 allowed-tools 的边界要读完整

技能可声明 `allowed-tools`，限制允许的工具。该快照有几条不能省略的分支：

| 条件 | 技能策略的结果 |
|---|---|
| 没有激活技能，或激活集合都未声明 allowed-tools | 保留该层的兼容性不限工具行为；其他授权照常生效 |
| 至少一个激活技能有明确声明 | 合并明确声明；未声明的技能不会抹掉已有约束 |
| 用户本轮显式 slash 激活技能 | 该策略优先，随后被动读第二个技能不能扩大它 |
| 活动引用存在但无法解析或授权 | 该层降到框架保留工具集合，而不是开放全部工具 |

多个被动激活技能的明确声明采用并集，不是默认为交集。`read_file`、`describe_skill`、`review_skill_package`、`tool_search` 是该技能策略的保留工具；“保留”不意味着绕过沙箱或其他授权读取任意资源。[声明合并规则](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/skills/tool_policy.py) · [活动策略解析](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/skill_tool_policy_middleware.py#L79-L221)

技能策略既过滤模型看到的工具，也在真正调用时检查。连 `tool_search` 返回的参数说明与展开名字也需过滤；否则发现入口就可能把被禁止的工具重新带回来。某一模型请求形成的决策带有组装实例的归属标记，不能仅凭客户端同名字段或过期缓存冒充有效策略。

> ⚠️ **提示中的限制不是执行授权。** “不要发布”写进技能可以帮助模型规划，但危险工具仍需要程序侧限制。反过来，把用户编写的全部技能内容提升成系统指令，也不等于正确的安全设计。

### 3.2 Secret 绑定的是这次请求，不是技能永久拥有宿主环境

技能可以声明需要哪些 Secret（秘密凭证）。实际值由本次请求运行上下文提供，激活路径根据技能启用状态、允许列表、显式或自主激活规则等筛选。不能因为磁盘上存在某个技能，就把宿主进程所有环境变量交给它。

凭证名可以用于诊断缺少哪项配置；凭证值不应写入普通审计文本。技能更新、停用或当前请求没有提供相应凭证时，不能沿用一次历史激活永久获得的权限。[激活与秘密绑定](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/skill_activation_middleware.py)

## 4. 从一个调用提议到真实执行，要经过哪些检查

以“修改现有支付页文件”为例，模型先产生工具名和参数，随后才进入包装链。各层回答不同的问题：

| 层次 | 它要确认什么 |
|---|---|
| 参数与业务输入 | 参数可解析吗，目标和操作是否有意义 |
| 发现与技能限制 | 这个工具已展开吗，当前技能允许吗 |
| 产品授权与护栏 | 当前身份可使用这项能力吗，策略是否拒绝 |
| 沙箱与路径 | 操作实际发生在哪，能接触什么资源 |
| 文件新鲜度 | 修改现有文件之前，模型是否看过当前版本 |
| 结果规范化与收据 | 发生了什么，怎样让下一轮模型与产品记录理解它 |

这是职责表，不是伪造一条全部组件都必经的固定线性顺序。实际安装取决于配置；外层可以提前拒绝，后面的工具正文根本不会运行。授权提供者通过适配器复用 GuardrailMiddleware 的拒绝和错误语义，执行护栏与沙箱边界仍是独立责任。[真实构建顺序](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L202-L420)

## 5. 先读后写怎样防止基于旧文件反复修改

假设文件内容为版本 A，模型先 `read_file`，工具结果上记下当前完整内容的 SHA-256。稍后准备 `write_file` 或 `str_replace` 时，门控重新检查文件哈希：如果仍是 A，可以继续；若被其他调用改成 B，旧标记失效，模型需要重读。

一次写入不会替模型刷新“已经读过”标记。成功写入改变内容后，下一次修改需要重新读取；如果写入后字节完全相同，哈希未变，不能把这条规则夸大为“任何写调用无条件废除全部标记”。部分区间读取也可以记录当前文件版本，这不表示模型已经理解整份文件的每一行。[检查与标记](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py#L291-L419)

### 5.1 两个并发写为什么还需要锁

同一条模型响应可以包含多个工具调用。如果两个修改都先检查 A，然后同时写入，就算每个检查单独正确，整体也会失去保护。DeerFlow 用同一作用域、规范化路径的锁覆盖检查和执行，读取与标记也在相同保护下进行。

但这个锁是进程内机制，且只覆盖接入它的工具路径。它不是任意编辑器、外部进程或其他宿主写入者共同遵守的分布式文件事务。不能据此宣称并行智能体永远不会丢更新。[锁与异步取消处理](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py#L97-L289)

### 5.2 这道门不是普遍的 fail-closed 安全边界

| 检查时发生的情况 | 该门控的实际处理 |
|---|---|
| 文件存在且可检查，缺少当前版本读取标记 | 返回错误，不进入写工具正文 |
| 文件不存在 | 放行，创建或替换是否可行由工具判断 |
| 普通检查故障，或返回 `Error:` 等无法检查内容 | fail-open：放行，让工具产生自己的结果或错误 |
| 沙箱授权明确拒绝 | 返回授权错误，不把它混成可放行检查故障 |

因此“DeerFlow 修改任何文件都必须先读，否则绝不执行”是错误概括。这是有具体适用条件的新鲜度护栏，不能替代授权和隔离。被该门确实拦住的大写入参数，会在后续模型视图中省去；保存的原参数仍留作相应证据，但不得把未执行写入表述成文件已经改变。[实际分支](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py#L291-L378)

## 6. 沙箱是需要管理的资源，不是每次调用的装饰对象

沙箱中间件负责获取、复用和释放执行环境，状态保存标识，不保存不可序列化的提供者对象。默认 `lazy_init=True` 时，普通共享视图可以推迟到工具调用才实际获取；需要策略范围内的技能文件投影时，可能提前取得环境，防止旧的宽权限视图沿检查点继续使用。

并发主智能体与子智能体分别持有执行租约。一个子任务结束，不能关闭其他子任务仍在使用的沙箱。最后持有者释放可以把远程环境放回暖池，提供者关闭才是另一层最终清理；release 不一定等于销毁容器或删除所有文件。[沙箱生命周期](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/sandbox/middleware.py#L51-L240)

取消时，还要等待已交给工作线程的同步文件或命令操作结束，再释放其持有资源。取消等待者不会自动杀掉那个线程；过早释放会让“已终止”子任务继续使用失效环境。租约只解决资源所有权，不会自动撤销命令已产生的副作用。

## 7. MCP 会话为什么要有明确的所有者

查询无状态接口可以每次重新连接，但浏览器类 MCP 服务可能把已打开页面保存在会话里。第二次“点击”若连到新会话，就找不到第一次打开的页面。

池化路径用服务器、用户与线程作用域，以及拥有它的事件循环共同标识连接。同一事件循环的连续调用可以复用服务端状态；不同循环使用不同会话。该快照的同步包装每次运行新的事件循环，因此不能承诺同步工具调用间仍保留浏览器状态。[会话池边界](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/session_pool.py#L1-L37)

### 7.1 为什么创建和关闭都交给同一个任务

MCP ClientSession 使用的异步上下文有任务归属要求：进入与退出取消作用域需要由同一任务完成。让调用 A 创建、调用 B 直接执行退出，可能触发运行错误。

DeerFlow 为连接建立专门的 owner task（拥有者任务）：进入上下文、初始化、把连接登记到池，然后等待关闭信号，最后由自己退出。其他调用者借用会话或发出关闭信号，不接管其退出动作。初始化完成与登记入池在同一临界区内完成，因此返回成功连接时，它已经有人负责回收。[拥有者任务](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/session_pool.py#L162-L230)

同一个键并发创建时，共享尚未完成的创建结果，避免重复连接；池按容量淘汰，旧连接退出时还要确认自己仍是当前项，不能误删后来替换的新连接。检测到明确传输断开时，会清理对应连接并抛出原错误；这不是无条件重放可能有副作用的工具调用。[调用与断连](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/session_pool.py#L104-L157)

### 7.2 外部工具生成的文件也要接回工作区

stdio MCP 子进程可能输出截图、导出文件等。桥接路径会处理工作目录、临时目录及虚拟路径，尽量让输出进入线程可访问的数据树；已有明确环境配置与不同服务行为仍需按实现核对，不能把这些默认安排说成能强制任意 MCP Server 的全部输出位置。

从外部返回一个宿主路径，到模型能够 `read_file`、前端能够访问产物，中间还有路径映射、权限与文件存在性。路径字符串看起来正确并不足够。[MCP 工具桥接](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/tools.py)

## 8. 工具返回后，观察、证据与任务成功仍然不同

普通执行异常会被 `ToolErrorHandlingMiddleware` 转成带对应调用 ID 的错误 `ToolMessage`，模型可以修正参数或换路径。LangGraph 的暂停等控制流要继续传播，不能包装成普通业务错误。取消也不能被通用重试吞掉。[错误与控制流](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L64-L201)

ToolMessage 告诉模型“观察到了什么”；Tool Receipt（工具收据）记录某次执行的身份、参数和结果证据；Run Journal 则把相应事件接入产品历史。这些是不同表示，不能保证每处都保存完全相同的全文。外层收据要能看到被策略提前拒绝的结果，否则日志中会缺少一次真实拒绝。[收据安装位置](https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py#L270-L390)

大结果之后还可能被外置或裁剪。对于已经成功的外部动作，回填超时也不能证明动作没发生；重新执行之前应核对实际状态，必要时依赖业务幂等或补偿。这是工程设计要求，不是声明所有 DeerFlow 工具已经具备统一的外部幂等保证。

`task` 从父模型看也是工具，但它启动一套独立子智能体执行。父级工具返回中的“子任务完成”还需结合停止原因、收据和验收条件判断；详细的上下文隔离、容量与持久批任务在工程篇统一建立，不把 ToolMessage 的文字当最终完成证明。

## 本章小结

工具生命周期包括能力组装、按需展开、策略限制、实际执行和结果回填。DeerFlow 将模型可见性与执行检查同时落在程序中，又为文件新鲜度、沙箱和 MCP 会话分别管理边界。理解它的关键是每一层实际保证什么，尤其不要把发现当授权、把资源释放当副作用回滚、把收据当业务验收。

## 🎯 面试怎么回答

**Q：Skill 或 MCP 数量太多，怎样避免上下文膨胀？**

> 我会分开能力目录、完整说明和真实执行。DeerFlow 可先保留目录入口，让工具搜索或路由按需展开 MCP 定义，技能正文也按需加载。展开状态关联目录哈希，避免升级后沿用旧定义。但缩短说明不是安全措施的全部：真正调用时仍检查展开状态、技能限制、授权和沙箱，搜索返回本身也不能恢复被禁止的工具。

**Q：修改前强制读文件，能解决并发与安全问题吗？**

> 它能减少基于旧内容的重复修改。DeerFlow 将读取标记放在工具消息中，用内容哈希检查新鲜度，再用进程内锁覆盖门控和执行。但它只覆盖特定工具和接入路径，普通检查失败还有放行分支；因此不是跨进程文件事务，更不是完整安全隔离。权限、路径、外部写入者以及最终文件验证仍需分别考虑。

## ⚠️ 高频易错点

- **只隐藏说明，不检查执行。** 模型仍可能从历史或猜测中得到工具名。
- **把激活技能的并集说成交集。** slash 优先、显式声明并集和框架保留工具都要按该版本解释。
- **把 LocalSandbox 当成容器安全边界。** 名字里有 sandbox 不代表宿主命令已隔离。
- **把重连当成安全重试。** 接口断开不证明外部动作尚未发生。

## 本章自测

**任务 A：** 旧展开状态属于目录 A，包含 `read`；新状态属于 B，只包含 `export`。预测函数返回值，再判断“export 已展开但技能只允许 read”时能否执行。第一问检查状态，第二问必须明确是哪一层拒绝。

<details>
<summary>任务 A 提示</summary>

先运行合并函数，再把 DeferredToolFilter 与 SkillToolPolicy 分开判断。

</details>
<details>
<summary>任务 A 答案与解释</summary>

新状态只保留 B 的 `export`，A 的旧名字不继承。展开只满足发现条件；技能策略不允许 `export`，因此可见性和执行阶段仍应拒绝它。不能因合并函数返回了名字就断言工具能够执行。

</details>

**任务 B：** 现有文件没有读取标记，但门控读取时出现普通 I/O 故障，未发生 SandboxAuthorizationError。工具正文尚未调用。请预测门控结果，说明什么仍未知，并给出需要核对的后续证据。

<details>
<summary>任务 B 提示</summary>

区分“确认文件存在且未读”和“无法检查文件”两个分支。

</details>
<details>
<summary>任务 B 答案与解释</summary>

按该实现的普通检查失败分支放行，随后由工具执行并给出结果。此时不能说已写成，也不能说被新鲜度门拦住。还要检查工具结果、收据以及目标文件；实际授权仍由对应层决定。

</details>

下一篇：[04｜工程与评测 →](04-engineering-evaluation.md)
